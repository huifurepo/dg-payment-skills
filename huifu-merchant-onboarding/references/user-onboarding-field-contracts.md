# 用户开户与入驻字段合同

## 公共包络

五个接口均为 HTTPS POST JSON。请求外层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；同步响应外层包含 `sign:String(512) Y` 和业务 `data`。五页正式公共返回表都把外层 `response.data` 标为 `N`：企业开户、个人开户、申请状态查询和用户信息查询为 `Json`，业务入驻类型列为 `String`。接入方已确认五接口成功响应都包含原生 JSON Object `response.data`；因此成功响应缺少 `data` 按协议异常处理，同时 DTO 仍允许网关或异常响应整体缺失。这些是 JSON 包络参数，不是 HTTP 请求头。

`sys_id` 表示调用主体：渠道商填写渠道商号，直连/总部商户填写商户号。它不是本次开户生成的用户号。`jpt-x-skill-source` 是本地 Skill/SDK 合同，不是五份官网页面声明的业务字段；其他 SDK 内部请求头不进入本 Skill 的字段合同。

## Y/N/C 与值来源

- `Y` 必填、`N` 非必填；接入方已确认 `C` 统一表示条件必填。保留官网原始标记，按字段说明和主体/卡类型矩阵执行触发条件，不得把全部 `C` 无条件映射成必填。
- 字段为 `N` 但说明给出条件时，按说明触发条件校验并保留官网矛盾。
- 示例值不是默认值；只有说明明确写“默认”才能使用默认口径。
- 未读取外部编码表正文时，只能要求调用方提供经核验编码，不能从示例猜测。
- 不得为满足 SDK 的“required”标记而给官方 `C` 字段填空字符串。

## 官网未定义项

完整目录对官网空白单元格统一保留 `—`，不代表值为空字符串，也不授权从同名字段或 SDK 推断。当前官网正式参数表共有9个空说明路径：

- 用户业务入驻：`request.data.elec_acct_config`、`request.data.elec_receipt_config`、`request.data.sign_user_info.mobile_no`。
- 用户信息查询：`response.data.elec_acct_config.bank_message`、`response.data.elec_acct_config.elec_card_list[].mp`、`response.data.elec_receipt_config`、`response.data.sign_user_info.cert_no`、`response.data.sign_user_info.mobile_no`、`response.data.sign_user_info.name`。

当前共有15个标量叶字段未定义长度：

- 用户业务入驻：`async.sign`、`request.data.elec_receipt_config.switch_state`、`request.data.sign_user_info.type`、`request.data.sign_user_info.mobile_no`、`request.data.sign_user_info.cert_no`、`request.data.sign_user_info.name`。
- 用户信息查询：`response.data.indv_base_info.mcc`、`response.data.indv_base_info.prov_id`、`response.data.indv_base_info.area_id`、`response.data.indv_base_info.district_id`、`response.data.elec_receipt_config.switch_state`、`response.data.sign_user_info.type`、`response.data.sign_user_info.name`、`response.data.sign_user_info.mobile_no`、`response.data.sign_user_info.cert_no`。

官网没有写出两个 `C` 字段的触发条件，接入方现已补充裁决：所有通过主体校验的 `request.data.card_info.card_type` 都条件必填 `card_name`；`response.data.elec_acct_config.elec_card_list[].mp` 在 `card_type=1` 对私法人卡时要求存在，在 `card_type=0` 对公卡时不要求。官网空说明仍在机械目录保留为 `—`，语义校验读取接入决策，不从同名字段推断。

## 开户合同

- 企业证照和法人证件：`validity_type=0` 时结束日期必填；法人证件为外国人居留证时国籍必填。官网长期有效示例仍带结束日期，不构成长期时必填。
- 企业页在参数表外明确：系统会对 `request.data.legal_name` 与 `request.data.legal_cert_no` 做法人姓名和身份证号实名认证；完整目录把同一注记绑定到两个字段，不能只保留其中一个。
- 个人证件：`cert_end_date:String(8)` 的必填列为 `N`，说明却要求非长期有效时必填；保留为“官网 N + 条件必填”。外国人居留证触发国籍。
- 企业 `mcc` 以及个人 `mcc/prov_id/area_id/district_id` 的必填列均为 `N`，但说明明确“用户业务入驻修改且电子回单配置开通时需填写”；必须保留该完整触发条件。
- 个人 `file_list` 的表外官网注意说明：证件类型为身份证时，汇付会对姓名和身份证号做实名认证。wire 按说明和接入方确认使用 String(JSON Array)，普通数组示例只登记为示例冲突，禁止直接发送原生数组。
- 两个开户接口的 `sms_send_flag` 只使用 `Y/N`，默认不发送。企业要发送时 `login_name` 必填。示例中的 `"1"` 与合同冲突，禁止照抄。
- 企业注册省/市/区长度分别为6/8/12；个人电子回单相关省/市/区字段为6位口径。不得统一截断或补齐。
- 两个开户请求都没有 `data.huifu_id` 或 `upper_huifu_id`，也没有异步通知。
- 传 `login_name` 时可能返回 `login_password`；该字段按一次性高敏凭据处理。
- 企业与个人的公共响应表都把 `response.sign:String(512)` 标为 `Y`，成功示例却省略 `sign`；必须继续验签并保留 `[官网示例冲突]`，不得按示例删除响应签名字段。

## 用户业务入驻合同

- `data.huifu_id:String(18) Y` 必须是开户返回的 `userHuifuId`；`data.upper_huifu_id:String(18) Y` 必须是真实渠道商/商户号。
- `settle_config_list:String(JSON Array)` 不支持同时开通 T1 与 D1；`settle_cycle` 为 `T1/D1/TS`。
- `card_info:String(JSON Object)` 的 `card_type` 为 `0` 对公、`1` 对私法人、`2` 对私非法人、`4` 对公非同名。接入方确认：个人用户只允许 `1`，禁止 `0/2/4`；企业用户按业务条件使用 `0/1/2/4`。所有接受的类型都要求 `card_name`，并按企业/个人及账户关系填写对应账户名。
- `card_type=4` 需要文件 `F07`、`F08`、`F516`，并按法人证件类型补相应材料。示例多出的 `bank_code`、`branch_name` 不属于该正式子表。
- `settle_cycle=D1` 时正式说明要求 `fixed_ratio`、`constant_amt` 必填且费率/金额保留两位小数；请求示例却漏传 `constant_amt` 并传 `fixed_ratio:"2"`。`cash_config.fee_rate` 的示例也为 `"2"`，与两位小数要求冲突。只执行正式字段规则，不复制示例格式。
- `elec_acct_config.elec_card_list[].card_type` 正式枚举为 `0/1`，同行示例却为 `310100`；不得提升为枚举。
- `cash_config:String(JSON Array)` 中 `fix_amt` 与 `fee_rate` 至少一项；`out_fee_flag=1/2`，默认2；账户类型只按正式枚举处理。
- `delay_flag` 仅 `Y/N`。电子回单开通时 `sign_user_info` 条件必填；wire 按 Object 发送原生 JSON Object。
- 同步成功 `response.data` 是原生对象，`resp_business:String(JSON Array)` 解一层后读取 `type=1/2/3/5`、`code=S/F`；接入方确认成功响应返回 `apply_no`，但这不等同审核最终通过。

## 业务入驻异步合同

异步外层已声明 `resp_code:String(6) Y`、`resp_desc:String(512) Y`、`sign Y`、`data:String(JSON) N`。内部至少包含原请求流水、日期、`huifu_id` 和 `notify_type`。其中 `async.data.huifu_id:String(18) Y` 的中文名为“汇付客户号”，官网说明却写“汇付分配的商户号”，与请求侧 `data.huifu_id` 的用户号语义冲突；必须原样保留并标记 `[需要官方确认]`，不得直接映射为 `userHuifuId` 或 `merchantHuifuId`：

| 通知 | 条件与状态 |
| --- | --- |
| `notify_type=A` | `audit_info:String(JSON Object)`；`audit_status=Y/P/N`，内含 `apply_no`，配置列表 `code=S/F` |
| `notify_type=Z` | `elec_acct_result:String(JSON Object)`；`bank_status=S/F` |

公共异步规范已补齐：汇付以 POST/UTF-8 推送配置类 `data`，默认超时5秒；超时及500-599默认重试3次，不支持重定向，URL 不带查询参数。接收端对原始 `data` 免排序执行 SHA256WithRSA 验签，成功处理后返回 HTTP 200 和 `RECV_ORD_ID_` + `req_seq_id`，并对重复通知做状态感知幂等。完整协议和 Webhook 隔离读取 `user-onboarding-platform-contracts.md`。

## 查询合同

- 申请状态查询必须带真实用户号、当日唯一流水、日期和 `apply_no`；仅用于非同名对公结算卡审核。官网必填列把 `apply_reason/apply_status/huifu_id` 标为 `N`；接入方确认成功查询在 `apply_status=Y/P/N/F` 四种状态都会返回这三个字段。该裁决不能泛化为其他用户申请状态接口。
- 用户信息查询请求只有用户号、流水和日期；官网同样明确 `req_seq_id` 在同一商户号当天唯一。响应大部分字段可选，不能把缺失父对象解释为未开户或失败。
- 用户信息查询的 `ent_base_info`、`indv_base_info`、`card_info`、`settle_config_list`、`qry_cash_config_list`、`qry_cash_card_info_list` 是 String(JSON)；先解一层字符串，再在各自父路径内解析。
- `elec_acct_config` 按接入方确认解为 String(JSON Object)；`elec_receipt_config` 和 `sign_user_info` 为原生 JSON Object。
- `response.data.ent_base_info.file_list[]` 与 `response.data.indv_base_info.file_list[]` 按说明和接入方确认，是解码各自 String(JSON Object) 父字段后的原生 JSON Array；完整目录分别保留两组 `file_list[]` 子路径，不得合并。
- `elec_acct_config.elec_card_list` 是解码 `elec_acct_config` 父字符串后的 String(JSON Array)，需要再解一层；保留 `elec_card_list[]` 及子路径，不得按普通对象或直接数组解析。
- `sign_user_info` 的必填列为 `N`，说明却写“开通电子回单必填”；保留为官网 N 与说明条件必填，不得把响应中缺少该父对象直接判为失败。
- 个人基础信息的省/区示例分别为 `310101/310000`，取现卡的市/省示例分别为 `310000/310100`，与同页其他省市区样例顺序相反。示例不能作为默认编码，必须用外部地区编码表校验。
- `response.data.qry_cash_card_info_list[].branch_code` 原接口行没有链接目标；接入方提供的官方“基础参数汇总”明确给出银行支行编码 XLSX/JSON/CSV 下载入口，现按完整路径绑定该公共编码来源。
- `settle_config_list[].out_settle_acct_type` 正式枚举为 `01/02/05`，同行示例却为 `0`。保留 `[官网示例冲突]`，不得把 `0` 提升为有效枚举；真实响应出现 `0` 时标记 `[需要官方确认]`。
- `qry_cash_config_list[].weekday_fix_amt` 与 `weekday_fee_rate` 的同一说明同时写“`cash_type=D1` 时不生效”和“D1遇工作日按此费率结算”。不得静默选择任一规则，统一标记 `[需要官方确认]`。
- `resp_code:String(5)` 与8位示例的冲突必须由 DTO 容忍并记录，不能复用假定 `String(8)` 的商户响应类。
