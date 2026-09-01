# 商户进件官方来源索引

普通回答使用本地 references；以下 URL 只用于来源追溯、维护刷新和显式联网核验。

## 十三接口来源

| 接口 | 官方原始地址 | 当前 SHA-256 |
| --- | --- | --- |
| 企业商户进件 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md | `ae2744b9142fe463010b4a9d66a89b0c5ef3e84576f87a553bc59331dd868415` |
| 个人商户进件 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md | `03c5059bc4ad2aea832fe98bee356bf199e28bc27c74be22ef641e84af0d7d36` |
| 商户业务开通 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md | `9b62bba487f981bbdd293f0328a68b3c8c526b1fa1d47a8ab7b8912b427b6ec5` |
| 图片上传 | https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json | `e1acf74e60436d069f3c605c19b24aab6d703494e1ebdd8c90b11104e4646125` |
| 商户详情查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md | `8f1b46ae924919fac886d9f96ad3da3b2fbb7d48aae892e8ac236ea15bb1e66a` |
| 申请状态查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md | `89f51fdbca529b1f7166aeba1d5d24eb16469fd153cd09cafbf811d9e68f050f` |
| 商户业务开通修改 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md | `51a11858b9d312a3e6112f6abf91e1b9a1dbb1db4ed4f4dd27fa14950094d1d9` |
| 商户基本信息修改 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md | `458f021fa0e626133d17a65ce1fee21aa445d45b75493c00740562c3c64259c6` |
| 商户费率信息查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md | `c9bfb5ed774cf8bce622bb536d16b1ed60ffedd5bd5540bf83177cdf592008b9` |
| 商户状态变更 | https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md | `d2fe6ab4404abd79b3ac5f5eecffaaec9d61d245ac1a60ebccddee889535a07f` |
| 商户短信发送 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md | `562e269268e10248931e0c9ed556a99e88966ddd953b67333f9a106df5934bc3` |
| 商户多费率配置 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md | `0536049a616e68929341d4176cf1c5348b1bcf8fabeff3ceb384945fa5dce987` |
| 商户多费率配置查询 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md | `6a5b970177f67985f1ce20c6b2900580117496f870c97c3391055afaaa66438f` |

核验快照：`2026-08-31`。十三接口均已逐页重新下载并锁定；本轮七页发生变化，商户目录由2,155增至2,183个字段路径。企业新增 `head_type` 并调整材料，业务开通及修改分别新增10个捷行付/线上费率字段，详情新增8个响应字段，多费率两页修正长度、String(JSON) 与场景说明。历史快照保持不可变。

辅助公共资料（不计入上述13个接口快照）：[基础参数汇总](https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md)、[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)、[名词解释](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_mcjs.md)。它们用于公共编码、返回码全集和术语释义，不能覆盖具体接口页的字段类型、长度、必填性、层级或通知结构。

## 使用规则

1. 官网 URL 不列入“本轮实际使用的 references”。
2. 当前本地目录是冻结快照，不自动代表官网未来版本。
3. 字段说明引用外部编码、XLSX、协议或第三方资料时，读取 `merchant-onboarding-external-resources.md`。
4. 未读取外部正文时明确要求人工核验，不根据文件名猜规则。
5. 刷新来源时必须记录 URL、获取时间、SHA 和字段 delta。
