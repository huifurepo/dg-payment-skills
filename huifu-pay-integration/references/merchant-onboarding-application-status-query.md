# 商户申请单状态查询

## 适用范围

用于基础进件或业务开通后的审核、配置与渠道状态补偿确认。官方来源：[申请单状态查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md)。

## 已确认的请求合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/basicdata/status/query`；顶层使用 `sys_id`、`product_id`、`sign`、`data`。
- 请求与响应 93 个具名路径（含父容器）的类型、长度、Y/N/C 和官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“申请单状态查询”；本页不能替代完整字段目录。
- `data` 必填新的 `req_seq_id:String(32)`、`req_date:String(8)`（`yyyyMMdd`、北京时间）、`apply_no:String(18)`、`huifu_id:String(18)`；不得复用原进件或开通请求的查询流水。高风险约束见 `merchant-onboarding-field-contracts.md`。
- **本 Skill 补偿策略**：网络不确定、回调丢失、回调验签失败或状态乱序时可受控查询作为补偿依据；它不替代回调合同，也不授权固定频率轮询或并发重复进件。
- 回答 `sign`、返回码或其他说明中带外部地址的字段时，必须同时读取 `merchant-onboarding-external-resources.md`，单列 `外部资料提示`，保留官网相对地址原文并给出索引中的规范原始地址；不得因状态字段相似而追加无关业务开通材料。官方状态查询不存在 `data.wx_config_list[].pay_scene`；该列表只有 `config_type` 与 `config_value`，禁止生成悬空路径。

## 公共请求头

- Java 与 PHP 使用 Skill 调用时都要求 `jpt-x-skill-source: <skill_source>`；当前 Java `3.0.39` 与 PHP `2.0.29` 的官方 SDK 主链路会在配置来源值后自动补该头。Python `2.0.23` 同样从 `MerConfig.jpt_x_skill_source` 自动补头。
- 本接口 `data.huifu_id` 必填，因此三种 SDK 还必须从本次请求自动补 `jpt-x-skill-huifu_id: <data.huifu_id>`；禁止配置固定商户号。

## 状态解释

- `apply_status`、基础配置状态、渠道配置状态、直连申请状态、渠道实名与协议状态分别保存，不能压成单一“成功/失败”。
- 询问“能否合并状态”或“字段类型”时，答案必须先列全四个请求字段：`req_seq_id:String(32)`、`req_date:String(8)`、`apply_no:String(18)`、`huifu_id:String(18)`。
- 同一答案必须区分 `data.apply_status:String(1)`、`data.reg_status:String(1)` 和逐业务通知 `reg_result_list[].business_stat:String(1)`；第三者来自业务开通异步通知，不是本查询响应的同层字段。
- 六个基础配置状态 `data.bank_card_conf_status:String(1)`、`data.bind_card_status:String(1)`、`data.cash_status:String(1)`、`data.settle_status:String(1)`、`data.union_conf_status:String(1)`、`data.out_order_funds_status:String(1)` 均使用 `P/S/F`，其中 `P=处理中`、`S=成功`、`F=失败`；它们仍是六个独立状态，不能彼此覆盖或与 `apply_status` 合并。
- 状态查询中的微信直连路径为 `data.wx_zl_config.apply_state:String(32)`，支付宝直连路径为 `data.ali_zl_config[].apply_status:String(1)`；二者枚举均为 `S/P/N/F/C`，但字段名、容器类型和长度不同。
- 协议路径为 `data.agreement_info_list[].con_stat:String(2)`，枚举 `2..8`；`5` 才表示电子协议签约完成。
- 其他渠道叶子状态也按完整路径解析：支付宝/微信配置结果的 `ali_conf_status/wx_conf_status` 使用 `P/S/F`；渠道实名认证状态使用各自英文枚举，不能压成 `1/0`。官网将 `wx_config_list[].config_type` 标成 `String(1)`，却列出 `01/02` 两字符枚举，属于页面内部不一致；建立严格 DTO 前标记 `[需要官方确认]`，不得自行改长度或截值。
- 账户创建、审核通过、业务配置成功、渠道实名和协议签约完成均不等同；只有该能力所需状态同时满足时才可判断可用。
- 拒绝或失败时保存脱敏原因和人工补件路径；不伪造材料、费率、MCC、商户号或渠道状态。

## SDK 证据边界

Java `3.0.39`、PHP `2.0.29`、Python `2.0.23` 都有 `V2MerchantBasicdataStatusQueryRequest` 作为可选封装，字段定位到 `req_seq_id`、`req_date`、`apply_no`、`huifu_id`。Python 不会自动生成 `req_seq_id` / `req_date`；三个 SDK 的默认同步验签路径也不替代本页的状态分层解释。

## 轮询与回调边界

轮询频率、审核回调 ACK、重试和超时策略为 `[需要官方确认]`。在获得官方样本前，Skill 只建议受控补偿查询，不输出固定频率、自动重提或回调实现。
