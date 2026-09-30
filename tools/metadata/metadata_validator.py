# SPDX-FileCopyrightText: Copyright (c) 2023-2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
"""Validate the optional metadata.json files in the organization directories."""

import json
import sys

import jsonschema
from jsonschema import Draft202012Validator
from referencing import Registry
from referencing.jsonschema import DRAFT202012
from utils import (
    BASE_SCHEMA_PATH,
    PROJECT_TYPES,
    SCHEMA_DIR,
    iter_metadata_paths,
    iter_org_dirs,
)


def validate_json(json_data):
    """Validate metadata against the schema selected by its top-level project type key."""
    project_types = []
    if isinstance(json_data, dict):
        project_types = [key for key in PROJECT_TYPES if key in json_data]
    if len(project_types) != 1:
        return False, f"Expected exactly one top-level key from: {', '.join(PROJECT_TYPES)}"

    with open(BASE_SCHEMA_PATH) as file:
        base_schema = json.load(file)
    registry = Registry().with_resource(
        base_schema["$id"], DRAFT202012.create_resource(base_schema)
    )
    with open(SCHEMA_DIR / f"{project_types[0]}.schema.json") as file:
        schema = json.load(file)
    validator = Draft202012Validator(schema, registry=registry)

    try:
        validator.validate(json_data)
    except jsonschema.exceptions.ValidationError as err:
        return False, err

    return True, "valid"


def main() -> int:
    exit_code = 0
    metadata_paths = list(iter_metadata_paths(list(iter_org_dirs())))
    if not metadata_paths:
        print("No metadata.json files found in the organization directories.")

    for name in metadata_paths:
        with open(name, "r") as file:
            try:
                json_data = json.load(file)
            except json.decoder.JSONDecodeError:
                print("ERROR:" + name + ": invalid")
                exit_code = 1
                continue

        is_valid, msg = validate_json(json_data)
        if is_valid:
            print(name + ": valid")
        else:
            print("ERROR:" + name + ": invalid")
            print(msg)
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
