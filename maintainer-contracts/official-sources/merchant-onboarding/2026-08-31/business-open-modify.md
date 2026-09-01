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
## 商户业务开通修改

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/busi/modify

*最近更新时间：2026.08.12*
> 2023.6.30斗拱升级了商户进件类接口，老版接口、升级指引请参考[说明文档](old_api/api_2023shglsj)
### 应用场景
已完成业务开通的商户若信息填写有误或需变更，用此接口修改企业&小微商户业务信息。支持：
 - 商户微信、支付宝业务补开；（银联、银行卡业务开通仍通过[商户业务开通接口](https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt)）
 - 快捷支付、网银、手机网页支付等线上业务的开通；
 - 修改商户微信、支付宝、银联二维码、银行卡、快捷、网银、手机网页等业务的交易费率；

 **适用对象**  
  商户需要补开、修改已开通支付功能参数，可调用该接口。

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

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 业务申请编号，同一商户号当天唯一，<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 请求日期：yyyyMMdd，以北京时间为准；<font color="green">示例值：20220904</font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000104778898</font> |
| short_name | 微信支付宝商户简称 | String | 64 | N | 修改微信、支付宝商户简称；<font color="green">示例值：汇付天下</font> |
| <span class="extend 1cc81b3c_3b78_465b_b44e_00679a6071a6">agreement_info</span> | *协议信息实体* | String |  | N | jsonObject字符串；[签约协议材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx)<br/>若未签署过协议的情况下，调用该接口时必填；<br/>若已签署过纸质或电子协议下，调用该接口时必填，且只可以选择纸质或电子协议；<br/>若已签署过挂网协议下，调用该接口时，选填。 |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1：外扣，2：内扣；（默认2内扣）示例值：2 该公共参数只影响：支付宝支付，微信支付，银行卡支付，银联二维码支付，花呗分期配置 以下支付方式手续费请在各配置域字段中修改：网银、快捷、手机WAP、余额支付、补贴支付、全域资金管理、银行大额转账 |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时必填；示例值：6666000123123123 该公共参数只影响：支付宝支付，微信支付，银行卡支付，银联二维码支付，花呗分期配置 以下支付方式手续费请在各配置域字段中修改：网银、快捷、手机WAP、余额支付、补贴支付、全域资金管理、银行大额转账 |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01：基本户（不填默认01），02-现金户，05：充值户；09：营销户；示例值：01 该公共参数只影响：支付宝支付，微信支付，银行卡支付，银联二维码支付，花呗分期配置 以下支付方式手续费请在各配置域字段中修改：网银、快捷、手机WAP、余额支付、补贴支付、全域资金管理、银行大额转账 |
| <span class="showCompleteParams">online_flag</span> | 是否开通网银 | String | 1 | N | Y:是 N:否；<font color="green">示例值：Y</font> |
| <span class="showCompleteParams">quick_flag</span> | 是否开通快捷 | String | 1 | N | Y：是， N：否；<font color="green">示例值：Y</font> |
| <span class="showCompleteParams">withhold_flag</span> | 是否开通代扣 | String | 1 | N | Y:是 N:否；<font color="green">示例值：Y</font> |
| delay_flag | 延迟入账开关 | String | 1 | N | N：否，Y：是；默认否；<font color="green">示例值：Y</font> |
| alipay_pre_auth_flag | 开通支付宝预授权 | String | 1 | N | Y：是，N：否；<font color="green">示例值：Y</font>；目前仅支持MCC为7011住宿服务、7296服装出租、7512汽车出租三个行业开通预授权； |
| wechatpay_pre_auth_flag | 开通微信预授权 | String | 1 | N | Y：是，N：否；<font color="green">示例值：Y</font>；目前仅支持MCC为7011住宿服务、7296服装出租、7512汽车出租三个行业开通预授权； |
| mer_bus_type | 商户业务类型 | String | 2 | N | 快捷，网银，手机WAP，银联统一在线收银台开通时（线上费率配置对象不为空）必填；<br/>取值参见[商户业务类型](http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%95%86%E6%88%B7%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B)；<font color="green">示例值：01</font> |
| <span class="extend 2d6ce28c_2edf_4050_aadb_ad6527ffe80d showCompleteParams">online_fee_conf_list</span> | 线上费率配置 | String |  | N | jsonArray格式 |
| <span class="extend 955e3989_1534_48cb_85f2_bf64c16bf3ab">ali_conf_list</span> | 支付宝配置对象 | String |  | N | jsonArray格式字符串 |
| <span class="extend c43755a0_2d38_459f_b306_d6caee0e8c27">wx_conf_list</span> | 微信配置对象 | String |  | N | jsonArray格式字符串 |
| <span class="extend 00bbe674_5d0c_41cd_afd3_3f334f590c7c">union_conf_list</span> | 银联二维码配置对象 | String |  | N | jsonArray格式字符串 |
| <span class="extend 906e4fc1_b0dc_4f00_819a_8970ce087463">bank_card_conf</span> | 银行卡支付配置信息 | String |  | N | jsonObject字符串 |
| <span class="extend d3c95540_d66d_41d0_993c_cf675cf37784">balance_pay_config</span> | *余额支付配置对象* | String |  | N | jsonObject字符串 |
| <span class="extend 0f19bc4f_b9f7_4847_b3e5_010e2f2dd52e showCompleteParams">combine_pay_config</span> | 补贴支付 | String |  | N | jsonObject格式 |
| <span class="extend c8000ecb_bd67_4367_8a72_744586362426 showCompleteParams">online_pay_fee_conf_list</span> | 线上手续费承担方配置 | String |  | N | jsonArray格式 |
| <span class="extend 277cdca6_05de_4cef_9f44_995d4f502c1f showCompleteParams">out_order_funds_config</span> | 全域资金管理配置(华通银行) | String |  | N | jsonObject字符串；**即将废弃**，请对接[全渠道资金管理配置接口](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_qypz) |
| async_return_url | 异步消息接收地址 | String | 128 | N | 审核消息接收地址，<font color="green">示例值：http://service.example.com/to/path</font> 。为空不推送审核消息。 |
| busi_async_return_url | 业务开通结果异步消息接收地址 | String | 128 | N | 当前申请同步成功或者审核通过之后，<font color="green">示例值：http://service.example.com/to/path</font>。为空不推送审核消息。 |
| recon_resp_addr | 交易异步应答地址 | String | 256 | N | <font color="green">示例值：http://service.example.com/to/path</font>。为空不推送交易异步消息。 |
| <span class="extend b2cb1108_d934_4ef4_a074_162e97f1a475">online_media_info_list</span> | *运营媒介* | String |  | N | jsonArray字符串；如果开通快捷、网银、余额支付Pro版、分账、银行大额转账、代扣需提供运营媒介材料 |
| <span class="extend f3640ad3_0e33_443f_b864_f0cbd34f160a">extended_material_list</span> | *补充文件信息* | String |  | N | jsonArray字符串；根据开通的功能补充相关材料，包括[商户纸质协议说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx)、[线上行业补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx)、[开通余额支付补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E4%BD%99%E9%A2%9D%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx) 、[分账功能提供材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/spin/files/20260611/KYC-%E5%88%86%E8%B4%A6%E5%8A%9F%E8%83%BD%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E%281%29.xlsx) 、[代扣支付补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/%E4%BB%A3%E6%89%A3%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx)； |
| online_busi_type | *线上业务类型编码* | String | 8 | C | 开通快捷、网银、余额支付Pro版、银行大额转账、分账比例>30%、代扣必填；参见[线上业务类型编码及补充材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx)；<font color="green">示例值：H7999AL</font> |
| <span class="extend ee26f101_9115_4692_9ca2_768d37d37874">sign_user_info</span> | 签约人 | String |  | C | jsonObject字符串；agreement_info中选择电子签约时必填；个人商户填本人信息。 |
| forced_delay_flag | 商户开通强制延迟标记 | String | 1 | N | 选项：N：否 Y：是，默认否；**开关打开后商户所有交易都是延迟交易**，需要调用[交易确认接口](http://paas.huifu.com/open/doc/api/#/smzf/api_jyqr)完成交易；<font color="green">示例值：N</font> |
| <span class="extend a890b28f_39f4_4425_9256_13cddf26ec60 showCompleteParams">wx_zl_conf</span> | 微信直连配置对象 | String |  | N | jsonObject格式 |
| <span class="extend e0db17f1_5ad8_48b0_9227_774a1d580dbd showCompleteParams">ali_zl_conf</span> | 支付宝直连配置对象 | String |  | N | jsonObject格式 |
| enter_fee | 开户费用值(元) | String | 14 | N | <font color="green">示例值：5.00</font> |
| enter_fee_flag | 开户费用类型 | String | 1 | N | 1-一次性开户费，2-平台套餐费（元/年）<br/><font color="green">示例值：2</font> |
| online_refund | 是否开通在线退款 | String | 1 | N | N：否 Y：是；<font color="green">示例值：Y</font> |
| platform_refund | 是否支持平台退款 | String | 1 | N | N：否 Y：是；<font color="green">示例值：Y</font> |
| support_revoke | 是否支持撤销 | String | 1 | N | N：否 Y：是；<font color="green">示例值：Y</font> |
| <span class="extend 08b66b7f_6dbc_440f_8b65_0ed8812ef4df">split_conf_info</span> | 分账配置信息 | String |  | N | jsonObject字符串 |
| <span class="extend b8588871_fd0a_4971_9c5e_2a02aaa26da2 showCompleteParams">uni_app_payment_config</span> | 银联线上收银台 | String |  | N | jsonObject字符串 |
| <span class="showCompleteParams">fund_collection_flag</span> | 资金归集开通标记 | String | 1 | N | Y：是，N：否；<font color="green">示例值：Y</font> |
| <span class="extend 2ff9898e_abf9_4551_be1e_32efddb0cd9c showCompleteParams">surrogate_config_list</span> | 代发配置 | String |  | N | jsonArray格式字符串 |
| <span class="extend 41da7da6_63f0_44d9_b41f_59626cb4b551 showCompleteParams">large_amt_pay_config</span> | 大额支付配置 | String |  | N | jsonObject字符串 |
| half_pay_host_flag | 统一收银台开关 | String | 1 | N | Y:是 N:否（为空默认未开通） ；<font color="green">示例值：Y</font> |
| <span class="extend f779d4d4_b8b8_4621_9d3b_ef3e757b8cf8 showCompleteParams">agent_recheck_config</span> | 代发复核配置 | Object |  | N | jsonObject字符串 |
| <span class="showCompleteParams">online_recharge_flag</span> | 商户开通网银充值开关 | String | 1 | N | Y:是 N:否；<font color="green">示例值：Y</font> |
| refund_mend_open_flag | 是否开通垫资退款 | String | 1 | N | Y:是 N:否 ；<font color="green">示例值：Y</font> |
| <span class="extend 243a11a8_a956_4ebc_83f3_db8dfb4a1eee showCompleteParams">jxf_conf_info</span> | 捷行付配置 | Object |  | N | jsonObject字符串 |
| <span class="extend c40da533_43e0_4165_a2fb_e3cf45213db2 showCompleteParams">merge_pay_config_info</span> | 合单支付配置信息 | Object |  | N | jsonObject字符串 |
| bill_payment_flag | 是否开通账单支付 | String | 1 | N | Y:是 N:否 ；<font color="green">示例值：Y</font> |
| <span class="showCompleteParams">withhold_pay_scene</span> | 代扣场景 | String |  | C | withhold_flag开通需填写 1:权益投流(订阅),2:非权益投流(订阅),3:保险缴纳,4:道路通行费(ETC),5:公共事业(水电煤)缴费,6:物业缴费 |
| recon_resp_sys_id | 交易应答返回推送系统号 | String | 32 | N | 交易应答返回推送系统号；<font color="green">示例值：6666000123123123</font> |

<!-- extend:start -->
<!-- div:extend-table 1cc81b3c_3b78_465b_b44e_00679a6071a6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_type | *协议类型* | String | 1 | Y | 0-电子协议 1-纸质协议 3-挂网协议；<font color="green">示例值：3</font><br/>退出地区且开通（银联二维码或刷卡业务）不支持挂网协议；如果业务开通时选了纸质或电子，变更时也不支持挂网协议； |
| agreement_url | *挂网协议地址* | String | 256 | C | 挂网协议必填；**必须按示例值填写**，<font color="green">示例值：https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm</font>； |
| agree_begin_date | 纸质协议开始日期 | String | 8 | N | 格式yyyyMMdd，<font color="green">示例值：20220822</font> |
| agree_end_date | 纸质协议结束日期 | String | 8 | N | 格式yyyyMMdd，<font color="green">示例值：20230822</font> |
| message_send_type | 电子协议签约短信发送标识 | String | 1 | N | 协议类型为电子，业务开通审核通过后发送协议签约短信；<br/>0：发送，默认；<br/>1：不发送；<br/><font color="green">示例值：1</font> |
| agreement_async_return_url | 电子协议异步通知地址 | String | 128 | N | 示例值：http://service.example.com/to/path |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2d6ce28c_2edf_4050_aadb_ad6527ffe80d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_type | 业务类型 | String | 25 | Y | ONLINE_PERSON:个人网银支付，online_flag开通了才需要填；<br/>ONLINE_ENT:企业网银支付，online_flag开通了才需要填；<br/>QUICK_DEBIT:快捷借记卡支付，quick_flag开通了才需要填；<br/>QUICK_CREDIT:快捷贷记卡支付，quick_flag开通了才需要填；<br/>WAP:手机WAP支付，online_flag开通了才需要填；<br/>ONLINE_ENT_TOP_UP:B2B网银充值，online_recharge_flag开通了才需要填；<br/>ONLINE_PERSON_TOP_UP:B2C网银充值，online_recharge_flag开通了才需要填；<br/>WITHHOLD_DEBIT:代扣借记卡支付<br/>WITHHOLD_CREDIT:代扣贷记卡支付，withhold_flag开通了才需要填；<br/><font color="green">示例值：ONLINE_PERSON</font> |
| bank_id | 银行编码 | String | 8 | Y | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font> |
| dc_flag | 借贷标志 | String | 1 | Y | D:借记,C:贷记；<font color="green">示例值：D</font> |
| fix_amt | 手续费（固定/元） | String | 16 | N | 必须填写一种收费方式；保留两位小数；保留两位小数；<font color="green">示例值：1.00</font> |
| fee_rate | 费率（%） | String | 6 | N | 必须填写一种收费方式；保留两位小数；<font color="green">示例值：0.38</font> |
| bank_name | 银行名称 | String | 50 | N | <font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| bank_short_chn | 银行中文简称 | String | 50 | N | <font color="green">示例值：工行上海市中北支行</font> |
| stat_flag | 费率状态 | String | 1 | Y | 1开，0关；<font color="green">示例值：1</font> |
| fee_min_amt | 手续费最小值（元） | String | 6 | N | 必须填写一种收费方式；保留两位小数；保留两位小数；<font color="green">示例值：1.00</font> |
| fee_formula_type | 代扣手续费计费模式 | String |  | N | withhold_flag为Y时，才可传入；<br/>01: 百分比手续费，无封顶值或保底值<br/>02: 百分比手续费，有保底值<br/>03: 固定手续费<br/>04: 固定手续费+百分比手续费<br/>为空默认04 <font color="green">示例值：04</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 955e3989_1534_48cb_85f2_bf64c16bf3ab-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于0,保留2位小数；<font color="green">示例值：0.38</font> |
| fee_min_amt | 最低收取手续费（元） | String | 6 | N | 固定金额保留2位小数；大于0。需要渠道商开通此功能。<font color="green">示例值：0.38</font> |
| mcc | 商户经营类目 | String | 32 | N | 支付宝商户经营类目，[支付宝MCC](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc) ；<font color="green">示例值：5411</font> |
| pay_scene | 支付场景 | String | 2 | Y | 1、线下扫码，2.线上扫码，3.非盈利费率；<font color="green">示例值：1</font> |
| pay_channel_id | 子渠道号 | String | 50 | N | 不填入驻到渠道默认配置的支付宝渠道号下；<font color="green">示例值：JP00001</font> |
| switch_state | *功能开关* | String | 2 | Y | 1:开通 0:关闭 默认：1；<font color="green">示例值：1</font><br/> |
| is_check_real_name | 是否需要实名认证 | String | 1 | N | Y-是，业务功能开通成功后使用法人信息发起实名认证申请 ；  <br/>N-否；默认为N<br/><font color="green">示例值：Y</font> |
| <span class="extend d2760d0d_bc3b_4406_87e9_4c18d4169c82">al_real_name_info</span> | 实名认证信息 | String |  | N | 实名时需要填写；jsonObject字符串 <br/>若请求支付宝入驻成功，但实名申请失败需要调用单独的实名接口重新发起实名。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d2760d0d_bc3b_4406_87e9_4c18d4169c82-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| finance_institution_flag | 是否金融机构 | String |  | N | 选填，请根据申请主体的实际情况填写<br>1、若商户主体是金融机构，则填写：true。<br>2、若商户主体不是金融机构，则填写：false。<br>若未传入将默认填写：false<br>3，支付宝实名金融机构需要提供 F236：金融机构许可证图片一 ；F237：金融机构许可证图片二；F238：金融机构许可证图片三；F239：金融机构许可证图片四；F240：金融机构许可证图片五<br>补充资料填写在extended_material_list对象中；<font color="green">示例值：true</font> |
| finance_type | 金融机构类型 | String | 128 | N | 当主体是金融机构时，必填<br>金融机构类型需与营业执照/登记证书上一致<br>BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等<br>PAYMENT_AGENT：支付机构, 适用于非银行类支付机构<br>INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务<br>TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等<br>OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；<br/><font color="green">示例值：BANK_AGENT</font> |
| cert_type | 证书类型 | String | 64 | N | 企业商户必填<br>枚举：<br>统一社会信用代码证书(CERTIFICATE_TYPE_2389)<br>慈善组织公开募捐资格证书(CERTIFICATE_TYPE_2397)<br>社会团体法人登记证书(CERTIFICATE_TYPE_2394)<br>民办非企业单位登记证书(CERTIFICATE_TYPE_2395)<br>基金会法人登记证书(CERTIFICATE_TYPE_2396)<br>农民专业合作社法人营业执照(CERTIFICATE_TYPE_2398)<br>宗教活动场所登记证(CERTIFICATE_TYPE_2399)<br>其他证书/批文/证明(CERTIFICATE_TYPE_2400)<br>示例值：CERTIFICATE_TYPE_2389<br>政府机关/事业单位/其他组织 对应需要补充单位证明函照片 文件类型F46<br>补充资料填写在extended_material_list对象中；<font color="green">示例值：CERTIFICATE_TYPE_2395</font> |
| micro_biz_type | 小微经营类型 | String | 32 | N | 小微经营类型 必填字段<br>门店场所：MICRO_TYPE_STORE<br>流动经营/便民服务：MICRO_TYPE_MOBILE<br>线上商品/服务交易：MICRO_TYPE_ONLINE<br>个人商户需要填写；<font color="green">示例值：MICRO_TYPE_STORE</font><br/>需要提供 F22：店铺门头照图片；F24：店铺内景图片； 补充资料填写在extended_material_list对象中 |
| special_category_id | 特殊行业id | String | 20 | N | 特殊行业必填，参见支付宝商家行业二级类目code<br>1，支付宝实名特殊行业提供 F150:行业经营许可证资质照片一；F151:行业经营许可证资质照片二；F152:行业经营许可证资质照片三；F153:行业经营许可证资质照片四；F154:行业经营许可证资质照片五；F155:行业经营许可证资质照片六；<br>补充资料填写在extended_material_list对象中；<font color="green">示例值：100</font> |
| <span class="extend 788de602_c132_49dd_99b6_179ef02c561b">contact_person_info</span> | 联系人信息对象 | String |  | N |  |
| <span class="extend ace511db_54f7_46b1_981f_0829f3030793">legal_person_info</span> | 法人身份信息 | String |  | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 788de602_c132_49dd_99b6_179ef02c561b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 联系人姓名 | String | 64 | N | 为空时取企业商户取联系人姓名，个人商户取入驻时填写的名称；示例值：张三 |
| mobile | 联系人手机号 | String | 64 | N | 为空时取企业商户取联系人手机号；示例值：13917353627 |
| id_card_number | 联系人身份证号码 | String | 32 | Y | 示例值：320926198512053827 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ace511db_54f7_46b1_981f_0829f3030793-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| legal_type | 证件持有人类型 | String | 32 | N | 法人：LEGAL，为空时默认选项； 主体类型为企业、个体户、社会组织、小微商户时，必须为经营者/法人。<br/>经办人：SUPER；主体类型为政府机关、事业单位时默认是法人。若因特殊情况，无法提供法人证件时可填经办人类型。<br/>示例值：LEGAL |
| card_type | 证件类型 | String | 32 | N | 枚举值：00:身份证 01:护照 13：港澳居民证 14:台湾居民证；<br/>为空时取开户时法人信息<br/>个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关、小微商户仅支持身份证类型。<br/>示例值：00 |
| person_name | 姓名 | String | 64 | N | 为空时取开户时法人信息；示例值：李四 |
| card_no | 证件号码 | String | 64 | N | 为空时取开户时法人信息；示例值：233330199001010001 |
| effect_time | 证件生效时间 | String | 32 | N | 为空时取开户时法人信息；示例值：19990101 |
| expire_time | 证件过期时间 | String | 32 | N | 为空时取开户时法人信息；示例值：20001101，长期有效时传“长期” |
| card_front_img | 证件正面照 | String | 128 | N | 为空时取开户时法人信息，如果开户时未传该字段必填；上送图片上传返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| card_back_img | 证件反面照 | String | 128 | N | 为空时取开户时法人信息，如果开户时未传该字段必填；只有身份证类型需要上传反面；上送图片上传返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| auth_letter_img | 授权函照片 | String | 128 | N | 上送图片上传返回的jfileId；文件类型F224业务办理授权函；当证件持有人类型为经办人时必须上传。其他情况，无需上传。示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| is_benefit_person | 是否为受益人 | String | 1 | N | Y-受益人;N-非受益人 默认值：Y；示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c43755a0_2d38_459f_b306_d6caee0e8c27-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 开关状态 | String | 1 | Y | 1:开通，0关闭；<font color="green">示例值：1</font> |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于0,保留2位小数；<font color="green">示例值：0.38</font> |
| fee_min_amt | 最低收取手续费（元） | String | 6 | N | 固定金额保留2位小数；大于0。需要渠道商开通此功能。<font color="green">示例值：0.38</font> |
| pay_scene | 支付场景 | String | 2 | Y | 参见《[微信支付场景](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》说明；<font color="green">示例值：1</font> |
| fee_rule_id | 费率规则ID | String | 3 | N | [微信费率规则](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wxflgz)，简称cid。<font color="green">示例值：758</font> |
| pay_channel_id | 子渠道号 | String | 32 | N | 不填入驻到渠道默认配置的微信渠道号下；<font color="green">示例值：JP00001</font> |
| service_codes | 申请服务 | String | 100 | N | 微信(JSAPI:JSAPI支付,APPLET:小程序支付,MICROPAY:付款码支付,APP:app支付,MWEB:H5支付,PAP:委托代扣支付,AUTH:授权平台代扣支付),<br/><font color="green">示例值:[JSPAI","APPLET",MICROPAY"]</font><br/>默认值为:[JSPAI","APPLET","MICROPAY"] |
| is_check_real_name | 是否需要实名认证 | String | 1 | N | Y-是，业务功能开通成功后使用法人信息发起实名认证申请 ； N-否；默认为N ;<font color="green">示例值：Y</font> |
| <span class="extend ad24cf81_aacd_4aa1_b18b_0206c038cfc1">wx_real_name_info</span> | 实名认证信息 | Object |  | N | 实名时需要填写 jsonObject字符串 <br>若请求微信入驻成功，实名申请失败需要调用单独的实名接口重新发起实名。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ad24cf81_aacd_4aa1_b18b_0206c038cfc1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| finance_institution_flag | 是否金融机构 | String |  | N | 选填，请根据申请主体的实际情况填写，可参考选择：https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html<br>1、若商户主体是金融机构，则填写：true。<br>2、若商户主体不是金融机构，则填写：false。<br>若未传入将默认填写：false<br>3，微信实名金融机构需要提供 F236：金融机构许可证图片一 ；F237：金融机构许可证图片二；F238：金融机构许可证图片三；F239：金融机构许可证图片四；F240：金融机构许可证图片五<br>补充资料填写在extended_material_list对象中；<font color="green">示例值：false</font> |
| finance_type | 金融机构类型 | String | 128 | N | 当主体是金融机构时，必填<br>金融机构类型需与营业执照/登记证书上一致，可参考选择金融机构指引：<br>https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html<br>BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等<br>PAYMENT_AGENT：支付机构, 适用于非银行类支付机构<br>INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务<br>TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等<br>OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；<font color="green">示例值：INSURANCE</font> |
| cert_type | 证书类型 | String | 64 | N | 企业商户必填<br>CERTIFICATE_TYPE_2388：事业单位法人证书<br>CERTIFICATE_TYPE_2389：统一社会信用代码证书<br>CERTIFICATE_TYPE_2394：社会团体法人登记证书<br>CERTIFICATE_TYPE_2395：民办非企业单位登记证书<br>CERTIFICATE_TYPE_2396：基金会法人登记证书<br>CERTIFICATE_TYPE_2399：宗教活动场所登记证<br>CERTIFICATE_TYPE_2400：其他证书/批文/证明<br>CERTIFICATE_TYPE_2520：执业许可证/执业证<br>CERTIFICATE_TYPE_2521：基层群众性自治组织特别法人统一社会信用代码证<br>CERTIFICATE_TYPE_2522：农村集体经济组织登记证<br>主体为政府机关/其他组织/事业单位时,F46：单位证明函照片必填<br>主体为政府机关/其他组织/事业单位时,F45：登记证书必填<br>补充资料填写在extended_material_list对象中；<font color="green">示例值：CERTIFICATE_TYPE_2389</font> |
| micro_biz_type | 小微经营类型 | String | 32 | N | 小微经营类型 必填字段<br>门店场所：MICRO_TYPE_STORE<br>流动经营/便民服务：MICRO_TYPE_MOBILE<br>线上商品/服务交易：MICRO_TYPE_ONLINE<br>个人商户需要填写；<font color="green">示例值：MICRO_TYPE_STORE</font> <br/>需要提供 F22：店铺门头照图片；F24：店铺内景图片； 补充资料填写在extended_material_list对象中 |
| special_category_id | 特殊行业id | String | 3 | N | 特殊行业必填，参看微信支付提供的特殊行业id对照表：<br>https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/applysubject_new/chapter6_1.shtml<br>1，微信实名特殊行业提供 F150:行业经营许可证资质照片一；F151:行业经营许可证资质照片二；F152:行业经营许可证资质照片三；F153:行业经营许可证资质照片四；F154:行业经营许可证资质照片五；F155:行业经营许可证资质照片六；<br>补充资料填写在extended_material_list对象中；<font color="green">示例值：100</font>； |
| contact_type | 联系人类型 | String | 10 | N | LEGAL：经营者/法人；SUPER：经办人（经商户授权办理微信支付业务的人员），默认：LEGAL<br/>1、主体为“小微/个人卖家”，可选择：LEGAL<br/>2、主体为“个体工商户/企业/政府机关/事业单位/社会组织”，可选择：LEGAL、SUPER 示例值：LEGAL<br/>联系人类型为SUPER时需在extended_material_list文件列表中上传联系人证件正反面照片；<br/>F28：联系人身份证正面照；<br/>F29：联系人身份证反面照；<br/>F33：联系人**护照**人像面；<br/>F241：联系人证件照正面，非身份证与护照类型；<br/>F242：联系人证件照反面，非身份证类型； |
| name | 联系人姓名 | String | 64 | C | 联系人类型contact_type=SUPER时必填。示例值：张三 |
| mobile | 联系人手机号 | String | 11 | C | 联系人类型contact_type=SUPER时必填。示例值：13917364538 |
| contact_id_doc_type | 联系人证件类型 | String | 10 | C | 联系人类型contact_type=SUPER时必填。<br/>枚举值参见《自然人证件类型》说明，示例值：00<br/>个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关仅支持身份证类型。 |
| id_card_number | 联系人证件号码 | String | 32 | C | 联系人类型contact_type=SUPER时必填。示例值：320936198512035017 |
| contact_period_begin | 联系人证件有效期开始时间 | String | 20 | C | 联系人类型contact_type=SUPER时必填<br/>格式：yyyy-MM-dd；示例值：2019-06-06 |
| contact_period_end | 联系人证件有效期结束时间 | String | 20 | C | 联系人类型contact_type=SUPER时必填<br/>格式：yyyy-MM-dd；示例值：2029-06-06<br/>结束时间大于开始时间;若证件有效期为长期，请填写：长期 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 00bbe674_5d0c_41cd_afd3_3f334f590c7c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| charge_cate_code | 银行业务手续费类型 | String | 2 | N | 01：减免类<br/>02：优惠类<br/>03：标准类，默认标准类 。（小微商户仅有03标准类）；<br/>04：线上类<br/><font color="green">示例值：03</font> |
| switch_state | 功能开关 | String | 2 | N | 1:开通 0:关闭 默认：1；<font color="green">示例值：1</font><br/> |
| debit_fee_rate | 借记卡手续费（%） | String | 9 | Y | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：0.38</font> |
| credit_fee_rate_up | 贷记卡手续费1000以上（%） | String | 9 | Y | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：0.60</font> |
| credit_fee_rate_down | 贷记卡手续费1000及以下（%） | String | 9 | Y | 数字格式，大于等于0，保留2位小数；<font color="green">示例值：0.60</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 906e4fc1_b0dc_4f00_819a_8970ce087463-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| charge_cate_code | 银行业务手续费类型 | String | 2 | N | 01：减免类<br/>02：优惠类<br/>03：标准类（默认03）；<font color="green">示例值：03</font> |
| debit_fee_rate | 借记卡手续费（%） | String | 9 | Y | 数字类型，大于0,保留2位小数；<font color="green">示例值：0.50</font>代表费率为0.5% |
| debit_fee_limit | 借记卡封顶值 | String | 4 | N | 数字类型，大于0,保留2位小数；<font color="green">示例值：15.00</font> |
| credit_fee_rate | 贷记卡手续费（%） | String | 9 | Y | 数字类型，大于0,保留2位小数；<font color="green">示例值：0.60</font>代表费率为0.6% |
| is_open_small_flag | 是否开通小额双免 | String | 1 | N | 开关状态<br/>0：不开通双免<br/>1：开通双免<br/>2：仅免签；<font color="green">示例值：1</font> |
| small_free_amt | 小额双免单笔限额(元) | String | 9 | N | 限额需小于等于1000，不传默认0（不开通小额双免）；<font color="green">示例值：1000.00</font> |
| small_fee_amt | 小额双免手续费（%） | String | 9 | N | 数字类型，大于0,保留2位小数，开通小额双免填必须填制；<font color="green">示例值：0.38</font>代表费率为0.38% |
| switch_state | 功能开关 | String | 2 | N | 1:开通 0:关闭 默认：1；<font color="green">示例值：1</font><br/> |
| is_open_cloud_flag | 云闪付开通状态 | String | 1 | N | 0-关闭 1-开通 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d3c95540_d66d_41d0_993c_cf675cf37784-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 支付手续费(%) | String | 9 | N | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；<font color="green">示例值：0.50</font>代表费率为0.5% |
| fee_fix_amt | 支付固定手续费(元) | String | 9 | N | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；<font color="green">示例值：1.50</font><br/>注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额\*fee_rate |
| switch_state | 功能开关 | String | 2 | N | 1:开通 0:关闭 默认：1；<font color="green">示例值：1</font><br/> |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，<font color="green">示例值：01</font><br/>优先级高于相同名称的公共参数； |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时必填，<font color="green">示例值：6666000123123123</font><br/>优先级高于相同名称的公共参数； |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认2内扣），<font color="green">示例值：1</font><br/>优先级高于相同名称的公共参数； |
| balance_model | *业务模式* | String | 1 | Y | 2-入驻商户货款（周期性结算）<br/>3-营销补贴（周期性结算）<br/>4-推广方（渠道/代理/个人）的服务佣金/抽成<br/>5-红包发放<br/>6-钱包功能<br/>7-其他模式<br/>8-线上入驻商户货款（周期性结算）<br/>9-线上营销补贴（周期性结算）<br/>10-线上推广方（渠道/代理/个人）的服务佣金/抽成<br/>11-线上其他模式<br/>单选；<font color="green">示例值：6</font> |
| <span class="extend d4117e92_9390_4c10_b968_97bf1aca4b4c">description_info</span> | *业务情况说明* | Object |  | Y | jsonObject字符串 |
| charge_mode | 扣费模式 | String | 2 | N | 内扣时枚举值: 01: 默认规则, 02: 收款方分摊, 03: 交易时指定承担方<br>外扣时枚举值: 10: 指定承担方, 11: 出款方承担, 12: 交易时指定承担方<br><font color="green">示例值：11</font>；内扣时默认为01，外扣时默认为10； |
| pay_mode | 余额支付模式 | String | 4 | N | pro，lite；示例值：pro<br/>为空时默认为pro<br/>lite版不支持当日收款资金余额支付<br/><font color="green">示例值：lite</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d4117e92_9390_4c10_b968_97bf1aca4b4c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| busi_instruction | *业务模式说明* | String | 500 | C | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）。最大500个汉字，必填<br/><font color="green">示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。</font> |
| capital_instruction | *资金流向说明* | String | 500 | C | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等）。最大500个汉字，必填<br/><font color="green">示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。</font> |
| function_instruction | *功能开通用途说明* | String | 500 | C | 请详述所申请功能的原因、场景、涉及对象类型。最大500个汉字，必填<br/><font color="green">示例值：企业工资代发</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0f19bc4f_b9f7_4847_b3e5_010e2f2dd52e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 功能开关 | String | 1 | Y | 0：关闭，1：开通；<font color="green">示例值：1</font> |
| fee_rate | 支付手续费(%) | String | 9 | N | 支付手续费(%)  支持两位小数；<font color="green">示例值：0.50</font>代表费率为0.5% |
| fee_fix_amt | 支付固定手续费(元) | String | 9 | N | 支付固定手续费(元)支持两位小数；<font color="green">示例值：1.50</font><br/>注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额\*fee_rate |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | Y | 1:外扣，仅支持外扣，<font color="green">示例值：1</font><br/>优先级高于相同名称的公共参数； |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | Y | 开通交易手续费外扣业务时必填，<font color="green">示例值：6666000123123123</font><br/>优先级高于相同名称的公共参数； |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，<font color="green">示例值：01</font><br/>优先级高于相同名称的公共参数； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c8000ecb_bd67_4367_8a72_744586362426-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_type | 业务类型 | String | 25 | N | ONLINE_PERSON:个人网银<br/>ONLINE_ENT:企业网银<br/>QUICK:快捷<br/>WAP:手机WAP支付<br/>ONLINE_ENT_TOP_UP:B2B网银充值<br/>ONLINE_PERSON_TOP_UP:B2C网银充值<br/>WITHHOLD:代扣支付<br/><font color="green">示例值：WAP</font> |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户；<font color="green">示例值：01</font> |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时必填；<font color="green">示例值：6666000108854952</font> |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：2</font> |
| switch_state | 功能开关 | String | 1 | N | 0-关闭/1-打开；<font color="green">示例值：1</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 277cdca6_05de_4cef_9f44_995d4f502c1f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 功能开关 | String | 1 | Y | 全域资金管理配置功能开关。0:关闭，1:开通；<font color="green">示例值：1</font> |
| out_order_auto_acct_flag | 自动入账开关 | String | 1 | Y | 开通、关闭自动入账功能；0:关闭，1:开通；<font color="green">示例值：1</font><br/>关闭自动入账需要[处理银行来账通知](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_lztz)，并调用[汇付入账确认接口](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_yhskfk)来确认入账。 |
| fee_rate | 支付手续费(%) | String | 6 | N | 支持两位小数；<font color="green">示例值：0.45</font>；fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| fee_min_amt | 手续费最小值(元) | String | 6 | N | 支付手续费最小值，支持两位小数；<font color="green">示例值：1.00</font></br>fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户；<font color="green">示例值：01</font> |
| out_fee_flag | 交易手续费外扣标记 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：2</font> |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | <font color="green">示例值：6666000123123123</font> |
| <span class="extend 5b7dc8ba_8b20_4a31_9c17_029bc3315e24">out_order_acct_card</span> | 全域资金开户使用的银行卡信息 | Object |  | N | jsonObject字符串 |
| <span class="extend b67e2d8f_2d8d_4b0c_9eee_5cc6012534b8">out_order_acct_open_fees</span> | 全域资金开户手续费 | Object |  | N | jsonObject字符串 |
| business_model | 全域支付业务模式 | String | 20 | N | acquiringMode：收单模式，<br/><font color="green">示例值：acquiringMode</font> |
| other_payment_institutions_pic | 全渠道资金管理补充材料 | String | 64 | C | 涉及文件类型：F504-全渠道资金管理补充材料；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5b7dc8ba_8b20_4a31_9c17_029bc3315e24-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| prov_id | 银行所在省 | String | 6 | N | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> |
| area_id | 银行所在市 | String | 6 | N | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font> |
| bank_code | 银行编码 | String | 8 | N | 对公时根据支行编码获取总行编码；参考[银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font> |
| branch_code | 支行联行号 | String | 12 | N | card_type为0时必填，参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：102290026507</font> |
| branch_name | 支行名称 | String | 64 | N | card_type为0时必填 ,参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；<font color="green">示例值：中国工商银行上海市中山北路支行</font> |
| card_name | 结算账户名 | String | 128 | Y | 银行卡对应的户名；<font color="green">示例值：上海汇付支付有限公司</font> |
| card_no | 银行卡号 | String | 32 | Y | <font color="green">示例值：98140008801800008888</font> |
| card_type | 卡类型 | String | 1 | Y | 0:对公 1:对私；<font color="green">示例值：01</font> |
| cert_type | 持卡人证件类型 | String | 2 | C | 00:身份证；<font color="green">示例值：00</font>；card_type为1时选填。 |
| cert_begin_date | 持卡人证件有效期（起始） | String | 8 | C | card_type为1时选填；格式：yyyyMMdd，<font color="green">示例值：20210830</font>；<br/>若填写cert_no，cert_validity_type，cert_type需同时填写。 |
| cert_end_date | 持卡人证件有效期（截止） | String | 8 | C | cert_validity_type变更为0时必填，格式：yyyyMMdd；<font color="green">示例值：20210830</font> |
| cert_no | 持卡人证件号码 | String | 32 | C | card_type为1时选填；<font color="green">示例值：310112200001018888</font>； |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | N | card_type为1时选填；1:长期有效 0:非长期有效；<font color="green">示例值：0</font><br/>若填写cert_begin_date，cert_no，cert_type需同时填写。 |
| mp | 银行卡绑定手机号 | String | 11 | Y | <font color="green">示例值：18611111111</font> |
| open_licence_no | 开户许可证核准号 | String | 32 | N | <font color="green">示例值：J2900123456789</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b67e2d8f_2d8d_4b0c_9eee_5cc6012534b8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_fix_amt | 开户手续费(元) | String | 9 | Y | 支持两位小数；<font color="green">示例值：1.00</font> |
| out_fee_acct_type | 开户手续费外扣时的账户类型 | String | 2 | C | 01-基本户，02-现金户，05-充值户，09-营销户，不填默认01；<font color="green">示例值：01</font><br/>注：fee_fix_amt：开户手续费大于0时必填 |
| out_fee_huifuid | 开户手续费外扣汇付ID | String | 18 | C | 开通手续费外扣业务时必填；<font color="green">示例值：6666000109812123</font><br/>注：fee_fix_amt：开户手续费大于0时必填 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b2cb1108_d934_4ef4_a074_162e97f1a475-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| media_type | *运营媒介类型* | String | 2 | Y | S1-PC网站；若媒介项为PC网站：必填字段（PC网站域名、ICP备案/许可证号）<br/>S2-APP场景；若媒介项为APP场景：必填字段（APP名称、APP下载地址），若开通微信App支付，则新增app_id、app_name必填<br/>S3-小程序场景；若媒介项为小程序：必填字段（小程序名称）<br/>S4-公众号场景；若媒介项为公众号：必填字段（公众号名称）<br/>S5-其他；媒介项为其他：其他有效信息或链接地址必填<br/>线上场景时必填一项；<font color="green">示例值：S1</font> |
| media_name | *媒介名称* | String | 200 | C | PC网站域名／APP名称／小程序名称／公众号名称；<font color="green">示例值：汇付服务</font><br/>运营媒介类型为 ：S1/S2/S3/S4时，必填； |
| test_account | *测试账号* | String | 64 | N | <font color="green">示例值：test</font> |
| test_secret | *测试密码* | String | 64 | N | <font color="green">示例值：test</font> |
| mer_icp | ICP备案/许可证号 | String | 200 | C | 运营媒介类型为 ：S1时必填；<font color="green">示例值：沪ICP备06046402号-28</font> |
| other_info | *其他有效信息* | String | 200 | C | 其他有效信息或链接地址/APP下载地址；类型为S5或S2必填<br/><font color="green">示例值：http://download.huifu.com</font> |
| media_front_page | *运营媒介-首页* | String | 128 | N | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| media_service_page | *运营媒介-服务/商品明细页面* | String | 128 | N | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| media_order_page | *运营媒介-下单场景页面* | String | 128 | N | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| media_pay_page | *运营媒介-支付页面* | String | 128 | N | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| media_mer_common_flag | *媒介主体与商户主体是否一致* | String | 1 | C | Y/N；<font color="green">示例值：Y</font><br/>运营媒介为S1、S2、S3、S4且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填<br/>若不一致，则需提供ICP备案/APP/微信公众号/小程序主体与商户的使用授权或开发证明材料； |
| authorize_materials | *授权或开发证明材料* | String | 128 | C | 运营媒介为S1、S2、S3、S4且媒介主体与商户主体不一致时，且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font> |
| other_material | 微信APP补充材料 | String | 128 | C | 运营媒介为S2且开通微信下app支付时选填，具体见[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) |
| app_id | appId | String | 128 | C | 运营媒介为S2且开通微信下app支付时必填 |
| app_name | appId认证主体名称 | String | 128 | C | 运营媒介为S2且开通微信下app支付时必填 |
| supplement | 补充说明 | String | 512 | C | 运营媒介为S2且开通微信下app支付时选填 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f3640ad3_0e33_443f_b864_f0cbd34f160a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_id | *文件id* | String | 64 | Y | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取；<br/><font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_type | *文件类型* | String | 64 | N | [参见文件类型说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；开通[分账功能提供材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%88%86%E8%B4%A6%E5%8A%9F%E8%83%BD%E6%8F%90%E4%BE%9B%E6%9D%90%E6%96%99.xlsx)；<font color="green">示例值：F01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ee26f101_9115_4692_9ca2_768d37d37874-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 签约人类型 | String | 7 | Y | LEGAL-法人，对公结算或对私法人结算时可选法人签约；<br/>CONTACT-联系人，对公结算可选联系人（经办人）签约；<br/>OTHER-其他，对私非法人结算选“其他”，必须是结算人；<br/><font color="green">示例值：LEGAL</font> |
| name | 姓名 | String | 32 | C | 签约人类型=其他，必填；<font color="green">示例值：张三</font> |
| mobile_no | 手机号 | String | 11 | C | 签约人类型=法人/其他 ，必填；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；<font color="green">示例值：13917463536</font> |
| cert_no | 身份证 | String | 32 | C | 签约人类型=联系人/其他，必填 ；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；<font color="green">示例值：320946195712025082</font> |
| email | 邮箱 | String | 32 | N | <font color="green">示例值：example@email.com</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a890b28f_39f4_4425_9256_13cddf26ec60-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_mch_id | 微信子商户号 | String | 32 | Y | 微信支付分配的子商户号；<font color="green">示例值：1632157057</font> |
| <span class="extend 978473be_20af_4759_a6f8_6d3d72331504">wx_zl_pay_conf_list</span> | 配置集合 | Array | 512 | Y |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 978473be_20af_4759_a6f8_6d3d72331504-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| service_code | 申请服务 | String | 16 | Y | JSAPI-公众号，APPLET-小程序；<font color="green">示例值：JSAPI</font> |
| sub_app_id | 功能服务appid | String | 32 | Y | 子商户的公众号、小程序ID；<font color="green">示例值：wx51aa91a575359ff5</font> |
| switch_state | 功能开关 | String | 1 | Y | 0-关闭，1-打开；<font color="green">示例值：1</font> |
| fee_rate | 功能费率(%) | String | 6 | Y | 保留两位小数。<font color="green">示例值：0.60</font> |
| operate_type | 操作类型 | String | 10 | C | ADD-新增， UPDATE-修改， 默认新增；<font color="green">示例值：ADD</font> |
| <span class="extend e97fc51c_d20f_45ea_b7a1_882b8a03e7e7">contact_info</span> | 联系人信息 | Object |  | C | jsonObject字符串,新增时必填 |
| <span class="extend 06b9dcd7_e4de_4477_aacb_deb1375d362c">certificate_info</span> | 特殊主体登记证书 | Object |  | C | jsonObject字符串，商户营业执照类型为政府机关/事业单位/其他组织时，传入相应信息。新增时需填入 |
| <span class="extend 6d3c6454_5d56_47f0_8d2c_694062a50cc6">ubo_info</span> | 最终受益人信息 | Object |  | C | jsonObject字符串，商户类型为企业时，微信侧必填。（如果基本信息里有的话，可以不传取 huifu_id 对应的信息）。新增时填入 |
| <span class="extend 8f7a71f5_516a_4d25_a9c1_6cbc0da3ac61">sales_info</span> | 经营场景 | Object |  | C | jsonObject字符串，新增时填入 |
| <span class="extend b7e03d15_bd5b_4751_b933_bdad4023d09a">wx_card_info</span> | 银行账户信息 | Object |  | C | jsonObject字符串，该字段不填时，取商户在汇付系统录入的结算账号信息。新增或修改时填入，修改时必填 |
| business_addition_msg | 补充说明信息 | String | 512 | N | <font color="green">示例值：补充说明</font> |
| <span class="extend 1271a7f1_f3d6_4a13_845c_d88844abb26a">addition_file_list</span> | 补充说明文件列表 | Object |  | N | jsonArray格式，根据实际审核情况，额外要求商家提供指定的补充资料<br>F85-微信直连额外补充材料一<br>F86-微信直连额外补充材料二<br>F87-微信直连额外补充材料三<br>F88-微信直连额外补充材料四<br>F89-微信直连额外补充材料五<br>F90-法人开户承诺函<br>F91-法人开户意愿视频 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e97fc51c_d20f_45ea_b7a1_882b8a03e7e7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| contact_type | 联系人类型 | String | 1 | Y | 1： 法人；2：经办人；<font color="green">示例值：1</font> |
| contact_name | 联系人姓名 | String | 128 | C | 联系人类型为经办人时必填；<font color="green">示例值：张三</font> |
| cert_type | 联系人证件类型 | String | 2 | C | 联系人类型为经办人时必填；<br>00：身份证<br>01:护照<br>11：港澳台同胞通行证<br>12：外国人居留证<br>13：港澳居民证<br>14：台湾居民证<br/><font color="green">示例值：00</font>； |
| contact_cert_no | 联系人证件号码 | String | 18 | C | 联系人类型为经办人时必填；<font color="green">示例值：32090297512026402</font> |
| contact_mobile_no | 联系人手机号 | String | 11 | Y | <font color="green">示例值：13911111111</font> |
| contact_email | 联系人电子邮箱 | String | 40 | Y | <font color="green">示例值：carl.chen@huifu.com</font> |
| <span class="extend c1e865b1_3d95_473e_8941_6072be538e4f">contact_file_list</span> | 联系人资料 | Object |  | C | 联系人类型为经办人时必填<br>F28-联系人身份证国徽面   <br>F29-联系人身份证人像面<br>F227-微信业务办理授权函<br/><font color="green">示例值：</font> |
| contact_cert_validity_type | 证件有效期类型 | String | 1 | Y | 有效期类型 1:长期有效 0:非长期有效；<font color="green">示例值：1</font><br/>若长期有效，则无需填写证书有效期截止日期 |
| contact_cert_begin_date | 证件有效期开始日期 | String | 8 | Y | 格式：YYYYMMDD；<font color="green">示例值：20100908</font> |
| contact_cert_end_date | 证件有效期截止日期 | String | 8 | N | 格式：YYYYMMDD；<font color="green">示例值：20300908</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c1e865b1_3d95_473e_8941_6072be538e4f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 6 | Y | <font color="green">示例值：F50</font> |
| file_id | 文件jfileId | String | 64 | Y | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 06b9dcd7_e4de_4477_aacb_deb1375d362c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cert_type | 登记证书类型 | String | 32 | Y | CERTIFICATE_TYPE_2388：事业单位法人证书<br>CERTIFICATE_TYPE_2389：统一社会信用代码证书<br>CERTIFICATE_TYPE_2390：有偿服务许可证（军队医院适用）<br>CERTIFICATE_TYPE_2391：医疗机构执业许可证（军队医院适用）<br>CERTIFICATE_TYPE_2392：企业营业执照（挂靠企业的党组织适用）<br>CERTIFICATE_TYPE_2393：组织机构代码证（政府机关适用）<br>CERTIFICATE_TYPE_2394：社会团体法人登记证书<br>CERTIFICATE_TYPE_2395：民办非企业单位登记证书<br>CERTIFICATE_TYPE_2396：基金会法人登记证书<br>CERTIFICATE_TYPE_2397：慈善组织公开募捐资格证书<br>CERTIFICATE_TYPE_2398：农民专业合作社法人营业执照<br>CERTIFICATE_TYPE_2399：宗教活动场所登记证<br>CERTIFICATE_TYPE_2400：其他证书/批文/证明<br/><font color="green">示例值：CERTIFICATE_TYPE_2400</font> |
| cert_no | 证书号 | String | 32 | Y | 请填写登记证书上的证书编号。<font color="green">示例值：92650109MA79R8E308</font> |
| cert_mer_name | 证书商户名称 | String | 128 | Y | 请填写登记证书上的商户名称。<font color="green">示例值：上海汇付支付服务公司</font> |
| reg_detail | 注册地址 | String | 128 | Y | 请填写登记证书的注册地址。<font color="green">示例值：上海徐汇宜山路601号C5栋</font> |
| legal_name | 法人姓名 | String | 32 | Y | 1、只能由中文字符、英文字符、可见符号组成。<br>2、请填写登记证书上的法定代表人姓名。<font color="green">示例值：张三</font> |
| cert_validity_type | 证书有效期类型 | String | 1 | Y | 有效期类型 1:长期有效 0:非长期有效；<font color="green">示例值：0</font><br>若长期有效，则无需填写证书有效期截止日期 |
| cert_begin_date | 证书有效期开始日期 | String | 8 | Y | 格式：YYYYMMDD；<font color="green">示例值：20100908</font> |
| cert_end_date | 证书有效期截止日期 | String | 8 | N | 格式：YYYYMMDD；<font color="green">示例值：20300908</font> |
| <span class="extend 1350907b_763e_4702_ac56_6d932792755f">cert_file_list</span> | 文件列表 | Object |  | Y | jsonArray，F46-单位证明函，F45-登记证书 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1350907b_763e_4702_ac56_6d932792755f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 6 | Y | <font color="green">示例值：F50</font> |
| file_id | 文件jfileId | String | 64 | Y | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6d3c6454_5d56_47f0_8d2c_694062a50cc6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| ubo_type | 经营者/法人是否为受益人 | String | 1 | Y | Y-是，N-否；<font color="green">示例值：Y</font> |
| <span class="extend 08de14dd_27a0_487e_88ff_d9dbfc057cff">ubo_info_list</span> | 受益人信息列表 | Object |  | C | jsonArray格式,当ubo_type为Y时可不填 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 08de14dd_27a0_487e_88ff_d9dbfc057cff-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| ubo_cert_type | 证件类型 | String | 2 | Y | 00:身份证 01:护照；<font color="green">示例值：00</font> |
| ubo_cert_no | 证件号码 | String | 18 | Y | <font color="green">示例值：320926198512027462</font> |
| ubo_name | 姓名 | String | 32 | Y | <font color="green">示例值：张三</font> |
| ubo_cert_doc_address | 受益人证件居住地址 | String | 128 | Y | <font color="green">示例值：上海宝山区共富路11号</font> |
| ubo_cert_validity_type | 证件有效类型 | String | 1 | Y | 1:长期有效 0:非长期有效；<font color="green">示例值：0</font> |
| ubo_cert_begin_date | 证件有效期开始日期 | String | 8 | Y | <font color="green">示例值：20200908</font> |
| ubo_cert_end_date | 证件有效期截止日期 | String | 8 | N | <font color="green">示例值：20330908</font> |
| <span class="extend c516f533_5d9c_4ec1_b1b4_92023c7b7056">ubo_file_list</span> | 文件列表 | Object |  | Y | jsonArray，F228-受益人身份证正面（国徽面），F229-联系人身份证反面（人像面）；<font color="green">示例值：F229</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c516f533_5d9c_4ec1_b1b4_92023c7b7056-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 6 | Y | <font color="green">示例值：F50</font> |
| file_id | 文件jfileId | String | 64 | Y | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8f7a71f5_516a_4d25_a9c1_6cbc0da3ac61-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sales_scenes_type | 经营场景类型 | String | 256 | Y | 多个以英文逗号分割，至少要有一个<br>线下门店：SALES_SCENES_STORE<br>公众号：SALES_SCENES_MP<br>小程序：SALES_SCENES_MINI_PROGRAM<br>互联网：SALES_SCENES_WEB<br>APP：SALES_SCENES_APP<br>企业微信：SALES_SCENES_WEWORK<br/><font color="green">示例值：SALES_SCENES_WEWORK</font> |
| fee_rate | 功能费率 | String | 6 | C | 仅支持渠道商传入该字段。<font color="green">示例值：0.06</font><br>平台商户为子商户开通微信直连支付时，不支持该字段，取平台商户费率上送微信。 |
| fee_rate_file_list | 文件列表 | String |  | N | 微信直连商户费率材料，根据微信要求上送。<font color="green">示例值：d1451277-85c6-3177-ac3d-a8be47b9ae9d</font> |
| biz_store_name | 门店名称 | String | 128 | N | 不传，取 huifu_id 关联信息,微信侧条件必填；<font color="green">示例值：卡卡奶茶共富店</font> |
| biz_address_code | 门店省市编码 | String | 128 | N | 不传，取 huifu_id 关联信息,微信侧条件必填；<font color="green">示例值：310100</font> |
| biz_store_address | 门店地址 | String | 128 | N | 不传，取 huifu_id 关联信息,微信侧条件必填；<font color="green">示例值：上海宝山共富路1号</font> |
| biz_sub_jsapi_app_id | 线下场所对应的商家公众号APPID | String | 256 | C | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。<font color="green">示例值：wx51aa91a575359ff5</font> |
| biz_sub_mini_app_id | 线下场所对应的商家小程序APPID | String | 256 | C | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。<font color="green">示例值：wxea9c30a90fs8d3fe</font> |
| jsapi_app_id | 服务商公众号 ID | String | 256 | C | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| jsapi_sub_app_id | 商家公众号APPID | String | 256 | C | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。<font color="green">示例值：wxea9c30a90fs8d3fe</font> |
| mini_app_id | 服务商小程序APPID | String | 256 | C | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| mini_sub_app_id | 商家小程序APPID | String | 256 | C | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| app_app_id | 服务商应用APPID | String | 256 | C | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| app_sub_app_id | 商家应用APPID | String | 256 | C | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。<font color="green">示例值：wx51aa91a575359ff5</font> |
| web_domain | 互联网网站域名 | String | 256 | C | 开通互联网场景时填入；<font color="green">示例值：huifu.com</font> |
| web_app_id | 互联网网站对应的商家APPID | String | 256 | C | 开通互联网场景时填入；<font color="green">示例值：wx51aa91a575359ff5</font> |
| sub_corp_id | 商家企业微信CorpID | String | 256 | C | 开通企业微信场景时填入；<font color="green">示例值：xxxxx</font> |
| <span class="extend 6f9a72fe_27c5_421e_bc53_9d32d5f7ca73">sales_scenes_file_list</span> | 文件列表 | Object | 6 | Y | 场景资料文件<br>附件资料列表fileList<br>线下门店场景，F49与F50必传<br>公众号场景，F95，F96，F97，F98，F99，总共至少传1张，最多传5张<br>小程序场景，F60，F61，F62，F63，F64，总共至少传1张，最多传5张<br>APP场景，F65，F66，F67，F68，各传1张<br>互联网网站场景，若备案主体与申请主体不同，请务必上传加盖公章的网站授权函(F69)。<br>企业微信场景，F70，F71，F72，F73，F74，总共至少传1张，最多传5张<br>F49-店铺内景图片<br>F50-店铺门头照图片<br>F95-公众号页面截图一<br>F96-公众号页面截图二<br>F97-公众号页面截图三<br>F98-公众号页面截图四<br>F99-公众号页面截图五<br>F60-小程序截图截图一<br>F61-小程序截图截图二<br>F62-小程序截图截图三<br>F63-小程序截图截图四<br>F64-小程序截图截图五<br>F65-APP首页截图<br>F66-APP尾页截图<br>F67-APP应用内截图<br>F68-APP支付页截图<br>F69-网站授权函<br>F70-企业微信页面截图一<br>F71-企业微信页面截图二<br>F72-企业微信页面截图三<br>F73-企业微信页面截图四<br>F74-企业微信页面截图五<br/><font color="green">示例值：F74</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6f9a72fe_27c5_421e_bc53_9d32d5f7ca73-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 6 | Y | <font color="green">示例值：F50</font> |
| file_id | 文件jfileId | String | 64 | Y | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b7e03d15_bd5b_4751_b933_bdad4023d09a-table -->
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
<!-- div:extend-table 1271a7f1_f3d6_4a13_845c_d88844abb26a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 6 | Y | <font color="green">示例值：F50</font> |
| file_id | 文件jfileId | String | 64 | Y | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e0db17f1_5ad8_48b0_9227_774a1d580dbd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| apply_type | 申请类型 | String | 32 | Y | FACE_TO_FACE：当面付；<font color="green">示例值：FACE_TO_FACE</font> |
| contact_name | 联系人姓名 | String | 64 | N | 支付宝联系人信息，不传取商户的联系人信息；<font color="green">示例值：张三</font> |
| contact_mobile_no | 联系人手机号 | String | 11 | N | 支付宝联系人信息，不传取商户的联系人信息；<font color="green">示例值：13911111111</font> |
| contact_email | 联系人电子邮箱 | String | 40 | N | 支付宝联系人信息，不传取商户的联系人信息；<font color="green">示例值：carl.chen@huifu.com</font> |
| order_ticket | 订单授权凭证 | String | 40 | N | <font color="green">示例值：</font> |
| account | 商户支付宝账号 | String | 128 | Y | 商户登录支付宝控台的账号；<font color="green">示例值：zhangsan</font> |
| fee_rate | 服务费率 | String | 6 | C | 仅支持渠道商。平台商户调用不支持该字段<br>服务费率（%），0.38~3之间，精确到0.01。<font color="green">示例值：0.06</font> |
| license_code | 营业执照编号 | String | 20 | N | 工商营业执照编号，<font color="green">示例值：92650109MA79R8E308</font> |
| license_validity_type | 营业执照有效期类型 | String | 1 | N | 1:长期有效 0:非长期有效<font color="green">示例值：</font> |
| license_begin_date | 营业执照有效期开始日期 | String | 8 | N | 日期格式yyyyMMdd，<font color="green">示例值：20110112</font> |
| license_end_date | 营业执照有效期截止日期 | String | 8 | N | 日期格式yyyyMMdd，<font color="green">示例值：20110112</font> |
| <span class="extend 40b985cc_3e48_4e7a_8d1a_87c09cb5fa0d">file_list</span> | 文件列表 | Object |  | Y | jsonArray格式，F47-企业特殊资质图片(可选，企业特殊资质图片，可参考商家经营类目中的“需要的特殊资质证书”)<br>F48-营业执照授权函图片（可选，个体工商户如果使用总公司或其他公司的营业执照认证需上传该授权函图片）<br>F49-店铺内景图片(可选)<br>F50-店铺门头照图片(必填)<br/><font color="green">示例值：F50</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 40b985cc_3e48_4e7a_8d1a_87c09cb5fa0d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 6 | Y | <font color="green">示例值：F50</font> |
| file_id | 文件jfileId | String | 64 | Y | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 08b66b7f_6dbc_440f_8b65_0ed8812ef4df-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| rule_origin | 分账规则来源 | String | 2 | Y | 01 接口发起 02页面配置；<font color="green">示例值：01</font> |
| div_flag | 分账开关 | String | 1 | Y | Y：开，N：关；<font color="green">示例值：Y</font> |
| apply_ratio | 最大分账比例% | String | 9 | Y | 0-100 的数值，支持两位小数; <font color="green">示例值：20.00</font> |
| <span class="extend 15bdd769_1dad_4329_b640_59244a527e7a">acct_split_bunch_list</span> | 分账明细 | Object |  | N | 分账规则来源选择平台配置时必填,jsonArray格式 |
| start_type | 生效类型 | String | 1 | N | 0-审核通过即时生效；1-审核通过次日生效；<font color="green">示例值：1</font> |
| out_fee_flag | 交易手续费外扣开关 | String | 1 | N | 1:外扣 2:内扣（默认）；<font color="green">示例值：1</font> |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户(默认)，02-现金户，05-充值户；<font color="green">示例值：01</font> |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | 选择手续费外扣时必填；<font color="green">示例值：</font> |
| split_fee_rate | 手续费% | String | 9 | N | 开通分账业务时必须填写一种收费方式；百分比，支持两位小数；<font color="green">示例值：1.00</font> <br/>分账手续费收取方式为费率手续费与固定手续费之和 |
| per_amt | 固定手续费 | String | 9 | N | 开通分账业务时必须填写一种收费方式；单位元，支持小数点后两位；<font color="green">示例值：1.00</font> <br/>分账手续费收取方式为费率手续费与固定手续费之和 |
| scene | 分账模式 | String | 2 | Y | 00-其他<br>01-医美医院分账<br>02-线上其他<br>A1- 教培机构分账<br>A2-公办/民办学校分账<br>A3-医美渠道独立收款分账<br>A4-线上供应商货款<br>A5-线上推广方（渠道/代理/个人）的服务佣金/抽成<br>A7-入驻商户货款<br>A8-线下供应商货款<br>A9-线下推广方<br>A10-个人与合作方分账<br>单选；<font color="green">示例值：A9</font> |
| <span class="extend e4fe4505_de94_4e55_a090_6ed53f020e8e">split_ext_info</span> | 业务情况说明 | Object | 128 | N | jsonObject；分账模式选择则其它，分账比例30%以上必填； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 15bdd769_1dad_4329_b640_59244a527e7a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 分账比例 | String | 9 | Y | 百分比支持两位小数，<font color="green">示例值：0.20</font> |
| huifu_id | 汇付Id | String | 18 | Y | <font color="green">示例值：6666000104778898</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e4fe4505_de94_4e55_a090_6ed53f020e8e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| busi_instruction | *业务模式说明* | String | 500 | Y | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）。最大500个汉字，必填<br/><font color="green">示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。</font> |
| capital_instruction | *资金流向说明* | String | 500 | Y | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等）。最大500个汉字，必填<br/><font color="green">示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。</font> |
| function_instruction | *功能开通用途说明* | String | 500 | Y | 请详述所申请功能的原因、场景、涉及对象类型。最大500个汉字，必填<br/><font color="green">示例值：企业工资代发</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b8588871_fd0a_4971_9c5e_2a02aaa26da2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 状态开关 | String | 1 | N | 0-关闭; 1-开通, 为空默认开通；<font color="green">示例值：1</font> |
| debit_fee_rate | 借记手续费（%） | String | 6 | C | 借记卡费率与贷记卡费率不能同时为空;<br>保留2位小数，最大值100.00，最小值0.00；<font color="green">示例值：0.02</font> |
| credit_fee_rate | 贷记手续费（%） | String | 6 | C | 借记卡费率与贷记卡费率不能同时为空;<br>保留2位小数，最大值100.00，最小值0.00；<font color="green">示例值：0.06</font> |
| out_fee_flag | 是否交易手续费外扣 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：1</font> <br/>如果不为空，则out_fee_acct_type，out_fee_huifuid，out_fee_flag取单独配置，否则取公共配置； |
| out_fee_huifuid | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时必填；<font color="green">示例值：6666000123123123</font> |
| out_fee_acct_type | 交易手续费外扣时的账户类型 | String | 2 | N | 01-基本户，02-现金户，05-充值户，09-营销户；不填默认01；<font color="green">示例值：01</font> |
| cloud_quick_pass_secret_free_flag | 云闪付免密支付开通标识 | String | 1 | N | Y：是，N：否；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2ff9898e_abf9_4551_be1e_32efddb0cd9c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 开通状态 | String | 1 | N | 1:是 0:否, 为空默认开；<font color="green">示例值：1</font> |
| surrogate_type | 代发业务类型 | String | 2 | Y | D0:当日到账；<br>T1:下个工作日到账;<br>D1:下个自然日到账;<br><font color="green">示例值：T1</font> |
| fix_amt | 手续费（固定/元） | String | 17 | C | 手续费（固定/元），保留小数点后两位；fee_formula_type为05，06时必填 <font color="green">示例值：1.00</font> |
| fee_rate | 手续费（百分比/%） | String | 6 | C | 手续费（百分比/%），保留小数点后两位；取值范围[0.00,100.00]；fee_formula_type为01，02，03，06时必填 <font color="green">示例值：0.05</font> |
| out_fee_flag | 是否交手续费外扣标记 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）<br>优先级高于相同名称的公共参数；<font color="green">示例值：1</font> |
| out_fee_acct_type | 交易手续费外扣时账户类型 | String | 2 | N | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，<font color="green">示例值：01</font><br>优先级高于相同名称的公共参数； |
| out_fee_huifu_id | 交易手续费外扣汇付ID | String | 18 | N | 开通交易手续费外扣业务时必填，<font color="green">示例值：6666000123123123<br>优先级高于相同名称的公共参数； |
| surrogate_private_flag | 是否允许对私代发 | String | 1 | N | 是否允许代发卡为对私类型<br>Y:允许 N:不允许；<font color="green">示例值：Y</font> |
| fee_formula_type | 代发手续费计费模式 | String | 17 | C | 01: 百分比手续费，无封顶值或保底值<br/>02: 百分比手续费，有保底值<br/>03: 百分比手续费，有封顶值<br/>05: 固定手续费 <br/>06: 固定手续费+百分比手续费<br/>为空默认06 <font color="green">示例值：06</font> |
| fee_max_amt | 手续费封顶值（固定/元） | String | 17 | C | 手续费封顶值（固定/元），保留小数点后两位；fee_formula_type为03时必填 <font color="green">示例值：100.00</font> |
| fee_min_amt | 手续费保底值（固定/元） | String | 17 | C | 手续费保底值（固定/元），保留小数点后两位；fee_formula_type为02时必填 <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 41da7da6_63f0_44d9_b41f_59626cb4b551-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 3c692b97_d3f7_4314_8d76_19ac9b95845d">large_amt_pay_config_info_list</span> | 大额支付配置列表 | Object |  | Y | 大额支付配置列表，jsonArray格式 |
| out_fee_flag | 交易手续费外扣标记 | String | 1 | N | 1:外扣 2:内扣（默认2内扣）；<font color="green">示例值：1</font> |
| out_fee_huifu_id | 交易手续费外扣huifuId | String | 18 | C | 交易手续费外扣时必填；<font color="green">示例值：6666000108854952</font> |
| out_fee_acct_id | 交易手续费外扣账户号 | String | 16 | C | 交易手续费外扣时必填；<font color="green">示例值：F00598602</font> |
| mer_payer_card_type | 商户付款方卡类型 | String | 10 | N | CORPORATE-对公,PRIVATE-对私,ALL-全部，默认全部<br><font color="green">示例值：ALL</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3c692b97_d3f7_4314_8d76_19ac9b95845d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| switch_state | 功能开关 | String | 1 | N | 1:开通 0:关闭 默认：1；<font color="green">示例值：1</font> |
| business_model | 大额支付业务模式 | String | 15 | Y | 大额支付业务模式 bank：银行模式 provisions：备付金模式；<font color="green">示例值：bank</font> |
| fee_rate | 费率（%） | String | 6 | C | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；<font color="green">示例值：1.00</font> |
| fee_fix_amt | 交易手续费（固定/元） | String | 9 | C | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；<font color="green">示例值：10.00</font> |
| biz_type | 大额调账标识申请类型 | String | 2 | N | 01-四要素，05-三要素；[订单匹配的要素信息](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_ddppys)；<font color="green">示例值：05</font> |
| mer_same_card_recharge_flag | 是否允许绑卡支付 | String | 1 | N | Y-开通/N-关闭，备付金模式时，支持传入；备付金模式银行卡绑定支付权限；<font color="green">示例值：Y</font> |
| allow_user_deposit_flag | 是否允许用户入账 | String | 1 | N | Y-开通/N-关闭 ；默认为N；<font color="green">示例值：Y</font> |
| provisions_auto_refund_flag | 备付金固定账号模式自动退款 | String | 1 | N | Y-开通/N-关闭 ；<font color="green">示例值：Y</font>；该配置仅在开通大额支付备付金绑卡模式时生效 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f779d4d4_b8b8_4621_9d3b_ef3e757b8cf8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agent_recheck_flag | 代发复核开关 | String | 1 | N | Y:是 N:否（为空默认未开通） ；<font color="green">示例值：Y</font> |
| agent_recheck_huifu_id | 复核授权商户号 | String | 18 | N | 复核授权商户号只能填当前商户主体或总部商户号 |
| agent_recheck_type | 复核类型 | String | 1 | N | A:复核  B:短信验证 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 243a11a8_a956_4ebc_83f3_db8dfb4a1eee-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_type | 账户类型 | String | 1 | Y | 2:银行账户 |
| open_flag | 开通状态 | String | 1 | Y | Y:开 N:关 |
| bank_name | 银行名称 | String | 8 | Y | PINGAN-平安银行 BOC-中国银行；<font color="green">示例值：PINGAN</font> |
| <span class="extend a257039a_2631_456c_a166_8bc8cf3d0339">jxf_bank_info</span> | 银行账户信息 | Object |  | C | 当账户类型为银行账户时必填 |
| <span class="extend 429d5c50_a6cd_4acd_be0c_ea80ebe6d6f2">jxf_fee_info</span> | 手续费信息 | Object |  | N | jsonObject字符串 |
| pay_confirm_flag | 付款确认标识 | String | 1 | N | Y:是 N:否 ；<font color="green">示例值：Y</font> |
| pay_confirm_req_url | 付款确认请求URL | String | 256 | C | 付款确认标识为Y时，该字段必填 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a257039a_2631_456c_a166_8bc8cf3d0339-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| user_name | 操作人姓名 | String | 16 | C | 银行名称非平安银行时，需填写；示例：张三 |
| operator_phone | 操作人手机号 | String | 11 | C | 银行名称非平安银行时，需填写；示例：13333333333 |
| acct_type | 付款方账户类型 | String | 2 | N | 00：单位结算卡，不填默认单位结算卡 |
| acct_no | 付款方账号 | String | 50 | Y | 示例：6212149999831234577 |
| acct_name | 付款方账户名称 | String | 25 | Y | 示例：上海汇付支付有限公司 |
| bank_branch_code | 开户行联行号 | String | 50 | Y | 示例：991290000099 |
| bank_branch_name | 开户行行名 | String | 25 | Y | 示例：中国银行 |
| sign_start_date | 签约申请生效日期 | String | 8 | C | 银行名称非平安银行时，需填写；示例：20251219 |
| sign_end_date | 签约申请失效日期 | String | 8 | C | 银行名称非平安银行时，需填写；示例：20261219 |
| remark | 附言 | String | 128 | N | 示例：附言 |
| org_code | 机构编码 | String | 64 | Y | 示例：12133 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 429d5c50_a6cd_4acd_be0c_ea80ebe6d6f2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| open_card_fix_fee | 虚拟卡开卡手续费（元） | String | 11 | N | 单位元，支持小数点后两位；<font color="green">示例值：1.00</font> 虚拟卡开卡手续费收取方式为发放数量*固定手续费 |
| quota_issue_fee_rate | 虚拟卡额度发放手续费（%） | String | 6 | N | 百分比，支持两位小数；<font color="green">示例值：1.00</font> 虚拟卡发放额度手续费收取方式为交易金额*费率手续费 |
| out_fee_flag | 捷行付手续费内外扣标记 | String | 1 | N | 捷行付手续费只支持外扣；1:外扣；<font color="green">示例值：1</font> |
| out_fee_huifuid | 捷行付手续费外扣汇付ID | String | 18 | C | 捷行付设置手续费时必填；<font color="green">示例值：6666000108854952</font> |
| out_fee_acct_type | 捷行付手续费扣款账户类型 | String | 2 | C | 捷行付手续费外扣时必填；01-基本户(默认)，05-充值户；<font color="green">示例值：01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c40da533_43e0_4165_a2fb_e3cf45213db2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| merge_pay_flag | 合单支付开关 | String |  | Y | 合单支付开关 Y：开通 N：关闭 |
| <span class="extend 47d4cf80_3254_4d44_883e_2d1026857c79">merge_pay_config</span> | 合单支付配置 | Object |  | C | 合单支付配置 （当合单支付开关为开时必填） |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 47d4cf80_3254_4d44_883e_2d1026857c79-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| merge_pay_mode | 合单支付模式 | String |  | Y | 1:电商 2:加油站 3:停车场 4:物业 5:休闲娱乐（不同模式需上传不同材料信息，调用图片上传接口；若选择电商，需上传文件F673《电商平台商家入驻协议》、F674《商家入驻截图》，以及填写线上业务类型编码及运营媒介字段信息；若选择加油站，需上传文件F676《加油站与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择停车场，需上传文件F677《停车场与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择物业需上传文件F678《物业与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择休闲娱乐需上传文件F679《休娱与任一合单参与方合作协议》、F675《任一合单参与方经营照片》） |
<!-- extend:end -->


#### 请求示例

```json
{  
    "sys_id":"ssproxy_dev",  
    "data":{  
        "req_seq_id":"2022042213314053740test001",  
        "req_date":"20220422",  
        "huifu_id":"6666000103668046",  
        "delay_flag":"Y",  
        "out_fee_flag":"2",  
        "out_fee_huifuid":"",  
        "out_fee_acct_type":"",  
        "async_return_url":"http://www.baidu55.com",  
        "busi_async_return_url":"",  
        "ali_conf_list":"[{\"pay_scene\":\"1\",\"fee_rate\":\"3.15\",\"mcc\":\"2016062900190337\",\"pay_channel_id\":\"10000001\",\"indirect_level\":\"\"}]",  
        "wx_conf_list":"[{\"service_codes\":\"\",\"pay_scene\":\"10\",\"fee_rate\":\"2.15\",\"mcc\":\"5943\",\"pay_channel_id\":\"JP00001\",\"fee_rule_id\":\"765\"}]",  
        "union_conf_list":"[{\"charge_cate_code\":\"\",\"debit_fee_rate_up\":\"6\",\"debit_fee_limit_up\":\"641\",\"credit_fee_rate_up\":\"6.566\",\"debit_fee_rate_down\":\"2.55\",\"debit_fee_limit_down\":\"11.3\",\"credit_fee_rate_down\":\"1\"}]",  
        "bank_card_conf":{  
            "charge_cate_code":"02",  
            "debit_fee_rate":"3",  
            "debit_fee_limit":"5",  
            "credit_fee_rate":"6",  
            "cloud_debit_fee_rate_up":"7",  
            "cloud_debit_fee_limit_up":"8.922",  
            "cloud_credit_fee_rate_up":"4.86",  
            "cloud_debit_fee_rate_down":"0",  
            "cloud_debit_fee_limit_down":"10",  
            "cloud_credit_fee_rate_down":"2",  
            "is_open_small_flag":"0",  
            "small_free_amt":"500",  
            "small_fee_amt":"1"  
        },
        "quick_flag":"",  
        "withhold_flag":"",  
        "online_flag":"",  
        "short_name":"",  
        "agreement_info":{  
            "agreement_type":"0",  
            "agreement_no":"202106070100000380",  
            "agreement_model":"202106070100000380",  
            "agreement_name":"电子协议签约模板",  
            "sign_date":"20200325",  
            "agree_begin_date":"20200325",  
            "agree_end_date":"20400325"  
        },  
        "alipay_pre_auth_flag":"Y",  
        "balance_pay_config":{  
            "switch_state":"1",  
            "fee_rate":"2",  
            "fee_fix_amt":"1"  
        },  
        "combine_pay_config":{  
            "switch_state":"0",  
            "fee_rate":"10",  
            "fee_fix_amt":"5"  
        },  
        "recon_resp_addr":"http://192.168.85.157:30031/sspm/testVirgo"
    },
    "sign":"jtu0LvjqGknAoccmVHs1h9ZDcehwpW9zb9m3y2jeMBRjFlqtAh1ftAKCOiLuPMHttQTuodPf05GROrYcOCg2SZrvRaFztyNZErfYl2LFi/OOX3VVFHAh9rTWtUs61zrOF6MVt1em18WrnfXVSN0oFXMQRmt4q8IGJgs3d5Hmwi8=",  
    "product_id":"ZDTEST"  
}

```
### 返回参数


#### 同步返回

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| resp_desc | 返回描述 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| huifu_id | 商户号 | String | 18 | N | 汇付分配的商户号，<font color="green">示例值：6666000105215341</font> |
| apply_no | 申请单号 | String | 18 | N | 审核中时有值，汇付返回商户的业务申请单号；<font color="green">示例值：202209120038432</font> |


#### 异步返回

**异步公共返回参数**

| 参数      | 中文名       | 类型   | <div style="width: 25pt">长度</div> | 必填 | 说明                 |
| :-------- | :----------- | :----- | :------- | :--- | :------------------- |
| resp_code | 网关返回码   | String | 6        | Y    | [网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#网关返回码)          |
| resp_desc | 网关返回描述 | String | 512      | Y    | [网关返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#网关返回码)         |
| sign      | 签名         | String |          | Y    | 签名，对报文整体签名 |
| data      | 业务返回参数 | String |          | N    | JSON                 |

**data**   

申请单审核异步：申请单审核通过后，往async _ return_url地址推送审核结果。

| 参数          | 中文名       | 类型   | <div style="width: 25pt">长度</div> | 必填 | 说明                                |
| :------------ | :----------- | :----- | :------- | :--- | :---------------------------------- |
| sub_resp_code | 业务返回码   | String | 8        | Y    | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| sub_resp_desc | 业务返回描述 | String | 512      | Y    | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码)                        |
| req_seq_id    | 请求流水号   | String | 32       | Y    | 原样返回请求参数的请求流水号；<font color="green">示例值：2022012614120615001</font>|
| req_date      | 请求时间     | String | 8        | Y    |原请求时间yyyyMMdd；<font color="green">示例值：20220912</font>|
| audit_status  | 审核结果     | String | 1        | Y    | Y：审核通过  N：审核拒绝 F：失败 C：拒签；<font color="green">示例值：Y</font>   |
| audit_desc    | 审核描述     | String | 512      | N    | 审核结果描述                        |
| product_id    | 产品编号     | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>  |
| huifu_id      | 汇付客户号   | String | 18       | Y    | 汇付分配的商户号，<font color="green">示例值：6666000105215341</font>  |
| apply_no      | 申请单号     | String | 18       | N    | 汇付返回商户的业务申请单号；<font color="green">示例值：202209120038432</font>        |

业务开通结果异步：申请单审核通过，各支付业务开通完成之后，往busi_async_return_url地址推送业务开通结果。按每个业务（notify_type：W:微信 A：支付宝 U:银联二维码 B:刷卡 E:全域资金管理 J:大额转账备付金模式，I:大额转账银行模式）推送给调用方一条。

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | 业务返回码 |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | 业务返回描述 |
| req_seq_id | 请求流水号 | String | 32 | Y | 原请求流水号；示例值：2022012614120615001 |
| req_date | 请求时间 | String | 8 | Y | 原请求时间yyyyMMdd；示例值：20220912 |
| product_id | 产品编号 | String | 32 | Y | 汇付分配的产品号，<font color="green">示例值：YYZY</font> |
| huifu_id | 汇付客户号 | String | 18 | Y | 汇付分配的产品号，示例值：YYZY |
| apply_no | 申请单号 | String | 18 | N | 汇付返回商户的业务申请单号；示例值：202209120038432 |
| notify_type | 通知类型 | String | 1 | Y | W:微信  A：支付宝，U:银联二维码，B:刷卡 E：全域资金管理，J:大额转账备付金模式，I:大额转账银行模式<font color="green">示例值：W</font> |
| <span class="extend 36212a1e_8808_4d1a_83d4_c6147b25bcb8">reg_result_list</span> | 入驻结果集合 | String |  | N | josnArray格式；notify_type等于A或者W时，此集合可能有多条数据 |
| ord_id | 通知流水号 | String | 44 | N | 回调方返回应答，应答内容为：”RECV_ORD_ID_”+该ordId |
| <span class="extend e72c6115_a2cb_4a80_8c48_6643ff19d93b">zl_async_info</span> | 直连结果合集 | String | 512 | N | 直连微信/支付宝结果合集 |

<!-- extend:start -->
<!-- div:extend-table 36212a1e_8808_4d1a_83d4_c6147b25bcb8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 费率类型 | String | 2 | N | 请求参数pay_scene；当notify_type是W/A时返回；参见《[微信支付场景](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》说明；<font color="green">示例值：1</font> |
| business_stat | 业务开通状态 | String | 1 | Y | S-成功，F-失败；当notify_type是W/A/E时返回；<font color="green">示例值：S</font> |
| business_desc | 业务开通描述 | String | 200 | N | 当notify_type是W/A/E时返回 |
| sub_mer_id | 二级商户号 | String | 32 | N | 微信/支付宝二级商户号；当notify_type是W/A时返回；<font color="green">示例值：A1035134718828858326</font> |
| bank_channel_no | 渠道号 | String | 50 | N | 当notify_type是W/A时返回；<font color="green">示例值：JP00001</font> |
| bank_mer_code | 真实商户号 | String | 20 | N | 当notify_type是W/A时返回；<font color="green">示例值：2088431912900000</font> |
| electron_bank_name | 电子账户开户行 | String | 32 | N | 全域资金管理电子账户开户行,  当notify_type是E时返回；<font color="green">示例值：武汉众邦银行股份有限公司</font>； |
| electron_account | 电子账号 | String | 32 | N | 全域资金管理电子账号,  当notify_type是E时返回；<font color="green">示例值：2088431912900000</font> |
| real_name_applyment_stat | 实名认证状态 | String | 64 | N | W:微信 A：支付宝 申请实名时返回<br>A：支付宝对应值<br>审核中(AUDITING)<br>待联系人确认(CONTACT_CONFIRM)<br>待法人确认(LEGAL_CONFIRM)<br>审核通过(AUDIT_PASS)<br>审核失败(AUDIT_REJECT)<br>已冻结(AUDIT_FREEZE)<br>已撤回(CANCELED)<br>未申请(NOT_APPLY)<br>W:微信对应值<br>APPLYMENT_STATE_EDITTING--【编辑中】--可能在提交申请时发生错误导致，可用同一个业务申请编号重新提交<br>APPLYMENT_STATE_WAITTING_FOR_AUDIT--【审核中】--请耐心等待1~2个工作日，微信支付将会完成审核<br>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT--【待确认联系信息】--请扫描微信支付返回的小程序码确认联系信息(此过程可修改超级管理员手机号)<br>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON--【待账户验证】--请扫描微信支付返回的小程序码在小程序端完成账户验证<br>APPLYMENT_STATE_PASSED--【审核通过】--请扫描微信支付返回的小程序码在小程序端完成授权流程<br>APPLYMENT_STATE_REJECTED--【审核驳回】--请按照驳回原因修改申请资料，并更换业务申请编码，重新提交申请<br>APPLYMENT_STATE_FREEZED--【已冻结】--可能是该主体已完成过入驻，请查看驳回原因，并通知驳回原因中指定的联系人扫描微信支付返回的小程序码在小程序端完成授权流程<br>APPLYMENT_STATE_CANCELED--【已作废】--表示申请单已被撤销，无需再对其进行操作<br>APPLYMENT_STATE_NOAPPLY--未申请<br/><font color="green">示例值：AUDITING</font> |
| real_name_applyment_desc | 实名认证描述 | String | 128 | N | W:微信 A：支付宝 申请实名时返回；<font color="green">示例值：W</font> |
| qrcode_data | 授权二维码 | String | 512 | N | W:微信 A：支付宝 申请实名时返回<br>若notify_type=W时  且 实名认证状态 real_name_applyment_stat=<br>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT、<br>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON、<br>APPLYMENT_STATE_PASSED、<br>APPLYMENT_STATE_FREEZED时返回<br>若notify_type=A时  且 实名认证状态 real_name_applyment_stat=<br>CONTACT_CONFIRM、LEGAL_CONFIRM时返回；<font color="green">示例值：https://qr.alipay.com/bax02911brluc2xieoph6001</font> |
| agreement_link | 协议签署连接 | String | 1024 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：</font> |
| agreement_id | 协议编号 | String | 64 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：</font> |
| agreement_name | 协议名称 | String | 256 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e72c6115_a2cb_4a80_8c48_6643ff19d93b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| confirm_url | 签约链接 | String | 256 | N | <font color="green">示例值：https://www.huifu.com</font> |
| mer_app_id | 应用ID | String | 32 | N | <font color="green">示例值：wx51aa91a575359ff5</font> |
| reject_reason | 拒绝原因 | String | 128 | N | <font color="green">示例值：支付功能未开通</font> |
| sub_mch_id | 支付宝/微信商户号 | String | 32 | N | <font color="green">示例值：1632157057</font> |
| apply_type | 申请类型 | String | 32 | N | <font color="green">示例值：FACE_TO_FACE</font> |
| apply_state | 申请单状态 | String | 1 | N | S：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；<br>新增状态枚举：C：待签约 |
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
| <span class="extend 01615a1c_73de_4be1_a34a_1f768375a1dc">agreement_info_list</span> | 协议信息 | String |  | N | 签署电子协议时返回 |

<!-- extend:start -->
<!-- div:extend-table 01615a1c_73de_4be1_a34a_1f768375a1dc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_type | 协议类型 | String | 1 | N | 0-电子协议 |
| agreement_link | 协议签署链接 | String | 512 | N |  |
| agreement_no | 协议号 | String | 32 | N | <font color="green">示例值：3245234</font> |
| agreement_name | 协议名称 | String | 128 | N |  |
| con_stat | 合同状态 | String | 2 | N | 电子协议类型会返回以下值： 2：创建合同异常 3：待签约 4：签约中 5：签约完成(电子协议只有签约完成才能做交易) 6：已失效 7：已拒签 8：签约失败 <font color="green">示例值：5</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{  
    "data":{  
        "apply_no":"2022042201091802",  
        "huifu_id":"6666000103668046",  
        "product_id":"ZDTEST",  
        "req_date":"20220422",  
        "req_seq_id":"2022042213314053740test001",  
        "resp_code":"00000000",  
        "resp_desc":"成功"  
    },  
    "sign":"W94y5imRC0YBKMkjDC6E7AD4AAzQwCRU9TsGiFDFmqSJqKoEnoHwMop67aZ++LsRMcBTay4JSnaRNdTbYuFcIfZV+6vXOjjw8D2tVg/VpBEEekobUWP0TFCpIV0+yc1sCkSRM/79iIRtkvQN9jYb9pDA9u1zEMzasqfwxf5a3Fs="  
}

```
