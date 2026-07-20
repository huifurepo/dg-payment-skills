# 商户进件字段合同索引

## 目录

- 使用方式与证据边界
- 公共信封
- 字段生成硬约束
- 请求字段速查
- 值域、默认值与条件速查
- 状态与回调字段归属

## 使用方式与证据边界

本索引是 `1.3.2` 对六个官网页面及“商户业务类型”公共编码页的高风险约束速查，不是完整字段目录。完整字段是否存在、嵌套路径、类型、长度、Y/N/C 与官方说明必须读取 `merchant-onboarding-complete-field-catalog.md`；本页负责枚举、默认值、跨方向隔离、官网冲突和安全边界。业务开通仍必须先选定具体能力，不存在跨渠道通用的完整请求模板。核验日期：`2026-07-17`。企业、个人和业务开通页最近更新时间为 `2026-06-26`，详情查询页为 `2026-07-14`，申请状态查询页为 `2025-08-21`，商户业务类型页为 `2025-03-26`。

- **官网 API 合同**：本页的端点、顶层信封、`data` 第一层字段、类型、最大长度与 Y/N/C 均以所列官网页面为准。
- **SDK 源码事实**：只读取 `shared-server-sdk-matrix.md`；不能推断材料条件、回调验签、响应枚举或审核结果。
- **本 Skill 策略**：安全、脱敏、补偿查询等标为本 Skill 策略，不是官网字段。
- **完整字段目录**：`merchant-onboarding-complete-field-catalog.md` 已机械展开官方全部可达嵌套表。生成对象时必须从父路径读到全部相关叶子，再按调用方真实业务选择取子集；禁止仅凭本页速查、字段名或示例补字段。

## 公共信封

五个 JSON 接口（企业、个人、业务开通、详情、申请状态）的请求顶层均为：`sys_id:String(32), product_id:String(32), sign:String(512), data:Json`，均为 Y。图片上传文档的接口元数据标记 `sign=true`；其 `requestDemo` 只列出 `sys_id`、`product_id`、`data`、`file`，没有列出 `sign`。不得因示例省略 `sign` 而推断 SDK 请求不签名；顶层 `file` 文件流与 `data.file_url` 互斥。

六个接口页均执行同一来源头合同：Java、PHP、Python 使用 Skill 调用时要求 `jpt-x-skill-source: <skill_source>`；当前请求 `data.huifu_id` 存在且非空时还要求 `jpt-x-skill-huifu_id: <data.huifu_id>`。当前 Java、PHP、Python SDK 主链路均能自动补来源头，Java 会条件补商户头；PHP `2.0.29` 对缺失键无保护读取，企业/个人基础进件及图片未传可选 `huifu_id` 时继续阻断对应 PHP 可运行代码。Python `2.0.23` 在缺失字段时发送空商户头，但只作为 SDK 兼容性提示和联调/上线前验证项，不单独阻断 Python 代码，也不把是否允许空头的问题抛给客户。所有语言都禁止固定、虚构或补空业务字段 `data.huifu_id`。

五个 JSON 接口和图片 `file_url` 模式的 Java 调用均进入 `dg-java-sdk 3.0.39` 的公共 `AbstractRequest`。其 `BasePay.debug` 默认为 `true`，会打印私钥、签名和请求数据；任何 Java 可运行代码都必须在进程初始化阶段、任何 SDK 请求之前执行一次 `BasePay.debug = false;`，不得在并发请求中临时切换。该设置只关闭调试输出，不改变签名流程；五个 JSON 接口保留请求签名和响应验签，图片 `file_url` 必须使用 `isPage=true`，保留请求签名但跳过响应验签。

| 接口 | 方法 / URI | 官网来源 |
| --- | --- | --- |
| 企业进件 | `POST /v2/merchant/basicdata/ent` | [企业商户进件](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md) |
| 个人进件 | `POST /v2/merchant/basicdata/indv` | [个人商户进件](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md) |
| 业务开通 | `POST /v2/merchant/busi/open` | [商户业务开通](https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md) |
| 图片上传 | 官网仅给 URI `/v2/supplementary/picture`，未给 method；当前 SDK 适配证据使用 `POST` | [图片上传](https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json) |
| 详情查询 | `POST /v2/merchant/basicdata/query` | [商户详细信息查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md) |
| 申请状态查询 | `POST /v2/merchant/basicdata/status/query` | [申请单状态查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md) |

## 字段生成硬约束

生成、评审 DTO 或解释字段时，按以下顺序逐字段核对；任一项没有本地依据时停止为该字段赋值，并标记 `[需要官方确认]`：

1. 先锁定接口与方向：请求、同步响应、审核通知、逐业务通知、电子协议通知或查询响应。
2. 再锁定完整路径：例如业务开通请求 `data.online_flag` 与详情响应 `data.online_flag` 是两个合同，禁止只按字段名匹配。
3. 同时核对定义、最大长度、Y/N/C、枚举、默认值、条件必填、互斥和补充材料；不得只核对类型或示例。
4. 示例值只演示格式，**不是默认值，也不是推荐值**。禁止把示例里的 `1`、`Y`、费率、MCC、商户号或材料编号复制到真实请求。
5. 官网定义为 `String` 的枚举保持字符串；不得把 `Y/N`、`1/2`、`01` 转成 JSON 布尔值或数字。
6. 可选字段有默认值且调用方确实接受该默认行为时，优先省略字段；只有调用方明确选择并通过约束校验后才显式赋值。
7. String(JSON Object/Array) 必须先校验叶子字段，再统一序列化；未展开目标子表时只列缺口，不生成对象。

同名字段不得跨接口复用值域：

| 完整路径 | 正确值域 | 禁止外推 |
| --- | --- | --- |
| 业务开通请求 `data.online_flag/quick_flag/withhold_flag` | `String(1) N`，仅 `Y/N` | 不得写 `1/0`。 |
| 详情查询响应 `data.online_flag/quick_flag/withhold_flag` | `String(1) N`，`1=开通`、`0=未开通`、空=未配置 | 只用于解析，不得复制回业务开通请求。 |
| 业务开通请求 `data.alipay_pre_auth_flag/wechatpay_pre_auth_flag` | `String(1) N`，仅 `Y/N` | 不得使用详情响应的 `pre_authorization_flag=1/0`。 |
| 业务开通请求 `data.out_fee_flag` | `String(1) N`，`1=外扣`、`2=内扣`，默认 `2` | 不得因为示例值为 `1` 就填 `1`。 |
| 企业/个人进件请求 `data.sms_send_flag` | `M/E/A/空` | 不得套用详情响应 `sms_send_flag=Y/N`。 |
| 详情查询响应 `data.sms_send_flag` | `Y=已发送`、`N=未发送` | 不得反向生成进件请求。 |

## 请求字段速查

`Y` 必填、`N` 非必填、`C` 条件必填。所有 `req_date` 均为 `String(8)`、格式 `yyyyMMdd`；个人、业务开通、详情、申请状态页面明确以北京时间为准。

### 企业进件 `data`

| 字段组 | 字段（类型 / 长度 / 必填） | 官方条件或说明 |
| --- | --- | --- |
| 定位 | `req_seq_id String(32) Y`; `req_date String(8) Y`; `upper_huifu_id String(18) Y` | 请求流水当日唯一；归属渠道商号。 |
| 主体 | `reg_name String(64) Y`; `short_name String(64) Y`; `receipt_name String(50) Y`; `mer_en_name String(256) N`; `ent_type String(1) Y`; `mcc String(7) C`; `busi_type String(1) C` | 使用上级资料时部分主体字段不填；MCC/经营类型按官网条件。 |
| 证照与地址 | `scene_type String(8) Y`; `license_pic String(64) Y`; `license_code String(18) Y`; `license_type String(32) N`; `license_validity_type String(1) Y`; `license_begin_date String(8) Y`; `license_end_date String(8) C`; `found_date String(8) Y`; `reg_capital String(16) C`; `business_scope String(1000) N`; `reg_prov_id/reg_area_id/reg_district_id String(6) N/N/Y`; `reg_detail String(255) Y`; `prov_id/area_id String(6) N`; `district_id String(6) Y`; `detail_addr String(256) C` | `scene_type=OFFLINE/ALL` 时 `detail_addr` 必填；非长期证照时结束日期必填。 |
| 法人与联系人 | `legal_name String(32) Y`; `legal_cert_type String(2) Y`; `legal_cert_no String(32) Y`; `legal_cert_validity_type String(1) Y`; `legal_cert_begin_date String(8) Y`; `legal_cert_end_date String(8) C`; `legal_mobile_no String(11) N`; `legal_addr String(256) Y`; `legal_cert_back_pic/legal_cert_front_pic String(64) Y`; `contact_name String(128) N`; `contact_mobile_no String(11) Y`; `contact_email String(32) Y`; `service_phone String(32) N`; `login_name String(32) Y`; `sms_send_flag String(1) N` | 法人证件非长期时结束日期必填。 |
| 资金与材料 | `card_info String(JSON Object) Y`; `settle_config String(JSON Object) N`; `cash_config String(JSON Array) N`; `reg_acct_pic String(64) C`; `settle_card_front_pic/settle_cert_back_pic/settle_cert_front_pic/auth_entrust_pic String(64) C` | 对私、非同名等材料条件必须按官网 `card_info` 子表核验；未展开时不得生成完整对象。 |
| 组织与扩展 | `head_office_flag/use_head_info_flag String(1) N`; `head_huifu_id String(18) C`; `mer_url String(256) N`; `mer_icp String(50) C`; `store_header_pic/store_indoor_pic/store_cashier_desk_pic String(64) Y`; `ext_mer_id String(64) N`; `remarks String(300) N`; `async_return_url String(120) N`; `elec_acct_config String(JSON Object) N`; `beneficiary_info/share_holder_info_list/extended_material_list String(JSON Array) N`; `activated_products String N` | 审核异步地址只能使用 `async_return_url`，禁止使用支付字段 `notify_url`；下级商户与线上业务条件以官网表为准。 |

### 个人进件 `data`

| 字段组 | 字段（类型 / 长度 / 必填） | 官方条件或说明 |
| --- | --- | --- |
| 定位与经营 | `req_seq_id String(32) Y`; `req_date String(8) Y`; `upper_huifu_id String(18) Y`; `reg_name String(32) Y`; `short_name String(32) N`; `mcc String(7) Y`; `scene_type String(8) Y`; `prov_id/area_id String(6) N`; `district_id String(6) Y`; `detail_addr String(256) C` | 同一商户号当天唯一；线下场景时经营详细地址必填。 |
| 负责人 | `legal_cert_no String(32) Y`; `legal_cert_begin_date String(8) Y`; `legal_cert_validity_type String(1) N`; `legal_cert_end_date String(8) Y`; `legal_addr String(256) Y`; `legal_cert_back_pic/legal_cert_front_pic String(64) Y`; `occupation String(2) N`; `contact_mobile_no String(11) Y`; `contact_email String(32) Y` | 负责人证件仅支持官网允许的类型和日期约束。 |
| 结算与扩展 | `card_info String(JSON Object) Y`; `settle_card_front_pic String(64) Y`; `settle_config String(JSON Object) N`; `cash_config String(JSON Array) N`; `sms_send_flag String(1) N`; `login_name String(32) N`; `mer_url String(256) N`; `mer_icp String(50) C`; `store_header_pic/store_indoor_pic/store_cashier_desk_pic String(64) C`; `ext_mer_id String(64) N`; `remarks String(300) N`; `async_return_url String(120) N`; `head_office_flag String(1) N`; `head_huifu_id String(18) C`; `elec_acct_config String(JSON Object) N`; `extended_material_list String(JSON Array) N`; `activated_products String N` | 审核异步地址只能使用 `async_return_url`，禁止使用支付字段 `notify_url`；卡信息和条件材料的叶子字段未在本页展开时不得生成。 |

### 业务开通 `data`

| 字段组 | 字段（类型 / 长度 / 必填） | 官方条件或说明 |
| --- | --- | --- |
| 定位与费用 | `req_seq_id String(32) Y`; `req_date String(8) Y`; `huifu_id/upper_huifu_id String(18) Y`; `short_name String(64) N`; `out_fee_flag String(1) N`; `out_fee_huifuid String(18) N`; `out_fee_acct_type String(2) N` | 业务申请编号同一商户号当天唯一；费用承担字段按业务条件。 |
| 支付能力 | `online_flag/quick_flag/withhold_flag/alipay_pre_auth_flag/wechatpay_pre_auth_flag String(1) N`; `mer_bus_type String(2) N`; `ali_conf_list/wx_conf_list/union_conf_list/online_fee_conf_list/online_pay_fee_conf_list String(JSON Array) N`; `ali_zl_conf/wx_zl_conf/bank_card_conf String(JSON Object) N`; `online_busi_type String(8) C`; `online_media_info_list String(JSON Array) N`; `use_chains_flag String(8) N` | 渠道、费率和线上业务字段按申请能力填写，不能使用通用模板猜填。 |
| 协议与资金 | `sign_user_info String(JSON Object) C`; `agreement_info String(JSON Object) C`; `balance_pay_config/out_order_funds_config/combine_pay_config/hb_fq_fee_config/split_conf_info String(JSON Object) N`; `delay_flag/forced_delay_flag/fund_collection_flag String(1) N`; `extended_material_list String(JSON Array) N` | 电子签约时 `sign_user_info` 必填；`agreement_async_return_url` 路径是 `data.agreement_info.agreement_async_return_url`。 |
| 其他申请 | `enter_fee String(14) N`; `enter_fee_flag/online_refund/platform_refund/support_revoke/half_pay_host_flag/online_recharge_flag/refund_mend_open_flag/bill_payment_flag String(1) N`; `async_return_url/busi_async_return_url String(128) N`; `recon_resp_addr String(256) N`; `uni_app_payment_config String(JSON Object) N`; `surrogate_config_list String(JSON Array) N`; `large_amt_pay_config String(JSON Object) N`; `agent_recheck_config/jxf_conf_info/merge_pay_config_info Object N`; `withhold_pay_scene String C`; `recon_resp_sys_id String(32) N` | 对象叶子字段以官网路径和条件为准，未展开时不得生成。 |

## 值域、默认值与条件速查

下表只收录官网对顶层标量或本页已展开公共对象明确给出的约束。没有列出的自由文本、编号、URL、费率、金额、MCC、地区、银行或材料值必须由调用方真实提供，不能由 Skill 生成。

### 企业进件约束

| 路径 | 官网约束 |
| --- | --- |
| `data.short_name` | 至少 4 个字符；不是从 `reg_name` 任意截取。 |
| `data.ent_type` | `1/2/3/4/5/6/7/9` 分别为政府机构、国营企业、私营企业、外资企业、个体工商户、其他组织、事业单位、业主委员会；`use_head_info_flag=Y` 时不传。 |
| `data.mcc` / `data.busi_type` | `mcc` 从汇付 MCC 表选择；`busi_type` 仅 `1=实体`、`2=虚拟`；`use_head_info_flag=Y` 时均不传。 |
| `data.scene_type` | 仅 `ONLINE/OFFLINE/ALL`；`OFFLINE/ALL` 时 `detail_addr` 必填。 |
| `data.license_type` | 从机构证照类型表选择；不传默认 `NATIONAL_LEGAL_MERGE`，示例 `NATIONAL_LEGAL` 不是默认值。 |
| `data.license_validity_type` / `license_end_date` | `0=非长期`、`1=长期`；`0` 时结束日必填，`1` 时结束日为空。 |
| `data.reg_capital` | 保留 2 位小数；国营、私营、外资、事业单位、其他、集体经济必填，政府机构和个体工商户可空。 |
| `data.legal_cert_validity_type` / `legal_cert_end_date` | `0=非长期`、`1=长期`；`0` 时结束日必填，`1` 时为空。法人年龄为 18 至 80 岁。 |
| `data.sms_send_flag` | `M=短信`、`E=邮件`、`A=短信和邮件`、空=不通知。 |
| `data.head_office_flag` | `1=总部商户`、`0=下级商户`、不传=普通商户；不是 `Y/N`。 |
| `data.use_head_info_flag` / `head_huifu_id` | `use_head_info_flag` 仅 `Y/N`；`head_office_flag=0` 时 `head_huifu_id` 必填，`head_office_flag=1` 时禁止传。 |
| `data.reg_acct_pic` / 结算材料 | 企业对公结算时 `reg_acct_pic` 必填；对私时银行卡面、持卡人证件正反面必填；对私非法人或对公非同名时授权委托书必填。 |
| `data.activated_products` | 只从 `01=收款产品`、`02=账户与资金产品`、`03=业财数通产品` 选择；多值按官网格式组合，不传为空。 |

### 个人进件约束

| 路径 | 官网约束 |
| --- | --- |
| `data.short_name` | 非必填；传入时至少 4 个字符。 |
| `data.scene_type` | 仅 `ONLINE/OFFLINE/ALL`；包含线下场景时 `detail_addr` 必填。 |
| `data.legal_cert_no` | 只支持身份证；负责人年龄为 18 至 80 岁。 |
| `data.legal_cert_begin_date` / `legal_cert_end_date` | 开始日必须早于当前日期，结束日必须晚于当前日期；官网将 `legal_cert_end_date` 标为 Y，不能因 `legal_cert_validity_type=1` 自行省略。 |
| `data.legal_cert_validity_type` | 非必填；仅 `1=长期`、`0=非长期`。 |
| `data.occupation` | 仅 `1A..1H`；不传默认 `1D=商业工作人员`。 |
| `data.sms_send_flag` | `M=短信`、`E=邮件`、`A=短信和邮件`、空=不通知。 |
| `data.head_office_flag` / `head_huifu_id` | `head_office_flag` 仅 `0=下级商户`，不传=普通商户；传 `0` 时 `head_huifu_id` 必填。 |
| `data.store_header_pic/store_indoor_pic/store_cashier_desk_pic` | 均为 C；线下场景至少按官网对应门头、内景/工作区、收银台材料条件提供，不能统一填占位图片。 |
| `data.card_info.card_no` | 只支持结算借记卡，不支持贷记卡；无法自动识别银行时填写 `bank_code`，官网建议统一填写以提高成功率。 |
| `data.activated_products` | 只从 `01/02/03` 选择；不传为空。 |

### 企业/个人公共资金对象约束

| 路径 | 官网约束 |
| --- | --- |
| `data.card_info.card_type`（企业） | 仅 `0=对公`、`1=对私法人`、`2=对私非法人`；个人 `card_info` 没有该字段。 |
| `data.card_info.cert_validity_type` / `cert_end_date` | 仅 `0=非长期`、`1=长期`；`0` 时结束日必填，`1` 时结束日为空。 |
| `data.card_info.is_settle_default` | 仅 `Y/N`；空表示未指定默认卡。 |
| `data.settle_config.settle_cycle` | 仅 `D1=下个自然日`、`T1=下个工作日`、`TS=笔笔结算`。 |
| `data.settle_config.out_settle_flag` | `1=外扣`、`2=内扣`，默认 `2`；为 `1` 时 `out_settle_huifuid` 必填。 |
| `data.settle_config.out_settle_acct_type` | 仅 `01/02/05/09`，默认 `01`。 |
| `data.settle_config.settle_pattern` | `P0/P1/P2/E1`，默认 `P0`；官网建议选择 `P0` 或 `P2`，`P0` 时批次号必填，`P1/P2` 时结算时间必填；`TS` 时不传。 |
| `data.settle_config.is_priority_receipt` | 仅 `Y/N`，默认 `N`；按官网指定批次范围生效。 |
| `data.cash_config[].cash_type` | 仅 `D0/T1/D1/DM`；企业页未传默认 `T1`，个人页将该字段标为 Y。 |
| `data.cash_config[].fix_amt/fee_rate` | 至少填一项；均按官网金额/百分比精度与范围，不得猜费率。 |
| `data.cash_config[].out_fee_flag` | `1=外扣`、`2=内扣`，默认 `2`；为 `1` 时承担方必填。 |
| `data.cash_config[].out_fee_acct_type` | 企业为 `01/02/05/09`、个人页列 `01/02/05`；默认 `01`，不得跨主体扩展枚举。 |
| `data.cash_config[].is_priority_receipt` | 仅 `Y/N`，默认 `N`；只在 `D1/T1` 生效。 |

### 商户业务开通顶层标量约束

| 路径 | 官网约束 |
| --- | --- |
| `data.short_name` | 企业商户必填且需与注册全称相关；微信只支持 20 字节/10 个汉字。 |
| `data.online_flag/quick_flag/withhold_flag` | 各自仅 `Y=是`、`N=否`；均为 String，禁止填 `1`。 |
| `data.mer_bus_type` | `String(2)`；快捷、网银、手机 WAP、银联统一在线收银台开通且线上费率对象非空时必填；仅可取下表 `01..23`。 |
| `data.out_fee_flag` | `1=外扣`、`2=内扣`，默认 `2`；需要外扣时才显式选 `1`。 |
| `data.out_fee_huifuid` | `out_fee_flag=1` 时必填；必须是真实承担方，不得使用当前商户或上级商户占位。 |
| `data.out_fee_acct_type` | `01=基本户`、`02=现金户`、`05=充值户`、`09=营销户`，默认 `01`。 |
| `data.alipay_pre_auth_flag` / `wechatpay_pre_auth_flag` | 仅 `Y/N`；目前仅支持企业商户，且汇付 MCC 仅 `7011/7296/7512`。主体或 MCC 不满足时不得填 `Y`。 |
| `data.online_busi_type` | 基础进件 `scene_type=ONLINE/ALL` 时必填；快捷、网银、余额支付 Pro、银行大额转账、分账比例大于 30%、代扣需按官方表提供补充材料。 |
| `data.online_media_info_list` | 顶层标为 N，但说明要求基础进件 `scene_type=ONLINE/ALL` 时提供；开快捷、网银、余额支付 Pro、分账、银行大额转账、代扣时还需运营媒介材料。按条件必填处理。 |
| `data.hb_fq_fee_config` | 开通分期业务时必填；费率不得猜填。 |
| `data.delay_flag/forced_delay_flag` | 仅 `Y/N`，默认 `N`；强制延迟为 `Y` 后所有交易需走交易确认。 |
| `data.use_chains_flag` | `1=微信+支付宝`、`2=不使用`、`3=微信`、`4=支付宝`；使用上级商户号前必须具备对应业务。 |
| `data.extended_material_list` | 按目标能力选择纸质协议、线上行业、余额支付、分账、代扣等官方材料；不得用同一材料覆盖所有能力。 |
| `data.agreement_info` | 未签协议时必填；已签纸质或电子协议时仍必填且只能二选一；已签挂网协议时选填。 |
| `data.enter_fee_flag` | 仅 `1=一次性开户费`、`2=平台套餐费（元/年）`；费用值由真实配置提供。 |
| `data.online_refund/platform_refund/support_revoke/fund_collection_flag` | 各自仅 `Y/N`。 |
| `data.half_pay_host_flag` | 仅 `Y/N`；空默认未开通。 |
| `data.online_recharge_flag/refund_mend_open_flag/bill_payment_flag` | 各自仅 `Y/N`。 |
| `data.withhold_pay_scene` | `withhold_flag=Y` 时必填；仅 `1=权益投流订阅`、`2=非权益投流订阅`、`3=保险缴纳`、`4=道路通行费`、`5=公共事业缴费`、`6=物业缴费`。 |
| `data.async_return_url/busi_async_return_url/recon_resp_addr` | 空值分别表示不推送审核、业务开通或交易异步消息；三者语义不同，禁止互换。 |

`mer_bus_type` 的完整公开枚举为：

| 编码 | 业务类型 | 编码 | 业务类型 |
| --- | --- | --- | --- |
| `01` | 综合电商-电商平台 | `13` | 数字虚拟-数字虚拟 |
| `02` | 综合电商-拍卖平台（非文物） | `14` | 医疗服务-药类生产企业 |
| `03` | 综合电商-旅游服务平台 | `15` | 医疗服务-药品批发、零售企业 |
| `04` | 综合电商-教育平台/职业培训/辅导 | `16` | 医疗服务-医疗器械信息展示 |
| `05` | 综合电商-其他 | `17` | 医疗服务-药品信息展示 |
| `06` | 自营电商-食品 | `18` | 医疗服务-医疗器械生产企业 |
| `07` | 自营电商-美妆/洗护 | `19` | 医疗服务-医疗器械自营 |
| `08` | 自营电商-综合百货类 | `20` | 医疗服务-医疗器械经营销售平台 |
| `09` | 自营电商-黄金/珠宝/饰品 | `21` | 医疗服务-互联网医院 |
| `10` | 游戏-游戏 | `22` | 物流服务-物流运输 |
| `11` | 社交-直播（不涉及带货） | `23` | 物流服务-快递业务 |
| `12` | 社交-语音聊天 |  |  |

### 查询响应方向约束

详情查询响应中的字段只用于解析现状，不能作为业务开通请求值：

| 响应路径 | 类型 / 值域 |
| --- | --- |
| `data.cust_type` | `String(1) Y`：`1=企业`、`2=个人`。 |
| `data.ent_type` | `String(1) Y`：`1/2/3/4/5/6/7/9`，含义同企业进件。 |
| `data.busi_type` | `String(1) N`：`1=实体`、`2=虚拟`。 |
| `data.license_validity_type/legal_cert_validity_type` | `String(1) N`：`1=长期`、`0=非长期`。 |
| `data.occupation` | `String(2) N`：`1A..1H`。 |
| `data.sms_send_flag` | `String(1) N`：`Y=已发送`、`N=未发送`；与进件请求的 `M/E/A/空` 不同。 |
| `data.quick_flag/online_flag/withhold_flag/pre_authorization_flag/web_flag/balance_pay_flag` | `String(1) N`：`1=开通`、`0=未开通`、空=未配置。只解析，不回填。 |
| `data.delay_flag/forced_delay_flag` | `Y/N`；`delay_flag` 空按否解析。 |
| `data.out_fee_flag` / `out_fee_acct_type` | `1/2`（默认 `2`）与 `01/02/05/09`（默认 `01`）。 |

官网详情页存在需保留原样的合同差异：企业进件请求 `reg_name` 为 `String(64)`、个人为 `String(32)`，详情响应为 `String(128)`；请求和响应 DTO 不得复用同一长度注解。详情页还把 `service_phone` 标为 `String(11)`，但示例固话超过 11 个字符；依赖该字段做严格 DTO 校验前标记 `[需要官方确认]`，不得擅自放宽或截断。

### 必填 `card_info` 叶子合同

企业 `data.card_info` 是 JSON Object 序列化后的字符串：

| 字段 | 类型 / 长度 / 必填 | 条件 |
| --- | --- | --- |
| `card_type`、`card_name`、`card_no` | `String(1) Y`、`String(128) Y`、`String(32) Y` | `card_type=0/1/2` 分别为对公、对私法人、对私非法人；户名必须匹配对应主体。 |
| `prov_id`、`area_id`、`branch_code` | `String(6) N`、`String(6) Y`、`String(12) C` | 对公 `card_type=0` 时 `branch_code` 必填。 |
| `cert_type`、`cert_no` | `String(2) C`、`String(32) C` | 对私 `card_type=1/2` 时必填；对公为空。 |
| `cert_validity_type`、`cert_begin_date`、`cert_end_date` | `String(1) N`、`String(8) N`、`String(8) C` | `cert_validity_type=0` 时结束日期必填，`=1` 时结束日期为空。 |
| `mp`、`is_settle_default` | `String(11) N`、`String(1) N` | 全域资金管理时手机号按官网条件必填；默认卡标识为 `Y/N`。 |

个人 `data.card_info` 是 JSON Object 序列化后的字符串：

| 字段 | 类型 / 长度 / 必填 | 条件 |
| --- | --- | --- |
| `card_name`、`card_no` | `String(128) Y`、`String(32) Y` | 结算户名及借记卡账号，禁止示例值或贷记卡。 |
| `prov_id`、`area_id`、`bank_code` | `String(6) N`、`String(6) Y`、`String(8) N` | 无法自动识别银行时应填写银行编号。 |
| `cert_type`、`cert_no` | `String(2) Y`、`String(32) Y` | 持卡人证件信息。 |
| `cert_validity_type`、`cert_begin_date`、`cert_end_date` | `String(1) Y`、`String(8) Y`、`String(8) C` | `cert_validity_type=0` 时结束日期必填，`=1` 时结束日期为空。 |
| `mp`、`is_settle_default` | `String(11) N`、`String(1) N` | 手机号及默认卡标识 `Y/N`。 |

业务开通没有跨能力的统一嵌套对象：微信、支付宝、银联、银行卡、直连、协议、分账或资金能力必须先由用户明确目标，再从官网相应的 `ali_conf_list`、`wx_conf_list`、`union_conf_list`、`bank_card_conf`、`ali_zl_conf`、`wx_zl_conf`、`sign_user_info`、`agreement_info`、`split_conf_info` 等子表加载完整叶子合同。未明确能力、费率、渠道权限和材料时，只能解释字段或输出缺口清单，不得生成“全能力通用请求”。

### 图片与查询请求

| 接口 | `data` 字段 |
| --- | --- |
| 图片上传 | `req_seq_id String(32) Y`; `req_date String(8) Y`; `file_type String(32) Y`; `huifu_id String(18) N`; `file_url String(512) N`。`data.file_url` 与顶层 `file` 互斥；图片为 JPG/BMP/PNG，最大 2MB。官网未定义响应 schema。 |
| 详情查询 | `req_seq_id String(32) Y`; `req_date String(8) Y`; `huifu_id String(18) Y`。响应公共字段为 `data.resp_code String(8) Y`、`data.resp_desc String(512) Y`；详情中的高敏字段按白名单读取。 |
| 申请状态查询 | `req_seq_id String(32) Y`; `req_date String(8) Y`; `apply_no String(18) Y`; `huifu_id String(18) Y`。响应公共字段为 `data.resp_code String(8) Y`、`data.resp_desc String(512) Y`。 |

## 状态与回调字段归属

| 路径 | 类型 / 枚举 | 解释 |
| --- | --- | --- |
| 业务开通审核通知 `data.audit_status` | `String(1)`：`P/Y/N/F/C` | 审核通知官网明确使用 `data` 包装；不能与渠道结果混用。 |
| 逐业务通知 `reg_result_list[].business_stat` | `String(1)`：`S/F` | 仅官网规定的 `notify_type=W/A/E` 返回；逐业务通知外层包装待官方样本确认。 |
| 逐业务直连结果 `zl_async_info.apply_state` | `String(1)`：`S/P/N/F/C` | 业务开通逐业务通知中的直连申请状态；逐业务通知外层包装待官方样本确认。 |
| 业务开通协议结果 `agreement_info_list[].con_stat` | `String(2)`：`2..8` | `5` 表示签约完成；仍须结合所需能力判断。 |
| 申请状态查询 `data.apply_status` | `String(1)`：`Y/P/N/F` | 顶层申请审核状态。 |
| 申请状态查询 `data.reg_status` | `String(1)`：`P/S/F` | 商户入驻汇付状态。 |
| 申请状态查询 `data.bank_card_conf_status`、`bind_card_status`、`cash_status`、`settle_status`、`union_conf_status`、`out_order_funds_status` | 均为 `String(1)`：`P/S/F` | 银行卡、绑卡、取现、结算、银联二维码及资金入账的独立状态；`P=处理中`、`S=成功`、`F=失败`，不得与申请审核或协议状态合并。 |
| 申请状态查询 `data.wx_zl_config.apply_state` | `String(32)`：`S/P/N/F/C` | 微信直连对象状态；字段长度与业务开通逐业务通知不同。 |
| 申请状态查询 `data.ali_zl_config[].apply_status` | `String(1)`：`S/P/N/F/C` | 支付宝直连列表状态；字段名不是 `apply_state`。 |
| 申请状态查询 `data.agreement_info_list[].con_stat` | `String(2)`：`2..8` | 状态查询中的电子协议状态，`5` 为签约完成。 |
| 申请状态查询 `data.ali_conf_result_list[]`、`wx_conf_result_list[]`、`zft_apply_result_list[]`、`wx_config_list[]` | `String(JSON Array)` | 渠道信息集合；读取叶子状态前按官网对应对象路径核验。 |

仅 `busi_async_return_url` 的逐业务通知在**存在** `ord_id:String(44)` 时，官网明确应答 `RECV_ORD_ID_` + 该 `ord_id`。审核通知与电子协议通知的 ACK、验签原文、HTTP 语义、超时和重试均为 `[需要官方确认]`；不得用 `req_seq_id` 代替 `ord_id`，也不得生成回调实现。
