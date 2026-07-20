# 商户详细信息查询

## 适用范围

用于已获得目标 `huifu_id` 后的服务端最小化资料核对。官方来源：[商户详细信息查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md)。它不是申请单状态查询，也不能用于前端轮询或回调重放。

## 已确认的请求合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/basicdata/query`；顶层使用 `sys_id`、`product_id`、`sign`、`data`。
- 请求与响应 551 个具名路径（含父容器）的类型、长度、Y/N/C 和官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户详细信息查询”；本页的字段白名单策略不能替代完整目录。
- `data` 必填新的 `req_seq_id:String(32)`（当天同商户唯一）、`req_date:String(8)`（`yyyyMMdd`、北京时间）、目标 `huifu_id:String(18)`；高风险约束见 `merchant-onboarding-field-contracts.md`。
- 响应可能覆盖主体、证照、图片、结算卡、结算/取现、协议、渠道配置和账户资料；按查询目的字段白名单读取，禁止沉淀完整响应表或完整原文。
- 若白名单字段说明带 MCC/地区/证件/银行编码表、图片上传文档、签约规则或线上材料 XLSX，必须同时读取 `merchant-onboarding-external-resources.md`，并按响应完整路径单列 `外部资料提示`、给出未经改写的原始地址；不得把响应中的示例/运行时 URL 当资料或请求默认值。

## 请求与响应值域隔离

本接口请求只有 `req_seq_id:String(32) Y`、`req_date:String(8) Y`、`huifu_id:String(18) Y`。其余字段均为响应字段，不得放入请求。

- 响应 `data.quick_flag/online_flag/withhold_flag/pre_authorization_flag/web_flag/balance_pay_flag` 是 `String(1) N`，值域为 `1=开通`、`0=未开通`、空=未配置。
- 上述 `1/0/空` 只用于解析当前状态。业务开通请求 `data.online_flag/quick_flag/withhold_flag` 使用 `Y/N`，预授权请求使用 `data.alipay_pre_auth_flag` / `data.wechatpay_pre_auth_flag=Y/N`；禁止把查询响应直接复制为开通请求。
- 响应 `data.sms_send_flag=Y/N` 表示注册短信是否发送；企业/个人进件请求的同名字段使用 `M/E/A/空`。禁止跨方向复用。
- 响应 `data.cust_type=1/2` 表示企业/个人；`data.ent_type=1/2/3/4/5/6/7/9` 表示企业种类；它们不是可由调用方猜填的请求参数。
- 请求与响应 DTO 分开建模。企业请求 `reg_name:String(64)`、个人请求 `reg_name:String(32)`，本接口响应 `reg_name:String(128)`，不得共享同一长度校验。
- 官网 `2026-07-14` 页面将 `service_phone` 标为 `String(11)`，但固话示例长度超过 11；严格校验该字段前标记 `[需要官方确认]`，不要截断或擅自放宽。

## 公共请求头

- Java 与 PHP 使用 Skill 调用时都要求 `jpt-x-skill-source: <skill_source>`；当前 Java `3.0.39` 与 PHP `2.0.29` 的官方 SDK 主链路会在配置来源值后自动补该头。Python `2.0.23` 同样从 `MerConfig.jpt_x_skill_source` 自动补头。
- 本接口 `data.huifu_id` 必填，因此三种 SDK 还必须从本次请求自动补 `jpt-x-skill-huifu_id: <data.huifu_id>`；禁止配置固定商户号。

## 数据边界

- 响应中的证件号、银行卡号、地址、联系人、图片资料和 `token_no` 默认不记录原文、不下发前端、不写日志。
- 必须持久化时采用字段级加密、最小权限、访问审计和保留期；日志只保留掩码或不可逆摘要。
- 审核或渠道状态不明时改用申请单状态查询，不凭详情字段推断审核成功。

## SDK 证据边界

Java `3.0.39`、PHP `2.0.29`、Python `2.0.23` 都有 `V2MerchantBasicdataQueryRequest` 作为可选封装，字段仅定位到 `req_seq_id`、`req_date`、`huifu_id`。调用方必须为本次查询生成新的当天唯一流水；SDK 默认响应验签路径不等于允许保存完整响应。
