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
## 账户余额信息查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/acctpayment/balance/query

*最近更新时间：2025.08.12*
### 应用场景
本接口用于查询商户各类账户的余额信息。

**适用对象**      
商户完成基本信息进件或业务入驻流程创建账户后才能查询账户余额信息。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sys_id     | 系统号   | String | 32   | Y    | 渠道商/代理商/商户的huifu_id <br />（1）当主体为渠道商/代理商时，此字段填写渠道商/代理商huifu_id； <br />（2）当主体为直连商户时，此字段填写商户huifu_id<br/><font color="green">示例值：6666000108854952</font> |
| product_id | 产品号   | String | 32   | Y    |汇付分配的产品号，<font color="green">示例值：HFQ</font>  |
| sign       | 加签结果 | String | 512  | Y    | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)|
| data       | 请求数据 | JSON   |      | Y    | 业务请求参数，具体值参考API文档                              |


### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 请求时间yyyyMMdd；<font color="green">示例值：20221123</font> |
| req_seq_id | 请求流水号 | String | 128 | N | 请求方生成，用于定位查询请求，<font color="green">示例值：2021091708126665001</font> |
| huifu_id | 商户号 | String | 32 | Y | 汇付分配的商户号，<font color="green">示例值：6666000109812123</font> |
| acct_date | 账务日期 | String | 8 | N | 账务日期yyyyMMdd，默认为当天；<font color="green">示例值：20221123</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108854952",
    "product_id": "YYZY",
    "data": {
        "req_seq_id": "202211101668071566142",
        "req_date": "20221110",
        "huifu_id": "6666000108854952"
    },
    "sign": "Ghc8FKQLPqWFMpHnHV8ZVqNzCvM+/xV7WL8G+V/KtY/PsZtu2+2EABcr2SH1yRSekeTKEJffemRjXmuqTgZwsXnse9JduNRtj9Z/1t1H07V4YzpuWw8NVVT7M9R2Z9djjzsOxTYpdF37QRj3kVbg8mAbFcNDuV1vStLm2pRF7lhq6yGB1Q+GAsW2KxEvwuuUnY1BsmMOmzrx+YH/jZ74dSsmYCdZS/SolHcqsgqbqrNUHR/q1Z6j+UmH+s+2A7WS6TvCPoZEY3XVv8uLysm1U2J/1l/4CSsKgW2PlWIBFqhRJikymUw7No+8Yz89DATcLj/9k5sCv7JzVu0G87/bvw=="
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| <span class="extend 2e66c64c_0447_422d_a388_54795e5146d3">data</span> | 交易响应内容体 | Object |  | N | 业务返回参数，jsonObject格式 |
| sign | 加签结果 | String | 512 | N | [接口加签验签说明](https://paas.huifu.com/partners/guide/#/api_v2jqyq) |

<!-- extend:start -->
<!-- div:extend-table 2e66c64c_0447_422d_a388_54795e5146d3-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务响应码](#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务响应信息](#业务返回码)；<font color="green">示例值：查询成功</font> |
| req_date | 请求日期 | String | 8 | Y | 交易时传入，原样返回；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 128 | N | 交易时传入，原样返回；<font color="green">示例值：20211019656229593</font> |
| <span class="extend 81e93514_19ef_46d3_a27d_7ca18d037759">acctInfo_list</span> | 账户信息列表 | String |  | N | JsonArray格式；各子账户余额信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 81e93514_19ef_46d3_a27d_7ca18d037759-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 商户号 | String | 32 | Y | 汇付分配的商户号，例6666000109812123；<font color="green">示例值：6666000109812123</font> |
| acct_id | 账户号 | String | 9 | Y | 商户账户的账户号；<font color="green">示例值：C00690000</font> |
| acct_type | 账户类型 | String | 19 | Y | 01:基本户 02:现金户 03：延时户 04:钱包户 05:充值户 09营销户；<br/><br/><font color="green">示例值：01</font> |
| balance_amt | 账户余额 | String | 16 | N | balanceAmt=avlBal+frzBal；保留2位小数；账务日期为当天时返回；<font color="green">示例值：2100.00</font> |
| avl_bal | 可用余额 | String | 16 | N | 账户可用余额，保留2位小数；账务日期为当天时返回；<font color="green">示例值：2000.00</font> |
| frz_bal | 冻结余额 | String | 16 | N | 账户冻结余额，保留2位小数；账务日期为当天时返回；<font color="green">示例值：100.00</font> |
| last_avl_bal | 昨日日终余额 | String | 16 | Y | 昨日可用余额，保留2位小数；<font color="green">示例值：1000.00</font> |
| acct_stat | 状态 | String | 1 | N | N：“正常”; C：“关闭”; F：“冻结”; D：“销户”；<font color="green">示例值：N</font> |
| control_bal | 管控金额 | String | 16 | N | 该金额包含在冻结金额中；<font color="green">示例值：2100.00</font> |
| last_balance_amt | 昨日账户余额 | String | 16 | Y | 昨日账户余额，保留2位小数；<font color="green">示例值：1000.00</font> |
| last_frz_bal | 昨日冻结余额 | String | 16 | Y | 昨日冻结余额，保留2位小数；<font color="green">示例值：1000.00</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
  "data": {
    "acctInfo_list": "[{\"acct_id\":\"B04606358\",\"acct_stat\":\"N\",\"acct_type\":\"01\",\"avl_bal\":\"0.00\",\"balance_amt\":\"0.00\",\"frz_bal\":\"0.00\",\"huifu_id\":\"6666000018328947\"},{\"acct_id\":\"B07615833\",\"acct_stat\":\"N\",\"acct_type\":\"02\",\"avl_bal\":\"1.26\",\"balance_amt\":\"1.26\",\"frz_bal\":\"0.00\",\"huifu_id\":\"6666000018328947\"}]",
    "req_date": "20211019",
    "req_seq_id": "20211019656229593",
    "resp_code": "00000000",
    "resp_desc": "成功"
  },
  "sign": "HfwtXlElmrAvpPA2w2y1JpmZIrMQPjd/2/xFNwIUkMojJsM4D31ovcgX2bG31K5Nvj4uQM3t5TL61T/RZ3TZrcqHP/AZ5vmAT9b5W03B9dOAe2xwFwEh9+l/slNNNEAYXfV6GGiRn0lvUHcFh6d/nlothz5ru6T/i+LXfTq6Yje+i9QpXr17D5Q2Fr3jeZxzvvvAFddm8py98LetxmJahFi1SL/zQ8M27TthRX+jt0O0lbEcGAST1EEhBjr80f9lSvPfkRLLWr4ytB0XBBzCU8Y9ti5Aona4FH0MCdJOJAANI21qnzSKjuFN+SzBNpjTSzullRSBaV06n4WerdCYBg=="
}
```


#### 业务返回码

查看全部 [公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)

| 返回码   | 返回描述                                                     | 处理                     |
| :------- | :----------------------------------------------------------- | :----------------------- |
| 10000000 | 请求内容体不能为空                                           | 请求体不能为空           |
| 10000000 | 不能为空（%s代指具体报错参数名）                             | 检查该参数是否为空       |
| 10000000 | %s长度固定%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度） | 检查请求参数是否符合格式 |
| 10000000 | %s最大长度为%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度） | 检查请求参数是否符合格式 |
| 10000000 | %s的传入枚举[%d]不存在（%s代指具体报错参数名、%d代指具体报错参数的值） | 检查请求参数是否符合格式 |
| 10000000 | %s不符合%d格式（%s代指具体报错参数名、%d代指具体报错参数值的格式） | 检查请求参数长度         |
| 23000004 | 交易类型不支持                                               | 不支持的配置类型         |
| 22000003 | 账户信息不存在                                               | 检查账户信息             |
| 00000000 | 查询成功                                                     | 成功返回                 |
| 99999999 | 系统异常，请稍后重试                                         | 请稍后重试               |


