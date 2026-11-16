
## 聚合下单接口

<span class="request-method post-method">POST</span>https://api.huifu.com/v4/trade/payment/create

*最近更新时间：2025.11.05*
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


聚合支付将多种支付方式统一为一个下单 API。
1. 如需了解不同支付方式，接入前需准备材料，查看对应支付方式下【产品介绍】文档；
2. 如需了解不同支付方式开发接入全流程指引，查看对应支付方式下【开发指引】文档；
3. 在开发过程中遇到问题，查看对应支付方式下【常见问题】文档。

以下是聚合支付支持的支付方式：
-  [微信公众号支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/wx_gzh_intro)：T_JSAPI
- [微信小程序支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/wx_xcx_intro)：T_MINIAPP
-  [微信付款码支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/wx_fkm_intro)：T_MICROPAY
- [支付宝 JS 支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/zfb_js_intro)：A_JSAPI
-  [支付宝正扫支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/zfb_zs_intro)：A_NATIVE
- [支付宝付款码支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/zfb_fkm_intro)：A_MICROPAY
- [银联 JS 支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/yl_js_intro)：U_JSAPI
-  [银联正扫支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/yl_zs_intro)：U_NATIVE
-  [银联付款码支付](https://paas.huifu.com/open/doc/lightning/#/guide/zf/yl_fkm_intro)：U_MICROPAY

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[加签验签](https://paas.huifu.com/partners/guide/#/api_v2jqyq)

### 公共参数
<!--
 请参考 <a href='/partners/jiekouguifan/#/api_qqxy.md'>「接口规范-请求/响应体模型」</a>
 -->
* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font> |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档       |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | N | 格式yyyyMMdd；<font color="green">示例值：20220905</font>  |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：rQ2021121311173944134649875651</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font> |
| trade_type | 交易类型 | String | 16 | Y | T_JSAPI：微信公众号支付<br/>T_MINIAPP：微信小程序支付<br/>T_APP：微信APP支付<br/>T_MICROPAY：微信反扫支付<br/>A_JSAPI：支付宝JS支付<br/>A_NATIVE：支付宝正扫支付<br/>A_MICROPAY：支付宝反扫支付<br/>U_JSAPI：银联JS支付<br/>U_NATIVE：银联正扫支付<br/>U_MICROPAY：银联反扫支付<br/><font color="green">示例值：A_NATIVE</font> |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1000.00</font>，最低传入0.01； |
| goods_desc | 商品描述 | String | 128 | Y | <font color="green">示例值：XX商品</font> |
| remark | 备注 | String | 255 | N | 交易后原样返回；<font color="green">示例值：备注</font> |
| acct_id | 账户号 | String | 9 | N | 可指定收款账户号，仅支持基本户、现金户，不填默认为基本户；<br/><font color="green">示例值：F00598600</font> |
| time_expire | 交易有效期 | String | 14 | N | 该笔订单允许付款最晚时间，建议大于1分钟；<br/>注意：微信、支付宝交易有订单超时时间，默认两小时关单；<br/>请求格式：yyyyMMddHHmmss；<font color="green">示例值：20220912111230</font> |
| delay_acct_flag | 延迟标识 | String | 1 | N | Y 为延迟 N为不延迟，不传默认N；<font color="green">示例值：Y</font> |
| fee_flag | 手续费扣款标识 | Integer | 1 | N | 1: 外扣 2: 内扣 (默认取控台配置值)；<font color="green">示例值：1</font> |
| limit_pay_type | 禁用支付方式 | String | 128 | N | 本次交易禁止使用的支付方式，默认不禁用；[取值参见说明](#参数说明)；<font color="green">示例值：NO_CREDIT</font> |
| channel_no | 渠道号 | String | 32 | N | 如果交易走自有渠道请联系运维人员获取；<font color="green">示例值:10000001</font> |
| pay_scene | 场景类型 | String | 2 | N | 参见[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%BE%AE%E4%BF%A1%E4%B8%9A%E5%8A%A1%E5%BC%80%E9%80%9A%E7%B1%BB%E5%9E%8B)说明；<font color="green">示例值:02</font> |
| term_div_coupon_type | 传入分帐遇到优惠的处理规则 | String | 2 | N | 1:按比例分,2:按分账明细顺序保障,3:只给交易商户（默认)；<font color="green">示例值:1</font> |
| fq_mer_discount_flag | 商户贴息标记 | String | 1 | N | 商户补贴活动，Y: 商户全额贴息，P：商户部分贴息，不传为非商户贴息（默认）；<font color="green">示例值：Y</font><br/>选择P：商户部分贴息活动，需同时在【ali_business_params：商户业务信息】中传入支付宝约定的活动参数，参数说明详见分期支付指引文档。 |
| notify_url | 异步通知地址 | String | 504 | N | 交易异步通知地址，http或https开头，异步回调报文格式见[异步返回参数](#异步返回参数)<br/><font color="green">示例值：https://callback.service.com/xx</font> |
| <span class="extend 0797951e_91fe_445a_bbfb_5f06a5d0bd72">method_expand</span> | 交易类型扩展参数 | String |  | Y | jsonObject字符串 |
| <span class="extend f8f0b7af_6afa_4650_905b_14e9003cb1aa">tx_metadata</span> | 扩展参数集合 | String |  | C | jsonObject字符串，交易能力扩展，tx_metadata只是方便文档展示，实际请求时不需要传入，传入下面的子项即可 |

<!-- extend:start -->
<!-- div:extend-table 0797951e_91fe_445a_bbfb_5f06a5d0bd72-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 3b1fbbb5_577d_4a1d_8c2b_0d9b093e3154">T_JSAPI</span> | 微信公众号支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 8a14ae91_ce3d_4965_8466_3eedefe1b500">T_MINIAPP</span> | 微信小程序支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 1f8a6990_a87a_4c2a_89ec_79e34b8018be">T_APP</span> | 微信APP支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 26c8308b_17e2_48d3_89ec_fdcc4aead8a9">T_MICROPAY</span> | 微信反扫支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 6742f5e1_69d5_4002_93c7_c1847a7ee6a8">A_JSAPI</span> | 支付宝JS支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 9730ab2d_aa0b_4348_ac9e_cbd6c183bb2f">A_NATIVE</span> | 支付宝正扫支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend ddf3ebfd_3ae6_4dcf_8147_ea200e49ce4d">A_MICROPAY</span> | 支付宝反扫参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 421a2d35_a6c0_4857_8064_c922dcd05369">U_JSAPI</span> | 银联JS支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend fcaebd11_cb06_48c0_a4d7_fcdff044f130">U_NATIVE</span> | 银联正扫支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 796670c7_5dd9_4c21_ad9e_b66718d97e63">U_MICROPAY</span> | 银联反扫支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3b1fbbb5_577d_4a1d_8c2b_0d9b093e3154-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | N | 子商户在微信申请的应用ID，全局唯一。**走聚合正扫发货管理的商户，使用的微信公众号/小程序支付 需要填写sub_appid+sub_openid**<br/><font color="green">示例值：wxd678efh567hg6999</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 公众号和小程序场景必填。用户在子商户sub_appid下的唯一标识。下单前需获取到用户的sub_openid，sub_openid获取详见微信文档[openid获取](https://pay.weixin.qq.com/docs/partner/development/glossary/parameter.html)。<br/><font color="green">示例值：oUpF8uMuAJO_M2pxb1Q9zNjWeS6o</font> |
| attach | 附加数据 | String | 127 | N | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；<br/><font color="green">示例值：附加数据</font> |
| body | 商品描述 | String | 128 | N | 商品或支付单简要描述，格式要求：门店品牌名-城市分店名-实际商品名称；<font color="green">示例值：image形象店-深圳腾大- QQ 公仔</font> |
| <span class="extend 561aef7a_b311_4dd1_8cc6_10772f2c4c33">detail</span> | 商品详情 | Object |  | N | 单品优惠功能字段 |
| goods_tag | 订单优惠标记 | String | 32 | N | 代金券或立减优惠功能的参数；<font color="green">示例值：WXG</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 561aef7a_b311_4dd1_8cc6_10772f2c4c33-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cost_price | 订单原价(元) | String | 12 | N | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 <br>2.当订单原价与支付金额不相等，则不享受优惠。<br>3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。<br/><font color="green">示例值：999.00</font> |
| receipt_id | 商品小票ID | String | 32 | N | 商家小票 ID；<font color="green">示例值：20220628132043853798</font> |
| <span class="extend 55e3f7f1_6ff0_4b33_be50_655256276ef3">goods_detail</span> | 单品列表 | Array |  | Y | 单品信息，使用Json数组格式提交 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 55e3f7f1_6ff0_4b33_be50_655256276ef3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | N | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_name | 商品名称 | String | 256 | N | 商品的实际名称；<font color="green">示例值：太龙双黄连口服液</font> |
| price | 商品单价(元) | String | 12 | N | 如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50<br/><font color="green">示例值：43.00</font> |
| quantity | 商品数量 | Integer | 11 | N | 用户购买的数量；<font color="green">示例值：1</font> |
| wxpay_goods_id | 微信侧商品编码 | String | 32 | N | <font color="green">示例值：12235413214070356458058</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8a14ae91_ce3d_4965_8466_3eedefe1b500-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | N | 子商户在微信申请的应用ID，全局唯一。**走聚合正扫发货管理的商户，使用的微信公众号/小程序支付 需要填写sub_appid+sub_openid**<br/><font color="green">示例值：wxd678efh567hg6999</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 公众号和小程序场景必填。用户在子商户sub_appid下的唯一标识。下单前需获取到用户的sub_openid，sub_openid获取详见微信文档[openid获取](https://pay.weixin.qq.com/docs/partner/development/glossary/parameter.html)。<br/><font color="green">示例值：oUpF8uMuAJO_M2pxb1Q9zNjWeS6o</font> |
| attach | 附加数据 | String | 127 | N | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；<br/><font color="green">示例值：附加数据</font> |
| body | 商品描述 | String | 128 | N | 商品或支付单简要描述，格式要求：门店品牌名-城市分店名-实际商品名称；<font color="green">示例值：image形象店-深圳腾大- QQ 公仔</font> |
| <span class="extend 8a928340_d362_4076_90cb_cd5423e239ab">detail</span> | 商品详情 | Object |  | N | 单品优惠功能字段 |
| goods_tag | 订单优惠标记 | String | 32 | N | 代金券或立减优惠功能的参数；<font color="green">示例值：WXG</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8a928340_d362_4076_90cb_cd5423e239ab-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cost_price | 订单原价(元) | String | 12 | N | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 <br>2.当订单原价与支付金额不相等，则不享受优惠。<br>3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。<br/><font color="green">示例值：999.00</font> |
| receipt_id | 商品小票ID | String | 32 | N | 商家小票 ID；<font color="green">示例值：20220628132043853798</font> |
| <span class="extend 37c1ccca_79a1_453c_bde3_705cb0385a83">goods_detail</span> | 单品列表 | Array |  | Y | 单品信息，使用Json数组格式提交 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 37c1ccca_79a1_453c_bde3_705cb0385a83-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | N | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_name | 商品名称 | String | 256 | N | 商品的实际名称；<font color="green">示例值：太龙双黄连口服液</font> |
| price | 商品单价(元) | String | 12 | N | 如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50<br/><font color="green">示例值：43.00</font> |
| quantity | 商品数量 | Integer | 11 | N | 用户购买的数量；<font color="green">示例值：1</font> |
| wxpay_goods_id | 微信侧商品编码 | String | 32 | N | <font color="green">示例值：12235413214070356458058</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1f8a6990_a87a_4c2a_89ec_79e34b8018be-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | N | 子商户在微信申请的应用ID，全局唯一。**走聚合正扫发货管理的商户，使用的微信公众号/小程序支付 需要填写sub_appid+sub_openid**<br/><font color="green">示例值：wxd678efh567hg6999</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 公众号和小程序场景必填。用户在子商户sub_appid下的唯一标识。下单前需获取到用户的sub_openid，sub_openid获取详见微信文档[openid获取](https://pay.weixin.qq.com/docs/partner/development/glossary/parameter.html)。<br/><font color="green">示例值：oUpF8uMuAJO_M2pxb1Q9zNjWeS6o</font> |
| attach | 附加数据 | String | 127 | N | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；<br/><font color="green">示例值：附加数据</font> |
| body | 商品描述 | String | 128 | N | 商品或支付单简要描述，格式要求：门店品牌名-城市分店名-实际商品名称；<font color="green">示例值：image形象店-深圳腾大- QQ 公仔</font> |
| <span class="extend b095b151_f7d2_42eb_93b1_1e6153e350cb">detail</span> | 商品详情 | Object |  | N | 单品优惠功能字段 |
| goods_tag | 订单优惠标记 | String | 32 | N | 代金券或立减优惠功能的参数；<font color="green">示例值：WXG</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b095b151_f7d2_42eb_93b1_1e6153e350cb-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cost_price | 订单原价(元) | String | 12 | N | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 <br>2.当订单原价与支付金额不相等，则不享受优惠。<br>3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。<br/><font color="green">示例值：999.00</font> |
| receipt_id | 商品小票ID | String | 32 | N | 商家小票 ID；<font color="green">示例值：20220628132043853798</font> |
| <span class="extend 37105029_b942_47bd_9d51_7968440b50f9">goods_detail</span> | 单品列表 | Array |  | Y | 单品信息，使用Json数组格式提交 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 37105029_b942_47bd_9d51_7968440b50f9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | N | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_name | 商品名称 | String | 256 | N | 商品的实际名称；<font color="green">示例值：太龙双黄连口服液</font> |
| price | 商品单价(元) | String | 12 | N | 如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50<br/><font color="green">示例值：43.00</font> |
| quantity | 商品数量 | Integer | 11 | N | 用户购买的数量；<font color="green">示例值：1</font> |
| wxpay_goods_id | 微信侧商品编码 | String | 32 | N | <font color="green">示例值：12235413214070356458058</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 26c8308b_17e2_48d3_89ec_fdcc4aead8a9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| auth_code | 支付授权码 | String | 128 | Y | 扫码设备读出的条形码或者二维码信息；<br/><font color="green">示例值：2884138408701518074</font> |
| sub_appid | 子商户公众账号id | String | 32 | N | 微信分配的子商户公众账号id，微信js/小程序支付必传。<br/>如需在支付完成后获取sub_openid则此参数必传。<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| device_info | 设备号 | String | 32 | N | 终端设备号(门店号或收银设备id)，<font color="green">示例值：660035730311000126101</font> |
| goods_tag | 订单优惠标记 | String | 32 | N | 代金券或立减优惠功能的参数；<font color="green">示例值：WXG</font> |
| attach | 附加数据 | String | 127 | N | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；<br/><font color="green">示例值：附加数据</font> |
| <span class="extend 76dbe501_1b82_440b_9639_30fb896637a2">detail</span> | 商品详情 | Object | 6000 | N | 商品详情 |
| <span class="extend 90b8a551_8053_415b_841a_6e08a5affb78">scene_info</span> | 场景信息 | Object | 2048 | N | 该字段用于上报场景信息，目前支持上报实际门店信息 |
| promotion_flag | 单品优惠标识	 | String | 1 | N | 直联模式使用字段；Y-是，N-否，默认否；<font color="green">示例值：Y</font><br/>若使用单品优惠，该字段必填，若该字段为Y，则商品详情【detail】必填 |
| spbill_create_ip | 收款设备IP | String | 16 | C | 直联模式必填字段；<font color="green">示例值：192.168.2.2</font> |
| receipt | 电子发票入口开放标识 | String | 8 | N | 直联模式使用字段；Y-是；<font color="green">示例值：Y</font><br/>传入Y时，支付成功消息和支付详情页将出现开票入口。<br/>需要在微信支付商户平台或微信公众平台开通电子发票功能，传此字段才可生效 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 76dbe501_1b82_440b_9639_30fb896637a2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cost_price | 订单原价(元) | String | 12 | N | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 <br>2.当订单原价与支付金额不相等，则不享受优惠。<br>3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。<br/><font color="green">示例值：999.00</font> |
| receipt_id | 商品小票ID | String | 32 | N | 商家小票 ID；<font color="green">示例值：20220628132043853798</font> |
| <span class="extend 7e38e5e1_20a0_458a_b7db_5ef7aa751c70">goods_detail</span> | 单品列表 | Array |  | Y | 单品信息，使用Json数组格式提交 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7e38e5e1_20a0_458a_b7db_5ef7aa751c70-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | N | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_name | 商品名称 | String | 256 | N | 商品的实际名称；<font color="green">示例值：太龙双黄连口服液</font> |
| price | 商品单价(元) | String | 12 | N | 如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50<br/><font color="green">示例值：43.00</font> |
| quantity | 商品数量 | Integer | 11 | N | 用户购买的数量；<font color="green">示例值：1</font> |
| wxpay_goods_id | 微信侧商品编码 | String | 32 | N | <font color="green">示例值：12235413214070356458058</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 90b8a551_8053_415b_841a_6e08a5affb78-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend e18b4963_c997_4c1e_b757_a6bbde0ed44b">store_info</span> | 门店信息 | Object |  | Y | 门店信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e18b4963_c997_4c1e_b757_a6bbde0ed44b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 门店id | String | 32 | N | 门店编号，由商户自定义；<font color="green">示例值：sh001</font> |
| name | 门店名称 | String | 64 | N | 门店名称，由商户自定义；<font color="green">示例值：上海宝山分店</font> |
| area_code | 门店行政区划码 | String | 6 | N | 门店所在地行政区划码，详见[行政区划代码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，<font color="green">示例值：310101 </font>； |
| address | 门店详细地址 | String | 128 | N | 门店详细地址，由商户自定义；<font color="green">示例值：上海宝山区共富路100号</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6742f5e1_69d5_4002_93c7_c1847a7ee6a8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| alipay_store_id | 支付宝的店铺编号 | String | 32 | N | <font color="green">示例值：2016041400077000000003314986</font> |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | <font color="green">示例值：2088202954065786</font>； |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font><br/>交易类型为A_JSAPI时【买家支付宝账号】与【买家支付宝用户号】二选一必填； |
| <span class="extend 30432a07_779f_4444_a7df_c84daa760713">goods_detail</span> | 订单包含的商品列表信息 | Array |  | N | 订单包含的商品列表信息 |
| <span class="extend e3ef69d3_185a_4120_af5e_2a6f26e5834d">extend_params</span> | 业务扩展参数 | Object |  | N | 业务扩展参数 |
| ali_promo_params | 优惠明细参数 | String |  | N | 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。<br/>示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"}  |
| seller_id | 卖家支付宝用户号 | String | 28 | N | <font color="green">示例值：20880414938706770000</font> |
| merchant_order_no | 商户原始订单号 | String | 32 | N | <font color="green">示例值：39045032345</font> |
| operator_id | 商户操作员编号 | String | 28 | N | <font color="green">示例值：carl.li@huifu.com</font> |
| product_code | 销售产品码 | String | 32 | N | <font color="green">示例值：YYZY</font> |
| <span class="extend 2a5b0e1c_694a_45a3_925f_d8fa7db8e9c4">ext_user_info</span> | 外部指定买家 | Object |  | N | 外部指定买家 |
| subject | 订单标题 | String | 256 | N | 直连模式必填；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；<font color="green">示例值：红果奶茶</font>   |
| store_name | 商家门店名称 | String | 512 | N | 直连模式字段；<font color="green">示例值：红果奶茶上海宝山店</font> |
| op_app_id | 小程序应用的appid | String | 32 | N | 小程序支付中，商户实际经营主体的小程序应用的appid，也即最终唤起收银台支付所在的小程序的应用id；<font color="green">示例值：wxec280d4c8a1cc2ca</font>  |
| ali_business_params | 商户业务信息 | String | 512 | N | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| body | 订单描述 | String | 128 | N |  <font color="green">示例值：IPhone</font>      | | ali_promo_params | 优惠明细参数 | String | N   | 否  | 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。<br/>示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"} |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 30432a07_779f_4444_a7df_c84daa760713-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品的编号 | String | 32 | Y | <font color="green">示例值：apple-01</font> |
| goods_name | 商品名称 | String | 256 | Y | <font color="green">示例值：ipad</font> |
| price | 商品单价(元) | String | 16 | Y | 单位：元；<font color="green">示例值：43.40</font> |
| quantity | 商品数量 | String | 10 | Y | <font color="green">示例值：40</font> |
| body | 商品描述信息 | String | 1000 | N | <font color="green">示例值：个人电脑</font> |
| categories_tree | 商品类目树 | String | 128 | N | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\|分割<br/><font color="green">示例值：124868003\|126232002\|126252004</font> |
| show_url | 商品的展示地址 | String | 400 | N | <font color="green">示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html</font>  |
| goods_category | 商品类目 | String | 24 | N | <font color="green">示例值：34543238</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e3ef69d3_185a_4120_af5e_2a6f26e5834d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 32 | N | <font color="green">示例值：S0JP0000</font> |
| food_order_type | 支付宝点餐场景类型 | String | 20 | N | QR_ORDER（店内扫码点餐）<br/>PRE_ORDER（预点到店自提）<br/>HOME_DELIVERY（外送到家）<br/>DIRECT_PAYMENT（直接付款）<br/>QR_FOOD_ORDER（点餐先付）<br/>P_QR_FOOD_ORDER（点餐后付）<br/>SELF_PICK（门店自提）<br/>TAKE_OUT （餐饮外卖）<br/>OTHER（其他）<br/>该参数只适用于支付宝支付窗交易接口；<font color="green">示例值：TAKE_OUT</font> |
| hb_fq_num | 花呗分期数 | String | 5 | N | 使用花呗分期要进行的分期数；<font color="green">示例值：3</font> |
| hb_fq_seller_percent | 花呗卖家手续费百分比 | String | 3 | N | 使用花呗分期需要卖家承担的手续费比，单位比例的百分值。<br/> 花呗商贴支付默认传0，<font color="green">示例值：0</font> |
| fq_channels | 信用卡分期资产方式 | String | 20 | N | 代表优先使用资产类型；alipayfq_cc：表示信⽤卡分期，为空时默认花呗。<font color="green">示例值：alipayfq_cc</font> |
| parking_id | 停车场id | String | 28 | N | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；<br/><font color="green">示例值：PI1504848980306666666</font> |
| sys_service_provider_id | 系统商编号 | String | 64 | N | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；<br/><font color="green">示例值：20880414938706770000</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2a5b0e1c_694a_45a3_925f_d8fa7db8e9c4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 姓名 | String | 16 | N | 注：need_check_info=T时，该参数才有效；<font color="green">示例值：张三</font> |
| mobile | 手机号 | String | 20 | N | 注：该参数暂不校验；<font color="green">示例值：13911111111</font>    |
| cert_type | 证件类型 | String | 32 | N | 身份证：IDENTITY_CARD，<br/>护照：PASSPORT；<br/>军官证：OFFICER_CARD，<br/>士兵证：SOLDIER_CARD；<br/>户口本：HOKOU；<br/><font color="green">示例值：IDENTITY_CARD</font><br/>注：need_check_info=T时，该参数才有效 |
| cert_no | 证件号 | String | 64 | N |  <font color="green">示例值：Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9M</font> ，<br/>需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。 <br/>注：need_check_info=T时，该参数才有效     |
| min_age | 允许的最小买家年龄 | String | 3 | N | 买家年龄必须大于等于所传数值。<font color="green">示例值：18</font> <br/>注：1\. need_check_info=T 时该参数才有效，2\. min_age 为整数，必须大于等于 0 |
| fix_buyer | 是否强制校验付款人身份信息 | String | 8 | N |  T：强制校验，F：不强制；<font color="green">示例值：T</font>  |
| need_check_info | 是否强制校验身份信息 | String | 1 | N | T：强制校验，F：不强制；<font color="green">示例值：F</font>  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9730ab2d_aa0b_4348_ac9e_cbd6c183bb2f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| alipay_store_id | 支付宝的店铺编号 | String | 32 | N | <font color="green">示例值：2016041400077000000003314986</font> |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | <font color="green">示例值：2088202954065786</font>； |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font><br/>交易类型为A_JSAPI时【买家支付宝账号】与【买家支付宝用户号】二选一必填； |
| <span class="extend bc8a5dd5_c878_40ca_8d28_53d4969144b9">goods_detail</span> | 订单包含的商品列表信息 | Array |  | N | 订单包含的商品列表信息 |
| <span class="extend 7d9db592_19f6_4a42_9180_7e5302286fc4">extend_params</span> | 业务扩展参数 | Object |  | N | 业务扩展参数 |
| ali_promo_params | 优惠明细参数 | String |  | N | 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。<br/>示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"}  |
| seller_id | 卖家支付宝用户号 | String | 28 | N | <font color="green">示例值：20880414938706770000</font> |
| merchant_order_no | 商户原始订单号 | String | 32 | N | <font color="green">示例值：39045032345</font> |
| operator_id | 商户操作员编号 | String | 28 | N | <font color="green">示例值：carl.li@huifu.com</font> |
| product_code | 销售产品码 | String | 32 | N | <font color="green">示例值：YYZY</font> |
| <span class="extend c929ee19_1cdd_4896_b361_572e7f3ed2ea">ext_user_info</span> | 外部指定买家 | Object |  | N | 外部指定买家 |
| subject | 订单标题 | String | 256 | N | 直连模式必填；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；<font color="green">示例值：红果奶茶</font>   |
| store_name | 商家门店名称 | String | 512 | N | 直连模式字段；<font color="green">示例值：红果奶茶上海宝山店</font> |
| op_app_id | 小程序应用的appid | String | 32 | N | 小程序支付中，商户实际经营主体的小程序应用的appid，也即最终唤起收银台支付所在的小程序的应用id；<font color="green">示例值：wxec280d4c8a1cc2ca</font>  |
| ali_business_params | 商户业务信息 | String | 512 | N | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| body | 订单描述 | String | 128 | N |  <font color="green">示例值：IPhone</font>      | | ali_promo_params | 优惠明细参数 | String | N   | 否  | 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。<br/>示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"} |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bc8a5dd5_c878_40ca_8d28_53d4969144b9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品的编号 | String | 32 | Y | <font color="green">示例值：apple-01</font> |
| goods_name | 商品名称 | String | 256 | Y | <font color="green">示例值：ipad</font> |
| price | 商品单价(元) | String | 16 | Y | 单位：元；<font color="green">示例值：43.40</font> |
| quantity | 商品数量 | String | 10 | Y | <font color="green">示例值：40</font> |
| body | 商品描述信息 | String | 1000 | N | <font color="green">示例值：个人电脑</font> |
| categories_tree | 商品类目树 | String | 128 | N | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\|分割<br/><font color="green">示例值：124868003\|126232002\|126252004</font> |
| show_url | 商品的展示地址 | String | 400 | N | <font color="green">示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html</font>  |
| goods_category | 商品类目 | String | 24 | N | <font color="green">示例值：34543238</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7d9db592_19f6_4a42_9180_7e5302286fc4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 32 | N | <font color="green">示例值：S0JP0000</font> |
| food_order_type | 支付宝点餐场景类型 | String | 20 | N | QR_ORDER（店内扫码点餐）<br/>PRE_ORDER（预点到店自提）<br/>HOME_DELIVERY（外送到家）<br/>DIRECT_PAYMENT（直接付款）<br/>QR_FOOD_ORDER（点餐先付）<br/>P_QR_FOOD_ORDER（点餐后付）<br/>SELF_PICK（门店自提）<br/>TAKE_OUT （餐饮外卖）<br/>OTHER（其他）<br/>该参数只适用于支付宝支付窗交易接口；<font color="green">示例值：TAKE_OUT</font> |
| hb_fq_num | 花呗分期数 | String | 5 | N | 使用花呗分期要进行的分期数；<font color="green">示例值：3</font> |
| hb_fq_seller_percent | 花呗卖家手续费百分比 | String | 3 | N | 使用花呗分期需要卖家承担的手续费比，单位比例的百分值。<br/> 花呗商贴支付默认传0，<font color="green">示例值：0</font> |
| fq_channels | 信用卡分期资产方式 | String | 20 | N | 代表优先使用资产类型；alipayfq_cc：表示信⽤卡分期，为空时默认花呗。<font color="green">示例值：alipayfq_cc</font> |
| parking_id | 停车场id | String | 28 | N | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；<br/><font color="green">示例值：PI1504848980306666666</font> |
| sys_service_provider_id | 系统商编号 | String | 64 | N | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；<br/><font color="green">示例值：20880414938706770000</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c929ee19_1cdd_4896_b361_572e7f3ed2ea-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 姓名 | String | 16 | N | 注：need_check_info=T时，该参数才有效；<font color="green">示例值：张三</font> |
| mobile | 手机号 | String | 20 | N | 注：该参数暂不校验；<font color="green">示例值：13911111111</font>    |
| cert_type | 证件类型 | String | 32 | N | 身份证：IDENTITY_CARD，<br/>护照：PASSPORT；<br/>军官证：OFFICER_CARD，<br/>士兵证：SOLDIER_CARD；<br/>户口本：HOKOU；<br/><font color="green">示例值：IDENTITY_CARD</font><br/>注：need_check_info=T时，该参数才有效 |
| cert_no | 证件号 | String | 64 | N |  <font color="green">示例值：Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9M</font> ，<br/>需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。 <br/>注：need_check_info=T时，该参数才有效     |
| min_age | 允许的最小买家年龄 | String | 3 | N | 买家年龄必须大于等于所传数值。<font color="green">示例值：18</font> <br/>注：1\. need_check_info=T 时该参数才有效，2\. min_age 为整数，必须大于等于 0 |
| fix_buyer | 是否强制校验付款人身份信息 | String | 8 | N |  T：强制校验，F：不强制；<font color="green">示例值：T</font>  |
| need_check_info | 是否强制校验身份信息 | String | 1 | N | T：强制校验，F：不强制；<font color="green">示例值：F</font>  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ddf3ebfd_3ae6_4dcf_8147_ea200e49ce4d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| auth_code | 支付授权码 | String | 128 | Y | 扫码设备读出的条形码或者二维码信息；<br/><font color="green">示例值：2884138408701518074</font> |
| alipay_store_id | 支付宝的店铺编号 | String | 32 | N | <font color="green">示例值：20880414938706770156</font> |
| <span class="extend 1845df79_2639_43f1_b92b_105693bb0c6b">goods_detail</span> | 订单包含的商品列表信息 | Array | 2048 | N | 订单包含的商品列表信息 |
| <span class="extend 150a3ed7_69c2_4012_b8d6_4da8fbbd30bc">extend_params</span> | 业务扩展参数 | Object | 2048 | N | 业务扩展参数 |
| ali_business_params | 商户业务信息 | String | 512 | N | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| operator_id | 商户操作员编号 | String | 28 | N | <font color="green">示例值：carl.li@huifu.com</font> |
| store_id | 商户门店编号 | String | 32 | N | <font color="green">示例值：sh1001</font> |
| <span class="extend 510c117d_2620_44d5_9723_0f2e8a1a3759">ext_user_info</span> | 外部指定买家 | Object |  | N |  |
| body | 订单描述 | String | 128 | N | <font color="green">示例值：IPhone</font> |
| ali_promo_params | 优惠明细参数 | String |  | N | 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。<br/>示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"} |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1845df79_2639_43f1_b92b_105693bb0c6b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品的编号 | String | 32 | Y | <font color="green">示例值：apple-01</font> |
| goods_name | 商品名称 | String | 256 | Y | <font color="green">示例值：ipad</font> |
| price | 商品单价(元) | String | 16 | Y | 单位：元；<font color="green">示例值：43.40</font> |
| quantity | 商品数量 | String | 10 | Y | <font color="green">示例值：40</font> |
| body | 商品描述信息 | String | 1000 | N | <font color="green">示例值：个人电脑</font> |
| categories_tree | 商品类目树 | String | 128 | N | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\|分割<br/><font color="green">示例值：124868003\|126232002\|126252004</font> |
| goods_category | 商品类目 | String | 24 | N | <font color="green">示例值：34543238</font> |
| show_url | 商品的展示地址 | String | 400 | N | <font color="green">示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html</font>  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 150a3ed7_69c2_4012_b8d6_4da8fbbd30bc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 32 | N | <font color="green">示例值：S0JP0000</font> |
| food_order_type | 支付宝点餐场景类型 | String | 20 | N | QR_ORDER（店内扫码点餐）<br/>PRE_ORDER（预点到店自提）<br/>HOME_DELIVERY（外送到家）<br/>DIRECT_PAYMENT（直接付款）<br/>QR_FOOD_ORDER（点餐先付）<br/>P_QR_FOOD_ORDER（点餐后付）<br/>SELF_PICK（门店自提）<br/>TAKE_OUT （餐饮外卖）<br/>OTHER（其他）<br/>该参数只适用于支付宝支付窗交易接口；<font color="green">示例值：QR_ORDER</font> |
| hb_fq_num | 花呗分期数 | String | 5 | N | 使用花呗分期要进行的分期数；<font color="green">示例值：3</font> |
| hb_fq_seller_percent | 花呗卖家承担的手续费百分比 | String | 3 | N | 使用花呗分期需要卖家承担的手续费比，默认0；<br/>数据格式:比例的百分值，<font color="green">示例值：9</font>，传入100代表100%； |
| industry_reflux_info | 行业数据回流信息 | String | 512 | N | <font color="green">示例值：{\"scene_code\":\"metro_tradeorder\",\"channel\":\"xxxx\",\"scene_data\":{\"asset_name\":\"ALIPAY\"}}</font> |
| parking_id | 停车场id | String | 28 | N | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；<br/><font color="green">示例值：PI1504848980306666666</font> |
| sys_service_provider_id | 系统商编号 | String | 64 | N | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；<br/><font color="green">示例值：20880414938706770000</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 510c117d_2620_44d5_9723_0f2e8a1a3759-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 姓名 | String | 16 | N | 注：need_check_info=T时，该参数才有效；<font color="green">示例值：张三</font> |
| mobile | 手机号 | String | 20 | N | 注：该参数暂不校验；<font color="green">示例值：13911111111</font> |
| cert_type | 证件类型 | String | 32 | N | 身份证：IDENTITY_CARD，<br/>护照：PASSPORT；<br/>军官证：OFFICER_CARD，<br/>士兵证：SOLDIER_CARD；<br/>户口本：HOKOU；<br/><font color="green">示例值：IDENTITY_CARD</font><br/>注：need_check_info=T时，该参数才有效 |
| cert_no | 证件号 | String | 64 | N | <font color="green">示例值：Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9M</font>；<br/>需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。  <br/>注：need_check_info=T时，该参数才有效 |
| min_age | 允许的最小买家年龄 | String | 3 | N | 买家年龄必须大于等于所传数值。<font color="green">示例值：18</font> <br/>注：1\. need_check_info=T 时该参数才有效;<br/>2\. min_age 为整数，必须大于等于 0 |
| fix_buyer | 是否强制校验付款人身份信息 | String | 8 | N | T：强制校验，F：不强制；<font color="green">示例值：T</font> |
| need_check_info | 是否强制校验身份信息 | String | 1 | N | T：强制校验，F：不强制；<font color="green">示例值：F</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 421a2d35_a6c0_4857_8064_c922dcd05369-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| qr_code | 二维码 | String | 256 | N | 台牌码的url，交易类型为U_JSAPI:银联JS时必填 |
| addn_data | 收款方附加数据 | String | 3000 | N | 请参考[银联收款方附加数据(addn_data)说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylcsjh#银联收款方附加数据(addn_data)) |
| customer_ip | 持卡人ip | String | 40 | N | 持卡人确认付款时的ip地址，用于防钓鱼。（js支付必填）<font color="green">示例值：127.1.1.1</font> |
| front_url | 前台通知地址 | String | 200 | N | 收款方向银联推送订单时上送的前台通知地址（仅允许为外网地址）；<br/>用户完成支付点击“返回”后，银联通过浏览器post请求到该地址。<br/><font color="green">示例值：http://www.huifu.com</font> |
| order_desc | 订单描述 | String | 200 | N | <font color="green">示例值：订单描述</font> |
| payee_comments | 收款方附言 | String | 100 | N | <font color="green">示例值：业务收款</font> |
| <span class="extend 57674762_133b_447b_9c47_ca8dc81f967d">payee_info</span> | 收款方信息 | Object |  | N |  |
| req_reserved | 请求方自定义域 | String | 500 | N | <font color="green">示例值：</font> |
| user_id | 银联用户标识 | String | 128 | N | 调用[获取银联用户标识接口](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_unionauth)会返回【user_id】；<br/><font color="green">示例值：gaqiMrRnKwwOZO7dNtUc349YTMaa3HkRZg+OMU+46ysDzn6flfomHP88qOvH+6yG</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 57674762_133b_447b_9c47_ca8dc81f967d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| mer_cat_code | 商户类别 | String | 4 | N | [参考银联商户类别](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylshlb)；<font color="green">示例值：0101</font> |
| sub_id | 二级商户代码 | String | 20 | N | <font color="green">示例值：823586070110039</font> |
| sub_name | 二级商户名称 | String | 100 | N | <font color="green">示例值：上海白乐门酒店</font> |
| term_id | 终端号 | String | 8 | N | <font color="green">示例值：58000001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fcaebd11_cb06_48c0_a4d7_fcdff044f130-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| qr_code | 二维码 | String | 256 | N | 台牌码的url，交易类型为U_JSAPI:银联JS时必填 |
| addn_data | 收款方附加数据 | String | 3000 | N | 请参考[银联收款方附加数据(addn_data)说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylcsjh#银联收款方附加数据(addn_data)) |
| customer_ip | 持卡人ip | String | 40 | N | 持卡人确认付款时的ip地址，用于防钓鱼。（js支付必填）<font color="green">示例值：127.1.1.1</font> |
| front_url | 前台通知地址 | String | 200 | N | 收款方向银联推送订单时上送的前台通知地址（仅允许为外网地址）；<br/>用户完成支付点击“返回”后，银联通过浏览器post请求到该地址。<br/><font color="green">示例值：http://www.huifu.com</font> |
| order_desc | 订单描述 | String | 200 | N | <font color="green">示例值：订单描述</font> |
| payee_comments | 收款方附言 | String | 100 | N | <font color="green">示例值：业务收款</font> |
| <span class="extend ff3416a8_56f6_4a12_b9a1_ff23d28a6963">payee_info</span> | 收款方信息 | Object |  | N |  |
| req_reserved | 请求方自定义域 | String | 500 | N | <font color="green">示例值：</font> |
| user_id | 银联用户标识 | String | 128 | N | 调用[获取银联用户标识接口](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_unionauth)会返回【user_id】；<br/><font color="green">示例值：gaqiMrRnKwwOZO7dNtUc349YTMaa3HkRZg+OMU+46ysDzn6flfomHP88qOvH+6yG</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ff3416a8_56f6_4a12_b9a1_ff23d28a6963-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| mer_cat_code | 商户类别 | String | 4 | N | [参考银联商户类别](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylshlb)；<font color="green">示例值：0101</font> |
| sub_id | 二级商户代码 | String | 20 | N | <font color="green">示例值：823586070110039</font> |
| sub_name | 二级商户名称 | String | 100 | N | <font color="green">示例值：上海白乐门酒店</font> |
| term_id | 终端号 | String | 8 | N | <font color="green">示例值：58000001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 796670c7_5dd9_4c21_ad9e_b66718d97e63-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| auth_code | 支付授权码 | String | 128 | N | 扫码设备读出的条形码或者二维码信息；<br/><font color="green">示例值：2884138408701518074</font> |
| currency_code | 币种 | String | 3 | N | 156代表人民币；<font color="green">示例值：156</font> |
| invoice_st | 支持发票 | String | 1 | N | 0：表示不支持根据银行返回信息打印发票；此为缺省状态。<br/>1：表示可以根据银行返回信息打印发票；<br/><font color="green">示例值：1</font> |
| mer_cat_code | 商户类别 | String | 4 | N | 商户类别；<font color="green">示例值：</font> |
| pnr_ins_id_cd | 服务商机构标识码 | String | 11 | N | 银联分配的服务商机构标识码；<font color="green">示例值：01008330</font> |
| specfeeinfo | 特殊计费信息 | String | 3 | N | 特殊计费信息；<font color="green">示例值：</font> |
| term_id | 终端号 | String | 8 | N | 终端号；<font color="green">示例值：58000001</font> |
| addn_data | 收款方附加数据 | String | 3000 | N | 请参考[银联收款方附加数据(addn_data)说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylcsjh#银联收款方附加数据(addn_data)) |
| <span class="extend 81560daf_a6c7_45a6_907d_c36e53b72835">pid_info</span> | 服务商信息 | Object |  | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 81560daf_a6c7_45a6_907d_c36e53b72835-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pnr_order_id | 服务商订单编号 | String | 40 | N | 服务商自定义并发送，同一交易日期内不可重复，订单编号将作为服务商和银联对账的唯一索引，不超过40字节的变长字母和/或数字字符，不能含“-”或“_” |
| pid_sct | 服务商密文 | String | 8 | N | 由服务商根据服务商代码标识加密算法生成 |
| trade_scene | 场景标识 | String | 8 | N | 取值如下:1-扫码点餐<font color="green">示例值：1</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f8f0b7af_6afa_4650_905b_14e9003cb1aa-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 4cfd2ae6_412b_4c54_91d5_182977d27861">acct_split_bunch</span> | 分账对象 | String |  | N | jsonObject字符串 |
| <span class="extend f91949e8_09ab_4166_832a_4e21c1e7341d">terminal_device_data</span> | 设备信息 | String |  | C | 设备信息；反扫支付时必填 |
| <span class="extend cdbeed72_9296_40ae_9564_65b65ffa95fd">combinedpay_data</span> | 补贴支付信息	 | String |  | N | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| <span class="extend 7119054d_e2ca_44f2_82a0_1c29b8b5f9a9">combinedpay_data_fee_info</span> | 补贴支付手续费承担方信息 | String |  | N | jsonObject字符串 |
| <span class="extend 710b2926_7b1d_4c16_9558_9d09b7ac091d">trans_fee_allowance_info</span> | 手续费补贴信息 | String |  | N | 手续费补贴信息对象，jsonObject字符串 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4cfd2ae6_412b_4c54_91d5_182977d27861-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 7017c5bb_cf15_4575_b405_9f854033a254">acct_infos</span> | 分账明细 | Array |  | N | jsonArray分账明细 |
| percentage_flag | 百分比分账标志 | String | 1 | N | Y:使用百分比分账；<font color="green">示例值：Y</font> |
| is_clean_split | 是否净值分账 | String | 1 | N | Y:使用净值分账，仅在交易手续费内扣且使用百分比分账时起作用；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7017c5bb_cf15_4575_b405_9f854033a254-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120001</font> |
| acct_id | 账户号 | String | 9 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户；<font color="green">示例值：F00598600</font> |
| percentage_div | 分账百分比% | String | 6 | N | <font color="green">示例值：23.50</font>，表示23.50%。仅在percentage_flag=Y时起作用<br> acct_infos中全部分账百分比之和必须为100.00%。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f91949e8_09ab_4166_832a_4e21c1e7341d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| device_ip | 交易设备IP | String | 16 | N | 绑卡设备所在的公网IP，可用于定位所属地区，不是wifi连接时的局域网IP。<br/><font color="green">示例值：10.10.0.1</font>（IPv4）；<br/>ABCD&#58;EF01&#58;2345&#58;6789&#58;ABCD&#58;EF01&#58;2345&#58;6789（IPv6）；<!--<br/>0123&#58;4567&#58;89AB&#58;CDEF&#58;0123&#58;4567&#58;10.10.0.10（IPv6）；--> 目前暂传IPv4格式。（反扫交易必填） |
| device_mac | 交易设备MAC | String | 64 | N | <font color="green">示例值：F0E1D2C3B4A5</font> |
| device_imei | 交易设备IMEI | String | 64 | N | 移动终端设备的唯一标识；<font color="green">示例值：460030912121001</font> |
| device_imsi | 交易设备IMSI | String | 64 | N | <font color="green">示例值：460030912121001</font> |
| device_icc_id | 交易设备ICCID | String | 64 | N | <font color="green">示例值：898600680113F0123014</font> |
| device_wifi_mac | 交易设备WIFIMAC | String | 64 | N | <font color="green">示例值：968778695A4B</font> |
| device_gps | 交易设备GPS | String | 64 | N | <font color="green">示例值：20.346790,-4.654321</font> |
| app_version | 商户终端应用程序版 | String | 8 | N | 终端应用程序的版本号。应用程序变更应保证版本号不重复；<font color="green">示例值：3.2.5</font><!--259号文新增字段--> |
| encrypt_rand_num | 加密随机因子 | String | 10 | N | 参见[《加密随机因子说明》](https://paas.huifu.com/open/doc/api/#/smzf/api_jmsjyzsm) ；<br/>仅在被扫支付类交易报文中出现：<br/>若付款码为19位数字，则取后6位；<br/>若付款码为EMV二维码，则取其tag57的卡号/token号的后6位；<br/><font color="green">示例值：127026</font> |
| icc_id | SIM 卡卡号 | String | 20 | N | ICCID，SIM 卡卡号；<font color="green">示例值：898600680113F0123014</font> |
| location | 商户终端实时经纬度信息 | String | 32 | N | 受理终端设备实时经纬度信息，银联云闪付交易必填<br/>格式为纬度/经度，+表示北纬、东经，-表示南纬、西经。<font color="green">示例值：+37.12/-121.213</font>；<br/>经度整数位不超过3位，小数位不超过5位；纬度整数位不超过2位，小数位不超过6位。<br />注：银联AT交易时，location和mer_device_IP二选一必填其一 |
| mer_device_ip | 商户交易设备IP | String | 64 | N | <font color="green">示例值：10.10.0.1</font>；<br />注：银联AT交易时，location和mer_device_IP二选一必填其一 |
| mer_device_type | 商户设备类型 | String | 2 | N | 01：自动柜员机（含ATM和CDM）和多媒体自助终端，02：传统POS，03：mPOS，<br/>04：智能 POS，05：II 型固定电话，06：云闪付终端，<br/>08：手机POS，09：刷脸付终端，10：条码支付受理终端，<br/>11：条码支付辅助受理终端（如：台牌码），<br/>12：行业终端（公交、地铁用于指 定行业的终端），13：MIS 终端；<br/><font color="green">示例值：11</font><!--259号文新增字段--> |
| mobile_country_cd | 移动国家代码 | String | 3 | N | 基站信息，由国际电联(ITU)统一分配的移动国家代码（MCC），中国为 460（默认）；<br/><font color="green">示例值：460</font><!--259号文新增字段--> |
| mobile_net_num | 移动网络号码 | String | 2 | N | 由国际电联(ITU)统一分配的移动网络号码（MNC）。<br/>移动：00、02、04、07； 联通：01、06、09； 电信：03、05、11；<br/><font color="green">示例值：00</font><!--259号文新增字段--> |
| network_license | 商户终端入网认证编号 | String | 5 | N | 银行卡受理终端产品入网认证编号。格式：5 位字符，<font color="green">示例值：P3100</font>；<!--259号文新增字段--><br/>该编号由“中国银联标识产品企业资质认证办公室”为通过入网认证的终端进行分配； |
| secret_text | 密文数据 | String | 16 | N | <!--259号文新增字段。<br/>-->仅在被扫支付类交易报文中出现：64bit的密文数据，对终端硬件序列号和加密随机因子加密后的结果。<br/>本子域取值为：64bit密文数据进行base64编码后的结果。反扫辅助类设备可以为空；<br/><font color="green">示例值：MkQ2MTVEQkY=\n</font> |
| serial_num | 商户终端序列号 | String | 50 | N | 终端设备的硬件序列号；<font color="green">示例值：00000304N7NL01933217</font><!--259号文新增字段--> |
| devs_id | 汇付机具号 | String | 32 | N | 通过汇付报备的机具必传；<font color="green">示例值：SP003pcf</font><br/>参见[新增终端报备](https://paas.huifu.com/open/doc/api/#/zdgl/api_zdbb_xzzd)或[商户终端信息查询](https://paas.huifu.com/open/doc/api/#/zdgl/api_zdbb_bdzdxxcx)接口的返参device_id； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table cdbeed72_9296_40ae_9564_65b65ffa95fd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴方汇付商户号 | String | 32 | N | 补贴方汇付ID；<font color="green">示例值：6666000123123123</font> |
| user_type | 补贴方类型 | String | 32 | N | channel-渠道，merchant-总部商户，agent-代理，mertomer-商户；<font color="green">示例值：channel</font> |
| acct_id | 补贴方账户号 | String | 32 | N | 营销补贴方账户号；<font color="green">示例值：F00900982</font> |
| amount | 补贴金额 | String | 14 | N | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7119054d_e2ca_44f2_82a0_1c29b8b5f9a9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴支付手续费承担方汇付编号 | String | 32 | N | <font color="green">示例值：6666000123120001</font> |
| acct_id | 补贴支付手续费承担方账户号 | String | 32 | N | 补贴支付手续费承担方账户号；<font color="green">示例值：F00598610</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 710b2926_7b1d_4c16_9558_9d09b7ac091d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| allowance_fee_amt | 补贴手续费金额 | String | 16 | N | 金额以元为单位，最少1分，<font color="green">示例值：0.01</font>；</br>1.补贴手续费金额小于或等于该笔手续费金额时，按照补贴手续费金额补贴；</br>2.补贴手续费金额大于该笔手续费金额时，按照该笔交易实际手续费金额补贴； |
<!-- extend:end -->


#### SDK示例

```java
 public static void pay() throws Exception {
        BasePay.initWithMerConfig(OppsMerchantConfigDemo.getMerchantConfig());
        TradePaymentCreateRequest request = new TradePaymentCreateRequest();
        // 请求日期
        request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
        // 请求流水号
        request.setReqSeqId(SequenceTools.getReqSeqId32());
        // 商户号
        request.setHuifuId("6666000103334211");
        // 商品描述
        request.setGoodsDesc("支付宝Native");
        // 交易类型
        request.setTradeType("A_NATIVE");
        // 交易金额
        request.setTransAmt("0.01");
        request.setDelayAcctFlag("N");
        Map<String, Object> response = Factory.Payment.Common()
                .optional("method_expand", getMethodExpand(request.getTradeType()))
                .optional("terminal_device_data", getTerminalDeviceData())
                .create(request);
        ObjectMapper objectMapper = JacksonUtils.getInstance();
        System.out.println("返回数据:" + objectMapper.writeValueAsString(response))
    }

```
### 返回参数


#### 同步返回参数

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/docs/start/#/kfjr/jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数     |

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码) |
| resp_desc | 业务响应信息 | String | 256 | Y | [业务返回描述](#业务返回码) |
| req_date | 请求日期 | String | 8 | Y | 交易时传入，原样返回；<font color="green">示例值：20220905</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 交易时传入，原样返回；<font color="green">示例值：rQ2021121311173944134649875651</font> |
| hf_seq_id | 全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A221019132207P068ac1362af00000</font> |
| trade_type | 交易类型 | String | 16 | N | T_JSAPI:  微信公众号支付<br/>T_MINIAPP:  微信小程序支付  <br/>A_JSAPI:  支付宝JS  <br/>A_NATIVE:  支付宝正扫  <br/>U_NATIVE:  银联正扫  <br/>U_JSAPI:  银联 JS  <br/>D_NATIVE:  数字人民币正扫  <br/>T_H5：微信直连H5支付<br/>T_APP：微信APP支付<br/><font color="green">示例值：T_JSAPI</font> |
| trans_amt | 交易金额 | String | 14 | N | 单位元， <font color="green">示例值：1.00</font>单位元， <font color="green">示例值：1.00</font> |
| trans_stat | 交易状态 | String | 1 | N | P:处理中、S:成功、F:失败；交易状态以此字段为准。<font color="green">示例值：S</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font> |
| delay_acct_flag | 延时标记 | String | 1 | N | Y: 延迟 N: 实时（默认）；<font color="green">示例值：Y</font></br>注意延时交易要调【交易确认】接口资金才能进入收款方账户，否则会停留在延时账户中。 |
| remark | 备注 | String | 255 | N | 原样返回；<font color="green">示例值：备注</font> |
| device_type | 终端类型 | String | 2 | N | 01-智能POS<br>02-扫码POS<br>03-云音箱<br>04-台牌<br>05-云打印<br>06-扫脸设备<br>07-收银机<br>08-收银助手<br>09-传统POS<br>10-一体音箱<br>11-虚拟终端<br/><font color="green">示例值：01</font> |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | <font color="green">示例值：092021091922001451301445517582</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | 参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd)；<font color="green">示例值：03232109190255105603561</font> |
| pay_info | js支付信息 | String | 1024 | N | JSAPI支付返回信息； |
| qr_code | 二维码链接 | String | 1024 | N | NATIVE支付返回二维码链接；<br/><font color="green">示例值：https://qr.alipay.com/bax03232ftw69valbwmg000d</font> |
| atu_sub_mer_id | ATU真实商户号 | String | 32 | N | 微信、支付宝、银联真实商户号；<font color="green">示例值：411111141</font> |
| unconfirm_amt | 待确认金额 | String | 14 | N | 待确认金额；单位元。<font color="green">示例值：1.00</font> |
| settlement_amt | 结算金额 | String | 16 | N | 单位元；<font color="green">示例值：1.00</font> |
| debit_type | 借贷记标识 | String | 1 | N | 1-借记卡，2-贷记卡，3-其他；<font color="green">示例值：1</font> |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | <font color="green">示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk=</font> |
| end_time | 支付完成时间 | String | 14 | N | 格式yyyyMMddHHMMSS，<font color="green">示例值：20091225091010</font> |
| acct_id | 账户号 | String | 9 | N | 商户账户号；<font color="green">示例值：F00598600</font> |
| acct_stat | 账务状态 | String | 1 | N | P：处理中，S：成功，F：失败；<font color="green">示例值：S</font> |
| bank_message | 通道返回描述 | String | 200 | N | <font color="green">示例值：成功[0000000]</font> |
| <span class="extend 8a4defdd_dd91_4ef5_927e_5d63f591acd7">method_expand</span> | 交易扩展参数 | String |  | N | jsonObject字符串 |
| <span class="extend 044b6ea1_577c_448c_b9b8_e7feda377775">tx_metadata</span> | 扩展参数集合 | String |  | N | jsonObject字符串，tx_metadata只是方便文档展示，实际请求时不需要传入，传入下面的子项即可 |
| <span class="extend ba6f0baf_e65b_4233_9c72_5a2e18737588">payment_fee</span> | 手续费对象 | String |  | N | jsonObject字符串 |

<!-- extend:start -->
<!-- div:extend-table 8a4defdd_dd91_4ef5_927e_5d63f591acd7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend b17471e2_58f7_4213_9ca8_6496d21fec93">T_JSAPI</span> | 微信公众号支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 3ae5ad2a_4481_4ce0_9a83_1f73c4127ae6">T_MINIAPP</span> | 微信小程序支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend c99d5599_5738_4014_907e_4e1ce66c097d">T_APP</span> | 微信APP支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend ffd98ac2_2491_441c_8d80_c4af0b2cdb5e">T_MICROPAY</span> | 微信反扫支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 6b6b4c5c_9ab4_4629_bf1a_915aba64948e">A_JSAPI</span> | 支付宝JS支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend ff96e4ef_65e5_4bc5_a2e4_3e4a1236c4d3">A_NATIVE</span> | 支付宝正扫支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 1d7d3d0a_c588_4ae1_8eb4_1fc64f7aedad">A_MICROPAY</span> | 支付宝反扫参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 5f8f6e70_5c3c_4fc3_9597_280eced01f2b">U_JSAPI</span> | 银联JS支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 6af42ce3_fe7c_4958_8933_a28ad5e00fdb">U_NATIVE</span> | 银联正扫支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| <span class="extend 7edf1d20_21fc_4aea_9415_cce8e1064f10">U_MICROPAY</span> | 银联反扫支付参数 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b17471e2_58f7_4213_9ca8_6496d21fec93-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N |  微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | N | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | N | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；<font color="green">示例值：OTHERS</font> |
| coupon_fee | 代金券金额 | String | 100 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：0.10</font> |
| attach | 商家数据包 | String | 127 | N | 商家数据包，原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend 16d90316_9531_4890_a387_5bc59248e518">promotion_detail</span> | 营销详情列表 | Array |  | N | 营销详情列表，使返回值为Json格式； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 16d90316_9531_4890_a387_5bc59248e518-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| promotion_id | 券id | String | 32 | Y | 券或者立减优惠id；<font color="green">示例值：2345234235</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL: 全场代金券，SINGLE: 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON:  代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT:  优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font>  |
| amount | 优惠券面额 | String | 12 | Y | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）<font color="green">示例值：5.00</font> |
| activity_id | 活动ID | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| merchant_contribute | 商户出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；<br/><font color="green">示例值：10.00</font> |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方出资金额=商家出资+微信出资，单位为元；<font color="green">示例值：20.00</font> |
| <span class="extend 8ddaf16f_998f_43cc_b507_b177c47d32e4">goods_detail</span> | 单品列表 | Array |  | N | 单品信息，使用Json格式，是promotion_detail的元素； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8ddaf16f_998f_43cc_b507_b177c47d32e4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码	 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格 | String | 32 | Y | 单位为:元。<font color="green">示例值：99.00</font>；如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，<br/>则活动商品的单价应为原单价-50元 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3ae5ad2a_4481_4ce0_9a83_1f73c4127ae6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N |  微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | N | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | N | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；<font color="green">示例值：OTHERS</font> |
| coupon_fee | 代金券金额 | String | 100 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：0.10</font> |
| attach | 商家数据包 | String | 127 | N | 商家数据包，原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend 870555b0_9000_4a18_a444_e35f1288c44c">promotion_detail</span> | 营销详情列表 | Array |  | N | 营销详情列表，使返回值为Json格式； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 870555b0_9000_4a18_a444_e35f1288c44c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| promotion_id | 券id | String | 32 | Y | 券或者立减优惠id；<font color="green">示例值：2345234235</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL: 全场代金券，SINGLE: 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON:  代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT:  优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font>  |
| amount | 优惠券面额 | String | 12 | Y | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）<font color="green">示例值：5.00</font> |
| activity_id | 活动ID | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| merchant_contribute | 商户出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；<br/><font color="green">示例值：10.00</font> |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方出资金额=商家出资+微信出资，单位为元；<font color="green">示例值：20.00</font> |
| <span class="extend 10331b45_b61c_480f_9ffb_4e149e764c3b">goods_detail</span> | 单品列表 | Array |  | N | 单品信息，使用Json格式，是promotion_detail的元素； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 10331b45_b61c_480f_9ffb_4e149e764c3b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码	 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格 | String | 32 | Y | 单位为:元。<font color="green">示例值：99.00</font>；如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，<br/>则活动商品的单价应为原单价-50元 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c99d5599_5738_4014_907e_4e1ce66c097d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N |  微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | N | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | N | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；<font color="green">示例值：OTHERS</font> |
| coupon_fee | 代金券金额 | String | 100 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：0.10</font> |
| attach | 商家数据包 | String | 127 | N | 商家数据包，原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend 9aaecfb9_067e_4b81_bb52_14868812a882">promotion_detail</span> | 营销详情列表 | Array |  | N | 营销详情列表，使返回值为Json格式； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9aaecfb9_067e_4b81_bb52_14868812a882-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| promotion_id | 券id | String | 32 | Y | 券或者立减优惠id；<font color="green">示例值：2345234235</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL: 全场代金券，SINGLE: 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON:  代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT:  优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font>  |
| amount | 优惠券面额 | String | 12 | Y | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）<font color="green">示例值：5.00</font> |
| activity_id | 活动ID | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| merchant_contribute | 商户出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；<br/><font color="green">示例值：10.00</font> |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方出资金额=商家出资+微信出资，单位为元；<font color="green">示例值：20.00</font> |
| <span class="extend ae0a770d_a8c3_405e_a5ce_cab8a0a802f4">goods_detail</span> | 单品列表 | Array |  | N | 单品信息，使用Json格式，是promotion_detail的元素； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ae0a770d_a8c3_405e_a5ce_cab8a0a802f4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码	 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格 | String | 32 | Y | 单位为:元。<font color="green">示例值：99.00</font>；如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，<br/>则活动商品的单价应为原单价-50元 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ffd98ac2_2491_441c_8d80_c4af0b2cdb5e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| openid | 用户标识 | String | 128 | N | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 32 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| cash_fee | 现金支付金额 | String | 12 | N | 现金支付金额订单现金支付金额；<font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| coupon_fee | 代金券金额 | String |  | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| <span class="extend df45d9d1_72a8_42e7_95ba_18f48a1ddfa2">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 使返回值为Json格式， |
| bank_type | 付款银行 | String | 16 | N | 银行类型，采用字符串类型的银行标识，银行类型见[微信银行类型说明](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；<font color="green">示例值：ICBC_DEBIT</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table df45d9d1_72a8_42e7_95ba_18f48a1ddfa2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| activity_id | 活动id | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| promotion_id | 券或者立减优惠id | String | 32 | Y | <font color="green">示例值：2345234235</font> |
| <span class="extend d1ce1401_d32a_44e6_bf07_3f26cee3e7d0">goods_detail</span> | 单品列表 | Array | 3000 | N | 单品信息，使用Json格式，是promotion_detail的元素 |
| merchant_contribute | 商户出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；<br/><font color="green">示例值：10.00</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方出资金额=商家出资+微信出资，单位为元；<font color="green">示例值：20.00</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL:全场代金券，SINGLE:单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON:代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）<br />DISCOUNT:优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font> |
| wxpay_contribute | 微信出资 | String | 32 | N | 特指由微信支付商户平台创建的优惠，单位：元；<font color="green">示例值：20.00</font> |
| original_other_contribute | 微信交易其他出资方出资金额 | String | 32 | N | 微信的其他出资方出资金额，单位：元；<font color="green">示例值：20.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d1ce1401_d32a_44e6_bf07_3f26cee3e7d0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| price | 商品价格 | String | 32 | Y | 单位为：元<!--李锦说是元-->。<font color="green">示例值：50.00</font>。<br/>如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，<br/>则活动商品的单价应为原单价-50元； |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| goods_remark | 商品备注 | String | 32 | N | 按照配置原样返回，字段内容在微信后台配置券时进行设置。<font color="green">示例值：商品备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6b6b4c5c_9ab4_4629_bf1a_915aba64948e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend a901c3a7_38ac_49ab_9afe_498becc24a9a">voucher_detail_list</span> | 优惠券信息 | Array |  | N | 本交易支付时使用的所有优惠券信息<br/><font color="green">示例值："[{\"id\":\"20170307000730026487005X1M6V\",\"name\":\"全仓 5折优惠券\"}]"</font> |
| <span class="extend 1e760178_b5cb_4a31_942e_627e7fc95873">fund_bill_list</span> | 资金渠道 | Array |  | N | 支付成功的各个渠道金额信息。交易支付使用的资金渠道。只有在签约中指定需要返回资金明细，或者入参的query_options 中指定时才返回该字段信息。 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 买家的支付宝唯一用户号（2088开头的16位纯数字）<br/><font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| hb_fq_seller_percent | 卖家承担的手续费百分比 | String | 3 | N | 比例的百分值，<font color="green">示例值：0.9</font>，100代表100%； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a901c3a7_38ac_49ab_9afe_498becc24a9a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 券id | String | 32 | Y | <font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | <font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | 当前有三种类型：<br />ALIPAY_FIX_VOUCHER:  全场代金券<br />ALIPAY_DISCOUNT_VOUCHER:  折扣券<br />ALIPAY_ITEM_VOUCHER:  单品优惠 <br /><font color="green">示例值：ALIPAY_ITEM_VOUCHER</font></br>注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码  |
| amount | 优惠券面额 | String | 12 | Y | 优惠券面额，它应该会等于商家出资加上其他出资方出资；<br/><font color="green">示例值：10.00</font> |
| merchant_contribute | 商家出资 | String | 12 | N | 特指发起交易的商家出资金额；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 可能是支付宝，可能是品牌商，或者其他方，也可能是他们的一起出资；<font color="green">示例值：0.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1e760178_b5cb_4a31_942e_627e7fc95873-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | <font color="green">示例值：CEB</font> |
| amount | 该支付工具类型所使用的金额 | String | 32 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
| fund_channel | 交易使用的资金渠道 | String | 32 | N | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；<font color="green">示例值：ALIPAYACCOUNT</font>  |
| fund_type | 渠道所使用的资金类型 | String | 32 | N | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。<br/>DEBIT_CARD:借记卡，<br/>CREDIT_CARD:信用卡，<br/>MIXED_CARD:借贷合一卡<br/><font color="green">示例值：DEBIT_CARD</font>  |
| real_amount | 渠道实际付款金额 | String | 11 | N |  单位：元，两位小数；<font color="green">示例值：0.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ff96e4ef_65e5_4bc5_a2e4_3e4a1236c4d3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 0bf997a9_2f88_4fc3_bd3a_f9fb0314f9d3">voucher_detail_list</span> | 优惠券信息 | Array |  | N | 本交易支付时使用的所有优惠券信息<br/><font color="green">示例值："[{\"id\":\"20170307000730026487005X1M6V\",\"name\":\"全仓 5折优惠券\"}]"</font> |
| <span class="extend 45082ab6_baf5_44b3_a4f4_01d68a70558e">fund_bill_list</span> | 资金渠道 | Array |  | N | 支付成功的各个渠道金额信息。交易支付使用的资金渠道。只有在签约中指定需要返回资金明细，或者入参的query_options 中指定时才返回该字段信息。 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 买家的支付宝唯一用户号（2088开头的16位纯数字）<br/><font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| hb_fq_seller_percent | 卖家承担的手续费百分比 | String | 3 | N | 比例的百分值，<font color="green">示例值：0.9</font>，100代表100%； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0bf997a9_2f88_4fc3_bd3a_f9fb0314f9d3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 券id | String | 32 | Y | <font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | <font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | 当前有三种类型：<br />ALIPAY_FIX_VOUCHER:  全场代金券<br />ALIPAY_DISCOUNT_VOUCHER:  折扣券<br />ALIPAY_ITEM_VOUCHER:  单品优惠 <br /><font color="green">示例值：ALIPAY_ITEM_VOUCHER</font></br>注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码  |
| amount | 优惠券面额 | String | 12 | Y | 优惠券面额，它应该会等于商家出资加上其他出资方出资；<br/><font color="green">示例值：10.00</font> |
| merchant_contribute | 商家出资 | String | 12 | N | 特指发起交易的商家出资金额；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 可能是支付宝，可能是品牌商，或者其他方，也可能是他们的一起出资；<font color="green">示例值：0.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 45082ab6_baf5_44b3_a4f4_01d68a70558e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | <font color="green">示例值：CEB</font> |
| amount | 该支付工具类型所使用的金额 | String | 32 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
| fund_channel | 交易使用的资金渠道 | String | 32 | N | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；<font color="green">示例值：ALIPAYACCOUNT</font>  |
| fund_type | 渠道所使用的资金类型 | String | 32 | N | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。<br/>DEBIT_CARD:借记卡，<br/>CREDIT_CARD:信用卡，<br/>MIXED_CARD:借贷合一卡<br/><font color="green">示例值：DEBIT_CARD</font>  |
| real_amount | 渠道实际付款金额 | String | 11 | N |  单位：元，两位小数；<font color="green">示例值：0.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1d7d3d0a_c588_4ae1_8eb4_1fc64f7aedad-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| buyer_id | 买家支付宝用户号 | String | 28 | N | 买家的支付宝唯一用户号（2088开头的16位纯数字）；<br/><font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| <span class="extend bde64e3d_1834_4513_a618_214f1509918c">fund_bill_list</span> | 交易支付使用的资金渠道 | Array | 2048 | N |  |
| <span class="extend a6eedfbe_0e44_495d_aecc_de324867705c">voucher_detail_list</span> | 本交易支付时使用的所有优惠券信息 | Array | 2048 | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bde64e3d_1834_4513_a618_214f1509918c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | <font color="green">示例值：CEB</font>，请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| amount | 该支付工具类型所使用的金额 | String | 32 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
| fund_channel | 交易使用的资金渠道 | String | 32 | N | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；<font color="green">示例值：ALIPAYACCOUNT</font> |
| fund_type | 渠道所使用的资金类型 | String | 32 | N | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。<br/>DEBIT_CARD:借记卡，CREDIT_CARD:信用卡，MIXED_CARD:借贷合一卡<br/><font color="green">示例值：DEBIT_CARD</font> |
| real_amount | 渠道实际付款金额 | String | 11 | N | 单位：元，两位小数；<font color="green">示例值：2.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a6eedfbe_0e44_495d_aecc_de324867705c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| amount | 优惠券面额（元） | String | 8 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| id | 券id | String | 32 | Y | 优惠券号；<font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | 优惠名称；<font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | 当前有三种类型：<br/>ALIPAY_FIX_VOUCHER - 全场代金券,<br/>ALIPAY_DISCOUNT_VOUCHER - 折扣券,<br/>ALIPAY_ITEM_VOUCHER - 单品优惠。<br/><font color="green">示例值：ALIPAY_DISCOUNT_VOUCHER</font><br/>注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| merchant_contribute | 商家出资 | String | 12 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 单位为元；<font color="green">示例值：0.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5f8f6e70_5c3c_4fc3_9597_280eced01f2b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| qr_valid_time | 二维码有效时间 | String | 10 | N | 允许对一个订单进行支付的最长相对时间，单位为秒；<font color="green">示例值：120</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6af42ce3_fe7c_4958_8933_a28ad5e00fdb-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| qr_valid_time | 二维码有效时间 | String | 10 | N | 允许对一个订单进行支付的最长相对时间，单位为秒；<font color="green">示例值：120</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7edf1d20_21fc_4aea_9415_cce8e1064f10-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend dea266b1_198d_4e8b_b44e_e4cba63c8b64">coupon_info</span> | 银联优惠信息 | Array |  | N | 银联使用优惠活动时出现，jsonArray格式 |
| acc_no | 付款账号 | String | 40 | N | 付款方的卡号/账号/Token |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table dea266b1_198d_4e8b_b44e_e4cba63c8b64-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font> |
| type | 项目类型 | String | 4 | Y | DD01：随机立减<br>CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券<br>CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券<br><font color="green">示例值：DD01</font>  |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 044b6ea1_577c_448c_b9b8_e7feda377775-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 99c22a6a_33dd_4aff_9ab8_5a684fd5e025">combinedpay_data</span> | 补贴支付信息	 | String |  | N | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| <span class="extend 28866e50_6645_4df2_9964_b1f531b85b63">combinedpay_data_fee_info</span> | 补贴支付手续费承担方信息 | String |  | N | jsonObject字符串 |
| <span class="extend dfeb340b_4716_477c_b1c9_dc79b4fc24d2">trans_fee_allowance_info</span> | 手续费补贴信息 | String |  | N | 手续费补贴信息对象，jsonObject字符串 |
| <span class="extend 9788fc1a_d209_43a0_8382_d72e50447c63">terminal_device_data</span> | 设备信息 | String | 128 | N | 设备信息，jsonObject字符串； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 99c22a6a_33dd_4aff_9ab8_5a684fd5e025-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴方汇付商户号 | String | 32 | N | 补贴方汇付ID；<font color="green">示例值：6666000123123123</font> |
| user_type | 补贴方类型 | String | 32 | N | channel-渠道，merchant-总部商户，agent-代理，mertomer-商户；<font color="green">示例值：channel</font> |
| acct_id | 补贴方账户号 | String | 32 | N | 营销补贴方账户号；<font color="green">示例值：F00900982</font> |
| amount | 补贴金额 | String | 14 | N | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 28866e50_6645_4df2_9964_b1f531b85b63-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴支付手续费承担方汇付编号 | String | 32 | N | <font color="green">示例值：6666000123120001</font> |
| acct_id | 补贴支付手续费承担方账户号 | String | 32 | N | 补贴支付手续费承担方账户号；<font color="green">示例值：F00598610</font> |
| combinedpay_fee_amt | 补贴支付手续费金额 | String | 14 | N | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table dfeb340b_4716_477c_b1c9_dc79b4fc24d2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_fee_amt | 商户应收手续费 | String | 16 | N |  <font color="green">示例值：5.00</font> |
| actual_fee_amt | 商户实收手续费 | String | 16 | N | <font color="green">示例值：4.00</font> |
| allowance_fee_amt | 补贴手续费 | String | 16 | N | <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9788fc1a_d209_43a0_8382_d72e50447c63-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| terminal_ip | 交易设备IP | String | 64 | N | 绑卡设备（付款 APP） 所在的公网IP，可用于定位所属地区，不是 wifi 连接时的局域网 IP。<br/>局域网 IP 包括：<br/>A 类： 10.0.0.0-10.255.255.255<br/>B 类： 172.16.0.0-172.31.255.255<br/>C 类： 192.168.0.0-192.168.255.255<br/><font color="green">示例值：192.168.0.0</font> |
| terminal_location | 终端实时经纬度信息 | String | 32 | N | 设备（付款APP）GPS位置,格式为纬度/经度，+表示北纬、东经，-表示南纬、西经。<br/>经度整数位不超过3位，小数位不超过5位；纬度整数位不超过2位，小数位不超过6位。<br/><font color="green">示例值：+37.12/-121.213</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ba6f0baf_e65b_4233_9c72_5a2e18737588-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_huifu_id | 手续费商户号	 | String | 32 | N | <font color="green">示例值：6666000123120001</font> |
| fee_flag | 手续费扣款标志 | String | 1 | N | 1: 外扣，2: 内扣；<font color="green">示例值：1</font> |
| <span class="extend b8cd54b8_82a8_479b_bd3a_b291f85e22ce">fee_formula_infos</span> | 手续费费率信息 | Array |  | N | jsonArray格式；交易成功时返回手续费费率信息 |
| fee_amount | 手续费金额 | String | 14 | N | 单位元，需保留小数点后两位，同步成功时返回；<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b8cd54b8_82a8_479b_bd3a_b291f85e22ce-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | N | <font color="green">示例值：AMT\*0.003</font> |
| fee_type | 手续费类型 | String | 32 | N | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费<br/><font color="green">示例值：ACCT_FEE</font> |
| huifu_id | 商户号 | String | 32 | N | 组合支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
<!-- extend:end -->


##### 返回示例

###### 成功报文
```json
{
    "data": {
        "acct_id": "F22000000",
        "acct_stat": "I",
        "atu_sub_mer_id": "888000000",
        "bank_code": "SUCCESS",
        "bank_message": "支付成功",
        "debit_type": "2",
        "delay_acct_flag": "N",
        "end_time": "20260528091807",
        "hf_seq_id": "002900TOP2B260528091804P00000039d5300000",
        "huifu_id": "6666000000000767",
        "method_expand": "{\"bank_type\":\"KLB\",\"cash_fee\":\"41.20\",\"coupon_fee\":\"0.00\",\"openid\":\"o8jhot-0000000I33VJ_ZVDMxofv4\",\"sub_openid\":\"oGhiSxP3000000VnZ1JOSct5wAio\"}",
        "out_trans_id": "4200003030202605000000807603",
        "party_order_id": "03212605283348473210036",
        "payment_fee": "{\"fee_amount\":\"0.12\",\"fee_flag\":2,\"fee_formula_infos\":[{\"fee_formula\":\"AMT*0.0029\",\"fee_type\":\"TRANS_FEE\"}],\"fee_huifu_id\":\"6666000000000767\"}",
        "req_date": "20260528",
        "req_seq_id": "PRO00000-0",
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "settlement_amt": "41.20",
        "trade_type": "T_MICROPAY",
        "trans_amt": "41.20",
        "trans_stat": "S",
        "unconfirm_amt": "41.08"
    }
}
```


#### 聚合正扫异步返回参数

异步返回报文有两种不同的类型：间联模式与直联模式。如果商户业务开通时做了微信直连配置（wx_zl_conf），则属于直联模式，否则就是间联模式。 


* 公共返回参数

| 参数              | 中文名                 | 定义   | 长度 | 必填 | 说明                                                         |
| :---------------- | :--------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| resp_code         | 网关返回码             | String | 8    | Y    | <font color="green">示例值：00000000</font>  |
| resp_desc         | 网关返回信息           | String | 512  | Y    | <font color="green">示例值：交易成功[000]</font>  |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| resp_data | 返回业务数据       | String |        | Y    | jsonObject |

* 参数（resp_data）


| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码) |
| resp_desc | 业务响应信息 | String | 256 | Y | [业务返回描述](#业务返回码) |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 交易时传入，原样返回；<font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date | 请求日期 | String | 8 | Y | 交易时传入，原样返回；<font color="green">示例值：20220905</font> |
| trans_type | 交易类型 | String | 16 | N |  T_JSAPI:  微信公众号支付<br/>T_MINIAPP:  微信小程序支付  <br/>A_JSAPI:  支付宝JS  <br/>A_NATIVE:  支付宝正扫  <br/>U_NATIVE:  银联正扫  <br/>U_JSAPI:  银联 JS  <br/>D_NATIVE:  数字人民币正扫  <br/>T_H5：微信直连H5支付<br/>T_APP：微信APP支付<br/><font color="green">示例值：T_JSAPI</font> |
| hf_seq_id | 全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A221019132207P068ac1362af00000</font> |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | <font color="green">示例值：092021091922001451301445517582</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N |  <font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| trans_amt | 交易金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| pay_amt | 消费者实付金额 | String | 14 | N | 单位元， <font color="green">示例值：1.00</font> |
| settlement_amt | 结算金额(元)  | String | 16 | N | 实际应结金额(订单金额扣除优惠金额后的值)，保留小数点后两位，<font color="green">示例值：1000.00</font> |
| end_time | 支付完成时间 | String | 14 | N | 格式yyyyMMddHHmmss，<font color="green">示例值：20091225091010</font> |
| acct_date | 入账时间 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| trans_stat | 交易状态 | String | 1 | N | S：成功、F：失败，交易状态以此字段为准。<font color="green">示例值：S</font> |
| fee_flag | 手续费扣款标志 | Integer | 1 | N | 1:  外扣，2:  内扣；<font color="green">示例值：2</font> |
| <span class="extend 738186ac_df6e_45b4_bf3c_98f0293e73d0">fee_formula_infos</span> | 手续费费率信息 | Array |  | N | 交易成功时返回手续费费率信息 |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，保留小数点后两位，<font color="green">示例值：1.00</font> |
| <span class="extend 8fe60866_e706_4d31_933a_d84b86d09b39">trans_fee_allowance_info</span> | 手续费补贴信息 | Object |  | N | Json格式；参加银行补贴手续费 |
| <span class="extend f949e8b7_924e_4820_b93a_199ea6b9d3ec">combinedpay_data</span> | 补贴支付信息 | String |  | N | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| <span class="extend ecb16559_82e3_4673_9161_3b69c2bbe7f2">combinedpay_data_fee_info</span> | 补贴支付手续费信息 | String |  | N | jsonObject字符串 |
| debit_type | 借贷记标识 | String | 1 | N | D-借记卡，C-贷记卡，0-其他；<font color="green">示例值：D</font> |
| is_div | 是否分账交易 | String | 1 | Y | 1:分账交易， 0:非分账交易；<font color="green">示例值：1</font> |
| <span class="extend 5416df41_b701_4e17_b2b0_c7df7cac21a0">acct_split_bunch</span> | 分账对象 | Object |  | N | jsonObject字符串 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | 1:延迟， 0:非延迟；<font color="green">示例值：1</font>  |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | <font color="green">示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk=</font>；<!--259号文新增字段--> |
| <span class="extend f6c872ae_62b2_44c0_a6cd_08ce6c7530d1">wx_response</span> | 微信返回的响应报文 | Object |  | N | jsonObject字符串 |
| <span class="extend 9e55e59c_c374_428c_88b1_e870708986f0">alipay_response</span> | 支付宝返回的响应报文 | Object |  | N | jsonObject字符串 |
| <span class="extend 54d2d3ae_dd96_4a69_9c03_e04389964548">dc_response</span> | 数字货币返回的响应报文 | Object |  | N | jsonObject字符串 |
| <span class="extend a76b7ffb_e83a_490c_87ba_c8cb6c468ad4">unionpay_response</span> | 银联返回的响应报文 | Object |  | N | jsonObject字符串 |
| device_type | 终端类型 | String | 2 | N | 01-智能POS<br>02-扫码POS<br>03-云音箱<br>04-台牌<br>05-云打印<br>06-扫脸设备<br>07-收银机<br>08-收银助手<br>09-传统POS<br>10-一体音箱<br>11-虚拟终端<br/><font color="green">示例值：01</font> |
| <span class="extend dcf3e210_b598_460f_bdd1_fff3ac5e6f30">mer_dev_location</span> | 商户终端定位 | Object |  | N |  商户终端定位信息，jsonObject字符串；<!--259号文新增字段--> |
| bank_message | 通道返回描述 | String | 200 | N | <font color="green">示例值：成功[0000000]</font> |
| remark | 备注 | String | 255 | N | 原样返回；<font color="green">示例值：备注</font> |
| fq_channels | 分期资产方式 | String | 20 | N | 花呗分期功能，代表优先使用的资产类型；alipayfq_cc：表示信⽤卡分期。<br/><font color="green">示例值：alipayfq_cc</font> |
| notify_type | 通知类型 | Integer | 1 | N | 1：通道通知，2：账务通知；<font color="green">示例值：1</font> |
| <span class="extend e38a5599_65a4_434c_80ed_1d270893dfd1">split_fee_info</span> | 分账手续费信息 | Object |  | N | 分账手续费信息 |
| atu_sub_mer_id | ATU真实商户号 | String | 32 | N |  <font color="green">示例值：411111141</font> |
| devs_id | 汇付终端号 | String | 32 | N | 使用汇付机具交易时返回；<font color="green">示例值：660035730311200000</font> |
| fund_freeze_stat | 资金冻结状态 | String | 16 | N | FREEZE：冻结；UNFREEZE：解冻；<font color="green">示例值：UNFREEZE</font> |

<!-- extend:start -->
<!-- div:extend-table 738186ac_df6e_45b4_bf3c_98f0293e73d0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | Y |   <font color="green">示例值：AMT\*0.003</font>  |
| fee_type | 手续费类型 | String | 32 | Y |  TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费<br/><font color="green">示例值：ACCT_FEE</font>  |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8fe60866_e706_4d31_933a_d84b86d09b39-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y |  <font color="green">示例值：5.00</font> |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| allowance_type | 补贴类型 | String | 10 | N | 0：不补贴，为空默认<br/>1：补贴<br/>2：部分补贴<br/>3：全额补贴(优惠后)<br/>4：部分补贴(优惠后)<br/><font color="green">示例值：2</font> |
| no_allowance_desc | 不补贴原因 | String | 128 | N | 1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴<br/>2:额度用完<br/>3:不在有效期<br/>4:活动不存在<br/>5:手续费金额为0不补贴<br/>6:顶格优惠<br/>7:额度不足<br/>8:手续费后补<br/>9:未达到起始补贴金额<br/><font color="green">示例值：2</font> |
| <span class="extend 97dcdd7f_b90b_4346_a012_00fad924a6fd">cur_allowance_config_infos</span> | 手续费补贴活动详情 | Object |  | N | 补贴系统返回，斗拱原样返回； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 97dcdd7f_b90b_4346_a012_00fad924a6fd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_id | 门店 | String | 64 | N | <font color="green">示例值：sh002</font> |
| merchant_group | 商户号 | String | 64 | N | <font color="green">示例值：6666000123120000</font> |
| allowance_sys | 补贴方	 | String | 64 | Y | 1:银行  2:服务商 3:汇来米；<font color="green">示例值：1</font> |
| allowance_sys_id | 补贴方ID | String | 64 | Y | 对应补贴方的id；<font color="green">示例值：6666000123120000</font> |
| is_delay_allowance | 补贴类型 | String | 2 | Y |  1:实补,2:后补,默认实补；<font color="green">示例值：1 |
| market_id | 自定义活动编号 | String | 64 | Y |  <font color="green">示例值：ISFE00232</font> |
| market_name | 自定义活动名称 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| market_desc | 自定义活动描述 | String | 64 | N | <font color="green">示例值：新店开业大促</font> |
| start_time | 活动开始时间 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220909</font> |
| end_time | 活动结束时间 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220911</font> |
| pos_debit_limit_amt | pos借记卡补贴额度 | String | 16 | Y | <font color="green">示例值：2.00</font> |
| pos_credit_limit_amt | pos贷记卡补贴额度 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| pos_limit_amt | pos补贴额度 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| qr_limit_amt | 扫码补贴额度 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| total_limit_amt | 活动总补贴额度 | String | 16 | Y | <font color="green">示例值：10.00</font> |
| status | 活动是否有效 | String | 4 | Y | 1:生效 0：失效；<font color="green">示例值：1</font> |
| human_flag | 是否人工操作 | String | 4 | Y | N：自动 Y：人工；<font color="green">示例值：Y</font> |
| activity_id | 活动号 | String | 64 | Y |  <font color="green">示例值：223402342</font> |
| activity_name | 活动描述 | String | 128 | N |  <font color="green">示例值：开业大促</font> |
| create_by | 创建人 | String | 32 | Y | <font color="green">示例值：Lg2022022201394910571</font> |
| create_time | 创建时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 22:00:30</font> |
| update_time | 更新时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 23:00:30</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f949e8b7_924e_4820_b93a_199ea6b9d3ec-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴方汇付商户号 | String | 32 | Y | 补贴方汇付ID；<font color="green">示例值：6666000123123123</font> |
| user_type | 补贴方类型 | String | 32 | Y | 补贴方类型：channel-渠道，agent-代理；<font color="green">示例值：agent</font> |
| acct_id | 补贴方账户号 | String | 32 | Y | 营销补贴方账户号；<font color="green">示例值：F00900982</font> |
| amount | 补贴金额 | String | 14 | Y | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ecb16559_82e3_4673_9161_3b69c2bbe7f2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴支付手续费承担方汇付编号 | String | 32 | Y | 补贴支付手续费承担方汇付编号；<font color="green">示例值：6666000123123123</font> |
| acct_id | 补贴支付手续费承担方账户号 | String | 32 | Y | 补贴支付手续费承担方账户号；<font color="green">示例值：F00900982</font> |
| combinedpay_fee_amt | 补贴支付手续费金额 | String | 14 | Y | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5416df41_b701_4e17_b2b0_c7df7cac21a0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend f78b2cef_4ce3_47c6_a97f_45896c6a54b2">acct_infos</span> | 分账明细 | Array |  | Y | jsonArray分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f78b2cef_4ce3_47c6_a97f_45896c6a54b2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120001</font> |
| acct_date | 账务日期 | String | 8 | N | <font color="green">示例值：20220909</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f6c872ae_62b2_44c0_a6cd_08ce6c7530d1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N |  微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；<font color="green">示例值：OTHERS</font> |
| cash_fee | 现金支付金额	 | String | 100 | N | 现金支付金额订单现金支付金额；<font color="green">示例值：10.00</font> |
| coupon_fee | 代金券金额 | String | 100 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：0.10</font> |
| attach | 商家数据包 | String | 128 | N | 商家数据包，原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend 0172ec99_d1ea_4de2_9507_172b1e75d8b8">promotion_detail</span> | 营销详情列表 | Array |  | N | 营销详情列表，使返回值为Json格式； |
| sub_mch_id | 子商户号 | String |  | N | 微信支付分配的子商户号；直联模式返回字段；<font color="green">示例值：1632157057</font> |
| device_info | 设备号 | String |  | N | 调用接口提交的终端设备号；直联模式返回字段；<font color="green">示例值：SP003pcf</font> |
| is_subscribe | 是否关注公众账号 | String |  | N | 用户是否关注公众账号，直联模式返回字段；Y-关注，N-未关注（机构商户不返回）；<font color="green">示例值：Y</font>  |
| sub_is_subscribe | 是否关注子公众账号 | String |  | N | 用户是否关注子公众账号，直联模式返回字段；Y-关注，N-未关注（机构商户不返回）；<font color="green">示例值：Y</font>  |
| fee_type | 现金支付货币类型 | String |  | N |  符合ISO 4217标准的三位字母代码，默认人民币：CNY；直联模式返回字段；<font color="green">示例值：CNY</font>     |
| coupon_count | 代金券使用数量 | String |  | N | 直联模式返回字段；<font color="green">示例值：1</font>  <br/>使用单品优惠时不再返回coupon_count，参数promotion_detail会返回每张券的具体信息，<br/>商户可以通过解析promotion_detail参数来确认使用了几张代金券。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0172ec99_d1ea_4de2_9507_172b1e75d8b8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| promotion_id | 券id | String | 32 | Y | 券或者立减优惠id；<font color="green">示例值：2345234235</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL: 全场代金券，SINGLE: 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON:  代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT:  优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font>  |
| amount | 优惠券面额 | String | 12 | Y | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）<font color="green">示例值：5.00</font> |
| activity_id | 活动ID | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| merchant_contribute | 商户出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；<br/><font color="green">示例值：10.00</font> |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方出资金额=商家出资+微信出资，单位为元；<font color="green">示例值：20.00</font> |
| <span class="extend 8d4fe743_75bd_4622_af3d_4436ac8c84fd">goods_detail</span> | 单品列表 | Array |  | N | 单品信息，使用Json格式，是promotion_detail的元素； |
| wxpay_contribute | 微信出资 | String | 32 | N | 特指由微信支付商户平台创建的优惠，单位：元；<font color="green">示例值：20.00</font> |
| original_other_contribute | 微信交易其他出资方出资金额 | String | 32 | N | 微信的其他出资方出资金额，单位：元；<font color="green">示例值：20.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8d4fe743_75bd_4622_af3d_4436ac8c84fd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码	 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格 | String | 32 | Y | 单位为:元。<font color="green">示例值：99.00</font>；如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，<br/>则活动商品的单价应为原单价-50元 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9e55e59c_c374_428c_88b1_e870708986f0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 6bf18f9b_de71_4545_aecb_03026d89867b">voucher_detail_list</span> | 优惠券信息 | Array |  | N | 本交易支付时使用的所有优惠券信息<br/><font color="green">示例值："[{\"id\":\"20170307000730026487005X1M6V\",\"name\":\"全仓 5折优惠券\"}]"</font> |
| <span class="extend e3a4b2c4_7c88_4eb7_8e02_9791c7b132fd">fund_bill_list</span> | 资金渠道 | Array |  | N | 支付成功的各个渠道金额信息。交易支付使用的资金渠道。只有在签约中指定需要返回资金明细，或者入参的query_options 中指定时才返回该字段信息。 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 买家的支付宝唯一用户号（2088开头的16位纯数字）<br>示例值：20880414938706770000 |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| hb_fq_seller_percent | 卖家承担的手续费百分比 | String | 3 | N | 比例的百分值，<font color="green">示例值：0.9</font>，传入100代表100%； |
| notify_time | 通知时间 | String |  | N | 直连模式字段；通知的发送时间。格式为Date格式，yyyy-MM-dd HH&#58;mm&#58;ss；<font color="green">示例值2022-10-11 10&#58;12&#58;24</font> |
| app_id | 支付宝应用app_id | String | 32 | N | 直连模式字段；支付宝分配给开发者的应用Id；<font color="green">示例值：2021002122659346</font>  |
| out_biz_no | 商户业务号 | String | 64 | N | 直连模式字段；商户业务ID，主要是退款通知中返回退款申请的流水号；<font color="green">示例值：</font>  |
| invoice_amount | 开票金额 | String | 11 | N | 直连模式字段；用户在交易中支付的可开发票的金额；<font color="green">示例值：100.00</font> |
| buyer_pay_amount | 付款金额 | String | 13 | N | 直连模式字段；用户在交易中支付的金额；<font color="green">示例值：100.00</font>   |
| subject | 订单标题 | String | 256 | N | 直连模式字段；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；<font color="green">示例值：红果奶茶</font>  |
| body | 商品描述 | String | 128 | N | 直连模式字段；该订单的备注、描述、明细等。对应请求时的body参数，<br>原样通知回来；<font color="green">示例值：中杯</font> |
| gmt_create | 交易创建时间 | String | 64 | N | 直连模式字段；该笔交易创建的时间。格式为yyyy-MM-dd HH&#58;mm&#58;ss；<font color="green">示例值2022-10-11 10&#58;12&#58;24</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6bf18f9b_de71_4545_aecb_03026d89867b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 券id | String | 32 | Y | <font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | <font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | 当前有三种类型：<br />ALIPAY_FIX_VOUCHER:  全场代金券<br />ALIPAY_DISCOUNT_VOUCHER:  折扣券<br />ALIPAY_ITEM_VOUCHER:  单品优惠 <br /><font color="green">示例值：ALIPAY_ITEM_VOUCHER</font></br>注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码  |
| amount | 优惠券面额 | String | 12 | Y | 优惠券面额，它应该会等于商家出资加上其他出资方出资；<br/><font color="green">示例值：10.00</font> |
| merchant_contribute | 商家出资 | String | 12 | N | 特指发起交易的商家出资金额；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 可能是支付宝，可能是品牌商，或者其他方，也可能是他们的一起出资；<font color="green">示例值：0.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e3a4b2c4_7c88_4eb7_8e02_9791c7b132fd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | <font color="green">示例值：CEB</font> |
| amount | 该支付工具类型所使用的金额 | String | 32 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
| fund_channel | 交易使用的资金渠道 | String | 32 | N | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；<font color="green">示例值：ALIPAYACCOUNT</font>  |
| fund_type | 渠道所使用的资金类型 | String | 32 | N | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。<br/>DEBIT_CARD:借记卡，<br/>CREDIT_CARD:信用卡，<br/>MIXED_CARD:借贷合一卡<br/><font color="green">示例值：DEBIT_CARD</font>  |
| real_amount | 渠道实际付款金额 | String | 11 | N |  单位：元，两位小数；<font color="green">示例值：0.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 54d2d3ae_dd96_4a69_9c03_e04389964548-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| merchant_id | 商户号 | String | 35 | N | 数字货币:  工行；<font color="green">示例值：S5088295305</font> |
| term_id | 终端号 | String | 32 | N | 数字货币:  工行；<font color="green">示例值：58000001</font> |
| trade_type | 交易类型 | String | 16 | N | 数字货币:  工行；<font color="green">示例值：SCANPAY</font> |
| custom_bank_code | 客户所属运营机构代码 | String | 14 | N | 数字货币:  工行；<font color="green">示例值：</font> |
| custom_bank_name | 客户所属运营机构名称 | String | 70 | N | 数字货币:  工行；<font color="green">示例值：</font> |
| openid | 用户标识 | String | 64 | N | 数字货币:  工行；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 用户子标识 | String | 64 | N | 数字货币:  工行；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| coupon_amount | 代金券金额 | String | 14 | N | 数字货币:  工行;单位：元；<font color="green">示例值：0.01</font> |
| coupon_count | 代金券数量 | String | 3 | N | 数字货币:  工行；<font color="green">示例值：1</font> |
| <span class="extend 8ad5ef59_1d1f_454b_9609_fb9ddeed8754">coupon_list</span> | 代金券集合 | Array |  | N | 数字货币:  工行；<font color="green">示例值：[{"coupon_type":"5","coupon_id":"2020060702001","coupon_amount":"50.00"}]</font> |
| creditorWalletName | 收款钱包名称 | String | 60 | N | 数字货币:  邮储；<font color="green">示例值：上海汇涵信息科技服务有限公司</font> |
| creditorWalletId | 收款钱包ID | String | 68 | N | 数字货币:  邮储；<font color="green">示例值：002250******5081</font> |
| creditorWalletType | 收款钱包类型 | String | 4 | N | 数字货币:  邮储   <br />收款钱包类型   <br />WT01:  个人钱包   <br />WT02:  子个人钱包   <br />WT09:  对公钱包   <br />WT10:  子对公钱包<br/><font color="green">示例值：WT09</font> |
| creditorWalletLevel | 收款钱包等级 | String | 4 | N | 数字货币:  邮储   <br />收款钱包等级   <br />WL01:  一类钱包   <br />WL02:  二类钱包   <br />WL03:  三类钱包   <br />WL04:  四类钱包<br/><font color="green">示例值：WL01</font>  |
| debtorWalletName | 付款钱包名称 | String | 60 | N | 数字货币:  邮储；<font color="green">示例值：我的钱包</font> |
| debtorWalletId | 付款钱包ID | String | 68 | N | 数字货币:  邮储；<font color="green">示例值：004100******0032</font> |
| debtorWalletType | 付款钱包类型 | String | 4 | N | 数字货币:  邮储   <br />付款钱包类型   <br />WT01:  个人钱包   <br />WT02:  子个人钱包   <br />WT09:  对公钱包   <br />WT10:  子对公钱包<br/><font color="green">示例值：WT01</font>  |
| debtorWalletLevel | 付款钱包等级 | String | 4 | N | 数字货币:  邮储   <br />付款钱包等级   <br />WL01:  一类钱包   <br />WL02:  二类钱包   <br />WL03:  三类钱包   <br />WL04:  四类钱包<br/><font color="green">示例值：WL02</font> |
| debtorPartyIdentification | 付款运营机构 | String | 14 | N | 数字货币:  邮储；<font color="green">示例值：</font> |
| businessType | 支付类型 | String | 1 | N | 数字货币:  邮储；支付类型：O-本贷他，I-本贷本；<font color="green">示例值：O</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8ad5ef59_1d1f_454b_9609_fb9ddeed8754-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| coupon_id | 代金券ID | String | 40 | N |  <font color="green">示例值：2020060702001</font> |
| coupon_type | 代金券类型 | String | 8 | N |  <font color="green">示例值：5</font> |
| coupon_amount | 单个代金券支付金额 | String | 14 | N | 单个代金券支付金额，单位：元；<font color="green">示例值：50.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a76b7ffb_e83a_490c_87ba_c8cb6c468ad4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 6a3c0e76_a4e6_455e_84d2_ec25fde6f644">coupon_info</span> | 银联优惠信息 | Array |  | N | 银联使用优惠活动时出现，jsonArray格式  |
| acc_no | 付款账号 | String | 40 | N | 付款方的卡号/账号/Token |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6a3c0e76_a4e6_455e_84d2_ec25fde6f644-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font>   |
| type | 项目类型 | String | 4 | Y | DD01：随机立减<br>CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券<br>CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券<br><font color="green">示例值：DD01</font>  |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table dcf3e210_b598_460f_bdd1_fff3ac5e6f30-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| terminal_ip | 交易设备IP | String | 64 | N | 绑卡设备（付款 APP） 所在的公网IP，可用于定位所属地区，不是 wifi 连接时的局域网 IP。<br/>局域网 IP 包括：<br/>A 类： 10.0.0.0-10.255.255.255<br/>B 类： 172.16.0.0-172.31.255.255<br/>C 类： 192.168.0.0-192.168.255.255<br/><font color="green">示例值：172.3.46.44</font> |
| terminal_location | 终端实时经纬度信息 | String | 32 | N | 设备（付款APP）GPS位置,格式为纬度/经度，+表示北纬、东经，-表示南纬、西经。<br/><font color="green">示例值：+37.12/-121.213</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e38a5599_65a4_434c_80ed_1d270893dfd1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| total_split_fee_amt | 分账手续费总金额(元) | String | 14 | N |  <font color="green">示例值：0.10</font>   |
| split_fee_flag | 分账手续费扣款标志 | Integer | 1 | Y | 1: 外扣 2: 内扣；<font color="green">示例值：2</font> |
| <span class="extend c5297222_ec62_46e0_afea_c51b65ebcfbc">split_fee_details</span> | 分账手续费信息 | Array |  | Y | 分账手续费信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c5297222_ec62_46e0_afea_c51b65ebcfbc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| split_fee_amt | 分账手续费金额(元) | String | 14 | Y |  <font color="green">示例值：0.10</font>  |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font>  |
| split_fee_acct_id | 分账手续费承担方账号 | String | 32 | N | <font color="green">示例值：F00598600</font>  |
<!-- extend:end -->


#### 聚合正扫解冻异步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/smzf/api_jhfs?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81) |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/smzf/api_jhfs?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)  |
| hf_seq_id | 交易的汇付全局流水号 | String | 40 | Y | <font color="green">示例值：00470topo1A221019132207P068ac1362af00000</font>  |
| req_seq_id | 交易请求流水号 | String | 128 | Y | 交易时传入，原样返回；<font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date | 交易请求日期 | String | 8 | Y | 交易时传入，原样返回,格式为yyyyMMdd，<font color="green">示例值：20091225</font>  |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123120000</font>  |
| notify_type | 通知类型 | Integer | 1 | Y | 3：资金解冻通知；<font color="green">示例值：3</font>  |
| fund_freeze_stat | 资金冻结状态 | String | 16 | Y | UNFREEZE：解冻；<font color="green">示例值：UNFREEZE</font> |
| unfreeze_amt | 解冻金额 | String | 14 | Y | 单元：元。<font color="green">示例值：1.23</font> |
| freeze_time | 冻结时间 | String | 14 | Y | 格式为yyyyMMddHHMMSS，<font color="green">示例值：20091225091010</font>   |
| unfreeze_time | 解冻时间 | String | 14 | Y |  格式为yyyyMMddHHMMSS，<font color="green">示例值：20091225091010</font>   |


#### 聚合正扫业务返回码


| <div style="width: 60pt">返回码</div>     | 返回描述                                                     |
| :------- | :----------------------------------------------------------- |
| 00000000 | 交易受理成功；注：**交易状态以trans_stat为准；**                                                     |
| 00000100 | 下单成功                                                     |
| 10000000 | 产品号不能为空                                               |
| 10000000 | **交易类型不能为空**                                             |
| 10000000 | %s不能为空（%s代指报错参数名）                               |
| 10000000 | %s长度固定%d位（%s代指报错参数名、%d代指字段长度）           |
| 10000000 | %s最大长度为%d位（%s代指报错参数名、%d代指字段长度）         |
| 10000000 | %s的传入枚举[%s]不存在（%s代指报错参数名）                   |
| 10000000 | %s不符合%s格式（%s代指报错参数名）。如：交易金额不符合金额格式  |
| 10000000 | 订单已超时                                                   |
| 20000000 | **重复交易**                                                     |
| 21000000 | 手续费金额、手续费收取方式、手续费扣款标识、手续费子客户号、手续费账户号，必须同时为空或同时必填 |
| 22000000 | 产品号不存在                                                 |
| 22000000 | 产品号状态异常                                               |
| 22000002 | 商户信息不存在                                               |
| 22000002 | 商户状态异常                                                 |
| 22000003 | 延迟账户不存在                                               |
| 22000003 | 商户账户信息不存在                                           |
| 22000004 | 暂未开通分账权限                                             |
| 22000004 | 暂未开通%s权限（%s代指报错参数名）                           |
| 22000004 | 暂未开通延迟入账权限                                         |
| 22000005 | 手续费承担方必须参与分账                                     |
| 22000005 | 分账列表必须包含主交易账户                                   |
| 22000005 | 其他商户分账比例过高                                         |
| 22000005 | 商户入驻信息配置有误(多通道)                                 |
| 22000005 | 商户分期贴息未激活                                           |
| 22000005 | 分期交易不能重复激活                                         |
| 22000005 | 手续费配置有误                                               |
| 22000005 | 商户贴息信息未配置                                           |
| 22000005 | 花呗分期费率配置有误                                         |
| 22000005 | 分账配置有误                                                 |
| 22000005 | 分账配置未包含手续费承担方                                   |
| 22000005 | 商户入驻配置信息有误                                         |
| 22000005 | 商户支付宝/微信入驻信息配置有误                              |
| 22000005 | 商户银联入驻信息配置有误                                     |
| 22000005 | 商户贴息分期费率未配置渠道号                                 |
| 22000005 | 商户贴息分期费率未配置费率类型                               |
| 22000005 | 商户贴息分期费率配置有误                                     |
| 22000005 | 手续费费率未配置                                             |
| 22000005 | 手续费计算错误                                               |
| 22000005 | 商户贴息信息配置有误                                         |
| 22000005 | 商户未报名活动或活动已过期                                   |
| 22000005 | 数字货币手续费费率未配置                                     |
| 22000005 | 数字货币手续费配置有误                                       |
| 22000005 | 商户未配置默认入驻信息（多通道）                             |
| 23000003 | 交易金额不足以支付内扣手续费                                 |
| 23000003 | 优惠金额大于交易金额                                         |
| 23000004 | 交易类型不支持                                               |
| 23000004 | 当前交易类型不支持商户贴息                                   |
| 90000000 | 业务执行失败；如：**账户可用余额不足**|
| 90000000 | **该功能已关闭，请联系客服**|
| 90000000 | **交易失败，单日金额超限，请联系额服提额**|
| 90000000 | 交易存在风险                                                 |
| 91111119 | 通道异常，请稍后重试                            |
| 98888888 | 系统错误                            |



#### 聚合反扫异步返回参数

异步返回报文有两种不同的类型：间联模式与直联模式。如果商户业务开通时做了微信直连配置（wx_zl_conf），则属于直联模式，否则就是间联模式。

* 公共返回参数

| 参数              | 中文名                 | 定义   | 长度 | 必填 | 说明                                                         |
| :---------------- | :--------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| resp_code         | 网关返回码             | String | 8    | Y    | <font color="green">示例值：00000000</font>  |
| resp_desc         | 网关返回信息           | String | 512  | Y    | <font color="green">示例值：交易成功[000]</font>  |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| resp_data | 返回业务数据       | String |        | Y    | jsonObject |

* 参数（resp_data）


| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码) |
| resp_desc | 业务响应信息 | String | 256 | Y | [业务返回描述](#业务返回码) |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 交易时传入，原样返回；<font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date | 请求日期 | String | 8 | Y | 交易时传入，原样返回；<font color="green">示例值：20220905</font> |
| trans_type | 交易类型 | String | 16 | N |  T_MICROPAY:  微信反扫<br/>A_MICROPAY:  支付宝反扫  <br/>U_MICROPAY:  银联二维码反扫  <br/>D_MICROPAY:  数字人民币反扫  <br/><font color="green">示例值：T_MICROPAY</font> |
| hf_seq_id | 全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A221019132207P068ac1362af00000</font> |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | <font color="green">示例值：092021091922001451301445517582</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N |  <font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| trans_amt | 交易金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| pay_amt | 消费者实付金额 | String | 14 | N | 单位元， <font color="green">示例值：1.00</font> |
| settlement_amt | 结算金额(元)  | String | 16 | N | 实际应结金额(订单金额扣除优惠金额后的值)，保留小数点后两位，<font color="green">示例值：1000.00</font> |
| end_time | 支付完成时间 | String | 14 | N | 格式yyyyMMddHHmmss，<font color="green">示例值：20091225091010</font> |
| acct_date | 入账时间 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| trans_stat | 交易状态 | String | 1 | N | S：成功、F：失败，交易状态以此字段为准。<font color="green">示例值：S</font> |
| fee_flag | 手续费扣款标志 | Integer | 1 | N | 1:  外扣，2:  内扣；<font color="green">示例值：2</font> |
| <span class="extend 19c1b34f_76df_4fc9_bc35_e19061b970a5">fee_formula_infos</span> | 手续费费率信息 | Array |  | N | 交易成功时返回手续费费率信息 |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，保留小数点后两位，<font color="green">示例值：1.00</font> |
| <span class="extend 40ba46b4_c80e_4c4e_a42d_dc1c232820f9">trans_fee_allowance_info</span> | 手续费补贴信息 | Object |  | N | Json格式；参加银行补贴手续费 |
| <span class="extend a22aa4f4_7e41_4091_a3f9_95388a736622">combinedpay_data</span> | 补贴支付信息 | String |  | N | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| <span class="extend f83eb0be_3c3c_4e28_82db_5a48dd0078bf">combinedpay_data_fee_info</span> | 补贴支付手续费信息 | String |  | N | jsonObject字符串 |
| debit_type | 借贷记标识 | String | 1 | N | D-借记卡，C-贷记卡，0-其他；<font color="green">示例值：D</font> |
| is_div | 是否分账交易 | String | 1 | Y | 1:分账交易， 0:非分账交易；<font color="green">示例值：1</font> |
| <span class="extend aa0964fd_46e8_4a66_8638_01af287f34d8">acct_split_bunch</span> | 分账对象 | Object |  | N | jsonObject字符串 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | 1:延迟， 0:非延迟；<font color="green">示例值：1</font>  |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | <font color="green">示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk=</font>；<!--259号文新增字段--> |
| <span class="extend 169f6b54_75c3_45ee_a99a_d41b4eb6f984">wx_response</span> | 微信返回的响应报文 | Object |  | N | jsonObject字符串 |
| <span class="extend 3a38387b_86fa_4f44_af53_e8edb0289f7b">alipay_response</span> | 支付宝返回的响应报文 | Object |  | N | jsonObject字符串 |
| <span class="extend fbe70c7b_32da_4607_b4d3_cf09518f68e1">dc_response</span> | 数字货币返回的响应报文 | Object |  | N | jsonObject字符串 |
| <span class="extend 1abd562d_d602_4f85_a3df_b4e26c324de8">unionpay_response</span> | 银联返回的响应报文 | Object |  | N | jsonObject字符串 |
| device_type | 终端类型 | String | 2 | N | 01-智能POS<br>02-扫码POS<br>03-云音箱<br>04-台牌<br>05-云打印<br>06-扫脸设备<br>07-收银机<br>08-收银助手<br>09-传统POS<br>10-一体音箱<br>11-虚拟终端<br/><font color="green">示例值：01</font> |
| <span class="extend 7034afd8_03ca_47df_9fde_2a0950420a05">mer_dev_location</span> | 商户终端定位 | Object |  | N |  商户终端定位信息，jsonObject字符串；<!--259号文新增字段--> |
| bank_message | 通道返回描述 | String | 200 | N | <font color="green">示例值：成功[0000000]</font> |
| remark | 备注 | String | 255 | N | 原样返回；<font color="green">示例值：备注</font> |
| fq_channels | 分期资产方式 | String | 20 | N | 花呗分期功能，代表优先使用的资产类型；alipayfq_cc：表示信⽤卡分期。<br/><font color="green">示例值：alipayfq_cc</font> |
| notify_type | 通知类型 | Integer | 1 | N | 1：通道通知，2：账务通知；<font color="green">示例值：1</font> |
| <span class="extend efff8b80_d86a_464a_b22a_7c43b9e6d17e">split_fee_info</span> | 分账手续费信息 | Object |  | N | 分账手续费信息 |
| atu_sub_mer_id | ATU真实商户号 | String | 32 | N |  <font color="green">示例值：411111141</font> |
| devs_id | 汇付终端号 | String | 32 | N | 使用汇付机具交易时返回；<font color="green">示例值：660035730311200000</font> |

<!-- extend:start -->
<!-- div:extend-table 19c1b34f_76df_4fc9_bc35_e19061b970a5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | Y |   <font color="green">示例值：AMT\*0.003</font>  |
| fee_type | 手续费类型 | String | 32 | Y |  TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费<br/><font color="green">示例值：ACCT_FEE</font>  |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 40ba46b4_c80e_4c4e_a42d_dc1c232820f9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y |  <font color="green">示例值：5.00</font> |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| allowance_type | 补贴类型 | String | 10 | N | 0：不补贴，为空默认<br/>1：补贴<br/>2：部分补贴<br/>3：全额补贴(优惠后)<br/>4：部分补贴(优惠后)<br/><font color="green">示例值：2</font> |
| no_allowance_desc | 不补贴原因 | String | 128 | N | 1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴<br/>2:额度用完<br/>3:不在有效期<br/>4:活动不存在<br/>5:手续费金额为0不补贴<br/>6:顶格优惠<br/>7:额度不足<br/>8:手续费后补<br/>9:未达到起始补贴金额<br/><font color="green">示例值：2</font> |
| <span class="extend 4f88430e_de7d_48af_af22_8d7c3c821417">cur_allowance_config_infos</span> | 手续费补贴活动详情 | Object |  | N | 补贴系统返回，斗拱原样返回； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4f88430e_de7d_48af_af22_8d7c3c821417-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_id | 门店 | String | 64 | N | <font color="green">示例值：sh002</font> |
| merchant_group | 商户号 | String | 64 | N | <font color="green">示例值：6666000123120000</font> |
| allowance_sys | 补贴方	 | String | 64 | Y | 1:银行  2:服务商 3:汇来米；<font color="green">示例值：1</font> |
| allowance_sys_id | 补贴方ID | String | 64 | Y | 对应补贴方的id；<font color="green">示例值：6666000123120000</font> |
| is_delay_allowance | 补贴类型 | String | 2 | Y |  1:实补,2:后补,默认实补；<font color="green">示例值：1 |
| market_id | 自定义活动编号 | String | 64 | Y |  <font color="green">示例值：ISFE00232</font> |
| market_name | 自定义活动名称 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| market_desc | 自定义活动描述 | String | 64 | N | <font color="green">示例值：新店开业大促</font> |
| start_time | 活动开始时间 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220909</font> |
| end_time | 活动结束时间 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220911</font> |
| pos_debit_limit_amt | pos借记卡补贴额度 | String | 16 | Y | <font color="green">示例值：2.00</font> |
| pos_credit_limit_amt | pos贷记卡补贴额度 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| pos_limit_amt | pos补贴额度 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| qr_limit_amt | 扫码补贴额度 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| total_limit_amt | 活动总补贴额度 | String | 16 | Y | <font color="green">示例值：10.00</font> |
| status | 活动是否有效 | String | 4 | Y | 1:生效 0：失效；<font color="green">示例值：1</font> |
| human_flag | 是否人工操作 | String | 4 | Y | N：自动 Y：人工；<font color="green">示例值：Y</font> |
| activity_id | 活动号 | String | 64 | Y |  <font color="green">示例值：223402342</font> |
| activity_name | 活动描述 | String | 128 | N |  <font color="green">示例值：开业大促</font> |
| create_by | 创建人 | String | 32 | Y | <font color="green">示例值：Lg2022022201394910571</font> |
| create_time | 创建时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 22:00:30</font> |
| update_time | 更新时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 23:00:30</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a22aa4f4_7e41_4091_a3f9_95388a736622-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴方汇付商户号 | String | 32 | Y | 补贴方汇付ID；<font color="green">示例值：6666000123123123</font> |
| user_type | 补贴方类型 | String | 32 | Y | 补贴方类型：channel-渠道，agent-代理；<font color="green">示例值：agent</font> |
| acct_id | 补贴方账户号 | String | 32 | Y | 营销补贴方账户号；<font color="green">示例值：F00900982</font> |
| amount | 补贴金额 | String | 14 | Y | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f83eb0be_3c3c_4e28_82db_5a48dd0078bf-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴支付手续费承担方汇付编号 | String | 32 | Y | 补贴支付手续费承担方汇付编号；<font color="green">示例值：6666000123123123</font> |
| acct_id | 补贴支付手续费承担方账户号 | String | 32 | Y | 补贴支付手续费承担方账户号；<font color="green">示例值：F00900982</font> |
| combinedpay_fee_amt | 补贴支付手续费金额 | String | 14 | Y | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table aa0964fd_46e8_4a66_8638_01af287f34d8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 6f310c67_fba6_4ec1_88cd_567c4a00c9be">acct_infos</span> | 分账明细 | Array |  | Y | jsonArray分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6f310c67_fba6_4ec1_88cd_567c4a00c9be-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120001</font> |
| acct_date | 账务日期 | String | 8 | N | <font color="green">示例值：20220909</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 169f6b54_75c3_45ee_a99a_d41b4eb6f984-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N |  微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识，银行类型见[微信银行类型说明](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；<font color="green">示例值：ICBC_DEBIT</font> |
| cash_fee | 现金支付金额	 | String | 100 | N | 现金支付金额订单现金支付金额；<font color="green">示例值：10.00</font> |
| coupon_fee | 代金券金额 | String | 100 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：0.10</font> |
| attach | 商家数据包 | String | 128 | N | 商家数据包，原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend a0087ebb_c132_44b2_b51b_7b055ff6e605">promotion_detail</span> | 营销详情列表 | Array |  | N | 营销详情列表，使返回值为Json格式； |
| sub_mch_id | 子商户号 | String |  | N | 微信支付分配的子商户号；直联模式返回字段；<font color="green">示例值：1632157057</font> |
| device_info | 设备号 | String |  | N | 调用接口提交的终端设备号；直联模式返回字段；<font color="green">示例值：SP003pcf</font> |
| is_subscribe | 是否关注公众账号 | String |  | N | 用户是否关注公众账号，直联模式返回字段；Y-关注，N-未关注（机构商户不返回）；<font color="green">示例值：Y</font>  |
| sub_is_subscribe | 是否关注子公众账号 | String |  | N | 用户是否关注子公众账号，直联模式返回字段；Y-关注，N-未关注（机构商户不返回）；<font color="green">示例值：Y</font>  |
| fee_type | 现金支付货币类型 | String |  | N |  符合ISO 4217标准的三位字母代码，默认人民币：CNY；直联模式返回字段；<font color="green">示例值：CNY</font>     |
| coupon_count | 代金券使用数量 | String |  | N | 直联模式返回字段；<font color="green">示例值：1</font>  <br/>使用单品优惠时不再返回coupon_count，参数promotion_detail会返回每张券的具体信息，<br/>商户可以通过解析promotion_detail参数来确认使用了几张代金券。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a0087ebb_c132_44b2_b51b_7b055ff6e605-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| promotion_id | 券id | String | 32 | Y | 券或者立减优惠id；<font color="green">示例值：2345234235</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL: 全场代金券，SINGLE: 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | COUPON:  代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT:  优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font>  |
| amount | 优惠券面额 | String | 12 | Y | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）<font color="green">示例值：5.00</font> |
| activity_id | 活动ID | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| merchant_contribute | 商户出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；<br/><font color="green">示例值：10.00</font> |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方出资金额=商家出资+微信出资，单位为元；<font color="green">示例值：20.00</font> |
| <span class="extend 32050c9c_e9d1_4155_9baf_fac17d4427a3">goods_detail</span> | 单品列表 | Array |  | N | 单品信息，使用Json格式，是promotion_detail的元素； |
| wxpay_contribute | 微信出资 | String | 32 | N | 特指由微信支付商户平台创建的优惠，单位：元；<font color="green">示例值：20.00</font> |
| original_other_contribute | 微信交易其他出资方出资金额 | String | 32 | N | 微信的其他出资方出资金额，单位：元；<font color="green">示例值：20.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 32050c9c_e9d1_4155_9baf_fac17d4427a3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码	 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格 | String | 32 | Y | 单位为:元。<font color="green">示例值：99.00</font>；如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，<br/>则活动商品的单价应为原单价-50元 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3a38387b_86fa_4f44_af53_e8edb0289f7b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 6db1cec2_1da0_4f25_995f_4548ff829278">voucher_detail_list</span> | 优惠券信息 | Array |  | N | 本交易支付时使用的所有优惠券信息<br/><font color="green">示例值："[{\"id\":\"20170307000730026487005X1M6V\",\"name\":\"全仓 5折优惠券\"}]"</font> |
| <span class="extend 2a8f46ba_5937_47e5_a6a3_7eac44d4f6c5">fund_bill_list</span> | 资金渠道 | Array |  | N | 支付成功的各个渠道金额信息。交易支付使用的资金渠道。只有在签约中指定需要返回资金明细，或者入参的query_options 中指定时才返回该字段信息。 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 买家的支付宝唯一用户号（2088开头的16位纯数字）<br>示例值：20880414938706770000 |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| hb_fq_seller_percent | 卖家承担的手续费百分比 | String | 3 | N | 比例的百分值，<font color="green">示例值：0.9</font>，传入100代表100%； |
| notify_time | 通知时间 | String |  | N | 直连模式字段；通知的发送时间。格式为Date格式，yyyy-MM-dd HH&#58;mm&#58;ss；<font color="green">示例值2022-10-11 10&#58;12&#58;24</font> |
| app_id | 支付宝应用app_id | String | 32 | N | 直连模式字段；支付宝分配给开发者的应用Id；<font color="green">示例值：2021002122659346</font>  |
| out_biz_no | 商户业务号 | String | 64 | N | 直连模式字段；商户业务ID，主要是退款通知中返回退款申请的流水号；<font color="green">示例值：</font>  |
| invoice_amount | 开票金额 | String | 11 | N | 直连模式字段；用户在交易中支付的可开发票的金额；<font color="green">示例值：100.00</font> |
| buyer_pay_amount | 付款金额 | String | 13 | N | 直连模式字段；用户在交易中支付的金额；<font color="green">示例值：100.00</font>   |
| subject | 订单标题 | String | 256 | N | 直连模式字段；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；<font color="green">示例值：红果奶茶</font>  |
| body | 商品描述 | String | 128 | N | 直连模式字段；该订单的备注、描述、明细等。对应请求时的body参数，<br>原样通知回来；<font color="green">示例值：中杯</font> |
| gmt_create | 交易创建时间 | String | 64 | N | 直连模式字段；该笔交易创建的时间。格式为yyyy-MM-dd HH&#58;mm&#58;ss；<font color="green">示例值2022-10-11 10&#58;12&#58;24</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6db1cec2_1da0_4f25_995f_4548ff829278-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 券id | String | 32 | Y | <font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | <font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | 当前有三种类型：<br />ALIPAY_FIX_VOUCHER:  全场代金券<br />ALIPAY_DISCOUNT_VOUCHER:  折扣券<br />ALIPAY_ITEM_VOUCHER:  单品优惠 <br /><font color="green">示例值：ALIPAY_ITEM_VOUCHER</font></br>注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码  |
| amount | 优惠券面额 | String | 12 | Y | 优惠券面额，它应该会等于商家出资加上其他出资方出资；<br/><font color="green">示例值：10.00</font> |
| merchant_contribute | 商家出资 | String | 12 | N | 特指发起交易的商家出资金额；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 可能是支付宝，可能是品牌商，或者其他方，也可能是他们的一起出资；<font color="green">示例值：0.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2a8f46ba_5937_47e5_a6a3_7eac44d4f6c5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | <font color="green">示例值：CEB</font> |
| amount | 该支付工具类型所使用的金额 | String | 32 | N | 单位：元，两位小数；<font color="green">示例值：0.01</font> |
| fund_channel | 交易使用的资金渠道 | String | 32 | N | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；<font color="green">示例值：ALIPAYACCOUNT</font>  |
| fund_type | 渠道所使用的资金类型 | String | 32 | N | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。<br/>DEBIT_CARD:借记卡，<br/>CREDIT_CARD:信用卡，<br/>MIXED_CARD:借贷合一卡<br/><font color="green">示例值：DEBIT_CARD</font>  |
| real_amount | 渠道实际付款金额 | String | 11 | N |  单位：元，两位小数；<font color="green">示例值：0.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fbe70c7b_32da_4607_b4d3_cf09518f68e1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| merchant_id | 商户号 | String | 35 | N | 数字货币:  工行；<font color="green">示例值：S5088295305</font> |
| term_id | 终端号 | String | 32 | N | 数字货币:  工行；<font color="green">示例值：58000001</font> |
| trade_type | 交易类型 | String | 16 | N | 数字货币:  工行；<font color="green">示例值：SCANPAY</font> |
| custom_bank_code | 客户所属运营机构代码 | String | 14 | N | 数字货币:  工行；<font color="green">示例值：</font> |
| custom_bank_name | 客户所属运营机构名称 | String | 70 | N | 数字货币:  工行；<font color="green">示例值：</font> |
| openid | 用户标识 | String | 64 | N | 数字货币:  工行；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 用户子标识 | String | 64 | N | 数字货币:  工行；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| coupon_amount | 代金券金额 | String | 14 | N | 数字货币:  工行;单位：元；<font color="green">示例值：0.01</font> |
| coupon_count | 代金券数量 | String | 3 | N | 数字货币:  工行；<font color="green">示例值：1</font> |
| <span class="extend 80ff81c9_2962_4d62_be8b_8d64c434cc61">coupon_list</span> | 代金券集合 | Array |  | N | 数字货币:  工行；<font color="green">示例值：[{"coupon_type":"5","coupon_id":"2020060702001","coupon_amount":"50.00"}]</font> |
| creditorWalletName | 收款钱包名称 | String | 60 | N | 数字货币:  邮储；<font color="green">示例值：上海汇涵信息科技服务有限公司</font> |
| creditorWalletId | 收款钱包ID | String | 68 | N | 数字货币:  邮储；<font color="green">示例值：002250******5081</font> |
| creditorWalletType | 收款钱包类型 | String | 4 | N | 数字货币:  邮储   <br />收款钱包类型   <br />WT01:  个人钱包   <br />WT02:  子个人钱包   <br />WT09:  对公钱包   <br />WT10:  子对公钱包<br/><font color="green">示例值：WT09</font> |
| creditorWalletLevel | 收款钱包等级 | String | 4 | N | 数字货币:  邮储   <br />收款钱包等级   <br />WL01:  一类钱包   <br />WL02:  二类钱包   <br />WL03:  三类钱包   <br />WL04:  四类钱包<br/><font color="green">示例值：WL01</font>  |
| debtorWalletName | 付款钱包名称 | String | 60 | N | 数字货币:  邮储；<font color="green">示例值：我的钱包</font> |
| debtorWalletId | 付款钱包ID | String | 68 | N | 数字货币:  邮储；<font color="green">示例值：004100******0032</font> |
| debtorWalletType | 付款钱包类型 | String | 4 | N | 数字货币:  邮储   <br />付款钱包类型   <br />WT01:  个人钱包   <br />WT02:  子个人钱包   <br />WT09:  对公钱包   <br />WT10:  子对公钱包<br/><font color="green">示例值：WT01</font>  |
| debtorWalletLevel | 付款钱包等级 | String | 4 | N | 数字货币:  邮储   <br />付款钱包等级   <br />WL01:  一类钱包   <br />WL02:  二类钱包   <br />WL03:  三类钱包   <br />WL04:  四类钱包<br/><font color="green">示例值：WL02</font> |
| debtorPartyIdentification | 付款运营机构 | String | 14 | N | 数字货币:  邮储；<font color="green">示例值：</font> |
| businessType | 支付类型 | String | 1 | N | 数字货币:  邮储；支付类型：O-本贷他，I-本贷本；<font color="green">示例值：O</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 80ff81c9_2962_4d62_be8b_8d64c434cc61-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| coupon_id | 代金券ID | String | 40 | N |  <font color="green">示例值：2020060702001</font> |
| coupon_type | 代金券类型 | String | 8 | N |  <font color="green">示例值：5</font> |
| coupon_amount | 单个代金券支付金额 | String | 14 | N | 单个代金券支付金额，单位：元；<font color="green">示例值：50.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1abd562d_d602_4f85_a3df_b4e26c324de8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 4c9af0f2_f555_4faa_86c0_757b90656383">coupon_info</span> | 银联优惠信息 | Array |  | N | 银联使用优惠活动时出现，jsonArray格式  |
| acc_no | 付款账号 | String | 40 | N | 付款方的卡号/账号/Token |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4c9af0f2_f555_4faa_86c0_757b90656383-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font>   |
| type | 项目类型 | String | 4 | Y | DD01：随机立减<br>CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券<br>CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券<br><font color="green">示例值：DD01</font>  |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7034afd8_03ca_47df_9fde_2a0950420a05-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| terminal_ip | 交易设备IP | String | 64 | N | 绑卡设备（付款 APP） 所在的公网IP，可用于定位所属地区，不是 wifi 连接时的局域网 IP。<br/>局域网 IP 包括：<br/>A 类： 10.0.0.0-10.255.255.255<br/>B 类： 172.16.0.0-172.31.255.255<br/>C 类： 192.168.0.0-192.168.255.255<br/><font color="green">示例值：172.3.46.44</font> |
| terminal_location | 终端实时经纬度信息 | String | 32 | N | 设备（付款APP）GPS位置,格式为纬度/经度，+表示北纬、东经，-表示南纬、西经。<br/><font color="green">示例值：+37.12/-121.213</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table efff8b80_d86a_464a_b22a_7c43b9e6d17e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| total_split_fee_amt | 分账手续费总金额(元) | String | 14 | N |  <font color="green">示例值：0.10</font>   |
| split_fee_flag | 分账手续费扣款标志 | Integer | 1 | Y | 1: 外扣 2: 内扣；<font color="green">示例值：2</font> |
| <span class="extend 2d952e51_b7ca_4e56_8eca_82ab188eefda">split_fee_details</span> | 分账手续费信息 | Array |  | Y | 分账手续费信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2d952e51_b7ca_4e56_8eca_82ab188eefda-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| split_fee_amt | 分账手续费金额(元) | String | 14 | Y |  <font color="green">示例值：0.10</font>  |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font>  |
| split_fee_acct_id | 分账手续费承担方账号 | String | 32 | N | <font color="green">示例值：F00598600</font>  |
<!-- extend:end -->


#### webhook说明

斗拱交易完成后除了返回异步消息也支持另外发送webhook事件。webhook事件可以灵活配置多个接收端用于驱动业务流程。比如交易完成后发送webhook消息给财务系统入账，发送到物流系统配送商品等等。  
[webhook的使用参见说明](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao?id=%e5%a6%82%e4%bd%95%e4%bd%bf%e7%94%a8webhook)；




#### 参数说明

“禁用支付方式”【limit_pay_type】参数取值如下：

|取值|说明|
|:---|:---|
|NO_CREDIT|禁用信用卡，微信支付宝都禁用；**使用花呗支付时不能禁用信用卡**； |
|BALANCE|禁用支付宝余额|
|MONEY_FUND|禁用支付宝余额宝|
|BANK_PAY|禁用网银，仅支持支付宝禁用|
|DEBIT_CARD_EXPRESS|禁用借记卡快捷，仅支持支付宝禁用|
|CREDIT_CARD_EXPRESS|禁用信用卡快捷 ，仅支持支付宝禁用|
|CREDIT_CARD_CARTOON|禁用信用卡卡通，仅支持支付宝禁用|
|CARTOON|禁用卡通，仅支持支付宝禁用|
|PCREDIT|禁用支付宝花呗|
|PCREDIT_PAY_INSTALLMENT|禁用支付宝花呗分期|
|CREDIT_GROUP|禁用支付宝信用支付类型（包含 信用卡卡通，信用卡快捷,花呗，花呗分期）|
|COUPON|禁用支付宝红包|
|POINT|禁用支付宝积分|
|PROMOTION|禁用支付宝优惠（包含实时优惠+商户优惠）|
|VOUCHER|禁用支付宝营销券|
|MDISCOUNT|禁用支付宝商户优惠|
|HONEY_PAY|禁用支付宝亲密付|
|MCARD|禁用支付宝商户预存卡|
|PCARD|禁用支付宝个人预存卡|





#### 聚合反扫业务返回码


| <div style="width: 60pt">返回码</div>     | 返回描述                                                     |
| :------- | :----------------------------------------------------------- |
| 10000000 | 不支持交易类型                                               |
| 10000000 | 订单时间错误                                                 |
| 10000000 | **付款码格式异常**                                               |
| 10000000 | 请求日期必须是当前日期                                       |
| 10000000 | %s不能为空（%s代指报错参数名）                               |
| 10000000 | %s不符合%s格式（%s代指报错参数名）                           |
| 10000000 | %s长度固定%d位（%s代指报错参数名、%d代指字段长度）           |
| 10000000 | %s最大长度为%d位（%s代指报错参数名、%d代指字段长度）         |
| 10000000 | %s的传入枚举[%s]不存在（%s代指报错参数名）                   |
| 10000000 | 产品号,原预授权交易请求流水,请求日期都不能为空               |
| 21000000 | 手续费金额、手续费收取方式、手续费扣款标识、手续费子客户号、手续费账户号，必须同时为空或同时必填 |
| 22000002 | 商户信息不存在                                               |
| 22000002 | 商户状态异常                                                 |
| 22000002 | 商户和产品的关联信息有误                                     |
| 22000003 | 账户信息配置有误/账户信息不存在                              |
| 22000003 | 默认账户配置有误                                             |
| 22000004 | 商户支付交易业务配置错误/细化指定需要的功能                  |
| 22000004 | 暂未开通分账权限                                             |
| 22000004 | 暂未开通延时入账权限                                         |
| 22000005 | 分账串配置未包含手续费承担方                                 |
| 22000005 | 其他成员分账比例过高                                         |
| 22000005 | 分账列表必须包含主交易账户                                   |
| 22000005 | 内扣交易，手续费承担方必须参与分账                           |
| 22000005 | 商户未配置默认入驻信息(多通道)                               |
| 22000005 | 商户贴息分期费率有误                                         |
| 22000005 | 商户贴息分期费率未配置费率类型                               |
| 22000005 | 商户贴息分期费率未配置渠道号                                 |
| 22000005 | 商户多通道配置有误                                           |
| 22000005 | 商户入驻信息配置有误(多通道)                                 |
| 22000005 | 分账配置有误                                                 |
| 22000005 | 分账比例配置有误                                             |
| 22000005 | 该交易暂未配置支付费率                                       |
| 22000005 | 商户支付宝微信入驻信息配置有误                               |
| 22000005 | 多通道入驻信息配置有误                                       |
| 22000005 | **商户银联入驻信息配置有误**                                     |
| 23000001 | 原预授权交易不存在                                           |
| 23000003 | 交易金额不足以支付手续费                                     |
| 23000003 | 优惠金额大于交易金额                                         |
| 23000003 | 分账金额总和必须等于交易金额                                 |
| 23000004 | 交易类型不支持                                               |
| 90000000 | 业务执行失败，**付款码无效，请重新扫码**  |
| 90000000 | 业务执行失败，每个二维码仅限使用一次，请刷新再试 |
| 90000000 | 业务执行失败，付款码已过期，请退出重试  |
| 90000000 | 业务执行失败，当前商户需补齐相关资料后，才可进行支付交易，请商户联系服务商 |
| 90000000 | 交易存在风险                                                 |
| 98888888 | 系统错误                                                     |
| 91111119 | 通道异常，请稍后重试                            |
| 99999999 | 系统异常,请重试                                              |
| 00000000 | 交易受理成功；注：**交易状态以trans_stat为准；**                                                     |
| 00000100 | 交易正在处理中                                               |

