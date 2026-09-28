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
## 开通下级商户权限配置接口

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/busi/head/config

*最近更新时间：2026.09.09*
### 应用场景
服务商通过此接口可配置商户开通下级商户的权限和底价，支持配置支付宝、微信、抖音、银联二维码、POS刷卡、快捷支付、网银支付等支付业务对应功能权限及费率底价；

**适用对象**  
总部-下级商户体系结构内的商户需要开通下级商户时，可调用该功能。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sys_id     | 系统号   | String | 16       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，例MCS                                      |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数   

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求时间 | String | 8 | Y | 请求时间 yyyyMMdd；<font color="green">示例值：20220125</font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属商户ID；示例值：6666000108854952 |
| product_id | 产品编号 | String | 16 | Y | 汇付分配的产品号，示例值MCS |
| upper_huifu_id | 直属渠道号 | String | 18 | C | 该商户进件完成后归属的渠道商huifu_id；；<br/>sys_id主体为渠道商时填写； <br/>sys_id主体为总部商户时选填；<br/> 示例值：6666000123123123 |
| <span class="extend 74015a52_c594_4d51_96ac_781a85a3d7d2">ali_conf_list</span> | 支付宝配置对象 | String |  | N | jsonArray格式 |
| <span class="extend 3f0d9731_85b1_48a4_9df9_f4151f2d3b06">wx_conf_list</span> | 微信配置对象 | String |  | N | jsonArray格式 |
| <span class="extend 8f0e73a8_70a5_4d89_90ae_67a8fadbcb45">union_conf_list</span> | 银联二维码配置对象 | String |  | N | jsonArray格式 |
| <span class="extend ef2b8b7d_76ab_4421_8922_02d82b132e97">bank_card_config</span> | 银联卡配置对象 | String |  | N | jsonObject格式 |
| <span class="extend 3871b37f_02cc_4a39_9bfb_8626759acef7">split_config</span> | 分账配置对象 | String |  | N | jsonObject格式 |
| <span class="extend c2ecf201_1dd5_45d7_96fd_372b53368780">wx_zl_conf_list</span> | 微信直连配置对象 | String |  | N | jsonArray格式 |
| <span class="extend 1a28b0ab_2af8_47c2_b4e1_d83f73dad009">ali_zl_conf</span> | 支付宝直连配置对象 | String |  | N | jsonObject格式 |
| <span class="extend ea8f8331_c4fe_4d0d_a4de_d9b6d740d35f">online_fee_conf_list</span> | 线上配置对象 | String |  | N | jsonArray格式 |
| <span class="extend eef67449_6ad1_47aa_8fa9_8252064e50e6">balance_pay_config</span> | 余额支付配置对象 | String |  | N | jsonObject格式 |
| <span class="extend 6106eacb_569a_4c76_85ac_ab898536ab07">combine_pay_config</span> | 补贴支付配置对象 | String |  | N | jsonObject格式 |
| <span class="extend 0e5359b7_2ed9_4f46_8801_5f5dde76fc6d">bank_big_amt_pay_config</span> | 银行大额转账配置对象 | String |  | N | jsonObject格式 |
| <span class="extend 1d1a1f1d_5af5_4cd9_8885_76d059ad9a06">out_order_funds_config</span> | 全域资金管理配置对象（华通银行） | String |  | N | jsonObject格式 |
| <span class="extend e2ecdcdd_224a_4372_907b_507c6c454158">out_order_funds_new_net_config</span> | 全域资金管理配置(新网银行) | String |  | N | jsonObject格式 |
| <span class="extend 389f1758_740d_41d6_8e7c_14551cf02b7e">settle_config_list</span> | 结算配置对象 | String |  | N | jsonArray格式 |
| <span class="extend 8036306d_9d4b_469f_8a85_015c03d5ab5f">cash_config_list</span> | 取现配置对象 | String |  | N | jsonArray格式 |
| <span class="extend f1a9631c_3273_427d_9a6d_14c93fc43bca">out_fee_config</span> | 外扣配置对象 | String |  | N | jsonObject格式 内容参考：out_fee_config |
| alipay_pre_auth_flag | 允许开通支付宝预授权 | String | 1 | N | 支付宝预授权开通；Y：是，N：否； |
| wechatpay_pre_auth_flag | 允许开通微信预授权 | String | 1 | N | 微信预授权开通；Y：是，N：否； |
| mer_timing_settle_flag | 允许开通商户定时结算 | String | 1 | N | 定时结算开通；Y：是，N：否； |
| mer_prior_settle_flag | 允许开通商户优先结算 | String | 1 | N | 优先结算开通；Y：是，N：否； |
| use_upper_mer_auth_flag | 允许使用上级商户经营信息 | String | 1 | N | 开通下级商户时支持复用上级的经营信息；Y：是，N：否； |
| use_upper_mer_at_trans_flag | 允许使用上级商户号发起AT交易 | String | 1 | N | 开通下级商户时支持复用上级的微信、支付宝商户号信息；Y：是，N：否； |
| <span class="extend e0a8c8f7_cbbe_44cd_afe1_2700c79dfcac">large_amt_pay_config_list</span> | 大额支付配置 | String |  | N | jsonObject字符串 |
| <span class="extend f918ef20_437d_4af1_8f8a_da30f03f2ff0">out_order_funds_su_shang_config</span> | 全域资金管理配置(苏商) | String |  | N | jsonObject字符串 |
| half_pay_host_flag | 统一收银台开关 | String | 1 | N | Y:是 N:否（为空默认未开通） ；<font color="green">示例值：Y</font> |
| <span class="extend f5b7e753_920e_4fd1_8350_0679162989d4">out_order_funds_fee_list</span> | 全域资金费用配置对象 | String |  | N | jsonArray格式 |
| <span class="extend fe0ccc8c_7ab9_4357_97a8_b82e77a5bff2">lla_withhold_config</span> | 本地生活生活配置对象 | Object |  | N | jsonArray格式 |
| bill_payment_flag | 是否开通账单支付 | String | 1 | N | Y:是 N:否 ；<font color="green">示例值：Y</font> |
| <span class="extend 329728cf_1bfb_4616_b9b4_29459276bd4a">dy_conf_list</span> | 抖音配置对象 | Object |  | N | jsonArray字符串 |

<!-- extend:start -->
<!-- div:extend-table 74015a52_c594_4d51_96ac_781a85a3d7d2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1、线下扫码（正扫&反扫&台牌），2、线上扫码，示例值：1 |
| fee_rate | 手续费 | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通该业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
| fee_min_amt |  最低收取手续费（元） | String | 6 | N | 固定金额保留2位小数；大于0。<font color="green">示例值：0.38</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3f0d9731_85b1_48a4_9df9_f4151f2d3b06-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1：线下反扫<br>2：线下公众号<br>3：线下小程序<br>4：线上公众号<br>5：线上小程序<br>12：线上反扫<br/>13：APP支付<br/>示例值：1 |
| fee_rate | 手续费 | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通该场景业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
| fee_min_amt |  最低收取手续费（元） | String | 6 | N | 固定金额保留2位小数；大于0。<font color="green">示例值：0.38</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8f0e73a8_70a5_4d89_90ae_67a8fadbcb45-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| charge_cate_code | 银联业务手续费类型 | String | 2 | N | 03-标准类 小微商户仅有03 标准类 <br>04-线上费率（银联二维码线上）<br>默认03标志类 |
| debit_fee_rate_up | 借记卡手续费1000以上(%) | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| debit_fee_limit_up | 借记卡封顶1000以上（元） | String | 9 | N | 数字类型，大于0保留2位小数；示例值：20.00 |
| credit_fee_rate_up | 银联二维码业务贷记卡手续费1000以上(%) | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| debit_fee_rate_down | 借记卡手续费1000以下(%) | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| debit_fee_limit_down | 借记卡封顶1000以下（元） | String | 9 | N | 数字类型，大于0保留2位小数；示例值：20.00 |
| credit_fee_rate_down | 银联二维码业务贷记卡手续费1000以下(%) | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通银联二维码业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ef2b8b7d_76ab_4421_8922_02d82b132e97-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| debit_fee_rate | 借记卡手续费（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]； 示例值：0.60 |
| debit_fee_limit | 借记卡封顶值 | String | 9 | N | 数字类型，大于0保留2位小数； 示例值：20.00 |
| credit_fee_rate | 贷记卡手续费（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.90 |
| cloud_debit_fee_rate_up | 银联手机闪付借记卡手续费1000以上（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| cloud_debit_fee_limit_up | 银联手机闪付借记卡封顶1000以上（元） | String | 9 | N | 数字类型，大于0保留2位小数；示例值：20.00 |
| cloud_credit_fee_rate_up | 银联手机闪付贷记卡手续费1000以上（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| cloud_debit_fee_rate_down | 银联手机闪付借记卡手续费1000以下（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| cloud_debit_fee_limit_down | 银联手机闪付借记卡封顶1000以下（元） | String | 9 | N | 数字类型，大于0保留2位小数；示例值：20.00 |
| cloud_credit_fee_rate_down | 银联手机闪付贷记卡手续费1000以下（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通银行卡业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3871b37f_02cc_4a39_9bfb_8626759acef7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | N | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通分账业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c2ecf201_1dd5_45d7_96fd_372b53368780-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1、微信直连小程序<br>2、微信直连公众号<br>3、微信直连H5<br>示例值：1 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通微信直连业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1a28b0ab_2af8_47c2_b4e1_d83f73dad009-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通支付宝直连业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ea8f8331_c4fe_4d0d_a4de_d9b6d740d35f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bus_type | 业务类型 | String | 2 | Y | 1.网银支付，<br>2.快捷支付，<br>3.手机WAP支付,<br>4：B2B网银充值，<br>5：B2C网银充值<br>6：代扣支付;<br>示例值：1 |
| dc_flag | 借贷记标识 | String | 2 | Y | D:借记,C:贷记；B2B网银填写D；示例值：D |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| bank_code | 银行号 | String | 8 | Y | 8位银行号 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_flag | 允许开通线上支付业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
| fee_min_amt | 手续费最小值（元） | String | 6 | N | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| fee_formula_type | 代扣手续费计费模式 | String |  | N | bus_type为6：代扣支付时，才可传入；<br/>01: 百分比手续费，无封顶值或保底值<br/>02: 百分比手续费，有保底值<br/>03: 固定手续费<br/>04: 固定手续费+百分比手续费<br/>为空默认04 <font color="green">示例值：04</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table eef67449_6ad1_47aa_8fa9_8252064e50e6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通余额支付业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6106eacb_569a_4c76_85ac_ab898536ab07-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通补贴支付业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0e5359b7_2ed9_4f46_8801_5f5dde76fc6d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通大额转账业务 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1d1a1f1d_5af5_4cd9_8885_76d059ad9a06-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| open_fee_fix_amt | 开户手续费（元） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 保底手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通全域资金业务（华通） | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e2ecdcdd_224a_4372_907b_507c6c454158-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_min_amt | 保底手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| public_fee_fix_amt | 对公固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| private_fee_fix_amt | 对私固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通全域资金业务(新网) | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 389f1758_740d_41d6_8e7c_14551cf02b7e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bus_type | 业务类型 | String | 2 | Y | D1：下个自然日到账，<br>T1：下个工作日到账；<br>TS：笔笔到账<br>示例值：T1 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通结算配置 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8036306d_9d4b_469f_8a85_015c03d5ab5f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bus_type | 业务类型 | String | 2 | Y | D0：当日到账；当日交易资金当天可取现到账；<br>T1：下个工作日到账;<br>D1：下个自然日到账;<br>DM：当日到账；到账资金不包括当天的交易资金；<br>示例值：T1 |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| open_flag | 允许开通取现配置 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f1a9631c_3273_427d_9a6d_14c93fc43bca-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_out_fee_flag | 支持结算手续费外扣 | String | 1 | Y | Y：是，N：否，示例值：Y |
| trans_fee_out_flag | 支持交易手续费外扣 | String | 1 | Y | Y：是，N：否，示例值：Y |
| cash_out_fee_flag | 支持取现手续费外扣 | String | 1 | Y | Y：是，N：否，示例值：Y |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e0a8c8f7_cbbe_44cd_afe1_2700c79dfcac-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 6 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| fee_fix_amt | 固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ，最低传入0.00 |
| open_flag | 允许开通大额转账业务 | String | 1 | Y | Y：是，N：否，<font color="green">示例值：Y</font> |
| allow_user_deposit_flag | 允许用户入账 | String | 1 | N | Y：是，N：否，<font color="green">示例值：Y</font> ，默认为N |
| mer_same_card_recharge_flag | 银行卡绑定支付权限 | String | 1 | N | Y：是，N：否，<font color="green">示例值：Y</font> ，默认为N |
| business_model | 大额支付业务模式 | String | 15 | Y | 大额支付业务模式 bank：银行模式 provisions：备付金模式，<font color="green">示例值：provisions</font> |
| provisions_auto_refund_flag | 备付金固定账号模式自动退款 | String | 1 | N | Y-开通/N-关闭，默认为N ；<font color="green">示例值：Y</font>；该配置仅在开通大额支付备付金绑卡模式时生效 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f918ef20_437d_4af1_8f8a_da30f03f2ff0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| fee_min_amt | 保底手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| public_fee_fix_amt | 对公固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| private_fee_fix_amt | 对私固定手续费(元) | String | 9 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00 |
| open_flag | 允许开通全域资金业务(苏商) | String | 1 | Y | Y：是，N：否，<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f5b7e753_920e_4fd1_8350_0679162989d4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bus_type | 业务类型 | String | 2 | Y | 01：付款手续费，<br>02：取现手续费；<br><font color="green">示例值：01</font> |
| fee_rate | 手续费（百分比/%） | String | 6 | Y | 手续费（百分比/%），保留小数点后两位；取值范围[0.00,100.00] ；<font color="green">示例值：0.05</font> |
| fee_fix_amt | 手续费（固定/元） | String | 9 | Y | 手续费（固定/元），保留小数点后两位；<font color="green">示例值：1.00</font> |
| open_flag | 是否允许开通 | String | 1 | Y | Y：是，N：否；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fe0ccc8c_7ab9_4357_97a8_b82e77a5bff2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| llaWithholdFlag | 本地生活开关 | String |  | Y | Y:是 N:否（为空默认未开通） ；<font color="green">示例值：Y</font> |
| fee_rate | 佣金收取手续费率 | String |  | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 329728cf_1bfb_4616_b9b4_29459276bd4a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| mer_industry_category | 抖音商户行业分类 | String |  | Y | 目前仅支持C，适用于7999-其他娱乐服务、5541-加油加气充电站、5811-包办伙食，宴会承包商、 5812-就餐场所和餐馆、  5813-休闲饮品场所、酒吧、咖啡厅、茶馆 |
| fee_model | 手续费模式 | String |  | Y | 01-百分比 02-百分比+最低手续费 |
| fee_rate | 手续费（%） | String |  | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| fee_min_amt | 最低收取手续费（元） | String |  | N | 固定金额保留2位小数；大于0。需要渠道商开通此功能。<font color="green">示例值：0.38</font> |
| open_flag | 是否允许开通 | String |  | N | Y：是，N：否；<font color="green">示例值：Y</font> |
<!-- extend:end -->


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


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String |  | N | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务返回描述 | String |  | N | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| product_id | 产品号 | String |  | N | 汇付分配的产品号，<font color="green">示例值：MCS</font> |
| req_date | 请求时间 | String | 32 | Y | 请求时间 |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号 |
| huifu_id | 商户汇付Id | String | 18 | Y | 商户汇付Id；<font color="green">示例值：6666000123123123</font> |
| apply_no | 申请单 | String | 128 | Y | 申请单 |


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
