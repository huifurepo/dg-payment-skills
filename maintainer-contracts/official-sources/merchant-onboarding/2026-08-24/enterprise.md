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
## 企业商户进件

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/basicdata/ent

*最近更新时间：2026.08.07*
### 应用场景

通过此接口在汇付为企业类商户进行基本信息开户。传入企业商户基本资料和图片资料，开通汇付账号，为商户绑定银行卡、配置结算和取现等功能。

**适用对象**   
  企业类商户开通汇付账号并填写基本信息、配置结算和取现等功能，可调用该功能。  
  企业商户包括：
- 政府机构  
- 国营企业  
- 私营企业  
- 外资企业  
- 个体工商户（有营业执照）  
- 其它组织  
- 事业单位  
- 业主委员会

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

| 参数 | 中文名     | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div>| 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

- “必填”字段取值“Y“：必填；“N”：非必填；“C”代表条件必填； 

### **注意** 
- 系统会验证证照号、商户名称、法人姓名、法人证件号的一致性，请正确填写；
- card_info卡信息**对私结算会验证【银行卡户名】【银行卡号】【持卡人证件号码】，请正确上送参数值；**    
- card_info卡信息结算类型是对私法人结算时，持卡人姓名必须与法人姓名相同；
- 请上送utf-8格式的字体，否则影响后期AT入驻；

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号，当日唯一；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，<font color="green">示例值：20220125</font> |
| upper_huifu_id | 渠道商号 | String | 18 | C | 该商户进件完成后归属的渠道商huifu_id；<br/>sys_id主体为渠道商时填写； <br/>sys_id主体为总部商户时选填；<br/><font color="green">示例值：6666000123123123</font> |
| reg_name | 商户名称 | String | 64 | Y | 必须与企业证照上的名称一致；<br/>个体工商户的营业执照如没有名称，名称为“\*”或空，则商户名称应填 “个体户XXX”（XXX为营业执照上经营者姓名），如“个体户张三”，汉字以2个字符计算 ；<br/><font color="green">示例值：上海汇付支付有限公司</font> |
| short_name | 商户简称 | String | 64 | Y | 最少4个字符；会展示在消费账单上；<font color="green">示例值：汇付商城 </font> |
| receipt_name | 小票名称 | String | 50 | Y | 小票名称展示在POS小票上；<font color="green">示例值：汇付商城</font> |
| mer_en_name | 商户英文名称 | String | 256 | N | <font color="green">示例值：huifupay</font> |
| ent_type | 公司类型 | String | 1 | Y | 当use_head_info_flag=Y时不填；<br/>1：政府机构<br/>2：国营企业<br/>3：私营企业<br/>4：外资企业<br/>5：个体工商户<br/>6：其它组织<br/>7：事业单位<br/>9：业主委员会；<br/><font color="green">示例值：1</font>； |
| mcc | 所属行业 | String | 7 | C | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；当use_head_info_flag=Y时不填<br/><font color="green">示例值：5311</font> |
| busi_type | 经营类型 | String | 1 | C | 1：实体，2：虚拟 ；<font color="green">示例值：1</font> ；当use_head_info_flag=Y时不填 |
| scene_type | 场景类型 | String | 8 | Y | ONLINE：线上场景；<br/>OFFLINE：线下场景；<br/>ALL：线上线下；<br/><font color="green">示例值：ALL</font> |
| license_pic | 证照图片 | String | 64 | Y | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F07；**注意执照不能是过期的**； <br/> <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| license_code | 证照编号 | String | 18 | Y | 工商营业执照编号；当use_head_info_flag=Y时不填；<br/>公司类型为业主委员会，输入业主委员会备案证明上负责人的身份证号码；<br/><font color="green">示例值：92650109MA79R8E308</font>； |
| license_type | 证照类型 | String | 32 | N | 参见[机构证照类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E6%9C%BA%E6%9E%84%E8%AF%81%E7%85%A7%E7%B1%BB%E5%9E%8B)说明；默认NATIONAL_LEGAL_MERGE；<font color="green">示例值：NATIONAL_LEGAL</font> |
| license_validity_type | 证照有效期类型 | String | 1 | Y | 0：非长期有效,1：长期有效；当use_head_info_flag=Y时不填<br/><font color="green">示例值：0 </font> |
| license_begin_date | 证照有效期开始日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20220125</font>；当use_head_info_flag=Y时不填 |
| license_end_date | 证照有效期截止日期 | String | 8 | C | 格式：yyyyMMdd。<font color="green">示例值：20220125</font><br/>  当license_validity_type=0时必填；当license_validity_type=1时为空；当use_head_info_flag=Y时不填 |
| found_date | 成立时间 | String | 8 | Y | <font color="green">示例值：20091212</font> |
| reg_capital | 注册资本 | String | 16 | C | 保留两位小数；条件选填，国营企业、私营企业、外资企业、事业单位、其他、集体经济必填，政府机构、个体工商户可为空；<font color="green">示例值：100.00</font> |
| business_scope | 经营范围 | String | 1000 | N | <font color="green">示例值：日用百货、化妆品、珠宝、化工原料及产品(除危险品)、化学品、纺织原料</font> |
| reg_prov_id | 注册省 | String | 6 | N | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)  ；<font color="green">示例值：310000</font>；当use_head_info_flag=Y时不填 |
| reg_area_id | 注册市 | String | 6 | N | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)  ；<font color="green">示例值：310100</font>；当use_head_info_flag=Y时不填 |
| reg_district_id | 注册区 | String | 6 | Y | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310101</font>；当use_head_info_flag=Y时不填 |
| reg_detail | 注册详细地址 | String | 255 | Y | 商户注册地址或营业执照住所，汉字以2个字符计算  ；<br/><font color="green">示例值：上海市徐汇区XX路XX号</font><br/>当use_head_info_flag=Y时不填 |
| prov_id | 经营省 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)   ；<font color="green">示例值：310000</font> |
| area_id | 经营市 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font> |
| district_id | 经营区 | String | 6 | Y | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)    ；<font color="green">示例值：310101</font> |
| detail_addr | 经营详细地址 | String | 256 | C | scene_type=OFFLINE/ALL时必填；<br/><font color="green">示例值：上海市徐汇区XX路XX号</font> |
| legal_name | 法人姓名 | String | 32 | Y | 法人或负责人姓名，最大支持16个汉字；<br/>注意有名字中有“·”时要与银行账号名一致；<br/><font color="green">示例值：张三</font>；<br/>当use_head_info_flag=Y时不填 |
| legal_cert_type | 法人证件类型 | String | 2 | Y | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》；<font color="green">示例值：00</font><br/>当use_head_info_flag=Y时不填<br/>开通全域资金管理功能只支持法人证件类型是身份证；<br/>法人证件类型04、11、14需要补充 F31【法人】港澳台居民来往内地通行证<br/>法人证件类型13需要补充F511【法人】外国人居留证<br/>法人证件类型15需要补充F512【法人】港澳台居住证<br/>其它法人证件类型补充F32【法人】其它证件材料<br/>补充材料填写在extended_material_list 扩展资料包中 |
| legal_cert_no | 法人证件号码 | String | 32 | Y | 如法人证件类型为00：身份证，则填写身份证号码；<br/>当use_head_info_flag=Y时不填；年龄不能小于18岁且不能大于80岁；<br/><font color="green">示例值：310112200001018888</font>； |
| legal_cert_validity_type | 法人证件有效期类型 | String | 1 | Y | 1：长期有效；0：非长期有效   ；<font color="green">示例值 ：0</font> |
| legal_cert_begin_date | 法人证件有效期开始日期 | String | 8 | Y | 日期格式：yyyyMMdd，<font color="green">示例值：20220125</font>；当use_head_info_flag=Y时不填 |
| legal_cert_end_date | 法人证件有效期截止日期 | String | 8 | C | 日期格式：yyyyMMdd， <font color="green">示例值：20220125</font><br/>当legal_cert_validity_type=0时必填；<br/>当legal_cert_validity_type=1时为空；<br/>当use_head_info_flag=Y时不填 |
| legal_mobile_no | 法人手机号 | String | 11 | N | <font color="green">示例值：13911111111</font>；全域资金业务必填； |
| legal_addr | 法人证件地址 | String | 256 | Y | <font color="green">示例值：上海市徐汇区宜山路700号普天信息产业园2期C5栋</font> |
| legal_cert_back_pic | 法人身份证国徽面 | String | 64 | Y | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F03；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| legal_cert_front_pic | 法人身份证人像面 | String | 64 | Y | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F02；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| <span class="extend 561065db_e4d0_4304_b2cb_a7ef7b6b3d34">beneficiary_info</span> | 受益人列表 | String |  | N | jsonArray字符串 |
| contact_name | 管理员姓名 | String | 128 | N | 默认法人姓名；<font color="green">示例值：张三</font> |
| contact_mobile_no | 管理员手机号 | String | 11 | Y | 需为11位数字  ；<font color="green">示例值：18611111111</font> |
| contact_email | 管理员电子邮箱 | String | 32 | Y | 需要带@，遵循邮箱格式；<br/><font color="green">示例值：huifu@xxx.com</font> |
| sms_send_flag | 商户通知标识 | String | 1 | N | 进件成功后通知商户联系人，<br/>M：发送短信通知；<br/>E：发送邮件通知；<br/>A：短信、邮件都通知；<br/>为空：不作通知。 <br/><font color="green">示例值：M</font> |
| login_name | 管理员账号 | String | 32 | Y | 用于商户平台登录。全局唯一。支持英文、数字、下划线，区分大小写  ；<font color="green">示例值：huifu001</font> |
| service_phone | 客服电话 | String | 32 | N | 默认联系人手机号；<font color="green">示例值：021XXXXXXXX</font> |
| reg_acct_pic | 开户许可证 | String | 64 | C | 企业商户需要，结算账号为对公账户必填；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F08；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| <span class="extend ca68ad1f_4bfd_4386_8fc0_16b2ff1c2971">card_info</span> | 银行卡信息配置 | String |  | Y | 商户银行账户信息配置，jsonObject字符串 ；开通中信E管家结算的银行卡配置在【elec_acct_config】中 |
| <span class="extend 3c7587e7_8f47_4bb6_af7a_8f85d462289c">settle_config</span> | 结算业务配置 | String |  | N | 商户结算规则配置，jsonObject字符串 |
| settle_card_front_pic | 银行卡卡号面 | String | 64 | C | **对私必填**。通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F13；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| settle_cert_back_pic | 持卡人身份证国徽面 | String | 64 | C | **对私必填**。通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F56；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| settle_cert_front_pic | 持卡人身份证人像面 | String | 64 | C | **对私必填**。通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F55；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| auth_entrust_pic | 授权委托书 | String | 64 | C | **对私非法人、对公非同名结算必填**；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F15；开通银行电子账户（中信E管家）需提供F520；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| <span class="extend efd9c909_f73f_4462_b999_86f4e61a2087">cash_config</span> | 取现业务配置 | String |  | N | 商户取现信息配置，jsonArray字符串； |
| head_office_flag | 商户身份 | String | 1 | N | 1：总部商户， 0：下级商户；不传默认普通商户。<font color="green">示例值：0</font><br/>开通下级商户时，所选的上级商户需要有开通商户权限，需先调用“[开通下级商户权限配置接口](https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt_xjshpz)” |
| use_head_info_flag | 使用上级资料信息 | String | 1 | N | Y:是 N：否；<font color="green">示例值：Y</font><br/>选Y则部分信息复用上级，复用字段：<br/>license_code-营业执照编号,<br/>license_validity_type-营业执照有效期类型,<br/>license_begin_date-营业执照有效期开始日期,<br/>license_end_date-营业执照有效期截止日期,<br/>reg_prov_id-注册省,<br/>reg_area_id-注册市,<br/>reg_district_id-注册区,<br/>reg_detail- 注册详细地址,<br/>legal_name- 法人姓名,<br/>legal_cert_type-法人证件类型,<br/>legal_cert_no-法人证件号码,<br/>legal_cert_validity_type-法人证件有效期类型,<br/>legal_cert_begin_date-法人证件有效期开始日期,<br/>legal_cert_end_date-法人证件有效期截止日期,<br/>busi_type-经营类型,<br/>ent_type-公司类型,<br/>mcc-所属行业 |
| head_huifu_id | 上级汇付Id | String | 18 | C | 如果head_office_flag=0，则字段必填，如果head_office_flag=1，上级汇付Id不可传<br/>如果headOfficeFlag=0，useHeadInfoFlag=Y,且head_huifu_id不为空则基本信息部分复用上级的基本信息。<br/><font color="green">示例值：6666000123123123</font> |
| mer_url | 商户主页URL | String | 256 | N | 商户主页URL  ；<font color="green">示例值：https://paas.huifu.com/</font> |
| mer_icp | 商户ICP备案编号 | String | 50 | C | 商户ICP备案编号或网站许可证号；<font color="green">示例值：沪ICP备06046402号-28 </font><br/>类型为PC网站时，且为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填 |
| store_header_pic | 店铺门头照 | String | 64 | C | scene_type字段含有线下场景时必填；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F22；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font><br/>微信/支付宝实名认证个人商户，门头照也使用此字段； <br/>门店场所：提交门店门口照片，要求招牌清晰可见; <br/>小微商户流动经营/便民服务：提交经营/服务现场照片 |
| store_indoor_pic | 店铺内景/工作区域照 | String | 64 | C | scene_type字段含有线下场景时必填；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F24；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font><br/>微信/支付宝实名认证个人商户，内景照也使用此字段； <br/>门店场所：提交店内环境照片 <br/>小微商户流动经营/便民服务：可提交另一张经营/服务现场照片 |
| store_cashier_desk_pic | 店铺收银台/公司前台照 | String | 64 | C | scene_type字段含有线下场景时必填；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F105；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font><br/>微信/支付宝实名认证个人商户，内景照也使用此字段； |
| ext_mer_id | 外部商户号 | String | 64 | N | 支持关联外部商户系统中的商户号；<font color="green">示例值：HF100001</font> |
| remarks | 备注 | String | 300 | N | 备注内容；<font color="green">示例值：华东分公司</font> |
| async_return_url | 异步请求地址 | String | 120 | N | 审核结果消息接收地址，为空时不推送消息；<br/><font color="green">示例值：http://service.example.com/to/path</font> |
| <span class="extend d6dd0dfd_6c4a_4d50_9bb6_9720e7ceeeec">elec_acct_config</span> | 斗拱e账户功能配置 | String |  | N | jsonObject字符串；用于下级商户配置银行电子账户功能 |
| <span class="extend 548b3b06_b06f_4332_8faa_ca24b1d24389">share_holder_info_list</span> | 股东信息 | String |  | N | jsonArray字符串；全域资金业务新网银行必填 |
| <span class="extend a74b90ea_e018_4ee7_b48d_29d3ef662b00">extended_material_list</span> | 扩展资料包 | String |  | N | jsonArray字符串；根据要求上传补充相关材料 |
| activated_products | 产品大类 | String |  | N |   01：一体化收款产品，02：账户与资金产品，03：业财数通产品；不传为空 <font color="green">示例值：01,02,03</font> |
| <span class="extend 0ea6b7e9_c863_4e61_a115_f6781c247861">material_card_info</span> | 对公卡信息 | Object |  | N | jsonObject字符串；商户对公账户信息配置，当非个体工商户的企业商户，card_info选择对私结算（含法人、非法人）时，需补充对公同名账户信息 |

<!-- extend:start -->
<!-- div:extend-table 561065db_e4d0_4304_b2cb_a7ef7b6b3d34-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bo_name | 受益人名称 | String | 40 | Y | <font color="green">示例值：张三</font> |
| bo_type | 受益人证件类型 | String | 2 | Y | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》以及12:营业执照；<font color="green">示例值：12</font> |
| bo_no | 受益人证件号 | String | 50 | Y | <font color="green">示例值：3209219851202732</font> |
| bo_date_start | 受益人证件有效期开始时间 | String | 8 | Y | <font color="green">示例值：20210606</font> |
| bo_dead_line | 受益人证件有效期结束时间 | String | 8 | Y | <font color="green">示例值：20290606</font>；若证件有效期为长期，请填写：29991231；要求结束时间大于开始时间； |
| bo_address | 受益人证件地址 | String | 500 | Y | <font color="green">示例值：上海徐汇区共富一路55号401室</font>； |
| bo_mobile_no | 受益人手机号 | String | 11 | C | 开通全域资金管理业务时必填；<font color="green">示例值：13911111111</font> |
| final_beneficiary_mode | 最终受益人受益方式 | String | 3 | C | A01：直接或间接控股25%（含）以上 <br/>A02：通过人事、财务等其他方式对公司进行控制 <br/>A03：高级管理人员 <br/>A04：法人或公司负责人 <br/>A05：其他<br/><font color="green">示例值：A01</font><br/>开通全域资金管理业务时必填 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ca68ad1f_4bfd_4386_8fc0_16b2ff1c2971-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 银行账户类型 | String | 1 | Y | 0：对公账户 1：对私法人账户 2：对私非法人账户 <font color="green">示例值：0</font> |
| card_name | 银行账户名 | String | 128 | Y | <font color="green">示例值：上海汇付支付有限公司</font><br/> 当card_type=0时填写企业名称，**企业非同名时，需要在extended_material_list中额外上传非同名结算证明材料，文件枚举：F516**<br/> 当card_type=1时填写法人姓名，**对私法人银行账户名与法人姓名必需一致**；<br/> 当card_type=2时填写非法人姓名<br/> |
| card_no | 银行账号 | String | 32 | Y | <br/><font color="green">示例值：98140008801800008888</font><br/>注意：**系统会验证卡号所属银行**，请准确填写； |
| prov_id | 银行所在省 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font>；如修改省市要级联修改 |
| area_id | 银行所在市 | String | 6 | Y | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font>；如修改省市要级联修改 |
| branch_code | 联行号 | String | 12 | C | 当card_type=0时必填，参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) 当card_type=0时必填， 当card_type=1或2时非必填 <br/><font color="green">示例值：102290026507</font> |
| cert_type | 持卡人证件类型 | String | 2 | C | 持卡人证件类型，参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。<br/> 当card_type=0时为空， 当card_type=1或2时必填； <font color="green">示例值：00</font><br/>持卡人证件类型04、11需要补充 F101【结算人】港澳台居民来往内地通行证<br/>持卡人证件类型13需要补充 F513【结算人】外国人居留证<br/>持卡人证件类型14、15需要补充 F514【结算人】港澳台居住证<br/>其它持卡人证件类型补充F102【结算人】其它证件材料<br/>补充材料填写在extended_material_list 扩展资料包中 |
| cert_no | 持卡人证件号码 | String | 32 | C | 对私必填；年龄不小于18岁且不能大于80岁；如持卡人证件类型为00：身份证，则填写身份证号码 ；<br/><font color="green">示例值：310112200001018888</font> |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | N | 1:长期有效  0:非长期有效；<font color="green">示例值：0</font> |
| cert_begin_date | 持卡人证件有效期开始日期 | String | 8 | N | 日期格式：yyyyMMdd，<font color="green">示例值：20220125</font> |
| cert_end_date | 持卡人证件有效期截止日期 | String | 8 | C | 日期格式：yyyyMMdd，<font color="green">示例值：20220125</font><br/>  当cert_validity_type=0时必填；当cert_validity_type=1时为空 |
| mp | 银行卡绑定手机号 | String | 11 | N | 11位数字，开通全域资金管理功能必填； <font color="green">示例值：18611111111</font> |
| is_settle_default | 默认结算卡标志 | String | 1 | N | 是否为默认结算卡标志；Y:是 N:否(为空默认)；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3c7587e7_8f47_4bb6_af7a_8f85d462289c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_cycle | 结算周期 | String | 2 | Y | D1：下个自然日结算， T1：下个工作日结算；TS:笔笔结算； <font color="green">示例值：T1</font> |
| min_amt | 起结金额 | String | 14 | N | settle_cycle为TS时不填。账户余额大于等于起结金额才会发起结算；<br/>单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。<br/><font color="green">示例值：1000.00</font> |
| remained_amt | 留存金额 | String | 14 | N | settle_cycle为TS时不填。该部分资金不会结算。<br/>单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。<br/><font color="green">示例值：1000.00</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 可自定义结算打款备注，不填默认为空；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；<font color="green">示例值：汇付商城业务</font> |
| out_settle_flag | 手续费外扣标记 | String | 1 | N | 1:外扣，结算时从out_settle_huifuid账户扣手续费 <br/>2:内扣，从结算金额中扣手续费，默认为内扣<br/><font color="green">示例值：2</font> |
| out_settle_huifuid | 结算手续费外扣商户号 | String | 18 | C | 填写承担手续费的汇付商户号；当out_settle_flag=1时必填，否则非必填；<font color="green">示例值：6666000123123123</font> |
| out_settle_acct_type | 结算手续费外扣账户类型 | String | 2 | N | 01：基本户（不填默认取值）；02：现金户；05：充值户；09：营销户；<font color="green">示例值：01</font> |
| settle_pattern | 结算方式 | String | 2 | N | settle_cycle为TS时不填。 P0：批次结算 ，~~P1：定时结算~~(建议选P0和P2)，P2:批次定时结算，E1:中信E管家 ，<font color="green">示例值：P1</font></br>批次结算指按照指定结算批次号进行资金结算，自定义时间结算是指按照商户指定到账时间进行资金结算。两种结算方式需二选一，不填默认P0：批次结算； |
| settle_batch_no | 结算批次号 | String | 16 | C | settle_cycle为TS时不填。当settle_pattern=P0批次结算时必填，即将按指定结算批次号进行资金结算；<font color="green">示例值：100</font>；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| is_priority_receipt | 是否优先到账 | String | 1 | N | settle_cycle为TS时不填。当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效<br/> Y：是，N：否，<font color="green">示例值：Y</font> |
| settle_time | 自定义结算处理时间 | String | 6 | C | settle_cycle为TS时不填。当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定<br/>到账时间，格式：HHmmss；<font color="green">示例值：103000</font> |
| fixed_ratio | 节假日结算手续费率 | String | 6 | C | settle_cycle为D1、TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<br>settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；<font color="green">示例值：0.05</font> |
| constant_amt | 节假日结算手续费固定金额 | String | 15 | C | settle_cycle为D1、TS时必填。单位元，需保留小数点后两位。不收费请填写0.00；<br>settle_cycle结算周期为D1时，遇节假日按此费率结算 ；<br/> <font color="green">示例值：1.00</font> |
| workday_fixed_ratio | 工作日结算手续费率 | String | 6 | N | settle_cycle为TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；<font color="green">示例值：0.05</font> |
| workday_constant_amt | 工作日结算手续费固定金额 | String | 15 | N | settle_cycle为TS时必填。单位元，需保留小数点后两位。不填默认为0.00；<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table efd9c909_f73f_4462_b999_86f4e61a2087-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cash_type | 取现类型 | String | 2 | N | D0：当日到账；可取现资金包括当天的交易资金；<br/>T1：下个工作日到账；默认值<br/>D1：下个自然日到账;<br/>DM：当日到账；可取现资金不包括当天的交易资金；<br/><font color="green">示例值：T1</font> |
| fix_amt | 取现手续费（固定/元） | String | 6 | C | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；<font color="green">示例值：1.00</font><br>注：当cash_type=D1时为节假日取现手续费；当cash_type=T1时为工作日取现手续费 |
| fee_rate | 取现手续费率（%） | String | 6 | C | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate<br>2、当cash_type=D1时为节假日取现手续费；当cash_type=T1时为工作日取现手续费 |
| weekday_fix_amt | D1工作日取现手续费固定金额 | String | 6 | C | 单位元，需保留小数点后两位。不收费请填写0.00；<font color="green">示例值：1.00</font><br>cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| weekday_fee_rate | D1工作日取现手续费率 | String | 6 | C | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| out_fee_flag | 是否取现手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认）；<font color="green">示例值：2</font> |
| out_fee_huifu_id | 手续费承担方 | String | 18 | C | 手续费外扣时必需指定手续费承担方ID ；<font color="green">示例值：6666000123123123</font> |
| out_fee_acct_type | 手续费外扣的账户类型 | String | 2 | N | 01-基本户，02-现金户，05-充值户，09-营销户；<font color="green">示例值：01</font>不填默认01 |
| is_priority_receipt | 是否优先到账 | String | 1 | N | Y：是 ，N：否。不填，默认值为否。仅在cash_type为D1 和 T1 时生效。<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d6dd0dfd_6c4a_4d50_9bb6_9720e7ceeeec-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子账户开关 | String | 1 | Y | 电子账户开通总开关；0:关闭 1:开通；<font color="green">示例值：1</font> |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家；<font color="green">示例值：01</font> |
| cash_fee_party | 电子账户取现手续费承担方 | String | 1 | Y | 1:总部 2:其他；<font color="green">示例值：1</font> |
| scene | 场景类型 | String | 3 | Y | 必填；与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；<font color="green">示例值：001</font> |
| role_type | 角色类型 | String | 6 | Y | 必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；<font color="green">示例值：001001</font> |
| <span class="extend 6a4e6c8f_7578_4849_a9f9_ce795829de45">elec_card_list</span> | 银行卡信息 | Object |  | N | jsonArray字符串，如果开通斗拱E账户但不提供绑卡信息将无法取现，后续绑卡请调用[电子账户绑卡接口](https://paas.huifu.com/open/doc/api/#/yuer/api_acct_dzzhbk) |
| elec_acct_sign_seq_id | 中信签约短信流水号 | String | 64 | N | <font color="green">示例值：EMSSBPG2504284593690058431260676</font> |
| sign_success_flag | 签约成功标志 | String | 1 | Y | Y：成功 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6a4e6c8f_7578_4849_a9f9_ce795829de45-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) <font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) <font color="green">示例值：310100</font> |
| bank_code | 银行编码 | String | 8 | Y | [参考银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font> |
| branch_code | 支行联行号 | String | 12 | Y | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | Y | <font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| card_name | 银行账户名 | String | 128 | Y | 银行卡对应的户名；<font color="green">示例值：上海汇付支付有限公司</font> |
| card_no | 银行卡号 | String | 32 | Y | <font color="green">示例值：98140008801800008888</font> |
| card_type | 银行账户类型 | String | 1 | Y | 0:对公， 1:对私法人，仅限个体工商户；<font color="green">示例值：0</font> |
| default_cash_flag | 默认卡标识 | String | 1 | N | 0：非默认卡 1：默认卡(不填，默认为0)；<font color="green">示例值：0</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 548b3b06_b06f_4332_8faa_ca24b1d24389-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 股东姓名 | String | 32 | Y | <font color="green">示例值：张三</font> |
| cert_type | 股东证件类型 | String | 2 | Y | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》；支持00~11，以及12:营业执照；<font color="green">示例值：12</font> |
| cert_no | 股东证件号码 | String | 32 | Y | <font color="green">示例值：320926198512025014</font> |
| cert_validity_type | 股东证件有效期类型 | String | 1 | Y | 1:长期有效 0:非长期有效；<font color="green">示例值：1</font> |
| cert_begin_date | 股东证件有效期起始日 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20201223</font> |
| cert_end_date | 股东证件有效期到期日 | String | 8 | N | 格式yyyyMMdd; 非长期有效时必填；<font color="green">示例值：20301223</font> |
| mobile_no | 股东手机号 | String | 11 | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a74b90ea_e018_4ee7_b48d_29d3ef662b00-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_id | 文件id | String | 64 | Y | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_type | 文件类型 | String | 64 | Y | [参见文件类型说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；<font color="green">示例值：F01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0ea6b7e9_c863_4e61_a115_f6781c247861-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 银行账户类型 | String |  | N | 对公，不填默认 0 |
| card_name | 银行账户名称 | String |  | N | 账户名必须与营业执照名称一致 |
| card_no | 对公银行账号 | String |  | Y | 对公银行账号 |
| prov_id | 银行所在省 | String |  | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) <font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String |  | Y | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) <font color="green">示例值：310100</font> |
| branch_code | 支行联行号 | String |  | Y | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
<!-- extend:end -->


#### 请求示例

```json
{  
    "data":{  
        "req_seq_id":"20220422267883697",  
        "req_date":"20220422",  
        "upper_huifu_id":"6666000003080000",  
        "reg_name":"集成企业商户8664",  
        "short_name":"企业商户3471",  
        "ent_type":"1",  
        "license_code":"20220422267883697",  
        "license_validity_type":"1",  
        "license_begin_date":"20200401",  
        "license_end_date":"",  
        "reg_prov_id":"350000",  
        "reg_area_id":"350200",  
        "reg_district_id":"350203",  
        "reg_detail":"吉林省长春市思明区解放2路59096852",  
        "legal_name":"陈立一",  
        "legal_cert_type":"00",  
        "legal_cert_no":"321084198912060000",  
        "legal_cert_validity_type":"1",  
        "legal_cert_begin_date":"20121201",  
        "legal_cert_end_date":"20301201",  
        "prov_id":"310000",  
        "area_id":"310100",  
        "district_id":"310104",  
        "detail_addr":"吉林省长春市思明区解放1路49227677",  
        "contact_name":"联系人",  
        "contact_mobile_no":"13111112222",  
        "contact_email":"jeff.peng@huifu.com",  
        "service_phone":"021-121111221",  
        "sms_send_flag":"Y",  
        "login_name":"LG20220422267883697",  
        "busi_type":"1",  
        "receipt_name":"盈盈超市",  
        "mcc":"5411",    
        "async_return_url":"virgo://http://192.168.85.157:30031/sspm/testVirgo",  
        "mer_en_name":"",  
        "mer_url":"",  
        "mer_icp":"",  
        "license_type":"",   
        "card_info":"{\"branch_code\":\"305290002096\",\"card_no\":\"698043508\",\"card_name\":\"上海以道数据服务中心\",\"card_type\":\"0\"}",  
        "cash_config":"[{\"cash_type\":\"D0\",\"fix_amt\":\"1.00\",\"fee_rate\":\"\"},{\"cash_type\":\"D1\",\"fix_amt\":\"\",\"fee_rate\":\"10.00\"}]",  
        "settle_config":"{\"settle_pattern\":\"\",\"is_priority_receipt\":\"\",\"settle_time\":\"\",\"settle_cycle\":\"D1\",\"min_amt\":\"1.00\",\"remained_amt\":\"2.00\",\"settle_abstract\":\"abstract\",\"out_settle_flag\":\"2\",\"out_settle_huifuid\":\"\",  \"out_settle_acct_type\":\"\",\"fixed_ratio\":\"5.00\",\"settle_batch_no\":\"\"}"  
    },  
    "sys_id":"ssproxy_dev",  
    "sign":"fTill2l5tg47MLUJ+wOg0wyEIcNtfVIBA9bGyLWZflkl/ZaT9pIYQiWUFJGgkbzWTfa+jI4bwnjHQg4u7lshAwQfxCzELyAkPC4rLm7jiGw0RbNTwgD6LWwzMDkbHkhMGxhaZfrVcK6XNPSHD1dqmKHj66A67+XeWFev50dEQE4=",  
    "product_id":"ZDTEST"  
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| huifu_id | 商户号 | String | 18 | N | 汇付商户号，<font color="green">示例值：6666000123123123  </font> |
| apply_no | 申请单号 | String | 18 | N | 商户开户业务申请单号，<font color="green">示例值：2022012500073423</font> |
| token_no | 银行卡序列号 | String | 20 | N | 取现时使用 ；<font color="green">示例值：10004053462</font> |


#### 异步返回参数

| 参数      | 中文名         | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                       |
| :-------- | :------------- | :----- | :------- | :--- | :------------------------- |
| resp_code | 网关返回码     | String | 5        | Y    | [网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%bd%91%e5%85%b3%e8%bf%94%e5%9b%9e%e7%a0%81)；<font color="green">示例值：10000   </font> |
| resp_desc | 网关返回描述   | String | 512      | Y    | 网关返回描述；<font color="green">示例值：成功调用</font> |
| sign      | 签名           | String | 2048     | Y    | 签名，对报文整体签名；<font color="green">示例值：o8bYN+DO5AaYl41idy04tZknaRnNORy8TgIztI6d8e3EtrSU9DbSjlN99DAgopNex6pEFFbQimxGxN8n9rADO4Xe7IZ9McPy2I9zJ0hccGpK9YBa2cqSMMzLCmxFiVqlz04RxrduBOHrfIsr4HM9Z3g6r8yOAL/FS1LqH7M3bCo= </font>      |
| data      | 业务返回参数 | String |          | N    | 业务返回参数  jsonObject格式 |

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) ；<font color="green">示例值：00000000 </font> |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | <font color="green">示例值：处理成功</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | 原请求流水号；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 原请求日期；<font color="green">示例值：20220125</font> |
| audit_status | 审核结果 | String | 1 | Y | Y：审核通过，N：审核拒绝，F：失败，<font color="green">示例值：Y</font> |
| audit_desc | 审核描述 | String | 512 | N | <font color="green">示例值：审核通过 </font> |
| product_id | 产品号 | String | 32 | Y | 汇付分配的产品号，<font color="green">示例值：MCS</font> |
| huifu_id | 商户号 | String | 18 | N | 汇付商户号，状态为审核中时返回；<font color="green">示例值：6666000123123123</font> |
| apply_no | 申请单号 | String | 18 | N | 商户开户业务申请单号，状态为审核中时返回；<font color="green">示例值：2022012500073423</font> |
| token_no | 银行卡序列号 | String | 20 | N | 取现时使用；<font color="green">示例值：10004053462</font> |
| notify_type | 通知类型 | String | 1 | N | Z：电子账户；<font color="green">示例值：Z</font> |
| <span class="extend 82b8a139_9b80_4726_92ca_d9fa35ed503a">elec_acct_result</span> | 斗拱e账户开通结果 | String |  | N | jsonObject格式；notify_type=Z时返回 |

<!-- extend:start -->
<!-- div:extend-table 82b8a139_9b80_4726_92ca_d9fa35ed503a-table -->
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
    "data":{  
        "huifu_id":"6666000104778868",  
        "resp_code":"00000000",  
        "resp_desc":"成功",  
        "token_no":"10000713406"  
    },  
    "sign":"o8bYN+DO5AaYl41idy04tZknaRnNORy8TgIztI6d8e3EtrSU9DbSjlN99DAgopNex6pEFFbQimxGxN8n9rADO4Xe7IZ9McPy2I9zJ0hccGpK9YBa2cqSMMzLCmxFiVqlz04RxrduBOHrfIsr4HM9Z3g6r8yOAL/FS1LqH7M3bCo="  
}

```
