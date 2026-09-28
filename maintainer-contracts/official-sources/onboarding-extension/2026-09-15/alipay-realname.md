## 支付宝实名申请提交
*最近更新时间：2025.4.10* 

### 应用场景
需要开通支付宝支付或报名参与支付宝活动的商户，要先通过支付宝实名认证验证。调用支付宝实名认证申请接口之前请先调用【[图片上传](http://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)】接口上传相关证照。具体参见下文描述。  

**适用对象**    
已成功入驻支付宝的商户，需要开通支付宝支付权限。

### 接口参数
* 请求URL：https://api.huifu.com/v2/merchant/busi/ali/realname/apply
* 请求方式：POST
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数
* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font>  |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：MCS </font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名         | 定义   | 长度 | 必填 | 说明                 |
| :--- | :------------- | :----- | :--- | :--- | :------------------- |
| sign | 签名           | String | 512  | Y    | 签名，对报文整体签名 |
| data | 交易响应内容体 | String |      | N    | 业务返回参数         |

### **请求参数**

<style>
table th:first-of-type {
    width: 17%;
}
table th:nth-of-type(2) {
    width: 15%;
}
table th:nth-of-type(3) {
    width: 10%;
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

**data**

| 参数                  | 中文名     | 定义     | 长度 | 必填 | 说明    |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| req_seq_id          | 请求流水号   | String | 32 | Y  | <font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date            | 请求日期    | String | 8  | Y  | 请求日期格式yyyyMMdd；<font color="green">示例值：20220809</font>  |
| huifu_id            | 汇付ID    | String | 18 | Y  | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font> |
| pay_channel_id      | 子渠道号    | String | 32 | N  | 如需要填写汇付和渠道商约定的值，参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)；<br/><font color="green">示例值：JQF00001</font>|
| pay_scene           | 业务开通类型    | String | 2  | N  |1-线下扫码；<font color="green">示例值：1</font>； |
| <span class="extend auth_identity_info">auth_identity_info</span>   | 主体信息    | String |    | Y  | jsonObject字符串  |
| <span class="extend legal_person_info">legal_person_info</span>   | 法人身份信息  | String |    | N  | jsonObject字符串；为空时取开户时法人信息；       |
| <span class="extend contact_person_info">contact_person_info</span> | 联系人信息   | String |    | Y  | jsonObject字符串          |
| <span class="extend ubo_info">ubo_info</span>             | 受益人信息   | String |    | N  | jsonObject字符串；主体为企业，且经营者/法人不是最终受益人，因为受益人是第三方所以必需填写  |

<!--#### contact_person_info联系人信息  -->
<!-- extend:start -->
<!-- div:extend-table contact_person_info-table -->

| 参数             | 中文名      | 定义     | 长度 | 必填 | 说明                            |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| name           | 联系人姓名    | String | 64 | N  | 为空时取企业商户取联系人姓名，个人商户取入驻时填写的名称；<br/><font color="green">示例值：张三</font> |
| mobile         | 联系人手机号   | String | 11 | N  | 为空时取企业商户取联系人手机号；<font color="green">示例值：13917353627</font>  |
| id_card_number | 联系人身份证号码 | String | 32 | Y  |<font color="green">示例值：320926198512053827</font>    |

<!-- extend:end -->

<!--#### auth_identity_info主体信息-->
<!-- extend:start -->
<!-- div:extend-table auth_identity_info-table -->

| 参数                       | 中文名       | 定义     | 长度  | 必填 | 说明      |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| business_type            | 主体类型      | String | 32  | Y  | 枚举定义：<br/>0 - 个人/小微<br/>1 - 政府机构<br/>2 - 国营企业<br/>3 - 私营企业<br/>4 - 外资企业<br/>5 - 个体工商户<br/>7 - 事业单位 <br><font color="green">示例值：3</font>；    |
| finance_institution_flag | 是否金融机构    | String | 1   | N  | Y-金融机构，N-非金融机构；默认值：N；<font color="green">示例值：N</font>    |
| financial_type           | 金融机构类型    | String | 32  | N  | 当主体是金融机构时，必填；<br>金融机构类型需与营业执照/登记证书上一致。<br>BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等；<br>PAYMENT_AGENT：支付机构, 适用于非银行类支付机构；<br>INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务；<br>TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等；<br>OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；<br/><font color="green">示例值：BANK_AGENT</font>|
| finance_license_pics     | 金融机构许可证图片 | String | 350 | N  | 当主体是金融机构时，必填<br/>上送图片上传返回的jfileId，文件类型F236~F240。最多五张图片使用“,”分隔；<br/> <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529,57cc7f00-600a-33ab-b614-6221bbf2e530</font>|
| certificate_type         | 证照类型      | String | 32  | N  | 营业执照(BUSINESS_CERT)；登记证书(REGISTER_CERT)；<br/><font color="green">示例值：BUSINESS_CERT</font><br/>主体类型为企业/个体户/政府机关/事业单位/社会组织时（1/2/3/4/5/7），必填； <br/>主体为政府机关/事业单位/社会组织时（1/7），填登记证书；<br/>主体类型为企业/个体户时（2/3/4/5），填营业执照； |
| <span class="extend certificate_info">certificate_info</span>         | 登记证书信息    | String |     | N  | jsonObject字符串； <br/>主体类型为企业/个体户/政府机关/事业单位/社会组织（1/2/3/4/5/7）时必填，**小微商户切勿填写**|
| company_prove_copy       | 单位证明函照片   | String | 128 | N  | 上送图片上传返回的jfileId，文件类型F46。主体类型为政府机关/事业单位时必填；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>|
| <span class="extend support_credentials">support_credentials</span>       | 辅助证明材料信息  | String |     | N  | jsonObject字符串  <br/>  主体类型为小微商户时，辅助证明材料信息必填                                                                                                            |
| <span class="extend qualification_info_list">qualification_info_list</span>   | 经营许可证     | String |     | N  | jsonArray字符串 <br/>1、填写特殊行业的经营许可证信息<br/>2、最多填写支持5个行业  |

<!-- extend:end -->

<!--#### certificate_info登记证书信息-->
<!-- extend:start -->
<!-- div:extend-table certificate_info-table -->

| 参数                   | 中文名     | 定义     | 长度  | 必填 | 说明      |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| cert_type            | 登记证书类型  | String | 32  | C | **证照类型为登记证书时(certificate_type=REGISTER_CERT)必填**。枚举：<br/>统一社会信用代码证书(CERTIFICATE_TYPE_2389)<br/>慈善组织公开募捐资格证书(CERTIFICATE_TYPE_2397)<br/>社会团体法人登记证书(CERTIFICATE_TYPE_2394)<br/>民办非企业单位登记证书(CERTIFICATE_TYPE_2395)<br/>基金会法人登记证书(CERTIFICATE_TYPE_2396)<br/>农民专业合作社法人营业执照(CERTIFICATE_TYPE_2398)<br/>宗教活动场所登记证(CERTIFICATE_TYPE_2399)<br/>其他证书/批文/证明(CERTIFICATE_TYPE_2400)<br/><font color="green">示例值：CERTIFICATE_TYPE_2389</font>  |
| cert_number          | 证照编号    | String | 64  | N  | <font color="green">示例值：92650109MA79R8E308</font> |
| cert_copy            | 证照图片    | String | 128 | N  |  上送图片上传返回的jfileId；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 </font>  |
| cert_merchant_name   | 证照商户名称  | String | 64  | N  | <font color="green">示例值：新新饭店</font> |
| cert_legal_person    | 证照法人姓名  | String | 64  | N  | <font color="green">示例值：李四</font>|
| cert_company_address | 证照注册地址  | String | 128 | N  | <font color="green">示例值：浙江省杭州市西湖区xxx街道xxx门牌号</font>|
| effect_time          | 证照生效时间  | String | 32  | N  | <font color="green">示例值：19990101</font>    |
| expire_time          | 证照过期时间  | String | 32  | N  | <font color="green">示例值：20201101</font>，若证件有效期为长期，请填写：长期 |

<!-- extend:end -->

<!--#### support_credentials辅助证明材料信息-->
<!-- extend:start -->
<!-- div:extend-table support_credentials-table -->

| 参数              | 中文名           | 定义     | 长度  | 必填 | 说明                                                                              |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| micro_biz_type  | 小微经营类型        | String | 32  | Y  | 门店场所：MICRO_TYPE_STORE<br/>流动经营/便民服务：MICRO_TYPE_MOBILE<br/><font color="green">示例值：MICRO_TYPE_STORE</font>  |
| store_name      | 门店名称          | String | 64  | Y  | <font color="green">示例值：肯德基共富新村店</font> |
| province_code   | 门店省市编码        | String | 32  | Y  | [参考地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310000</font> |
| province        | 门店省份          | String | 32  | Y  | <font color="green">示例值：浙江省</font>|
| city_code       | 门店市行政区号       | String | 32  | Y  | [参考地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font> |
| city            | 门店城市          | String | 32  | Y  | <font color="green">示例值：杭州市</font> |
| district_code   | 门店街道区号        | String | 32  | Y  | [参考地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310101</font> |
| district        | 门店街道          | String | 32  | Y  | 最长16个汉字；<font color="green">示例值：西湖区留下街道</font>|
| store_address   | 门店场所填写门店详细地址  | String | 128 | Y  | 门店场所填写门店详细地址，流动经营类型填“无”；<br/><font color="green">示例值：上海宝山区共富路512号</font>|
| store_door_img  | 门店门头照信息或摊位照   | String | 128 | N  | 为空时取开户或开业务时上送的门头照片，文件类型F22<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>|
| store_inner_img | 门店店内照片或者摊位照侧面 | String | 128 | N  | 为空时取开户或开业务时上送的店铺内景图片，文件类型F24<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |

<!-- extend:end -->

<!--#### qualification_info_list经营许可证-->
<!-- extend:start -->
<!-- div:extend-table qualification_info_list-table -->

| 参数         | 中文名         | 定义     | 长度  | 必填 | 说明                                                                          |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| mcc_code   | 行业类目id      | String | 20  | Y  | 参见[支付宝商家行业二级类目code](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc)；<font color="green">示例值：5411</font>  |
| image_list | 行业经营许可证资质照片 | String | 400 | Y  | 上送图片上传返回的jfileId，一个行业类目下最多上传6张资质照片，文件类型F150~F155。使用“,”分隔<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529,57cc7f00-600a-33ab-b614-6221bbf2e534</font>                                  |

<!-- extend:end -->

<!--#### legal_person_info法人身份信息-->
<!-- extend:start -->
<!-- div:extend-table legal_person_info-table -->

| 参数                | 中文名     | 定义     | 长度  | 必填 | 说明             |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| legal_type        | 证件持有人类型 | String | 32  | N  | 法人：LEGAL，为空时默认选项； 主体类型为企业、个体户、社会组织、小微商户时，必须为经营者/法人。<br/>经办人：SUPER；主体类型为政府机关、事业单位时默认是法人。若因特殊情况，无法提供法人证件时可填经办人类型。<br/><font color="green">示例值：LEGAL</font>；  |
| card_type         | 证件类型    | String | 32  | N  |枚举值：<br/>00:身份证 01:护照  13：港澳居民证 14:台湾居民证；<br/>为空时取开户时法人信息 <br/>个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关、小微商户仅支持身份证类型。<br/><font color="green">示例值：00</font>|
| person_name       | 法人姓名    | String | 64  | N  | 为空时取开户时法人信息；<br/> <font color="green">示例值：李四</font>|
| card_no           | 证件号码    | String | 64  | N  | 为空时取开户时法人信息；<br/><font color="green">示例值：233330199001010001</font>|
| effect_time       | 证件生效时间  | String | 32  | N  | 为空时取开户时法人信息；<br/><font color="green">示例值：19990101</font> |
| expire_time       | 证件过期时间  | String | 32  | N  | 为空时取开户时法人信息；<br/><font color="green">示例值：20001101</font>，长期有效时传“长期”                                                                                                                                      |
| card_front_img    | 证件人像面   | String | 128 | N  | 为空时取开户时法人信息，如果开户时未传该字段必填；<br/>上送[图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)返回的jfileId；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font>  |
| card_back_img     | 证件国徽面   | String | 128 | N  | 为空时取开户时法人信息，如果开户时未传该字段必填；只有身份证类型需要上传反面；<br/>上送[图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)返回的jfileId，<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font>|
| auth_letter_img   | 授权函照片   | String | 128 | N  | 上送图片上传返回的jfileId；文件类型F224业务办理授权函；<br/>当证件持有人类型为经办人时必须上传。其他情况，无需上传。<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font>|
| is_benefit_person | 是否为受益人  | String | 1   | N  | Y-受益人;N-非受益人 默认值：Y；<font color="green">示例值：Y</font>|

<!-- extend:end -->

<!--#### ubo_info受益人信息-->
<!-- extend:start -->
<!-- div:extend-table ubo_info-table -->

| 参数                   | 中文名       | 定义     | 长度  | 必填 | 说明     |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| ubo_id_doc_name      | 证件姓名      | String | 128 | Y  | <font color="green">示例值：李四</font>  |
| ubo_id_doc_type      | 证件类型      | String | 10  | Y  | 枚举值：<br/>00:身份证； 01:护照；  13：港澳居民证； 14:台湾居民证；<font color="green">示例值：00</font><br/>个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关、小微商户仅支持身份证类型。  |
| ubo_id_doc_number    | 证件号码      | String | 128 | Y  | <font color="green">示例值：320936198512045029</font>                                                                             |
| ubo_period_begin     | 证件有效期开始时间 | String | 20  | Y  | 格式：yyyyMMdd； <font color="green">示例值：20190606</font>  |
| ubo_period_end       | 证件有效期结束时间 | String | 20  | Y  |  1、格式：yyyyMMdd； <font color="green">示例值：20290606</font>；若证件有效期为长期，请填写：长期；<br>2、结束时间大于开始时间|
| ubo_id_doc_copy      | 证件人像面    | String | 64  | Y  | 上送图片上传返回的jfileId；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>|
| ubo_id_doc_copy_back | 证件国徽面    | String | 64  | N  | 上送图片上传返回的jfileId，只有身份证类型需要上传反面；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font>   |

<!-- extend:end -->

* **受益人说明**：   
根据国家相关法律法规，需要提供公司受益所有人信息，受益所有人需符合至少以下条件之一：    
1. 直接或者间接拥有超过25%公司股权或者表决权的自然人。    
2. 通过人事、财务等其他方式对公司进行控制的自然人。    
3. 公司的高级管理人员，包括公司的经理、副经理、财务负责人、上市公司董事会秘书和公司章程规定的其他人员。  

<!--
* **联系人证件说明**：
1. 当联系人类型是经办人时，请上传联系人证件的正面照片；参见special_file_info_list特殊行业文件列表中文件类型说明；
	- 若证件类型为身份证，请上传正反面照片；
	- 若证件类型为护照，无需上传反面照片；
2. 请上传彩色照片or彩色扫描件or复印件（需加盖公章鲜章），可添加“微信支付”相关水印（如微信支付认证）；

* **微信业务办理授权函说明**：
1. 当经办人是联系人类型时，请上传业务办理授权函；
2. [请参照示例图](https://kf.qq.com/faq/220509Y3Yvym220509fQvYR7.html)；打印业务办理授权函，全部信息需打印，不支持手写商户信息，并加盖公章；
* **金融机构许可证图片说明**：
5. 当主体是金融机构时，必填；
6. 参见[微信金融机构接入指引](https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html);
7. 请提供为“申请商家主体”所属的许可证，可授权使用总公司/分公司的特殊资质。
8. 最多可上传5张照片；
-->
##### 请求示例

```json
{
    "sys_id": "6666000123123123",
    "product_id": "ZDTEST",
    "data": {
        "req_seq_id": "20220823022026245936650",
        "req_date": "20220823",
        "huifu_id": "6666000105418240",
        "pay_channel_id": "10000001",
        "pay_scene": "1",
        "contact_person_info": "{\"name\":\"谢季\",\"mobile\":\"18900400032\",\"id_card_number\":\"120103198507275017\"}",
        "legal_person_info": "{\"legal_type\":\"SUPER\",\"card_type\":\"00\",\"person_name\":\"李四\",\"card_no\":\"110101199909291419\",\"effect_time\":\"19990101\",\"expire_time\":\"长期\",\"card_front_img\":\"afce08c5-1548-30f8-bf70-1752c3012f66\",\"card_back_img\":\"51dd13bb-6268-36d0-ac84-c4cdc19eccba\",\"auth_letter_img\":\"51dd13bb-6268-36d0-ac84-c4cdc19eccba\",\"is_benefit_person\":\"N\"}",
        "auth_identity_info": "{\"finance_license_pics\":\"a5d373f6-3e79-405f-9993-fb7ea051c372\",\"financial_type\":\"INST\",\"business_type\":\"2\",\"qualification_info_list\":\"[{\\\"mcc_code\\\":\\\"2015050700000000\\\",\\\"image_list\\\":\\\"a5d373f6-3e79-405f-9993-fb7ea051c372\\\"}]\",\"finance_institution_flag\":\"N\",\"certificate_type\":\"BUSINESS_CERT\",\"company_prove_copy\":\"71da066c-5d15-3658-a86d-4e85ee67808a\",\"certificate_info\":\"{\\\"cert_number\\\":\\\"9111000071093465XC\\\",\\\"cert_type\\\":\\\"CERTIFICATE_TYPE_2389\\\",\\\"expire_time\\\":\\\"长期\\\",\\\"cert_legal_person\\\":\\\"李四\\\",\\\"cert_company_address\\\":\\\"浙江省杭州市西湖区1街道10号\\\",\\\"cert_merchant_name\\\":\\\"新新饭店\\\",\\\"cert_copy\\\":\\\"afce08c5-1548-30f8-bf70-1752c3012f66\\\",\\\"effect_time\\\":\\\"19990101\\\"}\",\"support_credentials\":\"{\\\"province\\\":\\\"上海\\\",\\\"store_door_img\\\":\\\"afce08c5-1548-30f8-bf70-1752c3012f66\\\",\\\"city\\\":\\\"上海市\\\",\\\"district_code\\\":\\\"310107\\\",\\\"micro_biz_type\\\":\\\"MICRO_TYPE_STORE\\\",\\\"district\\\":\\\"普陀区\\\",\\\"store_inner_img\\\":\\\"51dd13bb-6268-36d0-ac84-c4cdc19eccba\\\",\\\"store_name\\\":\\\"张三\\\",\\\"city_code\\\":\\\"310100\\\",\\\"store_address\\\":\\\"消息路\\\",\\\"province_code\\\":\\\"310000\\\"}\"}",
        "ubo_info": "{\"ubo_id_doc_name\":\"消化\",\"ubo_id_doc_type\":\"00\",\"ubo_id_doc_number\":\"110101199909291419\",\"ubo_period_begin\":\"19990101\",\"ubo_period_end\":\"20260606\",\"ubo_id_doc_copy\":\"afce08c5-1548-30f8-bf70-1752c3012f66\",\"ubo_id_doc_copy_back\":\"51dd13bb-6268-36d0-ac84-c4cdc19eccba\"}"
    },
    "sign": "etGyy6cmL8STBDwAHch47ueGGrplFzbmQc+Mq7fts2ny4kDjqzaju18ZvhJ0fK5VNvObgNQgDqzeXb2JCDA821RWorIOkOxsH683yV8JNQyp9M6ZMj3+Ei0ZWkbdf1eUUkBezcfMej0c7xF2+USfrSqVAXvW08krl4sjjXxnjOc="
}
```

### 响应参数

| 参数           | 中文名     | 定义     | 长度  | 非空 | 说明    |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| resp_code    | 返回码     | String | 8   | Y  | [交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)     |
| resp_desc    | 返回描述    | String | 512 | Y  | [交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)      |
| applyment_id | 申请单编号   | String | 256 | N  | <font color="green">示例值：202207011000185133</font>    |
| order_status | 意愿申请单状态 | String |     | N  | 枚举值：<br/>审核中(AUDITING)<br/>待联系人确认(CONTACT_CONFIRM)<br/>待法人确认(LEGAL_CONFIRM)<br/>审核通过(AUDIT_PASS)<br/>审核失败(AUDIT_REJECT)<br/>已冻结(AUDIT_FREEZE)；本次申请冻结但仍会返回上次的授权码，可以扫码授权。<br/>已撤回(CANCELED)</br><font color="green">示例值：AUDIT_PASS</font>   |

##### 响应示例

```json
{
    "data": {
        "order_status": "AUDITING",
        "resp_desc": "成功",
        "resp_code": "00000000",
        "applyment_id": "202208011001005627"
    }
}
```