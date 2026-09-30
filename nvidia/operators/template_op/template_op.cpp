/*
 * SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "template_op.hpp"

#include <stdexcept>

namespace holoscan::ops {

void TemplateOp::setup(OperatorSpec& spec) {
  spec.input<int>("in");
  spec.output<int>("out");
  spec.param(multiplier_, "multiplier", "Multiplier", "Factor applied to each input value.", 2);
}

void TemplateOp::compute(InputContext& op_input, OutputContext& op_output,
                         [[maybe_unused]] ExecutionContext& context) {
  auto value = op_input.receive<int>("in");
  if (!value) {
    throw std::runtime_error("TemplateOp: no value received on port 'in'");
  }
  op_output.emit(value.value() * multiplier_.get(), "out");
}

}  // namespace holoscan::ops
