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
## 账务流水汇总结果查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/acctpayment/acctlog/summary

*最近更新时间：2026.09.22*
### 应用场景

支持查询渠道商、代理商、商户、用户在斗拱系统中子账户的资金变动流水明细汇总结果记录。包括基本户、充值户、营销户，以及延时户这样的中间账户。

**适用对象**     
  渠道商、代理商、商户需要开通了斗拱子账户。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)
* 当前只支持查历史账务流水的汇总结果，异步virgo返回商户汇总结果，如有疑问，请联系汇付技术支持人员；

### 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font> |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：HUIFENQI</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一商户号当天唯一，<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准； |
| huifu_id | 渠道/代理/商户/用户编号 | String | 32 | Y | 汇付分配的渠道商、代理商、商户、用户的编号，<font color="green">示例值：6666000109812123</font> |
| acct_id | 账户号 | String | 16 | Y | 账户号 |
| start_trade_time | 开始交易时间 | String | 19 | Y | 开始交易时间 <font color="green">示例值：2026-09-01 00:00:00</font> |
| end_trade_time | 截止交易时间 | String | 19 | Y | 截止交易时间  目前仅支持跨7天范围查询   <font color="green">示例值：2026-09-07 23:59:59</font> |
| notify_url | 异步通知地址 | String | 256 | Y | 异步通知地址<font color="green">示例值：https://www.baidu.com/</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108854952",
    "product_id": "YYZY",
    "data": {
        "req_seq_id": "202211101668071566142",
        "huifu_id": "6666000108854952",
        "acct_id": "A0000001",
        "start_trade_time": "2026-09-01 00:00:00",
        "end_trade_time": "2026-09-08 00:00:00",
        "notify_url":"https://www.baidu.com/"
    },
    "sign": "Ghc8FKQLPqWFMpHnHV8ZVqNzCvM+/xV7WL8G+V/KtY/PsZtu2+2EABcr2SH1yRSekeTKEJffemRjXmuqTgZwsXnse9JduNRtj9Z/1t1H07V4YzpuWw8NVVT7M9R2Z9djjzsOxTYpdF37QRj3kVbg8mAbFcNDuV1vStLm2pRF7lhq6yGB1Q+GAsW2KxEvwuuUnY1BsmMOmzrx+YH/jZ74dSsmYCdZS/SolHcqsgqbqrNUHR/q1Z6j+UmH+s+2A7WS6TvCPoZEY3XVv8uLysm1U2J/1l/4CSsKgW2PlWIBFqhRJikymUw7No+8Yz89DATcLj/9k5sCv7JzVu0G87/bvw=="
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| <span class="extend f8e896fc_c24e_42a7_b131_830873ff9003">data</span> | 交易响应内容体 | Object |  | N | 业务返回参数，jsonObject格式 |

<!-- extend:start -->
<!-- div:extend-table f8e896fc_c24e_42a7_b131_830873ff9003-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 256 | Y | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：处理成功</font> |
| req_date | 请求日期 | String | 8 | Y | 查询时传入，原样返回；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 查询时传入，原样返回；<font color="green">示例值：20211019656229593</font> |
| huifu_id | 渠道/代理/商户/用户编号 | String | 32 | Y | 汇付分配的渠道商、代理商、商户、用户的编号，<font color="green">示例值：6666000109812123</font> |
| acct_id | 账户号 | String | 16 | Y | 商户账户的账户号；<font color="green">示例值：F00598600</font> |
| total_count | 结果总条数 | String | 8 | N | <font color="green">示例值：100</font> |
| total_summary_amt | 汇总总金额 | String | 8 | N | <font color="green">示例值：120</font> |
| <span class="extend d1795cb5_2a8a_4017_bc46_9e0f3b0476c8">summary_list</span> | 账务流水汇总列表 | String |  | N | jsonArray； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d1795cb5_2a8a_4017_bc46_9e0f3b0476c8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_trans_type | 账务类型 | String | 32 | Y | 账务类型；<font color="green">示例值：1001/font> |
| acct_trans_type_desc | 账务类型 | String | 32 | Y | 账务类型见下文描述；<font color="green">示例值：支付收款</font> |
| summary_amt | 交易汇总金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| count | 该账务类型的交易总条数 | String | 14 | Y | 该账务类型的交易总条数 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
  "resp_code": "00000000",
  "resp_desc": "成功",
  "huifu_id": "6666000109133323",
  "acct_id": "F00300982",
  "total_count": "100",
  "total_summary_amt": "120",
  "summary_list": [
    {
      "acct_trans_type": "1001",
      "acct_trans_type_desc": "支付收款",
      "summary_amt": "120"，
      "count": "100",
    }
  ]
}

```


#### 账务类型acct_trans_type

1. 入账类型：
- 1001支付收款 ：聚合正扫、聚合反扫、快捷等支付方式的收款入账；
- 1008支付收款退款失败 ：支付退款失败后资金回款入账；
- 1002充值 ：网银、快捷等方式充值入账；
- 1082充值退款失败 ：充值退款失败后资金回账；
- 1093账户支付收款：分账、余额支付等支付方式的收款入账；
- 1004账户付款退款 ：分账、余额支付退款入账；
- 1012账务调账调入 ：手工调整账务入账；
- 1028退款手续费返还 ：退款手续费返还回账；
- 1036出金失败返还 ：取现、代付失败后资金回账；
- 1045结算回账：结算失败后资金回账；

2. 出账类型：
- 2006支付收款退款 ：聚合正扫、聚合反扫、快捷等支付方式退款出账；
- 2007转账转出
- 2070充值退款 ：充值退款出账；
- 2093账户支付付款 ：分账、余额支付等支付方式的付款出账；
- 2011账务调账调出 ：手工调整账务出账；
- 2018手续费收取 ：支付手续费收取出账；
- 2001取现 ：取现后资金出账；
- 2002代付：代付后资金出账；
- 2045结算：结算后资金出账；

