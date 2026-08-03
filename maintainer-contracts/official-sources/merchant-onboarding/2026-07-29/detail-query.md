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
## 商户详细信息查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/basicdata/query

*最近更新时间：2026.07.28*
> 2023.6.30斗拱升级了商户进件类接口，老版接口、升级指引请参考[说明文档](old_api/api_2023shglsj)
### 应用场景
商户获取到汇付商户号后，可使用此接口查询商户信息。支持查询商户基本信息、业务开通信息（线上&线下）、银行卡绑卡信息、结算和取现配置信息。

**适用对象**  
已开通成功获得huifu_id的商户；

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
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |


### **注意** 
- 必填字段取值“C”代表条件必填；  

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号，同一商户号当天唯一；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准；<font color="green">示例值：20220125</font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108854952",
    "product_id": "YYZY",
    "data": {
        "req_seq_id": "202211101668071566142",
        "req_date": "20221110",
        "huifu_id": "6666000108854952"
    },
    "sign": "Ghc8FKQLPqWFMpHnHV8ZVqNzCvM+/xV7WL8G+V/KtY/PsZtu2+2EABcr2SH1yRSekeTKEJffemRjXmuqTgZwsXnse9JduNRtj9Z/1t1H07V4YzpuWw8NVVT7M9R2Z9djjzsOxTYpdF37QRj3kVbg8mAbFcNDuV1vStLm2pRF7lhq6yGB1Q+GAsW2KxEvwuuUnY1BsmMOmzrx+YH/jZ74dSsmYCdZS/SolHcqsgqbqrNUHR/q1Z6j+UmH+s+2A7WS6TvCPoZEY3XVv8uLysm1U2J/1l/4CSsKgW2PlWIBFqhRJikymUw7No+8Yz89DATcLj/9k5sCv7JzVu0G87/bvw=="
}
```
### 返回参数


#### 返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| product_id | 产品号 | String | 32 | N | 汇付分配的产品号，<font color="green">示例值：MCS</font> |
| upper_huifu_id | 直属渠道号 | String | 18 | N | 该商户进件完成后隶属的渠道商号； 非直营商户时有值。<font color="green">示例值：6666000123123123</font> |
| ext_mer_id | 外部商户号 | String | 64 | N | 支持关联外部商户系统中的商户号；<font color="green">示例值：HF100001</font> |
| reg_name | 商户注册名称 | String | 128 | Y | 1.商户名称必须与商家证照上的名称一致； <br />2. 若个体工商户证照没有商家名称或者名称为“\*”或者“” 则商户名称应填 “个体户XXX”（XXX为营业执照上经营者姓名）当为汉字时，以2个字符计算；<br/><font color="green">示例值：上海汇付支付服务有限公司</font> |
| short_name | 商户简称 | String | 32 | Y | 商户经营简称；<font color="green">示例值：汇付支付</font> |
| receipt_name | 小票名称 | String | 50 | N | 可以作为POS小票的名称，企业商户有值；<font color="green">示例值：汇付支付</font> |
| mer_en_name | 商户英文名称 | String | 256 | N | 商户英文名称；<font color="green">示例值：Shanghai Huifu Payment Co. Ltd.</font> |
| remarks | 备注 | String | 300 | N | 备注内容；<font color="green">示例值：华东分公司</font> |
| cust_type | 商户类型 | String | 1 | Y | 1：企业   2：个人 ；<font color="green">示例值：1</font> |
| ent_type | 商户种类 | String | 1 | Y | 1：政府机构、2：国营企业、3：私营企业、4：外资企业、5：个体工商户、6：其他组织、7：事业单位、9：业主委员会；<br/><font color="green">示例值：3</font> |
| busi_type | 经营类型 | String | 1 | N | 1:实体 2:虚拟，企业商户有值；<font color="green">示例值：1</font> |
| mcc | 所属行业（MCC） | String | 7 | N | [银联MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylmccbm)，企业商户有值；<font color="green">示例值：5411</font> |
| license_type | 证照类型 | String | 32 | N | 参见[机构证照类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E6%9C%BA%E6%9E%84%E8%AF%81%E7%85%A7%E7%B1%BB%E5%9E%8B)说明； <font color="green">示例值：NATIONAL_LEGAL</font> |
| license_code | 营业执照编号 | String | 18 | N | 工商营业执照编号，<font color="green">示例值：92650109MA79R8E308</font> |
| license_validity_type | 证照有效期类型 | String | 1 | N | 企业类商户有值，1:长期有效 0:非长期有效；<font color="green">示例值：0</font> |
| license_begin_date | 证照开始日期 | String | 8 | N | 企业类商户有值，格式yyyyMMdd，<font color="green">示例值:20220125</font>，以北京时间为准; |
| license_end_date | 证照结束日期 | String | 8 | N | 企业类商户有值，格式yyyyMMdd，<font color="green">示例值:20250125</font>，以北京时间为准；“29991231“或”99991231”代表长期 |
| reg_prov_id | 注册省 | String | 6 | N | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font>；与证照保持一致 |
| reg_area_id | 注册市 | String | 6 | N | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font>；与证照保持一致 |
| reg_district_id | 注册区 | String | 6 | N | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310101</font>；与证照保持一致 |
| reg_detail | 注册详细地址 | String | 256 | N | 与证照保持一致；<font color="green">示例值：上海市徐汇区XX路XX号</font> |
| prov_id | 银行所在省 | String | 6 | N | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) <font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | N | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)  <font color="green">示例值：310100</font> |
| district_id | 经营地址所在区县 | String | 6 | N | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)<font color="green">示例值：310101</font> |
| detail_addr | 商户经营详细地址 | String | 256 | N | 企业商户有值；<font color="green">示例值：上海市徐汇区XX路XX号</font> |
| legal_name | 法人姓名 | String | 32 | N | 支持少数名族,最大支持10个汉字；<font color="green">示例值：张三</font> |
| legal_cert_type | 法人证件类型 | String | 2 | N | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》 说明；<font color="green">示例值：00</font> |
| legal_cert_no | 法人证件号码 | String | 40 | N | <font color="green">示例值：310112200001018888</font> |
| legal_cert_validity_type | 法人证件有效期类型 | String | 1 | N | 1:长期有效 0:非长期有效，<font color="green">示例值：0</font> |
| legal_cert_begin_date | 法人证件有效期开始日期 | String | 8 | N | yyyyMMdd，<font color="green">示例值:20220125</font>，以北京时间为准 |
| legal_cert_end_date | 法人证件有效期结束日期 | String | 8 | N | yyyyMMdd，<font color="green">示例值:20220125</font>，以北京时间为准。当法人证件有效期类型为0 |
| legal_mobile_no | 法人手机号 | String | 11 | N | <font color="green">示例值：13911111111</font> |
| legal_addr | 法人身份证地址 | String | 256 | N | <font color="green">示例值：上海市徐汇区宜山路700号普天信息产业园2期C5栋</font> |
| occupation | 负责人职业 | String | 2 | N | 1A：各类专业,技术人员<br/>1B：国家机关,党群组织,企事业单位的负责人<br/>1C：办事人员和有关人员<br/>1D：商业工作人员<br/>1E：服务性工作人员<br/>1F：农林牧渔劳动者<br/>1G：生产工作,运输工作和部分体力劳动者<br/>1H：不便分类的其他劳动者<br/><font color="green">示例值：1G</font> |
| <span class="extend 0e59d33d_70ca_46fb_adf2_ee1942b32022">beneficiary_info_list</span> | 受益人信息实体 | String |  | N | jsonArray字符串 |
| contact_name | 管理员姓名 | String | 30 | N | 商户联系人姓名。支持少数名族,最大支持15个汉字；示例值：张三 |
| contact_mobile_no | 管理员手机号 | String | 11 | N | 手机号格式；<font color="green">示例值：13911111111</font> |
| contact_email | 管理员邮箱 | String | 40 | N | 邮箱格式；<font color="green">示例值：carl.chen@huifu.com</font> |
| service_phone | 客服电话 | String | 11 | N | 支持固话格式，手机格式；<font color="green">示例值：021-88888888</font> |
| login_name | 管理员账号 | String | 32 | N | 自定义值，必须全系统唯一；作为控台的登陆用户名或POS机的登陆用户名；<font color="green">示例值：cwdsd1001</font> |
| sms_send_flag | 注册短信发送标记 | String | 1 | N | Y:已发送,N:未发送；<font color="green">示例值：Y</font> |
| mer_url | 商户主页URL | String | 256 | N | 商户主页URL； <font color="green">示例值：https://www.huifu.com/home/</font> |
| mer_icp | 商户ICP备案编号 | String | 50 | N | 商户ICP备案编号；<font color="green">示例值：沪ICP备06046402号-28</font> |
| open_licence_no | 开户许可证核准号 | String | 32 | N | <font color="green">示例值：J2900123456789</font> |
| <span class="extend b3803a3a_4f23_4fe5_9e4e_4dae916c7e2d">qry_cash_card_info_list</span> | 卡信息 | String |  | N | jsonArray格式 |
| <span class="extend 4b599cf8_8811_4302_9000_4a8ecdf744d0">qry_cash_config_list</span> | 取现配置列表 | String |  | N | jsonArray格式 |
| <span class="extend 4c00f562_6dd2_41c3_943c_670ce25808ac">qry_settle_config_list</span> | 结算配置 | String |  | N | jsonArray格式 |
| <span class="extend 3899f7bc_4fac_43b7_a80e_a96df3248793">agreement_info_list</span> | 协议信息 | String |  | N | jsonArray格式；[签约协议说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx) |
| <span class="extend b51121b8_c27c_4486_bfdf_356ac107a1bc">sign_user_info_list</span> | 签约人列表 | String |  | N | jsonArray格式 |
| online_busi_type | 线上业务类型 | String | 64 | C | 开通快捷、网银、余额支付Pro版、分账、代扣；参见[线上业务类型编码及补充材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx)；<font color="green">示例值：H7999AL</font> |
| <span class="extend 52584abe_c6f4_4f0b_8a85_44c8d3d1e0b6">online_media_info_list</span> | 运营媒介 | String |  | N | jsonObject字符串 |
| quick_flag | 是否开通快捷 | String | 1 | N | 1:开通 0:未开通，为空未配置(未开通);<font color="green">示例值：1</font> |
| online_flag | 是否开通网银 | String | 1 | N | 1:开通 0:未开通，为空未配置(未开通);<font color="green">示例值：1</font> |
| withhold_flag | 是否开通代扣 | String | 1 | N | 1:开通 0:未开通，为空未配置(未开通);<font color="green">示例值：1</font> |
| pre_authorization_flag | 是否开通支付宝预授权 | String | 1 | N | 1:开通 0:未开通，为空未配置(未开通);<font color="green">示例值：1</font> |
| web_flag | 是否开通手机WAP支付 | String | 1 | N | 1:开通 0:未开通，为空未配置(未开通)；<font color="green">示例值：1</font> |
| balance_pay_flag | 是否开通余额支付 | String | 1 | N | 1:开通 0:未开通，为空未配置(未开通)；<font color="green">示例值：1</font> |
| <span class="extend bceeb557_19e8_4ccf_8b4f_ae6316d7f0ea">qry_balance_pay_config</span> | 余额支付配置对象 | String |  | N | jsonObject格式 |
| <span class="extend fa0cf9b7_f7f8_47a3_aa39_b27623071334">online_fee_conf_list</span> | 线上费率配置 | String |  | N | jsonArray格式 |
| delay_flag | 是否开通延迟入账 | String | 1 | N | N：否 Y：是，为空则为否；<font color="green">示例值：Y</font> |
| forced_delay_flag | 商户开通强制延迟标记 | String |  | N | Y:开通,N:关闭；<font color="green">示例值：N</font> |
| out_fee_flag | 交易手续费外扣标记 | String | 1 | N | 1：外扣，2：内扣；（默认2内扣）；<font color="green">示例值：2</font> |
| out_fee_huifu_id | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时必填，<font color="green">示例值：6666000123123123<br>优先级高于相同名称的公共参数； |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，<font color="green">示例值：01</font><br/>优先级高于相同名称的公共参数； |
| <span class="extend ce1594e2_3b10_4705_8e23_b2c79b7478f8">qry_wx_conf_list</span> | 微信支付配置信息 | String |  | N | jsonArray格式 |
| <span class="extend 8e428b1f_cc73_4636_b586_25270785ac8b">qry_ali_conf_list</span> | 支付宝支付配置信息 | String |  | N | jsonArray格式 |
| <span class="extend 6bce7bb6_38bd_4a8c_a98d_a0f60d0e47b7">qry_bank_card_conf</span> | 银行卡支付配置信息 | String |  | N | jsonObject格式；只有企业商户有值 |
| <span class="extend 8af7c28a_9689_444a_b47b_364f2be87ea8">qry_union_conf</span> | 银联二维码支付配置信息 | String |  | N | jsonObject格式 |
| <span class="extend 6f680f62_7fc3_4cb6_90d9_8872cba6074b">out_order_funds_merge</span> | 全域资金管理配置 | String |  | N | jsonObject字符串 |
| <span class="extend 660caa09_1dc5_45bf_beb1_5ffaa44b146c">combine_pay_config</span> | 补贴支付配置对象 | String |  | N | jsonObject格式 |
| <span class="extend b578f1f6_4598_411f_a145_8859d2aaabe4">wx_zl_conf</span> | 微信直连配置对象 | String |  | N | jsonObject格式 |
| <span class="extend 8ea49697_3b3f_48f8_a24e_db010f0d7d8c">ali_zl_conf_list</span> | 支付宝直连配置列表 | String |  | N | jsonArray格式 |
| <span class="extend a634e58d_8b3f_42a5_b9f8_de8bfb15dc72">file_info_list</span> | 商户材料列表 | String |  | N | jsonArray格式 |
| recon_resp_addr | 交易应答异步通知地址 | String | 128 | N | 消息接收地址，为空不推送消息。 <font color="green">示例值：http://service.example.com/to/path</font>。 |
| enter_fee | 开户费用值(元) | String | 14 | N | <font color="green">示例值：5.00</font> |
| enter_fee_flag | 开户费用类型 | String | 1 | N | 1-一次性开户费，2-平台套餐费（元/年）<br/><font color="green">示例值：2</font> |
| mer_Identity | 商户身份 | String | 1 | N | 1：总部商户，0：下级商户；<font color="green">示例值：1</font> |
| mer_level | 商户层级 | String | 1 | N | 1：总部，2：一级，3：二级，4：三级，5：四级；<br><font color="green">示例值：1</font> |
| <span class="extend de0048b1_5426_49a4_9685_e56d649948f1">mer_config_info</span> | 开通下级商户权限配置对象 | String |  | N | 权限配置，价格配置 |
| <span class="extend d75ac4cd_ae7b_49a5_baa5_accfc15c14dc">elec_acct_config</span> | 斗拱e账户功能配置 | String |  | N | 用于总部商户、商户配置斗拱E账户功能 |
| <span class="extend df1962ce_4a44_4db3_9239_59ddec793412">tax_config</span> | 灵活用工配置 | String |  | N | jsonObject字符串 |
| online_refund | 是否开通在线退款 | String | 1 | N | N：否 Y：是；<font color="green">示例值：Y</font> |
| platform_refund | 是否支持平台退款 | String | 1 | N | N：否 Y：是；<font color="green">示例值：Y</font> |
| support_revoke | 是否支持撤销 | String | 1 | N | N：否 Y：是；<font color="green">示例值：Y</font> |
| <span class="extend b14d6d3b_aca5_48cf_82b3_d43534f1a24c">split_bill_result</span> | 分账配置信息 | String |  | N | jsonArray字符串 |
| <span class="extend f2c26e03_00b1_44ee_8069_4ba66b5b289b">share_holder_info_list</span> | 股东信息 | String |  | N | jsonArray格式； |
| head_office_flag | 是否总部商户 | String | 1 | N | 1：总部， 0：分店，默认总部。<font color="green">示例值：0</font> |
| <span class="extend 4527a325_62a0_4d51_8253_8c0419c65f9c">uni_app_payment_config</span> | 银联线上收银台 | String |  | N | jsonObject字符串 |
| <span class="extend 9926e0a8_41a0_4f92_b3ef_e39a5802e264">surrogate_config_list</span> | 代发配置 | String |  | N | jsonArray格式字符串 |
| <span class="extend fed0e7bc_6b1e_49c2_9c16_3df3afe350bd">large_amt_pay_config</span> | 大额支付配置 | String |  | N | jsonObject字符串 内容参考：large_amt_pay_config |
| half_pay_host_flag | 统一收银台开关 | String | 1 | N | Y:是 N:否（为空默认未开通） ；<font color="green">示例值：Y</font> |
| mer_stat | 商户状态 | String | 32 | N | NORMAL：正常 FREEZEWITHDRAWAL：冻结出金 CANCEL：注销 FREEZEDEPOSIT：冻结入金；示例值：NORMAL |
| <span class="extend 5d064fad_c285_4f15_8247_b3fe4a538681">agent_recheck_config</span> | 代发复核 | Object |  | N | jsonObject字符串 |
| online_recharge_flag | 商户开通网银充值开关 | String | 1 | N | 1:开通 0:未开通，为空未配置(未开通);<font color="green">示例值：1</font> |
| <span class="extend 47e44a99_28da_477d_9127_0988968eb991">lla_withhold_config</span> | 本地生活 | Object |  | N | jsonObject字符串 |
| refund_mend_open_flag | 是否开通垫资退款 | String | 1 | N | Y:是 N:否 ；<font color="green">示例值：Y</font> |
| <span class="extend 7c4f50ed_30b4_41a1_b2a8_4745331ec256">jxf_conf_info</span> | 捷行付配置 | Object |  | N | jsonObject字符串 |
| <span class="extend 9957cd9d_28f1_4c68_9bf8_c9c9bb50ea5a">merge_pay_config_info</span> | 合单支付配置信息 | Object |  | N | jsonObject字符串 |
| bill_payment_flag | 是否开通账单支付 | String | 1 | N | Y:是 N:否 ；<font color="green">示例值：Y</font> |
| activated_products | 产品大类 | String |  | N |  收款产品，02 账户与资金产品，03 业财数通产品；不传为空<font color="green">示例值：01,02,03</font> |
| withhold_pay_scene | 代扣场景 | String |  | N | 1:权益投流(订阅),2:非权益投流(订阅),3:保险缴纳,4:道路通行费(ETC),5:公共事业(水电煤)缴费,6:物业缴费 |
| <span class="extend 2651e296_3965_48d2_aa93_3280090bd718">material_card_info</span> | 对公卡信息 | Object |  | N | jsonObject字符串； |

<!-- extend:start -->
<!-- div:extend-table 0e59d33d_70ca_46fb_adf2_ee1942b32022-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bo_id | 受益人唯一ID | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| bo_name | 受益人名称 | String | 40 | Y | <font color="green">示例值：张三</font> |
| bo_type | 受益人证件类型 | String | 2 | Y | 00:身份证<br/> 01:护照<br/> 02:军官证<br/> 03:士兵证<br/> 04:回乡证<br/> 05:户口本<br/> 06:外国护照<br/> 07:其他<br/> 08:暂住证<br/> 09:警官证<br/> 10:文职干部证<br/> 11:港澳同胞回乡证<br/> 12:营业执照<br/><font color="green">示例值：00</font> |
| bo_no | 受益人证件号 | String | 50 | Y | <font color="green">示例值：3209219851202732</font> |
| bo_date_start | 受益人证件有效期开始时间 | String | 8 | Y | <font color="green">示例值：20210606</font> |
| bo_dead_line | 受益人证件有效期结束时间 | String | 8 | Y | <font color="green">示例值：20290606</font>；若证件有效期为长期，请填写：29991231；要求结束时间大于开始时间； |
| bo_address | 受益人地址 | String | 500 | Y | <font color="green">示例值：上海徐汇区共富一路55号401室</font>； |
| bo_mobile_no | 受益人手机号 | String | 11 | N | <font color="green">示例值：13911111111</font> |
| final_beneficiary_mode | 最终受益人受益方式 | String | 3 | N | A01：直接或间接控股25%（含）以上 <br/>A02：通过人事、财务等其他方式对公司进行控制 <br/>A03：高级管理人员 <br/>A04：法人或公司负责人 <br/>A05：其他<br/><font color="green">示例值：A01</font> |
| bo_stat | 受益人有效标识 | String | 10 | N | active：有效，inactive：无效 <font color="green">示例值：active</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b3803a3a_4f23_4fe5_9e4e_4dae916c7e2d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 1 | N | 0:对公 1:对私；<font color="green">示例值：0</font> |
| card_name | 卡户名 | String | 256 | N | 银行账户准确名称；<font color="green">示例值：上海汇付支付服务有限公司</font> |
| card_no | 卡号 | String | 32 | N | <font color="green">示例值：32453653455</font> |
| prov_id | 银行所在省 | String | 6 | N | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) <font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | N | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)  <font color="green">示例值：310100</font> |
| bank_code | 银行号 | String | 8 | N | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) <font color="green">示例值：01020000</font> |
| bank_name | 银行名称 | String | 32 | N | <font color="green">示例值：中国工商银行</font> |
| branch_code | 支行联行号 | String | 12 | N | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) 对公结算有值，对私结算不一定有值；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | N | 对公结算有值；<font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| cert_type | 持卡人证件类型 | String | 2 | N | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；<font color="green">示例值：00</font> |
| cert_no | 持卡人证件号码 | String | 32 | N | <font color="green">示例值：320937197512025018</font> |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | N | 1:长期有效 0:非长期有效；<font color="green">示例值：0</font> |
| cert_begin_date | 持卡人证件有效期开始日期 | String | 8 | N | 对私结算有值，持卡人证件有效期开始日期yyyyMMdd， <font color="green">示例值：20220125</font> ，以北京时间为准 |
| cert_end_date | 持卡人证件有效期截止日期 | String | 8 | N | 对私结算有值，持卡人证件有效期开始日期yyyyMMdd， <font color="green">示例值：20220125</font> ，以北京时间为准。证件类型长期有效时为空 |
| mp | 结算人手机号 | String | 11 | N | <font color="green">示例值：18611111111</font> |
| status | 银行卡绑定状态 | String | 1 | N | N:正常 C:关闭；<font color="green">示例值：N</font> |
| token_no | 绑卡序列号 | String | 20 | N | <font color="green">示例值：0097387899</font> |
| is_settle_default | 默认结算卡标志 | String | 1 | N | 是否为默认结算卡标志；Y:是 N:否；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4b599cf8_8811_4302_9000_4a8ecdf744d0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cash_type | 业务类型 | String | 2 | N | D0:当日到账；当日交易资金当天可取现到账；<br/>T1:下个工作日到账;<br/>D1:下个自然日到账;<br/>DM：当日到账；到账资金不包括当天的交易资金；<br/><font color="green">示例值：T1</font> |
| switch_state | 开关状态 | String | 1 | Y | 0:关闭 1:开通；<font color="green">示例值：1</font> |
| fix_amt | 提现手续费（固定/元） | String | 6 | C | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；<font color="green">示例值：1.00</font><br>注：当cash_type=D1时为节假日取现手续费 |
| fee_rate | 提现手续费率（%） | String | 6 | C | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate<br>2、当cash_type=D1时为节假日取现手续费 |
| weekday_fix_amt | D1工作日取现手续费固定金额 | String | 6 | C | 单位元，需保留小数点后两位。不收费请填写0.00；<font color="green">示例值：1.00</font><br>cash_type=D1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| weekday_fee_rate | D1工作日取现手续费率 | String | 6 | C | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>cash_type=D1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| out_cash_flag | 手续费外扣标记 | String | 1 | N | 1:外扣：取现时，从out_cash_huifuid账户扣手续费，2:内扣：从取现金额中扣手续费；<font color="green">示例值：1</font> |
| out_fee_huifuid | 手续费承担方 | String | 18 | N | 手续费外扣时必需指定手续费承担方ID；<font color="green">示例值：6666000123123123</font> |
| out_cash_acct_type | 取现手续费外扣时的账户类型 | String |  | N | 01-基本户，02-现金户， 05-充值户，out_cash_flag=1时有值；<font color="green">示例值：01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4c00f562_6dd2_41c3_943c_670ce25808ac-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_type | 结算类型 | String | 1 | N | 0:对公 1:对私；<font color="green">示例值：0</font> |
| settle_cycle | 结算周期 | String | 2 | N | T1:下个工作日到账;D1:下个自然日到账；<font color="green">示例值：T1</font> |
| min_amt | 起结金额 | String | 18 | N | 账户余额大于等于起结金额才会发起结算。无值则不设置起结金额；<font color="green">示例值：1000.00</font> |
| remained_amt | 留存金额 | String | 18 | N | 结算之后，账户剩余金额。无值则不设置留存金额；<font color="green">示例值：600.00</font> |
| fee_rate | 结算手续费率(%) | String | 17 | N |  保留两位小数，<font color="green">示例值：0.60</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 商户在基本信息入驻时编辑的结算摘要；<br/><font color="green">示例值：商品收款</font> |
| out_settle_flag | 手续费外扣标记 | String | 1 | N | 1:外扣：结算时，从out_settle_huifuid账户扣手续费；2:内扣：从结算金额中扣手续费；<font color="green">示例值：1</font> |
| out_settle_huifuid | 结算手续费外扣商户号 | String | 18 | N | 手续费外扣时必需指定手续费承担方ID；out_settle_flag=1时有值；<font color="green">示例值：6666000123123123</font> |
| out_settle_acct_type | 结算手续费外扣账户类型 | String | 2 | N | 01-基本户，02-现金户， 05-充值户，out_settle_flag=1时有值；<font color="green">示例值：01</font> |
| settle_status | 结算开关 | String | 1 | Y | 0:关闭 1:打开；<font color="green">示例值：1</font> |
| settle_pattern | 结算方式 | String | 2 | N | P0：批次结算 P1：定时结算 E1:中信E管家；<font color="green">示例值：P1</font> |
| is_priority_receipt | 是否优先到账 | String | 1 | N | settle_cycle为TS时不填。settle_pattern为P0时，有值 Y：是 N：否；<font color="green">示例值：Y</font> |
| settle_time | 自定义结算处理时间 | String | 6 | N | settle_pattern为P1时有值；格式：HHmmss；<br/><font color="green">示例值：113000</font> |
| token_no | 绑卡序列号 | String | 20 | N | 结算卡对应的绑卡序列号。<font color="green">示例值：10000093623</font> |
| settle_batch_no | 结算批次号 | String | 16 | N | 结算方式为P0：批次结算时有值，即将按指定结算批次号进行资金结算；<font color="green">示例值：100</font>;[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| constant_amt | 节假日结算手续费固定金额 | String | 15 | C | settle_cycle为D1时有值。单位元，需保留小数点后两位。不收费请填写0.00；<br>settle_cycle结算周期为D1时，遇节假日按此费率结算 ；<br/> <font color="green">示例值：1.00</font> |
| workday_fixed_ratio | 工作日结算手续费率 | String | 6 | N | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；<font color="green">示例值：0.05</font> |
| workday_constant_amt | 工作日结算手续费固定金额 | String | 15 | N | 单位元，需保留小数点后两位。不填默认为0.00；<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3899f7bc_4fac_43b7_a80e_a96df3248793-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_type | 协议类型 | String | 1 | Y | 0-电子协议 1-纸质协议 3-挂网协议；<font color="green">示例值：3</font> |
| agreement_query_url | 挂网协议查看地址 | String | 512 | N | <font color="green">示例值：示例值：https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm</font> |
| agreement_no | 协议号 | String | 64 | N | <font color="green">示例值：3245234</font> |
| agreement_model | 协议模板号 | String | 64 | C | <font color="green">示例值：202207010100001007</font> |
| agreement_name | 协议模板名称 | String | 256 | C | <font color="green">示例值：支付服务协议</font> |
| sign_date | 签约日期 | String | 8 | N | 格式：yyyyMMdd；<font color="green">示例值：20221202</font> |
| agree_begin_date | 协议开始日期 | String | 8 | N | 格式：yyyyMMdd；<font color="green">示例值：20221202</font> |
| agree_end_date | 协议结束日期 | String | 8 | N | 格式：yyyyMMdd；<font color="green">示例值：20221202</font> |
| agreement_id | 协议id | String | 32 | N | <font color="green">示例值：495603459634</font> |
| agreement_item | 协议分类 | String | 5 | N | 业务修改触发的业务分类类型；<font color="green">示例值：M0109</font> |
| con_stat | 合同状态 | String | 2 | N | 电子协议类型会返回以下值：<br/>2：创建合同异常<br/>3：待签约 <br/>4：签约中<br/>5：签约完成(电子协议只有签约完成才能做交易) <br/>6：已失效 <br/> 7：已拒签<br/> 8：签约失败<br/><font color="green">示例值：5</font> |
| <span class="extend 1f01f524_3c74_4f3d_b42b_5bb7d3a73e3d">sms_send_list</span> | 协议发送集合 | Object |  | N | jsonArray格式 |
| message_send_type | 电子协议签约短信发送标识 | String | 1 | N | 协议类型为电子，业务开通审核通过后发送协议签约短信；<br/>0：发送，默认；<br/>1：不发送；<br/><font color="green">示例值：1</font> |
| agreement_link | 协议签署链 | String | 512 | N | 电子协议时有值 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1f01f524_3c74_4f3d_b42b_5bb7d3a73e3d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sms_send_time | 协议短信发送时间 | String | 20 | N | 格式yyyy-MM-dd HH&#58;mm&#58;ss；<font color="green">示例值：2023-04-13 10&#58;11&#58;12</font> |
| sms_send_result | 协议短信发送结果 | String | 1 | N | S-成功  F-失败；<font color="green">示例值：S</font> |
| sms_receiver_owner | 协议短信接收人所属主体的名称 | String | 128 | N | <font color="green">示例值：上海汇付支付服务公司</font> |
| sms_receiver_name | 协议短信接收人姓名 | String | 64 | N | <font color="green">示例值：张三</font> |
| sms_receiver_phone | 协议短信接收人手机号码 | String | 11 | N | <font color="green">示例值：13911111111</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b51121b8_c27c_4486_bfdf_356ac107a1bc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 签约人类型 | String | 7 | Y | LEGAL-法人，对公结算或对私法人结算时可选法人签约；<br/>CONTACT-联系人，对公结算可选联系人（经办人）签约；<br/>OTHER-其他，对私非法人结算选“其他”，必须是结算人；<br/><font color="green">示例值：LEGAL</font> |
| name | 姓名 | String | 32 | N | 签约人类型=其他，有值；<font color="green">示例值：张三</font> |
| mobile_no | 手机号 | String | 11 | N | 签约人类型=法人/其他 ，有值；<font color="green">示例值：13917264536</font> |
| cert_no | 身份证 | String | 32 | N | 签约人类型=联系人/其他，有值；<font color="green">示例值：320925198512037021</font> |
| identity_front_file_id | 身份证照片-人像面 | String | 128 | N | 签约人类型=法人，法人身份证照片<br/>签约人类型=联系人，联系人身份证照片<br/>签约人类型=其他，签约人身份证照片<br/><font color="green">示例值：de2f6e1d-d9e9-3898-9b66-af2a96054193</font> |
| identity_back_file_id | 身份证照片-国徽面 | String | 128 | N | 签约人类型=法人，法人身份证照片<br/>签约人类型=联系人，联系人身份证照片<br/>签约人类型=其他，签约人身份证照片<br/><font color="green">示例值：de2f6e1d-d9e9-3898-9b66-af2a96054193</font> |
| auth_file_id | 法人授权书 | String | 128 | N | 签约人类型=联系人/其他，有值；<font color="green">示例值：de2f6e1d-d9e9-3898-9b66-af2a96054193</font> |
| email | 邮箱 | String | 32 | N | <font color="green">示例值：example@email.com</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 52584abe_c6f4_4f0b_8a85_44c8d3d1e0b6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| media_type | 运营媒介类型 | String | 2 | Y | S1-PC网站；若媒介项为PC网站：（PC网站域名、ICP备案号、ICP许可证号，测试账号、密码 ）<br/>S2-APP场景；若媒介项为APP场景：（APP名称、APP下载地址、测试账号、密码 ），若开通微信App支付，则新增app_id、app_name必填<br/>S3-小程序场景；若媒介项为小程序：（小程序名称、测试账号、密码）<br/>S4-公众号场景；若媒介项为公众号：（公众号名称、测试账号、密码）<br/>S5-其他；媒介项为其他：其他有效信息或链接地址必填<br/>线上场景时必填一项；<font color="green">示例值：S1</font> |
| media_name | 媒介名称 | String | 200 | C | PC网站域名／APP名称／小程序名称／公众号名称；<font color="green">示例值：汇付服务</font><br/>运营媒介类型为 ：S1/S2/S3/S4时，必填； |
| test_account | 测试账号 | String | 64 | Y | <font color="green">示例值：test</font> |
| test_secret | 测试密码 | String | 64 | Y | <font color="green">示例值：test</font> |
| other_info | 其他有效信息 | String | 200 | C | 其他有效信息或链接地址/APP下载地址；<br/><font color="green">示例值：http://download.huifu.com</font> |
| media_front_page | 运营媒介-首页 | String | 64 | C | 若为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%）<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| media_service_page | 运营媒介-服务/商品明细页面 | String | 64 | C | 若为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%）<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| media_order_page | 运营媒介-下单场景页面 | String | 64 | C | 若为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%）<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| media_pay_page | 运营媒介-支付页面 | String | 64 | C | 若为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%）<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| media_mer_common_flag | 媒介主体与商户主体是否一致 | String | 1 | C | Y/N；<font color="green">示例值：Y</font><br/>运营媒介为S1、S2、S3、S4且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），<br/>若不一致，则需提供ICP备案/APP/微信公众号/小程序主体与商户的使用授权或开发证明材料； |
| authorize_materials | 授权或开发证明材料 | String | 64 | C | 运营媒介为S1、S2、S3、S4且媒介主体与商户主体不一致时，且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| other_material | 微信APP补充材料 | String | 128 | C | 运营媒介为S2且开通微信下app支付时选填，具体见[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) |
| app_id | appId | String | 128 | C | 运营媒介为S2且开通微信下app支付时有 |
| app_name | appId认证主体名称 | String | 128 | C | 运营媒介为S2且开通微信下app支付时有 |
| supplement | 补充说明 | String | 512 | C | 运营媒介为S2且开通微信下app支付时有 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bceeb557_19e8_4ccf_8b4f_ae6316d7f0ea-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 支付手续费(%) | String | 17 | N | 开通余额支付时fee_amt与fee_rate必须填写一种收费方式。单位%，需保留小数点后两位，<font color="green">示例值：0.50</font>代表费率为0.5%，最低传入0.00 |
| fee_amt | 固定手续费(元) | String | 17 | N | 开通余额支付时fee_amt与fee_rate必须填写一种收费方式。单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| balance_model | 余额支付业务模式 | String | 2 | N | 2-线上（包括线上+线下）入驻商户货款（周期性结算）<br/>3-线上（包括线上+线下）营销补贴（周期性结算）<br/>4-线上（包括线上+线下）推广方（渠道/代理/个人）的服务佣金/抽成<br/>5-线上（包括线上+线下）红包发放<br/>6-线上（包括线上+线下）钱包功能<br/>7-线上（包括线上+线下）其他模式<br/>单选；<font color="green">示例值：6</font> |
| <span class="extend af060796_05fd_4384_815e_1857a99837f9">balance_pay_ext_info</span> | 余额支付情况说明 | Object |  | N | jsonObject |
| pay_mode | 余额支付模式 | String | 4 | Y | pro，lite；示例值：pro<br/>lite版不支持当日收款资金余额支付<br/><font color="green">示例值：pro</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table af060796_05fd_4384_815e_1857a99837f9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| busi_instruction | 余额支付业务模式说明 | String | 500 | N | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）<br/><font color="green">示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。</font> |
| capital_instruction | 余额支付资金流向说明 | String | 500 | N | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等），<br/><font color="green">示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。</font> |
| function_instruction | 余额支付功能开通用途说明 | String | 500 | N | 请详述所申请功能的原因、场景、涉及对象类型；<font color="green">示例值：商户给消费者发放补贴到钱包账户，用于奖励消费行为</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fa0cf9b7_f7f8_47a3_aa39_b27623071334-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_type | 业务类型 | String | 25 | Y | ONLINE_PERSON:个人网银支付，【biz_conf】中online_flag开通了才需要填； ONLINE_ENT:企业网银支付，【biz_conf】中online_flag开通了才需要填； QUICK_DEBIT:快捷借记卡支付，【biz_conf】中quick_flag开通了才需要填； QUICK_CREDIT:快捷贷记卡支付，【biz_conf】中quick_flag开通了才需要填； WAP:手机WAP支付，【biz_conf】中online_flag开通了才需要填；ONLINE_ENT_TOP_UP:B2B网银充值，【biz_conf】中online_recharge_flag开通了才需要填；ONLINE_PERSON_TOP_UP:B2C网银充值，【biz_conf】中online_recharge_flag开通了才需要填；WITHHOLD:代扣，【biz_conf】中withhold_flag开通了才需要填，示例值：ONLINE_PERSON |
| bank_id | 银行编码 | String | 8 | Y | 参考： 银行编码；示例值：01020000 |
| dc_flag | 借贷标志 | String | 1 | Y | D:借记,C:贷记 ；示例值：D |
| fix_amt | 手续费（固定/元） | String | 16 | N | 必须填写一种收费方式；保留两位小数；示例值：1.00 |
| fee_rate | 费率（%） | String | 6 | N | 必须填写一种收费方式；保留两位小数；示例值：0.38 |
| bank_name | 银行名称 | String | 50 | N | 示例值：中国工商银行上海市中山北路支行 |
| bank_short_chn | 银行中文简称 | String | 50 | N | 示例值：工行上海市中北支行 |
| stat_flag | 费率状态 | String | 1 | Y | 1开，0关；示例值：1 |
| fee_min_amt | 手续费最小值（元） | String |  | N | 必须填写一种收费方式；保留两位小数；示例值：1.00 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ce1594e2_3b10_4705_8e23_b2c79b7478f8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend fc203ab8_c2cf_4445_80b0_c4eb2742d141">wx_mer_infos</span> | 微信商户号信息 | Object |  | Y | 参见下文描述 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| fee_min_amt | 最低收取手续费（元） | String | 6 | N | 固定金额保留2位小数；大于0。需要渠道商开通此功能。<font color="green">示例值：0.38</font> |
| pay_channel_id_list | 子渠道号 | String |  | N | String集合，jsonArray格式；<font color="green">示例值：["JQF00001","JQF00002"]</font> |
| pay_scene | 支付场景 | String | 2 | Y | 参见《[微信支付场景](api_ggcsbm.md#微信支付场景)》说明；<font color="green">示例值：1</font> |
| fee_charge_type | 交易手续费收取类型 | String | 1 | Y | 1:实收,2:后收；<font color="green">示例值：1</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fc203ab8_c2cf_4445_80b0_c4eb2742d141-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_mer_code | 银联商户号 | String | 32 | N | 商户在银联开通的支付宝(或微信)商户号；<font color="green">示例值：2234544</font> |
| nucc_bank_mer_code | 网联商户号 | String | 32 | N | 商户在网联开通的支付宝(或微信)商户号 |
| pay_channel_id | 子渠道号 | String | 50 | N | <font color="green">示例值：JP00001</font> |
| is_default | 默认渠道标记 | String | 1 | N | 1：默认渠道；<font color="green">示例值：1</font> |
| sub_mer_id | 二级商户号 | String | 1 | N | <font color="green">示例值：6634423544</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8e428b1f_cc73_4636_b586_25270785ac8b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend ecd8b4e7_d863_44fe_83a4_9216eb77afbf">ali_mer_infos</span> | 支付宝商户信息 | Object |  | N |  |
| fee_rate | 手续费（%） | String |  | N | <font color="green">示例值：0.60</font> |
| fee_min_amt | 最低收取手续费（元） | String | 6 | N | 固定金额保留2位小数；大于0。需要渠道商开通此功能。<font color="green">示例值：0.38</font> |
| pay_scene | 支付场景 | String | 2 | Y | 1、线下扫码（正扫&反扫&台牌），2、线上扫码，3、非盈利费率；<font color="green">示例值：1</font> |
| fee_charge_type | 交易手续费收取类型 | String | 1 | Y | 1：实收,2：后收；<font color="green">示例值：1</font> |
| pay_channel_id_list | 子渠道号 | String |  | N | String集合；<font color="green">示例值：["JQF00001","JQF00002"]</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ecd8b4e7_d863_44fe_83a4_9216eb77afbf-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_mer_code | 银联商户号 | String | 32 | N | 商户在银联开通的支付宝(或微信)商户号；<font color="green">示例值：2234544</font> |
| nucc_bank_mer_code | 网联商户号 | String | 32 | N | 商户在网联开通的支付宝(或微信)商户号 |
| pay_channel_id | 子渠道号 | String | 50 | N | <font color="green">示例值：JP00001</font> |
| is_default | 默认渠道标记 | String | 1 | N | 1：默认渠道；<font color="green">示例值：1</font> |
| sub_mer_id | 二级商户号 | String |  | N | <font color="green">示例值：6634423544</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6bce7bb6_38bd_4a8c_a98d_a0f60d0e47b7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_mer_code | 银联商户号 | String | 18 | N | 银联报备生成的银行商户号；<font color="green">示例值：66345234544</font> |
| charge_cate_code | 银行业务手续费类型 | String | 2 | N | 01-减免类 02-优惠类 03-标准类（默认）；<font color="green">示例值：03</font> |
| debit_fee_rate | 借记卡手续费（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]； <font color="green">示例值：0.60</font> |
| debit_fee_limit | 借记卡封顶值 | String | 4 | N | 数字类型，大于0保留2位小数； <font color="green">示例值：20.00</font> |
| credit_fee_rate | 贷记卡手续费（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.90</font> |
| is_open_cloud_flag | 是否开通银联手机闪付 | String | 1 | Y | 选项：0：否 1：是。目前默认开通；<font color="green">示例值：0</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8af7c28a_9689_444a_b47b_364f2be87ea8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_mer_code | 银联商户号 | String | 18 | N | 银联报备生成的银行商户号；<font color="green">示例值：66345234544</font> |
| qr_code_info | 银联小微二维码 | String | 64 | N |  |
| fee_charge_type | 交易手续费收取类型 | String | 1 | N | 1:实收,2:后收；<font color="green">示例值：1</font> |
| credit_fee_rate_up | 贷记卡手续费1000以上（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00];<font color="green">示例值：0.60</font> |
| debit_fee_rate | 借记卡手续费（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00];<font color="green">示例值：0.60</font> |
| credit_fee_rate_down | 贷记卡手续费1000及以下（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| debit_fee_rate_up | 借记卡手续费1000以上（%） | String |  | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| debit_fee_rate_down | 借记卡手续费1000及以下（%） | String |  | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6f680f62_7fc3_4cb6_90d9_8872cba6074b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 开通状态 | String | 1 | Y | 0:关闭 1:开通；<font color="green">示例值：1</font> |
| out_order_auto_acct_flag | 全域资金自动入账开关 | String | 1 | Y | 开通、关闭自动入账功能；0:关闭 1:开通；<font color="green">示例值：1</font><br/>关闭自动入账需要[处理银行来账通知](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_lztz)，并调用[汇付入账确认接口](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_yhskfk)来确认入账。 |
| batch_auto_acct_flag | 批量入账开关 | String | 1 | N | 0:关闭（默认）；单笔入账模式； <br/>1:开通；开通批量入账；仅支持自动入账模式；<font color="green">示例值：0</font> |
| batch_no | 批次入账时间 | String | 20 | C | 10:00-10点批次入账<br/>16:00-16点批次入账</br>开通批次入账时必填 ，多个批次使用逗号分隔；<font color="green">示例值：10:00,16:00</font> |
| fee_rate | 支付手续费(%) | String | 6 | N | 支持两位小数；<font color="green">示例值：0.45</font>；fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| fee_min_amt | 手续费最小值(元) | String | 6 | N | 支付手续费最小值，支持两位小数；<font color="green">示例值：1.00</font></br>fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| out_fee_flag | 交易手续费外扣标记 | String | 1 | N | 1：外扣，2：内扣；（默认2内扣）；<font color="green">示例值：2</font> |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | <font color="green">示例值：6666000109812123</font> |
| out_fee_acctid | 交易手续费外扣子账户号 | String | 16 | N | <font color="green">示例值：F00598600</font> |
| account_name | 账户名 | String | 128 | N | 全域资金管理配置功能涉及字段；<font color="green">示例值：张三收款户</font> |
| electron_account | 电子账号 | String | 32 | N | 全域资金管理配置功能开通的电子账号；<font color="green">示例值：</font> |
| <span class="extend dfc3d5ee_a709_4250_bdeb_83f4c1d96f3e">out_order_acct_card</span> | 全域资金开户使用的银行卡信息 | Object |  | N | jsonObject字符串 |
| platform_mer_id | 全域资金平台商户ID | String | 32 | Y | 全域资金平台商户ID；<font color="green">示例值：XXXXXXXXX</font>； |
| business_model | 全域支付业务模式 | String | 20 | N | acquiringMode：收单模式，默认；rechargeMode：充值模式，<br/><font color="green">示例值：acquiringMode</font> |
| other_payment_institutions_pic | 商户与其他支付机构签署的收单协议或证明材料 | String | 64 | N | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table dfc3d5ee_a709_4250_bdeb_83f4c1d96f3e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | N | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | N | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font> |
| bank_code | 银行编码 | String | 8 | N | 对公时根据支行编码获取总行编码；参考[银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font> |
| branch_code | 支行联行号 | String | 12 | N | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | N | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| card_name | 结算账户名 | String | 128 | Y | 银行卡对应的户名；<font color="green">示例值：上海汇付支付有限公司</font> |
| card_no | 银行卡号 | String | 32 | Y | <font color="green">示例值：98140008801800008888</font> |
| card_type | 卡类型 | String | 1 | Y | 0:对公 1:对私<font color="green">示例值：01</font> |
| cert_type | 持卡人证件类型 | String | 2 | N | 00:身份证<font color="green">示例值：00</font>； |
| cert_begin_date | 持卡人证件有效期（起始） | String | 8 | N | 格式：yyyyMMdd，<font color="green">示例值：20210830</font> |
| cert_end_date | 持卡人证件有效期（截止） | String | 8 | N | 格式：yyyyMMdd；<font color="green">示例值：20210830</font> |
| cert_no | 持卡人证件号码 | String | 32 | N | <font color="green">示例值：310112200001018888</font> |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | N | 1:长期有效 0:非长期有效；<font color="green">示例值：0</font> |
| mp | 银行卡绑定手机号 | String | 11 | Y | <font color="green">示例值：18611111111</font> |
| open_licence_no | 开户许可证核准号 | String | 32 | N | <font color="green">示例值：J2900123456789</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 660caa09_1dc5_45bf_beb1_5ffaa44b146c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 支付手续费(%) | String | 9 | N | 支付手续费(%) 支持两位小数 fee_rate与fee_fix_amt 不能同时为空；示例值：0.50代表费率为0.5% |
| fee_fix_amt | 支付固定手续费(元) | String | 9 | N | 支付固定手续费(元)支持两位小数 fee_rate与fee_fix_amt 不能同时为空；示例值：1.50 注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额\fee_rate |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 ，示例值：1 优先级高于相同名称的公共参数； |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时有，示例值：6666000123123123 优先级高于相同名称的公共参数； |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01 优先级高于相同名称的公共参数； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b578f1f6_4598_411f_a145_8859d2aaabe4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_mch_id | 微信子商户号 | String | 32 | Y | 微信支付分配的子商户号；<font color="green">示例值：1632157057</font> |
| <span class="extend ba75342f_93ff_4665_8593_3083b5269894">wx_zl_pay_conf_list</span> | 配置集合 | Object | 512 | Y | jsonArray |
| <span class="extend 7c7bb97c_03b1_4cdd_aba8_9d6a8fc4345a">contact_info</span> | 联系人信息 | Object |  | Y | jsonObject 对象。按提交时的信息进行返回。 |
| <span class="extend f6e7a5d3_2043_49a6_a1d6_26676eb969a0">sales_info</span> | 经营场景信息 | Object |  | Y | json 对象 |
| <span class="extend ffe38042_4eec_4c67_bba3_43dda3c18fb1">wx_card_info</span> | 银行账户信息 | Object |  | N | json 对象， |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ba75342f_93ff_4665_8593_3083b5269894-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| service_code | 申请服务 | String | 16 | Y | JSAPI-公众号，APPLET-小程序；<font color="green">示例值：JSAPI</font> |
| sub_app_id | 功能服务appid | String | 32 | Y | 子商户的公众号、小程序ID；<font color="green">示例值：wx51aa91a575359ff5</font> |
| switch_state | 功能开关 | String | 1 | Y | 0-关闭，1-打开；<font color="green">示例值：1</font> |
| fee_rate | 功能费率(%) | String | 6 | Y | 保留两位小数。<font color="green">示例值：0.60</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7c7bb97c_03b1_4cdd_aba8_9d6a8fc4345a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| contact_type | 联系人类型 | String | 1 | Y | 1： 法人；2：经办人；<font color="green">示例值：1</font> |
| contact_name | 联系人姓名 | String | 128 | C | 联系人类型为经办人时有值；<font color="green">示例值：张三</font> |
| cert_type | 联系人证件类型 | String | 2 | C | 联系人类型为经办人时有值；<br>00：身份证<br>01:护照<br>11：港澳台同胞通行证<br>12：外国人居留证<br>13：港澳居民证<br>14：台湾居民证<br/><font color="green">示例值：00</font>； |
| contact_cert_no | 联系人证件号码 | String | 18 | C | 联系人类型为经办人时有值；<font color="green">示例值：32090297512026402</font> |
| contact_mobile_no | 联系人手机号 | String | 11 | Y | <font color="green">示例值：13911111111</font> |
| contact_email | 联系人电子邮箱 | String | 40 | Y | <font color="green">示例值：carl.chen@huifu.com</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f6e7a5d3_2043_49a6_a1d6_26676eb969a0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sales_scenes_type | 经营场景类型 | String | 256 | Y | 多个以英文逗号分割，至少要有一个<br>线下门店：SALES_SCENES_STORE<br>公众号：SALES_SCENES_MP<br>小程序：SALES_SCENES_MINI_PROGRAM<br>互联网：SALES_SCENES_WEB<br>APP：SALES_SCENES_APP<br>企业微信：SALES_SCENES_WEWORK<br/><font color="green">示例值：SALES_SCENES_WEWORK</font> |
| fee_rate | 功能费率 | String | 6 | C | 仅支持渠道商传入该字段。<font color="green">示例值：0.06</font><br>平台商户为子商户开通微信直连支付时，不支持该字段，取平台商户费率上送微信。 |
| biz_sub_jsapi_app_id | 线下场所对应的商家公众号APPID | String | 256 | C | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。<font color="green">示例值：wx51aa91a575359ff5</font> |
| biz_sub_mini_app_id | 线下场所对应的商家小程序APPID | String | 256 | C | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。<font color="green">示例值：wxea9c30a90fs8d3fe</font> |
| jsapi_app_id | 服务商公众号 ID | String | 256 | C | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| jsapi_sub_app_id | 商家公众号APPID | String | 256 | C | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。<font color="green">示例值：wxea9c30a90fs8d3fe</font> |
| mini_app_id | 服务商小程序APPID | String | 256 | C | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| mini_sub_app_id | 商家小程序APPID | String | 256 | C | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| app_app_id | 服务商应用APPID | String | 256 | C | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| app_sub_app_id | 商家应用APPID | String | 256 | C | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| web_app_id | 互联网网站对应的商家APPID | String | 256 | C | 开通互联网场景时填入；<font color="green">示例值：wx51aa91a575359ff5</font> |
| sub_corp_id | 商家企业微信CorpID | String | 256 | C | 开通企业微信场景时填入；<font color="green">示例值：xxxxx</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ffe38042_4eec_4c67_bba3_43dda3c18fb1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 账户类型 | String | 1 | Y | 0：对公银行账户<br>1：经营者个人银行卡；<font color="green">示例值：0</font> |
| card_name | 开户名称 | String | 128 | Y | 选择“经营者个人银行卡”时，开户名称必须与“经营者证件姓名”一致。选择“对公银行账户”时，开户名称必须与营业执照上的“商户名称”一致。<br/><font color="green">示例值：张三</font> |
| bank_code | 开户银行 | String | 8 | Y | 客户按汇付银行编码上送；<font color="green">示例值：01020000</font> |
| prov_id | 开户银行省编码 | String | 6 | Y | 按汇付的省市编码；<font color="green">示例值：310000</font> |
| area_id | 开户银行市编码 | String | 6 | Y | <font color="green">示例值：310100</font> |
| branch_code | 开户银行联行号 | String | 20 | C | 开户银行联行号与开户银行全称（含支行)二选一；<font color="green">示例值：102290026507</font> |
| branch_name | 开户银行全称（含支行) | String | 128 | C | 开户银行联行号与开户银行全称（含支行)二选一；<font color="green">示例值：中国工商银行股份有限公司上海市中山北路支行</font> |
| card_no | 银行账号 | String | 30 | Y | <font color="green">示例值：1001265009300682579</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8ea49697_3b3f_48f8_a24e_db010f0d7d8c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| mer_code | 支付宝商户号 | String | 32 | N | <font color="green">示例值：2088031396541893</font> |
| mer_app_id | 应用ID | String | 32 | N | <font color="green">示例值：2022002178643452</font> |
| apply_type | 申请类型 | String | 32 | Y | FACE_TO_FACE：当面付；<font color="green">示例值：FACE_TO_FACE</font> |
| contact_name | 联系人姓名 | String | 64 | N | 支付宝联系人信息，不传取商户的联系人信息；<br/><font color="green">示例值：张三</font> |
| contact_mobile_no | 联系人手机号 | String | 11 | N | 支付宝联系人信息，不传取商户的联系人信息；<br/><font color="green">示例值：13911111111</font> |
| contact_email | 联系人电子邮箱 | String | 40 | N | 支付宝联系人信息，不传取商户的联系人信息；<br/><font color="green">示例值：carl.chen@huifu.com</font> |
| account | 商户支付宝账号 | String | 128 | Y | 商户登录支付宝控台的账号；<font color="green">示例值：zhangsan</font> |
| fee_rate | 服务费率 | String | 6 | C | 仅支持渠道商。平台商户调用不支持该字段<br>服务费率（%），0.38~3之间，精确到0.01。<font color="green">示例值：0.06</font> |
| license_code | 营业执照编号 | String | 20 | N | 工商营业执照编号，<font color="green">示例值：92650109MA79R8E308</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a634e58d_8b3f_42a5_b9f8_de8bfb15dc72-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_id | 文件ID | String | 64 | Y | <font color="green">示例值：e91a6ed5-d258-3ed9-bf52-64ff2b0f2bae</font> |
| file_name | 文件名称 | String | 32 | N | <font color="green">示例值：00.jpg</font> |
| file_type | 文件类型 | String | 32 | Y | <font color="green">示例值：F24</font> |
| file_url | 文件地址 | String | 128 | Y | <font color="green">示例值：https://jfile.cloudpnr.com/app-e8f8442e-4e68-4a6c-b51b-8ae9647f22be/default_iOS/156b39ae-ef13-11ed-ac53-1111ac110003.jpg</font> |
| update_time | 更新时间 | String | 14 | Y | 格式：YYYYMMDDhhmmss<font color="green">示例值：20230512132234</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table de0048b1_5426_49a4_9685_e56d649948f1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 79e6f48d_03ec_46e6_bb46_a181d70934f3">ali_conf_list</span> | 支付宝配置对象 | Object |  | N | jsonArray格式 |
| <span class="extend e1d6c45a_9d8c_4152_b938_a6fc6249b515">wx_conf_list</span> | 微信配置对象 | Object |  | N | jsonArray格式 |
| <span class="extend 867949e9_14b2_422f_be4e_0b76daa297f0">union_conf_list</span> | 银联二维码配置对象 | Object |  | N | jsonArray格式 |
| <span class="extend db83b5db_a56b_46bc_8a8b_88f276e003a5">bank_card_config</span> | 银联卡配置对象 | Object |  | N | jsonObject格式 |
| <span class="extend bc7fb2ce_2554_4867_b394_aa2c3f6ea4fa">split_config</span> | 分账配置对象 | Object |  | N | jsonObject格式 |
| <span class="extend 266a8bae_0d8b_4230_ab81_adde5a6f552c">wx_zl_conf_list</span> | 微信直连配置对象 | Object |  | N | jsonArray格式 |
| <span class="extend cfe8f056_32af_49c8_a710_84ae64c41db3">ali_zl_conf</span> | 支付宝直连配置对象 | Object |  | N | jsonObject格式 |
| <span class="extend 5fbbd6c4_ac4a_4b2b_af81_6a93af2a951d">online_fee_conf_list</span> | 线上配置对象 | Object |  | N | jsonArray格式 |
| <span class="extend eba78873_90bb_4b9a_9900_e7943012d159">balance_pay_config</span> | 余额支付配置对象 | Object |  | N | jsonObject格式 |
| <span class="extend 79e2f245_2331_4392_ab05_3cc12dd37f1d">combine_pay_config</span> | 补贴支付配置对象 | Object |  | N | jsonObject格式 |
| <span class="extend 5685fec0_ddf2_4fed_989c_6dc4d8d9bfd4">bank_big_amt_pay_config</span> | 银行大额转账配置对象 | Object |  | N | jsonObject格式 |
| <span class="extend a20116e8_99a2_4c52_b2ba_1677b6f15f9c">out_order_funds_config</span> | 全域资金管理配置（华通）对象 | Object |  | N | jsonObject格式 |
| <span class="extend 03697988_71e4_4f3d_8956_ed5fa854d106">out_order_funds_su_shang_config</span> | 全域资金管理配置(苏商)对象 | Object |  | N | jsonObject格式 |
| <span class="extend 089b3977_9fd6_4442_97b4_9125ab276264">out_order_funds_new_net_config</span> | 全域资金管理配置(新网)对象 | Object |  | N | jsonObject格式 |
| <span class="extend f09bbfec_657e_4735_8178_7bbe43ef78f9">settle_config_list</span> | 结算配置对象 | Object |  | N | jsonArray格式 |
| <span class="extend 6463722b_a17d_4c5f_9ed7_0c5a16b62872">cash_config_list</span> | 取现配置对象 | Object |  | N | jsonArray格式 |
| <span class="extend aee93a4a_80b5_42f5_ade4_67047bff4e7c">out_fee_config</span> | 外扣配置对象 | Object |  | N | jsonArray字符串 |
| alipay_pre_auth_flag | 是否开通支付宝预授权 | String | 1 | N | 支付宝预授权开通；Y：是，N：否； |
| wechatpay_pre_auth_flag | 开通微信预授权 | String | 1 | N | 微信预授权开通；Y：是，N：否； |
| mer_timing_settle_flag | 是否开通商户定时结算 | String | 1 | N | 定时结算开通；Y：是，N：否； |
| mer_prior_settle_flag | 是否开通商户优先结算 | String | 1 | N | 优先结算开通；Y：是，N：否； |
| use_upper_mer_auth_flag | 是否使用上级商户经营信息 | String | 1 | N | 开通下级商户时支持复用上级的经营信息；Y：是，N：否； |
| use_upper_mer_at_trans_flag | 是否使用上级商户号发起AT交易 | String | 1 | N | 开通下级商户时支持复用上级的微信、支付宝商户号信息；Y：是，N：否； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 79e6f48d_03ec_46e6_bb46_a181d70934f3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1、线下扫码（正扫&反扫&台牌），2、线上扫码，示例值：1 |
| fee_rate | 手续费 | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通该业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e1d6c45a_9d8c_4152_b938_a6fc6249b515-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1：线下反扫<br>2：线下公众号<br>3：线下小程序<br>4：线上公众号<br>5：线上小程序<br>12：线上反扫<br/>示例值：1 |
| fee_rate | 手续费 | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通该场景业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 867949e9_14b2_422f_be4e_0b76daa297f0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| charge_cate_code | 银联业务手续费类型 | String | 2 | N | 03-标准类 小微商户仅有03 标准类 <br>04-线上费率（银联二维码线上）<br>默认03标志类 |
| open_flag | 允许开通银联二维码业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
| debit_fee_rate_up | 借记卡手续费1000以上（%） | String | 9 | Y | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：0.60</font> |
| debit_fee_limit_up | 借记卡封顶1000以上 | String | 9 | N | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：0.60</font> |
| debit_fee_rate_down | 借记卡手续费1000以下（%） | String | 9 | Y | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：0.38</font> |
| debit_fee_limit_down | 借记卡封顶1000以下 | String | 9 | N | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：18.00</font> |
| credit_fee_rate_up | 贷记卡手续费1000以上（%） | String | 9 | Y | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：0.60</font> |
| credit_fee_rate_down | 银联二维码业务贷记卡手续费1000以下（%） | String | 9 | Y | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：0.60</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table db83b5db_a56b_46bc_8a8b_88f276e003a5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| debit_fee_rate | 借记卡手续费（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]； 示例值：0.60 |
| debit_fee_limit | 借记卡封顶值 | String | 9 | N | 数字类型，大于0保留2位小数； 示例值：20.00 |
| credit_fee_rate | 贷记卡手续费（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.90 |
| open_flag | 允许开通银行卡业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
| cloud_debit_fee_rate_up | 银联手机闪付借记卡手续费1000以上（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| cloud_debit_fee_limit_up | 银联手机闪付借记卡封顶1000以上（元） | String | 9 | N | 数字类型，大于0保留2位小数；示例值：20.00 |
| cloud_credit_fee_rate_up | 银联手机闪付贷记卡手续费1000以上（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| cloud_debit_fee_rate_down | 银联手机闪付借记卡手续费1000以下（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| cloud_debit_fee_limit_down | 银联手机闪付借记卡封顶1000以下（元） | String | 9 | N | 数字类型，大于0保留2位小数；示例值：20.00 |
| cloud_credit_fee_rate_down | 银联手机闪付贷记卡手续费1000以下（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bc7fb2ce_2554_4867_b394_aa2c3f6ea4fa-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | N | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通分账业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 266a8bae_0d8b_4230_ab81_adde5a6f552c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1、微信直连小程序<br>2、微信直连公众号<br>3、微信直连H5<br>示例值：1 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通微信直连业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table cfe8f056_32af_49c8_a710_84ae64c41db3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通支付宝直连业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5fbbd6c4_ac4a_4b2b_af81_6a93af2a951d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bus_type | 业务类型 | String | 2 | Y | 1.网银支付， 2.快捷支付， 3.手机WAP支付；4：B2B网银充值
5：B2C网银充值，6：代扣支付 示例值：1 |
| dc_flag | 借贷记标识 | String | 2 | Y | D:借记,C:贷记；B2B网银填写D；示例值：D |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| bank_code | 银行号 | String | 8 | Y | 8位银行号 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通线上支付业务	 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table eba78873_90bb_4b9a_9900_e7943012d159-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通余额支付业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 79e2f245_2331_4392_ab05_3cc12dd37f1d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通补贴支付业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5685fec0_ddf2_4fed_989c_6dc4d8d9bfd4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通大额转账业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a20116e8_99a2_4c52_b2ba_1677b6f15f9c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_fee_fix_amt | 开户手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通全域资金（华通）业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 03697988_71e4_4f3d_8956_ed5fa854d106-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| fee_min_amt | 保底手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| public_fee_fix_amt | 对公固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| private_fee_fix_amt | 对私固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| open_flag | 允许开通全域资金业务(苏商) | String | 1 | Y | Y：是，N：否，<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 089b3977_9fd6_4442_97b4_9125ab276264-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| fee_min_amt | 保底手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| public_fee_fix_amt | 对公固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| private_fee_fix_amt | 对私固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| open_flag | 允许开通全域资金业务(新网) | String | 1 | Y | Y：是，N：否，<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f09bbfec_657e_4735_8178_7bbe43ef78f9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bus_type | 业务类型 | String | 2 | Y | D1：下个自然日到账，<br>T1：下个工作日到账；<br>TS：笔笔到账<br>示例值：T1 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通结算配置 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6463722b_a17d_4c5f_9ed7_0c5a16b62872-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bus_type | 业务类型 | String | 2 | Y | D0：当日到账；当日交易资金当天可取现到账；<br>T1：下个工作日到账;<br>D1：下个自然日到账;<br>DM：当日到账；到账资金不包括当天的交易资金；<br>示例值：T1 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通取现配置 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table aee93a4a_80b5_42f5_ade4_67047bff4e7c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_out_fee_flag | 支持结算手续费外扣 | String | 1 | Y | Y：是，N：否，示例值：Y |
| trans_fee_out_flag | 支持交易手续费外扣 | String | 1 | Y | Y：是，N：否，示例值：Y |
| cash_out_fee_flag | 支持取现手续费外扣 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d75ac4cd_ae7b_49a5_baa5_accfc15c14dc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子账户开关 | String | 1 | Y | 电子账户开通总开关；0:关闭 1:开通；<font color="green">示例值：1</font> |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家；<font color="green">示例值：01</font> |
| cash_fee_party | 电子账户提现手续费承担方 | String | 1 | Y | 1:总部 2:其他；<font color="green">示例值：1</font> |
| scene | 场景类型 | String | 3 | Y | 必填，与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；<font color="green">示例值：001</font> |
| role_type | 角色类型 | String | 6 | Y | 角色编号必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；<font color="green">示例值：001001</font> |
| <span class="extend 5c268755_ec81_4435_bd7d_bb47914f5583">elec_card_list</span> | 银行卡信息 | Object |  | N | jsonArray字符串 |
| bank_status | 电子账户开通状态 | String | 1 | Y | S：成功 F：失败；<font color="green">示例值：S</font> |
| bank_message | 银行信息 | String | 512 | Y | 示例值：成功 |
| merchant_id | 银行会员编号 | String | 15 | N | <font color="green">示例值：J00000000000001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5c268755_ec81_4435_bd7d_bb47914f5583-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| area_id | 银行所在市 | String | 6 | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)示例值：310100 |
| bank_code | 银行编码 | String | 8 | Y | [参考银行编码；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)示例值：01020000 |
| bank_name | 银行名称 | String | 64 | Y | 示例值：中国工商银行 |
| branch_code | 支行联行号 | String | 12 | Y | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| branch_name | 支行名称 | String | 64 | Y | 示例值：中国工商银行上海市中山北路支行 |
| card_name | 结算账户名 | String | 128 | Y | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| card_no | 银行卡号 | String | 32 | Y | 示例值：98140008801800008888 |
| card_type | 卡类型 | String | 1 | Y | 0:对公 1:对私法人 |
| default_cash_flag | 默认卡标识 | String | 1 | N | 0：非默认卡 1：默认卡 |
| token_no | 卡序列号 | String | 20 | N |  |
| mp | 银行绑定手机号 | String | 11 | N | 示例值：13911111111 |
| auth_version | 用户授权协议版本号 | String | 64 | N | 示例值：43563223 |
| auth_no | 用户授权协议号 | String | 64 | N | 示例值：654745222213 |
| status | 卡状态 | String | 1 | Y | 绑卡状态，:N-正常，C-关闭，D-注销；示例值：N |
| bind_card_msg | 绑卡返回描述 | String | 256 | Y | 示例值：成功 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table df1962ce_4a44_4db3_9239_59ddec793412-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| open_tax_flag | 是否开通灵活用工 | String | 1 | N | Y:开通, N或空:不开通；<font color="green">示例值：Y</font> |
| open_tax_state | 灵活用工开户状态 | String | 1 | N | 1-待开户，2 开户成功待签约，3-开户失败， 4-签约成功， 5-签约失败；<font color="green">示例值：2</font> |
| open_tax_state_desc | 灵活用工开户状态描述 | String | 256 | N | <font color="green">示例值：签约成功</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b14d6d3b_aca5_48cf_82b3_d43534f1a24c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| rule_origin | 分账规则来源 | String | 2 | Y | 01 接口发起 02页面配置；<font color="green">示例值：01</font> |
| repeal_flag | 分账是否支持撤销交易 | String | 1 | Y | Y：支持，N：不支持；<font color="green">示例值：Y</font> |
| refund_flag | 分账是否支持退货交易 | String | 1 | Y | Y：支持，N：不支持；<font color="green">示例值：Y</font> |
| div_flag | 分账开关 | String | 1 | Y | Y：开，N：关；<font color="green">示例值：Y</font> |
| apply_ratio | 最大分账比例% | Number | 9 | Y | 0-100 的数值，支持两位小数; <font color="green">示例值：20.00</font> |
| <span class="extend 5951e5d7_584d_4527_88d0_cb090dea73f9">acct_split_bunch_list</span> | 分账明细 | Array |  | N | jsonArray格式；分账规则来源选择平台配置时必填,jsonObject字符串 |
| out_fee_flag | 交易手续费外扣开关 | String | 1 | N | 1:外扣 2:内扣（默认）；<font color="green">示例值：1</font> |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户(默认)，02-现金户，05-充值户；<font color="green">示例值：01</font> |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | 选择手续费外扣时必填；<font color="green">示例值：</font> |
| split_fee_rate | 手续费% | String | 9 | N | 百分比，支持两位小数；<font color="green">示例值：1.00</font> |
| per_amt | 固定手续费 | String | 9 | N | 单位元，支持小数点后两位；<font color="green">示例值：1.00</font> |
| scene | 分账模式 | String | 2 | Y | 00-其他<br>01-医美医院分账<br>A1- 教培机构分账<br>A2-公办/民办学校分账<br>A3-医美渠道独立收款分账<br>A4-线上供应商货款<br>A5-线上推广方（渠道/代理/个人）的服务佣金/抽成<br>A7-入驻商户货款<br>A8-线下供应商货款<br>A9-线下推广方<br>A10-个人与合作方分账<br>单选；<font color="green">示例值：A9</font> |
| <span class="extend d57e4038_50f1_4ac3_a259_28c56dd10d2e">split_ext_info</span> | 业务情况说明 | Object | 128 | N | jsonObject；分账模式选择则其它，分账比例20%以上必填； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5951e5d7_584d_4527_88d0_cb090dea73f9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 分账比例 | String | 9 | N | 百分比支持两位小数，<font color="green">示例值：0.20</font> |
| huifu_id | 汇付Id | String | 18 | N | <font color="green">示例值：6666000104778898</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d57e4038_50f1_4ac3_a259_28c56dd10d2e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| busi_instruction | 业务模式说明 | String | 500 | Y | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）。最大500个汉字，必填<br/><font color="green">示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。</font> |
| capital_instruction | 资金流向说明 | String | 500 | Y | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等）。最大500个汉字，必填<br/><font color="green">示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。</font> |
| function_instruction | 功能开通用途说明 | String | 500 | Y | 请详述所申请功能的原因、场景、涉及对象类型。最大500个汉字，必填<br/><font color="green">示例值：企业工资代发</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f2c26e03_00b1_44ee_8069_4ba66b5b289b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| share_holder_id | 股东编号 | String | 32 | N | 修改时必填；<font color="green">示例值：</font> |
| name | 股东姓名 | String | 32 | Y | <font color="green">示例值：张三</font> |
| cert_type | 股东证件类型 | String | 2 | Y | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》；支持00~11，以及12:营业执照；<font color="green">示例值：12</font> |
| cert_no | 股东证件号码 | String | 32 | Y | <font color="green">示例值：320926198512025014</font> |
| cert_validity_type | 股东证件有效期类型 | String | 1 | Y | 1:长期有效 0:非长期有效；<font color="green">示例值：1</font> |
| cert_begin_date | 股东证件有效期起始日 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20201223</font> |
| cert_end_date | 股东证件有效期到期日 | String | 8 | N | 格式yyyyMMdd; 非长期有效时必填；<font color="green">示例值：20301223</font> |
| state | 股东状态 | String | 1 | N | 1:有效 0:无效；<font color="green">示例值：1</font> |
| mobile_no | 股东手机号 | String | 11 | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4527a325_62a0_4d51_8253_8c0419c65f9c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 状态开关 | String | 1 | N | 0-关闭; 1-开通, 为空默认开通；<font color="green">示例值：1</font> |
| debit_fee_rate | 借记手续费（%） | String | 6 | C | 借记卡费率与贷记卡费率不能同时为空;<br>保留2位小数，最大值100.00，最小值0.00；<font color="green">示例值：0.02</font> |
| credit_fee_rate | 贷记手续费（%） | String | 6 | C | 借记卡费率与贷记卡费率不能同时为空;<br>保留2位小数，最大值100.00，最小值0.00；<font color="green">示例值：0.06</font> |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：1</font> <br/>如果不为空，则out_fee_acct_type，out_fee_huifuid，out_fee_flag取单独配置，否则取公共配置； |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时必填；<font color="green">示例值：6666000123123123</font> |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户，02-现金户，05-充值户，09-营销户；不填默认01；<font color="green">示例值：01</font> |
| fee_charge_type | 交易手续费收取类型 | String | 1 | N | 1:实收 2:后收；<font color="green">示例值：1</font> |
| cloud_quick_pass_secret_free_flag | 云闪付免密支付开通标识 | String | 1 | N | Y-开通/N-关闭 ；<font color="green">示例值：Y</font>； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9926e0a8_41a0_4f92_b3ef_e39a5802e264-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 开通状态 | String | 1 | N | 1:是 0:否, 为空默认开；<font color="green">示例值：1</font> |
| surrogate_type | 代发业务类型 | String | 2 | Y | D0:当日到账；<br>T1:下个工作日到账;<br>D1:下个自然日到账;<br><font color="green">示例值：T1</font> |
| fix_amt | 手续费（固定/元） | String | 17 | C | 手续费（固定/元），保留小数点后两位；fee_formula_type为05，06时必填 <font color="green">示例值：1.00</font> |
| fee_rate | 手续费（百分比/%） | String | 6 | C | 手续费（百分比/%），保留小数点后两位；取值范围[0.00,100.00]；fee_formula_type为01，02，03，06时必填 <font color="green">示例值：0.05</font> |
| out_fee_flag | 是否交手续费外扣标记 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）<br>优先级高于相同名称的公共参数；<font color="green">示例值：1</font> |
| out_fee_acct_type | 交易手续费外扣时账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，<font color="green">示例值：01</font><br>优先级高于相同名称的公共参数； |
| out_fee_huifu_id | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时必填，<font color="green">示例值：6666000123123123<br>优先级高于相同名称的公共参数； |
| surrogate_private_flag | 是否允许对私代发 | String | 1 | N | 是否允许代发卡为对私类型<br>Y:允许 N:不允许；<font color="green">示例值：Y</font> |
| fee_formula_type | 代发手续费计费模式 | String |  | N | 01: 百分比手续费，无封顶值或保底值<br/>02: 百分比手续费，有保底值<br/>03: 百分比手续费，有封顶值<br/>05: 固定手续费 <br/>06: 固定手续费+百分比手续费<br/>为空默认06 <font color="green">示例值：06</font> |
| fee_max_amt | 手续费封顶值（固定/元） | String | 17 | C | 手续费封顶值（固定/元），保留小数点后两位；fee_formula_type为03时必填 <font color="green">示例值：100.00</font> |
| fee_min_amt | 手续费保底值（固定/元） | String | 17 | C | 手续费保底值（固定/元），保留小数点后两位；fee_formula_type为02时必填 <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fed0e7bc_6b1e_49c2_9c16_3df3afe350bd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 55c7cda4_7012_426f_8063_511fe2c35a72">large_amt_pay_config_info_list</span> | 大额支付配置列表 | Object |  | N | 大额支付配置列表，jsonArray格式 |
| out_fee_flag | 交易手续费外扣标记 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：1</font> |
| out_fee_huifu_id | 交易手续费外扣huifuId | String | 18 | C | 交易手续费外扣时必填；<font color="green">示例值：6666000108854952</font> |
| out_fee_acct_id | 交易手续费外扣账户号 | String | 16 | C | 交易手续费外扣时必填；<font color="green">示例值：F00598602</font> |
| mer_payer_card_type | 商户付款方卡类型 | String | 10 | N | CORPORATE-对公,PRIVATE-对私,ALL-全部，默认全部<br><font color="green">示例值：ALL</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 55c7cda4_7012_426f_8063_511fe2c35a72-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 功能开关 | String | 1 | N | 1:开通 0:关闭 默认：1；<font color="green">示例值：1</font> |
| business_model | 大额支付业务模式 | String | 15 | Y | 大额支付业务模式 bank：银行模式 provisions：备付金模式；<font color="green">示例值：bank</font> |
| fee_rate | 费率（%） | String | 6 | C | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；<font color="green">示例值：1.00</font> |
| fee_fix_amt | 交易手续费（固定/元） | String | 9 | C | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；<font color="green">示例值：10.00</font> |
| biz_type | 大额调账标识申请类型 | String | 2 | N | 01-四要素，05-三要素；[订单匹配的要素信息](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_ddppys)；<font color="green">示例值：05</font> |
| mer_same_card_recharge_flag | 是否允许绑卡支付 | String | 1 | N | Y-开通/N-关闭，备付金模式时，支持传入；备付金模式银行卡绑定支付权限；<font color="green">示例值：Y</font> |
| allow_user_deposit_flag | 是否允许用户入账 | String | 1 | N | Y-开通/N-关闭 ；默认为N；<font color="green">示例值：Y</font> |
| provisions_auto_refund_flag | 备付金固定账号模式自动退款 | String | 1 | N | Y-开通/N-关闭 ；<font color="green">示例值：Y</font>；该配置仅在开通大额支付备付金绑卡模式时生效 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5d064fad_c285_4f15_8247_b3fe4a538681-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agent_recheck_flag | 代发复核开关 | String | 1 | N | Y:是 N:否（为空默认未开通） ；<font color="green">示例值：Y</font> |
| agent_recheck_huifu_id | 复核授权商户号 | String | 18 | N | 复核授权商户号只能填当前商户主体或总部商户号 |
| agent_recheck_type | 复核类型 | String | 1 | N | A:复核  B:短信验证 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 47e44a99_28da_477d_9127_0988968eb991-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 佣金收取手续费率 | String |  | Y |  |
| lla_withhold_flag | 本地生活配置开关 | String |  | Y | Y:开通,N:关闭；示例值：N |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7c4f50ed_30b4_41a1_b2a8_4745331ec256-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_type | 账户类型 | String | 1 | N | 2:银行账户 |
| <span class="extend 267b8994_3ee0_4577_95c4_f82ced5e9495">jxf_bank_info</span> | 银行账户信息 | Object |  | N | jsonObject字符串 |
| bank_resp_desc | 通道返回描述 | String | 128 | N | 示例：成功 |
| bank_status | 业务开通状态 | String | 1 | N | S：成功 P:处理中 F:失败 |
| open_flag | 开通状态 | String | 1 | N | N-关闭 Y-开通 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 267b8994_3ee0_4577_95c4_f82ced5e9495-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| user_name | 操作人姓名 | String | 16 | N | 示例：张三 |
| operator_phone | 操作人手机号 | String | 11 | N | 示例：13333333333 |
| acct_type | 付款方账户类型 | String | 2 | N | 00：单位结算卡，不填默认单位结算卡 |
| acct_no | 付款方账号 | String | 50 | N | 示例：6212149999831234577 |
| acct_name | 付款方账户名称 | String | 25 | N | 示例：上海汇付支付有限公司 |
| bank_branch_code | 开户行联行号 | String | 50 | N | 示例：991290000099 |
| bank_branch_name | 开户行行名 | String | 25 | N | 示例：中国银行 |
| sign_start_date | 签约申请生效日期 | String | 8 | N | 示例：20251219 |
| sign_end_date | 签约申请失效日期 | String | 8 | N | 示例：20261219 |
| remark | 附言 | String | 128 | N | 示例：附言 |
| org_code | 机构编码 | String | 64 | N | 示例：12133 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9957cd9d_28f1_4c68_9bf8_c9c9bb50ea5a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| merge_pay_flag | 合单支付开关 | String |  | Y | 合单支付开关 Y：开通 N：关闭 |
| <span class="extend 275d0af3_d1c8_4e21_ad83_786493780abf">merge_pay_config</span> | 合单支付配置 | Object |  | C | 合单支付配置 （当合单支付开关为开时必填） |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 275d0af3_d1c8_4e21_ad83_786493780abf-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| merge_pay_mode | 合单支付模式 | String |  | Y | 1:电商 2:加油站 3:停车场 4:物业 5:休闲娱乐 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2651e296_3965_48d2_aa93_3280090bd718-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 银行账户类型 | String |  | N | 0：对公 |
| card_name | 银行账户名称 | String |  | N |  |
| card_no | 对公银行账号 | String |  | N | 示例值：98140008801800008888 |
| prov_id | 银行所在省 | String |  | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| area_id | 银行所在市 | String |  | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)示例值：310100 |
| branch_code | 支行联行号 | String |  | N | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "receipt_name": "尼博网络科技",
        "recon_resp_addr": "rmq://C_SSPM_YMFZ_AUDIT",
        "reg_area_id": "310100",
        "qry_settle_config_list": [
            {
                "fee_rate": "5.00",
                "min_amt": "1.00",
                "out_settle_flag": "2",
                "out_settle_huifuid": "",
                "remained_amt": "2.00",
                "settle_abstract": "我这里显示结算摘要",
                "settle_cycle": "D1",
                "settle_status": "1",
                "settle_type": "0"
            }
        ],
        "area_id": "310100",
        "mcc": "4816",
        "license_end_date": "20400813",
        "qry_cash_card_info_list": [
            {
                "area_id": "310100",
                "bank_code": "01020000",
                "bank_name": "中国工商银行",
                "branch_code": "102290026507",
                "branch_name": "中国工商银行上海市中山北路支行",
                "card_name": "上海尼博网络科技有限公司",
                "card_no": "1001265001234567890",
                "card_type": "0",
                "cert_begin_date": "20180106",
                "cert_end_date": "20380106",
                "cert_no": "321084198912075612",
                "cert_type": "00",
                "cert_validity_type": "0",
                "prov_id": "310000",
                "status": "N",
                "token_no": "10011703245"
            }
        ],
        "cust_type": "1",
        "product_id": "HUIFENQI",
        "reg_name": "上海尼博网络科技有限公司",
        "prov_id": "310000",
        "ent_type": "3",
        "qry_bank_card_conf": {
            "is_open_small_flag": "0"
        },
        "legal_cert_begin_date": "20180106",
        "reg_district_id": "310120",
        "legal_cert_no": "321084199112066311",
        "contact_mobile_no": "15221347112",
        "resp_code": "00000000",
        "short_name": "尼博网络科技",
        "license_code": "91310120MA1HXXWT5G",
        "legal_cert_end_date": "20380106",
        "license_validity_type": "0",
        "contact_email": "sunzhengnan@bunnypetcare.com",
        "legal_cert_validity_type": "0",
        "license_begin_date": "20200814",
        "detail_addr": "上海市奉贤区沿钱公路5601号1幢",
        "legal_name": "沈荣",
        "qry_union_conf": "{}",
        "contact_name": "沈荣",
        "legal_cert_type": "00",
        "resp_desc": "成功",
        "qry_ali_conf_list": [
            {
                "pay_channel_id_list": "JQF00001",
                "pay_scene": "1"
            },
            {
                "pay_channel_id_list": "JQF00002",
                "pay_scene": "1"
            },
            {
                "pay_channel_id_list": "JQF00003",
                "pay_scene": "1"
            }
        ],
        "service_phone": "15221347112",
        "login_name": "15221347112",
        "busi_type": "1",
        "delay_flag": "N",
        "reg_prov_id": "310000",
        "district_id": "310120",
        "reg_detail": "上海市奉贤区沿钱公路5601号1幢",
        "upper_huifu_id": "6666000021000120",
        "qry_cash_config_list": {
            "cash_type": "D0",
            "out_cash_flag": "2",
            "switch_state": "1"
        }
    }
}
```
