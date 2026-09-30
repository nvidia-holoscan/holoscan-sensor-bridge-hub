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

from utils import (
    PROJECT_TYPES,
    iter_metadata_paths,
    iter_org_dirs,
    list_normalized_languages,
)

logger = logging.getLogger(__name__)


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


def extract_project_name(metadata_filepath: str) -> str:
    """Extract the project name from the metadata.json file path.

    A `metadata.json` file must be located at either:
    - the named project folder; or
    - a language subfolder one level below the project folder.

    The following are valid examples:
    - nvidia/operators/my_operator/metadata.json -> my_operator
    - nvidia/examples/my_example/cpp/metadata.json -> my_example

    """
    parts = metadata_filepath.split(os.sep)
    if parts[-2] in ["cpp", "python", "py"]:
        return parts[-3]
    return parts[-2]


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
    """
    Collect project metadata from JSON files into a single dictionary

    This function will return a list of dictionaries, each containing metadata for a project.

    :input:
        repo_paths: list
            The paths to collect metadata from.
        exclude_paths: list
            A list of path segments to exclude from metadata collection.
    :return:
        A list of dictionaries, each containing metadata for a project.
    """
    metadata = []

    # Iterate over the found metadata files
    for file_path in iter_metadata_paths(repo_paths, exclude_patterns=exclude_paths):
        with open(file_path, "r") as file:
            try:
                entries = json.load(file)
                entries = entries if type(entries) is list else [entries]

                for data in entries:
                    try:
                        schema_type = next(key for key in data.keys() if key in PROJECT_TYPES)
                    except StopIteration:
                        logger.error(
                            'No valid schema type found in metadata file "%s". Available keys: %s',
                            file_path,
                            ", ".join(data.keys()),
                        )
                        continue

                    data["project_type"] = schema_type
                    data["metadata"] = data.pop(schema_type)
                    data["project_name"] = extract_project_name(file_path)
                    data["source_folder"] = str(Path(file_path).parent)
                    data["readme"] = extract_readme(file_path)
                    if schema_type in ["application", "benchmark"]:
                        command = generate_build_and_run_command(data)
                        if command:
                            data["build_and_run"] = command
                    metadata.append(data)
            except json.decoder.JSONDecodeError as e:
                logger.error('Error parsing JSON file "%s": %s', file_path, e)
                continue

    return metadata


def main(args: argparse.Namespace):
    """Run the gather application"""

    DEFAULT_OUTPUT_FILEPATH = "aggregate_metadata.json"

    repo_paths = args.include or list(iter_org_dirs())
    output_file = args.output or DEFAULT_OUTPUT_FILEPATH

    metadata = gather_metadata(repo_paths, exclude_paths=args.exclude)
    _warn_duplicate_projects(metadata)

    # Write the metadata to the output file
    with open(output_file, "w") as output:
        json.dump(metadata, output, indent=4)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(
        description="Utility to collect JSON metadata for Holoscan Sensor Bridge Hub projects"
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
        help="Path(s) to search for metadata files (default: every organization directory)",
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
