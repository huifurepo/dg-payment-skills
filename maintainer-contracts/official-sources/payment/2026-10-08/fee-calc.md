## 手续费试算
*最近更新时间：2024.9.1* 

### 应用场景
正式交易前通过手续费试算接口可以获取手续费。接口根据试算金额，返回对应交易类型的借贷记手续费，及通用手续费。支持交易类型：聚合正扫（微信、支付宝等）、快捷、网银、手机WAP支付、余额支付、银联APP、取现的手续费试算。

**适用对象**       
斗拱的商户。

### 接口说明
* 请求URL：https://api.huifu.com/v2/trade/feecalc
* 请求方式：POST
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font> |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

<style>
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

**data**

| 参数              | 中文名               | 类型   | 必填 | 长度 | 说明                                                         |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id               | 商户号     | String | 32  | Y  |<font color="green">示例值：6666000109812123</font>  |
| req_date         | 请求日期    | String | 8   | Y  |  格式为yyyyMMdd，<font color="green">示例值：20091225</font>  |
| req_seq_id     | 请求流水号   | String | 128 | Y  | 同一huifu_id下当天唯一；<font color="green">示例值：2021091708126665001</font>  |
| trade_type       | 交易类型    | String | 32  | Y  |  T_JSAPI: 微信公众号,<br/> T_MINIAPP: 微信小程序, <br/>A_JSAPI: 支付宝JS,<br/> A_NATIVE: 支付宝正扫,<br/> U_NATIVE: 银联正扫,<br/> U_JSAPI: 银联JS,<br/> ENCASHMENT：取现，<br/>ACCT_PAYMENT:余额支付，<br/> ONLINE_PAY:网银，<br/>QUICK_PAY:快捷，<br/>WAP_PAY:手机WAP，<br/>UNION_PAY：银联统一支付；<br/><font color="green">示例值：UNION_PAY</font>  |
| online_trans_type  | 网银交易类型  | String | 3   | N  |  网银交易必传；3000:B2B网银支付，3001:B2C网银支付，3002:B2B网银充值，3003:B2C网银充值<br/><font color="green">示例值：3001</font>   |
| trans_amt         | 交易金额    | String | 14  | Y  |  单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01                 |
| bank_id        | 付款方银行编号 | String | 8   | N  |  网银、快捷和wap手机支付类交易需传入；<br/>参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01020000</font>|
| card_type         | 卡类型     | String | 8   | N  |  D：借记卡，C：信用卡，默认：D（借记卡）；<font color="green">示例值：C</font>  |
| channel_no     | 渠道号     | String | 32  | N  |  扫码交易必传；如果交易走自有渠道请联系运维人员获取；<font color="green">示例值:10000001</font>|
| digital_bank_no       | 数字货币银行编号 | String | 5   | N  |01002: 工行，01004: 中行， 01005: 建行，01008：邮储 <!--<br>01003:  农行<br>01006:  网商 <br>01007:  微众 <br>01009:  交行--><br/><font color="green">示例值：01002</font>|
| encash_type         | 取现到账类型  | String | 3   | N  |  取现交易必传；T0：当日到账，T1：次工作日到账，D1：次自然日到账；<br/><font color="green">示例值:T0</font>|
| pay_scene   | 场景类型    | String | 2   | N  |01:标准线上场景<br/> 02:标准线下场景<br/>03:非盈利商户场景<br/>04:缴费行业场景<br/>05:保险行业场景<br/>06:蓝海绿洲活动场景<br/>07:校园餐饮场景<br/>08:k12中小幼行业场景<br/>09:非在线教培行业场景<br/><font color="green">示例值:01</font> |

##### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "online_trans_type": "3000",
        "digital_bank_no": "01002",
        "pay_scene": "01",
        "req_seq_id": "20240515135004896hzwva4okv70m3b",
        "bank_id": "01020000",
        "req_date": "20240515",
        "channel_no": "10000001",
        "trade_type": "ONLINE_PAY",
        "trans_amt": "1000.00",
        "encash_type": "T0",
        "huifu_id": "6666000109133323",
        "card_type": "D"
    },
    "sign": "dAt/fEVUVVXcZmxPSkSHOWsUtW9SPz7RAOFKyFcyIgKTHAjeBGK4g1tglgjipVbtYA/0humvJfvVFgpN5Pvvgx4QfAsO6GE6VKpbnfOkeRRz3GO4mud6dL0q7ar0wLkhP+fE1yJeTaaDZrzd9gJkIKAZxwXNZdPzU2vBqd1fU3UO8kIcu8iNTJk06xofeobup0HLlSGUPPJspinf+XIpzdKN3fZXW76kKKIrrF1dU7cemISiHEkH+sHkXEodGktzGm6AlDpCFrbvXcb7/SKpQSd88gnhpWFIpsIlhFAN/ydJVyclVEtsQ/OzfqsrWQMTwENWnRikQ3keuLCn4AQT7g=="
}
```

### 返回参数

**data**

| 参数             | 中文名              | 定义     | <div style="width: 25pt">长度</div>    | 必填 | 说明                                                  |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| resp_code      | 业务响应码            | String | 8   | Y  |  <font color="green">示例值：00000000</font>   |
| resp_desc      | 业务响应描述          | String | 256 | Y  |  <font color="green">示例值：成功</font>      |
| huifu_id       | 商户号              | String | 32  | Y  |<font color="green">示例值：6666000109812123</font>  |
| req_seq_id     | 请求流水号 | String | 128 | Y  |  原样返回；<font color="green">示例值：2021091708126665001</font>  |
| req_date       | 请求日期 | String | 8   | Y  |  原样返回,格式为yyyyMMdd；<font color="green">示例值：20091225</font>  |
| credit_fee_amt | 贷记手续费            | String | 14  | N  |  快捷、网银、代扣交易根据实际银行、借贷记取对应借贷记手续费；<font color="green">示例值：1.00</font>   |
| debit_fee_amt  | 借记手续费            | String | 14  | N  |  快捷、网银、代扣交易根据实际银行、借贷记取对应借贷记手续费；<font color="green">示例值：1.00</font>  |
| fee_amt        | 通用手续费            | String | 14  | N  | 扫码类、刷卡类交易取通用手续费；<font color="green">示例值：1.00</font>    |
| hf_seq_id      | 全局流水号            | String | 128 | N  | <font color="green">示例值：00470topo1A221019132207P068ac1362af00000</font>        |                                        |

#### 响应示例

```json
{
    "resp_code": "00000000",
    "resp_desc": "成功",
    "req_seq_id": "1399999097696555",
    "req_date": "20220824",
    "hfSeqId": "00320TOP1GR220826103509P567ac13262200000",
    "huifu_id": "6666000116584429",
    "fee_amt": "1.00"
}
```

