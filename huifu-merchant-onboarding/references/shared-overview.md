# 商户进件资料总览

本页只负责进件能力导航。详细字段必须读取原子接口页、完整字段目录和字段合同。

## 什么时候读取

- 用户尚未明确企业、个人、业务开通/修改、基本资料修改、图片、费率、短信、详情或状态任务。
- 需要判断最小阅读链路。
- 需要确认支付交易问题应交接到哪个 Skill。

## 能力地图

| 目标 | 首选 reference |
| --- | --- |
| 企业商户开户 | `merchant-onboarding-enterprise.md` |
| 无执照个人商户开户 | `merchant-onboarding-individual.md` |
| 图片资料 | `merchant-onboarding-image-upload.md` |
| 支付、分账等业务能力开通 | `merchant-onboarding-business-open.md` |
| 查询商户完整配置 | `merchant-onboarding-detail-query.md` |
| 查询申请、绑卡、结算等状态 | `merchant-onboarding-application-status-query.md` |
| 修改已开通业务或费率 | `merchant-onboarding-business-open-modify.md` |
| 修改商户基础资料 | `merchant-onboarding-basic-info-modify.md` |
| 查询商户费率配置 | `merchant-onboarding-rate-query.md` |
| 开通或关闭商户状态 | `merchant-onboarding-status-change.md` |
| 发送或核验商户短信验证码 | `merchant-onboarding-sms-send.md` |
| 完整字段和嵌套路径 | `merchant-onboarding-complete-field-catalog.md` |
| 条件、互斥、冲突和 SDK 边界 | `merchant-onboarding-field-contracts.md` |
| 外部编码、XLSX、协议和第三方资料 | `merchant-onboarding-external-resources.md` |

## 补充资料

| 主题 | reference |
| --- | --- |
| 调用方请求字段保留 | `shared-request-field-preservation.md` |
| 维护者回归提示 | `canonical-regression-prompts.md` |

## 固定边界

- `huifu_id` 已返回不等于支付能力已经可用。
- 业务开通结果必须按逐业务状态判断，不能只看同步受理。
- 本 Skill 不实现支付下单、退款、对账、checkout-js 或支付终态；这些能力交接给 `$huifu-pay-integration`。
- 未确认的图片本地文件流和通知协议只输出确认清单。

## 当前来源

当前字段快照复审于 `2026-08-10`，十一接口共 2,111 个字段路径。企业进件、个人进件和基本信息修改页仅补全 `activated_products` 的 `01=一体化收款产品`、`02=账户与资金产品`、`03=业财数通产品` 说明，字段、类型、必填性和嵌套均未变化；此前同步的 `upper_huifu_id:String(18) C`、门店图片条件及 `material_card_info` 路径继续保留。官网 URL 只用于来源追溯和维护刷新，不计入普通回答的本轮 references。
