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
## 账务流水查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/acctpayment/acctlog/query

*最近更新时间：2026.08.13*
### 应用场景

支持查询渠道商、代理商、商户、用户在斗拱系统中子账户的资金变动流水明细记录。包括基本户、充值户、营销户，以及延时户这样的中间账户。

**适用对象**     
  渠道商、代理商、商户需要开通了斗拱子账户。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)
* 当前每天可以查询出的账务流水记录不超过10000笔。超过一万笔的流水，就建议通过账务文件的形式获取流水，请联系汇付技术支持人员；

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
| huifu_id | 渠道/代理/商户/用户编号 | String | 32 | Y | 汇付分配的渠道商、代理商、商户、用户的编号，<font color="green">示例值：6666000109812123</font> |
| acct_date | 账务日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| page_size | 每页条数 | String | 8 | N | 最大100。不传则默认10。<font color="green">示例值：10</font> |
| page_num | 分页页码 | String | 8 | N | 从1开始。不传则默认1。last_end_log_id与page_num不能同时为空<font color="green">示例值：20</font> |
| acct_id | 账户号 | String | 32 | N | 可指定账户号，不填默认为基本户；；<font color="green">示例值：F00598600</font> |
| last_end_log_id | 流水号ID | String | 64 | N | 流水号ID；当传了last_end_log_id ,acct_id参数必填,page_num无须传第一次翻页填0即可<font color="green">示例值：209908070115364435850870</font> |
| acct_type | 账户类型 | String | 2 | N | 账户类型 01:基本户 02:现金户 03:延时户 05:充值户 09:营销户；不填默认01 |
| hf_seq_id | 汇付全局流水号 | String | 64 | N | 该参数传入时，优先使用该参数查询数据，<font color="red">此时分页条件失效，账务日期条件失效</font>，默认返回所有符合的数据；<font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108854952",
    "product_id": "YYZY",
    "data": {
        "req_seq_id": "202211101668071566142",
        "huifu_id": "6666000108854952",
        "acct_type": "01",
        "acct_date": "20220816",
        "page_num": "1",
        "page_size": "10",
        "hf_seq_id": "00470topo1A211015160805P090ac132fef00000"
    },
    "sign": "Ghc8FKQLPqWFMpHnHV8ZVqNzCvM+/xV7WL8G+V/KtY/PsZtu2+2EABcr2SH1yRSekeTKEJffemRjXmuqTgZwsXnse9JduNRtj9Z/1t1H07V4YzpuWw8NVVT7M9R2Z9djjzsOxTYpdF37QRj3kVbg8mAbFcNDuV1vStLm2pRF7lhq6yGB1Q+GAsW2KxEvwuuUnY1BsmMOmzrx+YH/jZ74dSsmYCdZS/SolHcqsgqbqrNUHR/q1Z6j+UmH+s+2A7WS6TvCPoZEY3XVv8uLysm1U2J/1l/4CSsKgW2PlWIBFqhRJikymUw7No+8Yz89DATcLj/9k5sCv7JzVu0G87/bvw=="
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| <span class="extend 096839cc_b4b7_415d_990b_34dde142b917">data</span> | 交易响应内容体 | Object |  | N | 业务返回参数，jsonObject格式 |
| sign | 加签结果 | String | 512 | Y | [接口加签验签说明](https://paas.huifu.com/partners/guide/#/api_v2jqyq) |

<!-- extend:start -->
<!-- div:extend-table 096839cc_b4b7_415d_990b_34dde142b917-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 256 | Y | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：处理成功</font> |
| huifu_id | 渠道/代理/商户/用户编号 | String | 32 | Y | 汇付分配的渠道商、代理商、商户、用户的编号，<font color="green">示例值：6666000109812123</font> |
| mer_name | 商户名称 | String | 128 | N | <font color="green">示例值：上海汇付支付服务公司</font> |
| mer_short_name | 商户简称 | String | 64 | N | <font color="green">示例值：汇付支付</font> |
| acct_type | 账户类型 | String | 19 | N | 01:基本户；  09:营销户；<br/><font color="green">示例值：01</font> |
| acct_id | 账户号 | String | 9 | N | 商户账户的账户号；<font color="green">示例值：F00598600</font> |
| page_size | 每页条数 | String | 8 | N | <font color="green">示例值：20</font> |
| page_num | 分页页码 | String | 8 | N | <font color="green">示例值：12</font> |
| result_count | 结果总条数 | String | 8 | N | <font color="green">示例值：120</font> |
| <span class="extend 23625a60_119a_460c_a7ec_213095ad2ba2">acct_log_list</span> | 账务流水列表 | String |  | N | jsonArray； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 23625a60_119a_460c_a7ec_213095ad2ba2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| acct_log_id | 账务流水号 | String | 32 | Y | <font color="green">示例值：7001709383</font> |
| acct_date | 账务日期 | String | 8 | Y | <font color="green">示例值：20220628</font> |
| trans_date_time | 账务时间 | String | 32 | Y | <font color="green">示例值：20230804125959</font> |
| acct_trans_type | 账务类型 | String | 32 | Y | 账务类型见下文描述；<font color="green">示例值：支付收款</font> |
| acct_trans_type_code | 账务类型编码 | String | 4 | Y | <font color="green">示例值：1001</font> |
| acct_product_req_seq_id | 账务侧产品流水号 | String | 64 | Y | <font color="green">示例值：2022062815265000top_Ait648656107TM01</font> |
| debit_type | 借贷记标识 | String | 1 | Y | D-借记 C-贷记；<font color="green">示例值：D</font> |
| trans_amt | 交易金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| fee_amt | 手续费金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| balance_amt | 交易后余额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| hf_seq_id | 全局流水号 | String | 128 | Y | 引起这笔账户资金变动的交易全局流水号；<font color="green">示例值：0035000topA220628152651P306c0a8217a00000</font> |
| control_ord_flag | 管控订单标识 | String | 2 | N | Y:管控订单，N:非管控订单；<font color="green">示例值：N</font> |
| log_id | 流水号ID | String | 64 | N | 流水号ID；<font color="green">示例值：202608070115364435850870</font> |
| mer_acct_seq_id | 商户账务流水编号 | String | 64 | Y | 商户账务流水编号<font color="green">示例值：20260807000000000001</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{  
"resp_code":"00000000",  
"resp_desc":"成功",  
"huifu_id":"6666000109133323",  
"acct_id":"F00300982",  
"acct_type":"01",  
"page_num":"1",  
"acct_log_list":[  
{  
"acct_date":"20220707",  
"acct_log_id":"4112955077",  
"acct_product_req_seq_id":"MUThumk19nce4h",  
"acct_trans_type":"转账转出",  
"balance_amt":"0.03",  
"debit_type":"D",  
"fee_amt":"0.00",  
"trans_amt":"0.01",  
"trans_date_time":"20220707161036"  
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

