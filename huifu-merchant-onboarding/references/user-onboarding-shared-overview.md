# 汇付用户开户与入驻总览

## 能力边界

本 Skill 面向服务商或商户为旗下企业/个人建立分账、结算用户并配置结算能力。它不创建支付商户，不代替 `/v2/merchant/*` 商户进件，也不处理支付交易。

| 生命周期 | 接口 | 结果定位 |
| --- | --- | --- |
| 企业用户开户 | `POST /v2/user/basicdata/ent` | 返回用户 `huifu_id`，可能返回管理员初始密码 |
| 个人用户开户 | `POST /v2/user/basicdata/indv` | 返回用户 `huifu_id`，可能返回管理员初始密码 |
| 用户业务入驻 | `POST /v2/user/busi/open` | 配置结算、结算卡、取现、e账户和电子回单；可能返回申请单 |
| 非同名对公卡审核查询 | `POST /v2/user/apply/query` | 通过用户号和申请单查询 `Y/P/N/F` |
| 用户信息查询 | `POST /v2/user/basicdata/query` | 查询用户资料、卡、结算/取现、e账户和电子回单配置 |

## 路由判定

先问目标实体：

- 需要支付收单、门店、支付渠道或商户状态的是 `merchantHuifuId`，切换到本 Skill 的 `/v2/merchant/*` 商户路由。
- 需要多方分账、结算用户或用户结算卡的是 `userHuifuId`，使用本 Skill。
- 仅出现字符串键 `huifu_id` 不能判定实体；上下文仍不清楚时硬停，只问实体类型。

用户开户返回的 `huifu_id` 不能写入图片上传接口的 `data.huifu_id`。图片上传该字段只支持直属商户号；用户材料应取得 `file_id` 后在本 Skill 请求中使用，但上传过程不得伪造用户号头或业务字段。

## 状态模型

业务入驻至少有三层状态：

1. 审核状态 `audit_status=Y/P/N`。
2. 配置结果 `resp_business[].code=S/F`。
3. e账户银行状态 `bank_status=S/F`。

申请状态查询另有 `apply_status=Y/P/N/F`，其中 `F` 是系统处理失败。不同层次和接口的同字母不能合并为一个通用状态。

## 已知文档冲突

- 五页公共返回表的外层 `response.data` 必填列均为 `N`（业务入驻类型列为 String，其余为 Json）；接入方确认成功响应都包含原生 JSON Object `data`，成功缺失按协议异常，异常响应 DTO 仍允许缺失。

- 官网曾将 `C` 同时说明为“条件必填”和“条件选填”；接入方已裁决为条件必填，按字段说明和主体/卡类型矩阵触发，不做无条件全局必填。
- `file_list` 被定义为 String(JSON Array)，个人开户示例却发送普通数组；wire 已按说明裁决为 String(JSON Array)。
- 企业与个人开户公共响应表均要求 `sign`，成功示例却省略该字段；不得据此取消响应验签。
- 业务入驻公共返回 `data` 标为 String，成功示例和开发规范为对象；成功 wire 已裁决为原生 JSON Object。
- 业务入驻 `async.data.huifu_id` 的中文名为“汇付客户号”，说明却写“汇付分配的商户号”。
- 业务入驻请求和用户详情响应的 `elec_card_list`、审核 `resp_business` 的 Object 类型列与 jsonArray 说明不一致；wire 已按说明及接入决策逐层裁决。
- 业务入驻 D1 请求示例漏传正式规则要求的 `constant_amt`，`fixed_ratio` 与取现 `fee_rate` 示例也未按说明保留两位小数；e账户卡 `card_type` 正式枚举为 `0/1`，同行示例却为 `310100`。
- 接入方确认个人用户只允许 `card_type=1` 对私法人卡，禁止 `0/2/4`；企业用户按业务条件使用 `0/1/2/4`。
- 用户详情 `ent_base_info.file_list` 与 `indv_base_info.file_list` 的 Object 类型列与 jsonArray 说明不一致；解码各自父字符串后按原生数组处理。
- 用户详情 `out_settle_acct_type` 正式枚举为 `01/02/05`，同行示例却为 `0`。
- 用户详情 D1 工作日 `weekday_fix_amt`、`weekday_fee_rate` 的说明同时写“生效”和“不生效”。
- 用户详情 `resp_code` 标为 `String(5)`，示例成功码为8位。
- 用户详情的个人省/区与取现卡市/省示例互相颠倒；不得把示例编码当默认值。

官网正式参数表另有9个空说明路径和15个空长度标量叶字段，机械目录继续保留 `—`。原先没有可执行触发条件的两个 `C` 字段已由接入方裁决：所有接受的卡类型要求 `card_name`，e账户卡 `mp` 在 `card_type=1` 时要求、`card_type=0` 时不要求。完整清单读取 `user-onboarding-field-contracts.md`。

参数表外另有3个字段注记绑定：企业 `legal_name/legal_cert_no` 的法人实名认证及个人 `file_list[]` 的身份证实名认证。完整目录必须继续携带这些注记。

原始合同、示例冲突和接入方裁决必须分层保留。未被裁决的冲突继续标记 `[需要官方确认]`；不得把接入决策伪装成官网字段表原文。
