# 用户进件五接口完整字段目录

本文件由仓库维护脚本从五份锁定的官方原文机械生成，负责保证字段路径不遗漏。条件必填、官方口径冲突、路由和安全边界仍需同时读取对应的原子接口 reference。

安全说明：官网说明中的用户号、证件号、手机号、邮箱、长流水和示例图片地址已机械脱敏；字段枚举、条件、材料编号和资料链接保持原文。

## 目录

- 使用规则
- 生成覆盖摘要
- 企业用户开户
- 个人用户开户
- 用户业务入驻
- 用户申请单状态查询
- 用户信息查询

## 使用规则

1. 必须以完整路径区分同名字段，不得按叶字段名合并。
2. `huifu_id` 必须结合接口与路径解释为用户号、渠道号或商户号，不得统一称为商户号。
3. String(JSON) 的对象/数组边界以完整路径保留；不得扁平化后复用商户进件 DTO。
4. 官网类型、长度、必填和示例互相冲突时，目录保留表格原值并标记为官方证据，不自行修正。
5. 异步通知仅来自用户业务入驻；本目录不补写官网未定义的 ACK、重试、去重或超时规则。

## 生成覆盖摘要

| 接口 | 字段路径总数 | 扩展表数量 | 最大路径深度 |
| --- | ---: | ---: | ---: |
| 企业用户开户 | 43 | 1 | 4 |
| 个人用户开户 | 34 | 1 | 4 |
| 用户业务入驻 | 118 | 12 | 5 |
| 用户申请单状态查询 | 15 | 0 | 3 |
| 用户信息查询 | 144 | 12 | 5 |

## 企业用户开户

- 原始地址：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxzc.md>
- SHA-256：`c224c78370903d00b06dd85abc45700f0e63154b4a4e397849641bf6ae01153f`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 格式yyyyMMdd；示例值：20220905 |
| `request.data.reg_name` | 企业用户名称 | `String` | `128` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.short_name` | 经营简称 | `String` | `20` | `N` | 20位英文字符或10个汉字；示例值：[官网敏感示例已脱敏] |
| `request.data.license_code` | 营业执照编号 | `String` | `18` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.license_validity_type` | 证照有效期类型 | `String` | `1` | `Y` | 1:长期有效 0:非长期有效；示例值：0 |
| `request.data.license_begin_date` | 证照有效期起始日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd；示例值：20220905 |
| `request.data.license_end_date` | 证照有效期结束日期 | `String` | `8` | `C` | 日期格式：yyyyMMdd; 非长期有效时必填；示例值：20320905 |
| `request.data.reg_prov_id` | 注册地址(省) | `String` | `6` | `Y` | 示例值：310000，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| `request.data.reg_area_id` | 注册地址(市) | `String` | `8` | `Y` | 示例值：310100，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| `request.data.reg_district_id` | 注册地址(区) | `String` | `12` | `Y` | 示例值：310101，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| `request.data.reg_detail` | 注册地址(详细信息) | `String` | `256` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.legal_name` | 法人姓名 | `String` | `32` | `Y` | 32位英文字符或16个汉字；示例值：[官网敏感示例已脱敏]；官网页内注意：系统会做法人姓名与身份证号的实名认证，请正确填写 |
| `request.data.legal_cert_type` | 法人证件类型 | `String` | `2` | `Y` | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。示例值：00 |
| `request.data.legal_cert_no` | 法人证件号码 | `String` | `20` | `Y` | 示例值：[官网敏感示例已脱敏]；官网页内注意：系统会做法人姓名与身份证号的实名认证，请正确填写 |
| `request.data.legal_cert_validity_type` | 法人证件有效期类型 | `String` | `1` | `Y` | 1:长期有效 0:非长期有效；示例值：0 |
| `request.data.legal_cert_begin_date` | 法人证件有效期开始日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd；示例值：20220905 |
| `request.data.legal_cert_end_date` | 法人证件有效期截止日期 | `String` | `8` | `C` | 日期格式：yyyyMMdd; 非长期有效时必填，长期有效为空；示例值：20320905 |
| `request.data.legal_cert_nationality` | 法人国籍 | `String` | `50` | `C` | 法人的证件类型为外国人居留证时，必填，参见《[国籍编码](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/area/%E5%9B%BD%E7%B1%8D.xlsx)》示例值：CHN |
| `request.data.contact_name` | 管理员姓名 | `String` | `32` | `Y` | 32位英文字符或16个汉字；示例值：[官网敏感示例已脱敏] |
| `request.data.contact_mobile` | 管理员手机号 | `String` | `11` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.contact_email` | 管理员电子邮箱 | `String` | `64` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.login_name` | 管理员账号 | `String` | `32` | `C` | 如需短信通知则必填；示例值：[官网敏感示例已脱敏] |
| `request.data.operator_id` | 操作员 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.sms_send_flag` | 是否发送短信标识 | `String` | `1` | `N` | 入驻成功后短信通知商户联系人，； Y：发送短信通知（联系人手机号）；如需短信通知则login_name必填；N：不发送短信通知；默认；示例值：Y |
| `request.data.expand_id` | 扩展方字段 | `String` | `18` | `N` | 如果该商户是第三方展业的可以填写拓展方的huifu_id；示例值：[官网示例已脱敏] |
| `request.data.file_list[]` | 文件列表 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.file_list[].file_type` | 文件类型 | `String` | `8` | `Y` | 请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；示例值：F01 |
| `request.data.file_list[].file_id` | 文件jfileID | `String` | `128` | `Y` | 示例值：[官网敏感示例已脱敏]；[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)返回的file_id字段 |
| `request.data.file_list[].file_name` | 文件名称 | `String` | `128` | `N` | 128位英文字符或64个汉字；示例值：[官网敏感示例已脱敏] |
| `request.data.ent_type` | 公司类型 | `String` | `1` | `N` | 1:政府机构 2:国营企业 3:私营企业 4:外资企业 5:个体工商户 6:其它组织 7:事业单位 8:集体经济；示例值：2 |
| `request.data.mcc` | 所属行业 | `String` | `7` | `N` | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；示例值：5311；当用户业务入驻修改，电子回单配置开关为开通时，需填写 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.huifu_id` | 汇付ID | `String` | `18` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.login_name` | 管理员账号 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.login_password` | 管理员密码 | `String` | `18` | `N` | 传login_name的时候返回初始密码；示例值：[官网敏感示例已脱敏] |

## 个人用户开户

- 原始地址：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxzc.md>
- SHA-256：`219b94e71c37764b6ce9261c4e345f26a9afeefef50541fc30937364c4608605`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 格式yyyyMMdd；示例值：20220905 |
| `request.data.name` | 个人姓名 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.cert_type` | 个人证件类型 | `String` | `2` | `Y` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；示例值：00 |
| `request.data.cert_no` | 个人证件号码 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.cert_validity_type` | 个人证件有效期类型 | `String` | `1` | `Y` | 1:长期有效 0:非长期有效；示例值：0 |
| `request.data.cert_begin_date` | 个人证件有效期开始日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd；示例值：20220909 |
| `request.data.cert_end_date` | 个人证件有效期截止日期 | `String` | `8` | `N` | 日期格式：yyyyMMdd; 示例值：20330909 ；长期有效时可不填，非长期有效必填 |
| `request.data.cert_nationality` | 个人国籍 | `String` | `50` | `C` | 个人证件类型为外国人居留证时，必填，参见《[国籍编码](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/area/%E5%9B%BD%E7%B1%8D.xlsx)》示例值：CHN |
| `request.data.mobile_no` | 手机号 | `String` | `11` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.email` | 电子邮箱 | `String` | `64` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.login_name` | 管理员账号 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.sms_send_flag` | 是否发送短信标识 | `String` | `1` | `N` | Y:发送短信通知，N：不发送短信通知。默认不发送短信通知。示例值：Y |
| `request.data.expand_id` | 拓展方字段 | `String` | `18` | `N` | 如果该商户是第三方展业的可以填写拓展方的huifu_id;示例值：[官网示例已脱敏] |
| `request.data.file_list[]` | 文件列表 | `String` | `—` | `N` | jsonArray格式；官网页内注意：证件类型是身份证的，会做姓名与身份证号的实名认证 |
| `request.data.file_list[].file_type` | 文件类型 | `String` | `8` | `Y` | 参见[文件类型](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；示例值：F85 |
| `request.data.file_list[].file_id` | 文件jfileID | `String` | `128` | `Y` | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；示例值：[官网敏感示例已脱敏] |
| `request.data.file_list[].file_name` | 文件名称 | `String` | `128` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.address` | 地址 | `String` | `256` | `C` | 开通中信E管家必填；开通电子回单必填 |
| `request.data.mcc` | 所属行业 | `String` | `7` | `N` | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；示例值：5311；当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| `request.data.prov_id` | 省 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 ；如修改省市区要级联修改；当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| `request.data.area_id` | 市 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 ；如修改省市区要级联修改；当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| `request.data.district_id` | 区 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310101 ；如修改省市区要级联修改；当用户业务入驻修改，电子回单配置开关为开通时，需填写 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.huifu_id` | 汇付ID | `String` | `18` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.login_name` | 管理员账号 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.login_password` | 管理员密码 | `String` | `18` | `N` | 传login_name的时候要返回初始密码；示例值：[官网敏感示例已脱敏] |

## 用户业务入驻

- 原始地址：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrz.md>
- SHA-256：`093ff1605bbf2eb9934e28a85b0458b06e75ad7124a432badee5dad6dacf8b20`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商或商户的huifu_id；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为总部商户时，此字段填写商户huifu_id |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `String` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.huifu_id` | 汇付ID | `String` | `18` | `Y` | 开户时返回的huifu_id；示例值：[官网示例已脱敏] |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 格式yyyyMMdd；示例值：20220905 |
| `request.data.upper_huifu_id` | 渠道商/商户汇付Id | `String` | `18` | `Y` | 汇付分配的渠道商或商户编号；示例值：[官网示例已脱敏] |
| `request.data.settle_config_list[]` | 结算信息配置列表 | `String` | `—` | `N` | jsonArray格式;不支持同时开通T1+D1 |
| `request.data.settle_config_list[].settle_cycle` | 结算周期 | `String` | `2` | `Y` | T1：下个工作日到账；D1：下个自然日到账；TS:笔笔结算；示例值：T1 |
| `request.data.settle_config_list[].min_amt` | 起结金额 | `String` | `14` | `N` | 超过该金额后才会结算，单位为元，精确到小数点后两位。；取值范围[0.01,99999999999.99]；示例值：100.00 |
| `request.data.settle_config_list[].remained_amt` | 留存金额 | `String` | `14` | `N` | 小于等于该金额不会结算，单位为元，精确到小数点后两位。；取值范围[0.01,99999999999.99]；示例值：100.00 |
| `request.data.settle_config_list[].settle_abstract` | 结算摘要 | `String` | `128` | `N` | 如果需要自定义结算打款备注，请使用此字段传入，默认为空；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；示例值：业务收款 |
| `request.data.settle_config_list[].out_settle_flag` | 手续费外扣标记 | `String` | `1` | `N` | 1：外扣；2：内扣(为空时默认值)；示例值：1 |
| `request.data.settle_config_list[].out_settle_huifuid` | 结算手续费外扣时的汇付ID | `String` | `18` | `C` | 外扣手续费承担方的汇付ID。外扣时必填；示例值：[官网示例已脱敏] |
| `request.data.settle_config_list[].out_settle_acct_type` | 结算手续费外扣时的账户类型 | `String` | `2` | `C` | 外扣手续费账户类型； 01：基本户（为空时默认值），02-现金户， 05：充值户；外扣时必填；示例值：01 |
| `request.data.settle_config_list[].settle_pattern` | 结算方式 | `String` | `2` | `N` | P0：批次结算（为空时默认值）， ~~P1：定时结算~~(建议选P0和P2)，P2:批次定时结算；示例值：P0 |
| `request.data.settle_config_list[].settle_batch_no` | 结算批次号 | `String` | `32` | `C` | settle_pattern为P0时必填；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| `request.data.settle_config_list[].is_priority_receipt` | 是否优先到账 | `String` | `1` | `C` | settle_pattern为P0时选填， Y：是 N：否（为空默认取值）；示例值：Y |
| `request.data.settle_config_list[].settle_time` | 自定义结算处理时间 | `String` | `6` | `C` | settle_pattern为P1/P2时必填，注意：00:00到00:30不能指定；格式：HHmmss；示例值：103000 |
| `request.data.settle_config_list[].fixed_ratio` | 节假日结算手续费率 | `String` | `6` | `C` | settle_cycle为D1时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；示例值：0.05 |
| `request.data.settle_config_list[].workday_fixed_ratio` | 工作日结算手续费率 | `String` | `6` | `N` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；示例值：0.05 |
| `request.data.settle_config_list[].workday_constant_amt` | 工作日结算手续费固定金额 | `String` | `15` | `N` | 单位元，需保留小数点后两位。不填默认为0.00；示例值：1.00 |
| `request.data.settle_config_list[].constant_amt` | 节假日结算手续费固定金额 | `String` | `15` | `C` | settle_cycle为D1时必填。单位元，需保留小数点后两位。不收费请填写0.00；settle_cycle结算周期为D1时，遇节假日按此费率结算；示例值：1.00 |
| `request.data.card_info` | 结算卡信息 | `String` | `—` | `N` | 配置取现或结算信息时必填，jsonObject格式 |
| `request.data.card_info.card_type` | 卡类型 | `String` | `1` | `Y` | 0：对公，1：对私法人，2：对私非法人，4：对公非同名；个人商户/用户不支持对公类型，对私非法人类型；示例值：0 |
| `request.data.card_info.card_name` | 卡户名 | `String` | `128` | `C` | 持卡人姓名；示例值：[官网敏感示例已脱敏]；当card_type=4时，需要在file_list中额外上传材料 |
| `request.data.card_info.card_no` | 卡号 | `String` | `32` | `Y` | 银行卡号；示例值：[官网敏感示例已脱敏] |
| `request.data.card_info.prov_id` | 银行所在省 | `String` | `6` | `Y` | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：100000 |
| `request.data.card_info.area_id` | 银行所在市 | `String` | `6` | `Y` | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：110000 |
| `request.data.card_info.branch_code` | 支行联行号 | `String` | `12` | `C` | 当card_type=0时必填，[点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：103124075619 |
| `request.data.card_info.cert_type` | 持卡人证件类型 | `String` | `2` | `C` | 对私必填；参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；示例值：00 |
| `request.data.card_info.cert_no` | 持卡人证件号码 | `String` | `32` | `C` | 对私必填； 如:证件类型为身份证, 则填写身份证号码；示例值：[官网敏感示例已脱敏] |
| `request.data.card_info.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `C` | 对私必填；1：长期有效；0：非长期有效；示例值：0 |
| `request.data.card_info.cert_begin_date` | 持卡人证件有效期（起始） | `String` | `8` | `C` | 对私必填；日期格式：yyyyMMdd，示例值：20110112 |
| `request.data.card_info.cert_end_date` | 持卡人证件有效期（截止） | `String` | `8` | `C` | 当cert_validity_type=0时必须填写；日期格式yyyyMMdd，示例值：20110112；当cert_validity_type=1可不填 |
| `request.data.card_info.mp` | 银行卡绑定手机号 | `String` | `11` | `N` | 11位数字，示例值：[官网示例已脱敏] |
| `request.data.card_info.is_settle_default` | 默认结算卡标志 | `String` | `1` | `N` | 是否为默认结算卡标志；Y:是 N:否(为空默认)；示例值：Y |
| `request.data.cash_config[]` | 取现配置列表 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.cash_config[].cash_type` | 业务类型 | `String` | `2` | `N` | T1:下一工作日到银行账户；D1：下一自然日到银行账户；D0：当日到银行账户；默认D0；DM：当日到账；到账资金不包括当天的交易资金；示例值：T1 |
| `request.data.cash_config[].fix_amt` | 提现手续费（固定/元） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；示例值：1.00；注：当cash_type=D1时为节假日取现手续费 |
| `request.data.cash_config[].fee_rate` | 提现手续费率（%） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；示例值：0.05；注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate；2、当cash_type=D1时为节假日取现手续费 |
| `request.data.cash_config[].weekday_fix_amt` | D1工作日取现手续费固定金额 | `String` | `6` | `C` | 单位元，需保留小数点后两位。不收费请填写0.00；示例值：1.00；D1取现配置时选填，其他取现配置无效；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| `request.data.cash_config[].weekday_fee_rate` | D1工作日取现手续费率 | `String` | `6` | `C` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；示例值：0.05；D1取现配置时选填，其他取现配置无效；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| `request.data.cash_config[].out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：1 |
| `request.data.cash_config[].out_fee_huifu_id` | 手续费承担方 | `String` | `18` | `N` | 手续费外扣时必需指定手续费承担方ID；示例值：[官网示例已脱敏] |
| `request.data.cash_config[].out_fee_acct_type` | 交易手续费外扣的账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户，05-充值户；不填默认01； 示例值：01 |
| `request.data.cash_config[].is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | Y：是 ，N：否。不填，默认值为否。仅在取现类型配置为D1 和 T1 时生效。示例值：Y |
| `request.data.file_list[]` | 文件列表 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.file_list[].file_type` | 文件类型 | `String` | `8` | `Y` | card_type为4时，需上传以下文件：营业执照(文件类型：F07)、开户许可证(文件类型：F08)、非同名结算证明材料(文件枚举：F516)；法人证件不同类型上传不同文件，00身份证：F02【法人】身份证人像面、F03【法人】身份证国徽面；04回乡证(港澳居民来往内地通行证)：F31【法人】港澳台居民来往内地通行证；13外国人居留证：F511【法人】外国人居留证；14台胞证(台湾居民来往大陆通行证)：F31【法人】港澳台居民来往内地通行证；15港澳台居民居住证：F512【法人】港澳台居住；请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx) ；示例值：F01 |
| `request.data.file_list[].file_id` | 文件jfileID | `String` | `128` | `Y` | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；示例值：[官网敏感示例已脱敏] |
| `request.data.file_list[].file_name` | 文件名称 | `String` | `128` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.delay_flag` | 延迟入账开关 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `request.data.elec_acct_config` | 斗拱e账户功能配置 | `String` | `—` | `N` | — |
| `request.data.elec_acct_config.switch_state` | 电子账户开关 | `String` | `1` | `Y` | 电子账户开通总开关：0:关闭 1:开通 |
| `request.data.elec_acct_config.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家 |
| `request.data.elec_acct_config.cash_fee_party` | 电子账户提现手续费承担方 | `String` | `1` | `Y` | 1:总部 2:其他 |
| `request.data.elec_acct_config.scene` | 场景 | `String` | `3` | `Y` | 与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| `request.data.elec_acct_config.role_type` | 角色类型(角色编号) | `String` | `6` | `Y` | 必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx);示例值：001001 |
| `request.data.elec_acct_config.elec_card_list[]` | 银行卡信息 | `Object` | `—` | `N` | jsonArray字符串，如果开通斗拱E账户但不提供绑卡信息将无法取现，后续绑卡请调用[电子账户绑卡接口](https://paas.huifu.com/open/doc/api/#/yuer/api_acct_dzzhbk) |
| `request.data.elec_acct_config.elec_card_list[].prov_id` | 银行所在省 | `String` | `6` | `Y` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 |
| `request.data.elec_acct_config.elec_card_list[].area_id` | 银行所在市 | `String` | `6` | `Y` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 |
| `request.data.elec_acct_config.elec_card_list[].bank_code` | 银行编码 | `String` | `8` | `Y` | [参考银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `request.data.elec_acct_config.elec_card_list[].branch_code` | 支行联行号 | `String` | `12` | `Y` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.elec_acct_config.elec_card_list[].branch_name` | 支行名称 | `String` | `64` | `Y` | 示例值：中国工商银行上海市中山北路支行 |
| `request.data.elec_acct_config.elec_card_list[].card_name` | 结算账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：[官网敏感示例已脱敏] |
| `request.data.elec_acct_config.elec_card_list[].card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.elec_acct_config.elec_card_list[].card_type` | 卡类型 | `String` | `1` | `Y` | 0:对公 1:对私法人；示例值：310100 |
| `request.data.elec_acct_config.elec_card_list[].mp` | 银行绑定手机号 | `String` | `11` | `N` | 个人用户为空时会取联系人手机号，如果非持卡人手机号银行会报错；示例值：[官网示例已脱敏] |
| `request.data.elec_acct_config.elec_card_list[].default_cash_flag` | 默认卡标识 | `String` | `1` | `N` | 0：非默认卡 1：默认卡(不填，默认为0)；示例值：1 |
| `request.data.elec_acct_config.elec_card_list[].auth_version` | 用户授权协议版本号 | `String` | `64` | `N` | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| `request.data.elec_acct_config.elec_card_list[].auth_no` | 用户授权协议号 | `String` | `64` | `N` | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
| `request.data.elec_acct_config.user_type` | 用户类型 | `String` | `18` | `N` | SPLIT-分账用户，默认；SETTLE-结算用户，**不支持分账、余额支付；** |
| `request.data.elec_acct_config.elec_acct_sign_seq_id` | 中信签约短信流水号 | `String` | `64` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.elec_acct_config.sign_success_flag` | 签约成功标志 | `String` | `1` | `Y` | Y：成功 |
| `request.data.async_return_url` | 异步请求地址 | `String` | `128` | `N` | 为空时不推送异步消息 格式：http://消息接收地址，示例值：http://service.example.com/to/path |
| `request.data.elec_receipt_config` | 电子回单配置 | `Object` | `—` | `N` | — |
| `request.data.elec_receipt_config.switch_state` | 电子回单开关 | `String` | `—` | `Y` | 0:关闭 1:开通 |
| `request.data.sign_user_info` | 签约人信息 | `Object` | `—` | `C` | 当电子回单配置开关为开通时必填 |
| `request.data.sign_user_info.type` | 签约人类型 | `String` | `—` | `Y` | LEGAL-法人 |
| `request.data.sign_user_info.mobile_no` | 签约人手机号 | `String` | `—` | `Y` | — |
| `request.data.sign_user_info.cert_no` | 签约人身份证 | `String` | `—` | `N` | 企业用户不填默认为法人证件号，个人用户不填默认为个人证件号；当前仅支持法人 |
| `request.data.sign_user_info.name` | 签约人姓名 | `String` | `—` | `N` | 企业用户不填默认为法人姓名，个人用户不填默认为个人姓名 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.huifu_id` | 汇付ID | `String` | `18` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.token_no` | 取现卡序列号 | `String` | `20` | `N` | 取现卡序列号，交易时使用；示例值：[官网敏感示例已脱敏] |
| `response.data.resp_business[]` | 业务配置结果状态列表 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.resp_business[].type` | 配置类型 | `String` | `1` | `Y` | 1、绑卡信息；2、取现配置；3、结算信息配置；5、灵工业务配置；示例值：1 |
| `response.data.resp_business[].code` | 配置状态 | `String` | `1` | `Y` | S:成功，F:失败；示例值：S |
| `response.data.resp_business[].msg` | 配置返回信息 | `String` | `512` | `N` | 业务响应信息；示例值： |
| `response.data.apply_no` | 申请单号 | `String` | `18` | `N` | 返回审核中时有值，业务申请单号；示例值：[官网示例已脱敏] |

### 异步通知信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.resp_code` | 网关返回码 | `String` | `6` | `Y` | 网关返回码 |
| `async.resp_desc` | 网关返回描述 | `String` | `512` | `Y` | 网关返回描述 |
| `async.sign` | 签名 | `String` | `—` | `Y` | 签名，对报文整体签名 |
| `async.data` | 业务返回参数 | `String` | `—` | `N` | JSON |

### 异步通知 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.data.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `async.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `async.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：rQ[官网示例已脱敏] |
| `async.data.req_date` | 请求时间 | `String` | `8` | `Y` | 原请求时间YYYYMMDD；示例值：20240123 |
| `async.data.huifu_id` | 汇付客户号 | `String` | `18` | `Y` | 固定18位 ,汇付分配的商户号；示例值：[官网示例已脱敏] |
| `async.data.notify_type` | 通知类型 | `String` | `1` | `Y` | A:审核消息，Z：电子账户；示例值：A |
| `async.data.audit_info` | 审核信息 | `String` | `—` | `N` | jsonObject; notify_type = A时返回; |
| `async.data.audit_info.audit_status` | 审核状态 | `String` | `1` | `Y` | Y:审核通过 P:审核中 N:审核拒绝；示例值：Y |
| `async.data.audit_info.audit_desc` | 审核意见 | `String` | `512` | `N` | 审核意见 |
| `async.data.audit_info.apply_no` | 申请单号 | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `async.data.audit_info.token_no` | 取现卡序列号 | `String` | `20` | `N` | 取现卡序列号，交易时使用 |
| `async.data.audit_info.resp_business[]` | 业务配置结果状态列表 | `Object` | `—` | `N` | jsonArray格式 |
| `async.data.audit_info.resp_business[].type` | 配置类型 | `String` | `1` | `Y` | 1、绑卡信息；2、取现配置；3、结算信息配置；5、灵工业务配置；示例值：1 |
| `async.data.audit_info.resp_business[].code` | 配置状态 | `String` | `1` | `Y` | S:成功，F:失败；示例值：S |
| `async.data.audit_info.resp_business[].msg` | 配置返回信息 | `String` | `512` | `N` | 业务响应信息；示例值： |
| `async.data.elec_acct_result` | 斗拱e账户开通结果 | `String` | `—` | `N` | jsonObject格式；notify_type=Z时返回 |
| `async.data.elec_acct_result.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家；示例值：01 |
| `async.data.elec_acct_result.bank_status` | 电子账户开通状态 | `String` | `1` | `Y` | S：成功 F：失败；示例值：S |
| `async.data.elec_acct_result.bank_message` | 银行信息 | `String` | `512` | `N` | 银行信息 |
| `async.data.elec_acct_result.sign_agreement_id` | 签约协议号 | `String` | `32` | `N` | 商户签约中信E管家协议编号； 签约成功才返回示例值：[官网示例已脱敏] |

## 用户申请单状态查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhsqdzt.md>
- SHA-256：`f7894c5e2bc3544a9501922d4e3d5bb8b1f054704a80c36405a51ef2ad768e56`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/customers/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属**用户ID**；示例值：[官网示例已脱敏] |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号（业务申请编号），同一商户号当天唯一，示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 格式yyyyMMdd；示例值：20220905 |
| `request.data.apply_no` | 申请单号 | `String` | `18` | `Y` | 汇付返回的申请单号；示例值：[官网示例已脱敏] |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.apply_reason` | 审核意见 | `String` | `512` | `N` | 审核意见 |
| `response.data.apply_status` | 申请单审核状态 | `String` | `1` | `N` | Y:审核通过 P:审核中 N审核拒绝 F:系统处理失败；示例值：Y |
| `response.data.huifu_id` | 用户号 | `String` | `18` | `N` | 汇付分配的用户号；示例值：[官网示例已脱敏] |

## 用户信息查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhywcx.md>
- SHA-256：`27b1627a928c1457766ce2e494f7d749a65666d1d0237af25cdf33fc7e28104d`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/customers/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属**用户ID**；示例值：[官网示例已脱敏] |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号（业务申请编号），同一商户号当天唯一，示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 格式yyyyMMdd；示例值：20220905 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `5` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.ent_base_info` | 企业用户基本信息 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.ent_base_info.reg_name` | 企业用户名称 | `String` | `128` | `Y` | 企业用户名称，当为汉字时以2个字符计算；示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.license_code` | 营业执照编号 | `String` | `20` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.license_validity_type` | 证照有效期类型 | `String` | `1` | `Y` | 1：长期有效；0：非长期有效；示例值：1 |
| `response.data.ent_base_info.license_begin_date` | 证照有效期起始日期 | `String` | `8` | `Y` | 有效期格式：yyyyMMdd；示例值：20220909 |
| `response.data.ent_base_info.license_end_date` | 证照有效期结束日期 | `String` | `8` | `N` | 有效期格式：yyyyMMdd；示例值：20420909 |
| `response.data.ent_base_info.reg_prov_id` | 注册地址(省) | `String` | `6` | `Y` | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310000 |
| `response.data.ent_base_info.reg_area_id` | 注册地址(市) | `String` | `6` | `Y` | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310100 |
| `response.data.ent_base_info.reg_district_id` | 注册地址(区) | `String` | `6` | `Y` | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310101 |
| `response.data.ent_base_info.reg_detail` | 注册地址(详细信息) | `String` | `256` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.legal_name` | 法人姓名 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.legal_cert_type` | 法人证件类型 | `String` | `2` | `Y` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明 ；示例值：00 |
| `response.data.ent_base_info.legal_cert_no` | 法人证件号码 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.legal_cert_validity_type` | 法人证件有效期类型 | `String` | `1` | `Y` | 1：长期有效； 0：非长期有效；示例值：0 |
| `response.data.ent_base_info.legal_cert_begin_date` | 法人证件有效期开始日期 | `String` | `8` | `Y` | 有效期格式：yyyyMMdd；示例值：20220909 |
| `response.data.ent_base_info.legal_cert_end_date` | 法人证件有效期截止日期 | `String` | `8` | `N` | 有效期格式：yyyyMMdd；示例值：20340909 |
| `response.data.ent_base_info.contact_name` | 管理员姓名 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.contact_mobile_no` | 管理员手机号 | `String` | `11` | `Y` | 11位数字；示例值：[官网示例已脱敏] |
| `response.data.ent_base_info.contact_email` | 管理员电子邮箱 | `String` | `64` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.login_name` | 管理员账号 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.file_list[]` | 附件资料列表 | `Object` | `—` | `N` | 格式jsonArray |
| `response.data.ent_base_info.file_list[].file_type` | 文件类型 | `String` | `8` | `Y` | 请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；示例值：F85 |
| `response.data.ent_base_info.file_list[].file_id` | 文件jfileID | `String` | `128` | `Y` | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.file_list[].file_name` | 文件名称 | `String` | `128` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.ent_base_info.mcc` | 所属行业 | `String` | `7` | `N` | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；示例值：5311 |
| `response.data.indv_base_info` | 个人用户基本信息 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.indv_base_info.name` | 个人姓名 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.indv_base_info.cert_type` | 个人证件类型 | `String` | `2` | `Y` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；示例值：00 |
| `response.data.indv_base_info.cert_no` | 个人证件号码 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.indv_base_info.cert_validity_type` | 个人证件有效期类型 | `String` | `1` | `Y` | 1：长期有效；0：非长期有效；示例值：0 |
| `response.data.indv_base_info.cert_begin_date` | 个人证件有效期开始日期 | `String` | `8` | `Y` | 有效期格式：yyyyMMdd；示例值：20220909 |
| `response.data.indv_base_info.cert_end_date` | 个人证件有效期截止日期 | `String` | `8` | `N` | 有效期格式：yyyyMMdd；示例值：20340909 |
| `response.data.indv_base_info.mobile_no` | 手机号 | `String` | `11` | `Y` | 11位数字，示例值：[官网敏感示例已脱敏] |
| `response.data.indv_base_info.email` | 电子邮箱 | `String` | `64` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.indv_base_info.login_name` | 管理员账号 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.indv_base_info.file_list[]` | 附件资料列表 | `Object` | `—` | `N` | 格式jsonArray |
| `response.data.indv_base_info.file_list[].file_type` | 文件类型 | `String` | `8` | `Y` | 请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；示例值：F85 |
| `response.data.indv_base_info.file_list[].file_id` | 文件jfileID | `String` | `128` | `Y` | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；示例值：[官网敏感示例已脱敏] |
| `response.data.indv_base_info.file_list[].file_name` | 文件名称 | `String` | `128` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.indv_base_info.mcc` | 所属行业 | `String` | `—` | `N` | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；示例值：5311 |
| `response.data.indv_base_info.prov_id` | 省 | `String` | `—` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310101 ；如修改省市区要级联修改 |
| `response.data.indv_base_info.area_id` | 市 | `String` | `—` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 ；如修改省市区要级联修改 |
| `response.data.indv_base_info.district_id` | 区 | `String` | `—` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 ；如修改省市区要级联修改 |
| `response.data.card_info` | 结算卡信息 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.card_info.card_type` | 卡类型 | `String` | `1` | `Y` | 0：对公，1：对私法人，2：对私非法人，4：对公非同名；示例值：1 |
| `response.data.card_info.card_name` | 银行卡户名 | `String` | `128` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.card_info.card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.card_info.prov_id` | 银行所在省 | `String` | `6` | `Y` | 地区编码参考下载 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310000 |
| `response.data.card_info.area_id` | 银行所在市 | `String` | `6` | `Y` | 地区编码参考下载 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310100 |
| `response.data.card_info.bank_code` | 银行号 | `String` | `8` | `N` | 请参考[点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `response.data.card_info.branch_code` | 联行号 | `String` | `12` | `N` | 请参考[点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `response.data.card_info.branch_name` | 支行名称 | `String` | `64` | `N` | 示例值：中国工商银行上海市中山北路支行 |
| `response.data.card_info.cert_type` | 持卡人证件类型 | `String` | `2` | `N` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；示例值：00 |
| `response.data.card_info.cert_no` | 持卡人证件号码 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.card_info.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | 1：长期有效； 0：非长期有效；示例值：1 |
| `response.data.card_info.cert_begin_date` | 持卡人证件有效期起始日期 | `String` | `8` | `N` | 有效期格式：yyyyMMdd；示例值：20140909 |
| `response.data.card_info.cert_end_date` | 持卡人证件有效期截止日期 | `String` | `8` | `N` | 有效期格式：yyyyMMdd；示例值：20440909 |
| `response.data.card_info.mp` | 银行卡绑定手机号 | `String` | `11` | `N` | 11位数字，示例值：[官网示例已脱敏] |
| `response.data.card_info.token_no` | 绑卡序列号 | `String` | `20` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.settle_config_list[]` | 结算信息配置列表 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.settle_config_list[].settle_status` | 结算状态 | `String` | `1` | `N` | 0：关闭 1：打开；示例值：1 |
| `response.data.settle_config_list[].settle_cycle` | 结算周期 | `String` | `2` | `Y` | T1：下个工作日到账；D1：下个自然日到账；TS:笔笔结算；示例值：T1 |
| `response.data.settle_config_list[].min_amt` | 起结金额 | `String` | `17` | `N` | 整数最多14位，小数最多两位；示例值：1000.00 |
| `response.data.settle_config_list[].remained_amt` | 留存金额 | `String` | `17` | `N` | 整数最多14位，小数最多两位；示例值：500.00 |
| `response.data.settle_config_list[].settle_abstract` | 结算摘要 | `String` | `128` | `N` | 默认为空，如果需要自定义结算打款备注，请使用此字段传入；示例值：业务收款 |
| `response.data.settle_config_list[].out_settle_flag` | 手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣；示例值：1 |
| `response.data.settle_config_list[].out_settle_huifuid` | 结算手续费外扣时的汇付ID | `String` | `16` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.settle_config_list[].out_settle_acct_type` | 结算手续费外扣时的账户类型 | `String` | `2` | `N` | 01:基本户；02:现金户；05:充值户；示例值：0 |
| `response.data.settle_config_list[].settle_batch_no` | 结算批次号 | `String` | `6` | `N` | 示例值：1100；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| `response.data.settle_config_list[].fixed_ratio` | 节假日结算手续费率 | `String` | `6` | `C` | settle_cycle为D1时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；示例值：0.05 |
| `response.data.settle_config_list[].constant_amt` | 节假日结算手续费固定金额 | `String` | `15` | `C` | settle_cycle为D1时必填。单位元，需保留小数点后两位。不收费请填写0.00；settle_cycle结算周期为D1时，遇节假日按此费率结算；示例值：1.00 |
| `response.data.settle_config_list[].workday_fixed_ratio` | 工作日结算手续费率 | `String` | `6` | `N` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；示例值：0.05 |
| `response.data.settle_config_list[].workday_constant_amt` | 工作日结算手续费固定金额 | `String` | `15` | `N` | 单位元，需保留小数点后两位。不填默认为0.00；示例值：1.00 |
| `response.data.qry_cash_config_list[]` | 取现配置列表 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.qry_cash_config_list[].cash_type` | 业务类型 | `String` | `2` | `N` | T1：下个工作日到账；D1：下个自然日到账；D0：自然日当日取现并到账；示例值：T1 |
| `response.data.qry_cash_config_list[].switch_state` | 开关状态 | `String` | `1` | `N` | 0：关闭； 1：开通；示例值：1 |
| `response.data.qry_cash_config_list[].fix_amt` | 提现手续费（固定/元） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；示例值：1.00；注：当cash_type=D1时为节假日取现手续费 |
| `response.data.qry_cash_config_list[].fee_rate` | 提现手续费率（%） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；示例值：0.05；注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate；2、当cash_type=D1时为节假日取现手续费 |
| `response.data.qry_cash_config_list[].weekday_fix_amt` | D1工作日取现手续费固定金额 | `String` | `6` | `C` | 单位元，需保留小数点后两位。不收费请填写0.00；示例值：1.00；cash_type=D1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| `response.data.qry_cash_config_list[].weekday_fee_rate` | D1工作日取现手续费率 | `String` | `6` | `C` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；示例值：0.05；cash_type=D1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| `response.data.qry_cash_config_list[].out_cash_flag` | 是否开通取现手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣；示例值：1 |
| `response.data.qry_cash_config_list[].out_cash_huifuid` | 手续费承担方 | `String` | `18` | `N` | 手续费外扣时必需指定手续费承担方ID；示例值：[官网示例已脱敏] |
| `response.data.qry_cash_config_list[].out_cash_acct_type` | 取现手续费外扣子账户类型 | `String` | `2` | `N` | 01:基本户；02:现金户；05:充值户；示例值：01 |
| `response.data.qry_cash_card_info_list[]` | 取现卡信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.qry_cash_card_info_list[].card_type` | 卡类型 | `String` | `1` | `N` | 0：对公； 1：对私；示例值：1 |
| `response.data.qry_cash_card_info_list[].card_name` | 银行卡户名 | `String` | `128` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.qry_cash_card_info_list[].card_no` | 银行卡号 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.qry_cash_card_info_list[].area_id` | 银行所在市 | `String` | `6` | `N` | [地区编码参考下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310000 |
| `response.data.qry_cash_card_info_list[].prov_id` | 银行所在省 | `String` | `6` | `N` | [地区编码参考下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310100 |
| `response.data.qry_cash_card_info_list[].bank_code` | 银行号 | `String` | `8` | `N` | [请参考点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `response.data.qry_cash_card_info_list[].bank_name` | 银行名称 | `String` | `32` | `N` | 示例值：中国工商银行 |
| `response.data.qry_cash_card_info_list[].branch_code` | 联行号 | `String` | `12` | `N` | 请参考点击查看；示例值：102290026507 |
| `response.data.qry_cash_card_info_list[].branch_name` | 支行名称 | `String` | `64` | `N` | 示例值：中国工商银行上海市中山北路支行 |
| `response.data.qry_cash_card_info_list[].cert_type` | 持卡人证件类型 | `String` | `2` | `N` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；示例值：00 |
| `response.data.qry_cash_card_info_list[].cert_no` | 持卡人证件号码 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.qry_cash_card_info_list[].cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | 1：长期有效； 0：非长期有效；示例值：1 |
| `response.data.qry_cash_card_info_list[].cert_begin_date` | 持卡人证件有效期起始日期 | `String` | `8` | `N` | 格式：yyyyMMdd；示例值：20140909 |
| `response.data.qry_cash_card_info_list[].cert_end_date` | 持卡人证件有效期截止日期 | `String` | `8` | `N` | 格式：yyyyMMdd；示例值：20340909 |
| `response.data.qry_cash_card_info_list[].mp` | 银行卡绑定手机号 | `String` | `11` | `N` | 11位数字，示例值：[官网示例已脱敏] |
| `response.data.qry_cash_card_info_list[].token_no` | 绑卡序列号 | `String` | `20` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.qry_cash_card_info_list[].status` | 银行卡绑定状态 | `String` | `1` | `N` | N:正常 C:关闭；示例值：N |
| `response.data.qry_cash_card_info_list[].is_settle_default` | 默认结算卡标志 | `String` | `1` | `N` | 是否为默认结算卡标志；Y:是 N:否；示例值：Y |
| `response.data.elec_acct_config` | 斗拱e账户功能配置 | `String` | `—` | `N` | 用于总部商户、下级商户配置斗拱E账户功能 |
| `response.data.elec_acct_config.switch_state` | 电子账户开关 | `String` | `1` | `Y` | 电子账户开通总开关：0:关闭 1:开通 |
| `response.data.elec_acct_config.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家 |
| `response.data.elec_acct_config.cash_fee_party` | 电子账户提现手续费承担方 | `String` | `1` | `Y` | 1:总部 2:其他 |
| `response.data.elec_acct_config.scene` | 场景 | `String` | `3` | `Y` | 与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| `response.data.elec_acct_config.role_type` | 角色类型(角色编号) | `String` | `6` | `Y` | 与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx);示例值：001001 |
| `response.data.elec_acct_config.elec_card_list[]` | 银行卡信息 | `Object` | `—` | `N` | jsonArray字符串 |
| `response.data.elec_acct_config.elec_card_list[].prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表；示例值：310000](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| `response.data.elec_acct_config.elec_card_list[].area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表；示例值：310100](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| `response.data.elec_acct_config.elec_card_list[].bank_code` | 银行编码 | `String` | `8` | `Y` | [参考银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `response.data.elec_acct_config.elec_card_list[].branch_code` | 支行联行号 | `String` | `12` | `Y` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `response.data.elec_acct_config.elec_card_list[].branch_name` | 支行名称 | `String` | `64` | `Y` | 示例值：中国工商银行上海市中山北路支行 |
| `response.data.elec_acct_config.elec_card_list[].card_name` | 结算账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：[官网敏感示例已脱敏] |
| `response.data.elec_acct_config.elec_card_list[].card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `response.data.elec_acct_config.elec_card_list[].card_type` | 卡类型 | `String` | `1` | `Y` | 0:对公 1:对私法人 |
| `response.data.elec_acct_config.elec_card_list[].mp` | 银行绑定手机号 | `String` | `11` | `C` | — |
| `response.data.elec_acct_config.elec_card_list[].default_cash_flag` | 默认卡标识 | `String` | `1` | `N` | 0：非默认卡 1：默认卡(不填，默认为0) |
| `response.data.elec_acct_config.elec_card_list[].auth_version` | 用户授权协议版本号 | `String` | `64` | `C` | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| `response.data.elec_acct_config.elec_card_list[].auth_no` | 用户授权协议号 | `String` | `64` | `C` | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
| `response.data.elec_acct_config.elec_card_list[].status` | 卡状态 | `String` | `1` | `Y` | 绑卡状态，:N-正常，C-关闭，D-注销；示例值：N |
| `response.data.elec_acct_config.elec_card_list[].bind_card_msg` | 绑卡返回描述 | `String` | `256` | `Y` | 示例值：成功 |
| `response.data.elec_acct_config.bank_status` | 电子账户开通状态 | `String` | `1` | `Y` | S：成功 F：失败；示例值：S |
| `response.data.elec_acct_config.bank_message` | 银行信息 | `String` | `512` | `N` | — |
| `response.data.elec_acct_config.merchant_id` | 银行会员编号 | `String` | `15` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.elec_receipt_config` | 电子回单配置 | `Object` | `—` | `N` | — |
| `response.data.elec_receipt_config.switch_state` | 电子回单开关 | `String` | `—` | `N` | 0:关闭 1:开通 |
| `response.data.sign_user_info` | 签约人信息 | `Object` | `—` | `N` | 开通电子回单必填 |
| `response.data.sign_user_info.type` | 签约人类型 | `String` | `—` | `Y` | LEGAL-法人 |
| `response.data.sign_user_info.name` | 签约人姓名 | `String` | `—` | `N` | — |
| `response.data.sign_user_info.mobile_no` | 签约人手机号 | `String` | `—` | `Y` | — |
| `response.data.sign_user_info.cert_no` | 签约人证件号 | `String` | `—` | `N` | — |
