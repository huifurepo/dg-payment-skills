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
## 拆单支付订单查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/splitpay/query

*最近更新时间：2026.10.10*
### 应用场景
拆单支付的交易可以通过本接口查询。

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
| org_req_date | 原交易请求日期 | String | 8 | Y | 请求格式：yyyyMMdd；<font color="green">示例值：20221023</font> |
| org_req_seq_id | 原交易请求流水号 | String | 64 | Y | <font color="green">示例值：rQ2021121311173944</font> |


#### 请求示例

```json
{
    "sys_id": "6666000123123123",
    "product_id": "SPIN",
    "data": {
        "huifu_id":"6666000109133323",  
        "req_date":"20231020",  
        "req_seq_id":"202310201652361987182513",  
        "org_req_seq_id":"202310201652361987182512",  
        "org_req_date":"20231020"
    },
    "sign": "dJCZn/tVUuzKh13ACOAcCSl/E6OvR018DXX1FZjqXVjQ5qpezzsEK7CJZRo91QFioC4EF/kI1ju04wlCBrRus7+/axbIXJlCAsNBR4Ixwz6N0gc1V8U0zB3jsDfOXYZleJKhcju3M+bJJ/5ne+LbvKhP8L0R3Fpc4+P7PH5Vf2Of7DDwyWApqstr75IppK/h8JedI8yt1lfQD5d2AEg5n8aGAmGMyy9V17UfcH153BSqP8gsJACKlkfEep2hQnR+2MG+wwvkfZReQKcpR3NgMAlGpcxyFRUF3X1nor/Cz5N9rxZW2IjNHmVZ9EMcIJKdby55RLkBf3b2kYZrCaHCTQ=="
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
| resp_code | 业务响应码 | String | 8 | Y | [参见业务返回码](http://paas.huifutest.com/partners/api/#/smzf/api_qrpay_cx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [参见业务返回码](http://paas.huifutest.com/partners/api/#/smzf/api_qrpay_cx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；<font color="green">示例值：操作成功</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| req_date | 请求日期 | String | 8 | Y | 请求格式：yyyyMMdd；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 64 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220125</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | <font color="green">示例值：202110210012100005</font> |
| pre_order_id | 预下单订单号 | String | 64 | Y | <font color="green">示例值：H2025102809433100508209050</font> |
| order_stat | 预下单状态 | String | 1 | N | 1:支付成功,2:支付中,3:已退款,4:处理中,5:支付失败,6-部分退款<br/>[参见状态说明文档](http://paas.huifu.com/open/doc/api/#/cpjs/api_cpjs_statsm)；<font color="green">示例值：1</font> |
| <span class="extend d3533183_2ad3_4e76_be80_ba715a0dab36">trans_list</span> | 拆单支付列表 | String |  | N | jsonArray格式 |

<!-- extend:start -->
<!-- div:extend-table d3533183_2ad3_4e76_be80_ba715a0dab36-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_type | 交易类型 | String | 16 | N | T_MINIAPP：微信小程序支付<br/>A_NATIVE ：支付宝正扫<br/><font color="green">示例值：T_JSAPI</font> |
| org_hf_seq_id | 原机构请求流水号 | String | 128 | N | <font color="green">示例值：00290TOP1GR210919004230P853ac13262200000</font> |
| trans_amt | 交易金额(元) | String | 14 | N | 保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | <font color="green">示例值：03232109190255105603561</font>；[参见用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| fee_amt | 手续费金额(元) | String | 14 | N | 保留小数点后两位，最低传入0.01。<font color="green">示例值：1.00</font> |
| ref_amt | 可退金额(元) | String | 14 | N | <font color="green">示例值：1.00</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中；S：成功；F：失败；I: 初始；<font color="green">示例值：S</font><br/>初始状态很罕见，请联系汇付技术人员处理 |
| trans_time | 交易时间 | String | 14 | N | 格式：yyyymmddHHMMSS；<font color="green">示例值：20231112200913</font> |
| bank_code | 外部通道返回码 | String | 32 | N | <font color="green">示例值：TRADE_SUCCESS</font> |
| bank_desc | 外部通道返回描述 | String | 200 | N | <font color="green">示例值：TRADE_SUCCESS</font> |
| <span class="extend 73e80540_a47e_4b07_9990_7e9ecf842c93">wx_response</span> | 微信返回的响应报文 | String | 6000 | N | jsonObject格式 |
| <span class="extend 086c7285_2a3b_4229_9299_e71f8062eab6">alipay_response</span> | 支付宝返回的响应报文 | String | 6000 | N | jsonObject格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 73e80540_a47e_4b07_9990_7e9ecf842c93-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| sub_appid | 子商户公众账号ID | String | 32 | N | 微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/wiki/doc/apiv3/terms_definition/chapter1_1_3.shtml#part-7)；<font color="green">示例值：OTHERS</font> |
| cash_fee | 现金支付金额 | String | 12 | N | 订单现金支付金额；<font color="green">示例值：10.00</font> |
| coupon_fee | 代金券金额 | String | 12 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend 2637a378_df79_4774_b4a8_2b86739c7c55">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 营销详情列表，使返回值为Json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2637a378_df79_4774_b4a8_2b86739c7c55-table -->
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
| <span class="extend 51fad1b5_ff55_4a70_93b3_d6734eba2cce">goods_detail</span> | 单品列表 | Object | 3000 | N | 使用Json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 51fad1b5_ff55_4a70_93b3_d6734eba2cce-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格 | String | 32 | Y | 单位为:  元。<font color="green">示例值：50.00</font><br/>如果商户有优惠，需传输商户优惠后的单价(例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50) |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 086c7285_2a3b_4229_9299_e71f8062eab6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 6d701785_132f_44f3_a2c8_24d6d5470c91">voucher_detail_list</span> | 优惠券信息 | Array |  | N | 本交易支付时使用的所有优惠券信息 |
| <span class="extend f4683e50_a068_4929_b68f_7cf07d2a552b">fund_bill_list</span> | 支付金额信息 | Object | 512 | N | 支付成功的各个渠道金额信息，详见资金明细信息说明；json格式 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 2088开头的16位纯数字；<font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| hb_fq_seller_percent | 卖家承担的手续费 | String | 3 | N | <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6d701785_132f_44f3_a2c8_24d6d5470c91-table -->
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
<!-- div:extend-table f4683e50_a068_4929_b68f_7cf07d2a552b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行代码 | String | 10 | N | 银行卡支付时的银行代码；<font color="green">示例值：CEB</font>；请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "huifu_id": "6666000003100615",
        "order_stat": "3",
        "org_req_date": "20251127",
        "org_req_seq_id": "rQ1764226397389",
        "pre_order_id": "H2025112714531800508693030",
        "product_id": "MYPAY",
        "req_date": "20251224",
        "req_seq_id": "rQ1766558521838111111111111111",
        "trans_list": "[{\"pay_type\":\"A_JSAPI\",\"org_hf_seq_id\":\"0150default251127145743P101c0a8321400000\",\"trans_amt\":\"0.02\",\"party_order_id\":\"03012511275386432300325\",\"fee_amt\":\"0.01\",\"ref_amt\":\"0.00\",\"trans_stat\":\"S\",\"trans_time\":\"20251127145938\",\"bank_code\":\"TRADE_SUCCESS\",\"bank_desc\":\"TRADE_SUCCESS\",\"alipay_response\":\"{\\\"fund_bill_list\\\":[{}],\\\"buyer_id\\\":\\\"2088932891702573\\\",\\\"buyer_logon_id\\\":\\\"839***%40qq.com\\\"}\"}]"
    }
}
```
