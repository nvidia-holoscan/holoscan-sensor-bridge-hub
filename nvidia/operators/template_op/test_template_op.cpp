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

#include <holoscan/holoscan.hpp>
#include <holoscan/operators/ping_rx/ping_rx.hpp>
#include <holoscan/operators/ping_tx/ping_tx.hpp>

#include "template_op.hpp"

// Sends 1, 2, and 3 through TemplateOp with a multiplier of 2; the receiver logs 2, 4, and 6.
class TemplateOpTestApp : public holoscan::Application {
 public:
  void compose() override {
    using namespace holoscan;

    auto tx = make_operator<ops::PingTxOp>("tx", make_condition<CountCondition>(3));
    auto multiply = make_operator<ops::TemplateOp>("multiply", Arg("multiplier", 2));
    auto rx = make_operator<ops::PingRxOp>("rx");
    add_flow(tx, multiply);
    add_flow(multiply, rx);
  }
};

int main() {
  auto app = holoscan::make_application<TemplateOpTestApp>();
  app->run();
  return 0;
}
