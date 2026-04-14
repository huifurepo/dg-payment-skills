# 汇付聚合支付 — 查询、关单与对账 Skill

基于 dg-lightning-sdk 的聚合支付查询、关单与对账技能。

## 定位

支付完成后的状态确认、订单关闭和财务对账。

## 核心内容

- **聚合交易查询**：`v4/trade/payment/scanpay/query` — 查询订单支付状态
- **聚合交易关单**：`v2/trade/payment/scanpay/close` — 关闭未支付订单
- **关单查询**：`v2/trade/payment/scanpay/closequery` — 查询关单结果
- **对账单查询**：`v2/trade/check/filequery` — 查询交易/结算对账文件

## 官方开发指引补充

- 微信 / 支付宝 / 银联多个渠道开发指引都明确写了：前端收到支付完成回调后，后端仍需进入查询链路确认最终状态。
- 这一组 skill 就是承接这些官方要求里的“结果确认”和“后续关单 / 对账”环节。

## 参考文件

| 文件 | 内容 |
|-----|------|
| [SKILL.md](../SKILL.md) | Skill 定义（Agent 加载入口） |
| [payment-query.md](payment-query.md) | 聚合交易查询（含完整字段、扩展参数与勘误） |
| [trade-close.md](trade-close.md) | 聚合交易关单（含 webhook、返回码与勘误） |
| [close-query.md](close-query.md) | 关单查询（含状态判定与原交易定位限制） |
| [reconciliation.md](reconciliation.md) | 对账单查询（请求字段名固定使用 `file_date`、`bill_type`） |
