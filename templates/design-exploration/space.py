"""读取设计空间，核对配置并枚举符合编码约束的组合。"""

import json
from dataclasses import dataclass
from itertools import product
from math import prod
from pathlib import Path
from typing import Any

Recipe = tuple[str, ...]
Pattern = dict[str, str]
MAX_COMBINATIONS = 50_000


@dataclass(frozen=True)
class Axis:
    id: str
    label: str
    kind: str
    source: str
    options: tuple[str, ...]


@dataclass(frozen=True)
class Group:
    id: str
    purpose: str
    minimum: int
    patterns: tuple[Pattern, ...]
    min_changes: int


@dataclass(frozen=True)
class Space:
    config: dict[str, Any]
    axes: tuple[Axis, ...]
    baseline: Recipe
    exclusions: tuple[tuple[Pattern, str], ...]
    groups: tuple[Group, ...]

    @property
    def focus_indices(self) -> tuple[int, ...]:
        kind = "core" if self.config["scope"] == "structure" else "visual"
        return tuple(i for i, axis in enumerate(self.axes) if axis.kind == kind)


def _text(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("名称、来源和原因必须是非空字符串")
    return value


def _count(value: Any, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"数量必须是大于等于 {minimum} 的整数")
    return value


def _axis(raw: dict[str, Any]) -> Axis:
    if not isinstance(raw["options"], list):
        raise TypeError("维度 options 必须是选项列表")
    options = tuple(_text(value) for value in raw["options"])
    if not options or len(options) != len(set(options)):
        raise ValueError("维度选项不能为空或重复")
    if raw["kind"] not in ("core", "visual"):
        raise ValueError("维度 kind 只能为 core 或 visual")
    return Axis(
        _text(raw["id"]),
        _text(raw["label"]),
        raw["kind"],
        _text(raw["source"]),
        options,
    )


def _pattern(raw: Pattern, axes: tuple[Axis, ...]) -> Pattern:
    if not isinstance(raw, dict):
        raise TypeError("组合条件必须是对象")
    options = {axis.id: axis.options for axis in axes}
    for key, value in raw.items():
        if key not in options or value not in options[key]:
            raise ValueError(f"组合条件包含未知维度或选项：{key}")
    return raw


def _group(raw: dict[str, Any], axes: tuple[Axis, ...], focus_size: int) -> Group:
    group_id = _text(raw["id"])
    if group_id in ("baseline", "coverage"):
        raise ValueError("baseline 和 coverage 是保留的分组名称")
    patterns = tuple(_pattern(item, axes) for item in raw["patterns"])
    if not patterns:
        raise ValueError("分组必须提供至少一个匹配条件，空对象表示不限选项")
    changes = _count(raw.get("min_changes", 0))
    if changes > focus_size:
        raise ValueError("min_changes 超过本轮比较的维度数")
    return Group(
        group_id,
        _text(raw["purpose"]),
        _count(raw["minimum"], 1),
        patterns,
        changes,
    )


def load_space(path: Path) -> Space:
    """读取配置；文字约束仍需人工审查，工具只执行编码排除条件。"""
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    if config["schema_version"] != 1:
        raise ValueError("仅支持 schema_version=1")
    if config["scope"] not in ("structure", "visual"):
        raise ValueError("scope 只能为 structure 或 visual")
    _text(config["task"])
    if not isinstance(config["constraints"], list):
        raise TypeError("constraints 必须是文字约束列表")
    for constraint in config["constraints"]:
        _text(constraint)
    axes = tuple(_axis(item) for item in config["axes"])
    ids = {axis.id for axis in axes}
    if not axes or len(ids) != len(axes):
        raise ValueError("维度不能为空，维度标识不得重复")
    baseline = _pattern(config["baseline"], axes)
    if set(baseline) != ids:
        raise ValueError("baseline 必须给出所有维度的选项")
    exclusions = tuple(
        (_pattern(item["match"], axes), _text(item["reason"]))
        for item in config["exclusions"]
    )
    if any(not pattern for pattern, _ in exclusions):
        raise ValueError("排除条件不能为空对象")
    focus_kind = "core" if config["scope"] == "structure" else "visual"
    focus_size = sum(axis.kind == focus_kind for axis in axes)
    if not focus_size:
        raise ValueError(f"本轮至少需要一个 {focus_kind} 维度")
    groups = tuple(_group(item, axes, focus_size) for item in config["groups"])
    if len({group.id for group in groups}) != len(groups):
        raise ValueError("探索分组标识不得重复")
    return Space(
        config,
        axes,
        tuple(baseline[axis.id] for axis in axes),
        exclusions,
        groups,
    )


def matches(recipe: Recipe, pattern: Pattern, axes: tuple[Axis, ...]) -> bool:
    """条件中的维度全部满足时命中；未指定的维度不受限制。"""
    return all(
        pattern.get(axis.id, value) == value for axis, value in zip(axes, recipe)
    )


def enumerate_recipes(space: Space) -> tuple[list[Recipe], dict[str, int]]:
    """返回允许组合及排除原因计数；同一组合可命中多个排除原因。"""
    if prod(len(axis.options) for axis in space.axes) > MAX_COMBINATIONS:
        raise ValueError("组合数超过 50000，请缩小本轮空间或分轮探索")
    allowed = []
    excluded = dict.fromkeys((reason for _, reason in space.exclusions), 0)
    for recipe in product(*(axis.options for axis in space.axes)):
        reasons = [
            reason
            for pattern, reason in space.exclusions
            if matches(recipe, pattern, space.axes)
        ]
        if reasons:
            for reason in reasons:
                excluded[reason] += 1
        else:
            allowed.append(recipe)
    if space.baseline not in allowed:
        raise ValueError("基准组合违反编码排除条件，请先修正配置")
    return allowed, excluded
