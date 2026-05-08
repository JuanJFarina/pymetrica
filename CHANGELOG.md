# CHANGELOG



## v1.5.4 (2026-05-08)

### Fix

* fix(config): add audit flag to get top findings regardless of thresholds ([`7f62f48`](https://github.com/JuanJFarina/pymetrica/commit/7f62f48decdcd191edbb03e5c4a27e339f60cbdb))


## v1.5.3 (2026-05-06)

### Fix

* fix(config): fix log level env issue and refactor commands exitting ([`f0d8cb2`](https://github.com/JuanJFarina/pymetrica/commit/f0d8cb22541344386db99a12fb052eb820d15d22))

* fix(config): apply law of demeter principle ([`ae77744`](https://github.com/JuanJFarina/pymetrica/commit/ae77744486466743dd98e8904f81bdf7636d7b87))


## v1.5.2 (2026-05-05)

### Fix

* fix(config): add support for union types in po metric ([`25ed3db`](https://github.com/JuanJFarina/pymetrica/commit/25ed3db2008c8ffe70df640b45863d43dc9cb233))

* fix(config): fix bug in file maintainability cost and refactor some logs ([`54c3294`](https://github.com/JuanJFarina/pymetrica/commit/54c3294cad33e080c8f4764a6f30c2cf70f4d6f5))


## v1.5.1 (2026-05-05)

### Fix

* fix(config): refactor report generation and set threshold defaults ([`3e1f632`](https://github.com/JuanJFarina/pymetrica/commit/3e1f63297e4818b7345988a90ecb3b8c21db3c58))


## v1.5.0 (2026-05-05)

### Feature

* feat(config): add top findings for when metric fails ([`aa64531`](https://github.com/JuanJFarina/pymetrica/commit/aa645310be06b47200412fe32a47a1b1c4d78a9d))

* feat(config): add precommit hook report generator ([`f13ea87`](https://github.com/JuanJFarina/pymetrica/commit/f13ea87567739778cc8580481c6a2c99b81fedbf))

### Fix

* fix(config): update docs and fix small bugs ([`927c835`](https://github.com/JuanJFarina/pymetrica/commit/927c8356fd291c8ec679d28385c895e212698f40))


## v1.4.0 (2026-05-04)

### Feature

* feat(config): add primitive obsession metric ([`bb28cbf`](https://github.com/JuanJFarina/pymetrica/commit/bb28cbf8e49cdae5ba9f2be2e2d2483275719018))

### Fix

* fix(config): update docs and fix small issues ([`e834f6b`](https://github.com/JuanJFarina/pymetrica/commit/e834f6bfab957152888b5263c9ab0939c71b5ceb))

* fix(config): refactor to simplify metrics ([`a8c588a`](https://github.com/JuanJFarina/pymetrica/commit/a8c588a7b23f95a8b4fae506cc4d56be639c43f5))


## v1.3.2 (2026-04-27)

### Fix

* fix(config): invert mc fail message condition ([`22c98a2`](https://github.com/JuanJFarina/pymetrica/commit/22c98a2a52648bbd394944dc4609cd0cf8d04d3f))


## v1.3.1 (2026-04-26)

### Fix

* fix(config): improve fail messages to help understand how to improve the codebase ([`f527d73`](https://github.com/JuanJFarina/pymetrica/commit/f527d734b23676a2261c2805d508f37198ca91ba))

* fix(config): invert cc fail threshold so it fails when there are fewer lloc per cc branch ([`7b04b77`](https://github.com/JuanJFarina/pymetrica/commit/7b04b779b14733a85c3caa40bb9f1e72bb0bf244))

* fix(config): invert cc fail threshold so it fails when there are fewer lloc per cc branch ([`f38dc20`](https://github.com/JuanJFarina/pymetrica/commit/f38dc20c3839ce54db282b59dbef162892fe24e3))


## v1.3.0 (2026-04-21)

### Feature

* feat(config): add dependabot ([`bf02a10`](https://github.com/JuanJFarina/pymetrica/commit/bf02a102f3474b94489557a12fa702e5754b14c3))

### Fix

* fix(config): update docs and readme ([`9721e1a`](https://github.com/JuanJFarina/pymetrica/commit/9721e1a1d4018b0b42b9bf13f8d9b38e17c05836))


## v1.2.1 (2026-04-21)

### Fix

* fix(config): add dir exclusion configuration ([`ff167d2`](https://github.com/JuanJFarina/pymetrica/commit/ff167d23e8d8374d327cd9c8f510d845cabfee68))

* fix(config): sort layer metrics correctly ([`9ceca5b`](https://github.com/JuanJFarina/pymetrica/commit/9ceca5bea27449e87c5fdfc17105caada94ecd2d))


## v1.2.0 (2026-04-21)

### Feature

* feat(config): add pre commit hook compatibility ([`af5fce0`](https://github.com/JuanJFarina/pymetrica/commit/af5fce0d212a76ca444b628310a2aa2f1f4ef43a))

* feat(config): add pyproject configuration feature ([`2f04d55`](https://github.com/JuanJFarina/pymetrica/commit/2f04d554539a0b878965bc67cf7eefb003d588ba))

* feat(config): add initial read the docs config ([`13f5dd5`](https://github.com/JuanJFarina/pymetrica/commit/13f5dd5f77ae582bd32d525eb6a4208cdfc22c65))

### Fix

* fix(config): finish first mkdocs implementation ([`b574281`](https://github.com/JuanJFarina/pymetrica/commit/b5742814fd8eb539cb291c6f29ab5b83ed6b9886))

* fix(config): add upcoming feature on primitive check ([`4ee6645`](https://github.com/JuanJFarina/pymetrica/commit/4ee66456510cbe6ff32daf3be562e721327293d7))

* fix(config): add dependencies installation in gh action ([`e5e0892`](https://github.com/JuanJFarina/pymetrica/commit/e5e0892c115fa916f2fed5e4464932fc1195296c))

* fix(config): change local hook config ([`8aee9a1`](https://github.com/JuanJFarina/pymetrica/commit/8aee9a1b053ac29e11780d7f238e791978afda22))

* fix(config): add todos and fix cicd ([`bb58a66`](https://github.com/JuanJFarina/pymetrica/commit/bb58a66594f3daa15a2fce48902c6a777db91e0e))

* fix(config): change error logs to error standard out ([`7aad07a`](https://github.com/JuanJFarina/pymetrica/commit/7aad07a5edf85bb2b9d33893f8e15e6100efc788))

* fix(config): add automatic discovery of source folder for hook ([`f473c57`](https://github.com/JuanJFarina/pymetrica/commit/f473c57369962da86384b1fbbf1b2ab7e71d76dc))

* fix(config): use pymetrica run all for this repository ([`7fa86ea`](https://github.com/JuanJFarina/pymetrica/commit/7fa86ea22686f01ab2b2e0133d86f4b99941b7a6))

* fix(config): add warning log for . dir ([`021253c`](https://github.com/JuanJFarina/pymetrica/commit/021253c9bd1abac45585be8e5b4b6a99144db642))

* fix(config): add int return to all metrics except instability ([`1218018`](https://github.com/JuanJFarina/pymetrica/commit/12180182f6fb39430565486979a34ee6e334646c))

* fix(config): fix mkdocs initial draft ([`2c62830`](https://github.com/JuanJFarina/pymetrica/commit/2c6283071c194a8f57a38994ecc0a081d463d7e1))


## v1.1.0 (2026-03-15)

### Feature

* feat(config): add optional diagram filename argument ([`4a1e2e0`](https://github.com/JuanJFarina/pymetrica/commit/4a1e2e079aff68b29ad1e4f3c1ac01d586c1569d))

### Fix

* fix(config): add heuristic tests for diagram generation ([`5c96ea2`](https://github.com/JuanJFarina/pymetrica/commit/5c96ea2e977d5265004486b3b601ff50e5332f3d))

* fix(config): update diagram tests ([`eaf047b`](https://github.com/JuanJFarina/pymetrica/commit/eaf047bfd4a23d1578e3220e7b22ff8900f2ab24))

* fix(config): increase size of layer labels ([`ef27241`](https://github.com/JuanJFarina/pymetrica/commit/ef27241b1bd089189127e0aa9bf4431d0c797464))

* fix(config): add hv per lloc ([`f639b56`](https://github.com/JuanJFarina/pymetrica/commit/f639b566647649ca5f21db27b44aa0eeeee4475f))

* fix(config): fix diagram generation not counting dependencies ([`d49c99d`](https://github.com/JuanJFarina/pymetrica/commit/d49c99d1b6557e5a3fc929ad88bf4bd39a90ce5b))


## v1.0.2 (2026-03-15)

### Fix

* fix(config): fix type checking issue with invariant generic for results ([`01b3d70`](https://github.com/JuanJFarina/pymetrica/commit/01b3d704d9d2222b661f45b84b2631c3cfd246d1))

* fix(config): improve mc metric to have more balanced output between raw line mc and codebase size ([`eff0bb8`](https://github.com/JuanJFarina/pymetrica/commit/eff0bb861a85c5e03cf23f7fa7091bd5b6f5f00b))

* fix(config): reduce weight of codebase size ([`c782a96`](https://github.com/JuanJFarina/pymetrica/commit/c782a96289dfb108b5e999a1aface1277f99ed1d))


## v1.0.1 (2026-03-15)

### Fix

* fix(config): add semantic release configuration ([`9387d98`](https://github.com/JuanJFarina/pymetrica/commit/9387d98780f9a24860372281b882b475fd30229f))

* fix(config): fix project entrypoint ([`dde6910`](https://github.com/JuanJFarina/pymetrica/commit/dde691088c1a0af349129c9ce774700ab026e9f6))

### Unknown

* Revise README with new badges and project details

Updated README.md to enhance project description and add badges. ([`9cb0bca`](https://github.com/JuanJFarina/pymetrica/commit/9cb0bca5382d4067901b055de9f8887ca15839ad))


## v1.0.0 (2026-03-15)

### Fix

* fix(config): format manifest ([`dff6195`](https://github.com/JuanJFarina/pymetrica/commit/dff6195dd45869e44e8a1856e0179f0caa995c7e))

* fix(config): create manifest for including pipfile files ([`28748d4`](https://github.com/JuanJFarina/pymetrica/commit/28748d490715a5ae31750bdcd7c200c8494f343a))

* fix(config): enhance tests ([`71ad4c2`](https://github.com/JuanJFarina/pymetrica/commit/71ad4c28ce407865f3e181c26232527c9f0438c4))

* fix(config): solve all remaining test issues ([`2dbe5b6`](https://github.com/JuanJFarina/pymetrica/commit/2dbe5b67e723cd8db5ecf2c4829a8e259c4918b6))

* fix(config): format code ([`a60dff7`](https://github.com/JuanJFarina/pymetrica/commit/a60dff7c487c5868a59c4bc3f0eb83b4cead6b99))

* fix(config): fix all tests ([`c5213c0`](https://github.com/JuanJFarina/pymetrica/commit/c5213c092f76d289d28d14af2c241625ede35776))

* fix(config): solve wrong asserts in tests ([`e7c293d`](https://github.com/JuanJFarina/pymetrica/commit/e7c293d50f9c5c99facde76cc4fb9b73fcc8bdab))

* fix(config): remove filepath comparisons ([`d76708b`](https://github.com/JuanJFarina/pymetrica/commit/d76708b5816f058f6dac21d9abe03fb9a75def3e))

* fix(config): accomodate tests to work in ci ([`8a84f6f`](https://github.com/JuanJFarina/pymetrica/commit/8a84f6fd299740108a6b85d3dc4609352d707e1e))

* fix(config): remove pipenv from build action ([`9ef0c80`](https://github.com/JuanJFarina/pymetrica/commit/9ef0c80675bb7b65e1a652e621659aef0e0f4d71))

* fix(config): add which python to run test ([`515ce5b`](https://github.com/JuanJFarina/pymetrica/commit/515ce5b33586bc2fe000e82811c0323f16993b92))

* fix(config): remove pinned versions in cicd ([`ef514dd`](https://github.com/JuanJFarina/pymetrica/commit/ef514dd26896626cb5815ed3e3225288a8297e6c))

* fix(config): try to specify python to pipenv ([`59b3bc3`](https://github.com/JuanJFarina/pymetrica/commit/59b3bc3a8f3cbcd6bb3dd833d018f0be80d5df3c))

* fix(config): remove matrix python version ([`895b745`](https://github.com/JuanJFarina/pymetrica/commit/895b745d9c9736318942b3856cf069e1d0c10683))

* fix(config): remove coverall and hardening in matrix test ([`98e4f49`](https://github.com/JuanJFarina/pymetrica/commit/98e4f49bd18dc9b016c35277df44641d9c6f1f29))

* fix(config): remove coverall job ([`1655cf1`](https://github.com/JuanJFarina/pymetrica/commit/1655cf1f5e2de3d9b3ba860986c6c06cff2afdd5))

* fix(config): solve lint issues and set version to 0.7.0 ([`8f82fb9`](https://github.com/JuanJFarina/pymetrica/commit/8f82fb92a926a18f6e8701bdb58b06c4dcb105e6))

### Unknown

* change yaml for yml ([`e069776`](https://github.com/JuanJFarina/pymetrica/commit/e069776c236c74eba665d6918ffa919fd497925a))

* cicd setup ([`64f1504`](https://github.com/JuanJFarina/pymetrica/commit/64f1504be974d6013a1ca3bc33a49b9b611ab3e1))

* add long report and a few other tweaks ([`d0d754a`](https://github.com/JuanJFarina/pymetrica/commit/d0d754a69a89b53b6fb208349778602c5e4fbc0f))

* cleanup and change maintainability index to cost function ([`164d48a`](https://github.com/JuanJFarina/pymetrica/commit/164d48a17ac6e27849c1dbc48f714a8dac4869d7))

* add dependencies count to diagram ([`c30e937`](https://github.com/JuanJFarina/pymetrica/commit/c30e9379a745625c05aa09a2f945606f1b9729d7))

* add layered mi ([`f2ae203`](https://github.com/JuanJFarina/pymetrica/commit/f2ae203779fad2cd2ce49d3492f60c8488d2b8f7))

* add layered halstead volume ([`add0758`](https://github.com/JuanJFarina/pymetrica/commit/add0758d5ad0f50aea2b486c4bb22af697ae9df7))

* add cc layered results ([`d352cef`](https://github.com/JuanJFarina/pymetrica/commit/d352cef34199db694c48d0182515e7e84fda4534))

* finish aloc calculator per layer ([`b4c2e49`](https://github.com/JuanJFarina/pymetrica/commit/b4c2e494f832649b00b7ab6016884c5c054ff6b7))

* fix tests and draft aloc changes ([`cc19167`](https://github.com/JuanJFarina/pymetrica/commit/cc191677927ab34be9f731e6c620cc581732b2bd))

* add tests for diagram generation ([`19ae0bc`](https://github.com/JuanJFarina/pymetrica/commit/19ae0bc8cab9b61340d403413d4d67aca3a3a987))

* enhance test suite coverage to prevent regressions in upcoming refactors ([`e142538`](https://github.com/JuanJFarina/pymetrica/commit/e14253880d9d908804197dac80ce1dcf762e8369))

* initial implementation of cross-cuting layer analysis for all metrics ([`65f99f8`](https://github.com/JuanJFarina/pymetrica/commit/65f99f88dc458aa3dfabd2eda7975975d55e95be))

* set default log level to info ([`5043419`](https://github.com/JuanJFarina/pymetrica/commit/504341936a0092aa3157f0ae139a919c4f1ae8e2))

* enhance logging with loguru and add a profiler decorator ([`09bad51`](https://github.com/JuanJFarina/pymetrica/commit/09bad51a8793987fdbaad5bd8f2924a5eabbb204))

* fix component name bug ([`23d4086`](https://github.com/JuanJFarina/pymetrica/commit/23d4086a2b47e7b34ef7bddc10d6f8ed5bc23a7d))

* replace hardcoded separators for os sep ([`f04408a`](https://github.com/JuanJFarina/pymetrica/commit/f04408afde4fdce74e98ca71c507ff0ab25c91aa))

* fix linting issues ([`3c4b1d7`](https://github.com/JuanJFarina/pymetrica/commit/3c4b1d7c7b6876b26e27ec2e7cb15c4d968d9ef3))

* update readme ([`c26d628`](https://github.com/JuanJFarina/pymetrica/commit/c26d628b76794eb5463ce34703fc4a868d1cda96))

* improve diagram generation ([`b3352f7`](https://github.com/JuanJFarina/pymetrica/commit/b3352f748de38c867a67d7f528192923a9fbe64a))

* add diagram generation to base-stats ([`10a45ae`](https://github.com/JuanJFarina/pymetrica/commit/10a45ae2a7e1b7e15a61220daa0fdff1d329f9d5))

* change logs for sqrt in mi and adjust weights ([`bf2db0e`](https://github.com/JuanJFarina/pymetrica/commit/bf2db0ec248aca68fc2e08f5079d9cf700200dea))

* add more weight to halstead volume in mi ([`36499a2`](https://github.com/JuanJFarina/pymetrica/commit/36499a291e1f6f361773129bf88bf9ff4b66bb61))

* soften cyclomatic complexity weight in maintainability index formula ([`12d735a`](https://github.com/JuanJFarina/pymetrica/commit/12d735ae6ec857e81251b48f321d7f332aa8aa75))

* add correct entrypoint ([`0c06ae0`](https://github.com/JuanJFarina/pymetrica/commit/0c06ae04d4a69be7e30620910fe243481053ebb0))

* improve maintainability index formula to soften the lloc penalty ([`32f2147`](https://github.com/JuanJFarina/pymetrica/commit/32f21471449cc0c3ebc86d9b90ef2e05b124142b))

* add halstead volume and maintainability index tests, and a bigger sample codebase ([`99f39ee`](https://github.com/JuanJFarina/pymetrica/commit/99f39ee19eeac0e618f0682d003cbfc11595b3d9))

* include root package in analysis ([`9cb23da`](https://github.com/JuanJFarina/pymetrica/commit/9cb23da4643a307ef95a836dda9fc74bcce712be))

* change guard clase to return float zero ([`d4b9983`](https://github.com/JuanJFarina/pymetrica/commit/d4b99837825ba8bc16dcea32af293655490ae52b))

* add efferent coupling zero guard ([`b963c97`](https://github.com/JuanJFarina/pymetrica/commit/b963c9742a1094ab73bf67b7e478ade8c2d15bf2))

* fix small issue when calculating imports from subdirs ([`d0fcab7`](https://github.com/JuanJFarina/pymetrica/commit/d0fcab7ada5e800afa700ccc378a7f65402fe6ca))

* fix lint issues ([`f024fc9`](https://github.com/JuanJFarina/pymetrica/commit/f024fc9a276fe190dfa32f6d7ba384891e6370b5))

* add instability metric for coupling analysis ([`77ce2e6`](https://github.com/JuanJFarina/pymetrica/commit/77ce2e6c274c8bb6d34ab45e2bb7f0aa3ac7e0b4))

* fix lloc over cc ratio and improve mi description ([`afe1035`](https://github.com/JuanJFarina/pymetrica/commit/afe1035ca4694688cba9b5bd9e3bea41b37485cb))

* improve readme ([`8a6fb90`](https://github.com/JuanJFarina/pymetrica/commit/8a6fb90a5c6460846b5505357e918426d6ac168e))

* make dependencies more flexible ([`c0fe4bd`](https://github.com/JuanJFarina/pymetrica/commit/c0fe4bd99d5720d3b413640f57b87242d1bee058))

* add maintainability index calculation ([`0b022b7`](https://github.com/JuanJFarina/pymetrica/commit/0b022b7d9e53b668ca3317b49e6ff24074c7cd22))

* add halstead volume draft ([`38377dd`](https://github.com/JuanJFarina/pymetrica/commit/38377dd4ff1381068da3992b9ec9193bad29a9c8))

* add pre-commit hooks to dockerfile ([`d785bfc`](https://github.com/JuanJFarina/pymetrica/commit/d785bfc4340d4133bea800a6fad910434c0cc2e1))

* implemented report strategy in cc metric ([`c6412db`](https://github.com/JuanJFarina/pymetrica/commit/c6412dbc8fb146c6744007bdfe7421856ed952c2))

* integrate first report generator ([`5f1e9a6`](https://github.com/JuanJFarina/pymetrica/commit/5f1e9a6d0a68fbbafd30441ac6ae2a962817b84f))

* add dockerignore ([`5d565b6`](https://github.com/JuanJFarina/pymetrica/commit/5d565b6ba5090d7879799f740dc95f6d0ce1ff9b))

* improve linting configuration and fix issues ([`ccbe3d8`](https://github.com/JuanJFarina/pymetrica/commit/ccbe3d8f83e7b7d5e0e4a2920b1732289460b5d1))

* finished cc and added precommit linters ([`02fb48c`](https://github.com/JuanJFarina/pymetrica/commit/02fb48ccd2dbb3c0f59c72dd751d80b759041fa8))

* completed cyclomatic complexity metric calculator ([`d199d9d`](https://github.com/JuanJFarina/pymetrica/commit/d199d9de347a10d169f2a81ef563ec29a86251e1))

* first draft of cyclomatic complexity ([`ac2fdcb`](https://github.com/JuanJFarina/pymetrica/commit/ac2fdcb13056942d27e4736b44efb9689dde1bed))

* remove deprecated code ([`72e1baf`](https://github.com/JuanJFarina/pymetrica/commit/72e1baf4d596a5b374cdf3d1ecc5612b553625c4))

* small tweaks to codebase model and parser ([`38f3665`](https://github.com/JuanJFarina/pymetrica/commit/38f36653adc531967dc0a3aa52bdf9a5f60c2ea5))

* add todo for ignoring non-relevant folders ([`75c2235`](https://github.com/JuanJFarina/pymetrica/commit/75c2235ce28e1a6321620c60096b8b6ef8e9aebe))

* improve lloc count ([`5cb890e`](https://github.com/JuanJFarina/pymetrica/commit/5cb890e5be930b34a789516ef7ea115c23b19c79))

* add return type to aloc preliminary results ([`149f85d`](https://github.com/JuanJFarina/pymetrica/commit/149f85ddcf46a67edfa06bf1789e91f85ab69291))

* first implementation of abstract lines of code metric calculator ([`a4c189d`](https://github.com/JuanJFarina/pymetrica/commit/a4c189d3e7805a85ac33b7532bd85987413ffaef))

* improve base-stats and add devcontainer ([`283d100`](https://github.com/JuanJFarina/pymetrica/commit/283d10046aa17c61a42a752809ee4d0b5280debe))

* improve structure, add commands, and start building base-stats ([`577e1d9`](https://github.com/JuanJFarina/pymetrica/commit/577e1d92abc31ac4568d844dc9b7f5d851124a2d))

* add architecture drafts and project skeleton ([`302949b`](https://github.com/JuanJFarina/pymetrica/commit/302949bff6a7a6f677d4f20472e89d90c6095d12))

* add entrypoint and small refactor ([`73975ed`](https://github.com/JuanJFarina/pymetrica/commit/73975edefc74785e63d78206138796697546e81f))

* proof of concept for abstractness metric ([`6e22843`](https://github.com/JuanJFarina/pymetrica/commit/6e228436c14e322068a26c36097a6ead7de79811))

* Initial commit ([`cfa7c3e`](https://github.com/JuanJFarina/pymetrica/commit/cfa7c3e136b7c1deb78060ab5a0b486e4071a895))
