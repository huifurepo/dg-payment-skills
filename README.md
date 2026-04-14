# 汇付支付 Skill 产品包

这是一个面向第三方客户的 Huifu 接入 Skill 包，用来帮助开发者借助 AI 工具完成 SDK 接入开发。

README 按 **产品线 → 开发任务 → 技术栈** 导航，先帮你定位入口，再进入对应 Skill。当前仓库同时覆盖：

- 服务端 Skill：Java、PHP、C#、Python、Go
- 前端支付组件：Node.js / Browser
- 产品能力主线：聚合支付、托管支付、前端支付组件

> 选择建议：优先使用聚合支付，接入更快、更轻量；当你需要托管收银台、项目制预下单或前端 checkout 能力时，再进入托管支付和前端支付组件路径。

## 如何开始

### 1. 先按产品线定位

| 产品线         | 适合什么场景                         | 从这里开始                                                             |
| ----------- | ------------------------------ | ----------------------------------------------------------------- |
| 汇付支付集成（总入口） | 第一次接入汇付、需要先判断产品线 / 开发任务 / 阅读顺序 | [huifu-payment-integration](huifu-payment-integration/)           |
| 聚合支付        | 标准支付场景，想尽快完成服务端接入              | [huifu-dougong-aggregation-base](huifu-dougong-aggregation-base/)     |
| 托管支付（服务端）   | 需要项目制预下单、托管收银台、服务端查询/退款闭环      | [huifu-dougong-hostingpay-base](huifu-dougong-hostingpay-base/)       |
| 前端支付组件      | 需要在商户自有页面嵌入 checkout 或单支付按钮    | [huifu-dougong-hostingpay-checkout-js](huifu-dougong-hostingpay-checkout-js/) |

### 2. 再按开发任务进入

| 开发任务            | 聚合支付                                                                          | 托管支付 / 前端支付组件                                                           |
| --------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 初始化 / 公共配置      | [huifu-dougong-aggregation-base](huifu-dougong-aggregation-base/)                 | [huifu-dougong-hostingpay-base](huifu-dougong-hostingpay-base/)             |
| 下单 / 预下单        | [huifu-dougong-aggregation-order](huifu-dougong-aggregation-order/)   | [huifu-dougong-hostingpay-cashier-preorder](huifu-dougong-hostingpay-cashier-preorder/)   |
| 查询 / 关单 / 对账    | [huifu-dougong-aggregation-query](huifu-dougong-aggregation-query/)   | [huifu-dougong-hostingpay-cashier-query](huifu-dougong-hostingpay-cashier-query/)   |
| 退款              | [huifu-dougong-aggregation-refund](huifu-dougong-aggregation-refund/) | [huifu-dougong-hostingpay-cashier-refund](huifu-dougong-hostingpay-cashier-refund/) |
| 收银台组件接入 / 单支付按钮 | 不适用                                                                           | [huifu-dougong-hostingpay-checkout-js](huifu-dougong-hostingpay-checkout-js/)       |

### 3. 最后按技术栈落地

#### 服务端技术栈

| 技术栈    | 推荐入口                                                                                                         | 说明        |
| ------ | ------------------------------------------------------------------------------------------------------------ | --------- |
| Java   | [huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md) | 当前资料最完整   |
| PHP    | [huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md) | 先走统一服务端入口 |
| C#     | [huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md) | 先走统一服务端入口 |
| Python | [huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md) | 先走统一服务端入口 |
| Go     | [huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md) | 先走统一服务端入口 |

#### 前端技术栈

| 技术栈               | 推荐入口                                                                                                             | 说明                              |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| Node.js / Browser | [huifu-dougong-pay-shared-base/runtime/frontend-sdk-matrix.md](huifu-dougong-pay-shared-base/runtime/frontend-sdk-matrix.md) | 前端 JS SDK 能力矩阵                  |
| Node.js / Browser | [huifu-dougong-hostingpay-checkout-js](huifu-dougong-hostingpay-checkout-js/)                                                | 嵌入 checkout / 单支付按钮的实际 Skill 入口 |

## 产品线说明

### 聚合支付

聚合支付是一条服务端主线，适合标准支付接入和快速上线。

推荐阅读顺序：

1. [huifu-dougong-aggregation-base](huifu-dougong-aggregation-base/)
2. [huifu-dougong-aggregation-order](huifu-dougong-aggregation-order/)
3. [huifu-dougong-aggregation-query](huifu-dougong-aggregation-query/)
4. [huifu-dougong-aggregation-refund](huifu-dougong-aggregation-refund/)（按需）

### 托管支付

托管支付的服务端主线负责 SDK 初始化、预下单、查询、关单、对账和退款。

推荐阅读顺序：

1. [huifu-dougong-hostingpay-base](huifu-dougong-hostingpay-base/)
2. [huifu-dougong-hostingpay-cashier-preorder](huifu-dougong-hostingpay-cashier-preorder/)
3. [huifu-dougong-hostingpay-cashier-query](huifu-dougong-hostingpay-cashier-query/)
4. [huifu-dougong-hostingpay-cashier-refund](huifu-dougong-hostingpay-cashier-refund/)（按需）

### 前端支付组件

前端支付组件是一条独立能力线，不只是“跳转托管页说明”。

[huifu-dougong-hostingpay-checkout-js](huifu-dougong-hostingpay-checkout-js/) 负责：

- 在商户自定义页面中嵌入 `checkout` 组件或单支付按钮
- 让商户自己控制页面布局、品牌样式和交互流程
- 通过前端 callback 接收支付流程事件
- 与服务端预下单、查询、异步通知一起完成闭环

必须注意：前端 callback 不等于最终支付成功，最终订单状态仍应由服务端查询或异步通知确认。

推荐主链路：

1. 服务端在 [huifu-dougong-hostingpay-cashier-preorder](huifu-dougong-hostingpay-cashier-preorder/) 完成预下单
2. 前端在 [huifu-dougong-hostingpay-checkout-js](huifu-dougong-hostingpay-checkout-js/) 渲染 checkout / 按钮
3. 服务端在 [huifu-dougong-hostingpay-cashier-query](huifu-dougong-hostingpay-cashier-query/) 做最终确认

## 共享资料层

这些共享资料不再分散在各个 Skill 中重复维护：

| 资料                                                                                                                 | 作用           |
| ------------------------------------------------------------------------------------------------------------------ | ------------ |
| [huifu-dougong-pay-shared-base/protocol/signing-v2.md](huifu-dougong-pay-shared-base/protocol/signing-v2.md)                   | V2 签名规则      |
| [huifu-dougong-pay-shared-base/protocol/async-notify.md](huifu-dougong-pay-shared-base/protocol/async-notify.md)               | 异步通知规则       |
| [huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md)       | 服务端多语言矩阵     |
| [huifu-dougong-pay-shared-base/runtime/frontend-sdk-matrix.md](huifu-dougong-pay-shared-base/runtime/frontend-sdk-matrix.md)   | 前端 JS SDK 矩阵 |
| [huifu-dougong-pay-shared-base/governance/versioning-policy.md](huifu-dougong-pay-shared-base/governance/versioning-policy.md) | 版本治理规则       |
| [huifu-dougong-pay-shared-base/governance/release-checklist.md](huifu-dougong-pay-shared-base/governance/release-checklist.md) | 发布检查清单       |

## 已发布 Skill 列表

### 总入口

| Skill                                                   | 功能                             | 前置依赖                    |
| ------------------------------------------------------- | ------------------------------ | ----------------------- |
| [huifu-payment-integration](huifu-payment-integration/) | 汇付支付总入口：产品线判断、任务路由、阅读顺序、关键边界提醒 | huifu-dougong-pay-shared-base |

### 共享基础资料

| Skill                                               | 功能                      | 前置依赖 |
| --------------------------------------------------- | ----------------------- | ---- |
| [huifu-dougong-pay-shared-base](huifu-dougong-pay-shared-base/) | 共享协议层、运行时矩阵、版本治理和发布检查入口 | 无    |

### 聚合支付

| Skill                                                                         | 功能                                | 前置依赖                         |
| ----------------------------------------------------------------------------- | --------------------------------- | ---------------------------- |
| [huifu-dougong-aggregation-base](huifu-dougong-aggregation-base/)                 | 公共基座：SDK 初始化、Factory 模式、支付类型、公共参数 | huifu-dougong-pay-shared-base      |
| [huifu-dougong-aggregation-order](huifu-dougong-aggregation-order/)   | 聚合支付下单：微信 / 支付宝 / 银联全场景           | huifu-dougong-aggregation-base |
| [huifu-dougong-aggregation-query](huifu-dougong-aggregation-query/)   | 交易查询、关单、关单查询、对账单                  | huifu-dougong-aggregation-base |
| [huifu-dougong-aggregation-refund](huifu-dougong-aggregation-refund/) | 退款申请、退款结果查询                       | huifu-dougong-aggregation-base |

### 托管支付（服务端）

| Skill                                                                   | 功能                          | 前置依赖                        |
| ----------------------------------------------------------------------- | --------------------------- | --------------------------- |
| [huifu-dougong-hostingpay-base](huifu-dougong-hostingpay-base/)             | 公共基座：SDK 初始化、技术规范、公共参数、错误码  | huifu-dougong-pay-shared-base     |
| [huifu-dougong-hostingpay-cashier-preorder](huifu-dougong-hostingpay-cashier-preorder/)   | 服务端预下单：H5 / PC、支付宝小程序、微信小程序 | huifu-dougong-hostingpay-base |
| [huifu-dougong-hostingpay-cashier-query](huifu-dougong-hostingpay-cashier-query/)   | 服务端查询、关单、对账单                | huifu-dougong-hostingpay-base |
| [huifu-dougong-hostingpay-cashier-refund](huifu-dougong-hostingpay-cashier-refund/) | 服务端退款申请、退款结果查询              | huifu-dougong-hostingpay-base |

### 前端支付组件

| Skill                                                             | 功能                                                  | 前置依赖                                                          |
| ----------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------- |
| [huifu-dougong-hostingpay-checkout-js](huifu-dougong-hostingpay-checkout-js/) | 商户自定义页面 + 嵌入式 checkout / 单支付按钮 + 前端事件回调 + 服务端最终确认协作 | huifu-dougong-hostingpay-base, huifu-dougong-hostingpay-cashier-preorder |

## 目录结构

```text
├── README.md
├── CHANGELOG.md
├── LICENSE
├── scripts/
├── huifu-payment-integration/
├── huifu-dougong-pay-shared-base/
├── huifu-dougong-aggregation-base/
├── huifu-dougong-aggregation-order/
├── huifu-dougong-aggregation-query/
├── huifu-dougong-aggregation-refund/
├── huifu-dougong-hostingpay-base/
├── huifu-dougong-hostingpay-cashier-preorder/
├── huifu-dougong-hostingpay-checkout-js/
├── huifu-dougong-hostingpay-cashier-query/
└── huifu-dougong-hostingpay-cashier-refund/
```

## 推荐接入主链路

### 聚合支付

```text
① huifu-dougong-aggregation-base
       ↓
② huifu-dougong-aggregation-order
       ↓
③ huifu-dougong-aggregation-query
       ↓
④ huifu-dougong-aggregation-refund（按需）
```

### 托管支付 + 前端支付组件

```text
① huifu-dougong-hostingpay-base
       ↓
② huifu-dougong-hostingpay-cashier-preorder     服务端预下单
       ↓
③ huifu-dougong-hostingpay-checkout-js       商户页面嵌入 checkout / 按钮
       ↓
④ huifu-dougong-hostingpay-cashier-query     服务端最终确认
       ↓
⑤ huifu-dougong-hostingpay-cashier-refund（按需）
```

## 文档说明

- 优先阅读各 Skill 目录下的 `SKILL.md` 与 `references/` 文档。
- 服务端接入优先从 base Skill 和 `server-sdk-matrix.md` 开始。
- 前端接入优先从 `frontend-sdk-matrix.md` 和 `huifu-dougong-hostingpay-checkout-js` 开始。
- AI 生成接入代码时，不应自行猜测商户参数、项目配置或最终支付状态。

## 官方技术支持

如需官方技术支持或接入答疑，可通过以下官方渠道联系：

- 客服电话：400-820-2819
- 官方邮箱：<cs@huifu.com>

企业微信技术支持群（仅用于接入答疑 / 技术支持）：

![汇付官方企业微信技术支持群二维码](huifu-payment-integration/references/qywx_goutong.png)

> 若二维码失效，请优先通过客服电话或官方邮箱联系。

