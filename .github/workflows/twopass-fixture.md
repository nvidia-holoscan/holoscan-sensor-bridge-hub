# Two-pass fixture (experiment)

- [real analog (lychee fails h2, should be rescued)](https://www.analog.com/en/products/adtf3175.html)
- [bogus analog (should stay FAILED, 404)](https://www.analog.com/en/products/zzz-nonexistent-xyz-98765.html)
- [dead github (should stay FAILED, 404)](https://github.com/nvidia-holoscan/this-repo-does-not-exist-xyz123)
- [live control (lychee passes)](https://github.com/nvidia-holoscan/holoscan-sensor-bridge)
