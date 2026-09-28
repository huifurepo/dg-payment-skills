# 汇付进件管理 API 文档静态审计报告

- 审计时间：2026-09-04 09:42:41—09:43:04（UTC+08:00）
- 审计对象：用户指定的 34 个在线文档（商户进件 13、用户进件 15、AT 管理 6）
- 审计方式：在线原文全量抓取、Markdown/JSON 结构检查、参数表与示例交叉比对、同类接口横向比对、仓库 2026-08-31 官方快照复核
- 结果：27 个根因级问题组，其中 P0 3 个、P1 16 个、P2 6 个、P3 2 个
- 可用性：34/34 个主链接返回 HTTP 200；53 个 Markdown 链接归一为 16 个一级资源地址，16/16 可访问。URL 中的 SPA fragment 是否能正确定位到目标小节，不能仅凭 HTTP 状态确认。

> “确认问题”表示当前文档内部存在可复现的矛盾、缺项或不安全示例，不表示本报告已推断出真实接口行为。凡真实 wire、长度、枚举或回调行为无法从文档唯一确定的，均在“开发确认清单”中要求后端裁决。

## 严重级别

| 级别 | 本报告口径 | 数量 |
| --- | --- | ---: |
| P0 | 敏感数据、内部地址或可用凭据暴露，可能造成安全事件 | 3 |
| P1 | 可能直接导致请求失败、响应解析失败或业务流程中断 | 16 |
| P2 | 约束不完整或表述矛盾，容易造成接入歧义 | 6 |
| P3 | 低风险格式、错字、旧链接或维护性问题 | 2 |

## 建议先处理的第一批

1. 立即清理 [M01]、[M02]、[M03]、[M07]、[U11] 的内网地址，以及 [U11] 的带摘要合同下载链接；检查相关链接是否仍有效，必要时失效处理。
2. 将所有完整证件号、银行卡号、手机号、邮箱和真实感较强的企业/个人样例替换为经批准的纯合成测试数据。
3. 修复 [U13] 复制了商户详情查询请求/响应示例的问题；这是当前最容易误导 SDK/调用方的结构性错误。
4. 修复 [U11] 的 `pageSize/page_size`、响应字段名、未声明分页字段和多处长度冲突。
5. 修复 [M04] 同时提交 `file_url` 与文件流的示例，并补齐完整上传/返回协议。
6. 统一响应信封、结构字段 wire 类型和条件必填定义，再批量修复其余页面，避免逐页修完后继续互相冲突。

## 确认问题

### HF-DOC-P0-001 — 在线示例暴露内网地址

- 状态：确认问题
- 类型：安全 / 示例数据
- API：[M01]、[M02]、[M03]、[M07]、[U11]
- 位置：请求示例中的 `async_return_url`、`recon_resp_addr`；合同列表返回示例中的 `sign_url`
- 证据：页面包含 `192.168.85.x`、`192.168.4.x`；[M01] 还出现 `virgo://http://...` 双重 scheme。
- 影响：泄露内部网络信息；复制示例会得到不可达地址，[M01] 的地址格式本身也不可作为正常 HTTP 回调地址。
- 建议修改：统一替换为 `https://callback.example.com/...`、`https://sign.example.com/...`；清理源数据和历史缓存中的内网地址。

### HF-DOC-P0-002 — 完整格式个人与商户敏感数据未脱敏

- 状态：确认问题；样例是否来自真实数据需内部安全确认
- 类型：安全 / 隐私
- API：[A03]、[A05]、[M01]、[M02]、[M05]、[M08]、[U01]、[U02]、[U03]、[U05]、[U06]、[U07]、[U08]、[U09]、[U13]
- 位置：请求或返回示例中的证件号、银行卡号、手机号、邮箱、姓名、企业名称和详细地址
- 证据：[M05] 与 [U13] 的返回示例完全相同，均包含完整格式的自然人证件号、银行账号、手机号、邮箱和地址；其规范化 `data` JSON 的 SHA-256 同为 `942979d1fa299ed66dceaf8ce1fac7dd68872a1ce89eb034e70a027bbaa15d79`。
- 影响：若数据并非纯合成，会构成隐私泄露；即使为测试数据，也会被安全扫描识别为高风险内容。
- 建议修改：使用专门生成、明确标注且不可关联真实主体的沙箱数据集。若示例要求可运行，不要简单打星号，应使用通过内部审批的有效格式合成数据。

### HF-DOC-P0-003 — 合同列表示例公开带摘要下载链接和测试签约链接

- 状态：确认问题；链接是否仍可用需内部安全确认
- 类型：安全 / 临时凭据
- API：[U11]
- 位置：成功返回示例 `result_list[].download_url`、`result_list[].sign_url`
- 证据：示例包含第三方测试合同地址、`contract_id`、`timestamp`、`msg_digest`，以及 integrationtest 域名和内网签约地址。
- 影响：带签名或摘要的 URL 可能等价于临时访问凭据，也暴露测试环境结构与合同标识。
- 建议修改：立即检查并失效仍有效链接；文档只保留 `https://contract.example.com/view?token=REDACTED` 一类不可用占位地址。

### HF-DOC-P1-001 — 图片上传示例违反自身互斥规则，且缺少完整协议

- 状态：确认问题；真实上传协议待开发确认
- 类型：请求示例 / 接口完整性
- API：[M04]
- 位置：`requestBody.params.file_url`、`requestDemo`、根级 `uri/sign`
- 证据：字段说明称 `file_url` 与文件流不能同时上传，但 `requestDemo` 同时给出二者；源 JSON 未给出响应字段、HTTP method、`Content-Type`、multipart 部件名和错误示例，`uri` 也没有完整 URL。
- 影响：调用方照抄示例会提交非法请求，且无法可靠解析 `file_id` 或处理错误。
- 建议修改：分别提供“URL 上传”和“文件流上传”两个示例；补充完整 endpoint、POST、multipart/form-data 规则、签名参与字段、文件部件名、成功/失败响应及 `file_id` 定义。闭合 `file_url` 说明中的 `<font>` 标签，并明确“其他类型文件”的允许扩展名/MIME。

### HF-DOC-P1-002 — 返回参数要求 `sign`，成功示例却省略签名或整个信封

- 状态：确认问题；真实返回信封待开发确认
- 类型：响应结构 / 签名
- API：[A01]、[A02]、[A05]、[A06]、[M02]、[M05]、[M08]、[M10]、[U10]、[U11]、[U12]、[U13]
- 位置：公共返回参数与成功返回示例
- 证据：上述页面把 `response.sign` 标为 `Y`，但示例只给 `data` 或直接给 data 内层字段。[A02] 的示例甚至没有外层 `data`。[M02] 的异步表又把 `sign` 标为 `N`、长度 512，而同族 [M01] 标为 `Y`、长度 2048。
- 影响：SDK 可能按示例生成错误 DTO、跳过验签，或在真实响应带信封时解析失败。
- 建议修改：先由网关确认各接口同步/异步真实信封；随后让每个示例与字段表逐键一致，并明确验签对象、无 `data` 时的签名规则。

### HF-DOC-P1-003 — 逻辑类型、wire 类型与示例编码混用

- 状态：确认问题；真实 wire 待开发确认
- 类型：序列化 / 数据模型
- API：[A01]、[A05]、[M01]、[M02]、[M03]、[M05]、[M07]、[M08]、[M12]、[M13]、[U03]、[U05]、[U08]、[U13]、[U15]
- 位置：类型为 `Object`/`String` 的结构字段及公共 `data`
- 证据：
  - [U03]/[U08]：`elec_receipt_config` 为 Object，说明为 jsonObject 字符串；`elec_card_list` 为 Object，说明为 jsonArray 字符串。
  - [U08]：公共 `response.data` 为 String，成功示例为原生 JSON Object。
  - [U15]：`wx_pay_config_info`、`ali_pay_config_info` 标为 Object 且说明 jsonArray，示例却是 String(JSON Object)；两个实名列表标为 Object，示例是 String(JSON Array)；字段表写 `wx_neal_name_list`，示例又写 `wx_real_name_list`。
  - [U13]：`lla_withhold_config` 标为 Object，说明为 jsonArray，但子表描述的是单个配置对象。
  - [M12]/[M13]：`conf_list` 为 String 且挂有子表，但未说明它是对象、数组、String(JSON Object) 还是 String(JSON Array)。
  - 商户进件页还大量存在 Object 与“jsonObject/jsonArray 字符串”并列的结构字段，如 `material_card_info`、`agent_recheck_config`、`jxf_conf_info`、`merge_pay_config_info`。
- 影响：不同语言 SDK 会生成互不兼容的字段类型，容易出现双重序列化、签名原文不一致和解析失败。
- 建议修改：参数表增加“逻辑结构”和“线上 wire”两列；wire 仅允许 `object`、`array`、`string(JSON object)`、`string(JSON array)` 四种明确值。每个结构字段都给出最小可解析示例。

### HF-DOC-P1-004 — `Y/N/C` 定义与字段条件互相冲突

- 状态：确认问题；具体触发矩阵待开发确认
- 类型：必填性 / 条件规则
- API：[A03]、[A05]、[M01]、[M03]、[M07]、[M08]、[U01]、[U03]、[U07]、[U08]、[U14]、[U15]
- 位置：必填说明及条件字段
- 证据：[U03] 同页同时写“C 代表条件必填”和“C 代表条件选填”；[U01] 只写“条件选填”；[M01] `reg_capital` 标 C，却同时出现“条件选填”和多类主体“必填”。多页把描述明确为“某条件下必填”的字段标成 N，例如 [U14] `head_huifu_id`、[U15] `upper_huifu_id`、[A03] `finance_type`、[A05] `certificate_info`。
- 影响：调用方无法仅凭表格构建校验器，容易漏传后收到业务拒绝。
- 建议修改：统一定义 `C=条件满足时必填`；所有条件必填字段标 C，并把条件写成可执行表达式，例如 `required_if: head_office_flag == "0"`。若字段只是建议传或有后端默认值，应标 N 并删除“必填”。

### HF-DOC-P1-005 — 三个电子合同接口的返回码长度与示例冲突

- 状态：确认问题；真实返回码长度待开发确认
- 类型：长度 / 返回码
- API：[U10]、[U11]、[U12]
- 位置：`response.data.resp_code`
- 证据：参数表长度为 9、内联示例为 9 个零，成功 JSON 示例均为 8 个零；同站其他业务响应码通常为 8 位。
- 影响：固定长度 DTO、校验器和成功码判断会不一致。
- 建议修改：以后端契约为准统一长度和所有示例；若标准成功码确为 `00000000`，表格长度应改为 8，并删除 9 位示例。

### HF-DOC-P1-006 — 电子合同列表请求和响应无法按字段表实现

- 状态：确认问题；空列表形态与分页字段待开发确认
- 类型：字段名 / 响应结构 / 长度
- API：[U11]
- 位置：请求示例、`response.data`、`result_list[]`
- 证据：
  - 必填字段表为 `page_size`，请求示例发送 `pageSize`。
  - 示例返回 `total_size/page_num/page_size`，响应表没有声明这三个字段。
  - 表格字段为 `createTime`，示例为 `create_time`。
  - `sign_status` 长度 1，但枚举最短也有 7 字符；`createTime` 长度 8、示例 14 位；`expiration_date` 长度 1、示例 8 位；`sign_url` 长度 1；`agreement_type` 长度 1、值 `ELECT`；`scene_code` 长度 1、值为 `MER_REGIST/MER_MODIFY/MER_KYC`。
  - `result_list` 说明“无返回 0”，但没有说明是数值 `0`、字符串 `"0"` 还是空数组。
- 影响：请求分页参数可能不生效，响应 DTO 必然出现字段丢失或长度校验失败。
- 建议修改：统一 snake_case；补齐分页字段；按真实返回修正长度；明确无结果统一返回 `[]` 或其他唯一形态；将大段 12 条样例缩成 1—2 条脱敏记录。

### HF-DOC-P1-007 — 下级商户权限接口复制了无关接口的请求/返回示例

- 状态：确认问题
- 类型：错贴示例 / 响应结构
- API：[U13]、对照 [M05]
- 位置：请求示例与成功返回示例
- 证据：[U13] 与 [M05] 两个 JSON 示例的规范化 `data` 内容逐字相同；[U13] 请求表要求内层 `data.product_id`，示例未发送；[U13] 返回表要求 `req_date/req_seq_id/huifu_id/apply_no`，示例却返回商户详情的 42 个字段且没有这些必填字段。
- 影响：调用方无法知道此接口的真实返回，自动生成 SDK 会得到完全错误的模型。
- 建议修改：删除复制内容，使用该接口真实请求/响应重新生成示例；示例必须逐键通过 schema 校验。补充失败示例和申请单后续查询关系。

### HF-DOC-P1-008 — 统一进件页面版的同步与异步字段约束冲突

- 状态：确认问题；`use_chains_flag` 真实枚举待开发确认
- 类型：返回码 / 长度 / 枚举
- API：[U14]
- 位置：同步返回、审核异步、请求 `head_huifu_id/use_chains_flag`
- 证据：`resp_code` 长度 8，成功示例只有 6 个零；`url` 长度 32，文档示例自身为 56 字符；审核异步 `req_date` 长度 32，格式却是 yyyyMMdd，同页业务异步为 8；`use_chains_flag` 先写 1=是/2=否，随后又定义 1—4 的渠道组合；`head_huifu_id` 标 N 但条件满足时明确必填。
- 影响：成功判断、跳转 URL 存储和异步 DTO 校验会失败，链路复用配置存在误配风险。
- 建议修改：按真实契约统一 `resp_code/req_date/url`；URL 建议给足可容纳带 query 的上限；只保留一套 `use_chains_flag` 枚举及默认值；将 `head_huifu_id` 改为 C。

### HF-DOC-P1-009 — 微信商户配置新增/查询页字段表互相冲突

- 状态：确认问题；真实长度待开发确认
- 类型：长度 / 表格列错位 / 响应示例
- API：[A01]、[A02]
- 位置：[A01] 异步 `result_list[]`；[A02] 配置结果子表与返回示例
- 证据：[A01] `config_type` 长度 1，枚举和示例却为 `01/02`；`config_stat` 中文名写成“配置值”，实际枚举是状态。[A02] `wx_woa_app_id` 长度 512，而 [A01] 输入同字段为 20；`micro_sub_appid` 一行把“必填/长度”列写成 `32/N`，与表头顺序相反；成功示例只展示 data 内层。
- 影响：字段生成器会读取错误列，长度校验和响应解析不一致。
- 建议修改：修正列顺序和中文名；以后端模型确定 `config_type`、`wx_woa_app_id` 的统一长度；示例补齐完整响应信封。

### HF-DOC-P1-010 — 微信实名认证二维码字段有三种互斥解释

- 状态：确认问题；真实载荷待开发确认
- 类型：返回字段 / 二进制编码
- API：[A04]
- 位置：`response.data.qrcode_data`
- 证据：说明同时称该字段为“二维码图片”、要求 base64 解码得到二进制、又称可直接放入 img 标签；示例实际是完整 `<img src="data:image/png;base64,...">` HTML，而不是纯 base64 或 data URL。
- 影响：客户端可能对 HTML 再做 base64 解码，或把未经处理的响应写入 DOM，造成显示失败和不必要的注入面。
- 建议修改：只选择一种 wire：纯 base64、data URL 或 HTTPS URL；给出准确 MIME、解码代码和长度上限。不要返回 HTML 标签。

### HF-DOC-P1-011 — 支付宝实名主体枚举缺项，示例同时违反多项约束

- 状态：确认问题；社会组织编码待开发确认
- 类型：枚举 / 请求示例
- API：[A05]
- 位置：`auth_identity_info.business_type` 及请求示例
- 证据：枚举列出 0、1、2、3、4、5、7，却在条件说明中继续引用“社会组织”，没有可用编码；同一说明把政府机关、事业单位、社会组织压到 `1/7` 两个编码。请求示例在 `finance_institution_flag=N` 时仍发送金融机构字段，`financial_type=INST` 又不在所列枚举中；辅助材料中的上海行政区代码与浙江/杭州/西湖文本互相矛盾。
- 影响：社会组织无法正确编码，照抄示例会被枚举或业务条件校验拒绝。
- 建议修改：由支付宝适配层确认完整主体枚举后重写映射；用一个内部自洽、能通过校验的非金融或金融示例，不要混用两套场景。

### HF-DOC-P1-012 — 商户费率查询的多选编码和商户号长度无法确定

- 状态：确认问题；真实 wire 待开发确认
- 类型：序列化 / 长度
- API：[M09]
- 位置：请求 `fee_rate_type/huifu_id`、响应 `huifu_id`
- 证据：`fee_rate_type` 类型为 String，却标“支持多选”；内联示例是 JSON 数组，请求示例是包含单引号的 Python 风格数组文本 `['ALI_FEE_RATE']`。请求 `huifu_id` 长度 32，响应为 18 且说明“同入参”。
- 影响：签名原文和服务端反序列化可能不一致，商户号 DTO 也会出现不必要的 18/32 分叉。
- 建议修改：明确多选的唯一 wire（推荐用标准 JSON array，是否采用需后端确认）；禁止单引号伪 JSON；统一同一值的长度。

### HF-DOC-P1-013 — 商户业务开通的捷行付示例含未声明字段和精度冲突

- 状态：确认问题；字段是否正式支持待开发确认
- 类型：参数缺失 / 数值精度
- API：[M03]
- 位置：`jxf_conf_info.jxf_fee_info`
- 证据：请求示例含 `fee_charge_type`，正式参数表没有该字段；`quota_issue_fee_rate` 说明只支持两位小数，示例发送四位小数。
- 影响：调用方无法判断未声明字段是否参与签名、是否会被服务端拒绝，费率示例也可能触发格式校验失败。
- 建议修改：若字段受支持，补入正式参数表并给出类型、长度、必填、枚举；否则从示例删除。把费率示例与后端精度统一。

### HF-DOC-P1-014 — 商户业务开通修改异步 `huifu_id` 被写成产品号

- 状态：确认问题
- 类型：字段语义 / 异步通知
- API：[M07]
- 位置：业务开通结果异步 `data.huifu_id`
- 证据：字段名、中文名和长度均指向 18 位商户号，但说明写“汇付分配的产品号”，示例值为 `YYZY`；同段 `product_id` 已单独存在。
- 影响：消费者可能把产品号写进商户号字段，导致通知无法归属商户。
- 建议修改：说明改为“汇付分配的商户号”，示例改为 18 位合成商户号；保留 `product_id` 承载产品号。顺带把 `josnArray` 改为 `jsonArray`。

### HF-DOC-P1-015 — 用户业务入驻修改对 D1 工作日手续费同时声明生效和不生效

- 状态：确认问题；实际计费规则待开发确认
- 类型：业务规则
- API：[U08]
- 位置：`cash_config[].weekday_fix_amt`、`cash_config[].weekday_fee_rate`
- 证据：同一字段说明先写 `cash_type=D1` 时“不生效”，紧接着又写 D1 工作日按该费率结算。
- 影响：会直接改变手续费计算和商户配置结果，不能由接入方自行选择解释。
- 建议修改：由计费后端确认唯一规则；若 D1 生效，删除“不生效”，并明确未配置时回退到节假日费率的算法。

### HF-DOC-P1-016 — 多个字段的声明长度小于页面自身示例

- 状态：确认问题；应改长度还是改示例需开发确认
- 类型：长度 / 示例
- API：[M03]、[M05]、[M07]、[M09]
- 位置与证据：

| API | 字段 | 声明长度 | 页面示例/枚举长度问题 |
| --- | --- | ---: | --- |
| [M03] | `bank_card_conf.debit_fee_limit` | 4 | `15.00` 为 5 位 |
| [M03] | 银行账户 `card_type` | 1 | 示例 `01`，枚举却为 `0/1` |
| [M05] | `service_phone` | 11 | `021-88888888` 为 12 位 |
| [M05] | `ali_mer_infos.sub_mer_id` | 1 | 示例为 10 位 |
| [M05] | `debit_fee_limit` | 4 | `20.00` 为 5 位 |
| [M05] | 银行账户 `card_type` | 1 | 示例 `01` |
| [M07] | `debit_fee_limit` | 4 | `15.00` 为 5 位 |
| [M07] | 银行账户 `card_type` | 1 | 示例 `01` |
| [M09] | `debit_fee_limit` | 4 | `20.00` 为 5 位 |

- 影响：代码生成器按文档生成的 maxLength 校验会拒绝官方示例或真实返回。
- 建议修改：从后端 schema 导出长度；在文档 CI 中增加“示例值长度不得超过 maxLength”的检查。

### HF-DOC-P2-001 — 34 个费率字段同时允许和排除 0

- 状态：确认问题；零费率是否允许待开发确认
- 类型：取值范围
- API：[M05]（16 处）、[M09]（1 处）、[U13]（17 处）
- 位置：多个 `fee_rate`、银行卡/银联/支付配置费率字段
- 证据：同一句写“大于等于 0”，又给开区间 `(0.00,100.00]`；开区间排除了 0。
- 影响：零费率配置是否有效无法判断，前后端校验可能不一致。
- 建议修改：允许零时统一写 `[0.00,100.00]`；不允许零时统一写 `(0.00,100.00]` 并删除“大于等于 0”。

### HF-DOC-P2-002 — 至少 76 个标量叶字段缺少长度

- 状态：确认问题
- 类型：字段约束缺失
- API：商户 13 页中的 58 个字段，以及 [A01]、[A05]、[U10]、[U11]、[U13]、[U14] 的 18 个字段
- 位置：见“附录 B：缺少长度的标量叶字段”
- 影响：无法生成可靠的 DTO、数据库列和前置校验；调用方只能试错。
- 建议修改：从后端 schema/校验注解机械导出 maxLength；无固定上限时明确写“无业务上限/仅受报文上限限制”，不要留空。

### HF-DOC-P2-003 — 至少 49 个字段说明为空

- 状态：确认问题
- 类型：字段语义缺失
- API：[M01]、[M03]、[M05]、[M07]、[M08]、[U08]、[U10]、[U11]、[U15]
- 位置：商户 13 页 37 个、用户原九页 1 个、合同/统一页面 11 个；见“附录 C”。
- 影响：同名字段在不同父对象下无法区分，异步通知和合同分页尤其难以实现。
- 建议修改：至少补齐语义、返回条件、格式/枚举、是否可空；不要用字段中文名重复充当说明。

### HF-DOC-P2-004 — 异步通知缺少统一可执行协议

- 状态：确认问题；真实回调行为待开发确认
- 类型：Webhook / 运维可靠性
- API：[A01]、[M01]、[M02]、[M03]、[M07]、[M08]、[U03]、[U08]、[U14]
- 位置：审核、业务开通、协议和 AT 配置异步返回章节
- 证据：页面没有统一给出 HTTP method、Content-Type、验签原文、响应状态码、超时、重试次数/间隔、幂等键、乱序/重复通知处理和来源校验。部分页面只给 `ord_id` 的 ACK 字符串，其他回调没有等价规则。
- 影响：调用方即使字段解析正确，也可能因 ACK 不匹配被反复通知或漏单。
- 建议修改：建立一个版本化“异步通知公共协议”并由所有页面引用；每种回调只补充差异项。把 `ord_id`、`req_seq_id/apply_no` 的幂等职责写清楚。

### HF-DOC-P2-005 — 三个接口没有任何成功/失败响应示例

- 状态：确认问题
- 类型：示例完整性
- API：[M09]、[M12]、[M13]
- 位置：返回参数章节末尾
- 证据：页面只有字段表，没有完整响应 JSON；[M12]/[M13] 恰好又存在 `conf_list` 编码歧义。
- 影响：调用方无法确认外层信封、结构字段编码、空结果和失败形态。
- 建议修改：每页增加通过 schema 校验的成功、空结果、业务失败三个最小示例。

### HF-DOC-P2-006 — 商户状态变更的申请单号长度与查询接口不一致

- 状态：待开发确认
- 类型：跨文档一致性
- API：[M06]、[M10]
- 位置：`response.data.apply_no`
- 证据：[M10] 将申请单号长度写为 128，而与其明确关联的 [M06] 申请单状态查询使用 18；[M10] 自身示例也是 16 位。
- 影响：调用方无法判断 128 是真实扩容还是复制错误，跨接口共享模型的约束不一致。
- 建议修改：由后端确认真实最大长度；若没有接口特例，统一为申请单号数据字典的标准长度；若确有扩容，说明格式和兼容边界。

### HF-DOC-P3-001 — Markdown/HTML 标记、错字和内部编辑注释影响可读性

- 状态：确认问题
- 类型：排版 / 维护性
- API：[A03]、[A04]、[A05]、[M01]、[M03]、[M05]、[M07]、[M10]、[U11]、[U13]、[U14]
- 位置与证据：`<font>` 标签数量不平衡（[U14] 40 个开标签、14 个闭标签；[M05] 365/361；[A04] 18/16 等）；使用非法 `</br>`；`josnArray`、`事业部单位法人证书`、`文件jfileID`、`本地生活生活配置对象`、`默认03标志类` 等错字。[M10] 原文残留“某人说这个字段不要了”的内部注释和脆弱的嵌套注释块。
- 影响：页面渲染、搜索、自动抽取和文档专业性受损。
- 建议修改：用标准 `<br/>`，在 CI 中执行 HTML 标签平衡、拼写词典和禁止内部人名注释检查；废弃字段用正式的 deprecated 标记。

### HF-DOC-P3-002 — 更新时间重复、格式不统一，且仍有 HTTP 文档链接

- 状态：确认问题
- 类型：元数据 / 链接规范
- API：[M03]、[M07]、[U15]、以及引用 `http://paas.huifu.com` 的页面
- 位置：页首更新时间和正文引用
- 证据：[U15] 同时展示 `2026.07.06` 与 `2024.9.1` 两个“最近更新时间”；全组日期格式混用 `YYYY.MM.DD`、`YYYY-MM-DD`。文中仍有 4 类 HTTP 链接，当前虽能跳转，但应直接使用 HTTPS。
- 影响：调用方无法判断文档新旧；HTTP 跳转增加混合内容和链路劫持风险。
- 建议修改：页面只保留一个机器可解析的 ISO 日期 `YYYY-MM-DD`；把所有站内 HTTP 引用改为 HTTPS。

## 开发确认清单

| 编号 | 关联问题 | 必须确认的问题 | 文档验收口径 |
| --- | --- | --- | --- |
| Q01 | P1-001 | 图片上传是 multipart 还是 JSON+文件？`file_url` 与文件流分别如何签名？成功响应完整字段是什么？ | 两种上传方式各有可执行请求和完整响应 |
| Q02 | P1-002 | 12 个页面的同步/异步响应是否都带外层 `sign/data`？何时允许不带 sign？ | 字段表、成功/失败示例、验签说明三者一致 |
| Q03 | P1-003 | 列出的 Object/String/Array 字段真实 wire 分别是什么？ | 每个结构字段只有一种 wire 类型，禁止依赖语言 SDK 猜测 |
| Q04 | P1-004 | `C` 是否统一表示条件必填？所有 N+“必填”字段的真实触发条件是什么？ | 发布可执行的 `required_if` 矩阵 |
| Q05 | P1-005/P1-006 | 电子合同成功码是 8 位还是 9 位？列表空结果、分页字段和 `create_time` 的真实名称是什么？ | 三个合同接口共用一致的返回码与分页模型 |
| Q06 | P1-008 | `use_chains_flag` 的完整枚举/默认值是什么？页面 URL 最大长度是多少？ | 枚举不重复，URL 上限覆盖真实返回 |
| Q07 | P1-009/P1-016 | `config_type` 是 1 位还是 2 位；`wx_woa_app_id` 是 20 还是 512；金额长度是否含小数点？ | schema 和示例自动校验通过 |
| Q08 | P1-010 | `qrcode_data` 是纯 base64、data URL 还是 URL？ | 文档只保留一种载荷及配套解码示例 |
| Q09 | P1-011 | 支付宝社会组织的 `business_type` 编码是什么？`INST` 是否为合法金融类型？ | 枚举覆盖所有正文引用主体，示例满足条件约束 |
| Q10 | P1-012 | `fee_rate_type` 的多选 wire 是数组、逗号串还是 JSON 字符串？ | 给出一种标准 JSON 示例及签名原文 |
| Q11 | P1-013 | `fee_charge_type` 是否为正式捷行付字段，费率支持几位小数？ | 参数表、示例、后端校验一致 |
| Q12 | P1-015/P2-001 | D1 工作日手续费是否生效；费率 0 是否允许？ | 计费边界用数学闭区间清楚表达 |
| Q13 | P2-004 | 各回调的 ACK、超时、重试、验签、幂等和乱序策略是什么？ | 建立公共 Webhook 协议并链接到每个异步章节 |
| Q14 | P2-006 | 状态变更返回的 `apply_no` 是否确实允许 128 位，还是应与申请单查询保持一致？ | 数据字典给出统一口径，真实特例显式说明 |

## 覆盖结论

- 未发现独立问题的页面：[M06] 申请单状态查询、[U04] 用户申请单状态查询。它们仍依赖站点公共签名、返回码和链接页面，未做真实 API 调用验证。
- 所有 JSON 代码块在把不间断空格规范为空格后均可解析，未发现 JSON 重复 key。
- 34 个主链接均为 200，没有确认的主链接失效问题。
- 16 个归一化一级引用资源均可访问，包括 8 个 XLSX/DOCX 文件。SPA fragment 的页面内锚点没有浏览器级断言。
- 2026-08-31 仓库快照覆盖的 22 页中，21 页与当前在线 SHA 完全一致；仅 [M08] 发生变化：更新时间改为 2026-09-03，并在 `card_info.is_settle_default` 增加更换结算卡时需传 Y 的说明。本报告以当前在线版本为准。
- 未发起任何真实业务 API 请求，因此无法验证实际后端枚举、必填条件、返回 wire、回调重试和错误码行为。

## 附录 A：在线来源、状态与内容哈希

| ID | 文档 | HTTP | Content-Type | SHA-256 |
| --- | --- | ---: | --- | --- |
| [M01] | 企业商户进件 | 200 | text/markdown | `ae2744b9142fe463010b4a9d66a89b0c5ef3e84576f87a553bc59331dd868415` |
| [M02] | 个人商户进件 | 200 | text/markdown | `03c5059bc4ad2aea832fe98bee356bf199e28bc27c74be22ef641e84af0d7d36` |
| [M03] | 商户业务开通 | 200 | text/markdown | `9b62bba487f981bbdd293f0328a68b3c8c526b1fa1d47a8ab7b8912b427b6ec5` |
| [M04] | 图片上传 | 200 | application/json | `e1acf74e60436d069f3c605c19b24aab6d703494e1ebdd8c90b11104e4646125` |
| [M05] | 商户详细信息查询 | 200 | text/markdown | `8f1b46ae924919fac886d9f96ad3da3b2fbb7d48aae892e8ac236ea15bb1e66a` |
| [M06] | 申请单状态查询 | 200 | text/markdown | `89f51fdbca529b1f7166aeba1d5d24eb16469fd153cd09cafbf811d9e68f050f` |
| [M07] | 商户业务开通修改 | 200 | text/markdown | `51a11858b9d312a3e6112f6abf91e1b9a1dbb1db4ed4f4dd27fa14950094d1d9` |
| [M08] | 商户基本信息修改 | 200 | text/markdown | `965d8f528cb8ac1fbeabe12f51bd0355213f7d3ba38b506588daeff2beb9c617` |
| [M09] | 商户费率信息查询 | 200 | text/markdown | `c9bfb5ed774cf8bce622bb536d16b1ed60ffedd5bd5540bf83177cdf592008b9` |
| [M10] | 商户状态变更 | 200 | text/markdown | `d2fe6ab4404abd79b3ac5f5eecffaaec9d61d245ac1a60ebccddee889535a07f` |
| [M11] | 商户短信发送 | 200 | text/markdown | `562e269268e10248931e0c9ed556a99e88966ddd953b67333f9a106df5934bc3` |
| [M12] | 商户多费率配置 | 200 | text/markdown | `0536049a616e68929341d4176cf1c5348b1bcf8fabeff3ceb384945fa5dce987` |
| [M13] | 商户多费率配置查询 | 200 | text/markdown | `6a5b970177f67985f1ce20c6b2900580117496f870c97c3391055afaaa66438f` |
| [U01] | 企业用户开户 | 200 | text/markdown | `4d0d3921368a9f536007a17a6efe8ed1d9c7d9eea40d9a3a4fd5dc8eef07baaf` |
| [U02] | 个人用户开户 | 200 | text/markdown | `0bcf5b8e085d7c6e760f7452d2fe7d3bb7879812de6a7953d41a4b44c53cee8c` |
| [U03] | 用户业务入驻 | 200 | text/markdown | `71fbf48ce46923034ac973488d1c73f1d376735028e13144839cb0031ff64249` |
| [U04] | 用户申请单状态查询 | 200 | text/markdown | `f7894c5e2bc3544a9501922d4e3d5bb8b1f054704a80c36405a51ef2ad768e56` |
| [U05] | 用户信息查询 | 200 | text/markdown | `2d1099e1af4af840d108a9f81d23b01119776ab494f893b45a0873805a072906` |
| [U06] | 企业用户基本信息修改 | 200 | text/markdown | `55f762001ed26859412b98248b71dc8aaecc3e508ec6669bc6e0bec92c6eb90d` |
| [U07] | 个人用户基本信息修改 | 200 | text/markdown | `f78db9dc5401496265b7836eb1dc3cdf6cce47263a0de366f29c0008c33ce23c` |
| [U08] | 用户业务入驻修改 | 200 | text/markdown | `e8abc91b15587be26552d8989c408769246e4686fcdde02b74efec581344faf9` |
| [U09] | 用户列表查询 | 200 | text/markdown | `606b95a1188cb64ed34daad76ebdb678225d3589fbbf7bea9e02f83698bf7f5f` |
| [U10] | 电子合同重发 | 200 | text/markdown | `1442a135b867cff33633afc5f42c6c69fd01096bb1bf4f793695b56652ace2a9` |
| [U11] | 电子合同列表查询 | 200 | text/markdown | `5e37abbb156201807b305b897aff531b70b627187fea8aad6b35eb90ff540746` |
| [U12] | 电子合同拒签 | 200 | text/markdown | `292ff70e8d3bd9a5f76421164d719ab5bf1844c81ca9712e32104b74a38f9c9c` |
| [U13] | 开通下级商户权限配置 | 200 | text/markdown | `f07ab5b3eab7e5bf36b4d31f9726aec0be9e9011f0b0435a1e42c7ee74e7ab3b` |
| [U14] | 商户统一进件（页面版） | 200 | text/markdown | `35e643b075ceccc7ec789e9fc7cb8a5bda9ea91a920db477abdbbaa87b035886` |
| [U15] | 统一进件页面版查询 | 200 | text/markdown | `ad14a14bc54bc2988b9f9520a11c52430e54ba0c6664faf5eaf126a05a632d94` |
| [A01] | 微信商户配置 | 200 | text/markdown | `9da3d982a8a68cac20c94a17a400efe3cf8d2715e5404f0e5c9498a3e52e8e4f` |
| [A02] | 微信商户配置查询 | 200 | text/markdown | `99937c6b7807a691d017830e8553521b1e13691f66a02473dcf6ce3e6bc0924e` |
| [A03] | 微信实名认证 | 200 | text/markdown | `41d4520a560c4cafb61cf8b87f7d15bf316c949e2b126a131833e343c8fa3197` |
| [A04] | 微信实名认证状态查询 | 200 | text/markdown | `8477b7bada0041c3f7ef6fc33ae2a35d041a3898e6ef2c23f6d1ff2d7be66872` |
| [A05] | 支付宝实名申请提交 | 200 | text/markdown | `fbc838ab36e99ad48c7e96c09304fa869879031e883d0eb55ad805cdc364a0a1` |
| [A06] | 支付宝实名申请单查询 | 200 | text/markdown | `cf2e66377106963060ac93656e20bfbc13e0dc4f1a1eaba0b935e9e7f2a8bed6` |

## 附录 B：缺少长度的标量叶字段

商户 13 页机械提取到 58 个：

```text
M01 request.data.activated_products
M01 request.data.material_card_info.{card_name,card_no,prov_id,area_id,branch_code}
M01 request.data.head_type
M02 request.data.settle_config.settle_pattern
M02 request.data.activated_products
M03 request.data.ali_conf_list[].al_real_name_info.finance_institution_flag
M03 request.data.wx_conf_list[].wx_real_name_info.finance_institution_flag
M03 request.data.wx_zl_conf.sales_info.fee_rate_file_list
M03 request.data.online_fee_conf_list[].fee_formula_type
M03 request.data.hb_fq_fee_config.{twentyfour_period,acq_twentyfour_period}
M03 request.data.merge_pay_config_info.{merge_pay_flag,merge_pay_config.merge_pay_mode}
M03 request.data.withhold_pay_scene
M03 async.audit.sign
M05 response.data.qry_cash_config_list[].out_cash_acct_type
M05 response.data.online_fee_conf_list[].{fee_min_amt,fee_formula_type}
M05 response.data.forced_delay_flag
M05 response.data.qry_wx_conf_list[].pay_channel_id_list[]
M05 response.data.qry_ali_conf_list[].ali_mer_infos.sub_mer_id
M05 response.data.qry_ali_conf_list[].{fee_rate,pay_channel_id_list}
M05 response.data.qry_union_conf.{debit_fee_rate_up,debit_fee_rate_down}
M05 response.data.surrogate_config_list[].fee_formula_type
M05 response.data.lla_withhold_config.{fee_rate,lla_withhold_flag}
M05 response.data.merge_pay_config_info.{merge_pay_flag,merge_pay_config.merge_pay_mode}
M05 response.data.{activated_products,withhold_pay_scene}
M05 response.data.material_card_info.{card_type,card_name,card_no,prov_id,area_id,branch_code}
M07 request.data.online_fee_conf_list[].fee_formula_type
M07 request.data.ali_conf_list[].al_real_name_info.finance_institution_flag
M07 request.data.wx_conf_list[].wx_real_name_info.finance_institution_flag
M07 request.data.wx_zl_conf.wx_zl_pay_conf_list[].sales_info.fee_rate_file_list
M07 request.data.merge_pay_config_info.{merge_pay_flag,merge_pay_config.merge_pay_mode}
M07 request.data.withhold_pay_scene
M07 async.audit.sign
M08 request.data.activated_products
M09 request.data.fee_rate_type
M09 response.data.ali_fee_rate_list[].fee_rate
M11 request.data.{verify_type,operation_type}
M11 response.data.{verify_type,operation_type,phone}
```

其余 18 个：

```text
A01 async.sign
A05 response.data.order_status
U10 request.data.{req_seq_id,req_date,huifu_id,agreement_id,sign_user_email}
U11 request.data.{agreement_type,page_size}
U11 response.data.result_list[].{scene_code_desc,order_id}
U13 request.data.{fee_formula_type,lla_withhold_config.llaWithholdFlag,lla_withhold_config.fee_rate}
U13 response.data.{resp_code,resp_desc,product_id}
U14 async.sign
```

## 附录 C：说明为空的字段

商户 13 页 37 个：

```text
M01 request.data.share_holder_info_list[].mobile_no
M03 request.data.ali_conf_list[].al_real_name_info.{contact_person_info,legal_person_info}
M03 async.agreement.{sub_resp_code,sub_resp_desc,req_seq_id,req_date,huifu_id,apply_no}
M03 async.agreement.agreement_info_list.{agreement_link,agreement_name}
M05 response.data.qry_ali_conf_list[].ali_mer_infos
M05 response.data.qry_union_conf.qr_code_info
M05 response.data.elec_acct_config.elec_card_list[].token_no
M05 response.data.share_holder_info_list[].mobile_no
M05 response.data.lla_withhold_config.fee_rate
M05 response.data.material_card_info.card_name
M07 request.data.ali_conf_list[].al_real_name_info.{contact_person_info,legal_person_info}
M07 request.data.wx_zl_conf.wx_zl_pay_conf_list[]
M07 async.agreement.{sub_resp_code,sub_resp_desc,req_seq_id,req_date,huifu_id,apply_no}
M07 async.agreement.agreement_info_list.{agreement_link,agreement_name}
M08 request.data.share_holder_info_list[].mobile_no
M08 async.agreement.{sub_resp_code,sub_resp_desc,req_seq_id,req_date,huifu_id,apply_no}
M08 async.agreement.agreement_info_list.{agreement_link,agreement_name}
```

用户原九页与额外页面共 12 个字段：

```text
U08 async.data
U10 request.data.{agreement_id,sign_user_email}
U11 request.data.{order_id,mer_name,page_num,page_size,product_id}
U11 response.data.result_list[].{download_url,scene_code_desc}
U15 response.data.agreement_info_list[].{agreement_link,agreement_name}
```

## 在线文档引用

[M01]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md
[M02]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md
[M03]: https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md
[M04]: https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json
[M05]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md
[M06]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md
[M07]: https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md
[M08]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md
[M09]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md
[M10]: https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md
[M11]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md
[M12]: https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md
[M13]: https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md
[U01]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxzc.md
[U02]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxzc.md
[U03]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrz.md
[U04]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhsqdzt.md
[U05]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhywcx.md
[U06]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxxg.md
[U07]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxxg.md
[U08]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrzxg.md
[U09]: https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhlbcx.md
[U10]: https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtcf.md
[U11]: https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtsqlbcx.md
[U12]: https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtjq.md
[U13]: https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_xjshpz.md
[U14]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shtyjjweb.md
[U15]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shtyjjwebcx.md
[A01]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxshpz.md
[A02]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxshpzcx.md
[A03]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrz.md
[A04]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrzztcx.md
[A05]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmrz.md
[A06]: https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmcx.md
