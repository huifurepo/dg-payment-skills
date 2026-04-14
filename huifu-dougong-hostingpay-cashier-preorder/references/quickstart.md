# huifu-dougong-hostingpay-cashier-preorder — 统一收银台预下单

覆盖三种预下单场景：H5/PC 网页支付、支付宝小程序、微信小程序。开发者接入汇付支付最高频的第一个接口。

> **前置依赖**：首次接入请先完成 [huifu-dougong-hostingpay-base](../../huifu-dougong-hostingpay-base/SKILL.md) 的 SDK 初始化。

> **编码约束**：开始写 Controller / DTO 前，先看 [customer-preparation.md](../../huifu-dougong-hostingpay-base/references/customer-preparation.md) 和 [payload-construction.md](../../huifu-dougong-hostingpay-base/references/payload-construction.md)。`hosting_data`、`biz_info`、`wx_data` 这类字段在业务层应保持对象形态，做完校验后再序列化给 SDK。

## 本 Skill 解决什么问题

调用汇付预下单接口创建支付订单，获取支付跳转链接（`jump_url`）或小程序拉起参数，引导用户完成支付。

## 文件结构

```
huifu-dougong-hostingpay-cashier-preorder/
├── SKILL.md                          # Skill 定义（端到端流程、触发词、通用参数）
└── references/
    ├── quickstart.md                 # 本文件
    ├── h5-pc-preorder.md             # H5/PC 预下单总览（pre_order_type=1）
    ├── h5-pc-preorder-request.md     # H5/PC 请求参数详解
    ├── h5-pc-preorder-channel.md     # H5/PC 渠道扩展请求参数
    ├── h5-pc-preorder-response.md    # H5/PC 同步/异步顶层返回
    ├── h5-pc-preorder-response-channel.md # H5/PC 渠道扩展返回参数
    ├── h5-pc-preorder-errors.md      # H5/PC 常见错误码与排查
    ├── alipay-mini-preorder.md       # 支付宝小程序预下单（pre_order_type=2）
    └── wechat-mini-preorder.md       # 微信小程序预下单（pre_order_type=3）
```

## 场景选择

| 用户支付方式 | pre_order_type | 参考文档 |
|------------|---------------|---------|
| H5 手机网页 / PC 网页 | `1` | [h5-pc-preorder.md](h5-pc-preorder.md) |
| 支付宝小程序 | `2` | [alipay-mini-preorder.md](alipay-mini-preorder.md) |
| 微信小程序 | `3` | [wechat-mini-preorder.md](wechat-mini-preorder.md) |

## 官方开发指引确认的接入前置项

- H5 / PC 场景：先在合作伙伴控台创建托管项目，启用实际要展示的支付方式，并留存 `project_id`。
- H5 / PC 微信支付：先配置微信授权域名 `api.huifu.com/hostingH5/`。
- 微信小程序场景：先完成小程序托管授权、代码发布和 appid 绑定，拿到真实应用 ID `seq_id`。
- 微信小程序拆单支付：不是普通字段开关，需先特批并开通权限。
- `notify_url` 需满足官方约束：`http/https`、不重定向、不带参数、自定义端口在 `8000-9005`、收到回调后返回 `200`。

## 端到端支付流程

预下单只是支付链路的第一步，完整流程如下：

```
① 预下单（本 Skill）
   调用 preorder 接口 → 获得 jump_url → 保存 req_seq_id + req_date
       ↓
② 用户支付
   H5/PC：window.location.href = jump_url
   小程序：scheme_code 或 gh_id + path 拉起支付
       ↓
③ 接收异步通知
   汇付 POST 到 notify_url → 5 秒内返回 RECV_ORD_ID_{req_seq_id}
   幂等键：hf_seq_id → 详见 tech-spec.md 异步通知指南
       ↓
④ 二次查询确认（huifu-dougong-hostingpay-cashier-query）
   trans_stat=P 时轮询：间隔 5 秒，最多 30 次
       ↓
⑤ 退款（可选，huifu-dougong-hostingpay-cashier-refund）
   trans_stat=S 后可发起退款
```

## 快速接入（H5/PC 场景）

### 1. 构建请求

```java
ObjectMapper objectMapper = new ObjectMapper();

V2TradeHostingPaymentPreorderH5Request request = new V2TradeHostingPaymentPreorderH5Request();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setTransAmt("1.00");
request.setGoodsDesc("商品描述");
request.setPreOrderType("1");
```

### 2. 设置托管参数和扩展参数

```java
// hosting_data：先构造成完整对象，再统一序列化
ObjectNode hostingData = objectMapper.createObjectNode();
hostingData.put("project_title", "项目名称");
hostingData.put("project_id", "项目ID");
hostingData.put("callback_url", "https://your-domain.com/callback");
request.setHostingData(hostingData.toString());

// biz_info：不要直接手写裸字符串，先把对象树补完整
ObjectNode payerCheckWx = objectMapper.createObjectNode();
payerCheckWx.put("real_name_flag", "Y");
payerCheckWx.put("limit_payer", "ADULT");

ObjectNode personPayer = objectMapper.createObjectNode();
personPayer.put("name", "张三");
personPayer.put("cert_type", "IDENTITY_CARD");
personPayer.put("cert_no", "加密后的证件号");

ObjectNode bizInfo = objectMapper.createObjectNode();
bizInfo.set("payer_check_wx", payerCheckWx);
bizInfo.set("person_payer", personPayer);

// 扩展参数：统一放到 extendInfoMap，复杂对象先序列化
Map<String, Object> extendInfoMap = new HashMap<>();
extendInfoMap.put("notify_url", "https://your-domain.com/notify");
extendInfoMap.put("delay_acct_flag", "N");
extendInfoMap.put("biz_info", objectMapper.writeValueAsString(bizInfo));
request.setExtendInfo(extendInfoMap);
```

### 2.1 本地参数校验建议

在客户自己的接口层先做校验和拦截：

- 必填字段：`huifu_id`、`trans_amt`、`goods_desc`、`pre_order_type`
- 条件必填：指定 `trans_type` 时校验 `hosting_data.request_type`
- 对象完整性：只要决定传 `biz_info`、`acct_split_bunch`、`terminal_device_data`、`largeamt_data`，就把其业务必需子字段补齐
- 来源校验：`project_id`、`notify_url`、`callback_url`、`fee_sign`、`devs_id`、`seq_id` 没有真实来源时不要生成请求
- URL 校验：`notify_url` 需符合官方回调地址规则，`callback_url` 仅作前端回跳，不作为支付成功判定

### 3. 发起请求并处理响应

```java
Map<String, Object> response = BasePayClient.request(request, false);
String respCode = (String) response.get("resp_code");
if ("00000000".equals(respCode)) {
    String jumpUrl = (String) response.get("jump_url");   // 支付跳转链接
    String reqSeqId = (String) response.get("req_seq_id"); // 务必保存！
    String reqDate = (String) response.get("req_date");    // 务必保存！
}
```

### 4. 前端跳转

```javascript
// H5/PC 直接跳转到汇付收银台
window.location.href = jumpUrl;
```

完整参数说明和 JSON 示例见 [h5-pc-preorder.md](h5-pc-preorder.md)。

## 额外环境变量

除 base Skill 的 4 个基础变量外，预下单还需要：

| 变量 | 说明 |
|------|------|
| `HUIFU_NOTIFY_URL` | 支付结果异步通知地址 |
| `HUIFU_PROJECT_ID` | 托管项目 ID |
| `HUIFU_PROJECT_TITLE` | 托管项目名称 |
| `HUIFU_CALLBACK_URL` | 支付完成后前端回调地址 |

这些环境变量只覆盖全局固定配置。像 `sub_openid`、`seller_id`、`devs_id`、`person_payer.cert_no`、`payer_client_ip` 这类运行时或场景专属值，仍然需要客户业务侧单独准备。

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `jump_url` 为空 | `resp_code` 非 00000000，预下单失败 | 检查必填参数和商户配置 |
| 流水号重复 (99010002) | `req_seq_id` 当天不唯一 | 使用 `SequenceTools.getReqSeqId32()` |
| 收不到异步通知 | notify_url 不可公网访问 | 检查 URL 可达性、端口范围 8000-9005 |
| 支付宝/微信拉起失败 | 小程序配置不正确 | 检查对应场景文档中的专属参数 |
