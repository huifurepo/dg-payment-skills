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
## 抖音直连下单接口

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/preorder

*最近更新时间：2026.04.17*

### 应用场景
抖音直连下单接口

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
| pre_order_type | 预下单类型 | String | 1 | Y | 抖音直连下单：4；<font color="green">示例值：4</font> |
| req_date | 请求日期 | String | 8 | Y | 请求格式：yyyyMMdd；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944</font> |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成；<font color="green">示例值：6666000123123123</font> |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| goods_desc | 商品描述 | String | 40 | Y | <font color="green">示例值：个人电脑</font> |
| time_expire | 交易失效时间 | String | 14 | N | 请求格式：yyyyMMddHHmmss；<font color="green">示例值：20220912111230</font><br/>注意:为空默认失效时间为10分钟；用户在交易失效时间后完成交易有可能被关单。最终结果以异步为准；<br>建议商户在交易量大时，或在搞营销活动时将失效时间设置短一些。 |
| notify_url | 交易异步通知地址 | String | 512 | N | http或https开头，<font color="green">示例值：https://callback.service.com/xx</font><br/>在交易成功/失败时触发回调，正常情况下只会触发一次，具体回调策略参见[链接](https://paas.huifu.com/open/doc/api_standard/#/ybxx/jiekouguifan_ybxx) |
| <span class="extend 692debdd_83ca_48a7_8b46_3c38300aba3a">dy_data</span> | 抖音参数集合 | String | 2048 | Y | jsonObject字符串 |

<!-- extend:start -->
<!-- div:extend-table 692debdd_83ca_48a7_8b46_3c38300aba3a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | Y | 子商户/二级商户在抖音开放平台申请的应用ID，全局唯一。<br/>此处请填写移动应用类型的AppID，并确保该sub_appid与sub_mchid有绑定关系。<br/><font color="green">示例值：awofz9bncda6x7w8</font> |
| busi_scene | 业务场景 | String | 3 | Y | APP、H5；<font color="green">示例值：H5</font> |
| coupon_info | 优惠标记 | String |  | N | 1、json格式。和抖音支付协商后可用。<br/>2、传参说明：<br/>（1）业务场景区分，可通过传入key值=biz_scene，value值为约定场景值。<br/>（2）个性化策略区分，可通过传入key值=product_tag，value值为约定参数值。<br/>（3）指定优惠信息区分，可通过传入key值=assign_discounts，value值为“抖音支付优惠查询接口”返回的“指定优惠信息”字段值。<br/><font color="green">示例值：{"biz_scene":"xxx","product_tag":"xxx","assign_discounts":"xxx"}</font> |
| <span class="extend a26dd1be_d9a6_42bd_9cdd_7ef4cd4e2bf2">h5_info</span> | H5场景信息 | Object | 2048 | C | 业务场景为H5时必填 |
| <span class="extend 40cab3ca_73b5_4abb_a914_c428bdc52dd9">scene_info</span> | 场景信息 | Object | 2048 | Y | 支付场景描述 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table a26dd1be_d9a6_42bd_9cdd_7ef4cd4e2bf2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| type | 场景类型 | String | 32 | Y | Ios, Android, Wap<font color="green">示例值：Ios</font> |
| app_name | 应用名称 | String | 64 | N | <font color="green">示例值：抖音</font> |
| app_url | 网站URL | String | 128 | N | <font color="green">示例值：示例值：https://douyinpay.com/</font> |
| bundle_id | iOS平台BundleID | String | 128 | N |  |
| package_name | Android平台PackageName | String | 128 | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 40cab3ca_73b5_4abb_a914_c428bdc52dd9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| payer_client_ip | 用户终端IP | String | 45 | Y | 用户的客户端IP，支持IPv4和IPv6两种格式的IP地址<br/><font color="green">示例值：14.23.150.211</font> |
<!-- extend:end -->

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
| trans_amt | 交易金额 | String | 12 | Y | 预下单时传入，原样返回；<font color="green">示例值：100.00</font> |
| jump_url | 预支付会话标识 | String | 256 | Y | app场景：预支付交易会话标识。用于后续接口调用中使用，该值有效期为2小时；<br/><font color="green">示例值：{\\"package\\":\\"Sign=DYPay\\",\\"appid\\":\\"aaaa\\",\\"sign\\":\\"aa4Wec0=\\",\\"partnerid\\":\\"6660001\\",\\"prepayid\\":\\"dy12346\\",\\"noncestr\\":\\"628easdfadsf\\",\\"timestamp\\":\\"1770277075\\"}</font><br/>H5场景：拉起抖音支付收银台的中间页面，可通过访问该url来拉起抖音客户端，完成支付，h5_url的有效期为5分钟。<br/><font color="green">示例值：https://cashier.ulpay.com/bytepay-cashdesk/bytepay-invoke?prepay_id=dy96y894ox66yv43x10uquv34s5s7sx3oso28squqsx</font> |


#### 异步返回参数

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
| trans_type | 交易类型 | String | 20 | N | Y_APP：抖音APP支付；<br/>Y_H5：抖音H5支付；<br/><font color="green">示例值：Y_H5</font> |
| trans_amt | 交易金额 | String | 12 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| settlement_amt | 结算金额 | String | 16 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| trans_stat | 交易状态 | String | 1 | N | S：成功、F：失败；<font color="green">示例值：S</font> |
| trans_finish_time | 汇付侧交易完成时间 | String | 6 | N | 格式yyyyMMddHHmmss，<font color="green">示例值：20091225091010</font> |
| end_time | 支付完成时间 | String | 14 | N | 格式yyyyMMddHHmmss，<font color="green">示例值：20091225091010</font> |
| acct_date | 入账时间 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| <span class="extend f3bfb2c1_4eab_4b98_9d2c_4e480421eb33">dy_response</span> | 抖音返回的响应报文 | String |  | N | jsonObject字符串 |
| is_div | 是否分账交易 | String | 1 | Y | 1:  分账交易, 0:  非分账交易；<font color="green">示例值：1</font> |
| <span class="extend 07529eb8_339f_4eb3_90dc_60e0bbe39e26">acct_split_bunch</span> | 分账对象 | String | 2048 | N | 分账对象，jsonObject字符串 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | 1:  延迟   0:  不延迟；<font color="green">示例值：1</font> |
| fee_flag | 手续费扣款标志 | Int | 1 | N | 1:  外扣，2:  内扣；默认返回控台配置方式；<font color="green">示例值：2</font> |
| fee_amount | 手续费金额 | String | 16 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| <span class="extend 549eca2a_e9bd_438f_ae9b_31c2ac38cd95">trans_fee_allowance_info</span> | 手续费补贴信息 | Object | 6000 | N | jsonObject格式 |
| remark | 备注 | String | 45 | N | 原样返回；<font color="green">示例值：备注</font> |
| bank_code | 通道返回码 | String | 32 | N | <font color="green">示例值：00</font> |
| bank_message | 通道返回描述 | String | 200 | N | <font color="green">示例值：成功[0000000]</font> |
| bank_id | 收款方银行代号 | String | 8 | N | 快捷、网银返回；<font color="green">示例值：01040000</font> |
| <span class="extend 3b545615_8203_4656_9e05_e4abed3a7f86">bank_extend_param</span> | 银行扩展信息 | String |  | N | jsonObject格式；网银返回 |
| <span class="extend 175d7be8_ce6f_4ab0_98cc_c6a5f91b5940">fee_formula_infos</span> | 手续费费率信息 | String |  | N | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| order_type | 订单类型 | String | 1 | N | P-支付 R-充值 默认：P-支付；<font color="green">示例值：P</font> |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传；<font color="green">示例值：660035730311000126101</font> |
| request_ip | 请求IP | String | 15 | N | 付款方IP,仅在支付成功后返回;示例：192.168.1.1 |

<!-- extend:start -->
<!-- div:extend-table f3bfb2c1_4eab_4b98_9d2c_4e480421eb33-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | N | 在抖音开放平台申请的应用ID，全局唯一。此处请填写移动应用（APP）/网站应用（H5）类型的AppID |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：897ae8bd9f194107-9cb3-85f5672037de</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：823ae8bd9f893402-9cb3-85f8794657ea</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识<font color="green">示例值：OTHERS</font> |
| <span class="extend 3056dedb_334d_4ff3_bc74_143a4929dea6">promotion_detail</span> | 营销详情列表 | String |  | N | 营销详情列表，使返回值为Json格式； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3056dedb_334d_4ff3_bc74_143a4929dea6-table -->
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
| <span class="extend 28b19469_793e_414c_bf08_3eb56788aa99">goods_detail</span> | 单品列表 | Array |  | N | 单品信息，使用Json格式，是promotion_detail的元素； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 28b19469_793e_414c_bf08_3eb56788aa99-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码	 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| unit_price | 商品单价 | String | 32 | N | 单位为:元。<font color="green">示例值：99.00</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| goods_remark | 商品备注 | String | 128 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 07529eb8_339f_4eb3_90dc_60e0bbe39e26-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend d7a2a012_1d17_429e_9435_b4cac005f2ee">acct_infos</span> | 分账明细 | Array | 2048 | Y | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d7a2a012_1d17_429e_9435_b4cac005f2ee-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120000</font> |
| acct_id | 收款汇付账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：A14186488</font><br>仅支持微信、支付宝、网银交易指定收款账户； |
| acct_date | 账务日期 | String | 8 | N | <font color="green">示例值：20221023</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 549eca2a_e9bd_438f_ae9b_31c2ac38cd95-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| allowance_type | 补贴类型 | String | 10 | N | 0：不补贴，为空默认<br/>1：补贴<br/>2：部分补贴<br/>3：全额补贴(优惠后)<br/>4：部分补贴(优惠后)<br/><font color="green">示例值：2</font> |
| no_allowance_desc | 不补贴原因 | String | 128 | N | 补贴系统返回的不补贴原因；<br/>1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴<br/>2:额度用完<br/>3:不在有效期<br/>4:活动不存在<br/>5:手续费金额为0不补贴<br/>6:顶格优惠<br/>7:额度不足<br/>8:手续费后补<br/>9:未达到起始补贴金额<br/><font color="green">示例值：2</font> |
| <span class="extend 38702b43_e713_41f7_a8f3_0ac47e259ac7">cur_allowance_config_infos</span> | 手续费补贴活动详情 | Object |  | N | 补贴系统返回，斗拱原样返回； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 38702b43_e713_41f7_a8f3_0ac47e259ac7-table -->
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
<!-- div:extend-table 3b545615_8203_4656_9e05_e4abed3a7f86-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| gate_type | 网关支付类型 | String | 2 | N | 01: 个人网关02:企业网关；<font color="green">示例值：02</font> |
| bank_id | 付款方银行号 | String | 32 | N | <font color="green">示例值：01040000</font> |
| pyer_acct_id | 付款方银行账户 | String | 1024 | N | B2B支付成功后可能返回密文；<font color="green">示例值：6226560119005276</font> |
| pyer_acct_nm | 付款方银行账户名 | String | 128 | N | <font color="green">示例值：上海汇付支付有限公司</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 175d7be8_ce6f_4ab0_98cc_c6a5f91b5940-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | Y | <font color="green">示例值：AMT*0.003</font> |
| fee_type | 手续费类型 | String | 32 | Y | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；<font color="green">示例值：ACCT_FEE</font> |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。<br/><font color="green">示例值：6850aad1e92f4244a74a42fcc1ad6360</font> |
<!-- extend:end -->
