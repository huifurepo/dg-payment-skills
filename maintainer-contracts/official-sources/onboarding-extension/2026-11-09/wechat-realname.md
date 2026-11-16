## 微信实名认证
*最近更新时间：2025.4.10* 

### 应用场景
需要开通微信支付或报名参与微信活动的商户，要先通过微信实名认证验证。调用微信实名认证接口之前请先调用[商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)接口上传相关证照。具体参见下文描述。  

**适用对象**  
已成功入驻微信的商户，需要开通微信支付权限。

### 接口参数
* 请求URL：https://api.huifu.com/v2/merchant/busi/realname
* 请求方式：POST
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数
* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                  |
| :--------- | :------- | :----- | :--- | :--- | :-------------------- |
| sys_id     | 系统号   | String | 32   | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id<br/><font color="green">示例值：6666000123120000</font>|
| sign       | 加签结果 | String | 512  | Y    | 签名，对报文整体签名  |
| product_id | 产品号   | String | 32   | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font> |
| data       | 数据     | String |      | Y    | jsonObject格式        |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

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

| 参数                      | 中文名           | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------------ | :--------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| req_seq_id                | 请求流水号       | String | 32   | Y    | <font color="green">示例值：rQ2021121311173944134649875651</font>  |
| req_date                  | 请求日期        | String | 8    | Y    | 必填，请求日期yyyyMMdd，<font color="green">示例值：20220809</font> |
| huifu_id                  | 汇付ID           | String | 18   | Y    | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font>；**请确认该商户已成功入驻微信**              |
| pay_channel_id            | 子渠道号         | String | 32   | N    | 如需要填写汇付和渠道商约定的值，参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)；<font color="green">示例值：JQF00001</font>|
| pay_scene                 | 支付场景         | String | 2    | N    | <font color="green">示例值：01</font>；参见《[微信业务开通类型](http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明 |
|owner|	经营者/法人是否为受益人|	String|	1|	N|企业开通微信支付时需要填写；Y：是最终受益人；N：非最终受益人(默认)；<font color="green">示例值：Y</font>|
| identification_address | 法人证件居住地址    | String  | 256 | N  |1、主体类型为企业时，需要填写。其他主体类型，无需上传。<br>2、请按照证件上住址填写，若证件上无住址则按照实际住址填写，<font color="green">示例值：广东省深圳市南山区xx路xx号xx室</font>。|
| <span class="extend ubo_info_list">ubo_info_list</span>| 受益人信息     | String    |     | N  |jsonArray格式；受益人仅企业需要填写。<br/>若经营者/法人不是最终受益所有人，则需提填写受益所有人信息，最多上传4个。 若经营者/法人是最终受益所有人之一，可在此填写其他受益所有人信息，最多上传3个。 |
| name                      | 联系人姓名       | String | 64   | Y    | <font color="green">示例值：张三</font>|
| mobile                    | 联系人手机号     | String | 11   | Y    | <font color="green">示例值：13917364538</font>|
| id_card_number            | 联系人身份证号码 | String | 32   | Y    | <font color="green">示例值：320936198512035017</font>|
| contact_type           | 联系人类型 | String | 10   | Y    |LEGAL：经营者/法人；SUPER：经办人（经商户授权办理微信支付业务的人员）<br/> 1、主体为“小微/个人卖家”，可选择：LEGAL：<br>2、主体为“个体工商户/企业/政府机关/事业单位/社会组织”，可选择：LEGAL、SUPER<br/><font color="green">示例值：LEGAL</font>|
| contact_id_doc_type          | 联系人证件类型      | String | 10 | N  |当联系人类型是经办人时，请上传联系人证件类型；<br>枚举值参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明，<font color="green">示例值：00</font><br>个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关仅支持身份证类型。<br/>另外还需上传证件件，见【special_file_info_list】字段说明；|
| contact_period_begin        | 联系人证件有效期开始时间 | String | 20 | N  |1、当联系人类型是经办人时，请填写证件有效期开始时间;<br>2、格式：yyyy-MM-dd； <font color="green">示例值：2019-06-06</font>   |
| contact_period_end           | 联系人证件有效期结束时间 | String | 20 | N  | 1、当联系人类型是经办人时，请填写证件有效期结束时间;<br>2、格式：yyyy-MM-dd； <font color="green">示例值：2029-06-06</font>   <br>3、结束时间大于开始时间;若证件有效期为长期，请填写：长期|
| cert_type                 | 证书类型         | String | 64   | N    | CERTIFICATE_TYPE_2388：事业单位法人证书 ；仅支持事业单位<br />CERTIFICATE_TYPE_2389：统一社会信用代码证书 ；政府机关使用此类型<br />社会组织使用以下类型：<br/>CERTIFICATE_TYPE_2389：统一社会信用代码证书 ；<br />CERTIFICATE_TYPE_2394：社会团体法人登记证书      <br />CERTIFICATE_TYPE_2395：民办非企业单位登记证书      <br />CERTIFICATE_TYPE_2396：基金会法人登记证书      <br />CERTIFICATE_TYPE_2399：宗教活动场所登记证 <br />CERTIFICATE_TYPE_2400：其他证书/批文/证明 <br/>CERTIFICATE_TYPE_2520：执业许可证/执业证<br/>CERTIFICATE_TYPE_2521：基层群众性自治组织特别法人统一社会信用代码证  <br/>CERTIFICATE_TYPE_2522：农村集体经济组织登记证<br/><font color="green">示例值：CERTIFICATE_TYPE_2389</font> |
| cert_number               | 证书编号         | String | 32   | N    | 各类证书编号，如营业执照编号、事业部单位法人证书等；<br/><font color="green">示例值：91310230MA1JTWAK00</font> |
| cert_copy                 | 证书照片         | String | 64   | N    | **事业单位**填写，图片上传接口生成的file_id；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>   |
| micro_biz_type            | 小微经营类型     | String | 32   | N    | 门店场所：MICRO_TYPE_STORE     <br />流动经营/便民服务：MICRO_TYPE_MOBILE     <br />线上商品/服务交易：MICRO_TYPE_ONLINE<br/><font color="green">示例值：MICRO_TYPE_STORE</font>  |
| store_name                | 门店名称         | String | 32   | N    | 32个字符，16个汉字；<font color="green">示例值：肯德基共富新村店</font> |
| store_header_copy         | 门店门头照片     | String | 64   | N    | 小微商户填写，图片上传接口生成的fileId；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>  |
| store_indoor_copy         | 店内环境照片     | String | 64   | N    | 小微商户填写，图片上传接口生成的fileId；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>  |
| store_address_code        | 门店省市编码     | String | 16   | N    | 小微商户填写，请参考[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：360400</font>  |
| store_address             | 门店地址         | String | 128  | N    | 小微商户填写；<font color="green">示例值：上海宝山区共富路512号</font> |
| identification_front_copy | 身份证件人像面 | String | 64   | N    | 小微商户填写，图片上传接口生成的fileId；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>  |
| identification_back_copy  | 身份证件国徽面 | String | 64   | N    | 小微商户填写，图片上传接口生成的fileId；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| company_prove_copy        | 单位证明函照片   | String | 64   | N    | 事业单位填写，图片上传接口生成的fileId；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>  |
| finance_institution_flag | 是否金融机构    | String |  1  | N  |选填，Y/N；默认N；<font color="green">示例值：N</font> <br>请根据申请主体的实际情况填写，可参见[微信金融机构接入指引](https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html)|
| finance_type         | 金融机构类型    | String  | 128 | N  |当主体是金融机构时，必填；金融机构类型需与营业执照/登记证书上一致，可参见[微信金融机构接入指引](https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html)。<br>BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等；<br>PAYMENT_AGENT：支付机构, 适用于非银行类支付机构；<br>INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务；<br>TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等；<br>OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务<br/><font color="green">示例值：INSURANCE</font>；<br/>金融机构需上传许可证图片，见【special_file_info_list】字段说明；   |
| category_id               | 特殊行业Id       | String | 3    | N    | 特殊行业填写，参看微信支付提供的[特殊行业id对照表](https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/applysubject_new/chapter6_1.shtml)；<font color="green">示例值：100</font> |
| <span class="extend special_file_info_list">special_file_info_list</span> | 文件列表         | String |      | N    | jsonArray格式          |

<!--#### ubo_info_list受益人  -->
<!-- extend:start -->
<!-- div:extend-table ubo_info_list-table -->

| 参数               | 中文名    | 定义     | 长度  | 必填  | 说明  |
| :-------- | :---------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| ubo_id_doc_type     | 受益人证件类型   | String | 10  | Y |企业开通微信业务必填；枚举值00：身份证， 01：护照，11：港澳同胞回乡证，12：外国人居留证，13：港澳居民证，14：台湾居民证；<br>个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关仅支持身份证类型。<br/><font color="green">示例值：00</font>|
| ubo_id_doc_copy     | 证件正面照片 | String | 64  |Y |1、请上传受益人证件的正面照片；企业开通微信业务必填；<br>2、若证件类型为身份证，请上传人像面照片;<br>3、请上传彩色照片or彩色扫描件or复印件;<br>4、开通微信业务时需加盖公章鲜章，可添加“微信支付”相关水印（如微信支付认证）<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>|
| ubo_id_doc_copy_back | 证件反面照片 | String | 64  | N   |1、请上传受益人证件的反面照片；企业开通微信业务必填；<br>2、若证件类型为护照，无需上传反面照片;<br>3、请上传彩色照片or彩色扫描件or复印件;<br>4、开通微信业务时需加盖公章鲜章，可添加“微信支付”相关水印（如微信支付认证）<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>|
| ubo_id_doc_name     | 受益人证件姓名   | String | 128 | Y   |<font color="green">示例值：张三</font> |
| ubo_id_doc_number   | 受益人证件号码   | String | 128 | Y   |<font color="green">示例值：320936198512045029</font>   |
| ubo_id_doc_address  | 证件居住地址 | String | 256 | Y   |请按照证件上住址填写，若证件上无住址则按照实际住址填写<br/><font color="green">示例值：广东省深圳市南山区xx路xx号xx室</font> 。  |
| ubo_period_begin | 证件有效期开始时间 | String | 20 | Y  | 格式：yyyyMMdd； <font color="green">示例值：20190606</font>   |
| ubo_period_end   | 证件有效期结束时间 | String | 20 | Y  | 1、格式：yyyyMMdd； <font color="green">示例值：20290606</font>；若证件有效期为长期，请填写：长期；<br>2、结束时间大于开始时间|

<!-- extend:end -->

<!--#### special_file_info_list特殊行业文件列表-->
<!-- extend:start -->
<!-- div:extend-table special_file_info_list-table -->

| 参数      | 中文名      | 定义   | 长度 | 必填 | 说明                                                         |
| :-------- | :---------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| file_type | 文件类型    | String | 8    | Y    | F28：联系人身份证人像面；（联系人是经办人时需要提供，参见下文说明）<br/>F29：联系人身份证国徽面；（联系人是经办人时需要提供，参见下文说明）<br/>F33：联系人护照人像面；（联系人是经办人时需要提供，参见下文说明）<br/>F241：联系人证件照正面，非身份证与护照类型；（联系人是经办人时需要提供，参见下文说明）<br/>F242：联系人证件照反面，非身份证类型；（联系人是经办人时需要提供，参见下文说明）<br>F227：微信业务办理授权函；（联系人是经办人时必需提供，参见下文说明）<br/>F236：金融机构许可证图片一；（金融机构需提供）<br/>F237：金融机构许可证图片二<br/>F238：金融机构许可证图片三<br/>F239：金融机构许可证图片四<br/>F240：金融机构许可证图片五；<br/>F150:行业经营许可证资质照片一（特殊行业选填）     <br />F151:行业经营许可证资质照片二     <br />F152:行业经营许可证资质照片三     <br />F153:行业经营许可证资质照片四     <br />F154:行业经营许可证资质照片五     <br />F155:行业经营许可证资质照片六<br/><font color="green">示例值：F28</font> |
| file_id   | 文件jfileID | String | 64   | Y    | 图片上传接口生成的fileId；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>  |

<!-- extend:end -->

* **受益人说明**：   
根据国家相关法律法规，需要提供公司受益所有人信息，受益所有人需符合至少以下条件之一：    
1. 直接或者间接拥有超过25%公司股权或者表决权的自然人。    
2. 通过人事、财务等其他方式对公司进行控制的自然人。    
3. 公司的高级管理人员，包括公司的经理、副经理、财务负责人、上市公司董事会秘书和公司章程规定的其他人员。  

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

##### 请求示例

```json
{
    "sys_id": "6666000123123123",
    "product_id": "ZDTEST",
    "data": {
        "req_seq_id": "rQ20220823176047585303390268",
        "req_date": "20220823",
        "huifu_id": "6666000104854510",
        "pay_channel_id": "JP00001",
        "pay_scene": "01",
        "name": "小枫",
        "mobile": "17521205027",
        "id_card_number": "130224198806083798",
        "cert_type": "CERTIFICATE_TYPE_2389",
        "cert_number": "1234567892",
        "micro_biz_type": "",
        "store_name": "",
        "store_address_code": "",
        "store_address": "",
        "store_header_copy": "",
        "store_indoor_copy": "",
        "identification_back_copy": "c7faf0e6-39e9-3c35-9075-2312ad6f4ea4",
        "identification_front_copy": "c7faf0e6-39e9-3c35-9075-2312ad6f4ea4",
        "cert_copy": "",
        "company_prove_copy": "",
        "contact_type": "SUPER",
        "contact_id_doc_type": "01",
        "contact_period_begin": "1990-03-07",
        "contact_period_end": "长期",
        "finance_institution_flag": "N",
        "finance_type": "",
        "category_id": "",
        "owner": "N",
        "identification_address": "上海市徐汇区宜山路789号789室",
        "ubo_info_list": "[{\"ubo_id_doc_type\":\"00\",\"ubo_id_doc_copy\":\"c7faf0e6-39e9-3c35-9075-2312ad6f4ea4\",\"ubo_id_doc_copy_back\":\"c7faf0e6-39e9-3c35-9075-2312ad6f4ea4\",\"ubo_id_doc_name\":\"杨雷\",\"ubo_id_doc_number\":\"110101199003072631\",\"ubo_id_doc_address\":\"上海市徐汇区宜山路789号\",\"ubo_period_begin\":\"19900307\",\"ubo_period_end\":\"长期\"}]",
        "special_file_info_list": "[{\"file_type\":\"F33\",\"file_id\":\"49ac7d9b-851c-31b4-8b21-2983ea97b98c\"},{\"file_type\":\"F227\",\"file_id\":\"49ac7d9b-851c-31b4-8b21-2983ea97b98c\"}]"
    },
    "sign": "etGyy6cmL8STBDwAHch47ueGGrplFzbmQc+Mq7fts2ny4kDjqzaju18ZvhJ0fK5VNvObgNQgDqzeXb2JCDA821RWorIOkOxsH683yV8JNQyp9M6ZMj3+Ei0ZWkbdf1eUUkBezcfMej0c7xF2+USfrSqVAXvW08krl4sjjXxnjOc="
}
```

### 响应参数

| 参数         | 中文名     | 定义   | 长度 | 必填 | 说明                                   |
| :----------- | :--------- | :----- | :--- | :--- | :------------------------------------- |
| resp_code    | 返回码     | String | 8    | Y    | [交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)    |
| resp_desc    | 返回描述   | String | 512  | Y    | [交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)  |
| huifu_id     | 汇付ID     | String | 18   | Y    | <font color="green">示例值：6666000123123123</font> |
| applyment_id | 申请单编号 | String | 256  | N    | 微信支付分配的申请单号，申请成功时返回；<font color="green">示例值：2000002327252449</font>|

##### 响应示例

```json
{  
    "data":{  
        "applyment_id":"2000002327252449",  
        "huifu_id":"6666000104854510",  
        "resp_code":"00000000",  
        "resp_desc":"成功"  
    },  
    "sign":"TMA8hscM3WUJn0zUR0hi1Joh+dTgJAwF4b6v/ubrv9KKcavLoujlUlonUO/J7Ivv+g78q6sGb2bKapgy105pdNbxTN0KW1Uc5q1R3l/5G8l4WjupdB8HZZGqN5yymjR6/m6D4+n3NMRNBU+aPWE7q1gFbxu5aL7IXzo0Jbi5EQQ="  
}
```


<!--
输入源“/body/subject_info/business_licence_info/licence_copy”映射到字段“营业执照照片”必填性规则校验失败，此字段为必填项
基础参数校验失败:【store_name-门店名称】长度不能超过32个字符
-->