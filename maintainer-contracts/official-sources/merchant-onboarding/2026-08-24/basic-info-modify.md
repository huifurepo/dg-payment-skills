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
## 商户基本信息修改

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/basicdata/modify

*最近更新时间：2026.08.07*
> 2023.6.30斗拱升级了商户进件类接口，老版接口、升级指引请参考[说明文档](old_api/api_2023shglsj)

### 应用场景
已完成基本信息入驻的商户若信息填写有误或需变更，调用此接口。支持商户的基本信息、银行卡信息、结算和取现配置信息的变更。

**适用对象**  
  商户需要申请修改基本信息、银行卡信息、结算取现配置，可调用该接口。

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

| 参数 | 中文名     | 类型   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

- “必填”字段取值“Y“：必填；“N”：非必填；“C”代表条件必填；
### **注意**
- card_info卡信息银行卡账户名、银行卡号、持卡人证件号码会做三要素验证，请正确填写；
- card_info卡信息若修改持卡人证件信息，则相关的字段cert_type，cert_no，cert_validity_type，cert_begin_date，cert_end_date需同时填写最新值。
- 必填字段取值“C”代表条件必填；  



### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号，同一商户号当天唯一；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准 <font color="green">示例值：20220125</font> |
| upper_huifu_id | 直属渠道号 | String | 18 | C | 该商户进件完成后归属的渠道商huifu_id；；<br/>sys_id主体为渠道商时填写； <br/>sys_id主体为总部商户时选填；<br/> <font color="green">示例值：6666000123123123</font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font> |
| reg_name | 商户名称 | String | 64 | N | 商户未开通业务时，支持修改。商户名称，必须与商家营业执照上的名称一致；个体工商户的营业执照如没有名称、名称为“\*”或空，则商户名称应填 “个体户XXX”（XXX为营业执照上经营者姓名），如“个体户张三”，汉字以2个字符计算。<font color="green">示例值：上海汇付支付有限公司</font> |
| short_name | 商户简称 | String | 64 | N | 商户简称，需与商户注册名称相关；<font color="green">示例值：汇付商城</font> |
| mer_en_name | 商户英文名称 | String | 256 | N | 商户英文名称；<font color="green">示例值：huifupay </font> |
| ent_type | 公司类型 | String | 1 | N | 商户未开通业务时，支持修改。<br/>1：政府机构<br/>2：国营企业<br/>3：私营企业<br/>4：外资企业<br/>5：个体工商户<br/>6：其它组织<br/>7：事业单位<br/>9：业主委员会；<br/><font color="green">示例值1</font>； |
| mcc | 所属行业 | String | 7 | N | 商户未开通业务时，支持修改。参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；<font color="green">示例值：5311</font> |
| license_type | 营业执照类型 | String | 32 | N | 参见[机构证照类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E6%9C%BA%E6%9E%84%E8%AF%81%E7%85%A7%E7%B1%BB%E5%9E%8B)说明； <font color="green">示例值：NATIONAL_LEGAL</font> |
| license_code | 营业执照编号 | String | 18 | N | 商户未开通业务时，支持修改。工商营业执照编号。<font color="green">示例值：92650109MA79R8E308；</font> |
| license_validity_type | 营业执照有效期类型 | String | 1 | N | 营业执照有效期类型;0：非长期有效； 1：长期有效；<font color="green">示例值：0 </font><br/>当使用总部资质时不填 |
| license_begin_date | 营业执照有效期开始日期 | String | 8 | N | 日期格式：yyyyMMdd，以北京时间为准； <font color="green">示例值：20220125</font><br/>当使用总部资质时不填 |
| license_end_date | 营业执照有效期截止日期 | String | 8 | N | 日期格式：yyyyMMdd，以北京时间为准。 <br/> 当license_validity_type=0时必填  <br/>当license_validity_type=1时为空<br/>当使用总部资质时不填  <br/><font color="green">示例值：20220125</font> |
| reg_prov_id | 注册省 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> ；如修改省市区要级联修改<br/>当使用总部资质时不填 |
| reg_area_id | 注册市 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> ；如修改省市区要级联修改<br/>当使用总部资质时不填 |
| reg_district_id | 注册区 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font>；如修改省市区要级联修改 <br/>当使用总部资质时不填 |
| reg_detail | 注册详细地址 | String | 255 | N | 商户注册地址或营业执照住所，汉字以2个字符计算；，<br/><font color="green">示例值：上海市徐汇区XX路XX号</font><br/>当使用总部资质时不填 |
| reg_capital | 注册资本 | String | 32 | N | 保留两位小数，国营企业、私营企业、外资企业、政府机构、事业单位、其他、集体经济必填，个体工商户可为空；<font color="green">示例值：100.00</font> |
| business_scope | 经营范围 | String | 64 | N | <font color="green">示例值：日用百货、化妆品、珠宝、化工原料及产品(除危险品)、化学品、纺织原料</font> |
| found_date | 成立时间 | String | 8 | N | <font color="green">示例值：20091212</font> |
| legal_name | 法人姓名 | String | 32 | N | 企业商户法人。最大支持16个汉字。企业商户时，结算类型为对私法人时，如果卡信息中证件号，证件类型，结算人证件有效期开始日期，结算人证件有效期结束日期，证件有效期类型任一字段为空，则必填。<br/>当使用总部资质时不填<br/><font color="green">示例值：张三 </font> |
| legal_cert_type | 法人证件类型 | String | 2 | N | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。当card_type=0时为空； 当card_type=1或2时选填 <font color="green">示例值：00</font><br/>当使用总部资质时不填 |
| legal_cert_no | 法人证件号码 | String | 32 | N | 法人证件号码，如法人证件类型为00：身份证，则填写身份证号码；<font color="green">示例值：310112200001018888</font><br/>；当使用总部资质时不填；年龄不能小于18岁且不能大于80岁； |
| legal_cert_validity_type | 法人证件有效期类型 | String | 1 | N | 0：非长期有效；1：长期有效；<font color="green">示例值：0 </font> |
| legal_cert_begin_date | 法人证件有效期开始日期 | String | 8 | N | 日期格式：yyyyMMdd，以北京时间为准；<font color="green">示例值：20220125 </font>；当使用总部资质时不填 |
| legal_cert_end_date | 法人证件有效期截止日期 | String | 8 | N | 日期格式：yyyyMMdd，以北京时间为准。<font color="green">示例值：20220125</font><br/>当legal_cert_validity_type=0时必填；<br/>当legal_cert_validity_type=1时为空；<br/>当使用总部资质时不填 |
| legal_addr | 法人身份证地址 | String | 256 | N | <font color="green">示例值：上海市徐汇区宜山路700号普天信息产业园2期C5栋</font> |
| legal_mobile_no | 法人手机号 | String | 11 | N | <font color="green">示例值：13917314256</font> |
| occupation | *负责人职业* | String | 2 | N | 1A：各类专业,技术人员<br/>1B：国家机关,党群组织,企事业单位的负责人<br/>1C：办事人员和有关人员<br/>1D：商业工作人员<br/>1E：服务性工作人员<br/>1F：农林牧渔劳动者<br/>1G：生产工作,运输工作和部分体力劳动者<br/>1H：不便分类的其他劳动者<br/>个人商户可修改；<font color="green">示例值：1G</font> |
| prov_id | 经营省 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000 </font>；如修改省市区要级联修改 |
| area_id | 经营市 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100 </font>；如修改省市区要级联修改 |
| district_id | 经营区 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000 ；</font>如修改省市区要级联修改 |
| detail_addr | 经营详细地址 | String | 255 | N | <font color="green">示例值：上海市徐汇区XX路XX号</font> |
| contact_name | 管理员姓名 | String | 30 | N | 默认法人姓名；最大支持15个汉字。<font color="green">示例值：张三</font> |
| contact_email | 管理员电子邮箱 | String | 32 | N | 联系人电子邮箱，需要带@，遵循邮箱格式 ；<font color="green">示例值：huifu@xxx.com </font> |
| service_phone | 客服电话 | String | 32 | N | 支持固话格式，手机格式；默认联系人手机号；<font color="green">示例值：021XXXXXXXX</font> |
| receipt_name | 小票名称 | String | 50 | N | 可以作为POS小票的名称；<font color="green">示例值：汇付商城     </font> |
| <span class="extend fb2718a6_1f40_4973_a313_2f036f049d7a">card_info</span> | *结算卡信息配置* | String |  | N | 商户结算账户信息配置，jsonObject字符串；开通中信E管家结算的银行卡配置在【elec_acct_config】中 |
| settle_agree_pic | 结算协议图片文件 | String | 128 | N | 请填写图片file_id，<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font><br/>可通过[商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)接口获取，文件类型F116 |
| <span class="extend dba26fa3_b022_4ef6_8cca_a2d47c2254dc">cash_config</span> | 取现信息配置 | String |  | N | 商户取现信息配置，jsonArray字符串 |
| <span class="extend 9bece88a_b827_43e3_9cdd_13522c113ecc">settle_config</span> | 结算规则配置 | String |  | N | 商户结算规则配置，jsonObject字符串 |
| mer_url | 商户主页URL | String | 256 | N | 商户主页URL；<font color="green">示例值：https://paas.huifu.com/ </font> |
| mer_icp | 商户ICP备案编号 | String | 50 | N | 商户ICP备案编号或网站许可证号；<font color="green">示例值：沪ICP备06046402号-28</font> |
| <span class="extend 6a869eb0_5018_4e4b_9c46_aa90386b322c">beneficiary_info</span> | 受益人列表 | String |  | N | jsonArray字符串 |
| <span class="extend a75d4171_940e_4512_aa2f_4960a6b03c8b">sign_user_info</span> | 签约人 | String |  | C | jsonObject格式；agreement_info中选择电子签约时必填；个人商户填本人信息。 |
| <span class="extend 78385a9b_9223_47a4_999b_9b1b119edf53">agreement_info</span> | 协议信息 | String |  | N | jsonObject格式；[签约协议材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx)<br/>若未签署过协议的情况下，调用该接口时必填 ，且注册地址或经营地址为如下地区（江苏省、浙江省、湖南省、湖北省、云南省、贵州省、陕西省、河南省、吉林省、黑龙江省、福建省、海南省、重庆市、青海省、宁夏回族自治区）开通银联二维码或刷卡业务不支持挂网协议；<br/>若已签署过纸质或电子协议下，调用该接口时必填，且只可以选择纸质或电子协议；<br/>若已签署过挂网协议下，调用该接口时，选填。 |
| license_pic | 营业执照图片 | String | 64 | N | 企业商户可改。通过[商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)接口获取file_id，[参考文件类型](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)：F07；**注意执照不能是过期的**；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| auth_entrust_pic | 授权委托书 | String | 64 | N | 通过[商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)接口获取file_id，[参考文件类型](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)：F15；请填写图片file_id，[下载模板](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/12%E3%80%90%E5%95%86%E6%88%B7%E3%80%91%E6%8E%88%E6%9D%83%E7%BB%93%E7%AE%97%E5%A7%94%E6%89%98%E4%B9%A6%EF%BC%88%E5%AF%B9%E7%A7%81%E7%BB%93%E7%AE%97%EF%BC%89%EF%BC%88%E7%BA%B8%E8%B4%A8%E5%90%88%E5%90%8C%E7%89%88%EF%BC%89.docx)。<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| scene_type | 场景类型 | String | 8 | N | ONLINE：线上场景，OFFLINE：线下场景，ALL：线上线下；<font color="green">示例值：ALL</font> |
| store_header_pic | 店铺门头照 | String | 64 | N | 文件类型：F22；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font><br/>微信/支付宝实名认证个人商户，门头照也使用此字段； <br/>门店场所：提交门店门口照片，要求招牌清晰可见; <br/>小微商户流动经营/便民服务：提交经营/服务现场照片 |
| store_indoor_pic | 店铺内景/工作区域照 | String | 64 | N | 文件类型：F24；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font><br/>微信/支付宝实名认证个人商户，内景照也使用此字段； <br/>门店场所：提交店内环境照片 <br/>小微商户流动经营/便民服务：可提交另一张经营/服务现场照片 |
| store_cashier_desk_pic | 店铺收银台/公司前台照 | String | 64 | N | 文件类型：F105；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| <span class="extend 26c38bfc_8a0a_4164_ab9d_1356ae29829f">extended_material_list</span> | 扩展资料包 | String |  | N | jsonArray字符串。根据要求上传补充相关材料 |
| async_return_url | 异步通知地址 | String | 128 | N | 审核结果消息接收地址，为空时不推送消息<br/><font color="green">示例值：http://service.example.com/to/path</font> |
| <span class="extend 75b29b93_bbc7_466c_9a0f_bfaa4aa0c695">elec_acct_config</span> | 斗拱e账户功能配置 | String |  | N | 用于总部商户、下级商户配置斗拱E账户功能 |
| <span class="extend 16058af9_240b_4d88_ad2b_53a26b0709f2">share_holder_info_list</span> | 股东信息 | String |  | N | jsonArray字符串；全域资金业务新网银行必填 |
| ext_mer_id | 外部商户号 | String | 64 | N | 支持关联外部商户系统中的商户号；<font color="green">示例值：HF100001</font> |
| remark | 备注 | String | 300 | N | 备注内容；<font color="green">示例值：华东分公司</font> |
| activated_products | 产品大类 | String |  | N |  01：一体化收款产品，02：账户与资金产品，03：业财数通产品；不传为空 <font color="green">示例值：01,02,03</font> |

<!-- extend:start -->
<!-- div:extend-table fb2718a6_1f40_4973_a313_2f036f049d7a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 结算账户类型 | String | 1 | Y | 0：对公账户 1：对私法人账户 2：对私非法人账户 <font color="green">示例值：0</font><br/>个人商户/用户不支持填写对公账户和对私非法人账户。<br/>若涉及结算账户类型变更，请前往 [企业商户结算人变更](https://paas.huifu.com/open/doc/api/#/shgl/shjj/changeofpayee)了解意愿核实方案 |
| card_name | 结算账户名 | String | 128 | Y | <font color="green">示例值：上海汇付支付有限公司</font><br/> 当card_type=0时填写企业名称，，**企业非同名时，需要在extended_material_list中额外上传非同名结算证明材料，文件枚举：F516**<br/> 当card_type=1时填写法人姓名，**对私法人结算银行户名与法人姓名必需一致**；<br/> 当card_type=2时填写非法人姓名<br/> |
| card_no | 结算账号 | String | 32 | Y | 结算账号，结算银行卡号，为避免资金结算失败，请正确填写；<br/><font color="green">示例值：98140008801800008888</font><br/>注意：系统会验证卡号所属银行，请准确填写；<!--建议对私结算也填写bank_code，提高进件成功率；李阳说对私结算不要填bank_code，会影响成功率--> |
| prov_id | 银行所在省 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000 </font>；如修改省市要级联修改 |
| area_id | 银行所在市 | String | 8 | Y | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100 </font>；如修改省市要级联修改 |
| branch_code | 支行联行号 | String | 12 | C | 当card_type=0时必填。参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) 当card_type=0时必填， 当card_type=1或2时非必填 <font color="green">示例值：102290026507</font> |
| cert_type | 持卡人证件类型 | String | 2 | C | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。<br/> 当card_type=0时为空， 当card_type=1或2时必填； <font color="green">示例值：00</font><br/>持卡人证件类型04、11需要补充 F101【结算人】港澳台居民来往内地通行证<br/>持卡人证件类型13需要补充 F513【结算人】外国人居留证<br/>持卡人证件类型14、15需要补充 F514【结算人】港澳台居住证<br/>其它持卡人证件类型补充F102【结算人】其它证件材料<br/>补充材料填写在extended_material_list 扩展资料包中 |
| cert_no | 持卡人证件号码 | String | 32 | N | 持卡人证件号码，如持卡人证件类型为00：身份证，则填写身份证号码；<font color="green">示例值：310112200001018888</font><br/>当card_type=0时为空<br/>当card_type=1或2时必填<br/>年龄不能小于18岁且不能大于80岁； |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | C | 0：非长期有效, 1：长期有效, <font color="green">示例值：0</font><br/>当card_type=0时为空； 当card_type=1或2时必填； |
| cert_begin_date | 持卡人证件有效期开始日期 | String | 8 | C | 日期格式：yyyyMMdd，以北京时间为准； 当card_type=0时为空， 当card_type=1或2时必填， <font color="green">示例值：20220125 </font> |
| cert_end_date | 持卡人证件有效期截止日期 | String | 8 | C | 日期格式：yyyyMMdd，以北京时间为准。<font color="green">示例值：20220125</font><br/>  当cert_validity_type=0时必填；当cert_validity_type=1时为空 |
| reg_acct_pic | 开户许可证 | String | 128 | C | 开户许可证图片文件，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F08；<br/>企业商户需要，结算账号为对公账户必填；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| legal_cert_front_pic | 法人身份证人像面 | String | 128 | C | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F02；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 </font> |
| legal_cert_back_pic | 法人身份证国徽面 | String | 128 | C | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F03；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| settle_card_front_pic | 银行卡卡号面 | String | 128 | C | 银行卡卡号面图片文件对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F13；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| settle_cert_front_pic | 结算人身份证人像面 | String | 128 | C | 对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F55；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| settle_cert_back_pic | 结算人身份证国徽面 | String | 128 | C | 对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F56；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529  </font> |
| mp | 结算人手机号 | String | 11 | N | 需为11位数字；<font color="green">示例值：18611111111 </font><br/>当card_type=0时为空; 当card_type=1或2时可修改；开通全域资金管理功能可修改； |
| authentication_type | 变更结算人核验方式 | String | 1 | N | 0：短信验证码 （不填默认）<br/>1：短信链接 <br/>2：材料核实<br/><font  color="green">示例值：1</font>；当审核结果、意愿核验、电子协议签约均通过时，结算变更生效。 |
| verify_code | 短信验证码 | String | 6 | C | 结算卡、结算人变更需要短信验证码；当【变更结算人核验方式 = 0】时必填。 请先调用商户短信发送接口；示例值：851249 |
| authentication_person_type | 核验人类型 | String | 1 | C | 当【变更结算人核验方式 = 1】时必填。企业用户选择0:法人，1:原持卡人；<font  color="green">示例值：0</font> |
| authentication_person_mobile | 核验人手机号 | String | 11 | C | 当【变更结算人核验方式 = 1】时必填。请根据核验人类型传入核验人实名手机号。<font  color="green">示例值：13911111111</font> |
| acct_ids | 适用子账户 | String | 128 | N | 结算卡适用子账户，多个用逗号隔开；示例值：D02348323,D01236743 |
| is_settle_default | 默认结算卡标志 | String | 1 | N | 是否为默认结算卡标志；Y:是 N:否；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table dba26fa3_b022_4ef6_8cca_a2d47c2254dc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 状态 | String | 1 | Y | 1:开通 0:关闭 ；<font color="green">示例值：1</font> |
| cash_type | 业务类型 | String | 2 | Y | <!--无论开关都要送值-->D0：当日到账；当日交易资金当天可取现到账；<br/>T1：下个工作日到账；<br/>D1：下个自然日到账；<br/>DM：当日到账；到账资金不包括当天的交易资金；<br/> <font color="green">示例值：T1</font> |
| fix_amt | 提现手续费（固定/元） | String | 6 | C | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；<font color="green">示例值：1.00</font><br>注：当cash_type=D1时为节假日取现手续费 |
| fee_rate | 提现手续费率（%） | String | 6 | C | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate<br>2、当cash_type=D1时为节假日取现手续费 |
| weekday_fix_amt | D1工作日取现手续费固定金额 | String | 6 | C | 单位元，需保留小数点后两位。不收费请填写0.00；<font color="green">示例值：1.00</font><br>cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| weekday_fee_rate | D1工作日取现手续费率 | String | 6 | C | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：2</font> |
| out_fee_huifu_id | 手续费承担方 | String | 18 | N | 手续费外扣时必需指定手续费承担方ID；<font color="green">示例值：6666000123123123</font> |
| out_fee_acct_type | 手续费外扣的账户类型 | String | 2 | N | 01-基本户，02-现金户，05-充值户；不填默认01；<font color="green">示例值：01</font> |
| is_priority_receipt | 是否优先到账 | String | 1 | N | Y：是 ，N：否。不填，默认值为否。仅在取现类型配置为D1 和 T1 时生效。<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9bece88a_b827_43e3_9cdd_13522c113ecc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_status | 结算开关 | String | 1 | Y | 1:开通 0:关闭；<font color="green">示例值：1</font> |
| settle_cycle | 结算周期 | String | 2 | Y | D1：下个自然日结算， T1：下个工作日结算；TS:笔笔结算； <font color="green">示例值：T1</font> |
| min_amt | 起结金额 | String | 17 | N | settle_cycle为TS时不填。账户余额大于等于起结金额才会发起结算。不传则不设置起结金额；<br/>单位元，小数点后两位，取值范围[0.00，99999999999.99]。<font color="green">示例值：1000.00</font> |
| remained_amt | 留存金额 | String | 17 | N | settle_cycle为TS时不填。该部分资金不会结算。不传则不设置留存金额 ；<br/>单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。<font color="green">示例值：1000.00</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 结算摘要，可自定义结算打款备注，不填默认为空；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；<font color="green">示例值：汇付商城业务</font> |
| out_settle_flag | 手续费外扣标记 | String | 1 | N | 1:外扣：结算时，从out_settle_huifuid账户扣手续费<br/>2:内扣：从结算金额中扣手续费，默认为内扣；<font color="green">示例值：2</font> |
| out_settle_huifuid | 结算手续费外扣商户号 | String | 18 | C | 结算手续费外扣商户号，填写承担手续费的汇付商户号；当out_settle_flag=1时必填，否则非必填；<font color="green">示例值：6666000123123123</font> |
| out_settle_acct_type | 结算手续费外扣时的账户类型 | String | 2 | N | 结算手续费外扣账户类型；01：基本户（不填默认取值）；02：现金户；05：充值户；09：营销户；<font color="green">示例值：01</font> |
| settle_batch_no | 结算批次号 | String | 16 | N | settle_cycle为TS时不填。结算批次号，按指定结算批次号进行资金结算；<font color="green">示例值：0</font>；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| is_priority_receipt | 是否优先到账 | String | 1 | N | settle_cycle为TS时不填。当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效<br/> Y：是，N：否，<font color="green">示例值：Y</font> |
| settle_time | 自定义结算处理时间 | String | 6 | N | settle_cycle为TS时不填。当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定<br/>到账时间，格式：HHmmss；<font color="green">示例值：103000</font> |
| fixed_ratio | 节假日结算手续费率 | String | 6 | C | settle_cycle为D1、TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<br>settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；<font color="green">示例值：0.05</font> |
| constant_amt | 节假日结算手续费固定金额 | String | 15 | C | settle_cycle为D1、TS时必填。单位元，需保留小数点后两位。不收费请填写0.00；<br>settle_cycle结算周期为D1时，遇节假日按此费率结算 ；<br/> <font color="green">示例值：1.00</font> |
| workday_fixed_ratio | 工作日结算手续费率 | String | 6 | N | settle_cycle为TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；<font color="green">示例值：0.05</font> |
| workday_constant_amt | 工作日结算手续费固定金额 | String | 15 | N | settle_cycle为TS时必填。单位元，需保留小数点后两位。不填默认为0.00；<font color="green">示例值：1.00</font> |
| settle_pattern | 结算方式 | String | 2 | N | settle_cycle为TS时不填。结算方式，批次结算指按照结算批次号进行资金结算，定时结算是指按照指定到账时间进行资金结算，不填默认P0：批次结算； P0：批次结算 ，P1：定时结算(建议选P0和P2)，P2:批次定时结算，E1:中信E管家 示例值：P1 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6a869eb0_5018_4e4b_9c46_aa90386b322c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bo_id | 受益唯一ID | String | 32 | N | 新增受益人时无需填写；<font color="green">示例值：6666000123123123</font> |
| bo_name | 受益人名称 | String | 40 | Y | <font color="green">示例值：张三</font> |
| bo_type | 受益人证件类型 | String | 2 | Y | 00:身份证<br/> 01:护照<br/> 02:军官证<br/> 03:士兵证<br/> 04:回乡证<br/> 05:户口本<br/> 06:外国护照<br/> 07:其他<br/> 08:暂住证<br/> 09:警官证<br/> 10:文职干部证<br/> 11:港澳同胞回乡证<br/> 12:营业执照<br/><font color="green">示例值：00</font> |
| bo_no | 受益人证件号 | String | 50 | Y | <font color="green">示例值：3209219851202732</font> |
| bo_date_start | 受益人证件有效期开始时间 | String | 8 | Y | <font color="green">示例值：20210606</font> |
| bo_deadline | 受益人证件有效期结束时间 | String | 8 | Y | <font color="green">示例值：20290606</font>；若证件有效期为长期，请填写：29991231；要求结束时间大于开始时间； |
| bo_address | 受益人地址 | String | 500 | Y | <font color="green">示例值：上海徐汇区共富一路55号401室</font>； |
| bo_mobile_no | 受益人手机号 | String | 11 | C | 开通全域资金管理业务时必填；<font color="green">示例值：13911111111</font> |
| final_beneficiary_mode | 最终受益人受益方式 | String | 3 | C | A01：直接或间接控股25%（含）以上 <br/>A02：通过人事、财务等其他方式对公司进行控制 <br/>A03：高级管理人员 <br/>A04：法人或公司负责人 <br/>A05：其他<br/><font color="green">示例值：A01</font> <br/>开通全域资金管理业务时必填 |
| bo_stat | 受益人有效标识 | String | 10 | N | active：有效，inactive：无效 <font color="green">示例值：active</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a75d4171_940e_4512_aa2f_4960a6b03c8b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 签约人类型 | String | 7 | Y | LEGAL-法人，对公结算或对私法人结算时可选法人签约；<br/>CONTACT-联系人，对公结算可选联系人（经办人）签约；<br/>OTHER-其他，对私非法人结算选“其他”，必须是结算人；<br/><font color="green">示例值：LEGAL</font> |
| name | 姓名 | String | 32 | N | 签约人类型=其他，必填；<font color="green">示例值：张三</font> |
| mobile_no | 手机号 | String | 11 | N | 签约人类型=法人/其他 ，必填；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；<font color="green">示例值：13917463536</font> |
| cert_no | 身份证 | String | 32 | N | 签约人类型=联系人/其他，必填；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；<font color="green">示例值：320946195712025082</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 78385a9b_9223_47a4_999b_9b1b119edf53-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_type | 协议类型 | String | 1 | Y | 0-电子协议，1-纸质协议，3-挂网协议<font color="green">示例值：3</font> |
| agreement_url | 挂网协议地址 | String | 256 | C | 挂网协议必填；**必须按示例值填写**，<font color="green">示例值：https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm</font>； |
| agree_begin_date | 纸质协议开始日期 | String | 8 | N | <font color="green">示例值：20220606</font>； |
| agree_end_date | 纸质协议结束日期 | String | 8 | N | <font color="green">示例值：20230606</font>；要求结束时间大于开始时间； |
| agreement_async_return_url | 电子协议异步通知地址 | String | 128 | N | 示例值：http://service.example.com/to/path |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 26c38bfc_8a0a_4164_ab9d_1356ae29829f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_id | 文件id | String | 64 | Y | 请填写图片file_id，可通过 商户图片上传 接口获取； 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| file_type | 文件类型 | String | 64 | Y | 参见文件类型说明；示例值：F01 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 75b29b93_bbc7_466c_9a0f_bfaa4aa0c695-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子账户开关 | String | 1 | Y | 电子账户开通总开关；0:关闭 1:开通；<font color="green">示例值：1</font> |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家；<font color="green">示例值：01</font> |
| cash_fee_party | 电子账户提现手续费承担方 | String | 1 | C | 下级商户必填；1:总部 2:其他；<font color="green">示例值：1</font> |
| scene | 场景类型 | String | 3 | Y | 必填；与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；<font color="green">示例值：001</font> |
| role_type | 角色类型 | String | 6 | Y | 角色编号必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；<font color="green">示例值：001001</font> |
| <span class="extend 561f928c_1a2f_44d6_9871_40aa2c5ac8e2">elec_card_list</span> | 银行卡信息 | Object |  | N | jsonArray字符串 |
| elec_acct_sign_seq_id | 中信签约短信流水号 | String | 64 | N | <font color="green">示例值：EMSSBPG2504284593690058431260676</font> |
| sign_success_flag | 签约成功标志 | String | 1 | N | Y：成功 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 561f928c_1a2f_44d6_9871_40aa2c5ac8e2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)示例值：310000 |
| area_id | 银行所在市 | String | 6 | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310100 |
| bank_code | 银行编码 | String | 8 | Y | [参考银行编码；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) 示例值：01020000 |
| branch_code | 支行联行号 | String | 12 | Y | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| branch_name | 支行名称 | String | 64 | Y | 示例值：中国工商银行上海市中山北路支行 |
| card_name | 结算账户名 | String | 128 | Y | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| card_no | 银行卡号 | String | 32 | Y | 示例值：98140008801800008888 |
| card_type | 卡类型 | String | 1 | Y | 0:对公 1:对私法人；示例值：0 |
| default_cash_flag | 默认卡标识 | String | 1 | N | 0：非默认卡 1：默认卡(不填，默认为0) |
| mp | 银行绑定手机号 | String | 11 | C | 个人必填 |
| auth_version | 用户授权协议版本号 | String | 64 | C | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| auth_no | 用户授权协议号 | String | 64 | C | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 16058af9_240b_4d88_ad2b_53a26b0709f2-table -->
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


#### 请求示例

```json
{
        "sys_id": "6666000021000120",
        "product_id": "HUIFENQI",
        "data": {
                "req_seq_id": "20211213105924999810140",
                "req_date": "20220119",
                "product_id": "HUIFENQI",
                "huifu_id": "6666000107932702",
                "upper_huifu_id": "6666000021000000",
                "short_name": "尼博网络",
                "license_validity_type": "0",
                "license_begin_date": "20200814",
                "license_end_date": "20400813",
                "reg_prov_id": "310000",
                "reg_area_id": "310100",
                "reg_district_id": "310120",
                "reg_detail": "台州市宜山路700解放2路715",
                "legal_name": "沈荣",
                "legal_cert_type": "00",
                "legal_cert_no": "320923199111206319",
                "legal_cert_validity_type": "0",
                "legal_cert_begin_date": "20200814",
                "legal_cert_end_date": "20400813",
                "contact_name": "我是联系人",
                "contact_email": "mei.zhang@huifu.com",
                "receipt_name": "小票上的名称",
                "mcc": "5411",
                "service_phone": "15556622368",
                "prov_id": "310000",
                "area_id": "310100",
                "district_id": "310105",
                "detail_addr": "徐州市徐汇区宜山路7497号",
                "card_info": "{\"bank_code\":\"01020000\",\"cert_type\":\"00\",\"cert_no\":\"320923199111206319\",\"mp\":\"18221987178\",\"prov_id\":\"310000\",\"settle_cert_back_pic\":\"d1451277-85c6-3177-ac3d-a8be47b9ae9d\",\"legal_cert_front_pic\":\"\",\"legal_cert_back_pic\":\"\",\"reg_acct_pic\":\"d1451277-85c6-3177-ac3d-a8be47b9ae9d\",\"card_type\":\"1\",\"area_id\":\"410100\",\"cert_begin_date\":\"20140905\",\"cert_validity_type\":\"0\",\"branch_code\":\"102491002812\",\"settle_card_back_pic\":\"d1451277-85c6-3177-ac3d-a8be47b9ae9d\",\"card_no\":\"1001265009300682579\",\"cert_end_date\":\"20240905\",\"comp_pic2\":\"d1451277-85c6-3177-ac3d-a8be47b9ae9d\",\"branch_name\":\"中国工商银行股份有限公司上海市中山北路支行\",\"comp_pic3\":\"d1451277-85c6-3177-ac3d-a8be47b9ae9d\",\"card_name\":\"万方肖\",\"comp_pic1\":\"d1451277-85c6-3177-ac3d-a8be47b9ae9d\",\"settle_card_front_pic\":\"d1451277-85c6-3177-ac3d-a8be47b9ae9d\",\"settle_cert_front_pic\":\"d1451277-85c6-3177-ac3d-a8be47b9ae9d\"}",
                "cash_config": "[{\"switch_state\":\"1\",\"cash_type\":\"D0\",\"fix_amt\":\"4.00\",\"fee_rate\":\"5.50\"}]",
                "async_return_url": "archer://C_SSPM_NSPOSM_BUSIRESULT",
                "settle_config": "{\"settle_status\":\"1\",\"settle_cycle\":\"T1\",\"out_settle_flag\":\"2\",\"out_settle_acct_type\":\"09\",\"fixed_ratio\":\"0\",\"settle_pattern\":\"P0\",\"settle_batch_no\":\"100\",\"is_priority_receipt\":\"N\",\"constant_amt\":\"0\"}"    
    },
        "sign": "K7IqpKGVWP2VsbpX9Qwwahf+wSYzJTN+d9ufO+PdHOFdnI/bWgUKQFkOG1t1wcrPD/89kOF2KeT76aPxS9W73Ue2Io/R5Zl89zn93cd1WHCC5WrpzaGjaF5m0uSBfF6Vpci56aGhn3ywah/xlEUYVH4i3dWdMr0uGlTYmieXU1o="
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码)；<font color="green">示例值：00000000 </font> |
| resp_desc | 业务返回描述 | String | 512 | Y | <font color="green">示例值：处理成功</font> |
| huifu_id | 商户号 | String | 18 | N | 汇付商户号，状态为审核中时返回；<font color="green">示例值：6666000123123123 </font> |
| apply_no | 申请单号 | String | 18 | N | 商户开户业务申请单号，状态为审核中时返回 ；<br/><font color="green">示例值：2022012500073423</font> |
| token_no | 取现卡序列号 | String | 20 | N | 取现时使用；<font color="green">示例值：10004053462 </font> |


#### 异步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | 参考业务返回码；<font color="green">示例值：00000000</font> |
| sub_resp_desc | 业务返回描述 | String | 512 | N | 业务返回描述；<font color="green">示例值：处理成功</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | 原请求流水号；示例值：2022012614120615001 |
| req_date | 请求日期 | String | 8 | Y | 原请求日期 示例值：20220125 |
| audit_status | 审核结果 | String | 1 | Y | 审核结果；Y：审核通过；N：审核拒绝 ；F：失败；<font color="green">示例值：Y</font> |
| audit_desc | 审核描述 | String | 512 | N | 审核描述，审核人员编辑的审核描述；<font color="green">示例值：审核通过</font> |
| product_id | 产品号 | String | 32 | Y | 汇付分配的产品号；<font color="green">示例值：MCS</font> |
| huifu_id | 商户号 | String | 18 | N | 返回：处理成功时有值，汇付分配的商户号； |
| apply_no | 申请单号 | String | 18 | N | 商户开户业务申请单号，状态为审核中时返回； 示例值：2022012500073423 |
| token_no | 取现卡序列号 | String | 20 | N | 取现时使用；<font color="green">示例值：10004053462</font> |
| notify_type | 通知类型 | String | 1 | N | Z：电子账户；<font color="green">示例值：Z</font> |
| <span class="extend fd7293a9_09d9_4612_88e6_32745c45b2c4">elec_acct_result</span> | 斗拱e账户开通结果 | String |  | N | jsonObject格式；notify_type=Z时返回 |

<!-- extend:start -->
<!-- div:extend-table fd7293a9_09d9_4612_88e6_32745c45b2c4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家；<font color="green">示例值：01</font> |
| bank_status | 电子账户开通状态 | String | 1 | Y | S：成功 F：失败；<font color="green">示例值：S</font> |
| bank_message | 银行信息 | String | 512 | N | 银行信息 |
| sign_agreement_id | 签约协议号 | String | 32 | N | 商户签约中信E管家协议编号； 签约成功才返回<font color="green">示例值：20250428091343030914951566827191</font> |
<!-- extend:end -->


#### 电子协议签署链接异步通知

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y |  |
| sub_resp_desc | 业务返回描述 | String | 512 | N |  |
| req_seq_id | 请求流水号 | String | 32 | Y |  |
| req_date | 请求日期 | String | 8 | Y |  |
| huifu_id | 商户号 | String | 18 | Y |  |
| apply_no | 申请单号 | String | 18 | Y |  |
| <span class="extend 9f0be817_0bc8_4b1f_85fd_006da80b709d">agreement_info_list</span> | 电子协议信息 | String |  | N | 电子协议信息，签署电子协议时返回 |

<!-- extend:start -->
<!-- div:extend-table 9f0be817_0bc8_4b1f_85fd_006da80b709d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_type | _协议类型_ | String | 1 | N | 0-电子协议 |
| agreement_link | 协议签署链 | String | 512 | N |  |
| agreement_no | 协议号 | String | 32 | N | <font color="green">示例值：3245234</font> |
| agreement_name | 协议名称 | String | 128 | N |  |
| con_stat | 签约状态 | String | 2 | N | 电子协议类型会返回以下值： 2：创建合同异常 3：待签约 4：签约中 5：签约完成(电子协议只有签约完成才能做交易) 6：已失效 7：已拒签 8：签约失败 <font color="green">示例值：5</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{  
    "data":{  
        "resp_desc":"审核中",  
        "apply_no":"2022011900390214",  
        "resp_code":"90000000",  
        "huifu_id":"6666000107932702"  
    }  
}  
```
