# check-urls experiment (do not merge)

Exercises the PR job of `check_urls.yml` from a nested directory.

- Nested relative: [aditof](aditof/README.md), [code](code_README.md), [patch](patches/0001-adi-spi-gpio.patch)
- Up to the repository root: [license](../../../LICENSE), [tools](../../../tools/README.md)
- Root-relative (resolved by `--root-dir`): [readme](/README.md)
- WAF-gated vendor page (rescued by the re-check): [ADTF3175](https://www.analog.com/en/products/adtf3175.html)
- Deliberately broken, must stay FAILED: [missing](does-not-exist.md)
