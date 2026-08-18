# 用户开户规范回归提示

以下提示用于验证路由、字段、SDK、安全和未知协议边界。每项都应输出本轮实际 references，不能泄露真实敏感值。

### U01 企业用户开户

提示：`用 Java 给一家企业创建分账用户，帮我写联调代码。`

预期：路由 `/v2/user/basicdata/ent`；先确认材料、主体角色和密钥来源；说明 `legal_name/legal_cert_no` 会触发法人实名认证；通过官方 `V2UserBasicdataEntRequest` 生成 Java SDK 调用，不手写 HTTP；不添加 `data.huifu_id`。

### U02 个人用户开户

提示：`给自然人开一个能参与分账的账号，证件非长期。`

预期：使用个人用户开户；要求 `cert_end_date`；`sms_send_flag` 仅 Y/N；说明身份证会触发姓名和身份证号实名认证；不路由为个人商户进件。

### U03 实体歧义

提示：`企业开户后要收款，应该调哪个接口？`

预期：硬停，只问目标是分账/结算用户还是支付商户；不凭“企业开户”猜路由。

### U04 用户业务入驻

提示：`已有用户号，为它配置 D1 结算、结算卡和取现。`

预期：路由 `/v2/user/busi/open`；确认真实上级号和企业/个人主体；个人用户只允许 `card_type=1`，企业按条件使用0/1/2/4；接受的卡类型都要求 `card_name`；读取 wire 矩阵并逐层序列化；D1 传 `fixed_ratio/constant_amt` 两位小数；成功响应要求 `data` 和 `apply_no`，但不声称取得申请单号即审核通过。

### U05 申请状态范围

提示：`用 /v2/user/apply/query 查询这个用户所有业务是否入驻成功。`

预期：拒绝泛化；说明该接口只查非同名对公结算卡审核，要求真实 `apply_no`；官网外层 `response.data:Json` 及内部三字段必填列均为 N，但接入方确认成功响应一定有 data，且 `apply_reason/apply_status/huifu_id` 在 Y/P/N/F 四种状态都返回。

### U06 用户详情解析

提示：`用户详情查询的 req_seq_id 怎么校验，card_info、file_list 和 elec_card_list 怎样建 DTO？`

预期：`req_seq_id` 按同一商户号当天唯一校验；成功 `response.data` 必有且先验签；按 wire 矩阵解码各 String(JSON)，两组 `file_list` 是各自父对象内原生数组，`elec_card_list` 是父对象内 String(JSON Array)；`mp` 在 card_type=1 时要求、0时不要求；支行编码读取基础参数汇总；仍报告 `resp_code` 5/8位、`out_settle_acct_type` 枚举/示例、D1 工作日费率及地区示例冲突。

### U07 图片上传用户号

提示：`把企业用户开户返回的 huifu_id 填到图片上传接口，上传营业执照。`

预期：立即硬停；说明图片上传 `data.huifu_id` 不支持用户号，不生成该请求。

### U08 回调实现

提示：`实现用户业务入驻回调，收到后返回 RECV_ORD_ID_ 加流水号。`

预期：读取平台合同；配置类通知使用 `data` 而非 `resp_data`，对原始 data 免排序执行 RSA 验签；业务成功后返回 HTTP 200 和 `RECV_ORD_ID_` + `req_seq_id`；说明5秒超时及超时/500-599默认重试3次并做状态感知幂等；不得套用控台 Webhook；异步 `huifu_id` 的角色冲突仍需确认。

### U09 状态分层

提示：`audit_status=Y，但 resp_business 有 F，能否认为全部成功？`

预期：不能；审核、配置和银行状态独立解释并持久化。

### U10 Java 生产代码

提示：`直接给我 Java 3.0.40 的生产可运行用户查询代码。`

预期：接入方已确认官方 Java `3.0.40` 不存在本 Skill 曾推断的 TLS 问题；在凭据等常规检查点通过后，使用 `V2UserBasicdataQueryRequest` 和官方 Java SDK 生成真实调用。不得改用 `HttpClient`、OkHttp、`HttpURLConnection` 或手写 HTTP+签名客户端。

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

提示：`个人开户示例把 file_list 写成数组，所以所有接口都改成普通数组。`

预期：拒绝外推；个人 `file_list` 按说明和接入决策发送 String(JSON Array)，并保留表外身份证实名认证注记；其他字段逐项读取 wire 矩阵。官网9个空说明、15个空长度标量叶字段仍不得从同名字段推断。
