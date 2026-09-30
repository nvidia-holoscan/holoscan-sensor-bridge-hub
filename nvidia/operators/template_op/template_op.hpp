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

#ifndef TEMPLATE_OP_HPP
#define TEMPLATE_OP_HPP

#include <holoscan/holoscan.hpp>

namespace holoscan::ops {

/**
 * @brief Multiplies each integer received on "in" by the "multiplier" parameter.
 *
 * ==Named Inputs==
 *
 * - **in** : `int`
 *
 * ==Named Outputs==
 *
 * - **out** : `int`
 *
 * ==Parameters==
 *
 * - **multiplier**: Factor applied to each input value. Optional (default: `2`).
 */
class TemplateOp : public Operator {
 public:
  HOLOSCAN_OPERATOR_FORWARD_ARGS(TemplateOp)

  TemplateOp() = default;

  void setup(OperatorSpec& spec) override;
  void compute(InputContext& op_input, OutputContext& op_output,
               ExecutionContext& context) override;

 private:
  Parameter<int> multiplier_;
};

}  // namespace holoscan::ops

#endif  // TEMPLATE_OP_HPP
