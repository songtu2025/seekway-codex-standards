"""安排设计方向覆盖，输出可复核的采样记录，不评价设计质量。"""

import argparse
import hashlib
import json
import platform
import random
import sys
from collections import Counter
from io import TextIOWrapper
from pathlib import Path
from typing import Any, cast

from space import Recipe, Space, enumerate_recipes, load_space, matches

TOOL_VERSION = "1.0.0"
# 距离矩阵随候选数平方增长，较大的探索应分轮进行。
MAX_CANDIDATES = 200


def encoded_distance(left: Recipe, right: Recipe, indices: tuple[int, ...]) -> int:
    """只统计不同的编码选项数，不推断真实体验差异。"""
    return sum(left[i] != right[i] for i in indices)


def reserve_groups(
    space: Space,
    pool: list[Recipe],
    rng: random.Random,
) -> tuple[list[tuple[str, Recipe]], list[dict[str, Any]]]:
    """通过组合与配额的匹配安排分组，避免重叠分组相互抢占候选。"""
    eligible = {}
    for group in space.groups:
        eligible[group.id] = [
            recipe
            for recipe in pool
            if recipe != space.baseline
            and encoded_distance(recipe, space.baseline, space.focus_indices)
            >= group.min_changes
            and any(matches(recipe, pattern, space.axes) for pattern in group.patterns)
        ]
        rng.shuffle(eligible[group.id])
    slots = [group.id for group in space.groups for _ in range(group.minimum)]
    owners: dict[Recipe, int] = {}

    def assign(slot: int, visited: set[Recipe]) -> bool:
        for recipe in eligible[slots[slot]]:
            if recipe in visited:
                continue
            visited.add(recipe)
            previous = owners.get(recipe)
            if previous is None or assign(previous, visited):
                owners[recipe] = slot
                return True
        return False

    for slot in range(len(slots)):
        assign(slot, set())
    selected = [(slots[slot], recipe) for recipe, slot in owners.items()]
    selected.sort(key=lambda item: owners[item[1]])
    counts = Counter(group_id for group_id, _ in selected)
    unmet = [
        {
            "group": group.id,
            "required": group.minimum,
            "selected": counts[group.id],
            "eligible": len(eligible[group.id]),
            "reason": "可用组合不足或分组重叠，无法同时满足全部配额",
        }
        for group in space.groups
        if counts[group.id] < group.minimum
    ]
    return selected, unmet


def fill_coverage(
    space: Space,
    pool: list[Recipe],
    selected: list[tuple[str, Recipe]],
    count: int,
    rng: random.Random,
) -> None:
    """先增加本轮维度覆盖，再拉开编码距离；同分时使用带种子的顺序。"""
    used = {recipe for _, recipe in selected}
    remaining = [recipe for recipe in pool if recipe not in used]
    rng.shuffle(remaining)
    while remaining and len(selected) < count:
        seen = {i: {recipe[i] for _, recipe in selected} for i in space.focus_indices}

        def priority(
            recipe: Recipe,
            covered: dict[int, set[str]] = seen,
        ) -> tuple[int, int]:
            new_options = sum(recipe[i] not in covered[i] for i in space.focus_indices)
            distance = min(
                encoded_distance(recipe, existing, space.focus_indices)
                for _, existing in selected
            )
            return new_options, distance

        chosen = max(remaining, key=priority)
        selected.append(("coverage", chosen))
        remaining.remove(chosen)


def coverage_summary(
    space: Space,
    pool: list[Recipe],
    recipes: list[Recipe],
) -> dict[str, Any]:
    """区分预算内未覆盖的选项与编码约束下没有可用组合的选项。"""
    result = {}
    for i, axis in enumerate(space.axes):
        used = {recipe[i] for recipe in recipes}
        possible = {recipe[i] for recipe in pool}
        result[axis.id] = {
            "covered": [value for value in axis.options if value in used],
            "uncovered_feasible": [
                value
                for value in axis.options
                if value in possible and value not in used
            ],
            "unavailable": [value for value in axis.options if value not in possible],
        }
    return result


def difference_summary(space: Space, recipes: list[Recipe]) -> dict[str, Any]:
    """提供编码距离矩阵及同签名候选，供人工检查实际方案是否重复。"""
    signatures: dict[Recipe, list[str]] = {}
    for i, recipe in enumerate(recipes, 1):
        signature = tuple(recipe[index] for index in space.focus_indices)
        signatures.setdefault(signature, []).append(f"C{i:02}")
    return {
        "axes_used": [space.axes[i].id for i in space.focus_indices],
        "matrix": [
            [encoded_distance(left, right, space.focus_indices) for right in recipes]
            for left in recipes
        ],
        "duplicate_signatures": [ids for ids in signatures.values() if len(ids) > 1],
        "meaning": "选项编码不同的数量；不代表体验差异、新颖性或设计质量",
    }


def sample_space(space: Space, seed: int, count: int) -> dict[str, Any]:
    """生成采样报告；完整状态仅表示数量与分组配额得到满足。"""
    if not 1 <= count <= MAX_CANDIDATES:
        raise ValueError("本工具候选预算为 1 至 200，较大探索请分轮进行")
    minimum = 1 + sum(group.minimum for group in space.groups)
    if count < minimum:
        raise ValueError(f"预算至少需要 {minimum}：包含基准及所有分组配额")
    rng = random.Random(seed)
    pool, excluded = enumerate_recipes(space)
    reserved, unmet = reserve_groups(space, pool, rng)
    selected = [("baseline", space.baseline), *reserved]
    fill_coverage(space, pool, selected, count, rng)
    recipes = [recipe for _, recipe in selected]
    canonical = json.dumps(space.config, sort_keys=True, ensure_ascii=False)
    return {
        "schema_version": 1,
        "tool_version": TOOL_VERSION,
        "python_version": platform.python_version(),
        "seed": seed,
        "requested_count": count,
        "space_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "space": space.config,
        "feasible_count": len(pool),
        "exclusion_matches": excluded,
        "candidates": [
            {
                "id": f"C{i:02}",
                "group": group_id,
                "axes": dict(zip((axis.id for axis in space.axes), recipe)),
            }
            for i, (group_id, recipe) in enumerate(selected, 1)
        ],
        "coverage": coverage_summary(space, pool, recipes),
        "encoded_difference": difference_summary(space, recipes),
        "unmet_groups": unmet,
        "count_shortfall": max(0, count - len(selected)),
        "sampling_complete": not unmet and len(selected) == count,
        "review_required": "文字约束、空间遗漏、解释忠实度和设计质量仍需核对",
    }


def main() -> int:
    """只向终端输出，不创建候选文件；配额或数量不足时退出码为 2。"""
    parser = argparse.ArgumentParser(description="设计空间覆盖与带种子采样")
    parser.add_argument("--space", required=True, type=Path, help="设计空间 JSON")
    parser.add_argument("--seed", required=True, type=int, help="复核用伪随机种子")
    parser.add_argument("--count", required=True, type=int, help="包含基准的候选预算")
    args = parser.parse_args()
    try:
        report = sample_space(load_space(args.space), args.seed, args.count)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"输入无效：{error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["sampling_complete"] else 2


if __name__ == "__main__":
    cast(TextIOWrapper, sys.stdout).reconfigure(encoding="utf-8")
    cast(TextIOWrapper, sys.stderr).reconfigure(encoding="utf-8")
    raise SystemExit(main())
