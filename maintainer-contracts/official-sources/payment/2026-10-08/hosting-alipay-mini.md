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
## 支付宝小程序预下单接口

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/preorder

*最近更新时间：2026.09.03*
### 应用场景
支付宝小程序预下单接口，可以满足商户或服务商在app拉起支付宝支付的需求。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共请求参数


| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sys_id     | 系统号     | String   | 32       | Y        | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font>|
| product_id | 产品号     | String   | 32       | Y        | 汇付分配的产品号，<font color="green">示例值：YYZY</font> |
| sign       | 加签结果   | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)  |
| data       | 请求数据   | JSON     |          | Y        | 业务请求参数，具体值参考API文档                              |



### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成；<font color="green">示例值：6666000123123123</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| req_date | 请求日期 | String | 8 | Y | 请求格式：yyyyMMdd；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| req_seq_id | 请求流水号 | String | 64 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944</font> |
| pre_order_type | 预下单类型 | String | 1 | Y | 支付宝预下单：2；<font color="green">示例值：2</font> |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| goods_desc | 商品描述 | String | 40 | Y | <font color="green">示例值：个人电脑</font> |
| delay_acct_flag | 是否延迟交易 | String | 1 | N | Y 为延迟 N为不延迟，不传默认N；<font color="green">示例值：N</font> |
| <span class="extend 486d5b40_5abf_43a6_b7df_5c4fc862c1bf">acct_split_bunch</span> | 分账对象 | String | 2000 | N | 分账对象，jsonObject字符串 |
| <span class="extend c87c3e10_b0b1_4733_a25a_b61f89739b74">hosting_data</span> | 统一收银台扩展参数集合 | String | 2000 | N | jsonObject统一收银台扩展参数集合 |
| <span class="extend 89f3467b_ba2b_465b_a6cb_ad07b1addac7">app_data</span> | app扩展参数集合 | String | 2000 | Y | app扩展参数 |
| time_expire | 交易失效时间 | String | 14 | N | 请求格式：yyyyMMddHHmmss；<font color="green">示例值：20220912111230</font><br/>注意:为空默认失效时间为10分钟；用户在交易失效时间后完成交易有可能被关单。最终结果以异步为准；<br>建议商户在交易量大时，或在搞营销活动时将失效时间设置短一些。 |
| <span class="extend 6719a7eb_e695_4321_8767_f50aee6a9beb">biz_info</span> | 业务信息 | String | 2000 | N | jsonObject格式；交易相关的信息 |
| notify_url | 异步通知地址 | String | 512 | N | 交易异步通知地址，http或https开头，<font color="green">示例值：https://callback.service.com/xx</font><br/>在交易成功/失败时触发回调，正常情况下只会触发一次，具体回调策略参见[链接](https://paas.huifu.com/open/doc/api_standard/#/ybxx/jiekouguifan_ybxx) |
| <span class="extend a35c28a9_f4c6_41cb_b33d_ecd8b6f3c3ba">alipay_data</span> | 支付宝参数集合 | String | 2048 | N | jsonObject字符串 |
| <span class="extend 606d3239_badf_48ef_a8b9_0053fd268ad0">terminal_device_data</span> | 设备信息 | String | 2048 | N | jsonObject字符串 |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。<br/><font color="green">示例值：6850aad1e92f4244a74a42fcc1ad6360</font> |
| fee_split_flag | 是否交易手续费分摊 | String | 1 | N | Y-分摊，N-不分摊，不传默认为N。<font color="green">示例值：N</font> |
| fee_flag | 手续费扣款标志 | String | 1 | N | 1: 外扣 2: 内扣 (默认取控台配置值)；<font color="green">示例值：1</font> |
| channel_no | 渠道号 | String | 32 | N | 如果交易走自有渠道请联系联调群运维人员获取；<font color="green">示例值:10000001</font> |
| pay_scene | 场景类型 | String | 2 | N | 取值参见[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%BE%AE%E4%BF%A1%E4%B8%9A%E5%8A%A1%E5%BC%80%E9%80%9A%E7%B1%BB%E5%9E%8B)说明；<font color="green">示例值:02</font><br/>pay_scene需和channel_no配合使用。在指定channel_no的情况下需要传入pay_scene取值；为空取默认配置  |

<!-- extend:start -->
<!-- div:extend-table 486d5b40_5abf_43a6_b7df_5c4fc862c1bf-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 111355cc_120e_4fcf_8f41_9413ca47503d">acct_infos</span> | 分账明细 | Array |  | N | 分账明细 |
| percentage_flag | 百分比分账标志 | String | 1 | N |  Y:使用百分比分账；<font color="green">示例值：Y</font> |
| is_clean_split | 是否净值分账 | String | 1 | N | Y:使用净值分账，仅在交易手续费内扣且使用百分比分账时起作用；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 111355cc_120e_4fcf_8f41_9413ca47503d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | N | 斗拱开户时生成；<font color="green">示例值：6666000111546360</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| percentage_div | 分账百分比% | String | 6 | N |  <font color="green">示例值：23.50</font>，表示23.50%。仅在percentage_flag=Y时起作用<br>acct_infos中全部分账百分比只和必须为100.00%。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c87c3e10_b0b1_4733_a25a_b61f89739b74-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| project_id | 项目号 | String | 32 | N | 商户创建的项目号；<font color="green">示例值：PROJECTID2022032912492559</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 89f3467b_ba2b_465b_a6cb_ad07b1addac7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| appid | 支付宝小程序ID | String | 32 | N | 支付宝小程序appid，托管支付宝小程序时上送；<font color="green">示例值：2088xxxxxxxx</font> |
| app_schema | 小程序返回码 | String | 100 | Y | 小程序完成支付后需要返回所填写的AppScheme，返回App必填信息。<br/><font color="green">示例值：https://callback.service.com/xx</font></br>注：参数过长容易导致浏览器截取跳转地址，无法唤起收银台，限100字符。 <br/>**如果地址中有“+/?%#&=”字符需要进行编码操作** |
| private_info | 私有信息 | String | 255 | N | 对应异步通知和主动查询接口中的remark字段；<font color="green">示例值：收取服务费</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6719a7eb_e695_4321_8767_f50aee6a9beb-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend bcb041f4_f48b_4164_8104_a27e3a9a32a6">payer_check_ali</span> | 付款人验证（支付宝） | Object |  | N | 支付宝特殊交易需验证买家信息；如彩票行业等；<br/>当前只支持AT类交易有验证功能； |
| <span class="extend 1fb821f7_c1a7_400c_b4ab_dc6918c77f74">person_payer</span> | 个人付款人信息 | Object |  | N | 付款人验证打开后需要填写付款人信息，但非必填；微信/支付宝共用字段； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bcb041f4_f48b_4164_8104_a27e3a9a32a6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| need_check_info | 是否提供校验身份信息 | String | 1 | N | T：强制校验，需要填写person_payer字段；F：不强制；<font color="green">示例值：T</font> |
| min_age | 允许的最小买家年龄 | String | 3 | N | 买家年龄必须大于等于所传数值。<font color="green">示例值：18</font><br/>注：1. need_check_info=T 时该参数才有效，<br/>2. min_age 为整数，必须大于等于 0； |
| fix_buyer | 是否强制校验付款人身份信息 | String | 8 | N | 用户进行实名认证校验；T：强制校验，F：不强制；<font color="green">示例值：T</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1fb821f7_c1a7_400c_b4ab_dc6918c77f74-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| name | 姓名 | String | 16 | N | 注：支付宝交易need_check_info=T时，该参数才有效；<font color="green">示例值：张三</font> |
| cert_type | 证件类型 | String | 32 | N | 身份证：IDENTITY_CARD，<br/>护照：PASSPORT；<br/>军官证：OFFICER_CARD，<br/>士兵证：SOLDIER_CARD；<br/>户口本：HOKOU；<br/><font color="green">示例值：IDENTITY_CARD</font> <br/>注：支付宝交易need_check_info=T时，该参数才有效 |
| cert_no | 证件号 | String | 64 | N | 注：支付宝交易need_check_info=T时，该参数才有效；需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。<br/><font color="green">示例值：Mc5pjf+b/Keyi/t/wnH……MfYQnK7Lzw==</font> |
| mobile | 手机号 | String | 20 | N | 注：该参数暂不校验；<font color="green">示例值：13911111111</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a35c28a9_f4c6_41cb_b33d_ecd8b6f3c3ba-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| alipay_store_id | 支付宝的店铺编号 | String | 32 | N | <font color="green">示例值：2016041400077000000003314986</font> |
| <span class="extend 142b4c38_f148_49f3_bd96_cdee8566a0be">extend_params</span> | 业务扩展参数 | Object | 2048 | N | 业务扩展参数 |
| <span class="extend eab0a717_0178_44c6_aa46_55151bea0d91">goods_detail</span> | 订单包含的商品列表信息 | Array | 2048 | N | 订单包含的商品列表信息 |
| merchant_order_no | 商户原始订单号 | String | 32 | N | <font color="green">示例值：39045032345</font> |
| operator_id | 商户操作员编号 | String | 28 | N | <font color="green">示例值：carl.li@huifu.com</font> |
| product_code | 产品码 | String | 32 | N | 商家和支付宝签约的产品码。小程序场景支付：JSAPI_PAY；当面付场景：FACE_TO_FACE_PAYMENT；<font color="green">示例值：JSAPI_PAY</font> |
| seller_id | 卖家支付宝用户号 | String | 28 | N | <font color="green">示例值：20880414938706770000</font> |
| store_id | 商户门店编号 | String | 32 | N | <font color="green">示例值：sh1001</font> |
| subject | 订单标题 | String | 256 | N | 直连模式必填；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；<font color="green">示例值：红果奶茶</font> |
| store_name | 商家门店名称 | String | 512 | N | 直连模式字段；<font color="green">示例值：红果奶茶上海宝山店</font> |
| ali_business_params | 商户业务信息 | String | 512 | N | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| fq_mer_discount_flag | 商户贴息标记 | String |  | N | 花呗分期商户补贴活动，Y：商户全额贴息，P：商户部分贴息，不传为非商户贴息（默认）；<br/><font color="green">示例值：P</font><br/>选择P：商户部分贴息活动，需同时在【ali_business_params：商户业务信息】中传入支付宝约定的活动参数，参数说明详见分期支付指引文档。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 142b4c38_f148_49f3_bd96_cdee8566a0be-table -->
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
<!-- div:extend-table eab0a717_0178_44c6_aa46_55151bea0d91-table -->
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
<!-- div:extend-table 606d3239_badf_48ef_a8b9_0053fd268ad0-table -->
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
        "delay_acct_flag": "N",
        "req_seq_id": "20240514165442868h32ss2g3s7vnxq",
        "req_date": "20240514",
        "trans_amt": "0.10",
        "huifu_id": "6666000109133323",
        "goods_desc": "app跳支付宝消费",
        "pre_order_type": "2",
        "app_data": "{\"app_schema\":\"app跳转链接\"}",
        "notify_url": "https://callback.service.com/xx",
        "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000109133323\",\"div_amt\":\"0.08\"}]}"
    },
    "sign": "ICrhwXXkR5kP52v+DesNIpfVUNw32TyEy6IlnW9tfdQxeHDrGP+i+BESYcK/JCafw8IX7vsd1vx7gX/WcFmrcS1XZNXC8Zuvxej5S8d4SIpvwPxY3m8UdmubM84vZvc7DPFKwNtuceLTgadcG82tCHXOTVNSLrfFBa+vEvhbxfZBT4Fh2gMlfwbB2+2d7t/oF0kIdmmYCq/jZ3a3HDSt3M8OgpW0liOkWZ+OlfUP8LNpokO42kJ4DGNBsThmHfGlEpnCTPHN0gl17ZGo+AKUv8XyG+JjyfOo2o3thrgVa5iLt7fdhudj56Uy4v63q2YE+knSVsyx3HxOGTHFDyhFMw=="
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
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 128 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| req_date | 请求日期 | String | 8 | Y | 预下单时传入，原样返回；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 预下单时传入，原样返回；<font color="green">示例值：20220424561166000</font> |
| huifu_id | 商户号 | String | 32 | Y | 预下单时传入，原样返回；<font color="green">示例值：6666000111546360</font> |
| trans_amt | 交易金额 | String | 12 | Y | 预下单时传入，原样返回；<font color="green">示例值：100.00</font> |
| jump_url | 支付跳转链接 | String | 256 | Y | 用于app跳转支付宝时使用；<font color="green">示例值：https://callback.service.com/xx</font> |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code":"00000000",
        "resp_desc":"交易成功",
        "req_date":"20220424",
        "req_seq_id":"20220424561166000",
        "huifu_id":"6666000111546360",
        "trans_amt":"0.10",
        "jump_url":"alipays://platformapi/startapp?appId=2021003121605466&thirdPartSchema=app跳转链接&page=pages/cashier/cashier?p%3DH2022042814245600912499897%26s%3Dapp"
    }
}
```


#### 异步返回参数

**resp_data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回信息 | String | 512 | Y | 业务返回描述；<font color="green">示例值：处理成功</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000111546360</font> |
| req_date | 请求时间 | String | 8 | Y | 交易时传入，原样返回，格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 交易时传入，原样返回；<font color="green">示例值：20220424561166000</font> |
| hf_seq_id | 全局流水号 | String | 40 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| out_trans_id | 用户账单上的交易订单号 | String | 64 | N | <font color="green">示例值：092021091922001451301445517582</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | <font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| trans_type | 交易类型 | String | 20 | N | T_JSAPI:  微信公众号支付<br/>T_MINIAPP:  微信小程序支付  <br/>A_JSAPI:  支付宝JS  <br/>A_NATIVE:  支付宝正扫  <br/>U_NATIVE:  银联正扫  <br/>U_JSAPI:  银联 JS  <br/>T_MICROPAY:  微信反扫  <br/>A_MICROPAY:  支付宝反扫  <br/>U_MICROPAY:  银联反扫  <br/>D_NATIVE:  数字人民币正扫  <br/>D_MICROPAY:  数字人民币反扫<br/><font color="green">示例值：D_NATIVE</font> |
| trans_amt | 交易金额 | String | 12 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| settlement_amt | 结算金额 | String | 16 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| trans_stat | 交易状态 | String | 1 | N | S：成功、F：失败，<font color="green">示例值：S</font> |
| trans_finish_time | 汇付侧交易完成时间 | String | 6 | N | 格式yyyyMMddHHmmss，<font color="green">示例值：20091225091010</font> |
| end_time | 支付完成时间 | String | 14 | N | 格式yyyyMMddHHmmss，<font color="green">示例值：20091225091010</font> |
| acct_date | 入账时间 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| debit_flag | 借贷记标识 | String | 1 | N | D-借记卡   C-信用卡   Z-借贷合一卡，<font color="green">示例值：D</font> |
| <span class="extend d05f2184_9df8_4b3b_aa31_87d046d170f8">alipay_response</span> | 支付宝返回的响应报文 | String | 6000 | N | Json格式 |
| is_div | 是否分账交易 | String | 1 | Y | 1:  分账交易, 0:  非分账交易；<font color="green">示例值：1</font> |
| <span class="extend 4ec510d5_f2e1_4c98_82b5_6a4d6004f96a">acct_split_bunch</span> | 分账对象 | String | 2048 | N | 分账对象，jsonObject字符串 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | 1:  延迟   0:  不延迟，<font color="green">示例值：1</font> |
| fee_flag | 手续费扣款标志 | Int | 1 | N | 1:  外扣    2:  内扣；默认返回控台配置方式 ，<font color="green">示例值：2</font> |
| <span class="extend abcaac3e_b722_4f07_93ac_071b473e2370">trans_fee_allowance_info</span> | 手续费补贴信息 | String | 6000 | N | Json格式 |
| <span class="extend dacf0fe3_79c4_45b5_9f54_774c3137dbcf">fee_formula_infos</span> | 手续费费率信息 | String |  | N | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| remark | 备注 | String | 45 | N | 原样返回，<font color="green">示例值：备注</font> |
| bank_code | 通道返回码 | String | 32 | N | <font color="green">示例值：00</font> |
| bank_message | 通道返回描述 | String | 200 | N | <font color="green">示例值：成功[0000000]</font> |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传；<font color="green">示例值：660035730311000126101</font> |

<!-- extend:start -->
<!-- div:extend-table d05f2184_9df8_4b3b_aa31_87d046d170f8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 0e7cb343_5c43_438d_b5f2_12b4447db983">voucher_detail_list</span> | 本交易支付时使用的所有优惠券信息 | Array |  | N | 本交易支付时使用的所有优惠券信息 |
| <span class="extend ee4efedd_0118_44fe_ae84_adf9d06a7086">fund_bill_list</span> | 支付金额信息 | String | 512 | N | 支付成功的各个渠道金额信息，详见资金明细信息说明 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 2088开头的16位纯数字；<font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| hb_fq_seller_percent | 卖家承担的手续费 | String | 3 | N | <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0e7cb343_5c43_438d_b5f2_12b4447db983-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 券id | String | 32 | Y | <font color="green">示例值：6934572310301</font> |
| name | 券名称 | String | 32 | Y | <font color="green">示例值：实体店付款通用立减券</font> |
| type | 券类型 | String | 32 | Y | 当前有三种类型：    <br />ALIPAY_FIX_VOUCHER:  全场代金券<br />ALIPAY_DISCOUNT_VOUCHER:  折扣券<br />ALIPAY_ITEM_VOUCHER:  单品优惠<br /><font color="green">示例值：ALIPAY_ITEM_VOUCHER</font> <br />注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| amount | 优惠券面额 | String | 8 | Y | 优惠券面额，它应该会等于商家出资加上其他出资方出资；<font color="green">示例值：10.00</font> |
| merchant_contribute | 商家出资（特指发起交易的商家出资金额） | String | 8 | N | 商家出资（特指发起交易的商家出资金额）；<font color="green">示例值：10.00</font> |
| other_contribute | 其他出资方出资金额 | String | 11 | N | 可能是支付宝、品牌商、第三方，也可能是他们的一起出资；<br/><font color="green">示例值：0.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ee4efedd_0118_44fe_ae84_adf9d06a7086-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行卡支付时的银行代码 | String | 10 | N | 银行卡支付时的银行代码；<font color="green">示例值：CEB</font>；请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 4ec510d5_f2e1_4c98_82b5_6a4d6004f96a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 3e904762_5c93_444a_bbbf_0832406c7b91">acct_infos</span> | 分账明细 | Array | 2048 | Y | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3e904762_5c93_444a_bbbf_0832406c7b91-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120000</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| acct_date | 账务日期 | String | 8 | N | <font color="green">示例值：20221023</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table abcaac3e_b722_4f07_93ac_071b473e2370-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| allowance_type | 补贴类型 | String | 10 | N | 0：不补贴，为空默认<br/>1：补贴<br/>2：部分补贴<br/>3：全额补贴(优惠后)<br/>4：部分补贴(优惠后)<br/><font color="green">示例值：2</font> |
| no_allowance_desc | 不补贴原因 | String | 128 | N | 补贴系统返回的不补贴原因<br/>1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴<br/>2:额度用完<br/>3:不在有效期<br/>4:活动不存在<br/>5:手续费金额为0不补贴<br/>6:顶格优惠<br/>7:额度不足<br/>8:手续费后补<br/>9:未达到起始补贴金额<br/><font color="green">示例值：2</font> |
| <span class="extend 855f0f29_0cc8_4848_8eb7_204d85243e82">cur_allowance_config_infos</span> | 手续费补贴活动详情 | Object |  | N | 补贴系统返回，斗拱原样返回 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 855f0f29_0cc8_4848_8eb7_204d85243e82-table -->
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
| end_time | 活动结束时间 | String | 8 | Y | yyyyMMdd；<font color="green">示例值：20220911</font> |
| pos_debit_limit_amt | pos借记卡补贴额度 | String | 16 | Y | <font color="green">示例值：2.00</font> |
| pos_credit_limit_amt | pos贷记卡补贴额度 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| pos_limit_amt | pos补贴额度 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| qr_limit_amt | 扫码补贴额度 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| total_limit_amt | 活动总补贴额度 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| status | 活动是否有效 | String | 4 | Y | 1:生效 0：失效；<font color="green">示例值：1</font> |
| human_flag | 是否人工操作 | String | 4 | Y | N：自动 Y：人工 |
| activity_id | 活动号 | String | 64 | Y | <font color="green">示例值：223402342</font> |
| activity_name | 活动描述 | String | 128 | N | <font color="green">示例值：开业大促</font> |
| create_by | 创建人 | String | 32 | Y | <font color="green">示例值：Lg2022022201394910571</font> |
| create_time | 创建时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 22&#58;00&#58;30</font> |
| update_time | 更新时间 | String | 32 | Y | <font color="green">示例值：2022-04-14 23&#58;00&#58;30</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table dacf0fe3_79c4_45b5_9f54_774c3137dbcf-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | Y | <font color="green">示例值：AMT*0.003</font> |
| fee_type | 手续费类型 | String | 32 | Y | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；<font color="green">示例值：ACCT_FEE</font> |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。<br/><font color="green">示例值：6850aad1e92f4244a74a42fcc1ad6360</font> |
<!-- extend:end -->


#### 业务返回码

常见错误码：

| 返回码   | 返回描述                                                   | 处理                                               |
| :------- | :--------------------------------------------------------- | :------------------------------------------------- |
| 99010002 | 预下单请求流水重复  | 提供新的流水号 |

