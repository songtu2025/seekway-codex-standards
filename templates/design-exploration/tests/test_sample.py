"""验证采样契约、覆盖报告与命令行退出状态。"""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))

from sample import sample_space
from space import Space, load_space


def configured_space(config: dict[str, Any]) -> Space:
    """复用配置入口验证内存中的测试数据，不产生临时配置文件。"""
    with patch("space.Path.read_text", return_value=json.dumps(config)):
        return load_space(Path("测试空间.json"))


class SamplingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config: dict[str, Any] = {
            "schema_version": 1,
            "scope": "structure",
            "task": "核对并提交记录",
            "constraints": ["所有方案完成相同任务"],
            "axes": [
                {
                    "id": "navigation",
                    "label": "导航",
                    "kind": "core",
                    "source": "测试任务",
                    "options": ["基准", "上下文", "命令"],
                },
                {
                    "id": "emphasis",
                    "label": "强调",
                    "kind": "visual",
                    "source": "测试任务",
                    "options": ["状态", "操作"],
                },
            ],
            "baseline": {"navigation": "基准", "emphasis": "状态"},
            "exclusions": [],
            "groups": [],
        }

    def test_replay_and_input_preservation(self) -> None:
        space = load_space(TEMPLATE / "example.json")
        original = copy.deepcopy(space.config)
        first = sample_space(space, 41382, 16)
        self.assertEqual(first, sample_space(space, 41382, 16))
        self.assertEqual(space.config, original)
        self.assertEqual(first["space"], original)
        self.assertEqual(first["candidates"][0]["axes"], original["baseline"])
        self.assertEqual(len(first["space_sha256"]), 64)

    def test_example_constraints_uniqueness_and_groups(self) -> None:
        space = load_space(TEMPLATE / "example.json")
        report = sample_space(space, 41382, 16)
        candidates = report["candidates"]
        signatures = {tuple(item["axes"].values()) for item in candidates}
        self.assertEqual(len(signatures), 16)
        self.assertTrue(report["sampling_complete"])
        self.assertFalse(report["unmet_groups"])
        for candidate in candidates:
            for exclusion in space.config["exclusions"]:
                with self.subTest(candidate=candidate["id"]):
                    self.assertFalse(
                        all(
                            candidate["axes"][key] == value
                            for key, value in exclusion["match"].items()
                        )
                    )
        for group in space.config["groups"]:
            assigned = [item for item in candidates if item["group"] == group["id"]]
            self.assertEqual(len(assigned), group["minimum"])
            for item in assigned:
                changed = sum(
                    item["axes"][axis.id] != space.config["baseline"][axis.id]
                    for axis in space.axes
                    if axis.kind == "core"
                )
                self.assertGreaterEqual(changed, group["min_changes"])
            self.assertTrue(
                all(
                    any(
                        all(
                            item["axes"][key] == value for key, value in pattern.items()
                        )
                        for pattern in group["patterns"]
                    )
                    for item in assigned
                )
            )
        for axis in report["coverage"].values():
            self.assertFalse(axis["uncovered_feasible"])

    def test_overlapping_groups_do_not_steal_reserved_directions(self) -> None:
        self.config["axes"][1]["options"] = ["状态"]
        self.config["groups"] = [
            {
                "id": "flexible",
                "purpose": "两个方向均可",
                "minimum": 1,
                "patterns": [{"navigation": "上下文"}, {"navigation": "命令"}],
            },
            {
                "id": "limited",
                "purpose": "必须覆盖上下文",
                "minimum": 1,
                "patterns": [{"navigation": "上下文"}],
            },
        ]
        for seed in range(6):
            report = sample_space(configured_space(self.config), seed, 3)
            assignments = {item["group"]: item["axes"] for item in report["candidates"]}
            self.assertTrue(report["sampling_complete"])
            self.assertEqual(assignments["limited"]["navigation"], "上下文")
            self.assertEqual(assignments["flexible"]["navigation"], "命令")

    def test_budget_shortfall_is_reported_without_duplicates(self) -> None:
        report = sample_space(configured_space(self.config), 7, 8)
        self.assertFalse(report["sampling_complete"])
        self.assertEqual(report["feasible_count"], 6)
        self.assertEqual(report["count_shortfall"], 2)
        self.assertEqual(len(report["candidates"]), 6)

    def test_unavailable_and_uncovered_options_are_distinguished(self) -> None:
        self.config["exclusions"] = [
            {"match": {"navigation": "命令"}, "reason": "测试中禁止命令"},
        ]
        report = sample_space(configured_space(self.config), 7, 1)
        coverage = report["coverage"]["navigation"]
        self.assertEqual(coverage["unavailable"], ["命令"])
        self.assertEqual(coverage["uncovered_feasible"], ["上下文"])
        self.assertEqual(report["exclusion_matches"]["测试中禁止命令"], 2)

    def test_impossible_group_keeps_its_quota_and_failure(self) -> None:
        self.config["exclusions"] = [
            {"match": {"navigation": "命令"}, "reason": "测试中禁止命令"},
        ]
        self.config["groups"] = [
            {
                "id": "command",
                "purpose": "必须覆盖命令",
                "minimum": 1,
                "patterns": [{"navigation": "命令"}],
            },
        ]
        report = sample_space(configured_space(self.config), 7, 2)
        self.assertFalse(report["sampling_complete"])
        self.assertEqual(report["unmet_groups"][0]["eligible"], 0)
        self.assertEqual(report["unmet_groups"][0]["required"], 1)
        self.assertEqual(report["count_shortfall"], 0)

    def test_budget_must_include_baseline_and_quotas(self) -> None:
        space = load_space(TEMPLATE / "example.json")
        with self.assertRaisesRegex(ValueError, "至少需要 7"):
            sample_space(space, 7, 6)

    def test_visual_skin_does_not_count_as_structural_distance(self) -> None:
        self.config["axes"][0]["options"] = ["基准"]
        report = sample_space(configured_space(self.config), 7, 2)
        differences = report["encoded_difference"]
        self.assertEqual(differences["matrix"], [[0, 0], [0, 0]])
        self.assertEqual(differences["duplicate_signatures"], [["C01", "C02"]])
        self.config["scope"] = "visual"
        visual = sample_space(configured_space(self.config), 7, 2)
        self.assertEqual(visual["encoded_difference"]["matrix"], [[0, 1], [1, 0]])
        self.assertFalse(visual["encoded_difference"]["duplicate_signatures"])

    def test_unknown_conditions_and_duplicate_axes_are_rejected(self) -> None:
        invalid = copy.deepcopy(self.config)
        invalid["exclusions"] = [{"match": {"missing": "值"}, "reason": "测试"}]
        with self.assertRaisesRegex(ValueError, "未知维度"):
            configured_space(invalid)
        invalid = copy.deepcopy(self.config)
        invalid["axes"].append(invalid["axes"][0])
        with self.assertRaisesRegex(ValueError, "标识不得重复"):
            configured_space(invalid)

    def test_invalid_baseline_and_space_size_are_rejected(self) -> None:
        self.config["exclusions"] = [
            {"match": {"navigation": "基准"}, "reason": "基准无效"},
        ]
        with self.assertRaisesRegex(ValueError, "基准组合"):
            sample_space(configured_space(self.config), 7, 1)
        self.config["exclusions"] = []
        self.config["axes"][0]["options"] = ["基准", *map(str, range(50000))]
        with self.assertRaisesRegex(ValueError, "超过 50000"):
            sample_space(configured_space(self.config), 7, 1)

    def test_config_hash_changes_with_exploration_space(self) -> None:
        first = sample_space(configured_space(self.config), 7, 3)
        self.config["task"] = "同一任务的修订描述"
        second = sample_space(configured_space(self.config), 7, 3)
        self.assertNotEqual(first["space_sha256"], second["space_sha256"])

    def test_option_string_cannot_silently_become_character_options(self) -> None:
        self.config["axes"][0]["options"] = "基准"
        with self.assertRaisesRegex(TypeError, "选项列表"):
            configured_space(self.config)

    def test_budget_limit_prevents_unbounded_distance_reports(self) -> None:
        for count in (0, 201):
            with (
                self.subTest(count=count),
                self.assertRaisesRegex(ValueError, "1 至 200"),
            ):
                sample_space(configured_space(self.config), 7, count)

    def test_cli_exit_states_and_json_output(self) -> None:
        command = [
            sys.executable,
            "-B",
            str(TEMPLATE / "sample.py"),
            "--space",
            str(TEMPLATE / "example.json"),
            "--seed",
            "41382",
            "--count",
        ]
        for count, expected in ((16, 0), (6, 1), (200, 2)):
            with self.subTest(count=count):
                result = subprocess.run(
                    [*command, str(count)],
                    capture_output=True,
                    encoding="utf-8",
                    check=False,
                )
                self.assertEqual(result.returncode, expected)
                if expected == 1:
                    self.assertFalse(result.stdout)
                    self.assertIn("输入无效", result.stderr)
                else:
                    self.assertFalse(result.stderr)
                    report = json.loads(result.stdout)
                    self.assertEqual(report["sampling_complete"], expected == 0)


if __name__ == "__main__":
    unittest.main()
