#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2022-2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

import argparse
import codecs
import json
import logging
import os
from pathlib import Path

from holoscan_cli.metadata.gather_metadata import gather_metadata as collect_project_metadata
from holoscan_cli.metadata.utils import list_normalized_languages

DEFAULT_INCLUDE_PATHS = ("applications", "operators", "tutorials")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def extract_readme(file_path):
    """Check for the README.md file in the current directory"""
    readme_path = os.path.join(os.path.dirname(file_path), "README.md")
    if os.path.exists(readme_path):
        with codecs.open(readme_path, "r", "utf-8") as readme_file:
            return readme_file.read()
    else:
        # If README.md is not found, look for it one level up
        readme_path = os.path.join(os.path.dirname(os.path.dirname(file_path)), "README.md")
        if os.path.exists(readme_path):
            with codecs.open(readme_path, "r", "utf-8") as readme_file:
                return readme_file.read()
        else:
            return ""


def generate_build_and_run_command(entry: dict) -> str:
    """Generate the build and run command for the application or workflow"""
    project_name = entry.get("project_name") or entry.get("application_name")
    if not project_name:
        return ""

    language = list_normalized_languages(entry.get("metadata", {}).get("language", ""))[0]
    if language == "python":
        return f"See README for {project_name} (python)"
    elif language in ["cpp", "c++"]:
        return f"See README for {project_name} (cpp)"
    else:
        return f"See README for {project_name}"


def _warn_duplicate_projects(metadata_entries: list[dict]) -> None:
    seen: dict[tuple[str, str], str] = {}
    for entry in metadata_entries:
        project_name = entry.get("project_name", "")
        source_folder = entry.get("source_folder", "")
        for language in list_normalized_languages(entry.get("metadata", {}).get("language")):
            key = (project_name, language or "")
            if key in seen:
                lang_label = language or "unspecified language"
                logger.warning(
                    "Duplicate project '%s' (%s) detected in '%s' and '%s'",
                    project_name,
                    lang_label,
                    seen[key],
                    source_folder,
                )
            else:
                seen[key] = source_folder


def gather_metadata(repo_paths: list[str], exclude_paths: list[str] | None = None) -> list[dict]:
    """Add hub documentation fields to metadata discovered by Holoscan CLI."""
    metadata = collect_project_metadata(repo_paths, exclude_paths)
    for entry in metadata:
        metadata_path = Path(entry["source_folder"]) / "metadata.json"
        entry["readme"] = extract_readme(metadata_path)
        if entry["project_type"] in ["application", "benchmark"]:
            command = generate_build_and_run_command(entry)
            if command:
                entry["build_and_run"] = command
    return metadata


def main(args: argparse.Namespace):
    """Run the gather application"""

    DEFAULT_OUTPUT_FILEPATH = "aggregate_metadata.json"

    repo_paths = args.include or DEFAULT_INCLUDE_PATHS
    output_file = args.output or DEFAULT_OUTPUT_FILEPATH

    metadata = gather_metadata(repo_paths, exclude_paths=args.exclude)
    _warn_duplicate_projects(metadata)

    # Write the metadata to the output file
    with open(output_file, "w") as output:
        json.dump(metadata, output, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility to collect JSON metadata for HoloHub projects"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        help="Output filepath for JSON collection of project metadata",
    )
    parser.add_argument(
        "--include",
        type=str,
        nargs="*",
        required=False,
        help="Path(s) to search for metadata files",
    )
    parser.add_argument(
        "--exclude",
        type=str,
        nargs="*",
        required=False,
        help="Filepath(s) to exclude from metadata collection. Takes priority over --include.",
    )
    args = parser.parse_args()
    main(args)
