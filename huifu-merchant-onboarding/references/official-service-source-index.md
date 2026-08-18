# 商户进件官方来源索引

普通回答使用本地 references；以下 URL 只用于来源追溯、维护刷新和显式联网核验。

## 十一接口来源

| 接口 | 官方原始地址 | 当前 SHA-256 |
| --- | --- | --- |
| 企业商户进件 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md | `38e7958dd7370796f713558325f33ea92aff34c303f3430bc329c7b611f20e78` |
| 个人商户进件 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md | `3b3f9b47fd55120a4c8f2b4876cc1bdbd4ada9e15d2995bc261d74b88dba1867` |
| 商户业务开通 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md | `1ef4ed0e644a0631e144dbb280482e03f596c1f470f43a26b59d3e063e56490c` |
| 图片上传 | https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json | `e1acf74e60436d069f3c605c19b24aab6d703494e1ebdd8c90b11104e4646125` |
| 商户详情查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md | `36d713243329871a4703aa414e9edb2e06e84ea6be484eecae3eaace46ea3d8d` |
| 申请状态查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md | `89f51fdbca529b1f7166aeba1d5d24eb16469fd153cd09cafbf811d9e68f050f` |
| 商户业务开通修改 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md | `fdeaaa0a40556046d817c70a46c2fe1c71756f8648ffe640db6585ca6f5963a3` |
| 商户基本信息修改 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md | `458f021fa0e626133d17a65ce1fee21aa445d45b75493c00740562c3c64259c6` |
| 商户费率信息查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md | `c9bfb5ed774cf8bce622bb536d16b1ed60ffedd5bd5540bf83177cdf592008b9` |
| 商户状态变更 | https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md | `d2fe6ab4404abd79b3ac5f5eecffaaec9d61d245ac1a60ebccddee889535a07f` |
| 商户短信发送 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md | `562e269268e10248931e0c9ed556a99e88966ddd953b67333f9a106df5934bc3` |

核验日期：`2026-08-10`。企业进件、个人进件和商户基本信息修改页相对 `2026-07-29` 快照有变化，官网均标最近更新时间 `2026.08.07`；除动态扩展表标识外，唯一业务语义变化是三条 `request.data.activated_products` 说明补全为 `01：一体化收款产品，02：账户与资金产品，03：业财数通产品`。字段数量、完整路径、类型、长度、Y/N/C 和嵌套均未变化；此前的 `upper_huifu_id` 条件、门店图片条件及 `material_card_info` 刷新继续保留。

辅助公共资料（不计入上述 11 个接口快照）：[基础参数汇总](https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md)、[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)、[名词解释](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_mcjs.md)。它们用于公共编码、返回码全集和术语释义，不能覆盖具体接口页的字段类型、长度、必填性、层级或通知结构。

## 使用规则

1. 官网 URL 不列入“本轮实际使用的 references”。
2. 当前本地目录是冻结快照，不自动代表官网未来版本。
3. 字段说明引用外部编码、XLSX、协议或第三方资料时，读取 `merchant-onboarding-external-resources.md`。
4. 未读取外部正文时明确要求人工核验，不根据文件名猜规则。
5. 刷新来源时必须记录 URL、获取时间、SHA 和字段 delta。
