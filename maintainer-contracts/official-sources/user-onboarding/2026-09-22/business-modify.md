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
## 用户业务入驻修改

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/busi/modify

*最近更新时间：2026.09.22*
### 应用场景
服务商或商户为旗下的企业/个人用户修改结算费率及结算卡等信息。

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
| data | 响应内容体 | String |          | N    | 业务返回参数                                                 |

- “必填”字段取值“Y“：必填；“N”：非必填；“C”代表条件必填； 

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 业务申请编号，同一商户号当天唯一，<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd；<font color="green">示例值：20220905</font> |
| huifu_id | 汇付ID | String | 18 | Y | 开户时返回的huifu_id；<font color="green">示例值：6666000123123123</font> |
| <span class="extend 36a60802_1444_44b9_b9f6_3cb5e7b67d95">settle_config_list</span> | 结算信息配置列表 | String |  | N | jsonArray格式；<br/>用户的上级机构要先开通相应的结算周期，才能支持用户开通；<br/>配置结算信息前要提供结算卡信息，或结算卡信息之前已提交；<br/>不支持同时开通D1+T1 |
| <span class="extend 5ffcfef0_41c1_4dcd_b389_ea1cbf85e176">card_info</span> | 结算卡信息 | String |  | N | 配置取现或结算信息时必填，jsonObject格式 |
| <span class="extend bfa0dc49_337e_4d94_9bb0_534980e7b673">cash_config</span> | 取现配置列表 | String |  | N | jsonArray格式；**这里配置的功能首先要求上级商户已开通对应功能**； |
| <span class="extend 8503cca7_93fe_4e50_82be_d12554aa13f1">file_list</span> | 文件列表 | String |  | N | jsonArray格式 |
| delay_flag | 延迟入账开关 | String | 1 | N | 选项：N：否 Y：是；<font color="green">示例值：N</font> |
| async_return_url | 异步请求地址 | String | 128 | N | 为空时不推送异步消息；<br/><font color="green">示例值：http://service.example.com/to/path</font> |
| <span class="extend 264b400b_d57c_4f21_8ed6_8d61d1be47c9">elec_acct_config</span> | 斗拱e账户功能配置 | String |  | N | jsonObject字符串；用于总部商户、下级商户配置斗拱E账户功能 |
| <span class="extend ef018082_368d_49d4_b8bd_48c88f4dd07f">elec_receipt_config</span> | 电子回单配置 | String |  | N | jsonObject字符串；银行电子回单配置功能 |
| <span class="extend 2219cafb_4ae1_4e7f_9cd8_8722d1d7f059">sign_user_info</span> | 签约人信息 | String |  | C | 当电子回单配置开关为开通时必填;<br>当用户升级LV3，并且开通 取现、余额支付、账户充值或者延迟支付任一功能时必填 |
| account_level | 用户等级  | String | 6 | N | LV1/LV2/LV3，不填默认LV1 |
| <span class="extend 941ff203_efcc_4337_9262_dd58f6a3ec2f">balance_pay_config</span> | 余额支付配置 | String |  | N | jsonObject格式 账户升级LV3 才能开通 |
| <span class="extend be8af990_6165_43ca_bc64_6c5d733c434d">account_recharge_config</span> | 账户充值配置 | String |  | N | jsonObject格式 账户升级LV3 才能开通 |
| <span class="extend 67f9d8a0_a76f_4e61_a1f2_5def8d1ebc93">delay_pay_config</span> | 延迟交易配置 | String |  | N | jsonObject格式 账户升级LV3 才能开通 |

<!-- extend:start -->
<!-- div:extend-table 36a60802_1444_44b9_b9f6_3cb5e7b67d95-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_status | 开通状态 | String | 1 | Y | 0：关闭 1：开通；<font color="green">示例值：1</font> |
| settle_cycle | 结算周期 | String | 2 | Y | T1：下个工作日到账；D1：下个自然日到账；TS:笔笔结算；<font color="green">示例值：D1</font> |
| min_amt | 起结金额 | String | 17 | N | 整数位不超过14位，小数最多2位；<font color="green">示例值：1000.00</font> |
| out_settle_acct_type | 结算手续费外扣时的账户类型 | String | 2 | N | 01：基本户，02-现金户， 05：充值户，不填默认01；<font color="green">示例值：01</font> |
| out_settle_flag | 手续费外扣标记 | String | 1 | N | 1：外扣； 2：内扣，默认；<font color="green">示例值：1</font> |
| out_settle_huifuid | 结算手续费外扣时的汇付ID | String | 18 | N | 手续费承担方的汇付ID<font color="green">示例值：6666000123120000</font> |
| remained_amt | 留存金额 | String | 17 | N | 整数最多14位，小数最多2位；<font color="green">示例值：500.00</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 默认为空，如果需要自定义结算打款备注，请使用此字段传入；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；<font color="green">示例值：业务收款</font> |
| settle_batch_no | 结算批次号 | String | 32 | C | settle_pattern为P0时必填；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| settle_pattern | 结算方式 | String | 2 | N | P0：批次结算（为空时默认值），~~P1：定时结算~~(建议选P0和P2)，P2:批次定时结算；<font color="green">示例值：P0</font> |
| is_priority_receipt | 是否优先到账 | String | 1 | C | settle_pattern为P0时必填， Y：是 N：否（为空默认取值）；<font color="green">示例值：Y</font> |
| settle_time | 自定义结算处理时间 | String | 6 | C | settle_pattern为P1/P2时必填，注意：00:00到00:30不能指定；格式：HHmmss；<font color="green">示例值：103000</font> |
| fixed_ratio | 节假日结算手续费率 | String | 6 | C | settle_cycle为D1时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<br>settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；<font color="green">示例值：0.05</font> |
| workday_fixed_ratio | 工作日结算手续费率 | String | 6 | N | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；<font color="green">示例值：0.05</font> |
| workday_constant_amt | 工作日结算手续费固定金额 | String | 15 | N | 单位元，需保留小数点后两位。不填默认为0.00；<font color="green">示例值：1.00</font> |
| constant_amt | 节假日结算手续费固定金额 | String | 15 | C | settle_cycle为D1时必填。单位元，需保留小数点后两位。不收费请填写0.00；<br>settle_cycle结算周期为D1时，遇节假日按此费率结算 ；<br/> <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5ffcfef0_41c1_4dcd_b389_ea1cbf85e176-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 1 | Y | 0：对公，1：对私法人，2：对私非法人，4：对公非同名；个人商户/用户不支持对公类型，对私非法人类型<br/><font color="green">示例值：0</font> |
| card_name | 卡户名 | String | 128 | Y | 持卡人姓名；<font color="green">示例值：张三</font><br/>当card_type=4时，需要在file_list中额外上传材料； |
| card_no | 卡号 | String | 32 | Y | 银行卡号；**不支持贷记卡绑定**；<font color="green">示例值：6228480031509448317</font> |
| prov_id | 银行所在省 | String | 6 | Y | 参见 [地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | Y | 参见 [地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font> |
| branch_code | 支行联行号 | String | 12 | C | 当card_type=0时必填，[点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| cert_type | 持卡人证件类型 | String | 2 | N | 参见[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)说明；<font color="green">示例值：00</font> |
| cert_no | 持卡人证件号码 | String | 32 | N | 对私必填， 如:证件类型为身份证, 则填写身份证号码<br/><font color="green">示例值：320926198412026034</font> |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | N | 对私必填 1：长期有效， 0：非长期有效；<font color="green">示例值：1</font> |
| cert_begin_date | 持卡人证件有效期起始日期 | String | 8 | N | 对私必填，日期格式：yyyyMMdd，<font color="green">示例值：20110112</font> |
| cert_end_date | 持卡人证件有效期截止日期 | String | 8 | N | 当cert_validity_type=0时必须填写，当cert_validity_type=1可不填，<br/> 日期格式yyyyMMdd，<font color="green">示例值：20310112</font> |
| mp | 银行卡绑定手机号 | String | 11 | N | 11位数字，<font color="green">示例值：18611111111</font> |
| is_settle_default | 默认结算卡标志 | String | 1 | N | 是否为默认结算卡标志；Y:是 N:否；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bfa0dc49_337e_4d94_9bb0_534980e7b673-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 开通状态 | String | 1 | Y | 0:关闭 1:开通；<font color="green">示例值：1</font> |
| cash_type | 业务类型 | String | 2 | N | T1/D1/D0/DM；默认D0；<font color="green">示例值：T1</font> |
| fix_amt | 提现手续费（固定/元） | String | 6 | C | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；<font color="green">示例值：1.00</font><br>注：当cash_type=D1时为节假日取现手续费 |
| fee_rate | 提现手续费率（%） | String | 6 | C | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate<br>2、当cash_type=D1时为节假日取现手续费 |
| weekday_fix_amt | D1工作日取现手续费固定金额 | String | 6 | C | 单位元，需保留小数点后两位。不收费请填写0.00；<font color="green">示例值：1.00</font><br>cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| weekday_fee_rate | D1工作日取现手续费率 | String | 6 | C | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：1</font> |
| out_fee_huifu_id | 手续费承担方 | String | 18 | N | 手续费外扣时必需指定手续费承担方ID ；<font color="green">示例值：6666000123120000</font> |
| out_fee_acct_type | 交易手续费外扣的账户类型 | String | 2 | N | 01-基本户，02-现金户，05-充值户；不填默认01 ；<font color="green">示例值：01</font> |
| is_priority_receipt | 是否优先到账 | String | 1 | N | Y：是 ，N：否。不填，默认值为否。仅在取现类型配置为D1 和 T1 时生效。<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8503cca7_93fe_4e50_82be_d12554aa13f1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 8 | Y | card_type为4时，需上传以下文件：营业执照(文件类型：F07)、开户许可证(文件类型：F08)、非同名结算证明材料(文件枚举：F516)；<br/>法人证件不同类型上传不同文件，00身份证：F02【法人】身份证人像面、F03【法人】身份证国徽面；<br/>04回乡证(港澳居民来往内地通行证)：F31【法人】港澳台居民来往内地通行证；<br/>13外国人居留证：F511【法人】外国人居留证；<br/>14台胞证(台湾居民来往大陆通行证)：F31【法人】港澳台居民来往内地通行证<br/>15港澳台居民居住证：F512【法人】港澳台居住；<br/>请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx) ；<font color="green">示例值：F01</font><br><br>用户账户等级为LV2时，需上传以下文件并进入审核；<br>企业用户：营业执照(文件类型：F07)、<br>对公结算：开户许可证(文件类型：F08)、<br>法人证件不同类型上传不同文件，<br>00身份证：F02【法人】身份证人像面、F03【法人】身份证国徽面；<br>04回乡证(港澳居民来往内地通行证)：F31【法人】港澳台居民来往内地通行证；<br>13外国人居留证：F511【法人】外国人居留证；<br>14台胞证(台湾居民来往大陆通行证)：F31【法人】港澳台居民来往内地通行证 <br>15港澳台居民居住证：F512【法人】港澳台居住；<br>个人用户：法人证件不同类型上传不同文件，<br>00身份证：F02【法人】身份证人像面、F03【法人】身份证国徽面；<br>04回乡证(港澳居民来往内地通行证)：F31【法人】港澳台居民来往内地通行证；<br>13外国人居留证：F511【法人】外国人居留证；<br>14台胞证(台湾居民来往大陆通行证)：F31【法人】港澳台居民来往内地通行证<br>15港澳台居民居住证：F512【法人】港澳台居住；<br><br>用户账户等级为LV3时，<br>需上传以下文件并进入审核；<br>企业用户：营业执照(文件类型：F07)、<br>对公结算：开户许可证(文件类型：F08)、<br>对私法人结算：银行卡卡号面(文件类型：F13)；<br>法人证件不同类型上传不同文件，<br>00身份证：F02【法人】身份证人像面、F03【法人】身份证国徽面；<br>04回乡证(港澳居民来往内地通行证)：F31【法人】港澳台居民来往内地通行证；<br>13外国人居留证：F511【法人】外国人居留证；<br>14台胞证(台湾居民来往大陆通行证)：F31【法人】港澳台居民来往内地通行证<br>15港澳台居民居住证：F512【法人】港澳台居住；<br>门头照 F22（店铺门头照图片）、收银台/前台照 F105（店铺收银台）、办公场地照 F371（办公环境照）<br>个人用户：不支持 |
| file_id | 文件jfileID | String | 128 | Y | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_name | 文件名称 | String | 128 | N | <font color="green">示例值：test42001.jpg</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 264b400b_d57c_4f21_8ed6_8d61d1be47c9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子账户开关 | String | 1 | Y | 电子账户开通总开关：0:关闭 1:开通 |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家 |
| cash_fee_party | 电子账户提现手续费承担方 | String | 1 | Y | 1:总部 2:其他； |
| scene | 场景 | String | 3 | Y | 与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| role_type | 角色类型(角色编号) | String | 6 | Y | 必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx);示例值：001001 |
| <span class="extend b1f910f2_2949_433e_86a8_40a751063705">elec_card_list</span> | 银行卡信息 | String |  | N | jsonArray字符串，如果开通斗拱E账户但不提供绑卡信息将无法取现，后续绑卡请调用电子账户绑卡接口 |
| bank_status | 电子账户开通状态 | String | 1 | Y | S：成功 F：失败；<font color="green">示例值：S</font> |
| bank_message | 银行信息 | String | 512 | N | 银行信息 |
| elec_acct_sign_seq_id | 中信签约短信流水号 | String | 64 | N | <font color="green">示例值：EMSSBPG2504284593690058431260676</font> |
| sign_success_flag | 签约成功标志 | String | 1 | N | Y：成功 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b1f910f2_2949_433e_86a8_40a751063705-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | Y | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | Y | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font> |
| bank_code | 银行编码 | String | 8 | Y | [参考银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font> |
| branch_code | 支行联行号 | String | 12 | Y | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | Y | <font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| card_name | 结算账户名 | String | 128 | Y | 银行卡对应的户名；<font color="green">示例值：上海汇付支付有限公司</font> <br/>当card_type=0时填写企业名称，企业非同名时，需要在file_list中额外上传材料；<br/>当card_type=1时填写法人姓名，卡户名与法人姓名必须一致；<br/>当card_type=2时填写非法人姓名； |
| card_no | 银行卡号 | String | 32 | Y | <font color="green">示例值：98140008801800008888</font> |
| card_type | 卡类型 | String | 1 | Y | 0:对公 1:对私法人；<font color="green">示例值：1</font> |
| mp | 银行绑定手机号 | String | 11 | N | 个人用户为空时会取联系人手机号，如果非持卡人手机号银行会报错；<font color="green">示例值：13911111111</font> |
| default_cash_flag | 默认卡标识 | String | 1 | N | 0：非默认卡 1：默认卡(不填，默认为0)；<font color="green">示例值：1</font> |
| auth_version | 用户授权协议版本号 | String | 64 | N | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| auth_no | 用户授权协议号 | String | 64 | N | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ef018082_368d_49d4_b8bd_48c88f4dd07f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子回单开关 | String | 1 | Y | 0:关闭 1:开通  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2219cafb_4ae1_4e7f_9cd8_8722d1d7f059-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 签约人类型 | String | 6 | Y | LEGAL-法人 |
| mobile_no | 签约人手机号 | String | 11 | Y | 签约人手机号 |
| cert_no | 签约人身份证 | String | 18 | N | 企业用户不填默认为法人证件号，个人用户不填默认为个人证件号；当前仅支持法人 |
| name | 签约人姓名 | String | 32 | N | 企业用户不填默认为法人姓名，个人用户不填默认为个人姓名 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 941ff203_efcc_4337_9262_dd58f6a3ec2f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费(%) | String | 9 | Y | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；<font color="green">示例值：0.50</font>代表费率为0.5% |
| fee_fix_amt |  手续费（固定/元） | String | 9 | Y | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；<font color="green">示例值：1.50 </font> <br> 注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额*fee_rate |
| out_fee_acct_type | 手续费外扣时的账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，<font color="green">示例值：01 </font> |
| out_fee_huifuid | 手续费外扣汇付ID | String | 18 | N | 开通余额支付手续费外扣业务时必填，<font color="green">示例值：6666000123123123</font> |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 是否交易手续费外扣 |
| charge_mode | 扣费模式 | String | 2 | N | 内扣时枚举值: 01: 默认规则, 02: 收款方分摊, 03: 交易时指定承担方 <br>外扣时枚举值: 10: 指定承担方, 11: 出款方承担, 12: 交易时指定承担方 <font color="green">示例值：11</font>；内扣时默认为01，外扣时默认为10； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table be8af990_6165_43ca_bc64_6c5d733c434d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费(%) | String | 9 | Y | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；<font color="green">示例值：0.50</font>代表费率为0.5% |
| fee_fix_amt |  手续费（固定/元） | String | 9 | Y | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；<font color="green">示例值：1.50 </font> <br> 注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额*fee_rate |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 67f9d8a0_a76f_4e61_a1f2_5def8d1ebc93-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 开通状态 | String | 1 | Y | 1 开通 0关闭 |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000104633228",
    "data": {
        "req_seq_id": "rQ202210170",
        "req_date": "20221017",
        "huifu_id": "6666000104896342",
        "async_return_url": "http://service.example.com/to/path",
        "card_info": "{\"card_type\":\"0\",\"card_name\":\"陈立一\",\"card_no\":\"6217001210064762000\",\"prov_id\":\"310000\",\"area_id\":\"310100\",\"bank_code\":\"01050000\",\"branch_code\":\"105305264815\",\"branch_name\":\"中国建设银行股份有限公司上海平凉路支行\",\"cert_type\":\"00\",\"cert_no\":\"110101197003077000\",\"cert_validity_type\":\"0\",\"cert_begin_date\":\"20210806\",\"cert_end_date\":\"20410806\",\"mp\":\"15556622000\"}",
        "settle_config_list": "[{\"settle_cycle\":\"D1\",\"settle_status\":\"1\",\"min_amt\":\"0.1\",\"remained_amt\":\"0.1\",\"settle_abstract\":\"吃吃\",\"out_settle_flag\":\"1\",\"out_settle_huifuid\":\"6666000104633228\",\"out_settle_acct_type\":\"05\",\"fixed_ratio\":\"0.1\",\"settle_batch_no\":\"0\",\"settle_pattern\":\"P0\",\"is_priority_receipt\":\"Y\",\"settle_time\":\"\"}]",
        "cash_config": "[{\"cash_type\":\"D0\",\"switch_state\":\"1\",\"fix_amt\":\"3\",\"fee_rate\":\"0.05\",\"out_fee_flag\":\"1\",\"out_fee_huifu_id\":\"6666000104633228\",\"out_fee_acct_type\":\"05\"}]",
        "file_list": "[{\"file_id\":\"99e00421-dad7-3334-9538-4f2ad10612d5\",\"file_name\":\"企业营业执照1.jpg\",\"file_type\":\"F02\"}]"
    },
    "sign": "Te7m80+K1RU2YEYelTsP3tKRnVvkeZ3rsL1I3HP5JrJdm6u0yiUNk8Zl3MKKedfNHtcQVnSGp2SM23euIGuOBAcOau/C8OjKar/rvbVxSK3/MlVtMew8Y8Zsf5g1XDxqKZNHwFo2JBFjKbdnDTBA1mUckyaB601DuT+uOprmpbgNKYTAM0/+eU9YsdImxsTRFYpd6HtOVTBMZ3wBKpqZ6+J4bs1Odmsc0qVNHYUN1n2sSPBdPqJchtsGYb838nv4eEoC9izIqfU54cPd5Ppy3vnI+XAGP7Ka7v+imOIdubPMXbE68OKI+FHnGUrbVinF0e/JV8xJo0gPiCttGK1X8A==",
    "product_id": "ZDTEST"
}

```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| huifu_id | 汇付ID | String | 18 | N | <font color="green">示例值：6666000123120000</font> |
| token_no | 取现卡序列号 | String | 20 | N | 取现卡序列号，交易时使用；<font color="green">示例值：10004053462</font> |
| <span class="extend fce92815_0903_4326_9864_048d892424c1">resp_business</span> | 业务配置结果状态列表 | Object |  | N | jsonArray格式 |
| apply_no | 申请单号 | String | 18 | N | 返回审核中时有值，业务申请单号；<font color="green">示例值：2024022934731647</font> |

<!-- extend:start -->
<!-- div:extend-table fce92815_0903_4326_9864_048d892424c1-table -->
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
| sign      | 签名     | String |  512   | Y  | 签名，对报文整体签名 |
| data      | 业务返回参数 | Json|     | N  |    |


| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| req_seq_id | 请求流水号 | String | 32 | Y | 原请求流水号；<font color="green">示例值：rQ2022101705562413620614285150</font> |
| req_date | 请求时间 | String | 8 | Y | 原请求时间YYYYMMDD；<font color="green">示例值：20240123</font> |
| huifu_id | 汇付客户号 | String | 18 | Y | 固定18位 ,汇付分配的汇付客户号；<font color="green">示例值：6666000123123123</font> |
| notify_type | 通知类型 | String | 1 | Y | A:审核消息，Z：电子账户；<font color="green">示例值：A</font> |
| <span class="extend 8f4235b7_ecb9_42bf_8e99_c89ebf05c253">audit_info</span> | 审核信息 | String |  | N | jsonObject; notify_type = A时返回; |
| <span class="extend f9fcc9de_3cf9_4886_9087_9db6614a6718">elec_acct_result</span> | 斗拱e账户开通结果 | String |  | N | jsonObject格式；notify_type=Z时返回 |
| <span class="extend 38a69a33_1549_4b78_ad8d_abc101fe23c7">account_info</span> | 升级信息 | Object |  | N | 用户升级信息 |

<!-- extend:start -->
<!-- div:extend-table 8f4235b7_ecb9_42bf_8e99_c89ebf05c253-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| audit_status | 审核状态 | String | 1 | Y | Y:审核通过 P:审核中 N:审核拒绝；<font color="green">示例值：Y</font> |
| audit_desc | 审核意见 | String | 512 | N | 审核意见 |
| apply_no | 申请单号 | String | 18 | Y | <font color="green">示例值：2024022934731647</font> |
| token_no | 取现卡序列号 | String | 20 | N | 取现卡序列号，交易时使用； |
| <span class="extend fdd36a3b_db42_4237_a33a_2660492790c4">resp_business</span> | 业务配置结果状态列表 | String |  | N | jsonArray格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fdd36a3b_db42_4237_a33a_2660492790c4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 配置类型 | String | 1 | Y | 1、绑卡信息；2、取现配置；3、结算信息配置；5、灵工业务配置；<font color="green">示例值：1</font> |
| code | 配置状态 | String | 1 | Y | S:成功，F:失败；<font color="green">示例值：S</font> |
| msg | 配置返回信息 | String | 512 | N | 业务响应信息；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f9fcc9de_3cf9_4886_9087_9db6614a6718-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家；<font color="green">示例值：01</font> |
| bank_status | 电子账户开通状态 | String | 1 | Y | S：成功 F：失败；<font color="green">示例值：S</font> |
| bank_message | 银行信息 | String | 512 | N | 银行信息 |
| sign_agreement_id | 签约协议号 | String | 32 | N | 商户签约中信E管家协议编号； 签约成功才返回<font color="green">示例值：20250428091343030914951566827191</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 38a69a33_1549_4b78_ad8d_abc101fe23c7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| account_level | 用户等级  | String | 6 | N | LV1/LV2/LV3，不填默认LV1 |
| trans_status | 验证状态 | String | 1 | N | 验证状态：打款打款验证：1-打款中，2-打款成功验证中，3-打款失败，4-验证通过，5-验证失败 ；<br>人脸验证： 1 验证中 4 验证通过 5 验证失败 |
| verify_ord_id | 打款验证流水号 | String | 32 | N | 对公卡时返回打款流水号，LV2、LV3用户升级绑定对公账户时返回，汇付在用户入驻时向用户对公账户打款，用户需通过打款验证接口上送打款流水号与打款金额完成验证； |
| face_url | 人脸活体验证 | String | 512 | N | 升级LV3，对私验证没有终态时返回 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "huifu_id": "6666000104896342",
        "resp_code": "00000000",
        "resp_desc": "成功",
        "token_no": "10000756292"
    },
    "sign": "N2NK76UUsGEvb5DXt6PH3Ova4XahA0l+eSKe3FBE4QlRXbyrdOBOixHjrLaUCur38GDPJs2+wg1VlXBO5SiwG3gXHZFNO1pTGTE3rSc4C049PMVIiYYjsFE0oSWiBHgfRGalWty0NaYpXbVzlJ9A4K1TrBhlHSAaEQGc1N/xYY8="
}
```
