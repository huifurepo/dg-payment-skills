---
name: huifu-payment-integration
display_name: 汇付支付集成
description: 汇付支付斗拱SDK接入总入口 Skill。用于帮助开发者和 AI 在聚合支付、托管支付、前端 checkout、查询、退款与共享协议资料之间做正确路由，先完成场景判断，再进入对应的基础 Skill 和业务 Skill。
version: 1.1.0
author: "jiaxiang.li | 内容版权：上海汇付支付有限公司"
homepage: https://paas.huifu.com/open/home/index.html
license: CC-BY-NC-4.0
compatibility:
  - skillhub
dependencies:
  - huifu-dougong-pay-shared-base
metadata:
  skillhub:
    requires:
      config: []
---

> **版权声明**：本 Skill 内容来源于上海汇付支付有限公司官方开放平台文档及当前仓库已整理的接入资料，版权归属上海汇付支付有限公司。如有疑问可咨询汇付支付客服：400-820-2819 / cs@huifu.com
>
> **Source**: Official Open Platform documentation of Shanghai Huifu Payment Co., Ltd.
>
> **Copyright**: Shanghai Huifu Payment Co., Ltd.

---

# 汇付支付集成

这个 Skill 是汇付支付接入的总入口。  
它不直接代替聚合支付、托管支付、前端 checkout、查询、退款等具体 Skill，而是先帮助开发者和 AI 判断当前场景应该进入哪条路径，再路由到对应的基础 Skill 和业务 Skill。

## 适配版本与定位

| 项目 | 内容 |
| --- | --- |
| Skill 版本 | `1.1.0` |
| Skill 定位 | 汇付支付接入总入口 / 总导航 / 场景分诊入口 |
| 适用范围 | 聚合支付、托管支付、前端 checkout、共享协议资料导航 |
| 不承担职责 | 具体字段表、语言 SDK 代码细节、单接口完整说明 |

## 适用场景

当你遇到以下问题时，先使用本 Skill：

- 第一次接触汇付支付，不确定该走**聚合支付**还是**托管支付**
- 已明确要接汇付，但不确定当前任务属于**初始化、下单、查询、退款、异步通知处理**还是**前端 checkout**
- 想先理解汇付支付的产品路径、前后端职责和推荐阅读顺序
- 想让 AI 帮忙接入汇付，但希望先锁定正确入口，避免直接猜场景、猜参数来源
- 需要一个对外可独立理解、对内可路由到已发布 skills 的总门户

## 不适用场景

以下情况请直接进入对应子 Skill：

- 已明确知道自己要做**聚合支付下单**、**托管预下单**、**查询**或**退款**
- 需要查看具体接口的**字段级参数表**
- 需要某个语言 SDK 的**初始化方式或调用代码**
- 需要查看**签名规则、异步通知规则、服务端/前端 SDK 矩阵**的完整细节
- 需要处理当前仓库未覆盖的更深层主题

## 快速决策树

```text
用户要接入汇付支付
        |
        +-- 先判断你要做什么？
        |       +-- 先看整体路径 / 不知道选哪条线 --> 当前 Skill
        |       +-- 看共享协议 / 签名 / 异步通知 --> huifu-dougong-pay-shared-base
        |
        +-- 你的接入目标是什么？
        |       +-- 标准服务端支付接入、优先快速上线 --> 聚合支付
        |       |        +-- 初始化 --> huifu-dougong-aggregation-base
        |       |        +-- 下单 --> huifu-dougong-aggregation-order
        |       |        +-- 查询 / 关单 / 对账 --> huifu-dougong-aggregation-query
        |       |        +-- 退款 --> huifu-dougong-aggregation-refund
        |       |
        |       +-- 项目制预下单 / 托管收银台 / 托管支付闭环 --> 托管支付
        |                +-- 初始化 --> huifu-dougong-hostingpay-base
        |                +-- 预下单 --> huifu-dougong-hostingpay-cashier-preorder
        |                +-- 查询 / 关单 / 对账 --> huifu-dougong-hostingpay-cashier-query
        |                +-- 退款 --> huifu-dougong-hostingpay-cashier-refund
        |
        +-- 你是不是在做商户前端页面？
                +-- 是 --> huifu-dougong-hostingpay-checkout-js
                +-- 否 --> 继续走服务端 skill
```

## 接入路由表

| 用户意图 | 推荐入口 | 为什么 | 下一步 |
| --- | --- | --- | --- |
| 我第一次接汇付，不知道怎么开始 | 当前 Skill | 先判断产品线、开发任务和阅读顺序 | 再进入 shared/base 或业务 skill |
| 我想看共享规则、签名、异步通知 | [huifu-dougong-pay-shared-base](https://skillhub.cn/skills/huifu-dougong-pay-shared-base) | 这是两条产品线共用的协议入口 | 再回到具体业务 skill |
| 我想做标准服务端支付接入，优先快速上线 | [huifu-dougong-aggregation-base](https://skillhub.cn/skills/huifu-dougong-aggregation-base) | 聚合支付更轻量，适合标准收款场景 | 再进入 order/query/refund |
| 我现在要创建聚合支付订单 | [huifu-dougong-aggregation-order](https://skillhub.cn/skills/huifu-dougong-aggregation-order) | 已按场景组织聚合支付下单能力 | 后续进入 query/refund |
| 我现在要查聚合支付订单或关单/对账 | [huifu-dougong-aggregation-query](https://skillhub.cn/skills/huifu-dougong-aggregation-query) | 聚合支付查询链路已独立整理 | 结合原订单链路使用 |
| 我现在要做聚合支付退款 | [huifu-dougong-aggregation-refund](https://skillhub.cn/skills/huifu-dougong-aggregation-refund) | 聚合退款能力独立维护 | 结合原订单链路使用 |
| 我需要项目制预下单、托管收银台或托管支付闭环 | [huifu-dougong-hostingpay-base](https://skillhub.cn/skills/huifu-dougong-hostingpay-base) | 托管支付路径更适合此类场景 | 再进入 cashier-order/query/refund |
| 我现在要创建托管支付预下单 | [huifu-dougong-hostingpay-cashier-preorder](https://skillhub.cn/skills/huifu-dougong-hostingpay-cashier-preorder) | 承载 H5/PC、支付宝小程序、微信小程序预下单 | 后续进入 query 或 checkout |
| 我现在要查托管支付订单或关单/对账 | [huifu-dougong-hostingpay-cashier-query](https://skillhub.cn/skills/huifu-dougong-hostingpay-cashier-query) | 托管支付查询能力独立维护 | 结合原预下单链路使用 |
| 我现在要做托管支付退款 | [huifu-dougong-hostingpay-cashier-refund](https://skillhub.cn/skills/huifu-dougong-hostingpay-cashier-refund) | 托管退款能力独立维护 | 结合原订单链路使用 |
| 我需要在商户页面里嵌入 checkout 或支付按钮 | [huifu-dougong-hostingpay-checkout-js](https://skillhub.cn/skills/huifu-dougong-hostingpay-checkout-js) | 前端 checkout 是独立能力线 | 与 cashier-order/query 配合使用 |

## 推荐阅读顺序

```text
1. 先判断产品线：聚合支付 / 托管支付 / 前端 checkout
2. 再进入基础 Skill：shared-base / pay-base
3. 再进入具体任务 Skill：order / query / refund
4. 最后按语言适配层落代码
```

## 与已发布 Skill 的关系

### 共享资料层
以下内容以共享资料为准，不在当前 Skill 重复维护：

- 签名规则
- 异步通知规则
- 服务端多语言 SDK 矩阵
- 前端 JS SDK 矩阵
- 版本治理与发布检查

共享入口：
- [huifu-dougong-pay-shared-base](https://skillhub.cn/skills/huifu-dougong-pay-shared-base)

### 聚合支付路径
适用于标准支付接入、优先快速上线的服务端场景：

- [huifu-dougong-aggregation-base](https://skillhub.cn/skills/huifu-dougong-aggregation-base)
- [huifu-dougong-aggregation-order](https://skillhub.cn/skills/huifu-dougong-aggregation-order)
- [huifu-dougong-aggregation-query](https://skillhub.cn/skills/huifu-dougong-aggregation-query)
- [huifu-dougong-aggregation-refund](https://skillhub.cn/skills/huifu-dougong-aggregation-refund)

### 托管支付路径
适用于项目制预下单、托管收银台和更完整闭环：

- [huifu-dougong-hostingpay-base](https://skillhub.cn/skills/huifu-dougong-hostingpay-base)
- [huifu-dougong-hostingpay-cashier-preorder](https://skillhub.cn/skills/huifu-dougong-hostingpay-cashier-preorder)
- [huifu-dougong-hostingpay-cashier-query](https://skillhub.cn/skills/huifu-dougong-hostingpay-cashier-query)
- [huifu-dougong-hostingpay-cashier-refund](https://skillhub.cn/skills/huifu-dougong-hostingpay-cashier-refund)

### 前端 checkout 路径
适用于商户自定义页面中嵌入收银台组件或支付按钮：

- [huifu-dougong-hostingpay-checkout-js](https://skillhub.cn/skills/huifu-dougong-hostingpay-checkout-js)

> 前端 callback 不等于最终交易成功；最终状态仍应由服务端查询或异步通知确认。

## 澄清话术

### 产品线不明确时

```text
请先确认你的接入目标：

1. 标准服务端支付接入，优先快速上线
   - 推荐先看聚合支付路径

2. 需要托管收银台、项目制预下单或更完整的托管支付闭环
   - 推荐先看托管支付路径

3. 需要在商户自己的页面中嵌入收银台组件或支付按钮
   - 推荐先看前端 checkout 路径

如果你不确定，我可以根据你的业务场景继续帮你判断。
```

### 任务阶段不明确时

```text
请确认你当前要做的是哪一步：

1. 初始化 / 公共配置
2. 下单 / 预下单
3. 查询 / 关单 / 对账
4. 退款
5. 前端页面接入
6. 签名 / 异步通知 / 共享协议确认
```

### 前后端职责不明确时

```text
请先分清当前问题属于哪一侧：

1. 服务端：配置凭据、下单、查询、退款、异步通知处理
2. 前端：渲染 checkout、支付按钮、接收前端流程回调
3. 闭环确认：即使前端返回成功，也仍需服务端查单或依赖异步通知确认最终状态
```

## 注意事项

- 本 Skill 是**总入口 Skill**，不代替具体业务 Skill 的字段表和实现说明。
- 首次接入时，优先先判断产品线，再进入对应的 `pay-base` 和业务 skill，不要跳过依赖链。
- `HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 等敏感配置只能留在服务端，严禁写入前端或仓库。
- `sub_openid`、`buyer_id`、`auth_code`、`project_id`、`callback_url` 等运行时值必须来自真实业务链路，不能由模型猜测。
- 前端支付完成回调不等于最终交易成功；同步返回也不一定等于最终终态，最终状态应由查询接口和异步通知共同确认。
- 如果已经明确知道要做哪个具体能力，请直接进入对应 skill，不要在本 Skill 停留过久。

## 官方技术支持

如需官方技术支持或接入答疑，可通过以下官方渠道联系：

- 客服电话：400-820-2819
- 官方邮箱：cs@huifu.com
- 官方支持页：https://paas.huifu.com/open/doc/devtools/#/skillsv1.0

企业微信技术支持群二维码请以官方支持页中的最新信息为准。

## 更新日志

### v1.1.0 (2026-04-14)
- 版本号与同产品包内其他 Skill 对齐到 `1.1.0`
- 保持总入口定位不变，避免发布时出现版本割裂

### v1.0.0 (2026-04-13)
- 新增"汇付支付集成"总入口 Skill
- 建立聚合支付、托管支付、前端 checkout 与共享资料的统一路由入口
- 明确总入口 Skill 与现有子 Skill 的边界关系
