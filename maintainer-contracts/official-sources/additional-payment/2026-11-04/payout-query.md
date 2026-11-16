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
## 出金交易查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/settlement/query

*最近更新时间：2026.07.20*
### 应用场景
用于查询单笔出金交易状态及明细。

**适用对象**     
  商户需开通取现功能权限。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                  |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| sys_id     | 系统号   | String | 32   | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font>  |
| sign       | 加签结果 | String | 512  | Y    | 签名，对报文整体签名  |
| product_id | 产品号   | String | 32   | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>  |
| data       | 数据     | String |      | Y    | JSON格式              |

* 公共返回参数

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)   |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 汇付客户Id | String | 32 | Y | 支持渠道商、商户、用户，<font color="green">示例值：6666000109812123</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20210916</font> |
| org_hf_seq_id | 原交易返回的全局流水号 | String | 128 | C | 原交易返回的全局流水号、原交易请求流水号二选一必填；<br/><font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | C | 原交易返回的全局流水号、原交易请求流水号二选一必填；<br/><font color="green">示例值：202109167745558220003</font> |


#### 请求示例

```json
{
  "sys_id": "6666000109812123",
  "product_id": "SPIN",
  "data": {
    "req_seq_id": "202109167745558220003",
    "req_date": "20210918",
    "huifu_id": "6666000021290000",
    "org_req_date": "20210916",
    "org_req_seq_id": "202109160899013231200005"
  }
}

```
### 返回参数


#### 返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | 参见[业务返回码](#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回信息 | String | 256 | Y | [业务返回信息](#业务返回码)；<font color="green">示例值：处理成功</font> |
| org_hf_seq_id | 原交易返回的全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20210916</font> |
| trans_status | 交易状态 | String | 1 | Y | S：成功；F：失败；P：处理中；<font color="green">示例值：S</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | <font color="green">示例值：202109167745558220003</font> |
| trans_desc | 交易描述 | String | 256 | N | <font color="green">示例值：结算</font> |
| cash_amt | 交易金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| fee_amt | 手续费金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| re_exchange | 退汇状态 | String | 1 | N | Y-已退汇；<font color="green">默认为空，该字段为Y时代表已退汇</font> |


##### 返回示例

###### 成功示例
```json
{
  "cash_amt": "0.01",
  "fee_amt": "0.00",
  "org_req_date": "20210916",
  "org_req_seq_id": "202109160899013231200005",
  "resp_code": "00000000",
  "resp_desc": "查询成功",
  "trans_desc": "交易失败,出账失败,ACCT交易失败",
  "trans_status": "F"
}

```


#### 业务返回码

| 返回码   | 返回描述                                                     |    
| :------- | :----------------------------------------------------------- |
| 10000000 | 请求内容体不能为空<br/>%s不能为空（%s代指具体报错参数名）<br/>%s长度固定%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度）<br/>%s最大长度为%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度）<br/>%s的传入枚举[%d]不存在（%s代指具体报错参数名、%d代指具体报错参数的值）<br/>%s不符合%d格式（%s代指具体报错参数名、%d代指具体报错参数值的格式）<br/>%s解密失败（%s代指具体报错参数名） |    |
| 22000000 | 产品号不存在                                                 |    
| 22000000 | 产品号状态异常                                               |   
| 23000001 | 交易不存在                                                   |  
| 00000000 | 查询成功                                                     |  

