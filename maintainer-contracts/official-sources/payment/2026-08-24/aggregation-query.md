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
## 交易订单查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v4/trade/payment/scanpay/query

*最近更新时间：2026.05.28*
## 接口说明

服务商/商户系统因网络原因未收到交易状态，可以通过本接口主动查询订单状态。支持微信公众号-T_JSAPI、小程序-T_MINIAPP、微信APP支付-T_APP、支付宝JS-A_JSAPI、支付宝正扫-A_NATIVE、银联二维码正扫-U_NATIVE、银联二维码JS-U_JSAP，以及微信反扫、支付宝反扫、银联二维码反扫交易查询。


## 公共参数

* 公共请求参数

| **参数**   | **中文名** | **定义** | **长度** | **必填** | **说明**                                                     |
| :--------- | :--------- | :------- | :------- | :------- | :----------------------------------------------------------- |
| sys_id     | 系统号     | String   | 32       | Y        | 渠道商/代理商/商户的huifu_id <br />（1）当主体为渠道商/代理商时，此字段填写渠道商/代理商huifu_id； <br />（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font>  |
| product_id | 产品号     | String   | 32       | Y        |汇付分配的产品号，<font color="green">示例值：MCS</font>    |
| sign       | 加签结果   | String   | 512      | Y        | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)  |
| data       | 请求数据   | JSON     |          | Y        | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| **参数** | **中文名** | **定义** | **长度** | **必填** | **说明**             |
| :------- | :--------- | :------- | :------- | :------- | :------------------- |
| sign     | 签名       | String   | 512      | Y        | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数  

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 汇付商户号 | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| req_date | 请求日期 | String | 8 | C | 日期格式：yyyyMMdd，以北京时间为准； |
| out_ord_id | 汇付服务订单号 | String | 32 | C | out_ord_id,hf_seq_id,req_seq_id 必填其一；汇付生成的服务订单号；<br/><font color="green">示例值：1234323JKHDFE1243252</font> |
| hf_seq_id | 创建服务订单返回的汇付全局流水号 | String | 128 | C | out_ord_id,hf_seq_id,req_seq_id 必填其一；<br/><font color="green">示例值：00290TOP1GR210919004230P853ac13262200000</font> |
| req_seq_id | 服务订单创建请求流水号 | String | 128 | C | out_ord_id,hf_seq_id,req_seq_id 必填其一；<br/><font color="green">示例值：202110210012100005</font> |


#### 请求示例

```json
{
  "sys_id": "6666000003100616",
  "product_id": "MYPAY",
  "data": {
    "hf_seq_id": "0029000topA250804164235P330c0a8200900000",
    "huifu_id": "6666000003100616"
  },
  "sign": "VvcUT0WQLfkYsg0dns2qR7yFs/1Z/eejZBOUSnhzCA0SqI97Gekq3yl3sriSr9eeSChFqPnFlqNKOol+dfPy8V3X3BrzKbYcSIvmJgn1fQlDrwFivf2/fW2XoHA5O6YQcOymfRtG8wIdt/tSBNrlbIkI92kTu8p8TXkvZGUh796zOtJO900DsQAcVc0xcjNiFTX8jPDP61SsUJQ3xNbSwFd6dgIAHnlGA=="
}

```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | 参见[业务返回码](#业务返回码) |
| resp_desc | 业务响应信息 | String | 512 | Y | 参见[业务返回码](#业务返回码) |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准； |
| hf_seq_id | 交易返回的全局流水号 | String | 128 | N | 斗拱返回的全局流水号；<font color="green">示例值：00290TOP1GR210919004230P853ac13262200000</font> |
| req_seq_id | 请求流水号 | String | 128 | N | 请求流水号，同一商户号当天唯一； |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | <font color="green">示例值：092021091922001451301445517582</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | <font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| settlement_amt | 结算金额 | String | 14 | N | 单位元；<font color="green">示例值：1000.00</font> |
| unconfirm_amt | 待确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| trade_type | 交易类型 | String | 16 | N | T_JSAPI:  微信JS支付<br/>
T_MINIAPP:  微信小程序支付<br/>
T_MICROPAY：微信付款码支付<br/>
A_JSAPI:  支付宝JS支付  <br/>
A_NATIVE:  支付宝正扫  <br/>
A_NATIVE:  支付宝付款码  <br/>
U_JSAPI:  银联JS支付  <br/>
U_NATIVE: 银联正扫支付 <br/>
U_MICROPAY: 银联付款码  <br/>
<font color="green">示例值：T_JSAPI</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中；S：成功；F：失败；I: 初始（初始状态很罕见，请联系汇付技术人员处理）；交易状态以此字段为准。<br/><font color="green">示例值：S</font> |
| end_time | 支付完成时间 | String | 14 | N | 格式yyyyMMddHHMMSS，如2009年12月25日9点10分10秒，<font color="green">示例值：20091225091010</font> |
| delay_acct_flag | 是否延时交易 | String | 1 | Y | Y：延迟， N：不延迟；<font color="green">示例值：Y</font> |
| acct_id | 账户号 | String | 9 | N | 商户账户号；<font color="green">示例值：F00598600</font> |
| acct_date | 账务日期 | String | 8 | N | 格式：yyyyMMdd；<font color="green">示例值：20221010</font> |
| acct_stat | 账务状态 | String | 1 | N | "I：初始"; "P:处理中"; "S:成功"; "F:失败。<font color="green">示例值：S</font><br/> 返回“I：初始”状态时，请联系客服确认订单问题 |
| debit_type | 借贷记标识 | String | 1 | N | D：借记卡，C：信用卡，Z：借贷合一卡，O：其他；<font color="green">示例值：D</font> |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | <font color="green">示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk=</font> |
| div_flag | 是否分账交易 | String | 1 | Y | Y：分账交易，N：非分账交易；<font color="green">示例值：Y</font> |
| <span class="showCompleteParams">combinedpay_fee_amt</span> | 补贴部分的手续费 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| remark | 备注 | String | 255 | N | 原样返回；<font color="green">示例值：备注</font> |
| device_type | 终端类型 | String | 2 | N | 01-智能POS<br>02-扫码POS<br>03-云音箱<br>04-台牌<br>05-云打印<br>06-扫脸设备<br>07-收银机<br>08-收银助手<br>09-传统POS<br>10-一体音箱<br>11-虚拟终端<br/><font color="green">示例值：01</font> |
| bank_message | 外部通道返回描述 | String | 200 | N | <font color="green">示例值：TRADE_SUCCESS</font> |
| atu_sub_mer_id | ATU真实商户号 | String | 32 | N | <font color="green">示例值：411111141</font> |
| freeze_time | 冻结时间 | String | 14 | Y | 格式为yyyyMMddHHMMSS，<font color="green">示例值：20091225091010</font> |
| unfreeze_amt | 解冻金额 | String | 14 | Y | 单元：元。<font color="green">示例值：1.23</font> |
| unfreeze_time | 解冻时间 | String | 14 | Y | 格式为yyyyMMddHHMMSS，<font color="green">示例值：20091225091010</font> |
| fund_freeze_stat | 资金冻结状态 | String | 16 | N | FREEZE：冻结；UNFREEZE：解冻；<font color="green">示例值：UNFREEZE</font> |
| <span class="extend d73067f5_2bab_4de4_b602_891f31d56765">method_expand</span> | 交易类型扩展参数 | String |  | N | jsonObject字符串 |
| <span class="extend 3f209cd8_41fd_4155_ba32_015c33948bd2">tx_metadata</span> | 扩展参数集合 | String |  | N | jsonObject字符串 |
| <span class="extend 5c7d0700_dc97_47c0_84be_f79430e028cc">payment_fee</span> | 手续费对象	 | String |  | N | jsonObject字符串 |

<!-- extend:start -->
<!-- div:extend-table d73067f5_2bab_4de4_b602_891f31d56765-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 554b2402_abab_4ff4_8238_7b955e4c113b">T_JSAPI</span> | 微信公众号支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend 50831545_c126_4800_b38a_95874af89fa0">T_MINIAPP</span> | 微信小程序支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend 1eadebda_0c14_4ce6_9e14_1a3455610501">T_APP</span> | 微信APP支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend 53de3548_c995_4c9f_a66e_78c0146063eb">T_MICROPAY</span> | 微信反扫支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend 280c7ae3_a4bc_44dd_88c2_9cb23843db8a">A_JSAPI</span> | 支付宝JS支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend b091b023_d98a_4054_8503_a7e6d84ad57a">A_NATIVE</span> | 支付宝正扫支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend 4530a8b7_faf6_4663_a808_c6202c36bdd7">A_MICROPAY</span> | 支付宝反扫支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend e071d780_9a84_4e0f_829a_8e2b1275f618">U_JSAPI</span> | 银联JS支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend 7c7d7b90_1cba_4ce3_bd1b_d47b2a1a1711">U_NATIVE</span> | 银联正扫支付参数 | String |  | N | jsonObject字符串 |
| <span class="extend 9df68175_70ad_497b_9a64_09090fc9a0da">U_MICROPAY</span> | 银联反扫支付参数 | String |  | N | jsonObject字符串 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 554b2402_abab_4ff4_8238_7b955e4c113b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_openid | 子商户公众账号ID | String | 16 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| openid | 用户标识 | String | 128 | N | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| cash_fee | 现金支付金额 | String | 14 | N | 现金支付金额订单现金支付金额；单位格式为0.00；<font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| coupon_fee | 代金券金额 | String | 14 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| <span class="extend 402e0380_5811_4c7d_bc53_d2955e5c4fdd">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 营销详情列表，使返回值为Json格式； |
| bank_type | 付款银行 | String | 16 | N | 银行类型，采用字符串类型的银行标识；参见[微信银行类型说明](https://pay.weixin.qq.com/wiki/doc/api/micropay_sl.php?chapter=4_2)；<font color="green">示例值：CMB</font> |
| sub_appid | 商户公众号APPID | String | 32 | N | 直连交易字段；<font color="green">示例值：wx5934540532</font> |
| device_info | 交易终端设备信息 | String | 32 | N | 直连交易字段；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 402e0380_5811_4c7d_bc53_d2955e5c4fdd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| activity_id | 活动id | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| promotion_id | 券或者立减优惠id | String | 32 | Y | <font color="green">示例值：2345234235</font> |
| <span class="extend 4cebc51b_c9e0_4552_9b8b_305bede9c341">goods_detail</span> | 单品列表 | Array | 3000 | N | 单品信息，Json格式 |
| merchant_contribute | 商户出资(元) | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；<font color="green">示例值：1000</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| other_contribute | 其他出资(元) | String | 32 | N | 其他出资方出资金额；<font color="green">示例值：2000</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL- 全场代金券，SINGLE- 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4cebc51b_c9e0_4552_9b8b_305bede9c341-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，**单位为：元**；<font color="green">示例值：20.00</font> |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| price | 商品价格 | String | 32 | Y | **单位为：元**。<font color="green">示例值：50.00</font><br/>如果商户有优惠，需传输商户优惠后的单价。<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| goods_remark | 商品备注 | String | 32 | N | 按照配置原样返回，字段内容在微信后台配置券时进行设置。<font color="green">示例值：商品备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 50831545_c126_4800_b38a_95874af89fa0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_openid | 子商户公众账号ID | String | 16 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| openid | 用户标识 | String | 128 | N | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| cash_fee | 现金支付金额 | String | 14 | N | 现金支付金额订单现金支付金额；单位格式为0.00；<font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| coupon_fee | 代金券金额 | String | 14 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| <span class="extend c3051319_41c3_46d0_bce8_de5e4367b7d5">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 营销详情列表，使返回值为Json格式； |
| bank_type | 付款银行 | String | 16 | N | 银行类型，采用字符串类型的银行标识；参见[微信银行类型说明](https://pay.weixin.qq.com/wiki/doc/api/micropay_sl.php?chapter=4_2)；<font color="green">示例值：CMB</font> |
| sub_appid | 商户公众号APPID | String | 32 | N | 直连交易字段；<font color="green">示例值：wx5934540532</font> |
| device_info | 交易终端设备信息 | String | 32 | N | 直连交易字段；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c3051319_41c3_46d0_bce8_de5e4367b7d5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| activity_id | 活动id | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| promotion_id | 券或者立减优惠id | String | 32 | Y | <font color="green">示例值：2345234235</font> |
| <span class="extend 31b83b20_80e9_4661_b794_6aed13009c60">goods_detail</span> | 单品列表 | Array | 3000 | N | 单品信息，Json格式 |
| merchant_contribute | 商户出资(元) | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；<font color="green">示例值：1000</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| other_contribute | 其他出资(元) | String | 32 | N | 其他出资方出资金额；<font color="green">示例值：2000</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL- 全场代金券，SINGLE- 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 31b83b20_80e9_4661_b794_6aed13009c60-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，**单位为：元**；<font color="green">示例值：20.00</font> |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| price | 商品价格 | String | 32 | Y | **单位为：元**。<font color="green">示例值：50.00</font><br/>如果商户有优惠，需传输商户优惠后的单价。<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| goods_remark | 商品备注 | String | 32 | N | 按照配置原样返回，字段内容在微信后台配置券时进行设置。<font color="green">示例值：商品备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1eadebda_0c14_4ce6_9e14_1a3455610501-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_openid | 子商户公众账号ID | String | 16 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| openid | 用户标识 | String | 128 | N | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| cash_fee | 现金支付金额 | String | 14 | N | 现金支付金额订单现金支付金额；单位格式为0.00；<font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| coupon_fee | 代金券金额 | String | 14 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| <span class="extend bba4eb1e_0913_465a_b849_42afc4bf2962">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 营销详情列表，使返回值为Json格式； |
| bank_type | 付款银行 | String | 16 | N | 银行类型，采用字符串类型的银行标识；参见[微信银行类型说明](https://pay.weixin.qq.com/wiki/doc/api/micropay_sl.php?chapter=4_2)；<font color="green">示例值：CMB</font> |
| sub_appid | 商户公众号APPID | String | 32 | N | 直连交易字段；<font color="green">示例值：wx5934540532</font> |
| device_info | 交易终端设备信息 | String | 32 | N | 直连交易字段；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bba4eb1e_0913_465a_b849_42afc4bf2962-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| activity_id | 活动id | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| promotion_id | 券或者立减优惠id | String | 32 | Y | <font color="green">示例值：2345234235</font> |
| <span class="extend aa0fe992_3236_4290_ac8a_28be2cbd496d">goods_detail</span> | 单品列表 | Array | 3000 | N | 单品信息，Json格式 |
| merchant_contribute | 商户出资(元) | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；<font color="green">示例值：1000</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| other_contribute | 其他出资(元) | String | 32 | N | 其他出资方出资金额；<font color="green">示例值：2000</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL- 全场代金券，SINGLE- 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table aa0fe992_3236_4290_ac8a_28be2cbd496d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，**单位为：元**；<font color="green">示例值：20.00</font> |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| price | 商品价格 | String | 32 | Y | **单位为：元**。<font color="green">示例值：50.00</font><br/>如果商户有优惠，需传输商户优惠后的单价。<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| goods_remark | 商品备注 | String | 32 | N | 按照配置原样返回，字段内容在微信后台配置券时进行设置。<font color="green">示例值：商品备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 53de3548_c995_4c9f_a66e_78c0146063eb-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_openid | 子商户公众账号ID | String | 16 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| openid | 用户标识 | String | 128 | N | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| cash_fee | 现金支付金额 | String | 14 | N | 现金支付金额订单现金支付金额；单位格式为0.00；<font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| coupon_fee | 代金券金额 | String | 14 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| <span class="extend ef67b657_765f_4583_83b5_e7b6f4639491">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 营销详情列表，使返回值为Json格式； |
| bank_type | 付款银行 | String | 16 | N | 银行类型，采用字符串类型的银行标识；参见[微信银行类型说明](https://pay.weixin.qq.com/wiki/doc/api/micropay_sl.php?chapter=4_2)；<font color="green">示例值：CMB</font> |
| sub_appid | 商户公众号APPID | String | 32 | N | 直连交易字段；<font color="green">示例值：wx5934540532</font> |
| device_info | 交易终端设备信息 | String | 32 | N | 直连交易字段；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ef67b657_765f_4583_83b5_e7b6f4639491-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| activity_id | 活动id | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| promotion_id | 券或者立减优惠id | String | 32 | Y | <font color="green">示例值：2345234235</font> |
| <span class="extend a4458d18_6006_4c66_95aa_bf7484e031d2">goods_detail</span> | 单品列表 | Array | 3000 | N | 单品信息，Json格式 |
| merchant_contribute | 商户出资(元) | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；<font color="green">示例值：1000</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| other_contribute | 其他出资(元) | String | 32 | N | 其他出资方出资金额；<font color="green">示例值：2000</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL- 全场代金券，SINGLE- 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a4458d18_6006_4c66_95aa_bf7484e031d2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，**单位为：元**；<font color="green">示例值：20.00</font> |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| price | 商品价格 | String | 32 | Y | **单位为：元**。<font color="green">示例值：50.00</font><br/>如果商户有优惠，需传输商户优惠后的单价。<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| goods_remark | 商品备注 | String | 32 | N | 按照配置原样返回，字段内容在微信后台配置券时进行设置。<font color="green">示例值：商品备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 280c7ae3_a4bc_44dd_88c2_9cb23843db8a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| buyer_id | 买家支付宝用户号 | String | 28 | N | 买家的支付宝唯一用户号（2088开头的16位纯数字）<br/><font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| <span class="extend 7f9e4145_a8a8_441b_a175_648444fa3292">fund_bill_list</span> | 交易支付使用的资金渠道 | Array | 2048 | N | 支付成功的各个渠道金额信息，详见资金明细信息说明 |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| <span class="extend 13a4a861_85ca_4655_9600_62b9d1372438">voucher_detail_list</span> | 本交易支付时使用的所有优惠券信息 | Array | 2048 | N | 本交易支付时使用的所有优惠券信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7f9e4145_a8a8_441b_a175_648444fa3292-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | <font color="green">示例值：CEB</font>，请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| amount | 该支付工具类型所使用的金额 | String | 32 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
| fund_channel | 交易使用的资金渠道 | String | 32 | N | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；<font color="green">示例值：ALIPAYACCOUNT</font> |
| fund_type | 渠道所使用的资金类型 | String | 32 | N | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。<br/>DEBIT_CARD:借记卡，CREDIT_CARD:信用卡，MIXED_CARD:借贷合一卡<br/><font color="green">示例值：DEBIT_CARD</font> |
| real_amount | 渠道实际付款金额 | String | 11 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 13a4a861_85ca_4655_9600_62b9d1372438-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| amount | 优惠券面额（元） | String | 32 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| id | 券id | String | 32 | Y | 优惠券号；<font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | 优惠名称；<font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）<br/>DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；<br/><font color="green">示例值：DISCOUNT</font> |
| merchant_contribute | 商家出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元。<!--分--><font color="green">示例值：0.10</font> |
| other_contribute | 其他出资方出资金额 | String | 14 | N | 其他出资方出资金额，单位为元。<!--分--><font color="green">示例值：0.20</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b091b023_d98a_4054_8503_a7e6d84ad57a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| buyer_id | 买家支付宝用户号 | String | 28 | N | 买家的支付宝唯一用户号（2088开头的16位纯数字）<br/><font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| <span class="extend 95b90a5e_dcd5_421f_be1c_acb3e5978426">fund_bill_list</span> | 交易支付使用的资金渠道 | Array | 2048 | N | 支付成功的各个渠道金额信息，详见资金明细信息说明 |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| <span class="extend aebaede1_a9b3_4944_b699_e9acbe0ed102">voucher_detail_list</span> | 本交易支付时使用的所有优惠券信息 | Array | 2048 | N | 本交易支付时使用的所有优惠券信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 95b90a5e_dcd5_421f_be1c_acb3e5978426-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | <font color="green">示例值：CEB</font>，请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| amount | 该支付工具类型所使用的金额 | String | 32 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
| fund_channel | 交易使用的资金渠道 | String | 32 | N | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；<font color="green">示例值：ALIPAYACCOUNT</font> |
| fund_type | 渠道所使用的资金类型 | String | 32 | N | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。<br/>DEBIT_CARD:借记卡，CREDIT_CARD:信用卡，MIXED_CARD:借贷合一卡<br/><font color="green">示例值：DEBIT_CARD</font> |
| real_amount | 渠道实际付款金额 | String | 11 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table aebaede1_a9b3_4944_b699_e9acbe0ed102-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| amount | 优惠券面额（元） | String | 32 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| id | 券id | String | 32 | Y | 优惠券号；<font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | 优惠名称；<font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）<br/>DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；<br/><font color="green">示例值：DISCOUNT</font> |
| merchant_contribute | 商家出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元。<!--分--><font color="green">示例值：0.10</font> |
| other_contribute | 其他出资方出资金额 | String | 14 | N | 其他出资方出资金额，单位为元。<!--分--><font color="green">示例值：0.20</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4530a8b7_faf6_4663_a808_c6202c36bdd7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| buyer_id | 买家支付宝用户号 | String | 28 | N | 买家的支付宝唯一用户号（2088开头的16位纯数字）<br/><font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| <span class="extend 2790db6f_a666_491e_907d_5b71d46b3141">fund_bill_list</span> | 交易支付使用的资金渠道 | Array | 2048 | N | 支付成功的各个渠道金额信息，详见资金明细信息说明 |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| <span class="extend 4c6640d6_02f6_4b7a_a505_79945bc7c772">voucher_detail_list</span> | 本交易支付时使用的所有优惠券信息 | Array | 2048 | N | 本交易支付时使用的所有优惠券信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2790db6f_a666_491e_907d_5b71d46b3141-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | <font color="green">示例值：CEB</font>，请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| amount | 该支付工具类型所使用的金额 | String | 32 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
| fund_channel | 交易使用的资金渠道 | String | 32 | N | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；<font color="green">示例值：ALIPAYACCOUNT</font> |
| fund_type | 渠道所使用的资金类型 | String | 32 | N | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。<br/>DEBIT_CARD:借记卡，CREDIT_CARD:信用卡，MIXED_CARD:借贷合一卡<br/><font color="green">示例值：DEBIT_CARD</font> |
| real_amount | 渠道实际付款金额 | String | 11 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4c6640d6_02f6_4b7a_a505_79945bc7c772-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| amount | 优惠券面额（元） | String | 32 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| id | 券id | String | 32 | Y | 优惠券号；<font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | 优惠名称；<font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）<br/>DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；<br/><font color="green">示例值：DISCOUNT</font> |
| merchant_contribute | 商家出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元。<!--分--><font color="green">示例值：0.10</font> |
| other_contribute | 其他出资方出资金额 | String | 14 | N | 其他出资方出资金额，单位为元。<!--分--><font color="green">示例值：0.20</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e071d780_9a84_4e0f_829a_8e2b1275f618-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend f355bf62_41b9_448d_879b_9377bf7d37a6">coupon_info</span> | 银联优惠信息 | Array |  | N | 银联使用优惠活动时出现，jsonArray格式 |
| acc_no | 付款账号 | String | 40 | N | 付款方的卡号/账号/Token |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f355bf62_41b9_448d_879b_9377bf7d37a6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 项目类型 | String | 4 | Y | DD01：随机立减<br>CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券<br>CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券<br><font color="green">示例值：DD01</font>  |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font> |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7c7d7b90_1cba_4ce3_bd1b_d47b2a1a1711-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend e5779e36_0b48_460c_bc0d_93b6201fd0e2">coupon_info</span> | 银联优惠信息 | Array |  | N | 银联使用优惠活动时出现，jsonArray格式 |
| acc_no | 付款账号 | String | 40 | N | 付款方的卡号/账号/Token |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e5779e36_0b48_460c_bc0d_93b6201fd0e2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 项目类型 | String | 4 | Y | DD01：随机立减<br>CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券<br>CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券<br><font color="green">示例值：DD01</font>  |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font> |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9df68175_70ad_497b_9a64_09090fc9a0da-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend e4932b29_2c0a_4838_be76_6566d4d0ff26">coupon_info</span> | 银联优惠信息 | Array |  | N | 银联使用优惠活动时出现，jsonArray格式 |
| acc_no | 付款账号 | String | 40 | N | 付款方的卡号/账号/Token |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e4932b29_2c0a_4838_be76_6566d4d0ff26-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 项目类型 | String | 4 | Y | DD01：随机立减<br>CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券<br>CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券<br><font color="green">示例值：DD01</font>  |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font> |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3f209cd8_41fd_4155_ba32_015c33948bd2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 78f1f2d0_674b_46af_9aad_3c079a605acf">acct_split_bunch</span> | 分账对象 | String | 4000 | N | 分账对象，jsonObject字符串 |
| <span class="extend dedfd11c_825e_4975_854d_b2934a31f379">combinedpay_data</span> | 补贴支付信息 | String |  | N | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| <span class="extend b6b6f5ad_cd66_4d7d_91f3_80b5c37afc28">combinedpay_data_fee_info</span> | 补贴支付手续费信息 | String |  | N | jsonObject字符串 |
| <span class="extend f82baf98_909d_4678_9031_b08f19b8b69e">trans_fee_allowance_info</span> | 手续费补贴信息 | String |  | N | 返回值为Json格式 |
| <span class="extend 135d2149_4110_4b45_b4be_57b40bdd2cf5">terminal_device_data</span> | 设备信息 | String |  | N | 设备信息，jsonObject字符串； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 78f1f2d0_674b_46af_9aad_3c079a605acf-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 32df2018_fb2e_4b70_8369_36dc8f234c2d">acct_infos</span> | 分账明细 | Array | 4000 | Y | 分账明细 |
| is_clean_split | 是否净值分账 | String | 1 | N | Y:使用净值分账，仅在percentage_flag=Y时起作用；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 32df2018_fb2e_4b70_8369_36dc8f234c2d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 描述:单位元；<font color="green">示例值：0.20</font> |
| huifu_id | 分账接收方ID | String | 32 | Y | <font color="green">示例值：6666000123120001</font> |
| acct_id | 分账接收方子账户 | String | 9 | N | <font color="green">示例值：F00598600</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table dedfd11c_825e_4975_854d_b2934a31f379-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴方汇付商户号 | String | 32 | Y | 补贴方汇付ID；<font color="green">示例值：6666000123123123</font> |
| user_type | 补贴方类型 | String | 32 | Y | 补贴方类型：channel-渠道，agent-代理；<font color="green">示例值：agent</font> |
| acct_id | 补贴方账户号 | String | 32 | Y | 营销补贴方账户号；<font color="green">示例值：F00900982</font> |
| amount | 补贴金额 | String | 14 | Y | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b6b6f5ad_cd66_4d7d_91f3_80b5c37afc28-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴支付手续费承担方汇付编号 | String | 32 | Y | 补贴支付手续费承担方汇付编号；<font color="green">示例值：6666000123123123</font> |
| acct_id | 补贴支付手续费承担方账户号 | String | 32 | Y | 补贴支付手续费承担方账户号；<font color="green">示例值：F00900982</font> |
| combinedpay_fee_amt | 补贴支付手续费金额 | String | 14 | Y | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f82baf98_909d_4678_9031_b08f19b8b69e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| actual_fee_amt | 商户实收手续费 | String | 14 | Y | <font color="green">示例值：0.10</font> |
| allowance_fee_amt | 补贴手续费 | String | 14 | Y | <font color="green">示例值：0.20</font> |
| allowance_type | 补贴类型 | String | 1 | Y | 0：不补贴，为空默认<br/>1：补贴<br/>2：部分补贴<br/>3：全额补贴(优惠后)<br/>4：部分补贴(优惠后)<br/><font color="green">示例值：2</font> |
| <span class="extend 44f12c8b_4bb9_4d1e_99fe_c4f647b7cc34">cur_allowance_config_infos</span> | 手续费补贴活动详情 | Object |  | N | Json格式，见下文描述 |
| no_allowance_desc | 不补贴原因 | String | 128 | Y | 1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴<br/>2:额度用完<br/>3:不在有效期<br/>4:活动不存在<br/>5:手续费金额为0不补贴<br/>6:顶格优惠<br/>7:额度不足<br/>8:手续费后补<br/>9:未达到起始补贴金额<br/><font color="green">示例值：2</font> |
| receivable_fee_amt | 商户应收手续费 | String | 14 | Y | <font color="green">示例值：4.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 44f12c8b_4bb9_4d1e_99fe_c4f647b7cc34-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| merchant_group | 商户号 | String | 64 | N | <font color="green">示例值：6666000123120000</font> |
| acct_id | 门店 | String | 64 | N | <font color="green">示例值：sh002</font> |
| activity_id | 活动号 | String | 64 | Y | <font color="green">示例值：223402342</font> |
| activity_name | 活动描述 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| status | 活动是否有效 | String | 4 | Y | 1:生效 0：失效；<font color="green">示例值：1</font> |
| total_limit_amt | 活动总补贴额度 | String | 16 | Y | <font color="green">示例值：10.00</font> |
| start_time | 活动开始时间 | String | 8 | Y | yyyyMMdd；<font color="green">示例值：20220909</font> |
| end_time | 活动结束时间 | String | 8 | Y | yyyyMMdd；<font color="green">示例值：202209011</font> |
| human_flag | 是否人工操作 | String | 4 | Y | N：自动 Y：人工；<font color="green">示例值：N</font> |
| allowance_sys | 补贴方 | String | 64 | Y | 1:银行  2:服务商 3:汇来米；<font color="green">示例值：1</font> |
| allowance_sys_id | 补贴方ID | String | 64 | Y | 对应补贴方的id；<font color="green">示例值：6666000123120000</font> |
| is_delay_allowance | 补贴类型 | String | 2 | Y | 1:实补,2:后补,默认实补；<font color="green">示例值：1</font> |
| is_share | 是不是共享额度 | String | 4 | N | <font color="green">示例值：</font> |
| market_id | 自定义活动编号 | String | 64 | Y | <font color="green">示例值：ISFE00232</font> |
| market_name | 自定义活动名称 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| market_desc | 自定义活动描述 | String | 64 | N | <font color="green">示例值：新店开业大促</font> |
| pos_credit_limit_amt | pos贷记卡补贴额度 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| pos_debit_limit_amt | pos借记卡补贴额度 | String | 16 | Y | <font color="green">示例值：2.00</font> |
| pos_limit_amt | pos补贴额度 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| qr_limit_amt | 扫码补贴额度 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| create_by | 创建人 | String | 32 | Y | <font color="green">示例值：Lg2022022201394910571</font> |
| create_time | 创建时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 22:00:30</font> |
| update_time | 更新时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 23:00:30</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 135d2149_4110_4b45_b4be_57b40bdd2cf5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| terminal_ip | 交易设备IP | String | 64 | N | 绑卡设备（付款 APP） 所在的公网IP，可用于定位所属地区，不是 wifi 连接时的局域网 IP。局域网 IP 包括：<br/>A 类： 10.0.0.0-10.255.255.255<br/>B 类： 172.16.0.0-172.31.255.255<br/>C 类： 192.168.0.0-192.168.255.255<br/><font color="green">示例值：192.168.0.200</font> |
| terminal_location | 终端实时经纬度信息 | String | 32 | N | 设备（付款APP）GPS位置,格式为纬度/经度。<br/>+表示北纬、东经，-表示南纬、西经。<font color="green">示例值：+37.12/-121.213</font><br/>经度整数位不超过3位，小数位不超过5位；纬度整数位不超过2位，小数位不超过6位； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5c7d0700_dc97_47c0_84be_f79430e028cc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_huifu_id | 手续费商户号 | String | 32 | N | <font color="green">示例值：6666000123120001</font> |
| <span class="extend 81a07675_41d6_4b66_bd3a_d8cf1b43ebe7">fee_formula_infos</span> | 手续费费率信息 | Array |  | N | jsonArray格式；交易成功时返回手续费费率信息 |
| fee_flag | 手续费扣款标志 | String | 1 | N | 1: 外扣，2: 内扣；<font color="green">示例值：1</font> |
| fee_amount | 手续费金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>,最低传入0.01 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 81a07675_41d6_4b66_bd3a_d8cf1b43ebe7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | N | <font color="green">示例值：AMT\*0.003</font> |
| fee_type | 手续费类型 | String | 32 | N | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费<br/><font color="green">示例值：ACCT_FEE</font> |
| huifu_id | 商户号 | String | 32 | N | 组合支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
  "data": {
    "atu_sub_mer_id": "2088641544658593",
    "bank_message": "处理成功",
    "delay_acct_flag": "N",
    "div_flag": "N",
    "end_time": "20250804164236",
    "hf_seq_id": "0029000topA250804164235P330c0a8200900000",
    "huifu_id": "6666000003100616",
    "method_expand": "{\"buyer_logon_id\":\"131******66\",\"buyer_pay_amount\":\"0.00\",\"buyer_user_id\":\"2088052888888888283\",\"invoice_amount\":\"0.00\",\"point_amount\":\"0.00\",\"send_pay_date\":\"2025-08-04 16:42:36\"}",
    "out_trans_id": "2025080422001478281403316633",
    "party_order_id": "2508046015554200132",
    "payment_fee": "{\"fee_amount\":\"0.01\",\"fee_formula_infos\":[{\"fee_formula\":\"AMT*0.38\",\"fee_type\":\"TRANS_FEE\"}]}",
    "remark": "聚合反扫消费",
    "req_date": "20250804",
    "req_seq_id": "202508040442356120",
    "resp_code": "00000000",
    "resp_desc": "查询成功",
    "settlement_amt": "0.03",
    "trade_type": "A_IMICROPAY",
    "trans_amt": "0.03",
    "trans_stat": "S"
  }
}

```


#### 业务返回码

| 返回码  |返回描述                                                     |
| :------- | :----------------------------------------------------------- |
| 10000000|请求内容体不能为空                                           |
| 10000000|%s不能为空（%s代指报错参数名）                               |
| 10000000|%s长度固定%d位（%s代指报错参数名、%d代指字段长度）           |
| 10000000|%s最大长度为%d位（%s代指报错参数名、%d代指字段长度）         |
| 10000000|%s的传入枚举[%s]不存在（%s代指报错参数名）                   |
| 10000000|%s不符合%s格式（%s代指报错参数名）                           |
| 21000000|原机构请求流水号、交易返回的全局流水号、用户账单上的商户订单号、用户账单上的交易订单号、外部订单号、终端订单号不能同时为空 |
| 22000000|产品号不存在                                                 |
| 22000000|产品状态异常                                                 |
| 23000001|交易不存在                                                   |
| 91111119 | 通道异常，请稍后重试                            |
| 98888888|系统错误                                                     |

