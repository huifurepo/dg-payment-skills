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
## 申请单状态查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/basicdata/status/query

*最近更新时间：2026.09.20*
### 应用场景
申请单提交后，调用此接口查询商户申请单审核状态及各业务开通结果。支持查询商户各种已提交的申请单，包括商户业务开通申请单、活动报名申请单、信息修改申请单等，若申请单审核拒绝，将返回拒绝的详细原因，可根据拒绝原因修改信息。

**适用对象**   
  商户查询汇付审核结果、业务开通、活动报名、信息修改以及对应的审核未通过原因，可调用该功能。

### 接口说明 
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font> |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数    

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 业务申请编号，同一商户号当天唯一；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd，以北京时间为准。<font color="green">示例值：20220125</font> |
| apply_no | 申请单 | String | 18 | Y | 汇付返回商户的申请单号；参见商户基本信息入驻、业务开通等接口返回的apply_no；<font color="green">示例值：2022011100377000</font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font> |


#### 请求示例

```json
{
    "sys_id": "6666000107803321",
    "data": {
        "req_seq_id": "rQ2021121311022061128035096289",
        "req_date": "20211213",
        "huifu_id": "6666000003117253",
        "apply_no": "2022011100377000"
    },
    "sign": "KLwRbZlYsPEg6kbAiG3y3Vk0rVv4LdW12xgLxOXxcEd6QtY7fnK/0bDvpPjCE4XPR1Rns80k048CBvo33VYLjLizrcobZECaNQkrq45bKrjQViyk4zc0pVjGrhKILQlg/eRDVMoKyh1MHJY59vAGjqXAtowkrfUhZpr0oNH63kY=",
    "product_id": "EDUSTD"
}
```
### 返回参数


#### 返回参数

注：申请单状态查询接口返回时，根据业务开通申请请求的业务信息返回。例：业务开通时未申请开通微信业务，则对应微信配置结果集合（wx_conf_result_list）不返回对应参数list的信息。

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| huifu_id | 商户号 | String | 18 | N | 汇付分配的商户号，<font color="green">示例值：666600000123123123</font> |
| reg_name | 商户注册名称 | String | 128 | N | 商户注册名称；<font color="green">示例值：上海汇付支付服务有限公司</font> |
| apply_reason | 审核意见 | String | 512 | N | 审核意见 |
| apply_status | 申请单审核状态 | String | 1 | N | Y：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；示例值：Y |
| bank_card_conf_reason | 银行卡业务开通描述 | String | 512 | N | 如银行卡业务开通失败，返回失败原因 |
| bank_card_conf_status | 银行卡支付业务开通状态 | String | 1 | N | P:处理中 S:成功 F:失败；<font color="green">示例值：S</font> |
| bank_sub_mer_id | 银行卡银联商户号 | String | 20 | N | 银行卡银联商户号，<font color="green">示例值：66345234544</font> |
| bind_card_status | 绑卡状态 | String | 1 | N | P:处理中 S:成功 F:失败；<font color="green">示例值：P </font> |
| cash_status | 取现配置状态 | String | 1 | N | P:处理中 S:成功 F:失败；<font color="green">示例值：P</font> |
| reg_status | 商户入驻汇付状态 | String | 1 | N | P:处理中 S:成功 F:失败；<font color="green">示例值：P</font> |
| settle_status | 结算配置状态 | String | 1 | N | P:处理中 S:成功 F:失败 ；<font color="green">示例值：P </font> |
| union_sub_mer_id | 银联二维码银联商户号 | String | 20 | N | 银联二维码银联商户号，<font color="green">示例值：66345234544</font> |
| union_conf_reason | 银联二维码业务开通描述 | String | 512 | N | 如银联二维码业务开通失败，返回失败原因 |
| union_conf_status | 银联二维码业务开通状态 | String | 1 | N | P:处理中 S:成功 F:失败；<font color="green">示例值：P</font> |
| <span class="extend 545425ed_e839_4741_8452_6e79da76014a">ali_conf_result_list</span> | 支付宝配置结果集合 | String |  | N | jsonArray格式；调用商户业务开通、商户业务开通修改接口，申请单支付宝业务配置会返回 |
| <span class="extend 5df50fa4_0474_4a50_b79d_8f3c1436083d">wx_conf_result_list</span> | 微信配置结果集合 | String |  | N | jsonArray格式；调用商户业务开通、商户业务开通修改接口，申请单微信业务配置会返回 |
| <span class="extend aded3404_f012_4b63_9a03_050f2ef4fe49">zft_apply_result_list</span> | 支付宝直付通申请结果集合 | String |  | N | jsonArray格式 |
| <span class="extend 77fc8c34_70cf_4424_8937_579f6ea39347">combine_pay_config</span> | 补贴支付 | String |  | N | jsonObject格式 |
| <span class="extend 16f04756_ad9f_47d1_80f4_92830d231f6c">wx_config_list</span> | 微信配置状态结果集 | String |  | N | jsonArray格式 |
| account_name | 银行账户名 | String | 128 | N | 全域资金管理开通的银行账户名；<font color="green">示例值：上海汇付支付服务有限公司</font> |
| electron_account | 银行收款电子账号 | String | 32 | N | 全域资金管理开的银行电子账号；<font color="green">示例值：</font> |
| out_order_funds_status | 银行收款入账状态 | String | 1 | N | 全域资金管理功能涉及字段； P：处理中S：成功F：失败；<font color="green">示例值：P</font> |
| out_order_funds_desc | 银行收款入账描述 | String | 256 | N | 全域资金管理功能涉及字段；只返回错误描述；<font color="green">示例值：</font> |
| <span class="extend b2c5680e_c362_410e_b56a_901d77978be6">wx_zl_config</span> | 微信直连配置对象 | String |  | N | jsonObject格式 |
| <span class="extend 555d0dd6_7d02_4fcd_873d_a9890a9013a2">ali_zl_config</span> | 支付宝直连配置列表 | String |  | N | jsonArray格式 |
| change_settle_state | 意愿核实状态 | String | 1 | N | F：拒绝/失败  S：成功/通过  P：等待处理  C：已撤销（控台操作）<br/>当【变更结算人核验方式 = 1】时返回意愿核实状态。<br/><font color="green">示例值：S</font> |
| <span class="extend 5775c0ff_d070_491a_a9b5_b02078e48f2b">agreement_info_list</span> | 协议信息 | String |  | N | 签署电子协议时返回 jsonArray格式 |

<!-- extend:start -->
<!-- div:extend-table 545425ed_e839_4741_8452_6e79da76014a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1线下扫码；<font color="green">示例值：1</font> |
| pay_channel_id | 子渠道号 | String | 50 | N | 不填入驻到渠道默认配置的支付宝渠道号下；<font color="green">示例值：JP00001</font> |
| sub_mer_id | 二级商户号 | String | 32 | N | 在汇付做支付宝入驻时，汇付端生成的唯一二级商户号；<font color="green">示例值：A4854135335181517376</font> |
| sub_mer_name | 二级商户名 | String | 60 | N | 二级商户名 ；<font color="green">示例值：上海汇付支付服务有限公司</font> |
| ali_bank_mer_code | 支付宝商户号 | String | 20 | N | 支付宝银行商户号；<font color="green">示例值：2234544</font> |
| ali_conf_reason | 支付宝业务开通描述 | String | 512 | N | 支付宝业务开通描述 |
| ali_conf_status | 支付宝业务开通状态 | String | 1 | N | P:处理中 S:成功 F:失败；<font color="green">示例值：S</font> |
| fq_flag | 分期标志 | String | 1 | N | 1：分期业务；<font color="green">示例值：1</font> |
| real_name_applyment_stat | 实名认证状态 | String | 64 | N | 申请实名时返回<br>审核中(AUDITING)<br>待联系人确认(CONTACT_CONFIRM)<br>待法人确认(LEGAL_CONFIRM)<br>审核通过(AUDIT_PASS)<br>审核失败(AUDIT_REJECT)<br>已冻结(AUDIT_FREEZE)<br>已撤回(CANCELED)<br>未申请(NOT_APPLY)<br/><font color="green">示例值：</font> |
| real_name_applyment_desc | 实名认证描述 | String | 128 | N | 申请实名时返回；<font color="green">示例值：</font> |
| qrcode_data | 授权二维码 | String | 128 | N | 若实名认证状态 real_name_applyment_stat=<br>CONTACT_CONFIRM、LEGAL_CONFIRM时返回；<font color="green">示例值：https://qr.alipay.com/bax02911brluc2xieoph6001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5df50fa4_0474_4a50_b79d_8f3c1436083d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 参见《[微信支付场景](api_ggcsbm.md#微信支付场景)》说明 ；<font color="green">示例值：1</font> |
| pay_channel_id | 子渠道号 | String | 50 | N | 不填入驻到渠道默认配置的微信渠道号下；<font color="green">示例值：JP00001</font> |
| sub_mer_id | 二级商户号 | String | 32 | N | 在汇付做微信入驻时，汇付端生成的唯一二级商户号；<font color="green">示值值：W5503418657189757903</font> |
| sub_mer_name | 二级商户名 | String | 60 | N | 二级商户名 ；<font color="green">示例值：上海汇付支付服务有限公司</font> |
| wx_bank_mer_code | 微信银行商户号 | String | 20 | N | 微信银行商户号；<font color="green">示例值：66345234544</font> |
| wx_conf_reason | 微信业务开通描述 | String | 512 | N | 微信业务开通描述 |
| wx_conf_status | 微信业务开通状态 | String | 1 | N | P:处理中 S:成功 F:失败；<font color="green">示例值：S</font> |
| real_name_applyment_stat | 实名认证状态 | String | 64 | N |  申请实名时返回<br>APPLYMENT_STATE_EDITTING--【编辑中】--可能在提交申请时发生错误导致，可用同一个业务申请编号重新提交<br>APPLYMENT_STATE_WAITTING_FOR_AUDIT--【审核中】--请耐心等待1~2个工作日，微信支付将会完成审核<br>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT--【待确认联系信息】--请扫描微信支付返回的小程序码确认联系信息(此过程可修改超级管理员手机号)<br>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON--【待账户验证】--请扫描微信支付返回的小程序码在小程序端完成账户验证<br>APPLYMENT_STATE_PASSED--【审核通过】--请扫描微信支付返回的小程序码在小程序端完成授权流程<br>APPLYMENT_STATE_REJECTED--【审核驳回】--请按照驳回原因修改申请资料，并更换业务申请编码，重新提交申请<br>APPLYMENT_STATE_FREEZED--【已冻结】--可能是该主体已完成过入驻，请查看驳回原因，并通知驳回原因中指定的联系人扫描微信支付返回的小程序码在小程序端完成授权流程<br>APPLYMENT_STATE_CANCELED--【已作废】--表示申请单已被撤销，无需再对其进行操作<br>APPLYMENT_STATE_NOAPPLY--未申请；<font color="green">示例值：APPLYMENT_STATE_WAITTING_FOR_AUDIT</font> |
| real_name_applyment_desc | 实名认证描述 | String | 128 | N |  申请实名时返回；<font color="green">示例值：</font> |
| qrcode_data | 授权二维码 | String | 128 | N | 若实名认证状态 real_name_applyment_stat=<br>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT、<br>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON、<br>APPLYMENT_STATE_PASSED、<br>APPLYMENT_STATE_FREEZED时返回；<font color="green">示例值：https://qr.alipay.com/bax02911brluc2xieoph6001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table aded3404_f012_4b63_9a03_050f2ef4fe49-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| apply_time | 申请单创建时间 | String | 20 | N | <font color="green">示例值：2017/11/11 12:00</font> |
| card_alias_no | 进件生成的卡编号 | String | 32 | N | 进件生成的卡编号，在发起结算时可以作为结算账号 |
| fk_audit | 风控审核状态 | String | 10 | N | CREATE：已创建待审批、SKIP：跳过风控审批步骤、PASS：风控审核通过、REJECT：风控审批拒绝；<font color="green">示例值：CREATE</font> |
| fk_audit_memo | 风控审批备注 | String | 64 | N | 风控审批备注，如有则返回 |
| kz_audit | 支付宝业务开通状态 | String | 64 | N | CREATE：已创建待审批、SKIP：跳过客资审批步骤、PASS：客资审核通过、REJECT：客资审批拒绝；<font color="green">示例值：CREATE</font> |
| kz_audit_memo | 客资审批备注 | String | 64 | N | 客资审批备注，如有则返回 |
| merchant_name | 进件时填写的商户名称 | String | 64 | N | 进件时填写的商户名称；<font color="green">示例值：上海汇付支付服务有限公司</font> |
| smid | 二级商户id | String | 32 | N | <font color="green">示例值：2088431912900000</font> |
| sub_confirm | 二级商户确认状态 | String | 16 | N | CREATE：已发起二级商户确认、SKIP：无需确认、FAIL：签约失败、NOT_CONFIRM：商户未确认、FINISH签约完成；<font color="green">示例值：CREATE</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 77fc8c34_70cf_4424_8937_579f6ea39347-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 开通状态 | String | 1 | Y | 0:关闭 1:开通；<font color="green">示例值：1</font> |
| fee_rate | 支付手续费(%) | String | 9 | N | 支付手续费(%)  支持两位小数；<font color="green">示例值：0.38</font> |
| fee_fix_amt | 支付固定手续费(元) | String | 9 | N | 支付固定手续费(元)支持两位小数；<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 16f04756_ad9f_47d1_80f4_92830d231f6c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| config_type | 配置类型 | String | 2 | Y | 01 -公众号配置  02-小程序配置 |
| config_value | 配置值 | String | 1 | Y | S-成功,F-失败，B-部分成功 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b2c5680e_c362_410e_b56a_901d77978be6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_mch_id | 特约商户号 | String | 32 | N | <font color="green">示例值：1632157057</font> |
| sales_scenes_type | 经营场景类型 | String | 32 | Y | 线下门店：SALES_SCENES_STORE<br>公众号：SALES_SCENES_MP<br>小程序：SALES_SCENES_MINI_PROGRAM<br>互联网：SALES_SCENES_WEB<br>APP：SALES_SCENES_APP<br>企业微信：SALES_SCENES_WEWORK<br/><font color="green">示例值：SALES_SCENES_WEWORK</font> |
| confirm_url | 超级管理员签约链接 | String | 512 | N | <font color="green">示例值：https://www.huifu.com</font> |
| apply_state | 申请单状态 | String | 32 | N | S：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；C：待签约<br/><font color="green">示例值：S</font> |
| reject_reason | 拒绝原因 | String | 256 | N | <font color="green">示例值：支付功能未开通</font> |
| mod_bank_acct_state | 结算卡修改结果返回码 | String | 1 | N | S:成功 F失败；<font color="green">示例值：S</font> |
| mod_bank_acct_desc | 结算卡修改结果返回描述 | String | 256 | N | <font color="green">示例值：成功</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 555d0dd6_7d02_4fcd_873d_a9890a9013a2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| apply_status | 申请单状态 | String | 1 | N | S：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；C：待签约；<font color="green">示例值：S</font> |
| confirm_url | 签约链接 | String | 256 | N | <font color="green">示例值：https://www.huifu.com</font> |
| mer_app_id | 应用ID | String | 32 | N | <font color="green">示例值：2022002178643452</font> |
| reject_reason | 拒绝原因 | String | 128 | N | <font color="green">示例值：未开通支付</font> |
| mer_code | 支付宝商户号 | String | 32 | N | <font color="green">示例值：2088031396541893</font> |
| apply_type | 申请类型 | String | 32 | N | FACE_TO_FACE：当面付；<font color="green">示例值：FACE_TO_FACE</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5775c0ff_d070_491a_a9b5_b02078e48f2b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_link | 协议签署连接 | String | 1024 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：</font> |
| agreement_id | 协议编号 | String | 64 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：</font> |
| agreement_name | 协议名称 | String | 256 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：</font> |
| con_stat | 合同状态 | String | 2 | N | 电子协议类型会返回以下值：<br/>2：创建合同异常<br/>3：待签约 <br/>4：签约中<br/>5：签约完成(电子协议只有签约完成才能做交易) <br/>6：已失效 <br/> 7：已拒签<br/> 8：签约失败<br/><font color="green">示例值：5</font> |
| agreement_type | _协议类型_ | String | 1 | N | 0-电子协议 |
| agreement_no | 协议号 | String | 32 | N | <font color="green">示例值：3245234</font> |
<!-- extend:end -->
