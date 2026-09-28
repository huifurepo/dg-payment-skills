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
## 商户费率信息查询（支持指定费率类型查询）

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/fee-rate/query

*最近更新时间：2026.09.04*
### 应用场景
商户获取到汇付商户号后，可使用此接口查询按照指定费率类型查询获取 支付宝支付费率信息、微信支付费率信息、银行卡支付配置信息、银联二维码支付配置信息等费率信息

**适用对象**  
已开通成功获得huifu_id的商户；

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


### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号 |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准； |
| huifu_id | 汇付商户号 | String | 18 | Y | 汇付分配的商户号，<font color="green">示例值：6666000108854952</font> |
| fee_rate_type | 费率类型（支持多选） | String | 117 | N | jsonArray字符串，<br/> ALI_FEE_RATE：支付宝支付费率信息<br/>WX_FEE_RATE：微信支付费率信息<br/>BANK_CARD_FEE_RATE：银行卡支付费率信息<br/>UNION_FEE_RATE：银联二维码支付费率信息<br/><font color="green">不传则返回全部费率;  示例值：["ALI_FEE_RATE","WX_FEE_RATE","UNION_FEE_RATE"]</font>； |


#### 请求示例

```json
{
    "sys_id": "6666000108854952",
    "product_id": "YYZY",
    "data": {
        "req_date": "20250501",
        "req_seq_id": "202211101668071566142",
        "fee_rate_type": "['ALI_FEE_RATE']",
        "huifu_id": "6666000108854952"
    },
    "sign": "Ghc8FKQLPqWFMpHnHV8ZVqNzCvM+/xV7WL8G+V/KtY/PsZtu2+2EABcr2SH1yRSekeTKEJffemRjXmuqTgZwsXnse9JduNRtj9Z/1t1H07V4YzpuWw8NVVT7M9R2Z9djjzsOxTYpdF37QRj3kVbg8mAbFcNDuV1vStLm2pRF7lhq6yGB1Q+GAsW2KxEvwuuUnY1BsmMOmzrx+YH/jZ74dSsmYCdZS/SolHcqsgqbqrNUHR/q1Z6j+UmH+s+2A7WS6TvCPoZEY3XVv8uLysm1U2J/1l/4CSsKgW2PlWIBFqhRJikymUw7No+8Yz89DATcLj/9k5sCv7JzVu0G87/bvw=="
}
```
### 返回参数


#### 成功

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| product_id | 产品号 | String | 32 | Y | 同入参 |
| huifu_id | 汇付商户号 | String | 18 | Y | 同入参 |
| req_seq_id | 请求流水号 | String | 32 | Y | 同入参 |
| req_date | 请求日期 | String | 8 | Y | 同入参 |
| <span class="extend c78b4dcd_7a92_4c80_a7f8_8f9e38810e9b">wx_fee_rate_list</span> | 微信支付费率信息 | String |  | N | jsonArray格式 |
| <span class="extend 0f43d8b7_cddc_4e4b_b793_c2b3a12861f4">ali_fee_rate_list</span> | 支付宝支付费率信息 | String |  | N | jsonArray格式 |
| <span class="extend d76c61c4_e977_4ea4_aa8f_a7a8dcbe4b94">bank_card_fee_rate_list</span> | 银行卡支付费率信息 | String |  | N | jsonArray格式 |
| <span class="extend 40b403f5_5ded_43c0_9a07_94cb8d969e8e">union_fee_rate_list</span> | 银联二维码支付费率信息 | String |  | N | jsonArray格式 |

<!-- extend:start -->
<!-- div:extend-table c78b4dcd_7a92_4c80_a7f8_8f9e38810e9b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String | 9 | Y | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| fee_min_amt | 最低收取手续费（元） | String | 6 | N | 固定金额保留2位小数；大于0。需要渠道商开通此功能。<font color="green">示例值：0.38</font> |
| pay_scene | 支付场景 | String | 2 | Y | 参见《[微信支付场景](api_ggcsbm.md#微信支付场景)》说明；<font color="green">示例值：1</font> |
| pay_type | 支付类型 | String | 3 | Y | C03-微信线下反扫支付<br/>C04-微信线下公众号支付<br/>C05-微信线下小程序支付<br/>C06-微信线上公众号支付<br/>C07-微信线上小程序支付<br/>C14-微信非盈利费率交易<br/>C15-微信缴费费率交易<br/>C16-微信保险费率交易<br/>C17-微信行业活动费率交易<br/>C18-微信校园餐饮费率交易<br/>C19-微信中小幼费率交易<br/>C20-微信线下教培费率交易<br/>C23-微信线上反扫支付<br/>C30-微信APP支付 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0f43d8b7_cddc_4e4b_b793_c2b3a12861f4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate | 手续费（%） | String |  | N | <font color="green">示例值：0.60</font> |
| fee_min_amt | 最低收取手续费（元） | String | 6 | N | 固定金额保留2位小数；大于0。需要渠道商开通此功能。<font color="green">示例值：0.38</font> |
| pay_scene | 支付场景 | String | 2 | Y | 1、线下扫码，2、线上扫码，3、非盈利费率；<font color="green">示例值：1</font> |
| pay_type | 支付类型 | String | 3 | Y | D02-线下支付宝正扫支付<br/>D03-线下支付宝反扫支付<br/>D04-线下支付宝JS支付<br/>D22-线上支付宝正扫支付<br/>D23-线上支付宝反扫支付<br/>D24-线上支付宝JS支付<br/>D07-支付宝非盈利费率交易<br/>D08-支付宝缴费费率交易<br/>D09-支付宝行业活动费率交易<br/>D21-支付宝校园餐饮费率交易 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d76c61c4_e977_4ea4_aa8f_a7a8dcbe4b94-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| debit_fee_rate | 借记卡手续费（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]； <font color="green">示例值：0.60</font> |
| debit_fee_limit | 借记卡封顶值 | String | 4 | N | 数字类型，大于0保留2位小数； <font color="green">示例值：2.00</font> |
| credit_fee_rate | 贷记卡手续费（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.90</font> |
| pay_scene | 支付场景 | String | 2 | Y | 1、银行卡支付 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 40b403f5_5ded_43c0_9a07_94cb8d969e8e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| fee_rate_up | 银联二维码业务手续费1000(包含1000)以上（%） | String | 9 | Y | 数字类型，大于0保留2位小数；取值范围（0.00,100.00];<font color="green">示例值：0.60</font> |
| fee_rate_down | 银联二维码业务手续费1000(包含1000)以下（%） | String | 9 | N | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；<font color="green">示例值：0.60</font> |
| pay_scene | 支付场景 | String | 2 | Y | 1、线下银联二维码 2、线上银联二维码 |
<!-- extend:end -->
