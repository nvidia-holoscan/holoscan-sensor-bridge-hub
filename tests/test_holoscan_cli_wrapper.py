# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _test_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("HOLOSCAN_CLI_ROOT", str(REPO_ROOT))
    return env


def _skip_unless_holoscan_cli(env: dict[str, str]) -> None:
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            "import holoscan_cli",
        ],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if probe.returncode != 0:
        raise unittest.SkipTest("holoscan_cli is not installed; install the pinned wheel")


class HoloscanCliWrapperTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = _test_env()
        _skip_unless_holoscan_cli(self.env)

    def run_wrapper(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(REPO_ROOT / "holohub"), *args],
            cwd=REPO_ROOT,
            env=self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_help_delegates_to_holoscan_cli(self) -> None:
        result = self.run_wrapper("--help")
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, output)
        self.assertIn("build-container", output)
        self.assertIn("run-container", output)
        self.assertIn("env-info", output)

    def test_list_uses_repo_search_paths(self) -> None:
        result = self.run_wrapper("list")
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, output)
        self.assertNotIn("applications/template/{{cookiecutter.project_slug}}", output)


if __name__ == "__main__":
    unittest.main()
