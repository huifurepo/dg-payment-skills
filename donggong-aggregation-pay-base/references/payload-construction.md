# 聚合支付参数校验与 JSON 构造规范

> 聚合支付最容易被大模型写坏的地方有两个：一是 `trade_type` 驱动的条件必填没有校验，二是把 `method_expand`、`tx_metadata` 直接写成简陋的 JSON 字符串。这里统一约束接入方式。

## 推荐的分层方式

```
外部请求 DTO（按 trade_type 使用强类型嵌套对象）
        ↓
参数校验层（必填 / 条件必填 / 场景组合）
        ↓
Payload Builder（序列化 method_expand / tx_metadata）
        ↓
dg-lightning-sdk Request
```

## 必填、非必填、条件必填怎么处理

| 类型 | 建议处理方式 |
|------|-------------|
| 必填 | API 层直接校验并拦截 |
| 非必填 | 有真实来源才传，不要为了“更完整”硬补 |
| 条件必填 | 依据 `trade_type` 或业务开关做组合校验 |

## 聚合支付里最常见的条件必填

| 条件 | 需要补充校验的字段 |
|------|------------------|
| `trade_type=T_JSAPI` / `T_MINIAPP` | `method_expand` 中微信对象的 `sub_appid`、`sub_openid`，且两者来源必须匹配 |
| `trade_type=T_MICROPAY` / `A_MICROPAY` / `U_MICROPAY` | `auth_code` |
| `trade_type=A_JSAPI` | `buyer_id`、`buyer_logon_id` 二选一 |
| `trade_type=U_JSAPI` | `user_id`、`customer_ip`，并按官方说明核对 `qr_code` |
| 传入 `tx_metadata.acct_split_bunch` | `acct_infos`、接收方 `huifu_id`、金额 / 比例规则完整 |
| 反扫或设备报备场景 | `tx_metadata.terminal_device_data` 中真实设备信息 |
| 使用报备机具 | `terminal_device_data.devs_id` |

## 建模规则

### 规则 1：不要把复杂对象在 DTO 层建成 `String`

不推荐：

```java
public class CreateOrderCommand {
    private String methodExpand;
    private String txMetadata;
}
```

推荐：

```java
public class CreateOrderCommand {
    private String tradeType;
    private WechatMethodExpand wechat;
    private AlipayMethodExpand alipay;
    private UnionpayMethodExpand unionpay;
    private TxMetadata txMetadata;
}
```

### 规则 2：只在 SDK 边界序列化一次

不推荐：

```java
request.setMethodExpand("{\"T_MINIAPP\":{\"sub_openid\":\"...\"}}");
request.setTxMetadata("{\"terminal_device_data\":{\"device_ip\":\"10.0.0.1\"}}");
```

推荐：

```java
request.setMethodExpand(objectMapper.writeValueAsString(methodExpand));
request.setTxMetadata(objectMapper.writeValueAsString(txMetadata));
```

### 规则 3：对象出现就要保证子字段业务有效

如果业务决定传 `method_expand.T_MINIAPP`、`tx_metadata.acct_split_bunch`、`tx_metadata.terminal_device_data`，就不能只给一个半截对象。要么不传，要么传可执行的完整结构。

## 推荐代码形态

```java
public TradePaymentCreateRequest buildRequest(
        CreateOrderCommand cmd,
        ObjectMapper objectMapper) throws JsonProcessingException {
    validate(cmd);

    TradePaymentCreateRequest request = new TradePaymentCreateRequest();
    request.setReqDate(cmd.getReqDate());
    request.setReqSeqId(cmd.getReqSeqId());
    request.setHuifuId(cmd.getHuifuId());
    request.setTradeType(cmd.getTradeType());
    request.setTransAmt(cmd.getTransAmt());
    request.setGoodsDesc(cmd.getGoodsDesc());

    Map<String, Object> methodExpand = buildMethodExpand(cmd);
    request.setMethodExpand(objectMapper.writeValueAsString(methodExpand));

    if (cmd.getTxMetadata() != null) {
        request.setTxMetadata(objectMapper.writeValueAsString(cmd.getTxMetadata()));
    }
    return request;
}
```

## 校验建议

### 第一层：基础字段校验

- 金额、日期、IP、URL、枚举值
- `req_seq_id` 是否唯一
- `goods_desc` 是否为真实业务描述

### 第二层：trade_type 驱动的组合校验

- 微信公众号 / 小程序：`sub_appid`、`sub_openid`
- 支付宝 JS：`buyer_id` / `buyer_logon_id`
- 付款码：`auth_code`
- 银联 JS：`customer_ip`

### 第三层：扩展能力校验

- 分账对象是否完整、比例是否闭合
- 设备对象是否来自真实终端采集
- `devs_id` 是否来自报备结果
- 补贴 / 手续费对象是否有真实承担方信息

### 第四层：官方来源校验

- `sub_openid` 是否真的来自当前 `sub_appid` 对应的公众号 / 小程序授权流程
- `buyer_id` 是否真的来自支付宝 `user_id`
- `user_id` 是否真的来自银联 `auth_code -> user_id` 交换流程
- `auth_code` 是否来自本次扫码设备实时采集，而不是配置文件、测试常量或历史缓存

## `method_expand` 构造约束

| 规则 | 说明 |
|------|------|
| 顶层 key 必须与 `trade_type` 对齐 | 例如 `trade_type=T_MINIAPP` 时，不要拼 `A_JSAPI` 的对象 |
| 只传当前场景所需分支 | 不要把多个渠道对象一起塞进一个 `method_expand` |
| 对象字段必须完整 | 有 `detail` 就把 `goods_detail[]` 补完整；有 `pid_info` 就把子字段补完整 |
| 关键身份字段必须真实 | `sub_openid`、`buyer_id`、`user_id`、`auth_code` 只能来自官方指引对应的真实获取链路 |

## `tx_metadata` 构造约束

| 对象 | 约束 |
|------|------|
| `acct_split_bunch` | 金额分账和百分比分账不要混乱拼接；比例之和要闭合 |
| `terminal_device_data` | 优先使用真实采集值；报备终端场景带 `devs_id` |
| `combinedpay_data` | 没有真实补贴账户就不要传 |
| `combinedpay_data_fee_info` | 没有明确承担方就不要传空壳 |
| `trans_fee_allowance_info` | 没有活动或补贴金额来源时不要硬造 |

## 明确禁止的写法

- 在代码里直接手写长 JSON 字符串，然后把变量名叫 `methodExpand` / `txMetadata`。
- 不做场景组合校验，只按平铺字段做 `@NotBlank`。
- 用示例值、空对象、半截对象去“补齐”复杂参数。
- 把多个 `trade_type` 的对象同时塞进一个请求里，指望汇付侧自己兜底。
- 把前端 success 回调直接当作支付成功，不再走后端查单确认。
