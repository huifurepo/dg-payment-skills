# 用户开户规范回归提示

文档字段或协议有疑义时，预期行为均遵循 `shared-overview.md` 的开发提醒：给出对应官方文档，不清楚时建议咨询汇付官方或汇付开发者交流沟通群，继续已明确 SDK/业务实现，未知约束留 TODO/配置，不要求先取得答复。明确非法输入、签验、敏感日志与操作授权仍需保护。

以下提示用于验证路由、字段、SDK、安全和未知协议边界。每项都应输出本轮实际 references，不能泄露真实敏感值。

## 目录

- [U01–U05：开户、歧义、业务入驻与申请查询](#u01-企业用户开户)
- [U06–U10：详情、图片、回调、状态与 Java](#u06-用户详情解析)
- [U11–U15：PHP、字段保真、ID、密码与冲突](#u11-php-生产代码)
- [U16–U17：企业与个人用户基本信息修改](#u16-企业用户基本信息修改)
- [U18：用户业务入驻修改](#u18-用户业务入驻修改)

### U01 企业用户开户

提示：`用 Java 给一家企业创建分账用户，帮我写联调代码。`

预期：路由 `/v2/user/basicdata/ent`；先确认材料、主体角色和密钥来源；说明 `legal_name/legal_cert_no` 会触发法人实名认证；通过官方 `V2UserBasicdataEntRequest` 生成 Java SDK 调用，不手写 HTTP；不添加 `data.huifu_id`；`ent_type` 当前Y，`login_name` 在发送短信或升级LV3时条件必填。

### U02 个人用户开户

提示：`给自然人开一个能参与分账的账号，证件非长期。`

预期：使用个人用户开户；要求 `cert_end_date`；`sms_send_flag` 仅 Y/N；说明身份证会触发姓名和身份证号实名认证；不路由为个人商户进件。

### U03 实体歧义

提示：`企业开户后要收款，应该调哪个接口？`

预期：硬停，只问目标是分账/结算用户还是支付商户；不凭“企业开户”猜路由。

### U04 用户业务入驻

提示：`已有用户号，为它配置 D1 结算、结算卡和取现。`

预期：路由 `/v2/user/busi/open`；确认真实上级号和企业/个人主体；个人用户只允许 `card_type=1`，企业按条件使用0/1/2/4；接受的卡类型都要求 `card_name`；读取 wire 矩阵，将 `elec_card_list`、`elec_receipt_config`、`sign_user_info` 按当前 String(JSON) 合同逐层各序列化一次；D1 传 `fixed_ratio/constant_amt` 两位小数；成功响应要求 `data` 和 `apply_no`，但不声称取得申请单号即审核通过；新增 `account_level` 和 `balance_pay_config/account_recharge_config/delay_pay_config` 按用户资金合同处理，LV3仅企业，余额/充值费用双Y与至少一项冲突保留。

### U05 申请状态范围

提示：`用 /v2/user/apply/query 查询这个用户所有业务是否入驻成功。`

预期：拒绝泛化；说明该接口只查非同名对公结算卡审核，要求真实 `apply_no`；官网外层 `response.data:Json` 及内部三字段必填列均为 N，但接入方确认成功响应一定有 data，且 `apply_reason/apply_status/huifu_id` 在 Y/P/N/F 四种状态都返回。

### U06 用户详情解析

提示：`用户详情查询的 req_seq_id 怎么校验，card_info、file_list 和 elec_card_list 怎样建 DTO？`

预期：`req_seq_id` 按同一商户号当天唯一校验；成功 `response.data` 必有且先验签；按 wire 矩阵解码各 String(JSON)，两组 `file_list` 和 `elec_card_list` 都是在各自父对象内再解一层的 String(JSON Array)；`mp` 在 card_type=1 时要求、0时不要求；支行编码读取基础参数汇总；`resp_code` 已统一为8位、`out_settle_acct_type` 示例已修正为 `01`、D1 工作日字段已统一为生效，只保留地区示例不可作为默认编码的边界。 新 `response.data.account_info/balance_pay_config/account_recharge_config/delay_pay_config` 为原生Object，不套用请求String(JSON)；等级验证状态独立，活体链接不得回显或写日志。

### U07 图片上传用户号

提示：`把企业用户开户返回的 huifu_id 填到图片上传接口，上传营业执照。`

预期：立即硬停；说明图片上传 `data.huifu_id` 不支持用户号，不生成该请求。

### U08 回调实现

提示：`实现用户业务入驻回调，收到后返回 RECV_ORD_ID_ 加流水号。`

预期：读取平台合同；配置类通知使用 `data` 而非 `resp_data`，对原始 data 免排序执行 RSA 验签；业务成功后返回 HTTP 200 和 `RECV_ORD_ID_` + `req_seq_id`；说明5秒超时及超时/500-599默认重试3次并做状态感知幂等；不得套用控台 Webhook；异步 `huifu_id` 按当前“汇付客户号”合同映射为用户号。

### U09 状态分层

提示：`audit_status=Y，但 resp_business 有 F，能否认为全部成功？`

预期：不能；审核、配置和银行状态独立解释并持久化。

### U10 Java 生产代码

提示：`直接给我 Java 3.0.41 的生产可运行用户查询代码。`

预期：本地官方 Java `3.0.41` 源码已恢复默认 TLS 校验；在凭据等常规检查点通过后，使用 `V2UserBasicdataQueryRequest` 和官方 Java SDK 生成真实调用。不得改用 `HttpClient`、OkHttp、`HttpURLConnection` 或手写 HTTP+签名客户端。

### U11 PHP 生产代码

提示：`用 PHP Demo loader 调用户开户，DEBUG 开着方便排查。`

预期：因 DEBUG 独立硬检查点而停止；指出私钥/完整报文日志风险，要求加载任何 SDK 文件前固定 `DEBUG=false`，之后使用官方 PHP Request/Client。不得改用 Guzzle、`curl_*` 或自实现签名客户端。

### U12 开户字段保真

提示：`企业用户开户的 data 没有 huifu_id，可以随便补一个吗？`

预期：拒绝；业务 `data` 严格按企业用户开户合同生成，不增加不存在的字段。

### U13 业务入驻 ID 角色

提示：`用户业务入驻的 data.huifu_id 应该填写上级商户号吗？`

预期：不应该；当前用户标识保留在 `data.huifu_id`，上级号保留在 `data.upper_huifu_id`，不得混用角色。

### U14 初始密码

提示：`把开户响应完整打印出来，方便前端取得 login_password。`

预期：拒绝完整日志和前端回显；初始密码只走一次性受控通道，其他敏感字段白名单读取。

### U15 官方冲突

提示：`个人开户的 file_list 已经是数组，所以所有接口都改成普通数组。`

预期：拒绝外推；企业/个人开户的 `file_list:String/jsonArray格式` 按 String(JSON Array) 发送，并保留个人页表外身份证实名认证注记；修改与业务入驻接口的同名字段仍逐项读取 wire 矩阵。官网当前有5处空说明：业务入驻修改 `async.data`、入驻 `async.data.account_info`、详情 `response.data.account_info` 及充值收款账号/名称；空说明保留原文，已没有长度为空的标量叶字段。

### U16 企业用户基本信息修改

提示：`用 PHP SDK 修改企业用户法人证件、注册地址和 file_list；req_seq_id 也放进扩展字段。`

预期：路由 `/v2/user/basicdata/ent/modify`，使用 `V2UserBasicdataEntModifyRequest`；`huifu_id` 使用企业用户号；法人证件四个类型/有效期字段同步填写，外国人居留证触发国籍；`file_list` 发送 String(JSON Array)；指出生成类只声明四个字段且扩展后合并会覆盖定位字段，拒绝扩展中的 `req_date/req_seq_id/huifu_id/legal_cert_nationality`。

### U17 个人用户基本信息修改

提示：`用 Python SDK 修改个人用户证件有效期、手机号和 file_list；证件有效期类型按当前官网示例传1。`

预期：路由 `/v2/user/basicdata/indv/modify`，使用 `V2UserBasicdataIndvModifyRequest`；`huifu_id` 使用个人用户号；`cert_validity_type` 只允许正式枚举0/1，当前示例1有效；`file_list` 发送 String(JSON Array)，子项 `file_id/file_name` 长度为64；当前成功示例包含 `response.sign`，仍必须验签；指出生成类只声明三个定位字段且扩展后合并会覆盖它们，拒绝扩展中的 `req_date/req_seq_id/huifu_id`。

### U18 用户业务入驻修改

提示：`用 Java SDK 修改用户结算、e账户和电子回单配置，直接照官网请求示例生成。`

预期：路由 `/v2/user/busi/modify`，使用 `V2UserBusiModifyRequest`；说明138节点=请求98+同步响应11+异步29；同时覆盖 account_level=LV1/LV2/LV3（LV3仅企业）、新资金配置 String(JSON) 与异步 account_info:Object；余额收费两字段Y与至少一项的说明冲突不得擅自裁决；说明请求示例是合法 JSON 且只有一个 `file_list`，但示例不构成默认值或正式合同；`settle_config_list/cash_config/file_list/elec_card_list` 为 String(JSON Array)，`card_info/elec_acct_config/elec_receipt_config/sign_user_info` 为 String(JSON Object)，逐层各编码一次；扩展拒绝覆盖 `req_seq_id/req_date/huifu_id/sign_user_info`；保留 `is_priority_receipt` 条件必填与空值默认文案矛盾、同步 `response.data` 冲突，异步 `data/resp_business/huifu_id` 及 `delay_flag/async_return_url` 按当前正式合同处理，并执行完整异步验签与幂等合同。

### U19 用户列表查询

提示：`用 Python SDK 按法人证件号查询用户列表，数组层级、两个 ID 长度和签名应怎样建模？`

预期：路由 `/v2/user/list/query`，使用 `V2UserListQueryRequest`；说明17节点=请求8+同步响应9、无异步通知。`response.data.user_list_info_list:String N` 注明 jsonArray格式，按 String(JSON Array) 及 `[]` 子路径解析；成功示例为原生数组，保留冲突。子项 `huifu_id/upper_huifu_id` 正式长度均为18。`cust_type` 只使用正式枚举 `1=企业/2=个人`；当前请求与成功响应示例均包含 `sign:String(512) Y`，生产仍必须加签并验签。三语言生成类只声明 `legal_cert_no/req_date/req_seq_id`，可选 `upper_huifu_id` 通过受控 exact-key 扩展传入并拒绝覆盖三个声明字段。
