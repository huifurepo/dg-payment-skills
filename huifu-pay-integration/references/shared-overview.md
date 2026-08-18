# 汇付支付资料总览

本页只负责支付产品线导航。详细字段、代码和通知规则读取对应原子 reference。

## 什么时候读取

- 首次接入且不知道选聚合支付、托管支付或 checkout-js。
- 需要判断服务端、前端和最终状态确认的职责。
- 存量项目需要确定增量改造入口。

## 产品线

| 需求 | 产品线 | 首选入口 |
| --- | --- | --- |
| 服务端直接下单、扫码、查单、退款 | 聚合支付 | `aggregation-quickstart.md` |
| H5/PC、小程序、抖音或托管项目 | 托管支付 | `hostingpay-quickstart.md` |
| 已完成托管预下单，只嵌入前端组件 | checkout-js | `checkout-js.md` |
| 已有订单、支付、回调或状态机 | 存量增量接入 | `copilot-existing-system.md` |

## 公共资料

| 主题 | reference |
| --- | --- |
| 签名和验签 | `shared-signing-v2.md` |
| 请求头 | `shared-request-header-policy.md` |
| 请求字段保留 | `shared-request-field-preservation.md` |
| 支付通知 | `shared-async-notify.md` |
| 控台 Webhook | `shared-webhook-signing.md` |
| SDK | `shared-server-sdk-matrix.md` |
| 本地沙箱 | `shared-local-sandbox.md` |

## 深层资料索引

以下原子资料只在命中相应实现问题时读取，不应一次性加载：

| 主题 | reference |
| --- | --- |
| 聚合下单最小流程、请求和错误 | `aggregation-order-quickstart.md`、`aggregation-order-request.md`、`aggregation-order-errors.md` |
| 聚合 Java 与退款快速接入 | `aggregation-java-adapter.md`、`aggregation-refund-quickstart.md` |
| 聚合查单快速接入 | `aggregation-query-quickstart.md` |
| 托管预下单快速接入与 Java | `hostingpay-preorder-quickstart.md`、`hostingpay-java-adapter.md` |
| 托管查询、关单和对账 | `hostingpay-query-quickstart.md`、`hostingpay-query-trade-close.md`、`hostingpay-query-reconciliation.md` |
| checkout-js 组件、流程和框架 | `checkout-js-readme.md`、`checkout-js-component-modes.md`、`checkout-js-integration-flow.md`、`checkout-js-framework-integration-notes.md` |
| 凭据与前端 SDK 边界 | `shared-credential-boundary.md`、`shared-frontend-sdk-matrix.md` |
| 维护者回归提示 | `canonical-regression-prompts.md` |

## 边界

- 同步成功、页面回跳和前端 callback 不是支付终态。
- 支付终态依赖验签通知与主动查单补偿。
- 本地沙箱不证明真实权限、通道、费率、风控、资金或生产准入。
- 企业/个人商户进件、图片、业务开通、详情和申请状态使用 `$huifu-merchant-onboarding`。

## 当前版本

支付 Skill 为 `1.3.4`。Java/PHP/Python 基线分别见 `shared-server-sdk-matrix.md`。`skill_source` 默认值与当前包版本同步为 `hfps/1.3.4`，显式合同值仍优先原样透传。
