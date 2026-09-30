# SPDX-FileCopyrightText: Copyright (c) 2024-2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Utility helpers shared across metadata consumers.

import os
from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path

# Contributions live under <org>/<category>/<project>/.
CATEGORIES = (
    "operators",
    "examples",
    "demos",
    "fpga",
    "ai/skills",
    "benchmarks",
    "tutorials",
    "utilities",
)
# Top-level directories that do not belong to a contributing organization.
NON_ORG_DIRS = ("tools",)

# Top-level metadata.json keys; each one selects <key>.schema.json.
PROJECT_TYPES = ("application", "benchmark", "operator", "tutorial")

SCHEMA_DIR = Path(__file__).resolve().parent
BASE_SCHEMA_PATH = SCHEMA_DIR / "project.schema.json"


def iter_category_dirs(root: str | os.PathLike = ".") -> Iterator[Path]:
    """Yield the existing <org>/<category> directories under the repository root."""
    for org in sorted(Path(root).iterdir()):
        if not org.is_dir() or org.name.startswith(".") or org.name in NON_ORG_DIRS:
            continue
        for category in CATEGORIES:
            if (org / category).is_dir():
                yield org / category


def normalize_language(language: str | None, *, strict: bool = False) -> str:
    """Normalize language names, optionally enforcing known languages."""
    if not language or not isinstance(language, str):
        return ""
    lang = language.strip().lower()
    if lang in ("cpp", "c++"):
        normalized = "cpp"
    elif lang in ("python", "py"):
        normalized = "python"
    else:
        normalized = lang

    if strict and normalized not in ("", "cpp", "python"):
        raise ValueError(f"Invalid language: {language}")
    return normalized


def list_normalized_languages(language, *, strict: bool = False) -> list[str]:
    """Return a list of normalized language tags from a single value or sequence."""
    if isinstance(language, str) or language is None:
        values = [language]
    elif isinstance(language, Iterable):
        values = list(language)
    else:
        values = []

    normalized = [
        normalize_language(value, strict=strict)
        for value in values
        if value is None or isinstance(value, str)
    ]
    normalized = [value for value in normalized if value]
    return normalized or [""]


def iter_metadata_paths(
    repo_paths: Sequence[str | os.PathLike],
    *,
    exclude_patterns: Sequence[str] | None = None,
) -> Iterator[str]:
    """Yield metadata.json paths, skipping paths that contain an excluded segment."""
    excludes = [pattern for pattern in (exclude_patterns or []) if pattern]

    def _matches_segment(path: str, patterns: Sequence[str]) -> bool:
        # Pattern must appear as a complete (slash-bordered) path segment, so
        # "template" matches "a/template/b" but not "a/my_template/b".
        norm = "/" + path.replace(os.sep, "/").strip("/") + "/"
        return any(
            ("/" + pattern.replace(os.sep, "/").strip("/") + "/") in norm for pattern in patterns
        )

    for repo_path in repo_paths:
        path = Path(repo_path)
        if path.is_file():
            candidates = [str(path)] if path.name == "metadata.json" else []
        else:
            candidates = sorted(
                os.path.join(root, "metadata.json")
                for root, _, files in os.walk(path)
                if "metadata.json" in files
            )

        for file_path in candidates:
            if excludes and _matches_segment(file_path, excludes):
                continue
            yield file_path
