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
## 统一收银台交易查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/queryorderinfo

*最近更新时间：2026.05.27*
### 应用场景
通过统一收银台预下单接口支付的交易都可以通过本接口查询。

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
| huifu_id | 商户号 | String | 32 | C | 开户自动生成；商户号不填时必填party_order_id；<font color="green">示例值：6666000123123123</font> |
| org_req_date | 原交易请求日期 | String | 8 | C | 请求格式：yyyyMMdd；该字段不填时必填party_order_id；<font color="green">示例值：20221023</font> |
| org_req_seq_id | 原交易请求流水号 | String | 64 | C | 该字段不填时必填party_order_id；<font color="green">示例值：rQ2021121311173944</font> |
| party_order_id | 用户账单上的商户订单号 | String | 64 | C | 该字段不填时，商户号、原交易请求日期、原交易请求流水号必填；<font color="green">示例值：03232109190255105603561</font> |


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
| org_req_date | 原机构请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220125</font> |
| org_req_seq_id | 原机构请求流水号 | String | 128 | N | <font color="green">示例值：202110210012100005</font> |
| org_hf_seq_id | 斗拱返回的全局流水号 | String | 128 | N | <font color="green">示例值：00290TOP1GR210919004230P853ac13262200000</font> |
| pre_order_id | 预下单订单号 | String | 64 | Y | <font color="green">示例值：H2022050711225100912503288</font> |
| order_stat | 预下单状态 | String | 1 | N | 1:支付成功,2:支付中,3:已退款,4:处理中,5:支付失败,6-部分退款<br/>[参见状态说明文档](http://paas.huifu.com/open/doc/api/#/cpjs/api_cpjs_statsm)；<font color="green">示例值：1</font> |
| party_order_id | 用户账单上的商户订单号 | String | 64 | N | <font color="green">示例值：03232109190255105603561</font>；[参见用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| trans_date | 订单日期 | String | 8 | Y | 格式：yyyymmdd；<font color="green">示例值：20221023</font> |
| trans_amt | 交易金额(元) | String | 14 | Y | 保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| pay_type | 交易类型 | String | 16 | N | T_JSAPI：微信公众号支付<br>T_MINIAPP：微信小程序支付<br>A_JSAPI：支付宝JS<br>A_NATIVE ：支付宝正扫<br>U_NATIVE：银联正扫<br>U_JSAPI：银联 JS<br>QUICK_PAY：快捷支付、快捷充值(查询快捷交易必填)<br>ONLINE_PAY_B2B：B2B网银支付<br/>ONLINE_PAY_B2C：B2C网银支付<br>UNION_PAY：银联APP统一支付<br>Y_H5：抖音H5支付<br><font color="green">示例值：ONLINE_PAY_B2C</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中；S：成功；F：失败；I: 初始；<font color="green">示例值：S</font><br/>初始状态很罕见，请联系汇付技术人员处理 |
| trans_time | 交易时间 | String | 14 | N | 格式：yyyymmddHHMMSS；<font color="green">示例值：20231112200913</font> |
| close_stat | 关单状态 | String | 1 | N | P：处理中、S：成功、F：失败；<font color="green">示例值：S</font> |
| fee_flag | 手续费扣款标志 | Int | 1 | N | 1: 外扣，2: 内扣；默认返回控台配置方式；示例值：2 |
| fee_amt | 手续费金额(元) | String | 14 | N | 保留小数点后两位，最低传入0.01。<font color="green">示例值：1.00</font> |
| ref_amt | 可退金额(元) | String | 14 | N | <font color="green">示例值：1.00</font> |
| goods_desc | 商品描述 | String | 40 | N | <font color="green">示例值：电脑PC</font> |
| remark | 备注 | String | 255 | N | 原样返回；<font color="green">示例值：备注</font> |
| mer_priv | 商户私有域 | String | 1500 | N | <font color="green">示例值：商户私有域</font> |
| bank_code | 外部通道返回码 | String | 32 | N | <font color="green">示例值：TRADE_SUCCESS</font> |
| bank_desc | 外部通道返回描述 | String | 200 | N | <font color="green">示例值：TRADE_SUCCESS</font> |
| <span class="extend df3f3656_efdb_449b_b1f3_c165941cdc3a">wx_response</span> | 微信返回的响应报文 | String | 6000 | N | jsonObject格式 |
| <span class="extend 1106d3e2_73fa_4a43_ac92_d843c1c61677">alipay_response</span> | 支付宝返回的响应报文 | String | 6000 | N | jsonObject格式 |
| <span class="extend 65186012_90ad_459a_84eb_8d49e187f6a7">unionpay_response</span> | 银联返回的响应报文 | String | 6000 | N | jsonObject格式 |
| wx_user_id | 微信用户唯一标识码 | String | 128 | N | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| <span class="extend bf5d28ab_9c4a_4611_9760_1f3b9a59ac65">dy_response</span> | 抖音返回的响应报文 | String |  | N | jsonObject字符串 |
| is_div | 是否分账交易 | String | 1 | Y | Y: 分账交易, N: 非分账交易；示例值：N |
| <span class="extend 0115b045_1163_4d63_b331_8ffaf6fa6cf8">acct_split_bunch</span> | 分账对象 | String | 2048 | N | 分账信息，jsonObject字符串 |
| is_delay_acct | 是否延时交易 | String | 1 | Y | Y: 延迟 N: 不延迟；示例值：N |
| <span class="extend 83233203_8373_43d1_91e4_5e755641e05e">trans_fee_allowance_info</span> | 手续费补贴信息 | String | 6000 | N | 手续费补贴信息，jsonObject字符串 |
| <span class="extend b6376f21_898b_481e_a6e6_cff0135d9ca2">quick_online_response</span> | 快捷网银响应 | String | 6000 | N | 新设计的域字段 |
| <span class="extend d2358263_535a_4f31_adbd_6f828514a889">bank_extend_param</span> | 银行扩展信息 | String |  | N | jsonObject格式；网银返回 |
| <span class="extend 5086b719_d004_448c_86e1_ddfd2df62086">fee_formula_infos</span> | 手续费费率信息 | String |  | N | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| devs_id | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传；<font color="green">示例值：660035730311000126101</font> |
| out_trans_id | 交易单号 | String | 64 | N | 用户账单上的交易订单号，示例值：092021091922001451301445517582；参见[用户账单说明](https://paas.huifu.com/partners/api/#/czsm/api_czsm_yhzd) |
| request_ip | 请求IP | String | 15 | N | 付款方IP,仅在支付成功后返回;示例：192.168.1.1 |

<!-- extend:start -->
<!-- div:extend-table df3f3656_efdb_449b_b1f3_c165941cdc3a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N | 微信分配的子商户公众账号ID；<font color="green">示例值：wxec280d4c8a1cc2ca</font> |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：oWNHX5RNaCUmZR</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/wiki/doc/apiv3/terms_definition/chapter1_1_3.shtml#part-7)；<font color="green">示例值：OTHERS</font> |
| cash_fee | 现金支付金额 | Int | 100 | N | 订单现金支付金额；<font color="green">示例值：10.00</font> |
| coupon_fee | 代金券金额 | Int | 100 | N | 代金券或立减优惠金额<=订单总金额，<br/>订单总金额-代金券或立减优惠金额=现金支付金额；<br/><font color="green">示例值：1.00</font> |
| attach | 商家数据包 | String | 128 | N | 原样返回；<font color="green">示例值：附加数据</font> |
| <span class="extend ccea8f5e_df58_4529_85e0_12f9dd11487d">promotion_detail</span> | 营销详情列表 | Array | 6000 | N | 营销详情列表，使返回值为Json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ccea8f5e_df58_4529_85e0_12f9dd11487d-table -->
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
| <span class="extend 170c126a_dfb6_42b0_8e35_5786bb5d8b47">goods_detail</span> | 单品列表 | Object | 3000 | N | 使用Json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 170c126a_dfb6_42b0_8e35_5786bb5d8b47-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| goods_remark | 商品备注 | String | 32 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<font color="green">示例值：商品备注</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| price | 商品价格 | String | 32 | Y | 单位为:  元。<font color="green">示例值：50.00</font><br/>如果商户有优惠，需传输商户优惠后的单价(例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50) |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1106d3e2_73fa_4a43_ac92_d843c1c61677-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend d48d593d_1634_4b83_b86e_37230ac4ece4">voucher_detail_list</span> | 优惠券信息 | Array |  | N | 本交易支付时使用的所有优惠券信息 |
| <span class="extend 563e5bc5_b443_43f7_9ac8_e31754327d90">fund_bill_list</span> | 支付金额信息 | Object | 512 | N | 支付成功的各个渠道金额信息，详见资金明细信息说明；json格式 |
| buyer_id | 买家的支付宝唯一用户号 | String | 28 | N | 2088开头的16位纯数字；<font color="green">示例值：20880414938706770000</font> |
| buyer_logon_id | 买家支付宝账号 | String | 100 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| hb_fq_num | 花呗分期数 | String | 10 | N | <font color="green">示例值：3</font> |
| hb_fq_seller_percent | 卖家承担的手续费 | String | 3 | N | <font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d48d593d_1634_4b83_b86e_37230ac4ece4-table -->
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
<!-- div:extend-table 563e5bc5_b443_43f7_9ac8_e31754327d90-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| bank_code | 银行代码 | String | 10 | N | 银行卡支付时的银行代码；<font color="green">示例值：CEB</font>；请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 65186012_90ad_459a_84eb_8d49e187f6a7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 6d6a0a8e_c047_4398_80de_0e6a9f0fd857">coupon_info</span> | 银联优惠信息 | Object |  | N | 优惠信息，银联使用优惠活动时出现，json格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6d6a0a8e_c047_4398_80de_0e6a9f0fd857-table -->
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
<!-- div:extend-table bf5d28ab_9c4a_4611_9760_1f3b9a59ac65-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户应用ID | String | 32 | N | 在抖音开放平台申请的应用ID，全局唯一。此处请填写移动应用（APP）/网站应用（H5）类型的AppID |
| openid | 用户标识 | String | 128 | Y | 用户在商户appid下的唯一标识；<font color="green">示例值：897ae8bd9f194107-9cb3-85f5672037de</font> |
| sub_openid | 子商户用户标识 | String | 128 | N | 用户在子商户appid下的唯一标识；<font color="green">示例值：823ae8bd9f893402-9cb3-85f8794657ea</font> |
| bank_type | 付款银行 | String | 16 | Y | 银行类型，采用字符串类型的银行标识<font color="green">示例值：OTHERS</font> |
| <span class="extend 7eb988ff_e13f_46fb_8e9c_c4ecffd14408">promotion_detail</span> | 营销详情列表 | String |  | N | 营销详情列表，使返回值为Json格式； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7eb988ff_e13f_46fb_8e9c_c4ecffd14408-table -->
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
| <span class="extend 24e29dca_32d7_48ae_b2fc_34fcc79c1efa">goods_detail</span> | 单品列表 | Array |  | N | 单品信息，使用Json格式，是promotion_detail的元素； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 24e29dca_32d7_48ae_b2fc_34fcc79c1efa-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码	 | String | 32 | Y | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；<font color="green">示例值：6934572310301</font> |
| quantity | 商品数量 | String | 32 | Y | 用户购买的数量；<font color="green">示例值：10</font> |
| unit_price | 商品单价 | String | 32 | N | 单位为:元。<font color="green">示例值：99.00</font> |
| discount_amount | 商品优惠金额 | String | 32 | Y | 单品的总优惠金额，单位为：元；<font color="green">示例值：20.00</font> |
| goods_remark | 商品备注 | String | 128 | N | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。<br/><font color="green">示例值：商品备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0115b045_1163_4d63_b331_8ffaf6fa6cf8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend b3ba0eef_2895_44c6_9135_0bc02710f99a">acct_infos</span> | 分账明细 | Array | 2048 | Y | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b3ba0eef_2895_44c6_9135_0bc02710f99a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120000</font> |
| acct_date | 账务日期 | String | 8 | N | <font color="green">示例值：20221023</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 83233203_8373_43d1_91e4_5e755641e05e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_fee_amt | 商户应收手续费 | String | 16 | Y | <font color="green">示例值：5.00</font> |
| actual_fee_amt | 商户实收手续费 | String | 16 | Y | <font color="green">示例值：4.00</font> |
| allowance_fee_amt | 补贴手续费 | String | 16 | Y | <font color="green">示例值：1.00</font> |
| allowance_type | 补贴类型 | String | 10 | N | 0：不补贴，为空默认<br/>1：补贴<br/>2：部分补贴<br/>3：全额补贴(优惠后)<br/>4：部分补贴(优惠后)<br/><font color="green">示例值：2</font> |
| no_allowance_desc | 不补贴原因 | String | 128 | N | 补贴系统返回的不补贴原因；<br/>1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴<br/>2:额度用完<br/>3:不在有效期<br/>4:活动不存在<br/>5:手续费金额为0不补贴<br/>6:顶格优惠<br/>7:额度不足<br/>8:手续费后补<br/>9:未达到起始补贴金额<br/><font color="green">示例值：2</font> |
| <span class="extend c531ab49_9fb8_49de_a7b4_236e04035f48">cur_allowance_config_infos</span> | 手续费补贴活动详情 | Object |  | N | 补贴系统返回，斗拱原样返回； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c531ab49_9fb8_49de_a7b4_236e04035f48-table -->
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
<!-- div:extend-table b6376f21_898b_481e_a6e6_cff0135d9ca2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| debit_flag | 借贷记标识 | String | 1 | N | D-借记卡 C-信用卡 Z-借贷合一卡；<font color="green">示例值：C</font> |
| user_huifu_id | 用户号 | String | 32 | N | 汇付分配的用户号快捷支付时才有值；<font color="green">示例值：6666000103905031</font> |
| order_type | 订单类型 | String | 1 | N | P-支付 R-充值 默认：P-支付；<font color="green">示例值：P</font> |
| bank_id | 银行代号 | String | 8 | N | <font color="green">示例值：30200000</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d2358263_535a_4f31_adbd_6f828514a889-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| gate_type | 网关支付类型 | String | 2 | N | 01: 个人网关02:企业网关；<font color="green">示例值：02</font> |
| bank_id | 付款方银行号 | String | 32 | N | <font color="green">示例值：01040000</font> |
| pyer_acct_id | 付款方银行账户 | String | 1024 | N | B2B支付成功后可能返回密文；<font color="green">示例值：6226560119005276</font> |
| pyer_acct_nm | 付款方银行账户名 | String | 128 | N | <font color="green">示例值：上海汇付支付有限公司</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5086b719_d004_448c_86e1_ddfd2df62086-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_formula | 手续费计算公式 | String | 512 | Y | <font color="green">示例值：AMT*0.003</font> |
| fee_type | 手续费类型 | String | 32 | Y | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；<font color="green">示例值：ACCT_FEE</font> |
| huifu_id | 商户号 | String | 32 | N | 补贴支付账户补贴时，补贴账户的huifuId；<font color="green">示例值：6666000123123123</font> |
| fee_sign | 手续费场景标识 | String | 32 | N | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。<br/><font color="green">示例值：6850aad1e92f4244a74a42fcc1ad6360</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{  
    "data":{  
        "resp_code":"00000000",  
        "resp_desc":"操作成功",  
        "huifu_id":"6666000109133323",  
        "req_date":"20231102",  
        "req_seq_id":"2023110222q11130232812311212",  
        "org_req_date":"20231020",  
        "org_req_seq_id":"202310201652361987182512",  
        "org_hf_seq_id":"0056default231020165304P660ac1360ef00000",  
        "pre_order_id":"H2023102016523600627296228",  
        "order_stat":"1",  
        "party_order_id":"03222310206078496112933",  
        "trans_amt":"0.01",  
        "pay_type":"A_JSAPI",  
        "trans_date":"20231020",  
        "trans_time":"20231020165311",  
        "trans_stat":"S",  
        "fee_amt":"0.00",  
        "ref_amt":"0.01",  
        "goods_desc":"个人电脑",  
        "remark":"商户私有信息test",  
        "product_id":"YYZY",  
        "bank_code":"TRADE_SUCCESS",  
        "bank_desc":"TRADE_SUCCESS"  
    }  
}
```
