# 最小回归 Prompt

这份文件随 Skill 分发，用于安装后快速复测主路径。完整回归仍以仓库级回归 Prompt JSON 为准。

## 目录

- 使用方式
- Prompt 清单
- C01 首次接入
- C02 存量系统
- C03 checkout-js 已完成前置
- C05 版本升级
- C06 托管新增接口
- C07 聚合字段更新
- C08 交易分账明细查询
- C09 余额支付
- C10 余额查单
- C11 余额退款
- C12 退款查单
- C13 手续费试算
- C14 付款关系
- C15 余额短信

## 使用方式

每个 Prompt 都要求回答中列出 3-5 份本轮实际使用的本地 references。不要把官网 URL 当作依据。

## Prompt 清单

### C01 首次接入

```text
第一次接汇付支付，我们只有一个普通 Java 服务端收款需求，不确定产品线。请用 $huifu-pay-integration 给我接入判断卡。
```

期望：推荐聚合支付，输出用户类型、产品线、阶段、技术栈、端形态、当前目标和还缺配置。

### C02 存量系统

```text
第一次接汇付，但这是现有商城项目，里面已经有 OrderService、PaymentService、NotifyController 和订单状态枚举。请用 $huifu-pay-integration 判断是不是存量项目并给改造建议。
```

期望：识别为存量业务系统首次接汇付，输出新增、保留、人工确认、落库字段、风险点和回归检查；不能因为“第一次接汇付”判成非存量，不直接替换原状态机。

### C03 checkout-js 已完成前置

```text
托管预下单和服务端查单已经跑通，现在只想接 checkout-js 前端按钮。请用 $huifu-pay-integration 给我下一步。
```

期望：直接进入 checkout-js、callback 和异步通知/最终确认链路；不重新列 quickstart、base、preorder、query 作为本轮阅读顺序。

### C05 版本升级

```text
后续你们 Skill 更新了，我怎么更新本地这个 $huifu-pay-integration？它能不能主动提醒我升级？
```

期望：读取版本策略，说明当前支付 Skill 版本 `1.4.0`、不能主动联网检查或推送升级，以及 Git 拉取、本地目录整体覆盖或独立发布包替换方式。

### C06 托管新增接口

```text
我要接抖音直连下单，另外还要查微信小程序拆单支付订单。请用 $huifu-pay-integration 给我阅读路径和字段边界。
```

期望：路由到抖音直连下单和拆单支付订单查询 reference；说明 `pre_order_type=4`、`dy_data`、`splitpay/query`，不能混用普通托管查单或 H5/PC `pre_order_type=1` 场景语义。

### C07 聚合字段更新

```text
我要做聚合支付合单交易关单和关单查询，还要拉取合并账单。请用 $huifu-pay-integration 告诉我关键字段边界。
```

期望：路由到聚合关单、关单查询和对账 reference；说明 `merge_flag=Y` 时用主单信息、非合单用子单信息；对账 `bill_type` 可用 `MERGE_BILL`，文件名需兼容 `file_name/file_Name`。

### C08 交易分账明细查询

```text
我要用 Java、PHP、Python 官方 SDK 查询一笔180天内的实时或延时分账明细。请用 $huifu-pay-integration 核对请求字段、完整响应和 split_trans_responses 编码。
```

期望：路由到 `trade-split-detail-query.md` 和完整字段目录；说明请求只有 `hf_seq_id/huifu_id/ord_type`，三语言都有专属 `V2TradeTransSplitQueryRequest` 且扩展映射为空；`split_trans_responses` 按 String(JSON Array) 只解码一次，16个子字段保留数组层级；示例独有的顶层 `response.data.huifu_id` 不进入合同。

### C09 余额支付

```text
我要用 Java 接余额支付，出款方和收款方已开户。请用 $huifu-pay-integration 说明分账、风控、短信验证和终态。
```

期望：读取 `balancepay-overview.md`、`balancepay-pay.md`、`balancepay-field-contracts.md`、`balancepay-java-adapter.md`。支付路由 /v2/trade/acctpayment/pay，out_huifu_id 是出款方；acct_split_bunch/risk_check_data 编码一次 String(JSON Object)。verify_value 条件必填，不能把 SDK 声明字段全当必填。C 需逐收款方判断；LV3 jump_url 有效5分钟。

### C10 余额查单

```text
用 Python 查余额支付，知道原支付日期和原请求流水。需要新 req_seq_id 吗？请用 $huifu-pay-integration 给 SDK 入口。
```

期望：读取 `balancepay-query.md`、`balancepay-python-adapter.md`、`balancepay-sdk-matrix.md`。路由 /v2/trade/acctpayment/pay/query；huifu_id/org_req_date 及 org_req_seq_id 或 org_hf_seq_id 定位原支付，不生成新的 req_seq_id/req_date。V2TradeAcctpaymentPayQueryRequest 将定位流水放扩展，扩展不能覆盖已声明字段。

### C11 余额退款

```text
余额支付部分退款，我只有支付全局流水，还需要收款方分账信息。请用 $huifu-pay-integration 核对 PHP 调用与限制。
```

期望：读取 `balancepay-refund.md`、`balancepay-field-contracts.md`、`balancepay-php-adapter.md`。路由 /v2/trade/acctpayment/refund；提供新退款 req_seq_id/req_date 和原支付日期，org_req_seq_id 与 org_hf_seq_id 条件二选一，但23000004说暂不支持全局流水退款，保留冲突并继续明确部分，争议分支TODO。退款分账金额不能超过原收款方分账且总和匹配 ord_amt，不能复制聚合退款协议。

### C12 退款查单

```text
余额退款查询的 org_req_seq_id 指支付还是退款？能传 org_hf_seq_id 替代吗？请用 $huifu-pay-integration 说明。
```

期望：读取 `balancepay-refund-query.md`、`balancepay-sdk-matrix.md`、`balancepay-field-contracts.md`。/v2/trade/acctpayment/refund/query 的请求仅三字段：原退款 org_req_seq_id/org_req_date 和 huifu_id，全为Y；没有请求 org_hf_seq_id。响应 org_hf_seq_id 属退款记录，状态 P/S/F，与支付查询 C 不同。

### C13 手续费试算

```text
余额支付金额已定，用 $huifu-pay-integration 做手续费试算，能否将返回 fee_amt 当最终扣费？
```

期望：读取 `balancepay-fee-calc.md`、`balancepay-field-contracts.md`、`balancepay-sdk-matrix.md`。路由 /v2/trade/feecalc，trade_type=ACCT_PAYMENT，金额字段 trans_amt 而非 ord_amt。费率配置与实际交易结果另核；不能将示例 fee_amt 当最终结算，保留表头列顺序、响应签名信封与示例字段名冲突。

### C14 付款关系

```text
我要提交付款关系 ADD 后马上余额支付，返回S和confirm_url。请用 $huifu-pay-integration 判断是否已生效。
```

期望：读取 `balancepay-pay-relation.md`、`balancepay-field-contracts.md`、`balancepay-sdk-matrix.md`。路由 /v2/trade/payrelation/apply；pay_relations 请求 String(JSON Array)，逐项 in_huifu_id/apply_type ADD/DEL。apply_stat=S 仍需收款方 confirm_url 确认，不能认定已生效；响应正式 jsonArry 编码保留疑义，不补不存在的查询接口。

### C15 余额短信

```text
用 $huifu-pay-integration 生成 Python 余额支付短信 SDK 调用，能否用商户短信 Request？
```

期望：读取 `balancepay-sms.md`、`balancepay-python-adapter.md`、`balancepay-sdk-matrix.md`。精确 /v2/trade/sms/verifycode/send，三语言均无专属 Request，Python DGTools.request_post 官方通用入口。五字段 req_date/req_seq_id/out_huifu_id/mobile_no/trans_type，ACCT_PAYMENT，验证码5分钟且同出款方+交易类型。不使用商户短信/快捷短信类，不传 need_sign 开关，不补虚构 huifu_id。
