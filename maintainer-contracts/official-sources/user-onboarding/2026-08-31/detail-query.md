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
## 用户信息查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/basicdata/query

*最近更新时间：2026.08.25*
### 应用场景
查询为用户基本信息、结算卡及配置费率等信息。

**适用对象**
  斗拱服务商或商户；

### 接口说明 
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)


### **公共参数**

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font> |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/customers/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |



### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属**用户ID**；<font color="green">示例值：6666000123120000</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号（业务申请编号），同一商户号当天唯一，<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220905</font> |


#### 请求示例

```json
{
    "sys_id": "ssproxy_dev",
    "data": {
        "req_seq_id": "rQ20221017061650234685690773988",
        "req_date": "20221017",
        "huifu_id": "6666000105447846"
    },
    "sign": "AHTW/j+t2Y2pjjfdaP8Fqbl/ryiMHCjKnZvakP1JfxRInc7z3RMflIFS+0jTAsTVT0GMO4Dzf/o55rslD/pFlrmZqxmYByC/6rjXOy5SmfdkRNM75gpJwgF7JGFfPMB4ZWPGpZmB+A60aC04s3ujDeZxSbn0Q9IkuPSeAuAHToY=",
    "product_id": "ZDTEST"
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| <span class="extend cb274f82_ca73_43ff_ad2c_b40b19f02b54">ent_base_info</span> | 企业用户基本信息 | String |  | N | jsonObject格式 |
| <span class="extend 7fd34fb5_de1c_4897_b66a_be4f31bd2b0b">indv_base_info</span> | 个人用户基本信息 | String |  | N | jsonObject格式 |
| <span class="extend 891569c7_06e6_45cd_b186_c549c1befbb9">card_info</span> | 结算卡信息 | String |  | N | jsonObject格式 |
| <span class="extend 9559f794_4474_41a0_a01d_e7a1b3e014fa">settle_config_list</span> | 结算信息配置列表 | String |  | N | jsonArray格式 |
| <span class="extend 002b5eb7_e066_4000_8676_0af659d7aad8">qry_cash_config_list</span> | 取现配置列表 | String |  | N | jsonArray格式 |
| <span class="extend 8ceacad3_652a_4a69_af6b_541ff654a4e6">qry_cash_card_info_list</span> | 取现卡信息 | String |  | N | jsonArray格式 |
| <span class="extend a907c3e5_5992_4a2c_a423_a5a57c6c1c2d">elec_acct_config</span> | 斗拱e账户功能配置 | String |  | N | 用于总部商户、下级商户配置斗拱E账户功能 |
| <span class="extend b83cfb4c_eee9_42cf_b2a3_02d56b68fd71">elec_receipt_config</span> | 电子回单配置 | Object |  | N | jsonObject格式；银行电子回单配置功能 |
| <span class="extend bb27d100_1c8a_4f47_98ba_f0b53b8fa8c1">sign_user_info</span> | 签约人信息 | Object |  | C | 开通电子回单必填 |

<!-- extend:start -->
<!-- div:extend-table cb274f82_ca73_43ff_ad2c_b40b19f02b54-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| reg_name | 企业用户名称 | String | 128 | Y | 企业用户名称，当为汉字时以2个字符计算；<font color="green">示例值：上海汇付支付服务公司</font> |
| license_code | 营业执照编号 | String | 20 | Y | <font color="green">示例值：92650109MA79R8E308</font> |
| license_validity_type | 证照有效期类型 | String | 1 | Y | 1：长期有效；0：非长期有效；<font color="green">示例值：1</font> |
| license_begin_date | 证照有效期起始日期 | String | 8 | Y | 有效期格式：yyyyMMdd；<font color="green">示例值：20220909</font> |
| license_end_date | 证照有效期结束日期 | String | 8 | N | 有效期格式：yyyyMMdd；<font color="green">示例值：20420909</font> |
| reg_prov_id | 注册地址(省) | String | 6 | Y | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310000</font> |
| reg_area_id | 注册地址(市) | String | 6 | Y | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font> |
| reg_district_id | 注册地址(区) | String | 6 | Y | 地区编码内容较多，请下载查询 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310101</font> |
| reg_detail | 注册地址(详细信息) | String | 256 | Y | <font color="green">示例值：上海市徐汇区XX路XX号</font> |
| legal_name | 法人姓名 | String | 32 | Y | <font color="green">示例值：张三</font> |
| legal_cert_type | 法人证件类型 | String | 2 | Y | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明 ；<font color="green">示例值：00</font> |
| legal_cert_no | 法人证件号码 | String | 32 | Y | <font color="green">示例值：3209026198312183829</font> |
| legal_cert_validity_type | 法人证件有效期类型 | String | 1 | Y | 1：长期有效；  0：非长期有效；<font color="green">示例值：0</font> |
| legal_cert_begin_date | 法人证件有效期开始日期 | String | 8 | Y | 有效期格式：yyyyMMdd；<font color="green">示例值：20220909</font> |
| legal_cert_end_date | 法人证件有效期截止日期 | String | 8 | N | 有效期格式：yyyyMMdd；<font color="green">示例值：20340909</font> |
| contact_name | 管理员姓名 | String | 32 | Y | <font color="green">示例值：李四</font> |
| contact_mobile_no | 管理员手机号 | String | 11 | Y | 11位数字；<font color="green">示例值：18611111111</font> |
| contact_email | 管理员电子邮箱 | String | 64 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| login_name | 管理员账号 | String | 32 | N | <font color="green">示例值：cwd10012423</font> |
| <span class="extend effda96c_9caa_4033_b3ff_636d34823801">file_list</span> | 附件资料列表 | Object |  | N | 格式jsonArray |
| mcc | 所属行业 | String | 7 | N | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；<font color="green">示例值：5311</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table effda96c_9caa_4033_b3ff_636d34823801-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 8 | Y | 请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；<font color="green">示例值：F85</font> |
| file_id | 文件jfileID | String | 128 | Y | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_name | 文件名称 | String | 128 | N | <font color="green">示例值：test42001.jpg</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7fd34fb5_de1c_4897_b66a_be4f31bd2b0b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 个人姓名 | String | 32 | Y | <font color="green">示例值：张三</font> |
| cert_type | 个人证件类型 | String | 2 | Y | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；<font color="green">示例值：00</font> |
| cert_no | 个人证件号码 | String | 32 | Y | <font color="green">示例值：320928198412030384</font> |
| cert_validity_type | 个人证件有效期类型 | String | 1 | Y | 1：长期有效；0：非长期有效；<font color="green">示例值：0</font> |
| cert_begin_date | 个人证件有效期开始日期 | String | 8 | Y | 有效期格式：yyyyMMdd；<font color="green">示例值：20220909</font> |
| cert_end_date | 个人证件有效期截止日期 | String | 8 | N | 有效期格式：yyyyMMdd；<font color="green">示例值：20340909</font> |
| mobile_no | 手机号 | String | 11 | Y | 11位数字，<font color="green">示例值：18611111111</font> |
| email | 电子邮箱 | String | 64 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| login_name | 管理员账号 | String | 32 | N | <font color="green">示例值：cws48304494532</font> |
| <span class="extend 1d12a675_8109_4e18_9322_f0b83ba1a1b2">file_list</span> | 附件资料列表 | Object |  | N | 格式jsonArray |
| mcc | 所属行业 | String | 7 | N | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；<font color="green">示例值：5311</font> |
| prov_id | 省 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> ；如修改省市区要级联修改<br/> |
| area_id | 市 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font> ；如修改省市区要级联修改<br/> |
| district_id | 区 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310101</font> ；如修改省市区要级联修改<br/> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1d12a675_8109_4e18_9322_f0b83ba1a1b2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 8 | Y | 请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；<font color="green">示例值：F85</font> |
| file_id | 文件jfileID | String | 128 | Y | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_name | 文件名称 | String | 128 | N | <font color="green">示例值：test42001.jpg</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 891569c7_06e6_45cd_b186_c549c1befbb9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 1 | Y | 0：对公，1：对私法人，2：对私非法人，4：对公非同名；<font color="green">示例值：1</font> |
| card_name | 银行卡户名 | String | 128 | Y | <font color="green">示例值：上海汇付支付服务公司</font> |
| card_no | 银行卡号 | String | 32 | Y | <font color="green">示例值：0206014170008888</font> |
| prov_id | 银行所在省 | String | 6 | Y | 地区编码参考下载 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | Y | 地区编码参考下载 [下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font> |
| bank_code | 银行号 | String | 8 | N | 请参考[点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font> |
| branch_code | 联行号 | String | 12 | N | 请参考[点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | N | <font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| cert_type | 持卡人证件类型 | String | 2 | N | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；<font color="green">示例值：00</font> |
| cert_no | 持卡人证件号码 | String | 32 | N | <font color="green">示例值：320926198412026034</font> |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | N | 1：长期有效； 0：非长期有效；<font color="green">示例值：1</font> |
| cert_begin_date | 持卡人证件有效期起始日期 | String | 8 | N | 有效期格式：yyyyMMdd；<font color="green">示例值：20140909</font> |
| cert_end_date | 持卡人证件有效期截止日期 | String | 8 | N | 有效期格式：yyyyMMdd；<font color="green">示例值：20440909</font> |
| mp | 银行卡绑定手机号 | String | 11 | N | 11位数字，<font color="green">示例值：18611111111</font> |
| token_no | 绑卡序列号 | String | 20 | N | <font color="green">示例值：10004053462</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9559f794_4474_41a0_a01d_e7a1b3e014fa-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_status | 结算状态 | String | 1 | N | 0：关闭 1：打开；<font color="green">示例值：1</font> |
| settle_cycle | 结算周期 | String | 2 | Y | T1：下个工作日到账；D1：下个自然日到账；TS:笔笔结算；<font color="green">示例值：T1</font> |
| min_amt | 起结金额 | String | 17 | N | 整数最多14位，小数最多两位；<font color="green">示例值：1000.00</font> |
| remained_amt | 留存金额 | String | 17 | N | 整数最多14位，小数最多两位；<font color="green">示例值：500.00</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 默认为空，如果需要自定义结算打款备注，请使用此字段传入；<font color="green">示例值：业务收款</font> |
| out_settle_flag | 手续费外扣标记 | String | 1 | N | 1:外扣 2:内扣；<font color="green">示例值：1</font> |
| out_settle_huifuid | 结算手续费外扣时的汇付ID | String | 16 | N | <font color="green">示例值：6666000123120000</font> |
| out_settle_acct_type | 结算手续费外扣时的账户类型 | String | 2 | N | 01:基本户；02:现金户；05:充值户；<font color="green">示例值：01</font> |
| settle_batch_no | 结算批次号 | String | 6 | N | <font color="green">示例值：1100</font>；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| fixed_ratio | 节假日结算手续费率 | String | 6 | C | settle_cycle为D1时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<br>settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；<font color="green">示例值：0.05</font> |
| constant_amt | 节假日结算手续费固定金额 | String | 15 | C | settle_cycle为D1时必填。单位元，需保留小数点后两位。不收费请填写0.00；<br>settle_cycle结算周期为D1时，遇节假日按此费率结算 ；<br/> <font color="green">示例值：1.00</font> |
| workday_fixed_ratio | 工作日结算手续费率 | String | 6 | N | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；<font color="green">示例值：0.05</font> |
| workday_constant_amt | 工作日结算手续费固定金额 | String | 15 | N | 单位元，需保留小数点后两位。不填默认为0.00；<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 002b5eb7_e066_4000_8676_0af659d7aad8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cash_type | 业务类型 | String | 2 | N | T1：下个工作日到账；D1：下个自然日到账；D0：自然日当日取现并到账；<font color="green">示例值：T1</font> |
| switch_state | 开关状态 | String | 1 | N | 0：关闭； 1：开通；<font color="green">示例值：1</font> |
| fix_amt | 提现手续费（固定/元） | String | 6 | C | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；<font color="green">示例值：1.00</font><br>注：当cash_type=D1时为节假日取现手续费 |
| fee_rate | 提现手续费率（%） | String | 6 | C | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate<br>2、当cash_type=D1时为节假日取现手续费 |
| weekday_fix_amt | D1工作日取现手续费固定金额 | String | 6 | C | 单位元，需保留小数点后两位。不收费请填写0.00；<font color="green">示例值：1.00</font><br>cash_type=D1时，生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| weekday_fee_rate | D1工作日取现手续费率 | String | 6 | C | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>cash_type=D1时，生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| out_cash_flag | 是否开通取现手续费外扣 | String | 1 | N | 1:外扣  2:内扣；<font color="green">示例值：1</font> |
| out_cash_huifuid | 手续费承担方 | String | 18 | N | 手续费外扣时必需指定手续费承担方ID；<font color="green">示例值：6666000123120000</font> |
| out_cash_acct_type | 取现手续费外扣子账户类型 | String | 2 | N | 01:基本户；02:现金户；05:充值户；<font color="green">示例值：01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8ceacad3_652a_4a69_af6b_541ff654a4e6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 1 | N | 0：对公； 1：对私；<font color="green">示例值：1</font> |
| card_name | 银行卡户名 | String | 128 | N | <font color="green">示例值：上海汇付支付服务公司</font> |
| card_no | 银行卡号 | String | 32 | N | <font color="green">示例值：0206014170008888</font> |
| area_id | 银行所在市 | String | 6 | N | [地区编码参考下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310000</font> |
| prov_id | 银行所在省 | String | 6 | N | [地区编码参考下载](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font> |
| bank_code | 银行号 | String | 8 | N | [请参考点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font> |
| bank_name | 银行名称 | String | 32 | N | <font color="green">示例值：中国工商银行</font> |
| branch_code | 联行号 | String | 12 | N | 请参考[点击查看](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | N | <font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| cert_type | 持卡人证件类型 | String | 2 | N | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；<font color="green">示例值：00</font> |
| cert_no | 持卡人证件号码 | String | 32 | N | <font color="green">示例值：320926198412026034</font> |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | N | 1：长期有效； 0：非长期有效；<font color="green">示例值：1</font> |
| cert_begin_date | 持卡人证件有效期起始日期 | String | 8 | N | 格式：yyyyMMdd；<font color="green">示例值：20140909</font> |
| cert_end_date | 持卡人证件有效期截止日期 | String | 8 | N | 格式：yyyyMMdd；<font color="green">示例值：20340909</font> |
| mp | 银行卡绑定手机号 | String | 11 | N | 11位数字，<font color="green">示例值：18611111111</font> |
| token_no | 绑卡序列号 | String | 20 | N | <font color="green">示例值：10004053462</font> |
| status | 银行卡绑定状态 | String | 1 | N | N:正常 C:关闭；<font color="green">示例值：N</font> |
| is_settle_default | 默认结算卡标志 | String | 1 | N | 是否为默认结算卡标志；Y:是 N:否；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a907c3e5_5992_4a2c_a423_a5a57c6c1c2d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子账户开关 | String | 1 | Y | 电子账户开通总开关：0:关闭 1:开通 |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家 |
| cash_fee_party | 电子账户提现手续费承担方 | String | 1 | Y | 1:总部 2:其他； |
| scene | 场景 | String | 3 | Y | 与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| role_type | 角色类型(角色编号) | String | 6 | Y | 与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx);示例值：001001 |
| <span class="extend 3ee9e0a2_4f31_4f46_b3de_1c92b54aef29">elec_card_list</span> | 银行卡信息 | Object |  | N | jsonArray字符串 |
| bank_status | 电子账户开通状态 | String | 1 | Y | S：成功 F：失败；<font color="green">示例值：S</font> |
| bank_message | 银行信息 | String | 512 | N | 银行返回开户结果 |
| merchant_id | 银行会员编号 | String | 15 | N | <font color="green">示例值：J00000000000001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3ee9e0a2_4f31_4f46_b3de_1c92b54aef29-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | N | [参考省市区编码表；示例值：310000](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| area_id | 银行所在市 | String | 6 | N | [参考省市区编码表；示例值：310100](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| bank_code | 银行编码 | String | 8 | Y | [参考银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| branch_code | 支行联行号 | String | 12 | Y | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| branch_name | 支行名称 | String | 64 | Y | 示例值：中国工商银行上海市中山北路支行 |
| card_name | 结算账户名 | String | 128 | Y | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| card_no | 银行卡号 | String | 32 | Y | 示例值：98140008801800008888 |
| card_type | 卡类型 | String | 1 | Y | 0:对公 1:对私法人 |
| mp | 银行绑定手机号 | String | 11 | C | 11位数字， 示例值：18611111111 |
| default_cash_flag | 默认卡标识 | String | 1 | N | 0：非默认卡 1：默认卡(不填，默认为0) |
| auth_version | 用户授权协议版本号 | String | 64 | C | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| auth_no | 用户授权协议号 | String | 64 | C | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
| status | 卡状态 | String | 1 | Y | 绑卡状态，:N-正常，C-关闭，D-注销；示例值：N |
| bind_card_msg | 绑卡返回描述 | String | 256 | Y | 示例值：成功 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b83cfb4c_eee9_42cf_b2a3_02d56b68fd71-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子回单开关 | String | 1 | N | 0:关闭 1:开通  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bb27d100_1c8a_4f47_98ba_f0b53b8fa8c1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 签约人类型 | String | 6 | Y | LEGAL-法人 |
| name | 签约人姓名 | String | 32 | N | 企业用户不填默认为法人姓名，个人用户不填默认为个人姓名；示例值：张三 |
| mobile_no | 签约人手机号 | String | 11 | Y | 需为11位数字 ；示例值：18611111111 |
| cert_no | 签约人证件号 | String | 18 | N | 企业用户不填默认为法人证件号，个人用户不填默认为个人证件号；当前仅支持法人;示例值：321012313213222133 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "card_info": "{\"area_id\":\"310100\",\"bank_code\":\"01050000\",\"branch_code\":\"105290075067\",\"branch_name\":\"中国建设银行股份有限公司上海五角场支行\",\"card_name\":\"王家二\",\"card_no\":\"6217007210064760000\",\"card_type\":\"0\",\"cert_begin_date\":\"20200101\",\"cert_end_date\":\"20260101\",\"cert_no\":\"371202198806087518\",\"cert_type\":\"00\",\"cert_validity_type\":\"0\",\"mp\":\"13700000214\",\"prov_id\":\"310000\",\"token_no\":\"10000979883\"}",
        "indv_base_info": "{\"cert_begin_date\":\"20200101\",\"cert_end_date\":\"29991231\",\"cert_no\":\"310112197806081453\",\"cert_type\":\"00\",\"cert_validity_type\":\"1\",\"email\":\"changliang.wang_c@huifu.com\",\"file_list\":[{\"file_id\":\"99e00421-dad7-3334-9538-4f2ad10612d5\",\"file_name\":\"法人身份证正面.jpg\",\"file_type\":\"F02\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"法人身份证反面.jpg\",\"file_type\":\"F03\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"营业执照.jpg\",\"file_type\":\"F07\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"开户许可证.jpg\",\"file_type\":\"F08\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"开户许可证.jpg\",\"file_type\":\"F15\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"银行卡正面.jpg\",\"file_type\":\"F13\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"银行卡反面.jpg\",\"file_type\":\"F14\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"门头照.jpg\",\"file_type\":\"F24\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"门头照.jpg\",\"file_type\":\"F22\"},{\"file_id\":\"99e00421-dad7-3334-9538-4f2ad10612d5\",\"file_name\":\"法人身份证正面.jpg\",\"file_type\":\"F02\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"法人身份证反面.jpg\",\"file_type\":\"F03\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"营业执照.jpg\",\"file_type\":\"F07\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"开户许可证.jpg\",\"file_type\":\"F08\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"开户许可证.jpg\",\"file_type\":\"F15\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"银行卡正面.jpg\",\"file_type\":\"F13\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"银行卡反面.jpg\",\"file_type\":\"F14\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"门头照.jpg\",\"file_type\":\"F24\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"门头照.jpg\",\"file_type\":\"F50\"},{\"file_id\":\"99e00421-dad7-3334-9538-4f2ad10612d5\",\"file_name\":\"法人身份证正面.jpg\",\"file_type\":\"F02\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"法人身份证反面.jpg\",\"file_type\":\"F03\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"营业执照.jpg\",\"file_type\":\"F07\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"开户许可证.jpg\",\"file_type\":\"F08\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"开户许可证.jpg\",\"file_type\":\"F15\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"银行卡正面.jpg\",\"file_type\":\"F13\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"银行卡反面.jpg\",\"file_type\":\"F14\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"门头照.jpg\",\"file_type\":\"F24\"},{\"file_id\":\"0c74b071-b0d6-3397-8fe5-dc93c9592019\",\"file_name\":\"门头照.jpg\",\"file_type\":\"F22\"}],\"login_name\":\"Lg20220ig3070j5kf48200\",\"mobile_no\":\"15556622369\",\"name\":\"王家二\"}",
        "qry_cash_config_list": "[{\"cash_type\":\"D0\",\"fee_rate\":\"10.00\",\"fix_amt\":\"0.01\",\"out_cash_flag\":\"2\",\"out_cash_huifuid\":\"\",\"switch_state\":\"1\"},{\"cash_type\":\"D1\",\"fee_rate\":\"11.01\",\"fix_amt\":\"0.02\",\"out_cash_flag\":\"2\",\"out_cash_huifuid\":\"\",\"switch_state\":\"1\"},{\"cash_type\":\"T1\",\"fee_rate\":\"43.00\",\"fix_amt\":\"1.02\",\"out_cash_flag\":\"2\",\"out_cash_huifuid\":\"\",\"switch_state\":\"1\"}]",
        "resp_code": "00000000",
        "resp_desc": "成功",
        "settle_config_list": "[{\"min_amt\":\"1.00\",\"out_settle_flag\":\"2\",\"out_settle_huifuid\":\"6666000105306730\",\"remained_amt\":\"10.00\",\"settle_abstract\":\"结算配置\",\"settle_batch_no\":\"0\",\"settle_cycle\":\"T1\",\"settle_status\":\"1\"}]"
    },
    "sign": "FWT1mMIJUFBOF12o4Y6vkeg8xiBm9ASSIsl7hibnAFU3HQFK17R6c8cFs/ysT6+5RFCkCyWeUkzxqPaWjJ7qDmsGRve/FVD6RzwllGHGc2j0EJxQKEVMZbbqjxswXVJiKNtl6SjxoUHfvhfW3qzgNmg+1h0KxJs0LRLjWRMfZjA="
}
```
