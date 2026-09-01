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
## 个人商户进件

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/basicdata/indv

*最近更新时间：2026.08.18*
> 2023.6.30斗拱升级了商户进件类接口，老版接口、升级指引请参考[说明文档](old_api/api_2023shglsj)

### 应用场景
<!--服务商通过此接口在汇付为个人类商户进行基本信息开户。传入个人商户基本资料和图片资料，开通汇付账号，为商户绑定银行卡、配置结算和取现等功能。若选择发送短信给商户，将会发送账号、密码、控台地址短信至商户联系人手机号。-->
通过此接口在汇付为个人类商户（无执照的商户）进行基本信息开户。传入个人商户基本资料和图片资料，开通汇付账号，为商户绑定银行卡、配置结算和取现等功能。


**适用对象**  
  个人类商户开通汇付账号并填写基本信息、配置结算和取现等功能，可调用该功能。

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

- “必填”字段取值“Y“：必填；“N”：非必填；“C”代表条件必填； 

### **注意**
- card_info卡信息**对私结算会验证【银行卡户名】【银行卡号】【持卡人证件号码】，请正确上送参数值；**    
- card_info卡信息系统会自动识别银行卡号所属银行，如果未能识别请填写银行编号【bank_code】。建议统一填写银行编号提高成功率；
- “必填”字段取值“C”代表条件必填；  
- 请上送utf-8格式的字体，否则影响后期AT入驻；

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号，同一商户号当天唯一；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准；<font color="green">示例值：20220125</font> |
| upper_huifu_id | 直属渠道号 | String | 18 | C | 该商户进件完成后归属的渠道商huifu_id；<br/>sys_id主体为渠道商时填写； <br/>sys_id主体为总部商户时选填；<br/> <font color="green">示例值：6666000123123123</font> |
| reg_name | 商户名 | String | 32 | Y | 商户名称，个人类商户为负责人姓名；<font color="green">示例值：张三</font> |
| short_name | 商户简称 | String | 32 | N | 最少4个字符；会展示在消费账单上；<font color="green">示例值：张三</font> |
| mcc | 所属行业 | String | 7 | Y | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；<font color="green">示例值：5311</font> |
| scene_type | 场景类型 | String | 8 | Y | ONLINE：线上场景，OFFLINE：线下场景，ALL：线上线下；<font color="green">示例值：ALL</font> |
| prov_id | 经营省 | String | 6 | N | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，<font color="green">示例值：310000</font> |
| area_id | 经营市 | String | 6 | N | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，<font color="green">示例值：310100 </font> |
| district_id | 经营区 | String | 6 | Y | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，<font color="green">示例值：310101 </font> |
| detail_addr | 经营详细地址 | String | 256 | C | scene_type字段含有线下场景时必填；<font color="green">示例值：上海市徐汇区XX路XX号</font> |
| legal_cert_no | 负责人证件号码 | String | 32 | Y | 只支持身份证号；<font color="green">示例值：32092198512025017</font>；年龄不允许小于18岁且不能大于80岁 |
| legal_cert_begin_date | 负责人证件有效期开始日期 | String | 8 | Y | 日期格式yyyyMMdd，<font color="green">示例值：20110112</font>。开始日期需小于当前日期； |
| legal_cert_validity_type | 负责人证件有效期类型 | String | 1 | N | 1：长期有效；0：非长期有效；<font color="green">示例值：1</font> |
| legal_cert_end_date | 负责人证件有效期截止日期 | String | 8 | Y | 日期格式yyyyMMdd；<font color="green">示例值：20410112</font>。结束日期大于当前日期； |
| legal_addr | 负责人身份证地址 | String | 256 | Y | <font color="green">示例值：上海市徐汇区XX路XX号</font> |
| legal_cert_back_pic | 负责人身份证国徽面 | String | 64 | Y | 涉及文件类型：F41；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| legal_cert_front_pic | 负责人身份证人像面 | String | 64 | Y | 涉及文件类型：F40；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| occupation | 负责人职业 | String | 2 | N | 1A：各类专业,技术人员<br/>1B：国家机关,党群组织,企事业单位的负责人<br/>1C：办事人员和有关人员<br/>1D：商业工作人员，默认<br/>1E：服务性工作人员<br/>1F：农林牧渔劳动者<br/>1G：生产工作,运输工作和部分体力劳动者<br/>1H：不便分类的其他劳动者<br/><font color="green">示例值：1G</font> |
| contact_mobile_no | 负责人手机号 | String | 11 | Y | 负责人手机号，需为11位数字；<font color="green">示例值：18611111111 </font> |
| contact_email | 负责人电子邮箱 | String | 32 | Y | 负责人电子邮箱，需要带@，遵循邮箱格式；<font color="green">示例值：huifu@xxx.com</font> |
| <span class="extend 5c0faa5c_c471_4126_8023_cd37326361fb">card_info</span> | 结算卡信息配置 | String |  | Y | 商户结算账户信息配置，jsonObject字符串；开通中信E管家结算的银行卡配置在【elec_acct_config】中 |
| settle_card_front_pic | 银行卡卡号面 | String | 64 | Y | 涉及文件类型：F13；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| <span class="extend 933264eb_9412_43bf_83f4_93336c5ac17f">settle_config</span> | 结算规则配置 | String |  | N | 商户结算规则配置，jsonObject格式 |
| <span class="extend 7fab2100_c2d6_4389_ab2e_b0b9f2f9c58e">cash_config</span> | 取现信息配置 | String |  | N | 商户取现信息配置，jsonArray字符串 |
| sms_send_flag | 商户通知标识 | String | 1 | N | 入驻成功后通知商户联系人，M：发送短信通知；E：发送邮件通知；A：短信、邮件都通知；为空：不作通知。 <font color="green">示例值：M</font> |
| login_name | 管理员账号 | String | 32 | N | 管理员账号，用于商户平台登录。全局唯一，支持英文、数字、下划线，区分大小写；<font color="green">示例值：huifu001</font> |
| mer_url | 商户主页URL | String | 256 | N | <font color="green">示例值：https://paas.huifu.com/ </font> |
| mer_icp | 商户ICP备案编号 | String | 50 | C | 商户ICP备案编号或网站许可证号；<font color="green">示例值：沪ICP备06046402号-28 </font><br/>类型为PC网站时，且为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填 |
| store_header_pic | 店铺门头照 | String | 64 | C | scene_type字段含有线下场景时必填；文件类型：F22；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font><br/>微信/支付宝实名认证个人商户，门头照也使用此字段； <br/>门店场所：提交门店门口照片，要求招牌清晰可见; <br/>小微商户流动经营/便民服务：提交经营/服务现场照片 |
| store_indoor_pic | 店铺内景/工作区域照 | String | 64 | C | scene_type字段含有线下场景时必填；文件类型：F24；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font><br/>微信/支付宝实名认证个人商户，内景照也使用此字段； <br/>门店场所：提交店内环境照片 <br/>小微商户流动经营/便民服务：可提交另一张经营/服务现场照片 |
| store_cashier_desk_pic | 店铺收银台/公司前台照 | String | 64 | C | scene_type字段含有线下场景时必填；文件类型：F105；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| ext_mer_id | 外部商户号 | String | 64 | N | 支持关联外部商户系统中的商户号；<font color="green">示例值：HF100001</font> |
| remarks | 备注 | String | 300 | N | 备注内容；<font color="green">示例值：华东分公司</font> |
| async_return_url | 异步通知地址 | String | 120 | N | 审核结果消息接收地址，为空时不推送消息 <br/><font color="green">示例值：http://service.example.com/to/path</font> |
| head_office_flag | 商户身份 | String | 1 | N | 0：下级商户，不传默认普通商户。<font color="green">示例值：0</font><br>开通下级商户时，所选的上级商户需要有开通商户权限，需先调用“[开通下级商户权限配置接口](https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt_xjshpz)”<br/>（1）若对应总部的客群类型为0，需要补充F725 （集团盖章说明函）；<br/>（2）若对应总部的客群类型为1，需要补充F726 （下级商户入驻大型商业综合体的合作协议）；<br/>（3）若对应总部的客群类型为2，加盟性质需要补充F727（加盟协议），直营性质需要补充F727（总部盖章说明函） |
| head_huifu_id | 上级商户汇付ID | String | 18 | C | 如果head_office_flag=0，则字段必填<br><font color="green">示例值：6666000123123123</font> |
| <span class="extend b2a96435_82bd_4e2d_9a49_faca1fa986a2">elec_acct_config</span> | 斗拱e账户功能配置 | String |  | N | 用于下级商户开通斗拱E账户功能 |
| <span class="extend 52efc0a5_29f4_444f_9728_f4f6ca873b95">extended_material_list</span> | 扩展资料包 | String |  | N | jsonArray字符串；根据要求上传补充相关材料 |
| activated_products | 产品大类 | String |  | N |  01：一体化收款产品，02：账户与资金产品，03：业财数通产品；不传为空 <font color="green">示例值：01,02,03</font> |

<!-- extend:start -->
<!-- div:extend-table 5c0faa5c_c471_4126_8023_cd37326361fb-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_name | 卡户名 | String | 128 | Y | 结算账户名，结算银行卡对应的户名；<font color="green">示例值：张三</font> |
| card_no | 结算账号 | String | 32 | Y | 结算银行卡号，不支持贷记卡。为避免资金结算失败，请正确填写； <font color="green">示例值：98140008801800008888</font> |
| prov_id | 银行所在省 | String | 6 | N | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | Y | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font> |
| bank_code | 银行编号 | String | 8 | N | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) ；<font color="green">示例值：01020000 </font> |
| cert_type | 持卡人证件类型 | String | 2 | Y | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》 <font color="green">示例值：00</font> |
| cert_no | 持卡人证件号码 | String | 32 | Y | 如持卡人证件类型为00：身份证，则填写身份证号码；<font color="green">示例值：310112200001018888</font>。**系统会做格式校验**；年龄不允许小于18岁且不能大于80岁 |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | Y | 1:长期有效，0:非长期有效；<font color="green">示例值：0   </font> |
| cert_begin_date | 持卡人证件有效期开始 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准；<font color="green">示例值：20220125</font> |
| cert_end_date | 持卡人证件有效期截止日期 | String | 8 | C | 格式yyyyMMdd，以北京时间为准。<font color="green">示例值：20220125</font><br/>当cert_validity_type=0时必填  <br/>当cert_validity_type=1时为空 |
| mp | 结算人手机号 | String | 11 | N | 11位数字；<!--开通全域资金管理功能必填；--><font  color="green">示例值：18611111111</font> |
| is_settle_default | 默认结算卡标志 | String | 1 | N | 是否为默认结算卡标志；Y:是 N:否(为空默认)；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 933264eb_9412_43bf_83f4_93336c5ac17f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_cycle | 结算周期 | String | 2 | Y | 结算周期；<font color="green">示例值：T1</font><br/> D1：下个自然日到账  <br/> T1：下个工作日到账<br/> TS:笔笔结算； |
| min_amt | 起结金额 | String | 14 | N | settle_cycle为TS时不填。账户余额大于等于起结金额才会发起结算。单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。不设置起结金额请填写0.00；<font color="green">示例值：1000.00 </font> |
| remained_amt | 留存金额 | String | 14 | N | settle_cycle为TS时不填。该部分资金不会结算。单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。不设置留存金额请填写0.00；<font color="green">示例值：1000.00</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 可自定义结算打款备注，不填默认为空；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；<font color="green">示例值：汇付商城业务</font> |
| out_settle_flag | 手续费外扣标记 | String | 1 | N | 手续费外扣标记，外扣时从out_settle_huifuid账户扣手续费，内扣时从结算金额中扣手续费；<br/>1：外扣；2：内扣；不填默认内扣；<font color="green">示例值：2</font> |
| out_settle_huifuid | 结算手续费外扣商户号 | String | 18 | C | 结算手续费外扣商户号，填写承担手续费的汇付商户号<br/>当out_settle_flag=1时必填，否则非必填；<font color="green">示例值：6666000123123123</font> |
| out_settle_acct_type | 结算手续费外扣账户类型 | String | 2 | N | 结算手续费外扣账户类型，不填默认01：基本户<br/>01：基本户，02：现金户，05：充值户 ，09：营销户；<font color="green">示例值：01 </font> |
| settle_pattern | 结算方式 | String |  | N | settle_cycle为TS时不填。P0：批次结算 ，P1：定时结算(建议选P0和P2)，P2:批次定时结算，E1:中信E管家 示例值：P1 批次结算指按照指定结算批次号进行资金结算，自定义时间结算是指按照商户指定到账时间进行资金结算。两种结算方式需二选一，不填默认P0：批次结算； |
| settle_batch_no | 结算批次号 | String | 16 | C | settle_cycle为TS时不填。结算方式为P0：批次结算时必填，即将按指定结算批次号进行资金结算；<font color="green">示例值：100</font>；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| is_priority_receipt | 是否优先到账 | String | 1 | N | 当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效<br/> Y：是，N：否，<font color="green">示例值：Y</font> |
| settle_time | 自定义结算处理时间 | String | 6 | C | settle_cycle为TS时不填。当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定；<br/>到账时间，格式：HHmmss；<font color="green">示例值：103000</font> |
| fixed_ratio | 节假日结算手续费率 | String | 6 | C | settle_cycle为D1、TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<br>settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；<font color="green">示例值：0.05</font> |
| constant_amt | 节假日结算手续费固定金额 | String | 15 | C | settle_cycle为D1、TS时必填。单位元，需保留小数点后两位。不收费请填写0.00；<br>settle_cycle结算周期为D1时，遇节假日按此费率结算 ；<br/> <font color="green">示例值：1.00</font> |
| workday_fixed_ratio | 工作日结算手续费率 | String | 6 | N | settle_cycle为TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；<font color="green">示例值：0.05</font> |
| workday_constant_amt | 工作日结算手续费固定金额 | String | 15 | N | settle_cycle为TS时必填。单位元，需保留小数点后两位。不填默认为0.00；<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7fab2100_c2d6_4389_ab2e_b0b9f2f9c58e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cash_type | 取现类型 | String | 2 | Y | T1：下个工作日到账<br />D1：下个自然日到账 <br/>D0：当日到账，当日交易资金当天可取现到账；<!--开户满30天，近30天内活跃10天以上，近30天内成功交易满1万才能开通D0。--><br/>DM：当日到账，到账资金不包括当天的交易资金；<br/> <font color="green">示例值：T1</font> |
| fix_amt | 提现手续费（固定/元） | String | 6 | C | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；<font color="green">示例值：1.00</font><br>注：当cash_type=D1时为节假日取现手续费 |
| fee_rate | 提现手续费率（%） | String | 6 | C | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate<br>2、当cash_type=D1时为节假日取现手续费 |
| weekday_fix_amt | D1工作日取现手续费固定金额 | String | 6 | C | 单位元，需保留小数点后两位。不收费请填写0.00；<font color="green">示例值：1.00</font><br>cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| weekday_fee_rate | D1工作日取现手续费率 | String | 6 | C | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<font color="green">示例值：0.05</font><br>cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）； <font color="green">示例值：2</font> |
| out_fee_huifu_id | 手续费承担方 | String | 18 | C | 手续费外扣时必需指定手续费承担方ID； <font color="green">示例值：6666000123123123</font> |
| out_fee_acct_type | 交易手续费外扣的账户类型 | String | 2 | N | 01-基本户，02-现金户，05-充值户；不填默认01； <font color="green">示例值：01</font> |
| is_priority_receipt | 是否优先到账 | String | 1 | N | Y：是 ，N：否。不填，默认值为否。仅在取现类型配置为D1 和 T1 时生效。<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b2a96435_82bd_4e2d_9a49_faca1fa986a2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 电子账户开关 | String | 1 | Y | 电子账户开通总开关；0:关闭 1:开通；<font color="green">示例值：1</font> |
| acct_type | 账户类型 | String | 2 | Y | 01：中信e管家；<font color="green">示例值：01</font> |
| cash_fee_party | 电子账户提现手续费承担方 | String | 1 | Y | 1:总部 2:其他；<font color="green">示例值：1</font> |
| scene | 场景类型 | String | 3 | Y | 必填，与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；<font color="green">示例值：001</font> |
| role_type | 角色类型 | String | 6 | Y | 角色编号必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；<font color="green">示例值：001001</font> |
| <span class="extend 1bacaa27_9462_4c73_85c8_761fd65eb9b7">elec_card_list</span> | 银行卡信息 | Object |  | N | jsonArray字符串；如果开通斗拱E账户但不提供绑卡信息将无法取现，后续绑卡请调用[电子账户绑卡接口](https://paas.huifu.com/open/doc/api/#/yuer/api_acct_dzzhbk) |
| elec_acct_sign_seq_id | 中信签约短信流水号 | String | 64 | N | <font color="green">示例值：EMSSBPG2504284593690058431260676</font> |
| sign_success_flag | 签约成功标志 | String | 1 | Y | Y：成功 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1bacaa27_9462_4c73_85c8_761fd65eb9b7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) <font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | N | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) <font color="green">示例值：310100</font> |
| bank_code | 银行编码 | String | 8 | Y | [参考银行编码；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)<font color="green">示例值：01020000</font> |
| branch_code | 支行联行号 | String | 12 | Y | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | Y | <font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| card_name | 结算账户名 | String | 128 | Y | 银行卡对应的户名；<font color="green">示例值：上海汇付支付有限公司</font> |
| card_no | 银行卡号 | String | 32 | Y | <font color="green">示例值：98140008801800008888</font> |
| card_type | 卡类型 | String | 1 | Y | 0:对公 1:对私法人；<font color="green">示例值：1</font> |
| default_cash_flag | 默认卡标识 | String | 1 | N | 0：非默认卡 1：默认卡(不填，默认为0)；<font color="green">示例值：1</font> |
| mp | 银行绑定手机号 | String | 11 | C | 为空取联系人手机号，注意如果联系人非持卡人银行会报错；<!--2024.5.19--><font color="green">示例值:13911111111</font> |
| auth_version | 用户授权协议版本号 | String | 64 | C | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| auth_no | 用户授权协议号 | String | 64 | C | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 52efc0a5_29f4_444f_9728_f4f6ca873b95-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_id | 文件id | String | 64 | Y | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_type | 文件类型 | String | 64 | Y | [参见文件类型说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；<font color="green">示例值：F01</font> |
<!-- extend:end -->


#### 请求示例

```json
{  
    "sys_id":"6666000107803321",  
    "data":{  
        "req_seq_id":"rQ2021121310551325125891638801",  
        "req_date":"20220117",  
        "upper_huifu_id":"6666000107803321",  
        "reg_name":"张天德",  
        "short_name":"张天德",  
        "prov_id":"310000",  
        "area_id":"310100",  
        "district_id":"310105",  
        "detail_addr":"上海市长宁区定西路1310号",  
        "contact_name":"张天德",  
        "contact_mobile_no":"13111112222",  
        "contact_email":"jeff.peng@huifu.com",  
        "sms_send_flag":"1",  
        "login_name":"tinysword0116",  
        "settle_agree_pic":"119bc780-b1c5-3a9c-8b18-f911de6ff28c",  
        "async_return_url":"http://192.168.85.157:30031/sspm/testVirgo",  
        "card_info":"{\"card_name\":\"张天德\",\"card_no\":\"4367421217494235081\",\"prov_id\":\"310000\",\"area_id\":\"310100\",\"bank_code\":\"01030000\",\"cert_type\":\"00\",\"cert_no\":\"321084198912066512\",\"cert_validity_type\":\"0\",\"cert_begin_date\":\"20180824\",\"cert_end_date\":\"20380824\",\"mp\":\"13700000214\"}",  
        "cash_config":"[{\"cash_type\":\"D1\",\"fix_amt\":\"1.00\",\"fee_rate\":\"\"}]",  
        "settle_config":"{\"settle_cycle\":\"D1\",\"min_amt\":\"1.00\",\"remained_amt\":\"2.00\",\"settle_abstract\":\"我这里显示结算摘要\",\"out_settle_flag\":\"2\",\"out_settle_huifuid\":\"\",\"fixed_ratio\":\"5.00\"}"
    },  
    "sign":"CwPVQzbFA3I1fOExMslMO48bi2nyVZtGhBGhasDRmvy8AHDtSL/Fl92z3fvma/J5Yiq2uuLK4+QEGDfmnEVHfZJs74mlW17pzjQE5VxJrV4Sr98pS0KsAzCH5C85jqsKokNGm3J2m3NI3Kakqc6lww8nNfGBPmXohrN6CgHxCks=",  
    "product_id":"HUIFENQI"  
}

```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) ；<font color="green">示例值：00000000  </font> |
| resp_desc | 业务返回描述 | String | 512 | Y | 业务返回描述 ；<font color="green">示例值：处理成功</font> |
| huifu_id | 商户号 | String | 18 | N | 汇付商户号，状态为审核中时返回；<font color="green">示例值：6666000123123123</font> |
| apply_no | 申请单号 | String | 18 | N | 商户开户业务申请单号，状态为审核中时返回；<font color="green">示例值：2022012500073423</font> |
| token_no | 取现卡序列号 | String | 20 | N | 取现时使用 ；<font color="green">示例值：10004053462</font> |


#### 异步返回参数

**公共返参**

| 参数      | 中文名         | 类型   |长度 | 必填 | 说明                 |
| :-------- | :------------- | :----- | :--- | :------- | :------------------- |
| resp_code | 网关返回码     | String |  5   | Y        | [网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#网关返回码) ；<font color="green">示例值：10000 </font> |
| resp_desc | 网关返回描述   | String | 512    | Y      | 网关返回描述 ；<font color="green">示例值：成功调用</font>|
| sign      | 签名           | String | 512  | N      |签名，对报文整体签名； <font color="green">示例值：o8bYN+……/FS1LqH7M3bCo=</font>|
| data      | 交易响应内容体 | String |     |   N       | 业务返回参数， jsonObject格式 |

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码)；<font color="green">示例值：00000000  </font> |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | 原请求流水号；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 原请求日期；格式：yyyyMMdd  <font color="green">示例值：20220125</font> |
| audit_status | 审核结果 | String | 1 | Y | 审核结果；Y：审核通过；N：审核拒绝；F：失败；<font color="green">示例值：Y</font> |
| audit_desc | 审核描述 | String | 512 | N | 审核描述，审核人员编辑的审核描述；<font color="green">示例值：审核通过</font> |
| product_id | 产品号 | String | 32 | Y | 汇付分配的产品号，<font color="green">示例值：MCS </font> |
| huifu_id | 商户号 | String | 18 | N | 汇付商户号，状态为审核中时返回 ；<font color="green">示例值：6666000123123123 </font> |
| apply_no | 申请单号 | String | 18 | N | 商户开户业务申请单号，状态为审核中时返回；<font color="green">示例值：2022012500073423 </font> |
| token_no | 取现卡序列号 | String | 20 | N | 取现时使用；<font color="green">示例值：10004053462</font> |
| notify_type | 通知类型 | String | 1 | N | Z：电子账户；<font color="green">示例值：Z</font> |
| <span class="extend fcb2957e_fae2_42e1_99a5_d72c1ecb66e4">elec_acct_result</span> | 斗拱e账户开通结果 | String |  | N | jsonObject格式；notify_type=Z时返回 |

<!-- extend:start -->
<!-- div:extend-table fcb2957e_fae2_42e1_99a5_d72c1ecb66e4-table -->
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
        "resp_desc":"审核中",  
        "apply_no":"2022011700383517",  
        "resp_code":"90000000",  
        "huifu_id":"6666000112180069"  
    }  
}

```
