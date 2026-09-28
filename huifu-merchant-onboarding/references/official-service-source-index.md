# 商户进件官方来源索引

普通回答使用本地 references；以下 URL 只用于来源追溯、维护刷新和显式联网核验。

## 十三接口来源

| 接口 | 官方原始地址 | 当前 SHA-256 |
| --- | --- | --- |
| 企业商户进件 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md | `6606629100f94813a7a4238c8f1ffc970ec3b905d1af9487bb92baee6138822e` |
| 个人商户进件 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md | `09862a3923b114abcf7dbc9e7545798481abc37f88b6eb64911ce7d53f9f5437` |
| 商户业务开通 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md | `9c3f2262c295489abc5ce32bf123128cfd7376c4d5e35399c5083e39ff206c5c` |
| 图片上传 | https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json | `bf2c22fc745b343e44c557daeda5c6013e7863302a5b910f0ceabc23d895c1f4` |
| 商户详情查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md | `df6014a1fc008bd81dff8de5708432010c60b002d34d0d9602a67145d1ae8806` |
| 申请状态查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md | `8c39b88e199d2c877267994172fa09de5130c47d38eb5f01147d2d1520c2bef4` |
| 商户业务开通修改 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md | `9dea690376cdf85cf6007e302900111a16f00bd92ab2a8335ca56eaaee9d491d` |
| 商户基本信息修改 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md | `f2146bc553eb4b1dc8c88d4487eb1b5c721468d6a8eec5be7d0ce9f086db4d6c` |
| 商户费率信息查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md | `20a3be9f505c542a716bbdad65da146f9089be05b206850c089c6df4e9ac050e` |
| 商户状态变更 | https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md | `d2fe6ab4404abd79b3ac5f5eecffaaec9d61d245ac1a60ebccddee889535a07f` |
| 商户短信发送 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md | `6982fe07d276cbb0739c9c205afbc5b238dd6d72422154efd6248932aa459b54` |
| 商户多费率配置 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md | `e4b23cb9bfaf59e9a88448a890f539d7ee9cbf7002d763a7d078294053aa7473` |
| 商户多费率配置查询 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md | `e2c0f53e77a1ef00827cc8be28ac688c068e5c8a4dc9f741845b841dcd16881a` |

核验快照：`2026-09-22`。十三接口相对 `2026-09-15` 有十页原文字节变化，完整路径新增82、删除79、同路径属性变化194，总计2,210个字段路径（请求1,277、响应753、异步180）。重点包括原生 `fee_rate_type:Array<string>`、材料必填/长度修正及冲突、JSON 容器形态与微信费率材料路径；历史快照保持不可变。

辅助公共资料（不计入上述13个接口快照）：[基础参数汇总](https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md)、[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)、[名词解释](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_mcjs.md)。它们用于公共编码、返回码全集和术语释义，不能覆盖具体接口页的字段类型、长度、必填性、层级或通知结构。

## 使用规则

1. 官网 URL 不列入“本轮实际使用的 references”。
2. 当前本地目录是冻结快照，不自动代表官网未来版本。
3. 字段说明引用外部编码、XLSX、协议或第三方资料时，读取 `merchant-onboarding-external-resources.md`。
4. 未读取外部正文时明确要求人工核验，不根据文件名猜规则。
5. 刷新来源时必须记录 URL、获取时间、SHA 和字段 delta。
