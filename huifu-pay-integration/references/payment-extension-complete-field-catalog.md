# 新增支付接口完整字段目录

来源日期：2026-10-25。共7个接口、238条完整字段路径。基础目录及其历史锁独立保留。

## 目录

- 使用规则
- 覆盖摘要
- 交易确认
- 交易确认查询
- 交易确认退款
- 交易确认退款查询
- 账户余额信息查询
- 账务流水查询
- 账务流水汇总结果查询

## 使用规则

字段身份为接口＋方向＋完整路径，不能按叶字段名去重。类型、长度和Y/N/C为空时保留未知；C按条件必填。String(JSON)逐层编码/解码，数组标记不是wire字段名。官网表与示例冲突须联读原子参考；本目录不将示例修成合同。

JSON退款查询只覆盖正式请求；汇总查询的正式返回表保留官网同步章节位置，正文异步描述的矛盾与通知协议缺口见原子参考，不能自动外推为完整Webhook。

## 覆盖摘要

| 接口 | 字段路径 | 根表 | 嵌套表 |
| --- | --- | --- | --- |
| 交易确认 | 72 | 6 | 7 |
| 交易确认查询 | 26 | 4 | 2 |
| 交易确认退款 | 45 | 4 | 4 |
| 交易确认退款查询 | 4 | 1 | 0 |
| 账户余额信息查询 | 26 | 3 | 2 |
| 账务流水查询 | 40 | 3 | 2 |
| 账务流水汇总结果查询 | 25 | 3 | 2 |

## 交易确认

- 官方来源：<https://paas.huifu.com/partners/api/doc/smzf/api_jyqr.md>
- SHA-256：`9fbf6c70cb9be4422fb2b0a724588c7bda363f6a8bb779cba54435a5e86c82fc`

### 请求信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id、（org_req_date、org_req_seq_id）、（org_req_date、org_mer_ord_id）三选一；**余额支付仅支持使用org_req_date+org_req_seq_id进行确认**；示例值：[官网示例已脱敏] |
| `request.data.org_mer_ord_id` | `request.data.org_mer_ord_id` | `—（直接 JSON 路径）` | 原交易商户订单号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id、（org_req_date、org_req_seq_id）、（org_req_date、org_mer_ord_id）三选一；示例值：[官网示例已脱敏] |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易全局流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id、（org_req_date、org_req_seq_id）、（org_req_date、org_mer_ord_id）三选一；示例值：00470topo1A211015160805P090ac132fef00000 |
| `request.data.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `4000` | `N` | 已确认 | jsonObject字符串；**为空时按交易时的分账串处理分账资金** |
| `request.data.acct_split_bunch.percentage_flag` | `request.data.acct_split_bunch` | `$.percentage_flag` | 百分比分账标志 | `String` | `1` | `N` | 已确认 | Y:使用百分比分账；示例值：Y |
| `request.data.acct_split_bunch.total_div_amt` | `request.data.acct_split_bunch` | `$.total_div_amt` | 分账总金额（元） | `String` | `14` | `C` | 已确认 | 本次交易确认总额。需保留小数点后两位；percentage_flag=Y时必填。该金额与分账百分比用来计算分账金额。示例值：10.00 |
| `request.data.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `2048` | `N` | 已确认 | 分账明细 |
| `request.data.acct_split_bunch.acct_infos[].percentage_div` | `request.data.acct_split_bunch` | `$.acct_infos[].percentage_div` | 分账百分比% | `String` | `6` | `N` | 已确认 | 示例值：23.50，表示23.50%。仅在percentage_flag=Y时起作用； acct_infos中全部分账百分比只和必须为100.00%。 |
| `request.data.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额(元) | `String` | `14` | `C` | 已确认 | 单位元，需保留小数点后两位，最低传入0.01 ，示例值：1.00 ，percentage_flag非Y时必填；percentage_flag=Y时div_amt不填，div_amt=total_div_amt*percentage_div |
| `request.data.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch.acct_infos[].acct_id` | `request.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 分账接收方账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户；示例值：F00598600 |
| `request.data.risk_check_data` | `request.data.risk_check_data` | `—（String(JSON) 容器）` | 安全信息 | `String` | `4000` | `N` | 已确认 | 安全信息，jsonObject字符串 |
| `request.data.risk_check_data.ip_addr` | `request.data.risk_check_data` | `$.ip_addr` | ip地址 | `String` | `32` | `N` | 已确认 | IP地址、经纬度、基站地址最少要送其中一项；示例值：172.28.52.52 |
| `request.data.risk_check_data.base_station` | `request.data.risk_check_data` | `$.base_station` | 基站地址 | `String` | `32` | `N` | 已确认 | IP地址、经纬度、基站地址最少要送其中一项；【mcc】+【mnc】+【location_cd】+【lbs_num】；- mcc:移动国家代码，460代表中国；3位长；- mnc：移动网络号码；2位长；- location_cd：位置区域码，16进制，5位长；- lbs_num：基站编号，16进制，5位长；- 注意若位数不足用空格补足；示例值：460001039217563，其中460（mcc)， 00(mnc)，10392(location_cd)， 17563(lbs_num) |
| `request.data.risk_check_data.latitude` | `request.data.risk_check_data` | `$.latitude` | 纬度 | `String` | `32` | `N` | 已确认 | 格式：+表示北纬，-表示南纬。纬度整数位不超过2位，小数位不超过6位。示例值：+37.12；IP地址、经纬度、基站地址最少要送其中一项 |
| `request.data.risk_check_data.longitude` | `request.data.risk_check_data` | `$.longitude` | 经度 | `String` | `32` | `N` | 已确认 | 格式：+表示东经，-表示西经；经度整数位不超过3位，小数位不超过5位；示例值：-121.213；IP地址、经纬度、基站地址最少要送其中一项 |
| `request.data.risk_check_data.sub_product` | `request.data.risk_check_data` | `$.sub_product` | 产品子类 | `String` | `20` | `N` | 已确认 | 推广大使、一卡通（智汇管家2.0必填）；示例值：-121.213 |
| `request.data.risk_check_data.transfer_type` | `request.data.risk_check_data` | `$.transfer_type` | 转账原因 | `String` | `2` | `N` | 已确认 | 01：卡券推广类,02：卡券核销类,03：消费,04：工资代发,05：分润；示例值：03 |
| `request.data.pay_type` | `request.data.pay_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `16` | `C` | 已确认 | **原交易为快捷支付必填：QUICK_PAY**；**原交易为余额支付必填：ACCT_PAYMENT**；原交易为全域资金必填：REMITTANCE_PAY；示例值：ACCT_PAYMENT |
| `request.data.remark` | `request.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 原样返回；示例值：备注 |

### 同步响应 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/smzf/api_jyqr.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/smzf/api_jyqr.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：交易成功 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值:[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20221013 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 业务请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `Y` | 已确认 | P:处理中；S：成功；F：失败；示例值：S |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `response.data.unconfirm_amt` | `response.data.unconfirm_amt` | `—（直接 JSON 路径）` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.confirmed_amt` | `response.data.confirmed_amt` | `—（直接 JSON 路径）` | 已确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.acct_resp_code` | `response.data.acct_resp_code` | `—（直接 JSON 路径）` | 账务返回码 | `String` | `16` | `N` | 已确认 | 示例值：000 |
| `response.data.acct_resp_desc` | `response.data.acct_resp_desc` | `—（直接 JSON 路径）` | 账务返回描述 | `String` | `256` | `N` | 已确认 | 示例值：成功 |
| `response.data.org_mer_ord_id` | `response.data.org_mer_ord_id` | `—（直接 JSON 路径）` | 原交易商户订单号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 支付交易业务请求时间 | `String` | `8` | `Y` | 已确认 | 示例值：20221012 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 支付交易业务请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 支付交易汇付全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00001 |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | — |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额(元) | `String` | `14` | `Y` | 已确认 | 单位元，示例值:1.00 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 示例值:[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].acct_id` | `response.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 分账接收方账户号 | `String` | `32` | `Y` | 已确认 | 示例值:F00598600 |
| `response.data.acct_split_bunch.acct_infos[].split_fee_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].split_fee_amt` | 分账手续费金额(元) | `String` | `14` | `N` | 已确认 | 示例值:0.10 |
| `response.data.acct_split_bunch.acct_infos[].split_fee_huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `N` | 已确认 | 示例值:[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].split_fee_acct_id` | `response.data.acct_split_bunch` | `$.acct_infos[].split_fee_acct_id` | 分账手续费承担方账号 | `String` | `32` | `N` | 已确认 | 示例值:F00598600 |
| `response.data.acct_split_bunch.acct_infos[].unconfirm_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].unconfirm_amt` | 待确认金额(元) | `String` | `14` | `N` | 已确认 | 示例值:0.10 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 请求参数里传入，返回参数里原样返回；示例值：备注 |

### 异步信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `async.resp_code` | `async.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `string` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%ba%bf%e4%b8%8a%e4%ba%a4%e6%98%93%e8%bf%94%e5%9b%9e%e7%a0%81)),示例值：00000000 |
| `async.resp_desc` | `async.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `string` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%ba%bf%e4%b8%8a%e4%ba%a4%e6%98%93%e8%bf%94%e5%9b%9e%e7%a0%81))，示例值：交易成功[000] |
| `async.resp_data` | `async.resp_data` | `—（直接 JSON 路径）` | 业务数据 | `string` | `—` | `Y` | [需要官方确认]：长度 | 业务数据，见resp_data |

### 异步 resp_data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `async.resp_data.req_seq_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 业务请求流水号 | `String` | `128` | `Y` | 已确认 | 业务请求流水号 |
| `async.resp_data.req_date` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 业务请求时间yyyyMMdd | `String` | `8` | `Y` | 已确认 | 业务请求时间yyyyMMdd |
| `async.resp_data.huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商户号 | `String` | `32` | `Y` | 已确认 | 商户号 |
| `async.resp_data.hf_seq_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 汇付全局流水号 | `String` | `128` | `Y` | 已确认 | 汇付全局流水号 |
| `async.resp_data.trans_stat` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 交易状态 | `String` | `1` | `Y` | 已确认 | S：成功，F：失败。 |
| `async.resp_data.acct_split_bunch` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账对象 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.resp_data.acct_split_bunch.acct_infos[]` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | — |
| `async.resp_data.acct_split_bunch.acct_infos[].div_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账金额(元) | `String` | `14` | `Y` | 已确认 | 单位元，示例值:1.00 |
| `async.resp_data.acct_split_bunch.acct_infos[].huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 示例值:[官网示例已脱敏] |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账接收方账户号 | `String` | `32` | `Y` | 已确认 | 示例值:F00598600 |
| `async.resp_data.acct_split_bunch.acct_infos[].split_fee_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账手续费金额(元) | `String` | `14` | `N` | 已确认 | 示例值:0.10 |
| `async.resp_data.acct_split_bunch.acct_infos[].split_fee_huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账手续费承担方商户号 | `String` | `32` | `N` | 已确认 | 示例值:[官网示例已脱敏] |
| `async.resp_data.acct_split_bunch.acct_infos[].split_fee_acct_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账手续费承担方账号 | `String` | `32` | `N` | 已确认 | 示例值:F00598600 |
| `async.resp_data.remark` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 备注 | `String` | `256` | `N` | 已确认 | 请求参数里传入，返回参数里原样返回；示例值：备注 |


## 交易确认查询

- 官方来源：<https://paas.huifu.com/partners/api/doc/smzf/api_jyqrcx.md>
- SHA-256：`da52b2f0ad6afe88d1487ee5235e6dc31e4411f4e1f3aec1b2de4c3387415526`

### 请求信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220905 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原请求流水号 | `String` | `128` | `Y` | 已确认 | 交易确认接口的请求流水号；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成；示例值：[官网示例已脱敏] |

### 同步响应 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/smzf/api_jyqrcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/smzf/api_jyqrcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：查询成功 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值:[官网示例已脱敏] |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `2` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：P |
| `response.data.unconfirm_amt` | `response.data.unconfirm_amt` | `—（直接 JSON 路径）` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 待确认总金额；单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.confirmed_amt` | `response.data.confirmed_amt` | `—（直接 JSON 路径）` | 已确认总金额 | `String` | `14` | `N` | 已确认 | 已确认总金额；单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 汇付全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `response.data.acct_split_bunch[]` | `response.data.acct_split_bunch` | `—（String(JSON Array) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账明细信息，jsonArray字符串。 |
| `response.data.acct_split_bunch[].acct_infos[]` | `response.data.acct_split_bunch` | `$[].acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | — |
| `response.data.acct_split_bunch[].acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$[].acct_infos[].div_amt` | 分账金额(元) | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，最低传入0.01；示例值:1.00 |
| `response.data.acct_split_bunch[].acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$[].acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值:[官网示例已脱敏] |
| `response.data.acct_split_bunch[].acct_infos[].acct_id` | `response.data.acct_split_bunch` | `$[].acct_infos[].acct_id` | 分账接收方账户号 | `String` | `9` | `N` | 已确认 | 示例值:F00598600 |
| `response.data.acct_split_bunch[].acct_infos[].split_fee_amt` | `response.data.acct_split_bunch` | `$[].acct_infos[].split_fee_amt` | 分账手续费金额(元) | `String` | `14` | `N` | 已确认 | 示例值:0.10 |
| `response.data.acct_split_bunch[].acct_infos[].split_fee_huifu_id` | `response.data.acct_split_bunch` | `$[].acct_infos[].split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `N` | 已确认 | 示例值:[官网示例已脱敏] |
| `response.data.acct_split_bunch[].acct_infos[].split_fee_acct_id` | `response.data.acct_split_bunch` | `$[].acct_infos[].split_fee_acct_id` | 分账手续费承担方账号 | `String` | `32` | `N` | 已确认 | 示例值:F00598600 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 请求参数里传入，返回参数里原样返回；示例值：备注 |


## 交易确认退款

- 官方来源：<https://paas.huifu.com/partners/api/doc/smzf/api_jyqrtk.md>
- SHA-256：`e740c12c8884f7f5ec242f0e1a053530f37ce2cd24418924b3f9f9a819c7f9ad`

### 请求信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20210917 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 指交易确认请求日期，格式为yyyyMMdd，示例值：20210917 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `Y` | 已确认 | 指交易确认请求流水号，示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `4000` | `N` | 已确认 | 分账信息，jsonObject字符串。 |
| `request.data.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | 分账明细 |
| `request.data.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额(元) | `String` | `14` | `Y` | 已确认 | 被分账商户退款金额；保留两位小数，示例值：1.00，最低传入0.01 |
| `request.data.acct_split_bunch.acct_infos[].part_loan_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].part_loan_amt` | 垫资金额(元) | `String` | `12` | `N` | 已确认 | 垫资方退款金额；保留两位小数，示例值：1.00，最低传入0.01；注：若指定了垫资方且由垫资方全额垫资，则该字段为空 |
| `request.data.loan_flag` | `request.data.loan_flag` | `—（直接 JSON 路径）` | 是否垫资退款 | `String` | `2` | `N` | 已确认 | Y 是垫资出款， N 是普通出款， 为空默认N；示例值：N |
| `request.data.loan_undertaker` | `request.data.loan_undertaker` | `—（直接 JSON 路径）` | 垫资承担者 | `String` | `32` | `N` | 已确认 | 垫资方的huifu_id；为空: 各自承担。不为空走第三方垫资。；示例值：[官网示例已脱敏]；目前支持商户垫资。**垫资方一定参与了交易分账，否则不支持垫资**。 |
| `request.data.loan_acct_type` | `request.data.loan_acct_type` | `—（直接 JSON 路径）` | 垫资账户类型 | `String` | `2` | `N` | 已确认 | 01:基本户, 05: 充值户, 默认充值户；示例值：05 |
| `request.data.remark` | `request.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 示例值：备注 |

### 同步响应 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/smzf/api_jyqrtk.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/smzf/api_jyqrtk.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：交易成功 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `Y` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值:[官网示例已脱敏] |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.unconfirm_amt` | `response.data.unconfirm_amt` | `—（直接 JSON 路径）` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 待确认总金额；单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.confirmed_amt` | `response.data.confirmed_amt` | `—（直接 JSON 路径）` | 已确认总金额 | `String` | `14` | `N` | 已确认 | 已确认总金额；单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 支付交易业务请求时间 | `String` | `8` | `Y` | 已确认 | 示例值：20210917 |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 支付交易汇付全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00001 |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | — |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额(元) | `String` | `14` | `Y` | 已确认 | 单位元，示例值:1.00 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 示例值:[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].acct_id` | `response.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 分账接收方账户号 | `String` | `32` | `Y` | 已确认 | 示例值:F00598600 |
| `response.data.acct_split_bunch.acct_infos[].split_fee_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].split_fee_amt` | 分账手续费金额(元) | `String` | `14` | `N` | 已确认 | 示例值:0.10 |
| `response.data.acct_split_bunch.acct_infos[].split_fee_huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `N` | 已确认 | 示例值:[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].split_fee_acct_id` | `response.data.acct_split_bunch` | `$.acct_infos[].split_fee_acct_id` | 分账手续费承担方账号 | `String` | `32` | `N` | 已确认 | 示例值:F00598600 |
| `response.data.acct_split_bunch.acct_infos[].part_loan_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].part_loan_amt` | 垫资金额(元) | `String` | `12` | `N` | 已确认 | 垫资方退款金额；保留两位小数 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 请求参数里传入，返回参数里原样返回；示例值：备注 |
| `response.data.loan_flag` | `response.data.loan_flag` | `—（直接 JSON 路径）` | 是否垫资退款 | `String` | `2` | `N` | 已确认 | Y 是垫资出款， N 是普通出款, 按请求原样返回 |
| `response.data.loan_undertaker` | `response.data.loan_undertaker` | `—（直接 JSON 路径）` | 垫资承担者 | `String` | `32` | `N` | 已确认 | 垫资方的huifu_id, 按请求原样返回 |
| `response.data.loan_acct_type` | `response.data.loan_acct_type` | `—（直接 JSON 路径）` | 垫资账户类型 | `String` | `2` | `N` | 已确认 | 01:基本户, 05: 充值户, 按请求原样返回 |


## 交易确认退款查询

- 官方来源：<https://paas.huifu.com/navigator/ossApi/api_jyqrtkcq.json>
- SHA-256：`65fa17cd59e7d18637ddb920e3e74a337d91e49821c4f96ad184538e9f9aae46`

本来源仅含正式请求data；requestDemo只作演示，不定义公共信封类型/必填或响应。未公布同步响应、通知、HTTP方法；SDK的POST是独立源码事实。

### 正式请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成。示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 指交易确认退款请求日期，格式为yyyyMMdd，示例值：20210917 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号指交易确认退款请求流水号，org_req_seq_id和org_hf_seq_id二选一；示例值：[官网示例已脱敏] | `String` | `128` | `C` | 已确认 | 指交易确认退款请求流水号，org_req_seq_id和org_hf_seq_id二选一；示例值：[官网示例已脱敏] |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原退款全局流水号原交易确认退款全局流水号。org_req_seq_id和org_hf_seq_id二选一；示例值：003500TOP2B211021163242P447ac132fd200000 | `String` | `128` | `C` | 已确认 | 原交易确认退款全局流水号。org_req_seq_id和org_hf_seq_id二选一；示例值：003500TOP2B211021163242P447ac132fd200000 |


## 账户余额信息查询

- 官方来源：<https://paas.huifu.com/partners/api/doc/jyjs/api_jyjs_yuexxcx.md>
- SHA-256：`4684913f1338f44423f025d72a73b7012e477dd48ec82b3a9216340571f6d39e`

### 请求信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/代理商/商户的huifu_id ；（1）当主体为渠道商/代理商时，此字段填写渠道商/代理商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：HFQ |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求时间yyyyMMdd；示例值：20221123 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `N` | 已确认 | 请求方生成，用于定位查询请求，示例值：[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `request.data.acct_date` | `request.data.acct_date` | `—（直接 JSON 路径）` | 账务日期 | `String` | `8` | `N` | 已确认 | 账务日期yyyyMMdd，默认为当天；示例值：20221123 |

### 同步响应信封及 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 交易响应内容体 | `Object` | `—` | `N` | N/A：结构字段长度 | 业务返回参数，jsonObject格式 |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务响应码](https://paas.huifu.com/partners/api/doc/jyjs/api_jyjs_yuexxcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务响应信息](https://paas.huifu.com/partners/api/doc/jyjs/api_jyjs_yuexxcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：查询成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `N` | 已确认 | 交易时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.acctInfo_list[]` | `response.data.acctInfo_list` | `—（String(JSON Array) 容器）` | 账户信息列表 | `String` | `—` | `N` | [需要官方确认]：长度 | JsonArray格式；各子账户余额信息 |
| `response.data.acctInfo_list[].huifu_id` | `response.data.acctInfo_list` | `$[].huifu_id` | 商户号 | `String` | `32` | `Y` | 已确认 | 汇付分配的商户号，例[官网示例已脱敏]；示例值：[官网示例已脱敏] |
| `response.data.acctInfo_list[].acct_id` | `response.data.acctInfo_list` | `$[].acct_id` | 账户号 | `String` | `9` | `Y` | 已确认 | 商户账户的账户号；示例值：C00690000 |
| `response.data.acctInfo_list[].acct_type` | `response.data.acctInfo_list` | `$[].acct_type` | 账户类型 | `String` | `19` | `Y` | 已确认 | 01:基本户 02:现金户 03：延时户 04:钱包户 05:充值户 09营销户；示例值：01 |
| `response.data.acctInfo_list[].balance_amt` | `response.data.acctInfo_list` | `$[].balance_amt` | 账户余额 | `String` | `16` | `N` | 已确认 | balanceAmt=avlBal+frzBal；保留2位小数；账务日期为当天时返回；示例值：2100.00 |
| `response.data.acctInfo_list[].avl_bal` | `response.data.acctInfo_list` | `$[].avl_bal` | 可用余额 | `String` | `16` | `N` | 已确认 | 账户可用余额，保留2位小数；账务日期为当天时返回；示例值：2000.00 |
| `response.data.acctInfo_list[].frz_bal` | `response.data.acctInfo_list` | `$[].frz_bal` | 冻结余额 | `String` | `16` | `N` | 已确认 | 账户冻结余额，保留2位小数；账务日期为当天时返回；示例值：100.00 |
| `response.data.acctInfo_list[].last_avl_bal` | `response.data.acctInfo_list` | `$[].last_avl_bal` | 昨日日终余额 | `String` | `16` | `Y` | 已确认 | 昨日可用余额，保留2位小数；示例值：1000.00 |
| `response.data.acctInfo_list[].acct_stat` | `response.data.acctInfo_list` | `$[].acct_stat` | 状态 | `String` | `1` | `N` | 已确认 | N：“正常”; C：“关闭”; F：“冻结”; D：“销户”；示例值：N |
| `response.data.acctInfo_list[].control_bal` | `response.data.acctInfo_list` | `$[].control_bal` | 管控金额 | `String` | `16` | `N` | 已确认 | 该金额包含在冻结金额中；示例值：2100.00 |
| `response.data.acctInfo_list[].last_balance_amt` | `response.data.acctInfo_list` | `$[].last_balance_amt` | 昨日账户余额 | `String` | `16` | `Y` | 已确认 | 昨日账户余额，保留2位小数；示例值：1000.00 |
| `response.data.acctInfo_list[].last_frz_bal` | `response.data.acctInfo_list` | `$[].last_frz_bal` | 昨日冻结余额 | `String` | `16` | `Y` | 已确认 | 昨日冻结余额，保留2位小数；示例值：1000.00 |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `N` | 已确认 | [接口加签验签说明](https://paas.huifu.com/partners/guide/#/api_v2jqyq) |


## 账务流水查询

- 官方来源：<https://paas.huifu.com/partners/api/doc/yuer/api_acctlscx.md>
- SHA-256：`46295c022efcc9464472d396cfe4c2befd74ba634a8c6f02e183fe1f99dd30c2`

### 请求信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：HUIFENQI |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一商户号当天唯一，示例值：[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 渠道/代理/商户/用户编号 | `String` | `32` | `Y` | 已确认 | 汇付分配的渠道商、代理商、商户、用户的编号，示例值：[官网示例已脱敏] |
| `request.data.acct_date` | `request.data.acct_date` | `—（直接 JSON 路径）` | 账务日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `request.data.page_size` | `request.data.page_size` | `—（直接 JSON 路径）` | 每页条数 | `String` | `8` | `N` | 已确认 | 最大100。不传则默认10。示例值：10 |
| `request.data.page_num` | `request.data.page_num` | `—（直接 JSON 路径）` | 分页页码 | `String` | `8` | `N` | 已确认 | 从1开始。不传则默认1。last_end_log_id与page_num不能同时为空示例值：20 |
| `request.data.acct_id` | `request.data.acct_id` | `—（直接 JSON 路径）` | 账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，不填默认为基本户；示例值：F00598600 |
| `request.data.last_end_log_id` | `request.data.last_end_log_id` | `—（直接 JSON 路径）` | 流水号ID | `String` | `64` | `N` | 已确认 | 流水号ID；当传了last_end_log_id ,acct_id参数必填,page_num无须传第一次翻页填0即可示例值：[官网示例已脱敏] |
| `request.data.acct_type` | `request.data.acct_type` | `—（直接 JSON 路径）` | 账户类型 | `String` | `2` | `N` | 已确认 | 账户类型 01:基本户 02:现金户 03:延时户 05:充值户 09:营销户；不填默认01 |
| `request.data.hf_seq_id` | `request.data.hf_seq_id` | `—（直接 JSON 路径）` | 汇付全局流水号 | `String` | `64` | `N` | 已确认 | 该参数传入时，优先使用该参数查询数据，此时分页条件失效，账务日期条件失效，默认返回所有符合的数据；示例值：00470topo1A211015160805P090ac132fef00000 |

### 同步响应信封及 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 交易响应内容体 | `Object` | `—` | `N` | N/A：结构字段长度 | 业务返回参数，jsonObject格式 |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `256` | `Y` | 已确认 | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：处理成功 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 渠道/代理/商户/用户编号 | `String` | `32` | `Y` | 已确认 | 汇付分配的渠道商、代理商、商户、用户的编号，示例值：[官网示例已脱敏] |
| `response.data.mer_name` | `response.data.mer_name` | `—（直接 JSON 路径）` | 商户名称 | `String` | `128` | `N` | 已确认 | 示例值：上海汇付支付服务公司 |
| `response.data.mer_short_name` | `response.data.mer_short_name` | `—（直接 JSON 路径）` | 商户简称 | `String` | `64` | `N` | 已确认 | 示例值：汇付支付 |
| `response.data.acct_type` | `response.data.acct_type` | `—（直接 JSON 路径）` | 账户类型 | `String` | `19` | `N` | 已确认 | 01:基本户； 09:营销户；示例值：01 |
| `response.data.acct_id` | `response.data.acct_id` | `—（直接 JSON 路径）` | 账户号 | `String` | `9` | `N` | 已确认 | 商户账户的账户号；示例值：F00598600 |
| `response.data.page_size` | `response.data.page_size` | `—（直接 JSON 路径）` | 每页条数 | `String` | `8` | `N` | 已确认 | 示例值：20 |
| `response.data.page_num` | `response.data.page_num` | `—（直接 JSON 路径）` | 分页页码 | `String` | `8` | `N` | 已确认 | 示例值：12 |
| `response.data.result_count` | `response.data.result_count` | `—（直接 JSON 路径）` | 结果总条数 | `String` | `8` | `N` | 已确认 | 示例值：120 |
| `response.data.acct_log_list[]` | `response.data.acct_log_list` | `—（String(JSON Array) 容器）` | 账务流水列表 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray |
| `response.data.acct_log_list[].acct_log_id` | `response.data.acct_log_list` | `$[].acct_log_id` | 账务流水号 | `String` | `32` | `Y` | 已确认 | 示例值：7001709383 |
| `response.data.acct_log_list[].acct_date` | `response.data.acct_log_list` | `$[].acct_date` | 账务日期 | `String` | `8` | `Y` | 已确认 | 示例值：20220628 |
| `response.data.acct_log_list[].trans_date_time` | `response.data.acct_log_list` | `$[].trans_date_time` | 账务时间 | `String` | `32` | `Y` | 已确认 | 示例值：20230804125959 |
| `response.data.acct_log_list[].acct_trans_type` | `response.data.acct_log_list` | `$[].acct_trans_type` | 账务类型 | `String` | `32` | `Y` | 已确认 | 账务类型见下文描述；示例值：支付收款 |
| `response.data.acct_log_list[].acct_trans_type_code` | `response.data.acct_log_list` | `$[].acct_trans_type_code` | 账务类型编码 | `String` | `4` | `Y` | 已确认 | 示例值：1001 |
| `response.data.acct_log_list[].acct_product_req_seq_id` | `response.data.acct_log_list` | `$[].acct_product_req_seq_id` | 账务侧产品流水号 | `String` | `64` | `Y` | 已确认 | 示例值：[官网示例已脱敏]top_Ait648656107TM01 |
| `response.data.acct_log_list[].debit_type` | `response.data.acct_log_list` | `$[].debit_type` | 借贷记标识 | `String` | `1` | `Y` | 已确认 | D-借记 C-贷记；示例值：D |
| `response.data.acct_log_list[].trans_amt` | `response.data.acct_log_list` | `$[].trans_amt` | 交易金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.acct_log_list[].fee_amt` | `response.data.acct_log_list` | `$[].fee_amt` | 手续费金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.acct_log_list[].balance_amt` | `response.data.acct_log_list` | `$[].balance_amt` | 交易后余额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.acct_log_list[].hf_seq_id` | `response.data.acct_log_list` | `$[].hf_seq_id` | 全局流水号 | `String` | `128` | `Y` | 已确认 | 引起这笔账户资金变动的交易全局流水号；示例值：0035000topA220628152651P306c0a8217a00000 |
| `response.data.acct_log_list[].control_ord_flag` | `response.data.acct_log_list` | `$[].control_ord_flag` | 管控订单标识 | `String` | `2` | `N` | 已确认 | Y:管控订单，N:非管控订单；示例值：N |
| `response.data.acct_log_list[].log_id` | `response.data.acct_log_list` | `$[].log_id` | 流水号ID | `String` | `64` | `N` | 已确认 | 流水号ID；示例值：[官网示例已脱敏] |
| `response.data.acct_log_list[].mer_acct_seq_id` | `response.data.acct_log_list` | `$[].mer_acct_seq_id` | 商户账务流水编号 | `String` | `64` | `Y` | 已确认 | 商户账务流水编号示例值：[官网示例已脱敏] |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/partners/guide/#/api_v2jqyq) |


## 账务流水汇总结果查询

- 官方来源：<https://paas.huifu.com/partners/api/doc/zhy/api_acct_log_summary.md>
- SHA-256：`d70d62be96cb1c20ba9be2355a57c8890468e8eab20e8adf2a81933e684e771a`

### 请求信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：HUIFENQI |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一商户号当天唯一，示例值：[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 日期格式：yyyyMMdd，以北京时间为准 |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 渠道/代理/商户/用户编号 | `String` | `32` | `Y` | 已确认 | 汇付分配的渠道商、代理商、商户、用户的编号，示例值：[官网示例已脱敏] |
| `request.data.acct_id` | `request.data.acct_id` | `—（直接 JSON 路径）` | 账户号 | `String` | `16` | `Y` | 已确认 | 账户号 |
| `request.data.start_trade_time` | `request.data.start_trade_time` | `—（直接 JSON 路径）` | 开始交易时间 | `String` | `19` | `Y` | 已确认 | 开始交易时间 示例值：2026-09-01 00:00:00 |
| `request.data.end_trade_time` | `request.data.end_trade_time` | `—（直接 JSON 路径）` | 截止交易时间 | `String` | `19` | `Y` | 已确认 | 截止交易时间 目前仅支持跨7天范围查询 示例值：2026-09-07 23:59:59 |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 异步通知地址 | `String` | `256` | `Y` | 已确认 | 异步通知地址示例值：https://www.baidu.com/ |

### 同步响应信封及 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 交易响应内容体 | `Object` | `—` | `N` | N/A：结构字段长度 | 业务返回参数，jsonObject格式 |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `256` | `Y` | 已确认 | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：处理成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 查询时传入，原样返回；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 查询时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 渠道/代理/商户/用户编号 | `String` | `32` | `Y` | 已确认 | 汇付分配的渠道商、代理商、商户、用户的编号，示例值：[官网示例已脱敏] |
| `response.data.acct_id` | `response.data.acct_id` | `—（直接 JSON 路径）` | 账户号 | `String` | `16` | `Y` | 已确认 | 商户账户的账户号；示例值：F00598600 |
| `response.data.total_count` | `response.data.total_count` | `—（直接 JSON 路径）` | 结果总条数 | `String` | `8` | `N` | 已确认 | 示例值：100 |
| `response.data.total_summary_amt` | `response.data.total_summary_amt` | `—（直接 JSON 路径）` | 汇总总金额 | `String` | `8` | `N` | 已确认 | 示例值：120 |
| `response.data.summary_list[]` | `response.data.summary_list` | `—（String(JSON Array) 容器）` | 账务流水汇总列表 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray |
| `response.data.summary_list[].acct_trans_type` | `response.data.summary_list` | `$[].acct_trans_type` | 账务类型 | `String` | `32` | `Y` | 已确认 | 账务类型；示例值：1001/font> |
| `response.data.summary_list[].acct_trans_type_desc` | `response.data.summary_list` | `$[].acct_trans_type_desc` | 账务类型 | `String` | `32` | `Y` | 已确认 | 账务类型见下文描述；示例值：支付收款 |
| `response.data.summary_list[].summary_amt` | `response.data.summary_list` | `$[].summary_amt` | 交易汇总金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.summary_list[].count` | `response.data.summary_list` | `$[].count` | 该账务类型的交易总条数 | `String` | `14` | `Y` | 已确认 | 该账务类型的交易总条数 |
