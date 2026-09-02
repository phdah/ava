# Changelog

## [1.0.0-alpha.17](https://github.com/phdah/ava/compare/v1.0.0-alpha.16...v1.0.0-alpha.17) (2026-09-02)


### Features

* **release:** qualify edge-independent behavior before edge authoring ([#120](https://github.com/phdah/ava/issues/120)) ([8c4771f](https://github.com/phdah/ava/commit/8c4771f9b434ff02a936e84e55799636430c2ce9))

## [1.0.0-alpha.16](https://github.com/phdah/ava/compare/v1.0.0-alpha.15...v1.0.0-alpha.16) (2026-09-01)


### Features

* add interaction evidence provenance ([#116](https://github.com/phdah/ava/issues/116)) ([7df5758](https://github.com/phdah/ava/commit/7df5758a5de1bf28cc8772575fe62bcaf21afa3c))
* reduce inbox claim provenance verbosity ([#118](https://github.com/phdah/ava/issues/118)) ([f92e834](https://github.com/phdah/ava/commit/f92e834728d4ec979091c154244f3f982c13648c))
* **roles:** add project task manager ([#115](https://github.com/phdah/ava/issues/115)) ([2f58086](https://github.com/phdah/ava/commit/2f58086f17249107fd8826564eb7e032b8fd6bc5))

## [1.0.0-alpha.15](https://github.com/phdah/ava/compare/v1.0.0-alpha.14...v1.0.0-alpha.15) (2026-08-29)


### Features

* shrink complete-pending-inbox qualification fixture ([#105](https://github.com/phdah/ava/issues/105)) ([39bcf33](https://github.com/phdah/ava/commit/39bcf33322b8768fe6b4ae69721c690ccef49227))


### Bug Fixes

* buffer large OpenCode qualification JSON ([#100](https://github.com/phdah/ava/issues/100)) ([a8db2ca](https://github.com/phdah/ava/commit/a8db2ca731931cb3af1eefd636e2778d3aa319af))
* close qualification audit findings ([#97](https://github.com/phdah/ava/issues/97)) ([ca07c95](https://github.com/phdah/ava/commit/ca07c951f2eea3c31cc22019bebd76cf26af1937))
* preserve scoped history during inbox ingestion ([#92](https://github.com/phdah/ava/issues/92)) ([b13e32c](https://github.com/phdah/ava/commit/b13e32cfc11335dfa124fc6ef8f42576c5bd1635))
* prohibit ad hoc code during inbox ingestion ([#102](https://github.com/phdah/ava/issues/102)) ([192e668](https://github.com/phdah/ava/commit/192e668b24ed6b4e1b5f052b676c777bade2d6f4))
* **qualification:** validate model identifiers by structure, not literal name ([e6edce9](https://github.com/phdah/ava/commit/e6edce954bedc60868907d86ad1e7519a7a74130))
* **release:** remove hardcoded semantic-inspection-path gate ([0505b7a](https://github.com/phdah/ava/commit/0505b7a5794fdb9c8b77dbe1dc2e4e9ed65ec233))
* remove inbox ingestion execution restriction ([#109](https://github.com/phdah/ava/issues/109)) ([20ccc4b](https://github.com/phdah/ava/commit/20ccc4b8a7d013c6d3f7226a0f48c39b013720fe))
* repair Inbox Ingester project-root links ([#88](https://github.com/phdah/ava/issues/88)) ([4ddbbfc](https://github.com/phdah/ava/commit/4ddbbfc30f8bdd1d99818ca19b7e045293f2b652))
* report semantic inspection paths during terminal cleanup ([#98](https://github.com/phdah/ava/issues/98)) ([87a7e8c](https://github.com/phdah/ava/commit/87a7e8ca092bb84f422bc18978260cd468fbbc34))
* report semantic inspections during reconciliation ([#99](https://github.com/phdah/ava/issues/99)) ([61d3a83](https://github.com/phdah/ava/commit/61d3a8370c1f0eb29f9bc812d1b274059fa13255))
* require reconciled inbox disposition evidence ([#103](https://github.com/phdah/ava/issues/103)) ([3f1bdef](https://github.com/phdah/ava/commit/3f1bdef7222a9fd26751f90d7cbce273f78a3204))
* **upgrades:** permit agent-driven finalization ([#90](https://github.com/phdah/ava/issues/90)) ([8df64b6](https://github.com/phdah/ava/commit/8df64b62d46c120647bb4170aa14a516fddbd24a))
* **upgrades:** recover interrupted terminal cleanup ([8ab49b8](https://github.com/phdah/ava/commit/8ab49b89f52252c573f145b5bde77d22ed1307e9))
* **upgrades:** remove complete finalized transaction ([16fd8ee](https://github.com/phdah/ava/commit/16fd8ee47372b49615b0667d81d89f388d546331))
* **upgrades:** validate terminal cleanup recovery ([c861828](https://github.com/phdah/ava/commit/c86182873e3d322fa8ffffae3fea53d53ba6557c))
* verify relative calendar dates before persisting ([#94](https://github.com/phdah/ava/issues/94)) ([ee10119](https://github.com/phdah/ava/commit/ee1011931025df4a23babb8f63d683c5ceff6291))

## [1.0.0-alpha.14](https://github.com/phdah/ava/compare/v1.0.0-alpha.13...v1.0.0-alpha.14) (2026-08-10)


### Bug Fixes

* **routing:** avoid redundant follow-up routing ([#82](https://github.com/phdah/ava/issues/82)) ([e423025](https://github.com/phdah/ava/commit/e423025b4921f0916df159acda6b663f85867d6a))

## [1.0.0-alpha.13](https://github.com/phdah/ava/compare/v1.0.0-alpha.12...v1.0.0-alpha.13) (2026-08-09)


### Bug Fixes

* **release:** enforce recursive adjacent edge records ([#78](https://github.com/phdah/ava/issues/78)) ([76600b9](https://github.com/phdah/ava/commit/76600b9a070ac2bb16ca96182e6b8138a373c8cb))

## [1.0.0-alpha.12](https://github.com/phdah/ava/compare/v1.0.0-alpha.11...v1.0.0-alpha.12) (2026-08-09)


### Features

* define review sufficiency and termination ([#73](https://github.com/phdah/ava/issues/73)) ([14bc564](https://github.com/phdah/ava/commit/14bc564534d45a50676e65c6081be186831ead8e))
* **release:** compose semantic upgrades from adjacent edges ([#76](https://github.com/phdah/ava/issues/76)) ([03f4bfd](https://github.com/phdah/ava/commit/03f4bfd80bfc91cb28d85f8cdf6ee00bc83f8b3c))

## [1.0.0-alpha.11](https://github.com/phdah/ava/compare/v1.0.0-alpha.10...v1.0.0-alpha.11) (2026-08-08)


### Features

* add project steward role ([1e991c1](https://github.com/phdah/ava/commit/1e991c12e77a9d1b41d916c30303de49444faa4e))
* add project steward role ([2fb01f6](https://github.com/phdah/ava/commit/2fb01f6c43efa076696a1e009ac4a93aa56da4fe))
* add project steward role ([6b1e4ac](https://github.com/phdah/ava/commit/6b1e4acffb9590553a9f544917c1dd012774fb9c))
* add project steward role ([dac4228](https://github.com/phdah/ava/commit/dac4228497dafe4a82cd9cfa25ae96e48cdeb3aa))
* add project steward role ([dad29a9](https://github.com/phdah/ava/commit/dad29a9ddf6fece1b9f0d7c3e048f3444355f5b4))
* add project steward role ([7fae0f3](https://github.com/phdah/ava/commit/7fae0f34bcdbe79bc15213590617873acc36733e))
* add project steward role ([794bec2](https://github.com/phdah/ava/commit/794bec2d0cbc92ce1de4e55b5d5090a875f0c466))
* add project steward role ([98945b0](https://github.com/phdah/ava/commit/98945b006ae447e8fdd3851e7817a2aa49436312))
* **release:** force first alpha proposal ([#38](https://github.com/phdah/ava/issues/38)) ([f284794](https://github.com/phdah/ava/commit/f2847946c6644379aed86e8e925c5625dc5ff805))
* **release:** publish qualified releases automatically ([#46](https://github.com/phdah/ava/issues/46)) ([9959b8c](https://github.com/phdah/ava/commit/9959b8c37d04d993c4857ef135ca862fbe4f672f))


### Bug Fixes

* align project steward routing ([c5f40bc](https://github.com/phdah/ava/commit/c5f40bcb07ce2f60e285ae90f45faf22c2007096))
* align project steward routing ([c5ddc92](https://github.com/phdah/ava/commit/c5ddc92922b10412b35ee068a341aa4edfe34316))
* align project steward routing ([3181434](https://github.com/phdah/ava/commit/31814347d2c11e2e0bf1b43ac7f38f66715e590d))
* align project steward routing ([50f9878](https://github.com/phdah/ava/commit/50f9878f2d6bcae9c3dd92b78ff67943438d7a2d))
* **ci:** set release workflow Python path ([#42](https://github.com/phdah/ava/issues/42)) ([b444343](https://github.com/phdah/ava/commit/b4443438200e83cf2b00b945b8457ca2b3de79a2))
* enforce faithful inbox ingestion completion ([#67](https://github.com/phdah/ava/issues/67)) ([5d9facb](https://github.com/phdah/ava/commit/5d9facb0302107f1d6a3c5d0436622245d86e7ff))
* enforce reviewed project-owned semantic impact ([#64](https://github.com/phdah/ava/issues/64)) ([2158a51](https://github.com/phdah/ava/commit/2158a5115589c4ab26937284099afc5a855330e0))
* enforce role routing before every response ([#70](https://github.com/phdah/ava/issues/70)) ([0a8db33](https://github.com/phdah/ava/commit/0a8db33f21735d54c428fc981a33eafa14957282))
* **installer:** remove empty transaction containers ([#62](https://github.com/phdah/ava/issues/62)) ([9dc481a](https://github.com/phdah/ava/commit/9dc481a955ad13fb3b7d8cc43da322934b59dca6))
* make knowledge hierarchy promotion predictable ([#65](https://github.com/phdah/ava/issues/65)) ([626cd30](https://github.com/phdah/ava/commit/626cd307e03deb26cf3ba14c904d42073dd13f9f))
* **release:** configure grouped release PR title ([#43](https://github.com/phdah/ava/issues/43)) ([8e2dacc](https://github.com/phdah/ava/commit/8e2dacc54f7b197991e55d3f14f05511fa1fbe46))
* **release:** enforce release PR upgrade edges ([#56](https://github.com/phdah/ava/issues/56)) ([a02dfa6](https://github.com/phdah/ava/commit/a02dfa6ede89724ae96c79433ff0ae4761d3a3a7))
* **release:** make release PR completion generic ([#60](https://github.com/phdah/ava/issues/60)) ([eabfec0](https://github.com/phdah/ava/commit/eabfec0209904dfe616af2bc38cb341d09c3d833))
* **release:** repair qualification validation ([#44](https://github.com/phdah/ava/issues/44)) ([ac51f15](https://github.com/phdah/ava/commit/ac51f152015678b0dd019e534e12073ad770eb5e))
* **release:** validate installed context links ([#53](https://github.com/phdah/ava/issues/53)) ([6fc4320](https://github.com/phdah/ava/commit/6fc4320c4fa9a0e5a078b93023e3e5562c5eac04))
* **release:** wire upgrade-sources.txt into release workflow assembler call ([#50](https://github.com/phdah/ava/issues/50)) ([a26e798](https://github.com/phdah/ava/commit/a26e7982131ffac9235a1860af772d757a9d5191))

## [1.0.0-alpha.10](https://github.com/phdah/ava/compare/v1.0.0-alpha.9...v1.0.0-alpha.10) (2026-08-07)


### Bug Fixes

* enforce faithful inbox ingestion completion ([#67](https://github.com/phdah/ava/issues/67)) ([d02e1ac](https://github.com/phdah/ava/commit/d02e1ac5328f78b47418047ff9eb3d5f63e54c75))
* make knowledge hierarchy promotion predictable ([#65](https://github.com/phdah/ava/issues/65)) ([071a646](https://github.com/phdah/ava/commit/071a6463955dbdc19e9b8a250996d68816186b9c))

## [1.0.0-alpha.9](https://github.com/phdah/ava/compare/v1.0.0-alpha.8...v1.0.0-alpha.9) (2026-08-06)


### Bug Fixes

* enforce reviewed project-owned semantic impact ([#64](https://github.com/phdah/ava/issues/64)) ([e64ebef](https://github.com/phdah/ava/commit/e64ebefb80c116ef10cc287e159509e544f829db))
* **installer:** remove empty transaction containers ([#62](https://github.com/phdah/ava/issues/62)) ([b18b751](https://github.com/phdah/ava/commit/b18b751348fc0d8e78e003d0696b063a1217ebf0))

## [1.0.0-alpha.8](https://github.com/phdah/ava/compare/v1.0.0-alpha.7...v1.0.0-alpha.8) (2026-08-06)


### Bug Fixes

* **release:** make release PR completion generic ([#60](https://github.com/phdah/ava/issues/60)) ([0652978](https://github.com/phdah/ava/commit/065297888b7211737e3eda7e7985825062913987))

## [1.0.0-alpha.7](https://github.com/phdah/ava/compare/v1.0.0-alpha.6...v1.0.0-alpha.7) (2026-08-05)


### Bug Fixes

* **release:** enforce release PR upgrade edges ([#56](https://github.com/phdah/ava/issues/56)) ([b5507bb](https://github.com/phdah/ava/commit/b5507bb5c96baf771aa98146c4cf583b123887f7))

## [1.0.0-alpha.6](https://github.com/phdah/ava/compare/v1.0.0-alpha.5...v1.0.0-alpha.6) (2026-08-05)


### Bug Fixes

* **release:** validate installed context links ([#53](https://github.com/phdah/ava/issues/53)) ([3081008](https://github.com/phdah/ava/commit/30810083aabd149ee63e017dc2a2cd265683b1af))

## [1.0.0-alpha.5](https://github.com/phdah/ava/compare/v1.0.0-alpha.4...v1.0.0-alpha.5) (2026-08-05)


### Bug Fixes

* **release:** wire upgrade-sources.txt into release workflow assembler call ([#50](https://github.com/phdah/ava/issues/50)) ([af7b258](https://github.com/phdah/ava/commit/af7b2587f756009ac743289e920488690091b0d3))

## [1.0.0-alpha.4](https://github.com/phdah/ava/compare/v1.0.0-alpha.3...v1.0.0-alpha.4) (2026-08-05)


### Features

* **release:** publish qualified releases automatically ([#46](https://github.com/phdah/ava/issues/46)) ([08f3523](https://github.com/phdah/ava/commit/08f3523559255508ef8efb866e4fea1fb209de47))

## [1.0.0-alpha.3](https://github.com/phdah/ava/compare/v1.0.0-alpha.2...v1.0.0-alpha.3) (2026-08-04)


### Bug Fixes

* **release:** repair qualification validation ([#44](https://github.com/phdah/ava/issues/44)) ([1bac03c](https://github.com/phdah/ava/commit/1bac03ca9cb1e23698fada56611db6ececbe0347))

## [1.0.0-alpha.2](https://github.com/phdah/ava/compare/v1.0.0-alpha.1...v1.0.0-alpha.2) (2026-08-04)


### Features

* add project steward role ([defad53](https://github.com/phdah/ava/commit/defad53018e8c1a41b397cd8a0987244d23a9552))
* add project steward role ([7c6b0ab](https://github.com/phdah/ava/commit/7c6b0ab96e0385c883b87ca141751067b926540e))
* add project steward role ([774e9c9](https://github.com/phdah/ava/commit/774e9c918979a49406b8e5977e3ba15c0d83cfbd))
* add project steward role ([6cc011f](https://github.com/phdah/ava/commit/6cc011f03f49c5234b357e34a29832548ce7898e))
* add project steward role ([dc5df6f](https://github.com/phdah/ava/commit/dc5df6f371e8d2d2daa25c62f278359d5dfa3de3))
* add project steward role ([4d95bae](https://github.com/phdah/ava/commit/4d95bae463855da2bbad4f7afbfa8eeac4437a41))
* add project steward role ([8fbf54e](https://github.com/phdah/ava/commit/8fbf54e443a0c11be4c4c4b43983b2e38847029c))
* add project steward role ([830e35c](https://github.com/phdah/ava/commit/830e35c2208ebcb55cc7a31000f1a8d081e7bfc6))
* **release:** force first alpha proposal ([#38](https://github.com/phdah/ava/issues/38)) ([70aca3c](https://github.com/phdah/ava/commit/70aca3c7f9e9ed2b3084f82d530f06282c4de5cc))


### Bug Fixes

* align project steward routing ([174f878](https://github.com/phdah/ava/commit/174f8788df8343f81ae569ea615f3b3152dbd1ab))
* align project steward routing ([a56d4b9](https://github.com/phdah/ava/commit/a56d4b901f5ecde80c356c13f9a2c9121089080c))
* align project steward routing ([cd5cbe8](https://github.com/phdah/ava/commit/cd5cbe856953354f316a14b23fd8957ac33aee20))
* align project steward routing ([220cf57](https://github.com/phdah/ava/commit/220cf576253d8d6d4a8ed11a6f01d78a09e45482))
* **ci:** set release workflow Python path ([#42](https://github.com/phdah/ava/issues/42)) ([aa32868](https://github.com/phdah/ava/commit/aa32868fa469e15f860274194d8db86b286b96b2))
* **release:** configure grouped release PR title ([#43](https://github.com/phdah/ava/issues/43)) ([d27d899](https://github.com/phdah/ava/commit/d27d899a3b6eb53d8d54fd83d68deae3fea288b0))

## 1.0.0-alpha.1 (2026-08-04)


### Features

* **release:** force first alpha proposal ([#38](https://github.com/phdah/ava/issues/38)) ([70aca3c](https://github.com/phdah/ava/commit/70aca3c7f9e9ed2b3084f82d530f06282c4de5cc))

## Changelog

Ava release notes are maintained by release-please from validated Conventional Commit pull-request titles.

`0.0.0` is an internal bootstrap sentinel. It is not a published or supported Ava release. The first managed release is `1.0.0-alpha.1`.
