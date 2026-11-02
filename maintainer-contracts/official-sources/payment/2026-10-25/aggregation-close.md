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
## 交易关单

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/payment/scanpay/close

*最近更新时间：2026.05.28*
## 接口说明

服务商/商户系统通过本接口发起订单关闭请求。注：
- 银联订单不支持关单；
- 原交易已是终态（成功/失败）的，关单会失败。

## 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font> |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220905</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944134649875651</font> |
| huifu_id | 商户号 | String | 32 | Y | 开户后自动生成；<font color="green">示例值：6666000123123123</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220905</font> |
| org_hf_seq_id | 原交易返回的全局流水号 | String | 128 | N | org_hf_seq_id，org_req_seq_id二选一；<br/><font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | org_hf_seq_id，org_req_seq_id二选一；<font color="green">示例值：202110210012100005</font> |
| merge_flag | 是否合单交易关单 | String | 2 | N | Y-合单交易关单，N或空-非合单交易关单。<br/>为Y时，上送的交易信息需要是主单信息，其他情况上送子单信息 |


#### 请求示例

```json
{
  "sys_id": "6666000108840829",
  "data": {
    "org_req_date": "20240405",
    "org_req_seq_id": "20210918956161001",
    "req_seq_id": "20240425105638838efkflqyi00ond6",
    "req_date": "20240425",
    "huifu_id": "6666000109133323"
  },
  "product_id": "YYZY",
  "sign": "ilDS3LYVqlJYS+q1F/MhiFfVZOyHngNAg3i0XvnqqHv2guQXyfcIOVp4us9WCaqF38FqVmnsnIRzEoxRfLEHF7kfGLSsfJGfcE0CjlhKsUjTyA6j+3vKrPRDCIIfV0YLqP8sh0XSWoWdqad5VNZgh4LuYa5DV2uV9BlnVlTNWHFr0csbcaTKiNlnPdKhXdybAKwQPi/M7ZVy8hTU1HbWSkrWfjM8Rb3ujVy3mGiYO+je9KT6ym//f9dgWidrh1uAkHBxn/N4dRiKsm9nIbiSjF0q2tNcF0PGaUjUtG4wo3+x/2fMAbG9Wz+oY3SQoS+g5VcsXayfbA5CBGkt3n8xBg=="
}

```
### 返回参数


#### 同步返回参数

* ##### data

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](#业务返回码) |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| req_date | 请求日期 | String | 8 | Y | 交易时传入，原样返回，<font color="green">示例值：20220905</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 交易时传入原样返回，<font color="green">示例值：rQ2021121311173944134649875651</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220905</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | <font color="green">示例值：rQ20221010134649875651</font> |
| org_hf_seq_id | 原交易的全局流水号 | String | 128 | N | <font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_trans_stat | 原交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；<font color="green">示例值：S</font> |
| trans_stat | 关单状态 | String | 1 | Y | P：处理中、S：成功、F：失败；<font color="green">示例值：S</font> |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "10000016", 
        "resp_desc": "原订单已为终态,请发起查询交易获取", 
        "huifu_id": "6666000018328947", 
        "req_date": "20210919", 
        "req_seq_id": "2021091981146428003", 
        "org_req_date": "20210918", 
        "org_req_seq_id": "202109187312431237001", 
        "trans_stat": "F"
    },
    "sign": "JooKBwoym+a4qA5xnSawA4NSAK/sPtxKR7vtErxeKAXJklD4WtbN8hjd2tUIgmOwH9g25HEtitn22xK2T+73u+xsQX31X/rtuY8/zWhr8/Jn0GF/hh1QbOxdYZybM2z4m/oqi6H0SZAajgKzQcrfNHdhvFCD2GP+cVI2rQEm/lMXYkzW7ik4AWicJSA429g7O+rQf+TSMA+qgefkhsMZ3xZeCl0sVDCqkyRfAc7m28cYKQZdFQY0aOsMMgUF7Wsq78R+McYmseASoDZv8dI1//Jl5+uKFYrMRq1ADt8s01pPGILjWSJPkj6cAcMd7pqRa4k8No7+Cv5MunFP3Wwhhg=="
}
```


#### webhook说明

斗拱交易完成后除了返回异步消息也支持另外发送webhook关单事件【trans.close】。webhook事件可以灵活配置接收端用于驱动业务流程。  
[webhook的使用参见说明](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao?id=%e5%a6%82%e4%bd%95%e4%bd%bf%e7%94%a8webhook)；



#### 业务返回码

| 返回码   |返回描述                               |
| :------- |  :--- |
| 00000000 |交易成功                               |
| 00000100 |交易处理中                             |
| 10000000 |入参数据不符合接口要求                 |
| 20000001 |**不允许关闭一分钟以内的订单**             |
| 20000001 |并发冲突,请稍后重试                    |
| 21000000 |原请求流水号和原全局流水号不能同时为空 |
| 22000000 |产品号不存在                           |
| 22000000 |产品号状态异常                         |
| 23000000 |**原订单已为终态,无法发起关单操作**        |
| 23000000 |关单状态为终态，不能重复关单           |
| 23000001 |**原交易不存在**                           |
| 23000004 |原订单为银联二维码交易，不支持关单     |
| 90000000 |业务执行失败                           |
| 98888888 |系统错误                               |
| 99999999 |系统异常,请稍后重试                    |

