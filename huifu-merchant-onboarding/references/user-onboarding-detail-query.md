# 用户信息查询

## 适用范围

查询用户基本信息、结算卡、结算/取现配置、斗拱e账户和电子回单。官方来源：[用户信息查询](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhywcx.md)。它不是商户详情查询，尽管请求业务字段同样只有 `huifu_id/req_seq_id/req_date`。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/basicdata/query`。
- 快照更新时间：官网 `2026.06.26`，本地冻结 `2026-08-10`。
- 共144个字段路径：请求7、同步响应137、异步0；4个根表、12个扩展表，最大深度5。
- 全部请求、响应父子路径、数组层级、类型、长度、Y/N/C 与官方说明读取 `user-onboarding-complete-field-catalog.md`；wire 裁决和官网冲突同时读取 `user-onboarding-field-contracts.md`。
- 请求 `data.huifu_id` 必须是直属用户 ID，不是商户 ID。
- 请求 `data.req_seq_id` 必须保持调用方真实值；官网明确要求同一商户号当天唯一，不得自动换流水或把该规则外推到开户、业务入驻接口。

## 响应解析顺序

外层 `response.data:Json` 的官网必填列为 `N`，接入方确认成功响应一定包含该对象；成功缺失按协议异常，异常响应 DTO 仍允许缺失。以下嵌套组只在父节点存在时解析。

先验外层签名，再读取业务 `data`。以下父字段按 String(JSON) 解一层后，才解析内部字段：

- `ent_base_info`、`indv_base_info`、`card_info`
- `settle_config_list`
- `qry_cash_config_list`、`qry_cash_card_info_list`

`elec_acct_config` 按接入方确认解为 String(JSON Object)；`elec_receipt_config` 和 `sign_user_info` 为原生 JSON Object。不得把所有父字段统一成对象或统一成字符串，也不得把同名省市、证件、卡字段跨父路径合并。

`response.data.ent_base_info.file_list[]` 与 `response.data.indv_base_info.file_list[]` 按说明和接入方确认，是解码各自父 String(JSON Object) 后的原生 JSON Array。完整目录分别保留两组 `file_list[]` 及子路径，不得合并附件或删除数组层级。

`elec_acct_config.elec_card_list` 按说明和接入方确认，是解码 `elec_acct_config` 后仍需再解一层的 String(JSON Array)。完整目录保留 `elec_card_list[]` 及其14个子路径，不得按普通数组直接解析。

官网把 `elec_card_list[].mp:String(11)` 标为 `C` 且说明为空；接入方确认 `card_type=1` 对私法人卡要求存在有效手机号，`card_type=0` 对公卡不要求。历史查询响应仍按存在性容错。`sign_user_info` 的必填列为 `N`，说明写“开通电子回单必填”，按条件必填执行。

官网还留有6个空说明路径和9个空长度标量叶字段，精确清单见 `user-onboarding-field-contracts.md`；目录均以 `—` 原样保留，不能从同名请求字段补写。

不同响应组均为可选。缺少 `ent_base_info` 或 `indv_base_info` 不能单独推断用户类型、失败或未开户；先检查 `resp_code`，再按存在性解析。

## 官方冲突与安全边界

- 正式表将 `resp_code` 定义为 `String(5) Y`，成功示例为 `"00000000"`。DTO 应保留字符串并允许记录长度冲突，不能静默改成商户通用响应模型。
- 企业与个人基础信息下两条 `file_list` 的 Object/jsonArray来源冲突继续登记，wire 已按说明裁决为父字符串解码后的原生数组。
- `elec_card_list` 的 Object/jsonArray字符串来源冲突继续登记，wire 已按说明裁决为父对象内的 String(JSON Array)。
- `response.data.settle_config_list[].out_settle_acct_type` 正式枚举为 `01/02/05`，同行示例却为 `0`。不得把示例 `0` 当成新枚举；若真实响应返回 `0`，记录 `[需要官方确认]`。
- `response.data.qry_cash_config_list[].weekday_fix_amt` 与 `weekday_fee_rate` 的说明同时声称 `cash_type=D1` 时“不生效”和“遇工作日按此费率结算”。该行为自相矛盾，必须标记 `[需要官方确认]`，不得据此生成确定性业务规则。
- `indv_base_info.prov_id/district_id` 的示例为 `310101/310000`，`qry_cash_card_info_list[].area_id/prov_id` 的示例为 `310000/310100`，与同页其他省市区示例顺序相反；必须查外部地区编码，不能照抄样例。`qry_cash_card_info_list[].branch_code` 原行缺链接，现使用接入方提供的官方基础参数汇总中的银行支行编码下载入口。
- 示例证明多组 String(JSON) 会以转义字符串返回；每组只解一次，再按自身父路径校验。
- 响应可能含证件、卡号、手机号、邮箱、地址、文件 ID、`token_no` 等高敏信息。使用白名单提取，只输出业务确需的脱敏字段；禁止完整响应日志。
- 查询响应中的配置状态用于展示现状，不能直接复制成业务入驻请求。

官网未声明异步通知。三语言专属类为 `V2UserBasicdataQueryRequest`；不得与 `V2MerchantBasicdataQueryRequest` 混用。
