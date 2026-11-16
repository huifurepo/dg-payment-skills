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
## 微信小程序预下单接口

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/preorder

*最近更新时间：2026.10.13*
### 应用场景
* 外部app跳转微信支付：APP 需要接入微信侧的OpenSDK，文档可参考微信[iOS](https://developers.weixin.qq.com/doc/oplatform/Mobile_App/Access_Guide/iOS.html) /[Android](https://developers.weixin.qq.com/doc/oplatform/Mobile_App/Access_Guide/Android.html)接入指南，跳转微信拉起小程序时，需要将下单返回miniapp_data中的path拼接上参数，path = "pages/cashier/cashier?p=xxx&s=app"。p 代表预下单号，xxx 填写接口返回的pre_order_id，s=app代表来源app固定写死；<br/>
* 外部浏览器H5跳转微信支付：访问下单返回miniapp_data中的scheme_code，注：H5跳转微信支付后不支持跳回原浏览器；<br/>
* 小程序跳转小程序支付：参见[小程序跳转小程序支付说明](https://paas.huifu.com/open/doc/api/#/cpjs/api_cpjs_xcxtz)；






### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共请求参数

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sys_id     | 系统号     | String   | 32       | Y        |渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font> |
| product_id | 产品号     | String   | 32       | Y        |  汇付分配的产品号，<font color="green">示例值：YYZY</font>    |
| sign       | 加签结果   | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 请求数据   | JSON     |          | Y        | 业务请求参数，具体值参考API文档                              |


### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| pre_order_type | 预下单类型 | String | 1 | Y | 微信预下单：3；<font color="green">示例值：3</font> |
| req_date | 请求日期 | String | 8 | Y | 请求格式：yyyyMMdd；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 同一huifu_id下当天唯一；<br/><font color="green">示例值：rQ2021121311173944</font> |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成；<font color="green">示例值：6666000123123123</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，保留两位小数，<font color="green">示例值：1.00</font>，最低传入0.01 |
| goods_desc | 商品描述 | String | 40 | Y | <font color="green">示例值：个人电脑</font> |
| delay_acct_flag | 是否延迟交易 | String | 1 | N | Y 为延迟 N为不延迟，不传默认N；<font color="green">示例值：N</font> |
| merge_pay_flag | 是否合单支付 | String | 1 | N | Y-合单支付，N-非合单支付，默认N，<font color="green">示例值：N</font><br>合单支付，不支持切换支付方式（即multi_pay_way_flag不能为Y）； |
| <span class="extend 9143825f_4e4c_4d89_a43a_9b7761ced267">sub_orders_request</span> | 子单信息列表 | String |  | N | 合单支付时，该字段必填；jsonArray字符串，最多支持20条，最少2条 |
| split_pay_flag | 是否拆单支付 | String | 1 | N | 拆单支付标识，Y：拆单支付，N：非拆单支付，不填默认为N。商户需预开通拆单支付权限后方可使用；<br/><font color="green">示例值：N</font> |
| <span class="extend 3aed07d2_04df_4d00_bad4_a1b45ed2ae5c">split_pay_data</span> | 拆单支付参数集合 | String | 2000 | N | 拆单支付参数集合 |
| <span class="extend 1a27caaf_4d0f_4d43_bcca_1b32c877da44">acct_split_bunch</span> | 分账对象 | String | 2000 | N | 分账对象，jsonObject字符串，拆单支付时该字段不生效 |
| <span class="extend 07227554_5b72_4f46_8092_55f85a93bc26">hosting_data</span> | 统一收银台扩展参数集合 | String | 2000 | N | jsonObject统一收银台扩展参数集合 |
| <span class="extend 3af138f4_08f6_4a08_8f39_a98432ac9e49">miniapp_data</span> | 微信小程序扩展参数集合 | String | 2000 | Y | 微信小程序扩展参数集合 |
| time_expire | 交易失效时间 | String | 14 | N | 请求格式：yyyyMMddHHmmss；<br/><font color="green">示例值：20220912111230</font><br/>注意:为空默认失效时间为10分钟；用户在交易失效时间后完成交易有可能被关单。最终结果以异步为准；<br>建议商户在交易量大时，或在搞营销活动时将失效时间设置短一些。 |
| <span class="extend b9a20bfd_2a8c_4dc3_af52_78ecf486ea99">biz_info</span> | 业务信息 | String | 2000 | N | jsonObject格式；交易相关的信息 |
| notify_url | 交易异步通知地址 | String | 512 | N | http或https开头，<font color="green">示例值：https://callback.service.com/xx</font><br/>在交易成功/失败时触发回调，正常情况下只会触发一次，具体回调策略参见[链接](https://paas.huifu.com/open/doc/api_standard/#/ybxx/jiekouguifan_ybxx) |
| <span class="extend d4b9debf_5921_44be_846e_b7eb65b13804">wx_data</span> | 微信参数集合 | String | 2048 | N | jsonObject字符串 |
| <span class="extend 69889c1c_c4cf_4c94_8329_ab0313a35373">terminal_device_data</span> | 设备信息 | String | 2048 | N | jsonObject字符串 |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。<br/><font color="green">示例值：6850aad1e92f4244a74a42fcc1ad6360</font> |
| fee_split_flag | 是否交易手续费分摊 | String | 1 | N | Y-分摊，N-不分摊，不传默认为N。<font color="green">示例值：N</font> |
| fee_flag | 手续费扣款标志 | String | 1 | N | 1: 外扣 2: 内扣 (默认取控台配置值)；<font color="green">示例值：1</font> |
| channel_no | 渠道号 | String | 32 | N | 如果交易走自有渠道请联系联调群运维人员获取；<font color="green">示例值:10000001</font> |
| pay_scene | 场景类型 | String | 2 | N | 取值参见[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%BE%AE%E4%BF%A1%E4%B8%9A%E5%8A%A1%E5%BC%80%E9%80%9A%E7%B1%BB%E5%9E%8B)说明；<font color="green">示例值:02</font><br/>pay_scene需和channel_no配合使用。在指定channel_no的情况下需要传入pay_scene取值；为空取默认配置  |

<!-- extend:start -->
<!-- div:extend-table 9143825f_4e4c_4d89_a43a_9b7761ced267-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_req_seq_id | 子单请求流水号 | String | 128 | Y | 同一合单huifu_id下，当天唯一 |
| sub_huifu_id | 子单商户号 | String | 32 | Y | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font> |
| sub_acct_id | 子单账户号 | String | 9 | N | 可指定收款账户号， 仅支持基本户、现金户，不填默认为基本户； |
| sub_trans_amt | 子单交易金额 | String | 18 | Y | 单位元，需保留小数点后两位，示例值：1000.00，最低传入0.01；<br/>全部子单交易金额之和等于合单交易金额。 |
| delay_acct_flag | 是否延迟交易 | String | 1 | N | Y 为延迟 N为不延迟，不传默认N；<font color="green">示例值：Y</font> |
| sub_remark | 子单备注 | String | 255 | N | 交易后原样返回；<font color="green">示例值：子单备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3aed07d2_04df_4d00_bad4_a1b45ed2ae5c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fq_mer_discount_flag | 商户贴息标记 | String | 1 | N | 花呗分期商户补贴活动，拆单支付时生效，Y：商户全额贴息，P：商户部分贴息，不传为非商户贴息（默认）；<br/><font color="green">示例值：P</font><br/>选择P：商户部分贴息活动，需同时在【ali_business_params：商户业务信息】中传入支付宝约定的活动参数，参数说明详见分期支付指引文档。 |
| ali_business_params | 商户业务信息 | String | 1 | N | 拆单支付时生效，商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1a27caaf_4d0f_4d43_bcca_1b32c877da44-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 9b9a6c95_a13f_4c6b_9fd6_9a2f41f9d2c3">acct_infos</span> | 分账明细 | Array |  | N | 分账明细 |
| percentage_flag | 百分比分账标志 | String | 1 | N |  Y:使用百分比分账；<font color="green">示例值：Y</font> |
| is_clean_split | 是否净值分账 | String | 1 | N | Y:使用净值分账，仅在交易手续费内扣且使用百分比分账时起作用；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9b9a6c95_a13f_4c6b_9fd6_9a2f41f9d2c3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | N | 斗拱开户时生成；<font color="green">示例值：6666000111546360</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| percentage_div | 分账百分比% | String | 6 | N |  <font color="green">示例值：23.50</font>，表示23.50%。仅在percentage_flag=Y时起作用<br>acct_infos中全部分账百分比只和必须为100.00%。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 07227554_5b72_4f46_8092_55f85a93bc26-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| project_id | 项目号 | String | 32 | N | 商户创建的项目号；<font color="green">示例值：PROJECTID2022032912492559</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3af138f4_08f6_4a08_8f39_a98432ac9e49-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| seq_id | 应用ID | String | 64 | N | <font color="green">示例值：APP_2022100912694428</font><br/>不传默认使用斗拱收银台唤起支付。<br/>如使用自有渠道时通过控台小程序托管功能上传同主体小程序并发布代码获取应用ID填写此处。[参见图片说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/%E6%94%AF%E4%BB%98%E6%89%98%E7%AE%A1%E5%BA%94%E7%94%A8ID.png) <br/>如使用微信插件该参数不传值。 |
| private_info | 私有信息 | String | 255 | N | 对应异步通知和主动查询接口中的remark字段；<font color="green">示例值：备注</font> |
| need_scheme | 是否生成scheme_code | String | 1 | Y | Y；适用于APP、短信链接、邮件、外部网页、微信内等拉起汇付小程序的业务场景时需填Y；<br/>N；通过汇付微信插件支付填N； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b9a20bfd_2a8c_4dc3_af52_78ecf486ea99-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 663201c2_5e1b_4c67_8b0c_241434e58ad0">payer_check_wx</span> | 付款人验证（微信） | Object |  | N | 微信实名支付需验证买家信息；如彩票行业等； <br/>当前只支持AT类交易有验证功能； |
| <span class="extend 7b416ac5_a262_4f95_bb77_9a1ae47c3c22">person_payer</span> | 个人付款人信息 | Object |  | N | 付款人验证打开后需要填写付款人信息，但非必填； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 663201c2_5e1b_4c67_8b0c_241434e58ad0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| limit_payer | 指定支付者 | String | 5 | N | 上传此参数，可限制用户只有是成年人才能支付，<br/>值：ADULT；<font color="green">示例值：ADULT</font> |
| real_name_flag | 微信实名验证 | String | 1 | N | Y/N；默认N；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7b416ac5_a262_4f95_bb77_9a1ae47c3c22-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 姓名 | String | 16 | N | <font color="green">示例值：张三</font> |
| cert_type | 证件类型 | String | 32 | N | 身份证：IDENTITY_CARD，（微信只支持身份证）；<font color="green">示例值：IDENTITY_CARD</font> |
| cert_no | 证件号 | String | 64 | N | 需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。<br/><font color="green">示例值：Mc5pjf+b/Keyi/t/wnH……MfYQnK7Lzw==</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d4b9debf_5921_44be_846e_b7eb65b13804-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | N | 子商户在微信申请的应用ID，全局唯一。**走聚合正扫发货管理的商户，使用的微信公众号/小程序支付 需要填写sub_appid+sub_openid**<br/><font color="green">示例值：wxd678efh567hg6999</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 公众号和小程序场景必填。用户在子商户sub_appid下的唯一标识。下单前需获取到用户的sub_openid，sub_openid获取详见微信文档[openid获取](https://pay.weixin.qq.com/docs/partner/development/glossary/parameter.html)。<br/><font color="green">示例值：oUpF8uMuAJO_M2pxb1Q9zNjWeS6o</font> |
| attach | 附加数据 | String | 127 | N | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；<br/><font color="green">示例值：附加数据</font> |
| body | 商品描述 | String | 128 | N | 商品或支付单简要描述，格式要求：门店品牌名-城市分店名-实际商品名称；<font color="green">示例值：image形象店-深圳腾大- QQ 公仔</font> |
| <span class="extend e5b7f3eb_e834_421f_ba1a_4347d5559700">detail</span> | 商品详情 | Object | 6000 | N | 单品优惠功能字段 |
| device_info | 设备号 | String | 32 | N | 终端设备号(商户自定义，如门店编号)，<font color="green">示例值：660035730311000126101</font><br/>注意：H5与小程序支付填以下值：<br/>苹果APP：1；安卓APP：2；IOS手机网站：3；ANDROID手机网站：4 |
| goods_tag | 订单优惠标记 | String | 32 | N | 代金券或立减优惠功能的参数；<font color="green">示例值：WXG</font> |
| identity | 实名支付 | String | 128 | N | 实名支付功能，用于公安和保险类商户使用, 包含类型、证件号、姓名三个子域。<br/><font color="green">示例值："{\\"type\":\\"IDCARD\\",\\"number\\":\\"111111111111\\",\\"name\\":\\"张三\\"}"</font> |
| receipt | 开发票入口开放标识 | String | 8 | N | <font color="green">示例值：Y</font> |
| <span class="extend c04e503e_e2fe_4166_aa9b_0a5dd323b83f">scene_info</span> | 场景信息 | Object | 2048 | N | 该字段用于上报场景信息，目前支持上报实际门店信息。 |
| spbill_create_ip | 终端ip | String | 64 | N | 调用微信支付API的机器IP；<font color="green">示例值：172.28.52.52</font> |
| promotion_flag | 单品优惠标识 | String | 1 | N | Y-是，N-否，默认否；直连模式需要填写；<font color="green">示例值：Y</font><br/>若使用单品优惠，该字段必填，若该字段为Y，则商品详情【detail】必填 |
| product_id | 新增商品ID | String | 32 | N | 直连模式【trade_type】=T_NATIVE支付的时候必填；<font color="green">示例值：</font> |
| limit_payer | 指定支付者 | String | 5 | N | 上传此参数，可限制用户只有是成年人才能支付，<font color="green">示例值：ADULT</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e5b7f3eb_e834_421f_ba1a_4347d5559700-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cost_price | 订单原价(元) | String | 12 | N | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 <br>2.当订单原价与支付金额不相等，则不享受优惠。<br>3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。<br/><font color="green">示例值：999.00</font> |
| receipt_id | 商品小票ID | String | 32 | N | 商家小票 ID；<font color="green">示例值：20220628132043853798</font> |
| <span class="extend 38f2595f_939e_450d_a569_3c68155dc8a6">goods_detail</span> | 单品列表 | Array | 2048 | Y | 单品信息，使用Json数组格式提交 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 38f2595f_939e_450d_a569_3c68155dc8a6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | N | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_name | 商品名称 | String | 256 | N | 商品的实际名称；<font color="green">示例值：太龙双黄连口服液</font> |
| price | 商品单价(元) | String | 12 | N | 如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50<br/><font color="green">示例值：43.00</font> |
| quantity | 商品数量 | Int | 11 | N | 用户购买的数量；<font color="green">示例值：1</font> |
| wxpay_goods_id | 微信侧商品编码 | String | 32 | N | <font color="green">示例值：12235413214070356458058</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c04e503e_e2fe_4166_aa9b_0a5dd323b83f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend d16c2f5a_b291_42e3_b8a0_4ead1c6e5af8">store_info</span> | 门店信息 | Object | 2048 | N | 门店信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d16c2f5a_b291_42e3_b8a0_4ead1c6e5af8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 门店id | String | 32 | N | 门店编号，由商户自定义；<font color="green">示例值：sh001</font> |
| name | 门店名称 | String | 64 | N | 门店名称，由商户自定义；<font color="green">示例值：上海宝山分店</font> |
| area_code | 门店行政区划码 | String | 6 | N | 门店所在地行政区划码，详见[行政区划代码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，<font color="green">示例值：310101 </font>； |
| address | 门店详细地址 | String | 128 | N | 门店详细地址，由商户自定义；<font color="green">示例值：上海宝山区共富路100号</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 69889c1c_c4cf_4c94_8329_ab0313a35373-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传；<font color="green">示例值：660035730311000126101</font><!--259号文新增字段--> |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "checkout_id": "",
        "delay_acct_flag": "Y",
        "req_seq_id": "20240515094131812h3xogy21j9dls6",
        "req_date": "20240515",
        "trans_amt": "0.13",
        "miniapp_data": "{\"need_scheme\":\"Y\",\"seq_id\":\"APP_2022100912694428\",\"private_info\":\"oppsHosting://\"}",
        "huifu_id": "6666000109133323",
        "goods_desc": "app跳微信消费",
        "pre_order_type": "3",
        "notify_url": "https://callback.service.com/xx",
        "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000109133323\",\"div_amt\":\"0.01\"}]}"
    },
    "sign": "F6hIPAhvouxmpXhKudDmSnWj7ezH3zuhLzevNlRKziz5o3xJWqBPccZ3AQU0m1NUsNjDJIeAdIFFUMH0W8/cahDxikcRQMupuTqTIULEBRFqqFbq8P5pTW/AUZZSHK0vV8of8Wt29jG8Zg6D97ItEIk4DL43COSolCexNUP5UwNJzb0drWr2k0+Os4wOWIGMloK+bDivZvqgaTmv574+gNOsNDjLk8Q7GQ3hB20EghKTDS2Jg6PO58dMTtxy55VZZs5l+W0mCZYboFIYtB1FEC93KEnxovmO0CpayAZf22DMjAThkhS9xThZKvb64xJd+QIoeqmXgKyeMmleMt2msg=="
}
```
### 返回参数


#### 同步返回参数

**公共返回参数**

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |


**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 128 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| req_date | 请求日期 | String | 8 | Y | 预下单时传入，原样返回；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 预下单时传入，原样返回；<br/><font color="green">示例值：20220424561166000</font> |
| huifu_id | 商户号 | String | 32 | Y | 预下单时传入，原样返回；<br/><font color="green">示例值：6666000111546360</font> |
| trans_amt | 交易金额 | String | 12 | Y | 预下单时传入，原样返回；<font color="green">示例值：300.00</font> |
| pre_order_id | 预下单订单号 | String | 64 | Y | <font color="green">示例值：H2022050711225100912503288</font> |
| <span class="extend d5742c0b_75aa_4cb7_b050_615d2941ef80">miniapp_data</span> | 微信小程序返回集合 | String | 2000 | Y | json格式，用于app跳转微信支付 |

<!-- extend:start -->
<!-- div:extend-table d5742c0b_75aa_4cb7_b050_615d2941ef80-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| gh_id | 小程序原始ID | String | 64 | N | <font color="green">示例值：gh_1ad0a7231d39</font> |
| path | 小程序页面支付路径 | String | 64 | N | <font color="green">示例值：pages/cashier/cashier</font> |
| scheme_code | 小程序跳转码 | String | 64 | N | <font color="green">示例值：weixin://dl/business/?t=c1HAi9XnUnt</font><br/>need_scheme=N时返回空 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "req_date": "20220321",
        "req_seq_id": "20220SQSS63235883",
        "huifu_id": "6666000003100616",
        "trans_amt": "0.13",
        "pre_order_id": "H2023112713461700667284637",
        "miniapp_data": "{\"appid\":\"wxd1b54ceabdfdbd4f\",\"gh_id\":\"gh_1a8554fca417\",\"need_scheme\":\"Y\",\"path\":\"pages/cashier/cashier\",\"private_info\":\"oppsHosting://\",\"scheme_code\":\"weixin://dl/business/?t=f5x3WMhYPat\",\"seq_id\":\"APP_2022033147154783\"}"
    }
}
```


#### 异步返回参数

交易完成返回异步。    
**resp_data** 

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回信息 | String | 512 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| req_date | 请求时间 | String | 8 | Y | 交易时传入，原样返回，格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 交易时传入，原样返回；<br/><font color="green">示例值：20220424561166000</font> |
| hf_seq_id | 全局流水号 | String | 40 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | <font color="green">示例值：092021091922001451301445517582</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | <font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000111546360</font> |
| trans_type | 交易类型 | String | 20 | N | T_JSAPI:  微信公众号支付<br/>T_MINIAPP:  微信小程序支付  <br/>A_JSAPI:  支付宝JS  <br/>A_NATIVE:  支付宝正扫  <br/>U_NATIVE:  银联正扫  <br/>U_JSAPI:  银联 JS  <br/>T_MICROPAY:  微信反扫  <br/>A_MICROPAY:  支付宝反扫  <br/>U_MICROPAY:  银联反扫  <br/>D_NATIVE:  数字人民币正扫  <br/>D_MICROPAY:  数字人民币反扫<br/><font color="green">示例值：U_MICROPAY</font> |
| trans_amt | 交易金额 | String | 12 | N | 单位元，保留两位小数，<font color="green">示例值：1.00</font>，最低0.01 |
| settlement_amt | 结算金额 | String | 16 | N | 单位元，保留两位小数，<font color="green">示例值：1.00</font>，最低0.01 |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，保留两位小数，<font color="green">示例值：1.00</font>，最低0.01 |
| acct_date | 入账时间 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| trans_stat | 交易状态 | String | 1 | N | S：成功、F：失败；<font color="green">示例值：S</font> |
| end_time | 支付完成时间 | String | 14 | N | 格式yyyyMMddHHmmss，<font color="green">示例值：20091225091010</font> |
| trans_finish_time | 汇付侧交易完成时间 | String | 13 | N | 毫秒时间戳，<font color="green">示例值：1791598928000</font> |
| debit_flag | 借贷记标识 | String | 1 | N | D-借记卡   C-信用卡   Z-借贷合一卡<font color="green">示例值：C</font> |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | <font color="green">示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk=</font> |
| <span class="extend c6379ddd_31db_4872_a035_26a96658c1c6">wx_response</span> | 微信返回的响应报文 | String | 6000 | N | JsonObject格式 |
| is_div | 是否分账交易 | String | 1 | Y | 1:  分账交易, 0:  非分账交易；<font color="green">示例值：1</font> |
| <span class="extend bab38129_3ce7_48d8_a3b9_f024b9c50995">acct_split_bunch</span> | 分账对象 | String | 2048 | N | 分账对象，jsonObject字符串 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | 1:  延迟   0:  不延迟；<font color="green">示例值：1</font> |
| fee_flag | 手续费扣款标志 | Int | 1 | N | 1:  外扣，2:  内扣；默认返回控台配置方式；<font color="green">示例值：1</font> |
| <span class="extend 422b67d3_af6d_4a3e_8aef_2048e8b3857d">trans_fee_allowance_info</span> | 手续费补贴信息 | String | 6000 | N | JsonObject格式 |
| <span class="extend 17b3fdbb_0306_45e1_a95a_a43de5e14f69">fee_formula_infos</span> | 手续费费率信息 | String |  | N | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| remark | 备注 | String | 45 | N | 原样返回；<font color="green">示例值：备注</font> |
| bank_code | 通道返回码 | String | 32 | N | <font color="green">示例值：00</font> |
| bank_message | 通道返回描述 | String | 200 | N | <font color="green">示例值：成功[0000000]</font> |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传；<font color="green">示例值：660035730311000126101</font> |
| <span class="extend 9a73b9d2_96bb_40fa_9491_2c42d68e7bf9">sub_orders_response</span> | 子单信息 | String |  | N | jsonArray格式；子单信息，合单支付的订单返回该字段 |

<!-- extend:start -->
<!-- div:extend-table c6379ddd_31db_4872_a035_26a96658c1c6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N | 微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 用户子标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/wiki/doc/apiv3/terms_definition/chapter1_1_3.shtml#part-7)；<font color="green">示例值：OTHERS</font> |
| cash_fee | 现金支付金额 | String | 12 | N | 订单现金支付金额；<font color="green">示例值：10.00</font> |
| coupon_fee | 代金券金额 | String | 12 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend fc1cc79e_5e3f_4d1a_9c1e_2219c44e8f01">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 营销详情列表，使返回值为Json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fc1cc79e_5e3f_4d1a_9c1e_2219c44e8f01-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| promotion_id | 券或者立减优惠id | String | 32 | Y | <font color="green">示例值：2345234235</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL:  全场代金券，SINGLE:  单品优惠；<font color="green">示例值：SINGLE</font> |
| type | 优惠类型 | String | 32 | N | COUPON: 代金券，需要走结算资金的充值型代金券,境外商户券币种与支付币种一致<br />DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，境外商户券币种与标价币种一致<br/><font color="green">示例值：DISCOUNT</font> |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| activity_id | 活动ID | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| merchant_contribute | 商户出资(元) | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资(元) | String | 32 | N | 其他出资方出资金额；<font color="green">示例值：5.00</font> |
| <span class="extend e1675c7f_b0cb_47a3_846c_153879b0ca5b">goods_detail</span> | 单品列表 | Object | 3000 | N | 使用Json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e1675c7f_b0cb_47a3_846c_153879b0ca5b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<br/><font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格(元) | String | 32 | Y | <font color="green">示例值：50.00</font>。如果商户有优惠，需传输商户优惠后的单价。<br/>例如：100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bab38129_3ce7_48d8_a3b9_f024b9c50995-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 26574233_563a_4ddc_9624_eb774ada0c13">acct_infos</span> | 分账明细 | Array | 2048 | Y | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 26574233_563a_4ddc_9624_eb774ada0c13-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120000</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| acct_date | 账务日期 | String | 8 | N | <font color="green">示例值：20221023</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 422b67d3_af6d_4a3e_8aef_2048e8b3857d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| allowance_type | 补贴类型 | String | 10 | N | 0：不补贴，为空默认<br/>1：补贴<br/>2：部分补贴<br/>3：全额补贴(优惠后)<br/>4：部分补贴(优惠后)<br/><font color="green">示例值：2</font> |
| no_allowance_desc | 不补贴原因 | String | 128 | N | 补贴系统返回的不补贴原因<br/>1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴<br/>2:额度用完<br/>3:不在有效期<br/>4:活动不存在<br/>5:手续费金额为0不补贴<br/>6:顶格优惠<br/>7:额度不足<br/>8:手续费后补<br/>9:未达到起始补贴金额<br/><font color="green">示例值：2</font> |
| <span class="extend 8ca386e1_9bbd_4feb_9169_7662bcc55fd2">cur_allowance_config_infos</span> | 手续费补贴活动详情 | Array |  | N | 补贴系统返回，斗拱原样返回 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8ca386e1_9bbd_4feb_9169_7662bcc55fd2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_id | 门店 | String | 64 | N | <font color="green">示例值：sh002</font> |
| merchant_group | 商户号 | String | 64 | N | <font color="green">示例值：6666000123120000</font> |
| allowance_sys | 补贴方 | String | 64 | N | 1:银行  2:服务商 3:汇来米；<font color="green">示例值：1</font> |
| allowance_sys_id | 补贴方ID | String | 64 | N | 对应补贴方的id；<font color="green">示例值：6666000123120000</font> |
| is_delay_allowance | 补贴类型 | String | 2 | N | 1:实补  2:后补,默认实补；<font color="green">示例值：1</font> |
| market_id | 自定义活动编号 | String | 64 | N | <font color="green">示例值：ISFE00232</font> |
| market_name | 自定义活动名称 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| market_desc | 自定义活动描述 | String | 64 | N | <font color="green">示例值：新店开业大促</font> |
| start_time | 活动开始时间 | String | 8 | N | yyyyMMdd；<font color="green">示例值：20220909</font> |
| end_time | 活动结束时间 | String | 8 | N | yyyyMMdd；<font color="green">示例值：20220919</font> |
| pos_debit_limit_amt | pos借记卡补贴额度 | String | 16 | N | <font color="green">示例值：2.00</font> |
| pos_credit_limit_amt | pos贷记卡补贴额度 | String | 16 | N | <font color="green">示例值：5.00</font> |
| pos_limit_amt | pos补贴额度 | String | 16 | N | <font color="green">示例值：4.00</font> |
| qr_limit_amt | 扫码补贴额度 | String | 16 | N | <font color="green">示例值：1.00</font> |
| total_limit_amt | 活动总补贴额度 | String | 16 | N | <font color="green">示例值：10.00</font> |
| status | 活动是否有效 | String | 4 | N | 1:生效 0：失效；<font color="green">示例值：1</font> |
| human_flag | 是否人工操作 | String | 4 | N | N：自动 Y：人工；<font color="green">示例值：N</font> |
| activity_id | 活动号 | String | 64 | N | <font color="green">示例值：223402342</font> |
| activity_name | 活动描述 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| create_by | 创建人 | String | 32 | N | <font color="green">示例值：Lg2022022201394910571</font> |
| create_time | 创建时间 | String | 32 | N | <font color="green">示例值：2022-04-14 22&#58;00&#58;30</font> |
| update_time | 更新时间 | String | 32 | N | <font color="green">示例值：2022-04-14 23&#58;00&#58;30</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 17b3fdbb_0306_45e1_a95a_a43de5e14f69-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | Y | <font color="green">示例值：AMT*0.003</font> |
| fee_type | 手续费类型 | String | 32 | Y | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；<font color="green">示例值：ACCT_FEE</font> |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。<br/><font color="green">示例值：6850aad1e92f4244a74a42fcc1ad6360</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9a73b9d2_96bb_40fa_9491_2c42d68e7bf9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_req_seq_id | 子单请求流水号 | String | 128 | Y | 交易时传入，原样返回；<font color="green">示例值：SUB2021121311173944134649875651</font> |
| sub_hf_seq_id | 子单全局流水号 | String | 128 | Y | <font color="green">示例值：00470topo1A221019132207P068ac1362af00001</font> |
| sub_huifu_id | 子单商户号 | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| sub_acct_id | 子单账户号 | String | 9 | Y | <font color="green">示例值：A123456</font> |
| sub_trams_amt | 子单交易金额 | String | 14 | Y | 位元；<font color="green">示例值：1.00</font> |
| sub_settlement_amt | 子单结算金额 | String | 14 | N | 位元；<font color="green">示例值：1.00</font> |
| sub_remark | 子单备注信息 | String | 255 | N | 原样返回；<font color="green">示例值：子单备注</font> |
| acct_date | 子单入账日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| acct_stat | 子单账务状态 | String | 1 | N | "I：初始"; "P:处理中"; "S:成功"; "F:失败。<font color="green">示例值：S</font><br/> 返回“I：初始”状态时，请联系客服确认订单问题 |
| is_div | 是否分账交易 | String | 1 | N | 1:分账交易， 0:非分账交易；<font color="green">示例值：1</font> |
| <span class="extend e09f3959_4de6_42c8_921a_9600c1a9a53f">acct_split_bunch</span> | 分账对象 | String |  | N | jsonObject字符串 |
| <span class="extend 8be43054_d8e9_46ee_9cc9_d9053c5f7342">fee_infos</span> | 交易手续费信息 | String |  | N | 交易手续费信息 |
| <span class="extend 05205c7c_ff8d_4188_a904_f8252cb32bee">split_fee_info</span> | 分账手续费信息 | String |  | N | 分账手续费信息 |
| fund_freeze_stat | 资金冻结状态 | String | 16 | N | FREEZE：冻结；UNFREEZE：解冻；<font color="green">示例值：UNFREEZE</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e09f3959_4de6_42c8_921a_9600c1a9a53f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 50455f80_c2d4_4786_b68d_49ea6013663a">acct_infos</span> | 分账明细 | String |  | Y | jsonArray分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 50455f80_c2d4_4786_b68d_49ea6013663a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120001</font> |
| acct_id | 分账接收方账户号 | String | 9 | N | <font color="green">示例值：A123456</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8be43054_d8e9_46ee_9cc9_d9053c5f7342-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | N | <font color="green">示例值：AMT\*0.003</font>  |
| fee_huifu_id | 手续费扣款商户号 | String | 32 | N |  |
| fee_acct_id | 手续费扣款账户号 | String | 9 | N |  |
| fee_flag | 手续费扣款标志 | Integer | 1 | N | 1:  外扣，2:  内扣；<font color="green">示例值：2</font> |
| fee_rec_type | 手续费扣取方式 | Integer | 1 | N | 1:  实收，2:  后收；<font color="green">示例值：1</font> |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，保留小数点后两位。根据手续费公式计算的手续费小于0.01时，至少收取0.01元。<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 05205c7c_ff8d_4188_a904_f8252cb32bee-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| total_split_fee_amt | 分账手续费总金额(元) | String | 14 | N |  <font color="green">示例值：0.10</font>   |
| split_fee_flag | 分账手续费扣款标志 | Integer | 1 | Y | 1: 外扣 2: 内扣；<font color="green">示例值：2</font> |
| <span class="extend 6f63bb31_21cc_47f1_9301_02fa268b29f9">split_fee_details</span> | 分账手续费信息 | String |  | Y | 分账手续费信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6f63bb31_21cc_47f1_9301_02fa268b29f9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| split_fee_amt | 分账手续费金额(元) | String | 16 | Y |  <font color="green">示例值：0.10</font>  |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font>  |
| split_fee_acct_id | 分账手续费承担方账号 | String | 9 | N | <font color="green">示例值：F00598600</font>  |
<!-- extend:end -->


#### 业务返回码

常见错误码：

| 返回码   | 返回描述                                                   | 处理                                               |
| :------- | :--------------------------------------------------------- | :------------------------------------------------- |
| 90000000 | 生成微信Scheme失败，errcode[40001],errmsg[invalid credential, access_token is invalid or not latest rid: xxxx]   | 小程序有变更或被微信封了，需要重新配置小程序 |
| 99010002 | 预下单请求流水重复  | 提供新的流水号 |




#### 拆单支付异步返回参数

拆单支付成功时返回该异步。    
**resp_data** 

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回信息 | String | 512 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000111546360</font> |
| req_date | 请求时间 | String | 8 | Y | 交易时传入，原样返回，格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 交易时传入，原样返回；<br/><font color="green">示例值：20220424561166000</font> |
| trans_stat | 交易状态 | String | 1 | Y | S：成功、F：失败；<font color="green">示例值：S</font> |
| sys_id | 系统号 | String | 32 | Y | 渠道商/商户的huifu_id<br/>（1）当主体为渠道商时，此字段填写渠道商huifu_id；<br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font> |
