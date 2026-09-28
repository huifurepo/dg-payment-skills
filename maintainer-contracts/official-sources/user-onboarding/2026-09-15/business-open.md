<style>
.request-method{
  padding: 4px 8px;
  margin-right: 8px;
  color: #fff;
  font-weight:700;
  font-size: 12px;
  border-radius:4px
}
.post-method {
  background-color: #fa8c16;
}
.get-method {
  background-color: #4caf50;
}
table th:first-of-type {
    width: 17%;
}
table th:nth-of-type(2) {
    width: 15%;
}
table th:nth-of-type(3) {
    width: 8%;
}
table th:nth-of-type(4) {
    width: 5%;
}
table th:nth-of-type(5) {
    width: 5%;
}
table th:nth-of-type(6) {
 width: 49%;
}
</style>
## 用户业务入驻

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/busi/open

*最近更新时间：2026.09.04*
### 应用场景
服务商或商户为旗下的企业/个人用户配置结算费率及结算卡等信息。

**适用对象**    
斗拱服务商或商户；

### 接口说明 
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| 参数       | 中文名   | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :-------------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商或商户的huifu_id； <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为总部商户时，此字段填写商户huifu_id |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>                                      |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |
* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json|          | N    | 业务返回参数                                                 |

- “必填”字段取值“Y“：必填；“N”：非必填；“C”代表条件必填； 

### **注意** 
- 必填类型“C”代表条件选填；

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 汇付ID | String | 18 | Y | 开户时返回的huifu_id；<font color="green">示例值：6666000123123123</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | <font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220905</font> |
| upper_huifu_id | 渠道商/商户汇付Id | String | 18 | Y | 汇付分配的渠道商或商户编号；<font color="green">示例值：6666000123123123</font> |
| <span class="extend 0236957d_6905_4f37_9c4e_ac19bb38ecc0">settle_config_list</span> | 结算信息配置列表 | String |  | N | jsonArray格式;不支持同时开通T1+D1 |
| <span class="extend c44cd0c6_fbdd_41a9_97df_89c09057bef4">card_info</span> | 结算卡信息 | String |  | N | 配置取现或结算信息时必填，jsonObject格式 |
| <span class="extend 28729fb0_9d84_4f7d_8c95_bf7371693180">cash_config</span> | 取现配置列表 | String |  | N | jsonArray格式 |
| <span class="extend be4285ea_e6f4_4003_94e9_912a935475f7">file_list</span> | 文件列表 | String |  | N | jsonArray格式 |
| delay_flag | 延迟入账开关 | String | 1 | N | N：否 Y：是；<font color="green">示例值：Y</font> |
| <span class="extend d7606524_43ce_4b3e_a41a_330febe03a1a">elec_acct_config</span> | 斗拱e账户功能配置 | String |  | N | jsonObject字符串；用于总部商户、下级商户配置斗拱E账户功能 |
| async_return_url | 异步请求地址 | String | 128 | N | 为空时不推送异步消息 格式：http://消息接收地址，<font color="green">示例值：http://service.example.com/to/path</font> |
| <span class="extend 917587dc_5682_4aaf_9b99_9a78b9d52ee6">elec_receipt_config</span> | 电子回单配置 | String |  | N | jsonObject字符串；银行电子回单配置功能 |
| <span class="extend b205498d_cef9_413b_b38d_275d34673d61">sign_user_info</span> | 签约人信息 | String |  | C | 当电子回单配置开关为开通时必填 |

<!-- extend:start -->
<!-- div:extend-table 0236957d_6905_4f37_9c4e_ac19bb38ecc0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_cycle | 结算周期 | String | 2 | Y | T1：下个工作日到账；D1：下个自然日到账；TS:笔笔结算；<font color="green">示例值：T1</font> |
| min_amt | 起结金额 | String | 14 | N | 超过该金额后才会结算，单位为元，精确到小数点后两位。<br/>取值范围[0.01,99999999999.99]；<font color="green">示例值：100.00</font> |
| remained_amt | 留存金额 | String | 14 | N | 小于等于该金额不会结算，单位为元，精确到小数点后两位。<br/>取值范围[0.01,99999999999.99]；<font color="green">示例值：100.00</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 如果需要自定义结算打款备注，请使用此字段传入，默认为空；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；<br/><font color="green">示例值：业务收款</font> |
| out_settle_flag | 手续费外扣标记 | String | 1 | N | 1：外扣；2：内扣(为空时默认值)；<font color="green">示例值：1</font> |
| out_settle_huifuid | 结算手续费外扣时的汇付ID | String | 18 | C | 外扣手续费承担方的汇付ID。外扣时必填；<font color="green">示例值：6666000123123123</font> |
| out_settle_acct_type | 结算手续费外扣时的账户类型 | String | 2 | C | 外扣手续费账户类型； 01：基本户（为空时默认值），02-现金户， 05：充值户；外扣时必填；<br/><font color="green">示例值：01</font> |
| settle_pattern | 结算方式 | String | 2 | N | P0：批次结算（为空时默认值）， ~~P1：定时结算~~(建议选P0和P2)，P2:批次定时结算；<font color="green">示例值：P0</font> |
| settle_batch_no | 结算批次号 | String | 32 | C | settle_pattern为P0时必填；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| is_priority_receipt | 是否优先到账 | String | 1 | C | settle_pattern为P0时选填， Y：是 N：否（为空默认取值）；<font color="green">示例值：Y</font> |
| settle_time | 自定义结算处理时间 | String | 6 | C | settle_pattern为P1/P2时必填，注意：00:00到00:30不能指定；格式：HHmmss；<font color="green">示例值：103000</font> |
| fixed_ratio | 节假日结算手续费率 | String | 6 | C | settle_cycle为D1时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<br>settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；<font color="green">示例值：0.05</font> |
| workday_fixed_ratio | 工作日结算手续费率 | String | 6 | N | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；<font color="green">示例值：0.05</font> |
| workday_constant_amt | 工作日结算手续费固定金额 | String | 15 | N | 单位元，需保留小数点后两位。不填默认为0.00；<font color="green">示例值：1.00</font> |
| constant_amt | 节假日结算手续费固定金额 | String | 15 | C | settle_cycle为D1时必填。单位元，需保留小数点后两位。不收费请填写0.00；<br>settle_cycle结算周期为D1时，遇节假日按此费率结算 ；<br/> <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c44cd0c6_fbdd_41a9_97df_89c09057bef4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 1 | Y | 0：对公，1：对私法人，2：对私非法人，4：对公非同名；个人商户/用户不支持对公类型，对私非法人类型<br/><font color="green">示例值：0</font> |
| card_name | 卡户名 | String | 128 | C | 持卡人姓名；<font color="green">示例值：张三</font><br/>当card_type=4时，需要在file_list中额外上传材料； |
| card_no | 卡号 | String | 32 | Y | 银行卡号；<font color="green">示例值：0206014170008888</font> |
| prov_id | 银行所在省 | String | 6 | Y | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：100000</font> |
| area_id | 银行所在市 | String | 6 | Y | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：110000</font> |
| branch_code | 支行联行号 | String | 12 | C | 当card_type=0时必填，[点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：103124075619</font> |
| cert_type | 持卡人证件类型 | String | 2 | C | 对私必填；参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；<font color="green">示例值：00</font> |
| cert_no | 持卡人证件号码 | String | 32 | C | 对私必填； 如:证件类型为身份证, 则填写身份证号码；<font color="green">示例值：320926198412032059</font> |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | C | 对私必填；1：长期有效；0：非长期有效；<font color="green">示例值：0</font> |
| cert_begin_date | 持卡人证件有效期（起始） | String | 8 | C | 对私必填；日期格式：yyyyMMdd，<font color="green">示例值：20110112</font> |
| cert_end_date | 持卡人证件有效期（截止） | String | 8 | C | 当cert_validity_type=0时必须填写；日期格式yyyyMMdd，<font color="green">示例值：20110112</font><br/>当cert_validity_type=1可不填 |
| mp | 银行卡绑定手机号 | String | 11 | N | 11位数字，<font color="green">示例值：18611111111</font> |
| is_settle_default | 默认结算卡标志 | String | 1 | N | 是否为默认结算卡标志；Y:是 N:否(为空默认)；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 28729fb0_9d84_4f7d_8c95_bf7371693180-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cash_type | 业务类型 | String | 2 | N | T1:下一工作日到银行账户；<br/>D1：下一自然日到银行账户；<br/>D0：当日到银行账户；默认D0；<br/>DM：当日到账；到账资金不包括当天的交易资金；<br/><font color="green">示例值：T1</font> |
| fix_amt | 提现手续费（固定/元） | String | 6 | C | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；<font color="green">示例值：1.00</font><br>注：当cash_type=D1时为节假日取现手续费 |
| fee_rate | 提现手续费率（%） | String | 6 | C | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate<br>2、当cash_type=D1时为节假日取现手续费 |
| weekday_fix_amt | D1工作日取现手续费固定金额 | String | 6 | C | 单位元，需保留小数点后两位。不收费请填写0.00；<font color="green">示例值：1.00</font><br>D1取现配置时选填，其他取现配置无效；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| weekday_fee_rate | D1工作日取现手续费率 | String | 6 | C | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>D1取现配置时选填，其他取现配置无效；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：1</font> |
| out_fee_huifu_id | 手续费承担方 | String | 18 | N | 手续费外扣时必需指定手续费承担方ID；<font color="green">示例值：6666000123123123</font> |
| out_fee_acct_type | 交易手续费外扣的账户类型 | String | 2 | N | 01-基本户，02-现金户，05-充值户；不填默认01； <font color="green">示例值：01</font> |
| is_priority_receipt | 是否优先到账 | String | 1 | N | Y：是 ，N：否。不填，默认值为否。仅在取现类型配置为D1 和 T1 时生效。<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table be4285ea_e6f4_4003_94e9_912a935475f7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 8 | Y | card_type为4时，需上传以下文件：营业执照(文件类型：F07)、开户许可证(文件类型：F08)、非同名结算证明材料(文件枚举：F516)；<br/>法人证件不同类型上传不同文件，00身份证：F02【法人】身份证人像面、F03【法人】身份证国徽面；<br/>04回乡证(港澳居民来往内地通行证)：F31【法人】港澳台居民来往内地通行证；<br/>13外国人居留证：F511【法人】外国人居留证；<br/>14台胞证(台湾居民来往大陆通行证)：F31【法人】港澳台居民来往内地通行证<br/>15港澳台居民居住证：F512【法人】港澳台居住；<br/>请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx) ；<font color="green">示例值：F01</font> |
| file_id | 文件jfileID | String | 128 | Y | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_name | 文件名称 | String | 128 | N | <font color="green">示例值：test42001.jpg</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d7606524_43ce_4b3e_a41a_330febe03a1a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子账户开关 | String | 1 | Y | 电子账户开通总开关：0:关闭 1:开通 |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家 |
| cash_fee_party | 电子账户提现手续费承担方 | String | 1 | Y | 1:总部 2:其他； |
| scene | 场景 | String | 3 | Y | 与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| role_type | 角色类型(角色编号) | String | 6 | Y | 必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx);示例值：001001 |
| <span class="extend 6b2839e4_d082_4658_8f33_51a80346f532">elec_card_list</span> | 银行卡信息 | String |  | N | jsonArray字符串，如果开通斗拱E账户但不提供绑卡信息将无法取现，后续绑卡请调用[电子账户绑卡接口](https://paas.huifu.com/open/doc/api/#/yuer/api_acct_dzzhbk) |
| user_type | 用户类型 | String | 18 | N | SPLIT-分账用户，默认；<br/>SETTLE-结算用户，**不支持分账、余额支付；** |
| elec_acct_sign_seq_id | 中信签约短信流水号 | String | 64 | N | <font color="green">示例值：EMSSBPG2504284593690058431260676</font> |
| sign_success_flag | 签约成功标志 | String | 1 | Y | Y：成功 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6b2839e4_d082_4658_8f33_51a80346f532-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | Y | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | Y | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font> |
| bank_code | 银行编码 | String | 8 | Y | [参考银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font> |
| branch_code | 支行联行号 | String | 12 | Y | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | Y | <font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| card_name | 结算账户名 | String | 128 | Y | 银行卡对应的户名；<font color="green">示例值：上海汇付支付有限公司</font> |
| card_no | 银行卡号 | String | 32 | Y | <font color="green">示例值：98140008801800008888</font> |
| card_type | 卡类型 | String | 1 | Y | 0:对公 1:对私法人；<font color="green">示例值：0</font> |
| mp | 银行绑定手机号 | String | 11 | N | 个人用户为空时会取联系人手机号，如果非持卡人手机号银行会报错；<font color="green">示例值：13911111111</font> |
| default_cash_flag | 默认卡标识 | String | 1 | N | 0：非默认卡 1：默认卡(不填，默认为0)；<font color="green">示例值：1</font> |
| auth_version | 用户授权协议版本号 | String | 64 | N | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| auth_no | 用户授权协议号 | String | 64 | N | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 917587dc_5682_4aaf_9b99_9a78b9d52ee6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子回单开关 | String | 1 | Y | 0:关闭 1:开通  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b205498d_cef9_413b_b38d_275d34673d61-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 签约人类型 | String | 6 | Y | LEGAL-法人 |
| mobile_no | 签约人手机号 | String | 11 | Y | 需为11位数字 ；示例值：18611111111 |
| cert_no | 签约人身份证 | String | 18 | N | 企业用户不填默认为法人证件号，个人用户不填默认为个人证件号；当前仅支持法人 |
| name | 签约人姓名 | String | 32 | N | 企业用户不填默认为法人姓名，个人用户不填默认为个人姓名 |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000003084836",
    "data": {
        "req_seq_id": "rQ2022101705562413620614285150",
        "req_date": "20221017",
        "huifu_id": "6666000105765113",
        "upper_huifu_id": "6666000003084836",
        "async_return_url": "",
        "card_info": "{\"card_type\":\"0\",\"card_name\":\"交通银行股份有限公司\",\"card_no\":\"6217001210064762121\",\"prov_id\":\"310000\",\"area_id\":\"310100\",\"branch_code\":\"103124075619\",\"branch_name\":\"中国农业银行股份有限公司唐山陶瓷市场分理处\",\"cert_type\":\"00\",\"cert_no\":\"110101197003077513\",\"cert_validity_type\":\"0\",\"cert_begin_date\":\"20210806\",\"cert_end_date\":\"20410806\",\"mp\":\"15556622368\"}",
        "settle_config_list": "[{\"settle_cycle\":\"D1\",\"min_amt\":\"0.01\",\"remained_amt\":\"10.00\",\"settle_abstract\":\"结算摘要\",\"out_settle_flag\":\"2\",\"out_settle_huifuid\":\"\",\"out_settle_acct_type\":\"\",\"fixed_ratio\":\"2.00\",\"settle_batch_no\":\"300\",\"settle_pattern\":\"\",\"is_priority_receipt\":\"\",\"settle_time\":\"\",\"constant_amt\":\"1.00\"}]",
        "cash_config": "[{\"cash_type\":\"D1\",\"fix_amt\":\"0.03\",\"fee_rate\":\"2.00\",\"out_fee_flag\":\"\",\"out_fee_huifu_id\":\"\",\"out_fee_acct_type\":\"\"}]",
        "elec_acct_config": "{\"elec_card_list\":[{\"branch_code\":\"103100000018\",\"default_cash_flag\":\"0\",\"bank_code\":\"01030000\",\"mp\":\"18611111111\",\"prov_id\":\"440000\",\"card_no\":\"44658001123435159\",\"branch_name\":\"中国农业银行股份有限公司总行营业部\",\"card_name\":\"XXXXX有限公司\",\"area_id\":\"441200\",\"card_type\":\"0\"}],\"role_type\":\"004001\",\"switch_state\":\"1\",\"cash_fee_party\":\"2\",\"acct_type\":\"01\",\"sign_success_flag\":\"Y\",\"scene\":\"004\"}",
        "file_list": "[{\"file_id\":\"71da066c-5d15-3658-a86d-4e85ee67808a\",\"file_name\":\"企业营业执照1.jpg\",\"file_type\":\"F02\"}]"
    },
    "sign": "dXANEKD6AJZFz8dktpxTDjTGqxrwq6wUoCRg32mB3Fiwu7Hz7cRcVHy5T/TYSQiEXWwxVGUcqv1eTgEboGs2eqnD/uPSwQCoLJX2WhB6TmGkLQxL8FSwUr5Kw6NcwzmD722HtMHqDusOhl+VlGhRCRHSOFjKFWh7 GwahDpmtV8cjPGKDiwPCUPu5HPvcGKabfr5czVljniw4vZA0cXjADgzr/k30+SE0Y4ZPLkRGhW3HTfCIirzF0MU8F+/ergJXPmuikeWSF1+GOr/s/mlRZS88fvkiT6CIJ91rOgNP7BsoIaJ1seM/n9HJymO8Wqe7vPih2ZakZCCu9O8rYvgNQg==",
    "product_id": "ZDTEST"
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| huifu_id | 汇付ID | String | 18 | N | <font color="green">示例值：6666000123123123</font> |
| token_no | 取现卡序列号 | String | 20 | N | 取现卡序列号，交易时使用；<font color="green">示例值：10000406827</font> |
| <span class="extend 8c2fa762_0c8e_4485_b202_4fa5c897a2a9">resp_business</span> | 业务配置结果状态列表 | String |  | N | jsonArray格式 |
| apply_no | 申请单号 | String | 18 | N | 返回审核中时有值，业务申请单号；<font color="green">示例值：2024022934731647</font> |

<!-- extend:start -->
<!-- div:extend-table 8c2fa762_0c8e_4485_b202_4fa5c897a2a9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 配置类型 | String | 1 | Y | 1、绑卡信息；2、取现配置；3、结算信息配置；5、灵工业务配置；<font color="green">示例值：1</font> |
| code | 配置状态 | String | 1 | Y | S:成功，F:失败；<font color="green">示例值：S</font> |
| msg | 配置返回信息 | String | 512 | N | 业务响应信息；<font color="green">示例值：</font> |
<!-- extend:end -->


#### 异步返回参数

**公共参数：**

| 参数        | 中文名    | 定义     | 长度  | 必填 | 说明         |
| :-------- | :----------- | :----- | :--- | :------- | :----------------------- |
| resp_code | 网关返回码  | String | 6   | Y  | 网关返回码      |
| resp_desc | 网关返回描述 | String | 512 | Y  | 网关返回描述     |
| sign      | 签名     | String |   512  | Y  | 签名，对报文整体签名 |
| data      | 业务返回参数 | String |     | N  | JSON       |


| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| req_seq_id | 请求流水号 | String | 32 | Y | 原请求流水号；<font color="green">示例值：rQ2022101705562413620614285150</font> |
| req_date | 请求时间 | String | 8 | Y | 原请求时间YYYYMMDD；<font color="green">示例值：20240123</font> |
| huifu_id | 汇付客户号 | String | 18 | Y | 固定18位 ,汇付分配的汇付客户号；<font color="green">示例值：6666000123123123</font> |
| notify_type | 通知类型 | String | 1 | Y | A:审核消息，Z：电子账户；<font color="green">示例值：A</font> |
| <span class="extend d363c275_9115_42e9_bf11_95cb8c34ec36">audit_info</span> | 审核信息 | String |  | N | jsonObject; notify_type = A时返回; |
| <span class="extend a8a67276_e514_4e72_9545_8c8ce26ba473">elec_acct_result</span> | 斗拱e账户开通结果 | String |  | N | jsonObject格式；notify_type=Z时返回 |

<!-- extend:start -->
<!-- div:extend-table d363c275_9115_42e9_bf11_95cb8c34ec36-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| audit_status | 审核状态 | String | 1 | Y | Y:审核通过 P:审核中 N:审核拒绝；<font color="green">示例值：Y</font> |
| audit_desc | 审核意见 | String | 512 | N | 审核意见 |
| apply_no | 申请单号 | String | 18 | Y | <font color="green">示例值：2024022934731647</font> |
| token_no | 取现卡序列号 | String | 20 | N | 取现卡序列号，交易时使用； |
| <span class="extend bc7fe7ff_d4a2_4c2b_835e_95d4ec1cca27">resp_business</span> | 业务配置结果状态列表 | String |  | N | jsonArray格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bc7fe7ff_d4a2_4c2b_835e_95d4ec1cca27-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 配置类型 | String | 1 | Y | 1、绑卡信息；2、取现配置；3、结算信息配置；5、灵工业务配置；<font color="green">示例值：1</font> |
| code | 配置状态 | String | 1 | Y | S:成功，F:失败；<font color="green">示例值：S</font> |
| msg | 配置返回信息 | String | 512 | N | 业务响应信息；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a8a67276_e514_4e72_9545_8c8ce26ba473-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家；<font color="green">示例值：01</font> |
| bank_status | 电子账户开通状态 | String | 1 | Y | S：成功 F：失败；<font color="green">示例值：S</font> |
| bank_message | 银行信息 | String | 512 | N | 银行信息 |
| sign_agreement_id | 签约协议号 | String | 32 | N | 商户签约中信E管家协议编号； 签约成功才返回<font color="green">示例值：20250428091343030914951566827191</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "huifu_id": "6666000105765113",
        "resp_code": "00000000",
        "resp_desc": "成功",
        "token_no": "10001127912"
    },
    "sign": "hl+Bv+zKXsZ+Dk3PSjUsLXMlEeoc25VBNFOcAnu5riQ0TPBEJ4KPKboQZk9hFi8DqMF05D2qowaEnla2DbKIiRpx0wOKJhoCiS1F+PiD0H08UZPhWsfjmQsgYG3O4IrTgKsLbL0YGBBHAL9Xujx7vGrxTvaCGO4aH8Hx+3+iIHZubMllXLYsQzeux31piOZY9FBEnb+OcWIFWdUnCwi3LHdioK/HeXgylz7loKp0dGUlXrpyfh4cwJ2g6/DDzxkSGmWA8rRDmk0QiMMre8lwLGZ8GzBrhL5wcxnhW/Nwtv77ognpOZAcRjJmTM/KWRHYHx5Xy6bj2YJhXhtFBaH6cA=="
}
```
