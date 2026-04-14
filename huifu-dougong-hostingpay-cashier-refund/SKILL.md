---
name: huifu-dougong-hostingpay-cashier-refund
display_name: 汇付支付斗拱统一收银台退款
description: " 汇付支付斗拱统一收银台退款 Skill：覆盖托管交易退款申请和退款结果查询。参数表和业务规则按协议字段组织，Java SDK 调用方式放在语言适配入口里。当开发者需要对收银台托管订单发起退款或查询退款状态时使用。触发词：托管退款、收银台退款、托管退款查询、收银台退款查询。"
version: 1.1.0
author: "jiaxiang.li | 内容版权：上海汇付支付有限公司"
homepage: https://paas.huifu.com/open/home/index.html
license: CC-BY-NC-4.0
compatibility:
  - openclaw
dependencies:
  - huifu-dougong-hostingpay-base
metadata:
  openclaw:
    requires:
      config:
        - HUIFU_PRODUCT_ID
        - HUIFU_SYS_ID
        - HUIFU_RSA_PRIVATE_KEY
        - HUIFU_RSA_PUBLIC_KEY
        - HUIFU_REFUND_NOTIFY_URL
---

> **版权声明**：本 Skill 内容来源于上海汇付支付有限公司官方开放平台文档，版权归属上海汇付支付有限公司。如有疑问可咨询汇付支付客服：400-820-2819 / cs@huifu.com
>
> **Source**: Official Open Platform documentation of Shanghai Huifu Payment Co., Ltd.
>
> **Copyright**: Shanghai Huifu Payment Co., Ltd.

---

# 统一收银台 - 退款

托管交易退款申请 + 退款结果查询。

## 适配版本与复核信息

| 项目 | 内容 |
| --- | --- |
| Skill 版本 | `1.1.0` |
| 当前适配 SDK | `dg-java-sdk` `3.0.34` |
| 最后复核日期 | `2026-04-08` |
| 官方文档来源 | 汇付开放平台托管支付退款/退款查询接口文档、Java SDK 文档、异步消息说明 |

## 运行依赖与凭据边界

本 Skill 依赖 [huifu-dougong-hostingpay-base](../huifu-dougong-hostingpay-base/SKILL.md) 提供公共运行时。凭据使用规则与存放边界见 [credential-boundary.md](../huifu-dougong-pay-shared-base/governance/credential-boundary.md)。

> **前置依赖**：首次接入请先阅读 [huifu-dougong-hostingpay-base](../huifu-dougong-hostingpay-base/SKILL.md) 完成 SDK 初始化。

> **进入本 Skill 前先确认**：原交易标识已经在订单侧沉淀并可回查，且退款参数按 [参数校验与 JSON 构造规范](../huifu-dougong-hostingpay-base/references/payload-construction.md) 做过必填 / 条件必填校验。

## 协议规则入口

- [signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- [async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md)

## 语言适配入口

这份 Skill 的退款字段、定位键和状态说明，都是语言无关的。  
具体语言怎么初始化和发请求，先看这里：

- [huifu-dougong-hostingpay-base/SKILL.md](../huifu-dougong-hostingpay-base/SKILL.md)
- [server-sdk-matrix.md](../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md)

## Java 适配说明

下面这一段是 Java 专属约束。  
如果你用的是其他语言，字段规则还是按协议表理解，但不要照搬 Java 的 setter 细节。

- Java 运行时入口：看 [../huifu-dougong-hostingpay-base/references/language-adapters/java.md](../huifu-dougong-hostingpay-base/references/language-adapters/java.md)
- 退款里最关键的 Java 专属坑，是 `org_req_seq_id` 没有独立 setter，必须走 `extendInfoMap`

**[关键陷阱]** 退款最重要的字段 `org_req_seq_id`（原交易流水号）**没有独立的 setter 方法**，必须通过 `extendInfoMap` 传入。调用 `request.setOrgReqSeqId()` 将导致**编译错误**。详见 [refund.md](references/refund.md)。

```java
// ERROR: 不存在此方法，编译报错
request.setOrgReqSeqId("20240514...");

// OK: 通过 extendInfoMap 传入
extendInfoMap.put("org_req_seq_id", "20240514...");
request.setExtendInfo(extendInfoMap);
```

## 触发词

- "托管退款"、"收银台退款"、"托管订单退款"、"收银台支付退款"
- "托管退款查询"、"收银台退款查询"、"查询托管退款结果"

## 场景路由

| 用户意图 | 场景 | 详细说明 |
|---------|------|---------|
| 对已支付订单发起退款 | 托管交易退款 | 见 [refund.md](references/refund.md) |
| 查询退款结果 | 退款结果查询 | 见 [refund-query.md](references/refund-query.md) |

## 汇付 API 端点

| 场景 | API 路径 | 请求方式 |
|------|---------|---------|
| 退款 | `v2/trade/hosting/payment/htRefund` | POST |
| 退款查询 | `v2/trade/hosting/payment/queryRefundInfo` | POST |

## 通用架构

```text
接口层
  |- 接收退款和退款查询请求
  |- 校验原交易定位键、退款金额和通知地址

业务逻辑层
  |- 组装退款报文和退款查询报文
  |- 调用对应语言 SDK 或 HTTP 客户端
  +- 输出退款受理结果和退款最终状态
```

下面出现的 SDK Request 类名，是 Java 适配层的写法。  
如果你不是 Java 项目，参数结构仍按本 Skill 的协议字段来实现。

## SDK Request 类对照

| 场景 | SDK Request 类 |
|------|---------------|
| 退款 | `V2TradeHostingPaymentHtrefundRequest` |
| 退款查询 | `V2TradeHostingPaymentQueryrefundinfoRequest` |

## device_type 映射表

退款时 `device_type` 应与原交易的预下单类型匹配：

| 原交易 pre_order_type | 原交易场景 | 退款 device_type | 值 |
|----------------------|-----------|-----------------|-----|
| 1 | H5 手机网页支付 | 手机 | `"1"` |
| 1 | PC 网页支付 | PC | `"4"` |
| 2 | 支付宝小程序 | 手机 | `"1"` |
| 3 | 微信小程序 | 手机 | `"1"` |

> 如果不确定原交易渠道，使用 `"4"` 作为默认值通常可以通过校验。

## 退款请求参数摘要

**专属字段**（有独立 setter）：

| 参数 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| reqDate | setReqDate() | String(8) | Y | 本次退款的请求日期 |
| reqSeqId | setReqSeqId() | String(128) | Y | 本次退款的请求流水号 |
| huifuId | setHuifuId() | String(32) | Y | 商户号 |
| ordAmt | setOrdAmt() | String(14) | Y | 退款金额，不超过原交易金额 |
| orgReqDate | setOrgReqDate() | String(8) | Y | 原交易的请求日期 |
| terminalDeviceData | setTerminalDeviceData() | String(2048) | C | 设备信息 JSON，线上退款必填 |
| riskCheckData | setRiskCheckData() | String(2048) | C | 风控信息 JSON，线上退款必填 |
| bankInfoData | setBankInfoData() | String(1024) | C | 银行信息 JSON，银行大额转账支付退款时必填 |

**扩展字段**（通过 `setExtendInfo(Map)` 传入，**无独立 setter**）：

| 参数 | 必填 | 说明 |
|------|------|------|
| org_req_seq_id | C | **原交易的请求流水号**；与 org_hf_seq_id、org_party_order_id 三选一；拆单支付场景下不作为定位字段 |
| org_party_order_id | C | 原交易微信/支付宝商户单号；与 org_hf_seq_id、org_req_seq_id 三选一；拆单支付场景下与 org_hf_seq_id 二选一 |
| org_hf_seq_id | C | 原交易汇付全局流水号；与 org_req_seq_id、org_party_order_id 三选一；拆单支付场景下与 org_party_order_id 二选一 |
| notify_url | N | 退款结果异步通知地址 |

> 完整字段说明见 [refund.md](references/refund.md)

## 退款返回参数摘要

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | `00000000` 表示退款请求**已受理** |
| trans_stat | String(1) | 退款状态：P=处理中、S=成功、F=失败 |
| ord_amt | String(14) | 退款金额 |
| org_req_seq_id | String(128) | 原交易请求流水号 |
| req_seq_id | String(128) | 本次退款的请求流水号 |

## 退款查询请求参数摘要

| 参数 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| reqDate | setReqDate() | String(8) | Y | 本次查询的请求日期 |
| reqSeqId | setReqSeqId() | String(128) | Y | 本次查询的请求流水号 |
| huifuId | setHuifuId() | String(32) | Y | 商户号 |
| orgReqDate | setOrgReqDate() | String(8) | Y | **退款交易**的请求日期 |
| orgReqSeqId | setOrgReqSeqId() | String(128) | C | **退款交易**的请求流水号（非原支付流水号，与 orgHfSeqId 二选一） |
| orgHfSeqId | setOrgHfSeqId() | String(128) | C | **退款交易**的全局流水号（与 orgReqSeqId 二选一） |

> **注意**：退款查询的 `orgReqSeqId` 是**退款请求**的流水号，不是原支付交易的流水号。`trans_stat=I` 属于罕见初始态，查询到后需联系汇付技术。分账对象、分账手续费、垫资信息和渠道报文见 [refund-query.md](references/refund-query.md)。

## 退款期限

| 渠道 | 最大退款期限 |
|------|-----------|
| 微信（小程序/公众号） | 360天 |
| 支付宝（小程序/JS） | 360天 |
| H5/PC 网页支付 | 360天 |

## 流水号关系图

退款涉及三层流水号，容易混淆：

```text
预下单: req_seq_id = "A001" (原支付交易流水号)
  ->
退款: req_seq_id = "B001" (退款请求流水号), org_req_seq_id = "A001"
  ->
退款查询: req_seq_id = "C001" (本次查询流水号), org_req_seq_id = "B001" (退款流水号)
```

> 退款查询查的是 **B001**（退款流水号），不是 A001（原支付流水号）。

## 异步通知参数

退款结果通过异步通知回调 notify_url，关键字段：

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 业务响应码 |
| huifu_id | String(32) | 商户号 |
| req_seq_id | String(128) | 退款请求流水号 |
| trans_stat | String(1) | 退款状态：S=成功、F=失败 |
| ord_amt | String(14) | 退款金额 |
| actual_ref_amt | String(14) | 实际退款金额 |
| total_ref_amt | String(14) | 累计退款金额 |
| org_req_seq_id | String(128) | 原交易流水号 |
| org_ord_amt | String(14) | 原订单金额 |

## 退款流程

```text
1. 确认原交易已支付成功（trans_stat=S）
2. 调用退款接口发起退款（org_req_seq_id 通过 extendInfoMap 传入）
3. 退款状态为 P（处理中）时，等待异步通知或轮询退款查询接口
4. 退款成功（trans_stat=S）后执行业务退款逻辑
```

## 常见错误与排查

| 错误码 | 场景 | 说明 | 排查方法 |
|-------|------|------|---------|
| 00000000 | 退款/查询 | 处理成功（退款仅表示已受理） | 等待异步通知确认最终状态 |
| 00000100 | 退款 | 退款处理中 | 正常状态，等待异步通知或轮询查询 |
| 10000000 | 退款/查询 | 无效参数 | 检查必填字段，特别是 extendInfoMap 中的 org_req_seq_id |
| 20000004 | 退款/查询 | 交易不存在 | 检查 org_req_date 和 org_req_seq_id |
| 编译错误 | 退款 | `setOrgReqSeqId()` 方法不存在 | 改用 extendInfoMap 传入 org_req_seq_id |

## 注意事项

1. **`org_req_seq_id` 无专属 setter**，必须通过 `extendInfoMap` 传入
2. **退款金额不能超过原交易金额**，汇付会在 API 侧校验
3. 退款接口需要 `terminal_device_data`（设备信息），线上交易退款**必填**
4. `resp_code=00000000` 仅表示退款请求**已受理**，最终结果以异步通知或查询为准
5. 重复退款请求会被拒绝，需做好**幂等校验**
6. `device_type` 根据原交易渠道选择，不确定时用 `"4"`
7. 退款查询的 `orgReqSeqId` 是**退款流水号**，不是原支付流水号
8. 线上交易退款除 `terminal_device_data` 外，`risk_check_data` 也要一并准备；银行大额转账退款还需补齐 `bank_info_data`
9. 拆单支付退款定位原交易时，优先使用 `org_hf_seq_id` 或 `org_party_order_id`，不要再按普通场景只传 `org_req_seq_id`

> 快速接入代码示例见 [quickstart.md](references/quickstart.md)。

---

> 版权声明与联系方式见 [copyright-notice.md](../huifu-dougong-pay-shared-base/governance/copyright-notice.md)
