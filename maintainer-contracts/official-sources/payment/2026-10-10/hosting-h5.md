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
## H5、PC预下单接口

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/preorder

*最近更新时间：2026.10.10*

### 应用场景
- 场景1-H5：接入统一收银台接口并获取链接，通过主动跳转链接完成支付。  
- 场景2-PC：接入统一收银台接口并获取链接，通过新窗口跳转链接完成支付。[点击链接体验](https://paas.huifu.com/checkout/demo/pc/goodsDetail.html?type=2)
- 场景3-动态二维码：接入统一收银台接口并获取链接转换成二维码，支持付款人用手机微信、支付宝、云闪付、浏览器扫码支付；  

请扫码体验，支持支付宝、微信、云闪付、浏览器扫码。     
<img src="https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/demo/%E6%94%AF%E4%BB%98%E6%89%98%E7%AE%A1H5%E6%89%AB%E7%A0%81%E4%BD%93%E9%AA%8C.png" alt="统一收银台H5扫码体验"  style="zoom: 80%;" />       

- 自有渠道对接请参考[统一收银台自有渠道对接流程](https://paas.huifu.com/open/doc/api/#/cpjs/api_cpjs_hostingdoc)

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共请求参数


| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sys_id     | 系统号     | String   | 32       | Y        | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font>  |
| product_id | 产品号     | String   | 32       | Y        | 汇付分配的产品号，<font color="green">示例值：YYZY</font>    |
| sign       | 加签结果   | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)|
| data       | 请求数据   | JSON     |          | Y        | 业务请求参数，具体值参考API文档                              |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 请求格式：yyyyMMdd；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944</font> |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成；<font color="green">示例值：6666000123123123</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| goods_desc | 商品描述 | String | 40 | Y | <font color="green">示例值：个人电脑</font> |
| pre_order_type | 预下单类型 | String | 1 | Y | H5/PC预先下单：1；<font color="green">示例值：1</font> |
| delay_acct_flag | 是否延迟交易 | String | 1 | N | Y 为延迟，N为不延迟，不传默认N；<font color="green">示例值：N</font> |
| multi_pay_way_flag | 是否支持切换支付方式 | String | 1 | N | N：不支持，不允许选择支付方式后切换另一种支付方式<br/>Y：支持，允许选择支付方式后切换另一种支付方式<br/>注：不传时默认N，若需要对接未完成时支持切换支付方式，对账环节需选择如下方式对账；<br/>方式1：以支付成功返回的全局流水号作为对账的唯一标记；<br/>方式2：以请求流水号作为对账的唯一标记时，解析斗拱的交易账单时，应忽略请求流水号字段中“-”及“-”后的数字信息；<br/><font color="green">示例值：N</font> |
| <span class="extend 62180bc2_7c30_47cb_af45_2511d2506f6a">acct_split_bunch</span> | 分账对象 | String | 2000 | N | 分账对象，jsonObject字符串 |
| <span class="extend b459756c_aecb_47dd_a35a_bedc9e64c07f">hosting_data</span> | 统一收银台扩展参数集合 | String | 2000 | Y | jsonObject统一收银台扩展参数集合 |
| time_expire | 交易失效时间 | String | 14 | N | 请求格式：yyyyMMddHHmmss；<font color="green">示例值：20220912111230</font><br/>注意:为空默认失效时间为10分钟；用户在交易失效时间后完成交易有可能被关单。最终结果以异步为准；<br>建议商户在交易量大时，或在搞营销活动时将失效时间设置短一些。 |
| <span class="extend 4d3f955d_a749_4f9c_ac5e_e4cf90c3abd1">biz_info</span> | 业务信息 | String | 2000 | N | jsonObject格式；交易相关的信息 |
| notify_url | 交易异步通知地址 | String | 512 | N | http或https开头，<font color="green">示例值：https://callback.service.com/xx</font><br/>在交易成功/失败时触发回调，正常情况下只会触发一次，具体回调策略参见[链接](https://paas.huifu.com/open/doc/api_standard/#/ybxx/jiekouguifan_ybxx) |
| usage_type | 使用类型 | String | 1 | N | P-支付（默认）； R-充值；<font color="green">示例值：P</font> |
| trans_type | 交易类型 | String | 256 | N | 支持同时上送多个支付类型（多个时，使用英文逗号分割），上送多个或未传值时进入收银台，上送单个时直接到支付页；<br/>T_JSAPI:  微信公众号支付；支付PC、H5场景；  <br/>A_JSAPI:  支付宝JS；支付PC、H5场景；  <br/>A_NATIVE:  支付宝正扫；支付PC、H5场景；  <br/>U_NATIVE:  银联正扫；支付PC、H5场景；  <br/>U_JSAPI:  银联 JS；支付PC、H5场景；  <br/>ONLINE_PAY_B2B：B2B网银支付；支付PC场景；<br/>ONLINE_PAY_B2C：B2C网银支付；支付PC场景；<br/>QUICK_PAY：快捷支付；支付PC、H5场景；<br/>LARGE_PAY：备付金下单模式；支付PC、H5场景；<br/>Y_H5：抖音H5支付；支付H5场景；<br/><font color="green">示例值：A_JSAPI</font><br/>**注意：[指定网银支付首次跳转银行页面需要打开浏览器弹窗限制](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/%E6%B5%8F%E8%A7%88%E5%99%A8%E5%85%81%E8%AE%B8%E5%BC%B9%E7%AA%97%E9%85%8D%E7%BD%AE.png)** |
| <span class="extend 6697c151_1ffe_49c8_8a24_8a0403523d2d">wx_data</span> | 微信参数集合 | String | 2048 | N | jsonObject字符串 |
| <span class="extend f8ccbdcf_f641_4ef5_a6c9_e4ff8f74ab6a">alipay_data</span> | 支付宝参数集合 | String | 2048 | N | jsonObject字符串 |
| <span class="extend e0c99825_0197_4b92_9bc6_4f5ecf5f06bb">dy_data</span> | 抖音参数集合 | String | 2048 | N | jsonObject字符串 |
| <span class="extend 98d137e9_46e8_4b0b_85af_a082f8c931af">unionpay_data</span> | 银联参数集合 | String | 2048 | N | jsonObject字符串 |
| <span class="extend ac2d3c22_c317_414f_8e3d_c91b176be50f">terminal_device_data</span> | 设备信息 | String | 2048 | N | jsonObject字符串 |
| <span class="extend 88b0cb84_e44a_4a6a_b8c0_85c2ad0d6e57">largeamt_data</span> | 大额支付参数集合 | String | 2500 | N | jsonObject字符串 |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。<br/><font color="green">示例值：6850aad1e92f4244a74a42fcc1ad6360</font> |
| fee_split_flag | 是否交易手续费分摊 | String | 1 | N | Y-分摊，N-不分摊，不传默认为N。<font color="green">示例值：N</font> |
| fee_flag | 手续费扣款标志 | String | 1 | N | 1: 外扣 2: 内扣 (默认取控台配置值)；<font color="green">示例值：1</font> |
| channel_no | 渠道号 | String | 32 | N | 如果交易走自有渠道请联系联调群运维人员获取；<font color="green">示例值:10000001</font> |
| pay_scene | 场景类型 | String | 2 | N | 取值参见[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%BE%AE%E4%BF%A1%E4%B8%9A%E5%8A%A1%E5%BC%80%E9%80%9A%E7%B1%BB%E5%9E%8B)说明；<font color="green">示例值:02</font><br/>pay_scene需和channel_no配合使用。在指定channel_no的情况下需要传入pay_scene取值；为空取默认配置  |

<!-- extend:start -->
<!-- div:extend-table 62180bc2_7c30_47cb_af45_2511d2506f6a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend c5f36ec0_56f6_4bf6_81a5_ad05b728073e">acct_infos</span> | 分账明细 | Array |  | N | 分账明细 |
| percentage_flag | 百分比分账标志 | String | 1 | N |  Y:使用百分比分账；<font color="green">示例值：Y</font> |
| is_clean_split | 是否净值分账 | String | 1 | N | Y:使用净值分账，仅在交易手续费内扣且使用百分比分账时起作用；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c5f36ec0_56f6_4bf6_81a5_ad05b728073e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>。<br/>支持传入0.00，如果是全额分账，可以分给商户自身0.00元； |
| huifu_id | 分账接收方ID | String | 32 | N | 斗拱开户时生成返回；<font color="green">示例值：6666000111546360</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| percentage_div | 分账百分比% | String | 6 | N |  <font color="green">示例值：23.50</font>，表示23.50%。仅在percentage_flag=Y时起作用<br>acct_infos中全部分账百分比只和必须为100.00%。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b459756c_aecb_47dd_a35a_bedc9e64c07f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| project_title | 项目标题 | String | 64 | Y | 用于账单页面显示；<font color="green">示例值：汇付收银台</font> |
| project_id | 项目号 | String | 32 | Y | 商户创建的项目号；<font color="green">示例值：PROJECTID2022032912492559</font> |
| private_info | 商户私有信息 | String | 255 | N | 对应异步通知和主动查询接口中的remark字段；<font color="green">示例值：收取服务费</font> |
| callback_url | 回调地址 | String | 512 | N | 若不填，支付成功后停留在当前页面，填写后跳转回指定地址；<font color="green">示例值：https://paas.huifu.com</font> |
| request_type | 请求类型 | String | 1 | C | P:PC页面版，默认：P；M:H5页面版；指定交易类型时必填；<font color="green">示例值：M</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4d3f955d_a749_4f9c_ac5e_e4cf90c3abd1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend fd6c34bf_7c9f_4e9f_94d5_9741c0b15b97">payer_check_ali</span> | 付款人验证（支付宝） | Object |  | N | 支付宝特殊交易需验证买家信息；如彩票行业等；<br/>当前只支持AT类交易有验证功能； |
| <span class="extend 46ab8006_316f_4f10_a868_6a4dd02467e3">payer_check_wx</span> | 付款人验证（微信） | Object |  | N | 微信实名支付需验证买家信息；如彩票行业等； <br/>当前只支持AT类交易有验证功能； |
| <span class="extend 48caad7a_77ce_4a97_95b3_e7f7e635c7dc">person_payer</span> | 个人付款人信息 | Object |  | N | 付款人验证打开后需要填写付款人信息，但非必填；微信/支付宝共用字段； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table fd6c34bf_7c9f_4e9f_94d5_9741c0b15b97-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| need_check_info | 是否提供校验身份信息 | String | 1 | N | T：强制校验，需要填写person_payer字段；F：不强制；<font color="green">示例值：T</font> |
| min_age | 允许的最小买家年龄 | String | 3 | N | 买家年龄必须大于等于所传数值。<font color="green">示例值：18</font><br/>注：1. need_check_info=T 时该参数才有效，<br/>2. min_age 为整数，必须大于等于 0； |
| fix_buyer | 是否强制校验付款人身份信息 | String | 8 | N | 用户进行实名认证校验；T：强制校验，F：不强制；<font color="green">示例值：T</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 46ab8006_316f_4f10_a868_6a4dd02467e3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| limit_payer | 指定支付者 | String | 5 | N | 上传此参数，可限制用户只有是成年人才能支付，<br/>值：ADULT；<font color="green">示例值：ADULT</font> |
| real_name_flag | 微信实名验证 | String | 1 | N | Y/N；默认N；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 48caad7a_77ce_4a97_95b3_e7f7e635c7dc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 姓名 | String | 16 | N | 注：支付宝交易need_check_info=T时，该参数才有效；<font color="green">示例值：张三</font> |
| cert_type | 证件类型 | String | 32 | N | 身份证：IDENTITY_CARD，（微信只支持身份证）<br/>护照：PASSPORT；<br/>军官证：OFFICER_CARD，<br/>士兵证：SOLDIER_CARD；<br/>户口本：HOKOU；<br/>微信/支付宝共用字段；<font color="green">示例值：IDENTITY_CARD</font> <br/>注：支付宝交易need_check_info=T时，该参数才有效 |
| cert_no | 证件号 | String | 64 | N | 注：支付宝交易need_check_info=T时，该参数才有效；需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。<br/><font color="green">示例值：Mc5pjf+b/Keyi/t/wnH……MfYQnK7Lzw==</font> |
| mobile | 手机号 | String | 20 | N | 支付宝字段；注：该参数暂不校验；<font color="green">示例值：13911111111</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6697c151_1ffe_49c8_8a24_8a0403523d2d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| attach | 附加数据 | String | 127 | N | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；<br/><font color="green">示例值：附加数据</font> |
| <span class="extend 580c5fee_15bf_44d5_9af3_a0e6adc695c4">detail</span> | 商品详情 | Object | 6000 | N | 单品优惠功能字段 |
| goods_tag | 订单优惠标记 | String | 32 | N | 代金券或立减优惠功能的参数；<font color="green">示例值：WXG</font> |
| receipt | 开发票入口开放标识 | String | 8 | N | <font color="green">示例值：Y</font> |
| <span class="extend d624ddca_e797_4cd1_aa2a_70d2fb1ebb15">scene_info</span> | 场景信息 | Object | 2048 | N | 该字段用于上报场景信息，目前支持上报实际门店信息。 |
| promotion_flag | 单品优惠标识 | String | 1 | N | Y-是，N-否，默认否；直连模式需要填写；<font color="green">示例值：Y</font><br/>若使用单品优惠，该字段必填，若该字段为Y，则商品详情【detail】必填 |
| product_id | 新增商品ID | String | 32 | N | 直连模式【trade_type】=T_NATIVE支付的时候必填；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 580c5fee_15bf_44d5_9af3_a0e6adc695c4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| cost_price | 订单原价(元) | String | 12 | N | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 <br>2.当订单原价与支付金额不相等，则不享受优惠。<br>3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。<br/><font color="green">示例值：999.00</font> |
| receipt_id | 商品小票ID | String | 32 | N | 商家小票 ID；<font color="green">示例值：20220628132043853798</font> |
| <span class="extend 333268ca_bf7a_4b95_8cdf_7339186d20d4">goods_detail</span> | 单品列表 | Array | 2048 | Y | 单品信息，使用Json数组格式提交 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 333268ca_bf7a_4b95_8cdf_7339186d20d4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | N | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_name | 商品名称 | String | 256 | N | 商品的实际名称；<font color="green">示例值：太龙双黄连口服液</font> |
| price | 商品单价(元) | String | 12 | N | 如果商户有优惠，需传输商户优惠后的单价；<br/>例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50<br/><font color="green">示例值：43.00</font> |
| quantity | 商品数量 | Int | 11 | N | 用户购买的数量；<font color="green">示例值：1</font> |
| wxpay_goods_id | 微信侧商品编码 | String | 32 | N | <font color="green">示例值：12235413214070356458058</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d624ddca_e797_4cd1_aa2a_70d2fb1ebb15-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend b93d2c86_271e_48f8_83a5_df4f090959df">store_info</span> | 门店信息 | Object | 2048 | N | 门店信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b93d2c86_271e_48f8_83a5_df4f090959df-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 门店id | String | 32 | N | 门店编号，由商户自定义；<font color="green">示例值：sh001</font> |
| name | 门店名称 | String | 64 | N | 门店名称，由商户自定义；<font color="green">示例值：上海宝山分店</font> |
| area_code | 门店行政区划码 | String | 6 | N | 门店所在地行政区划码，详见[行政区划代码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，<font color="green">示例值：310101 </font>； |
| address | 门店详细地址 | String | 128 | N | 门店详细地址，由商户自定义；<font color="green">示例值：上海宝山区共富路100号</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f8ccbdcf_f641_4ef5_a6c9_e4ff8f74ab6a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| alipay_store_id | 支付宝的店铺编号 | String | 32 | N | <font color="green">示例值：2016041400077000000003314986</font> |
| <span class="extend a3c12fef_ab67_4e92_a987_1e94ea5f19f8">extend_params</span> | 业务扩展参数 | Object | 2048 | N | 业务扩展参数 |
| <span class="extend f9ff0be7_c79e_4233_a9a5_329d6fc583de">goods_detail</span> | 订单包含的商品列表信息 | Array | 2048 | N | 订单包含的商品列表信息 |
| merchant_order_no | 商户原始订单号 | String | 32 | N | <font color="green">示例值：39045032345</font> |
| operator_id | 商户操作员编号 | String | 28 | N | <font color="green">示例值：carl.li@huifu.com</font> |
| product_code | 销售产品码 | String | 32 | N | <font color="green">示例值：YYZY</font> |
| seller_id | 卖家支付宝用户号 | String | 28 | N | <font color="green">示例值：20880414938706770000</font> |
| store_id | 商户门店编号 | String | 32 | N | <font color="green">示例值：sh1001</font> |
| subject | 订单标题 | String | 256 | N | 直连模式必填；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；<font color="green">示例值：红果奶茶</font> |
| store_name | 商家门店名称 | String | 512 | N | 直连模式字段；<font color="green">示例值：红果奶茶上海宝山店</font> |
| ali_business_params | 商户业务信息 | String | 512 | N | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| fq_mer_discount_flag | 商户贴息标记 | String | 1 | N | 花呗分期商户补贴活动，Y：商户全额贴息，P：商户部分贴息，不传为非商户贴息（默认）；<br/><font color="green">示例值：P</font><br/>选择P：商户部分贴息活动，需同时在【ali_business_params：商户业务信息】中传入支付宝约定的活动参数，参数说明详见分期支付指引文档。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a3c12fef_ab67_4e92_a987_1e94ea5f19f8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 卡类型 | String | 32 | N | <font color="green">示例值：S0JP0000</font> |
| food_order_type | 支付宝点餐场景类型 | String | 20 | N | QR_ORDER（店内扫码点餐）<br/>PRE_ORDER（预点到店自提）<br/>HOME_DELIVERY（外送到家）<br/>DIRECT_PAYMENT（直接付款）<br/>QR_FOOD_ORDER（点餐先付）<br/>P_QR_FOOD_ORDER（点餐后付）<br/>SELF_PICK（门店自提）<br/>TAKE_OUT （餐饮外卖）<br/>OTHER（其他）<br/>该参数只适用于支付宝支付窗交易接口；<font color="green">示例值：TAKE_OUT</font> |
| hb_fq_num | 花呗分期数 | String | 5 | N | 使用花呗分期要进行的分期数；<font color="green">示例值：3</font> |
| hb_fq_seller_percent | 花呗卖家手续费百分比 | String | 3 | N | 使用花呗分期需要卖家承担的手续费比，单位比例的百分值。<br/> 花呗商贴支付默认传0<!--孙洁要求这样写-->，<font color="green">示例值：0</font> |
| industry_reflux_info | 行业数据回流信息 | String | 64 | N | <font color="green">示例值：{\"scene_code\":\"metro_tradeorder\",\"channel\":\"xxxx\",\"scene_data\":{\"asset_name\":\"ALIPAY\"}}</font> |
| fq_channels | 信用卡分期资产方式 | String | 20 | N | 代表优先使用资产类型；alipayfq_cc：表示信⽤卡分期，为空时默认花呗。<font color="green">示例值：alipayfq_cc</font> |
| parking_id | 停车场id | String | 28 | N | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；<br/><font color="green">示例值：PI1504848980306666666</font> |
| sys_service_provider_id | 系统商编号 | String | 64 | N | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；<br/><font color="green">示例值：20880414938706770000</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f9ff0be7_c79e_4233_a9a5_329d6fc583de-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品的编号 | String | 32 | Y | <font color="green">示例值：apple-01</font> |
| goods_name | 商品名称 | String | 256 | Y | <font color="green">示例值：ipad</font> |
| price | 商品单价(元) | String | 16 | Y | 单位：元；<font color="green">示例值：43.40</font> |
| quantity | 商品数量 | String | 10 | Y | <font color="green">示例值：40</font> |
| body | 商品描述信息 | String | 1000 | N | <font color="green">示例值：个人电脑</font> |
| categories_tree | 商品类目树 | String | 128 | N | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\ |
| goods_category | 商品类目 | String | 24 | N | <font color="green">示例值：34543238</font> |
| show_url | 商品的展示地址 | String | 400 | N | <font color="green">示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e0c99825_0197_4b92_9bc6_4f5ecf5f06bb-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | Y | 子商户/二级商户在抖音开放平台申请的应用ID，全局唯一。<br/>此处请填写移动应用类型的AppID，并确保该sub_appid与sub_mchid有绑定关系。<br/><font color="green">示例值：awofz9bncda6x7w8</font> |
| coupon_info | 优惠标记 | String | 1024 | N | 1、json格式。和抖音支付协商后可用。<br/>2、传参说明：<br/>（1）业务场景区分，可通过传入key值=biz_scene，value值为约定场景值。<br/>（2）个性化策略区分，可通过传入key值=product_tag，value值为约定参数值。<br/>（3）指定优惠信息区分，可通过传入key值=assign_discounts，value值为“抖音支付优惠查询接口”返回的“指定优惠信息”字段值。<br/><font color="green">示例值：{"biz_scene":"xxx","product_tag":"xxx","assign_discounts":"xxx"}</font> |
| <span class="extend 667431be_3dcd_4ad7_9e24_0b1c02caef4b">h5_info</span> | H5场景信息 | Object | 2048 | Y | H5场景信息 |
| <span class="extend 25dad9f5_768b_4716_8d8d_dbda92084384">scene_info</span> | 场景信息 | Object | 2048 | Y | 支付场景描述 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 667431be_3dcd_4ad7_9e24_0b1c02caef4b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 场景类型 | String | 32 | Y | Ios, Android, Wap<font color="green">示例值：Ios</font> |
| app_name | 应用名称 | String | 64 | N | <font color="green">示例值：抖音</font> |
| app_url | 网站URL | String | 128 | N | <font color="green">示例值：示例值：https://douyinpay.com/</font> |
| bundle_id | iOS平台BundleID | String | 128 | N | iOS平台BundleID |
| package_name | Android平台PackageName | String | 128 | N | Android平台PackageName |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 25dad9f5_768b_4716_8d8d_dbda92084384-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| payer_client_ip | 用户终端IP | String | 45 | Y | 用户的客户端IP，支持IPv4和IPv6两种格式的IP地址<br/><font color="green">示例值：14.23.150.211</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 98d137e9_46e8_4b0b_85af_a082f8c931af-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addn_data | 收款方附加数据 | String | 3000 | N | 请参考[银联收款方附加数据(addn_data)说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylcsjh#银联收款方附加数据(addn_data)) |
| area_info | 地区信息 | String | 32 | N | <font color="green">示例值：310000</font> |
| front_url | 前台通知地址 | String | 200 | N | 收款方向银联推送订单时上送的前台通知地址（仅允许为外网地址）；<br/>用户完成支付点击“返回”后，银联通过浏览器post请求到该地址。<br/><font color="green">示例值：http://www.huifu.com</font> |
| payee_comments | 收款方附言 | String | 100 | N | <font color="green">示例值：业务收款</font> |
| <span class="extend 1fdffa8a_b9a2_48b6_961f_e29c17554888">payee_info</span> | 收款方信息 | Object | 2048 | N | 收款方信息 |
| pnr_ins_id_cd | 银联分配的服务商机构标识码 | String | 11 | N | <font color="green">示例值：01008330</font> |
| req_reserved | 请求方自定义域 | String | 500 | N | <font color="green">示例值：</font> |
| term_info | 终端信息 | String | 32 | N | <font color="green">示例值：</font> |
| <span class="extend d3a29548_caa4_4499_95a5_ae480d2eb5fe">pid_info</span> | 服务商信息 | String |  | N | 服务商信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1fdffa8a_b9a2_48b6_961f_e29c17554888-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| mer_cat_code | 商户类别 | String | 4 | N | [参考银联商户类别](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylshlb)；<font color="green">示例值：0101</font> |
| sub_id | 二级商户代码 | String | 20 | N | <font color="green">示例值：823586070110039</font> |
| sub_name | 二级商户名称 | String | 100 | N | <font color="green">示例值：上海白乐门酒店</font> |
| term_id | 终端号 | String | 8 | N | <font color="green">示例值：58000001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d3a29548_caa4_4499_95a5_ae480d2eb5fe-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pnr_order_id | 服务商订单编号 | String | 40 | N | 服务商自定义并发送，同一交易日期内不可重复，订单编号将作为服务商和银联对账的唯一索引，不超过40字节的变长字母和/或数字字符，不能含“-”或“_” |
| pid_sct | 服务商密文 | String | 8 | N | 由服务商根据服务商代码标识加密算法生成 |
| trade_scene | 场景标识 | String | 8 | N | 取值如下:1-扫码点餐<font color="green">示例值：1</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ac2d3c22_c317_414f_8e3d_c91b176be50f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传；<font color="green">示例值：660035730311000126101</font><!--259号文新增字段--> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 88b0cb84_e44a_4a6a_b8c0_85c2ad0d6e57-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| certificate_name | 付款方名称 | String | 64 | N | 要素校验时使用；使用大额支付三要素校验时必填；示例值：上海汇付支付有限公司 |
| bank_card_no | 付款方银行卡号 | String | 2048 | N | 要素校验时使用，使用大额支付四要素校验时必填；原文最大为19位，密文最大长度为2048；使用斗拱公钥做RSA加密；<br>示例值：b9LE5RccVVLChrHgo9lvp……PhWhjKrWg2NPfbe0mkQ== |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "data": {
        "checkout_id": "",
        "delay_acct_flag": "N",
        "hosting_data": "{\"callback_url\":\"https://paas.huifu.com\",\"project_id\":\"PROJECTID2023101225142567\",\"project_title\":\"收银台标题\",\"private_info\":\"商户私有信息test\"}",
        "req_seq_id": "20240514163256046l9da4ecgqugo7h",
        "biz_info": "{\"payer_check_wx\":{\"limit_payer\":\"ADULT\",\"real_name_flag\":\"Y\"},\"person_payer\":{\"cert_type\":\"IDENTITY_CARD\",\"cert_no\":\"OLOxrl809XmVIMmPRTIyIpJHxi4HFMJNmxGz1nhZAtps9xPEVDysU3UZPBZfsNFLFcXEMENPsJ+tymbYt42dNQ+76hyEtx+qz0BQhU8SKV8H5itrI4kaXpaJf+sV8OewrJkhDidPdz01vqMEDQRhaMnNwl8snHZxDdpu7HVUz5JwsLYfBbZP2Q4CZpVWS3NunQahZ8zHQ+8EhvYVH1vE7f/M6nJt1/4GoHz9C/UnuYudV0S2uBhlywbX+YkRGNMl/oz5+UNeMDA2jqhtTreSD4+w7S82L53rqKsAbosodOPo4OAMZk4/0QOH5LDbqFByVM97mzHfw7z+Tx/dsXJ8QQ==\",\"name\":\"张三\",\"mobile\":\"15012345678\"},\"payer_check_ali\":{\"fix_buyer\":\"F\",\"need_check_info\":\"T\",\"min_age\":\"12\"}}",
        "req_date": "20240514",
        "trans_amt": "0.10",
        "huifu_id": "6666000109133323",
        "goods_desc": "个人电脑",
        "pre_order_type": "1",
        "notify_url": "https://callback.service.com/xx",
        "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000111546360\",\"div_amt\":\"0.08\"}]}"
    },
    "product_id": "YYZY",
    "sign": "HADee/Q3ry34yV8k72ZHQcfWDUEBsbGdkIf86U002c0f94+TIukt+woWbCaqW2GTiEr7tFbeOEpdAHnYcusqE1BT/jmo3axqxNOTdNsG7g6OQFcepkyv9LgVqhgyPwXBVTa9KlNT0g7fWX5BwWRHPeOlnYh0eTtBwby7TxVTwj5kwo5JsYRjEiwb+58NBoN8S9eiW6o6j3IeWBIjYyCcDbQsmiC1bM8bMtq86DcHQm40D3+uiNTxEnf9BFIDxkswHQQ1vUsDDHAKnrrGU5qDx3S5hSGmwrKJInn6Wgmbj3S6vclzTiaRixllDBtSfbl4L/D3iINlOwrI6Bwu7f2a2w=="
}
```
### 返回参数


#### 同步返回参数

**公共返回参数**

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)   |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 128 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| req_date | 请求日期 | String | 8 | Y | 预下单时传入，原样返回；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 预下单时传入，原样返回；<font color="green">示例值：20220424561166000</font> |
| huifu_id | 商户号 | String | 32 | Y | 预下单时传入，原样返回；<font color="green">示例值：6666000111546360</font> |
| pre_order_type | 预下单类型 | String | 1 | Y | H5/PC预先下单：1；<font color="green">示例值：1</font> |
| pre_order_id | 预下单ID | String | 64 | Y | <font color="green">示例值：H2023121508555500668113779</font> |
| goods_desc | 商品描述 | String | 40 | Y | <font color="green">示例值：个人电脑</font> |
| jump_url | 支付跳转链接 | String | 256 | Y | 直接跳转当前链接唤起支付；<font color="green">示例值：https://callback.service.com/xx</font> |
| usage_type | 订单类型 | String | 1 | N | P-支付 R-充值 默认：P-支付；<font color="green">示例值：P</font> |
| trans_type | 交易类型 | String | 256 | N | 支持同时上送多个支付类型，上送多个或未传值时进入收银台，上送单个时直接到支付页；<br/>T_JSAPI:  微信公众号支付；支付PC、H5场景；  <br/>A_JSAPI:  支付宝JS；支付PC、H5场景；  <br/>A_NATIVE:  支付宝正扫；支付PC、H5场景；  <br/>U_NATIVE:  银联正扫；支付PC、H5场景；  <br/>U_JSAPI:  银联 JS；支付PC、H5场景；  <br/>ONLINE_PAY_B2B：B2B网银支付；支付PC场景；<br/>ONLINE_PAY_B2C：B2C网银支付；支付PC场景；<br/>QUICK_PAY：快捷支付；支付PC、H5场景；<br/>LARGE_PAY：备付金下单模式；支付PC、H5场景；<br/>Y_H5：抖音H5支付；支付H5场景；<br/><font color="green">示例值：A_JSAPI</font><br/>**注意：[指定网银支付首次跳转银行页面需要打开浏览器弹窗限制](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/%E6%B5%8F%E8%A7%88%E5%99%A8%E5%85%81%E8%AE%B8%E5%BC%B9%E7%AA%97%E9%85%8D%E7%BD%AE.png)** |
| <span class="extend 585541fb_5c7b_447e_ae27_1a5d3c879a09">hosting_data</span> | 统一收银台扩展参数集合 | String | 2000 | Y | jsonObject统一收银台扩展参数集合 |
| current_time | 系统响应时间 | String | 14 | Y | 格式：yyyyMMddHHmmss<font color="green">示例值：20231215090052</font> |
| time_expire | 交易失效时间 | String | 14 | Y | 格式：yyyyMMddHHmmss；<font color="green">示例值：20231215090052</font> |

<!-- extend:start -->
<!-- div:extend-table 585541fb_5c7b_447e_ae27_1a5d3c879a09-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| project_title | 项目标题 | String | 64 | Y | 用于账单页面显示；<font color="green">示例值：汇付收银台</font> |
| project_id | 项目号 | String | 32 | Y | 商户创建的项目号；<font color="green">示例值：PROJECTID2022032912492559</font> |
| private_info | 商户私有信息 | String | 255 | N | 对应异步通知和主动查询接口中的remark字段；<font color="green">示例值：收取服务费</font> |
| callback_url | 回调地址 | String | 512 | N | 若不填，支付成功后停留在当前页面，填写后跳转回指定地址；<font color="green">示例值：https://paas.huifu.com</font> |
| request_type | 请求类型 | String | 1 | C | P:PC页面版，默认：P；M:H5页面版；指定交易类型时必填；<font color="green">示例值：M</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "req_date": "20220424",
        "req_seq_id": "20220424561166000",
        "huifu_id": "6666000111546360",
        "jump_url": "https://api.huifu.com/hostingh5/?jump_id=H20220424140825009124199014&huifu_id=6666000111546360"
    }
}
```


#### 异步返回参数

**resp_data**    
注意：**成功发起支付才会有异步返回**；

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回信息 | String | 512 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 交易时传入，原样返回；<font color="green">示例值：20220424561166000</font> |
| req_date | 请求时间 | String | 8 | Y | 交易时传入，原样返回，格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| hf_seq_id | 汇付全局流水号 | String | 40 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | <font color="green">示例值：092021091922001451301445517582</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | <font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000111546360</font> |
| trans_type | 交易类型 | String | 20 | N | T_JSAPI:  微信公众号支付；支付PC、H5场景；  <br/>A_JSAPI:  支付宝JS；支付H5场景；  <br/>A_NATIVE:  支付宝正扫；支付PC场景；  <br/>U_NATIVE:  银联正扫；支付PC场景；  <br/>U_JSAPI:  银联 JS；支付H5场景；  <br/>ONLINE_PAY_B2B：B2B网银支付；支付PC场景；<br/>ONLINE_PAY_B2C：B2C网银支付；支付PC场景；<br/>QUICK_PAY：快捷支付；支付PC、H5场景；<br/>Y_H5：抖音H5支付；支付H5场景；<br/><font color="green">示例值：A_JSAPI</font> |
| trans_amt | 交易金额 | String | 12 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| settlement_amt | 结算金额 | String | 16 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| trans_stat | 交易状态 | String | 1 | N | S：成功、F：失败；<font color="green">示例值：S</font> |
| trans_finish_time | 汇付侧交易完成时间 | String | 13 | N | 毫秒时间戳，<font color="green">示例值：1791598928000</font> |
| end_time | 支付完成时间 | String | 14 | N | 格式yyyyMMddHHmmss，<font color="green">示例值：20091225091010</font> |
| acct_date | 入账时间 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| debit_flag | 借贷记标识 | String | 1 | N | D-借记卡   C-信用卡   Z-借贷合一卡；<font color="green">示例值：C</font> |
| user_huifu_id | 用户号 | String | 32 | N | 汇付分配的用户号快捷支付时才有值；<font color="green">示例值：6666000103905031</font> |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | <font color="green">示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk=</font> |
| <span class="extend 7948222d_1c09_4bbb_a1b7_740e15fcc8f2">wx_response</span> | 微信返回的响应报文 | Object | 6000 | N | jsonObject格式 |
| <span class="extend 700becb4_47db_4851_b8c8_873d42b78e57">alipay_response</span> | 支付宝返回的响应报文 | Object | 6000 | N | jsonObject格式 |
| <span class="extend 9ece1f06_294a_4031_9446_6270a7ba6d9d">unionpay_response</span> | 银联返回的响应报文 | Object | 6000 | N | jsonObject格式 |
| <span class="extend 290f582f_6174_4a6a_b3d4_89c935a4906f">dy_response</span> | 抖音返回的响应报文 | String |  | N | jsonObject字符串 |
| is_div | 是否分账交易 | String | 1 | Y | 1:  分账交易, 0:  非分账交易；<font color="green">示例值：1</font> |
| <span class="extend 5b408f76_987f_498d_b2bb_2b568096a40b">acct_split_bunch</span> | 分账对象 | String | 2048 | N | 分账对象，jsonObject字符串 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | 1:  延迟   0:  不延迟；<font color="green">示例值：1</font> |
| fee_flag | 手续费扣款标志 | Int | 1 | N | 1:  外扣，2:  内扣；默认返回控台配置方式；<font color="green">示例值：2</font> |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| <span class="extend 62baa955_813b_4b7c_b860_8a570e20fff2">trans_fee_allowance_info</span> | 手续费补贴信息 | Object | 6000 | N | jsonObject格式 |
| remark | 备注 | String | 45 | N | 原样返回；<font color="green">示例值：备注</font> |
| bank_code | 通道返回码 | String | 32 | N | <font color="green">示例值：00</font> |
| bank_message | 通道返回描述 | String | 200 | N | <font color="green">示例值：成功[0000000]</font> |
| bank_id | 收款方银行代号 | String | 8 | N | 快捷、网银返回；<font color="green">示例值：01040000</font> |
| <span class="extend edb87cb5_788d_4a13_8224_a3f09bb50af5">bank_extend_param</span> | 银行扩展信息 | String |  | N | jsonObject格式；网银返回 |
| <span class="extend 9fb69f20_3485_4028_b493_ff04ccc2ebcd">fee_formula_infos</span> | 手续费费率信息 | String |  | N | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| order_type | 订单类型 | String | 1 | N | P-支付 R-充值 默认：P-支付；<font color="green">示例值：P</font> |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传；<font color="green">示例值：660035730311000126101</font> |
| request_ip | 请求IP | String | 15 | N | 付款方IP,仅在支付成功后返回;示例：192.168.1.1 |

<!-- extend:start -->
<!-- div:extend-table 7948222d_1c09_4bbb_a1b7_740e15fcc8f2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N | 微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/wiki/doc/apiv3/terms_definition/chapter1_1_3.shtml#part-7)；<font color="green">示例值：OTHERS</font> |
| cash_fee | 现金支付金额 | String | 12 | N | 订单现金支付金额；<font color="green">示例值：10.00</font> |
| coupon_fee | 代金券金额 | String | 12 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend 91338d2b_505a_4206_8b1e_2bb9b10c43ab">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 营销详情列表，使返回值为Json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 91338d2b_505a_4206_8b1e_2bb9b10c43ab-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| promotion_id | 券或者立减优惠id | String | 32 | Y | <font color="green">示例值：2345234235</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL:  全场代金券，SINGLE:  单品优惠；<font color="green">示例值：SINGLE</font> |
| type | 优惠类型 | String | 32 | N | COUPON:  代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）    <br />DISCOUNT:  优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font> |
| amount | 优惠券面额 | String | 5 | Y | 用户享受优惠的金额；<font color="green">示例值：10.00</font> |
| activity_id | 活动ID | String | 32 | Y | 在微信商户后台配置的批次ID；<font color="green">示例值：458626534790131712</font> |
| merchant_contribute | 商户出资 | String | 32 | N | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资 | String | 32 | N | 其他出资方出资金额，单位为元；<font color="green">示例值：5.00</font> |
| <span class="extend 63613d6f_17ac_492f_ab90_355d92424814">goods_detail</span> | 单品列表 | Object | 3000 | N | 使用Json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 63613d6f_17ac_492f_ab90_355d92424814-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格 | String | 32 | Y | 单位为:  元。<font color="green">示例值：50.00</font><br/>如果商户有优惠，需传输商户优惠后的单价(例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50) |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 700becb4_47db_4851_b8c8_873d42b78e57-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 2abb6536_0f99_4e03_a7e5_102732ae1b69">voucher_detail_list</span> | 优惠券信息 | Array |  | N | 本交易支付时使用的所有优惠券信息 |
| <span class="extend b082efd1_eb34_4a19_a1c0_363c9fee1a3b">fund_bill_list</span> | 支付金额信息 | String | 512 | N | 支付成功的各个渠道金额信息，详见资金明细信息说明；json格式 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 2088开头的16位纯数字；<font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| hb_fq_seller_percent | 卖家承担的手续费 | String | 3 | N | <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2abb6536_0f99_4e03_a7e5_102732ae1b69-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 券id | String | 32 | Y | <font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | <font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | 当前有三种类型：    <br />ALIPAY_FIX_VOUCHER:  全场代金券<br />ALIPAY_DISCOUNT_VOUCHER:  折扣券<br />ALIPAY_ITEM_VOUCHER:  单品优惠 <br /><font color="green">示例值：ALIPAY_ITEM_VOUCHER</font><br/>注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| amount | 优惠券面额（元） | String | 8 | Y | 它应该会等于商家出资加上其他出资方出资；<font color="green">示例值：10.00</font> |
| merchant_contribute | 商家出资 | String | 8 | N | 特指发起交易的商家出资金额；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 可能是支付宝、品牌商、第三方，也可能是他们的一起出资；<br/><font color="green">示例值：0.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b082efd1_eb34_4a19_a1c0_363c9fee1a3b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行代码 | String | 10 | N | 银行卡支付时的银行代码；<font color="green">示例值：CEB</font>；请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9ece1f06_294a_4031_9446_6270a7ba6d9d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend ea0dde3c_3e8e_48a8_8f36_1fefc72957a1">coupon_info</span> | 银联优惠信息 | Object |  | N | 优惠信息，银联使用优惠活动时出现，json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ea0dde3c_3e8e_48a8_8f36_1fefc72957a1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
| spnsr_id | 出资方 | String | 20 | Y | 00010000：银联出资，<font color="green">示例值：00010000</font>；未来将增加付款方等出资方 |
| type | 项目类型 | String | 4 | Y | DD01：随机立减， CP01：抵金券；<font color="green">示例值：CP01</font> |
| offst_amt | 抵消交易金额 | String | 12 | Y | 不能为全0；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 290f582f_6174_4a6a_b3d4_89c935a4906f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | N | 在抖音开放平台申请的应用ID，全局唯一。此处请填写移动应用（APP）/网站应用（H5）类型的AppID |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：897ae8bd9f194107-9cb3-85f5672037de</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：823ae8bd9f893402-9cb3-85f8794657ea</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识<font color="green">示例值：OTHERS</font> |
| <span class="extend 0331ebb8_e157_4833_9766_ed8423c58fb3">promotion_detail</span> | 营销详情列表 | String |  | N | 营销详情列表，使返回值为Json格式； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0331ebb8_e157_4833_9766_ed8423c58fb3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| coupon_id | 券id | String | 32 | N | 券或者立减优惠id；<font color="green">示例值：2345234235</font> |
| name | 优惠名称 | String | 64 | N | <font color="green">示例值：八折券</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL: 全场代金券，SINGLE: 单品优惠；<font color="green">示例值：GLOBAL</font> |
| type | 优惠类型 | String | 32 | N | CASH:  充值型代金券<br/>NOCASH：免充值型代金券<br/><font color="green">示例值：CASH</font>  |
| amount | 优惠券面额 | String | 12 | Y | <font color="green">示例值：5.00</font> |
| stock_id | 活动ID | String | 32 | N | 活动ID |
| douyinpay_contribute | 抖音出资 | String | 32 | N | 抖音出资，单位为元；<br/><font color="green">示例值：10.00</font> |
| merchant_contribute | 商户出资 | String | 32 | N | 商户出资，单位为元；<br/><font color="green">示例值：10.00</font> |
| other_contribute | 其他出资 | String | 32 | N | 其他出资，单位为元；<font color="green">示例值：20.00</font> |
| currency | 优惠币种 | String | 32 | N | CNY：人民币，境内商户号仅支持人民币 |
| <span class="extend 90ac35c0_a9f6_4ad4_8edd_160d9c1301ac">goods_detail</span> | 单品列表 | Array |  | N | 单品信息，使用Json格式，是promotion_detail的元素； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 90ac35c0_a9f6_4ad4_8edd_160d9c1301ac-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码	 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| unit_price | 商品单价 | String | 32 | N | 单位为:元。<font color="green">示例值：99.00</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| goods_remark | 商品备注 | String | 128 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5b408f76_987f_498d_b2bb_2b568096a40b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 166438e7_b714_49f7_b8c3_207c2eb3e75f">acct_infos</span> | 分账明细 | Array | 2048 | Y | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 166438e7_b714_49f7_b8c3_207c2eb3e75f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120000</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| acct_date | 账务日期 | String | 8 | N | <font color="green">示例值：20221023</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 62baa955_813b_4b7c_b860_8a570e20fff2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| allowance_type | 补贴类型 | String | 10 | N | 0：不补贴，为空默认<br/>1：补贴<br/>2：部分补贴<br/>3：全额补贴(优惠后)<br/>4：部分补贴(优惠后)<br/><font color="green">示例值：2</font> |
| no_allowance_desc | 不补贴原因 | String | 128 | N | 补贴系统返回的不补贴原因；<br/>1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴<br/>2:额度用完<br/>3:不在有效期<br/>4:活动不存在<br/>5:手续费金额为0不补贴<br/>6:顶格优惠<br/>7:额度不足<br/>8:手续费后补<br/>9:未达到起始补贴金额<br/><font color="green">示例值：2</font> |
| <span class="extend 8184d04b_d3e1_46ed_9619_91b16309508f">cur_allowance_config_infos</span> | 手续费补贴活动详情 | Object |  | N | 补贴系统返回，斗拱原样返回； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8184d04b_d3e1_46ed_9619_91b16309508f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_id | 门店 | String | 64 | N | <font color="green">示例值：sh002</font> |
| merchant_group | 商户号 | String | 64 | N | <font color="green">示例值：6666000123120000</font> |
| allowance_sys | 补贴方 | String | 64 | Y | 1:银行  2:服务商 3:汇来米；<font color="green">示例值：1</font> |
| allowance_sys_id | 补贴方ID | String | 64 | Y | 对应补贴方的id；<font color="green">示例值：6666000123120000</font> |
| is_delay_allowance | 补贴类型 | String | 2 | Y | 1:实补  2:后补,默认实补；<font color="green">示例值：1</font> |
| market_id | 自定义活动编号 | String | 64 | Y | <font color="green">示例值：ISFE00232</font> |
| market_name | 自定义活动名称 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| market_desc | 自定义活动描述 | String | 64 | N | <font color="green">示例值：新店开业大促</font> |
| start_time | 活动开始时间 | String | 8 | Y | yyyyMMdd；<font color="green">示例值：20220909</font> |
| end_time | 活动结束时间 | String | 8 | Y | yyyyMMdd；<font color="green">示例值：20220913</font> |
| pos_debit_limit_amt | pos借记卡补贴额度 | String | 16 | Y | <font color="green">示例值：2.00</font> |
| pos_credit_limit_amt | pos贷记卡补贴额度 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| pos_limit_amt | pos补贴额度 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| qr_limit_amt | 扫码补贴额度 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| total_limit_amt | 活动总补贴额度 | String | 16 | Y | <font color="green">示例值：10.00</font> |
| status | 活动是否有效 | String | 4 | Y | 1:生效 0：失效；<font color="green">示例值：1</font> |
| human_flag | 是否人工操作 | String | 4 | Y | N：自动 Y：人工；<font color="green">示例值：N</font> |
| activity_id | 活动号 | String | 64 | Y | <font color="green">示例值：223402342</font> |
| activity_name | 活动描述 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| create_by | 创建人 | String | 32 | Y | <font color="green">示例值：Lg2022022201394910571</font> |
| create_time | 创建时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 22&#58;00&#58;30</font> |
| update_time | 更新时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 23&#58;00&#58;30</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table edb87cb5_788d_4a13_8224_a3f09bb50af5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| gate_type | 网关支付类型 | String | 2 | N | 01: 个人网关02:企业网关；<font color="green">示例值：02</font> |
| bank_id | 付款方银行号 | String | 32 | N | <font color="green">示例值：01040000</font> |
| pyer_acct_id | 付款方银行账户 | String | 1024 | N | B2B支付成功后可能返回密文；<font color="green">示例值：6226560119005276</font> |
| pyer_acct_nm | 付款方银行账户名 | String | 128 | N | <font color="green">示例值：上海汇付支付有限公司</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9fb69f20_3485_4028_b493_ff04ccc2ebcd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | Y | <font color="green">示例值：AMT*0.003</font> |
| fee_type | 手续费类型 | String | 32 | Y | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；<font color="green">示例值：ACCT_FEE</font> |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。<br/><font color="green">示例值：6850aad1e92f4244a74a42fcc1ad6360</font> |
<!-- extend:end -->


#### 业务返回码

常见错误码：

| <div style="width: 55pt">返回码</div>    | 返回描述                                                   | 处理                                               |
| :------- | :--------------------------------------------------------- | :------------------------------------------------- |
| 90000000 | 生成微信Scheme失败，errcode[40001],errmsg[invalid credential, access_token is invalid or not latest rid: xxxx]   | 小程序有变更或被微信封了，需要重新配置小程序 |
| 99010002 | 预下单请求流水重复  | 提供新的流水号 |

