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
## DM取现额度查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/settlement/enchashment/dmamt/query

*最近更新时间：2024.12.24*
### 应用场景
用于DM取现额度查询。DM取现是指取现资金当天到银行账户。由于DM取现可以到账的资金不包括当天的交易资金，为了方便您了解可DM取现的额度所以提供本接口。   
注：如果希望将当天收款到汇付账户中的资金取出并当天到账，可以使用D0/T0取现。

**适用对象**     
商户已开通DM取现功能权限。渠道商或SAAS服务商为商户提供DM取现服务时，先查询并展示出DM取现额度。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* ##### 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                  |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| sys_id     | 系统号   | String | 32   | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font>  |
| sign       | 加签结果 | String | 512  | Y    | 签名，对报文整体签名  |
| product_id | 产品号   | String | 32   | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>  |
| data       | 数据     | String |      | Y    | JSON格式              |


* ##### 公共返回参数

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)   |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 商户号 | String | 32 | Y | 汇付分配的商户号，<font color="green">示例值：6666000109812123</font> |
| acct_id | 账户号 | String | 32 | N | 只有基本户与现金户类型支持DM取现。为空默认取基本户账号。<font color="green">示例值：F00598600</font> |


#### 请求示例

```json
{
  "sys_id": "6666000109812123",
  "product_id": "SPIN",
  "data": {
    "huifu_id": "6666000021291985",
    "acct_id": "F00598600"
  }
}

```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | 参见[业务返回码](#业务返回码)，<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回信息](#业务返回码)，<font color="green">示例值：处理成功</font> |
| huifu_id | 商户号 | String | 32 | Y | 汇付分配的商户号，<font color="green">示例值：6666000109812123</font> |
| acct_id | 账户号 | String | 32 | N | <font color="green">示例值：F00598600</font> |
| dm_amt | 剩余dm取现额度 | String | 16 | N | 剩余dm取现额度，单位：元。<font color="green">示例值：1.23</font> |


##### 返回示例

###### 成功示例
```json
{
  "resp_code": "00000000",
  "req_date": "20230203",
  "huifu_id": "6666000109812123",
  "acct_id": "F00598600",
  "dm_amt": "1000.23"
}

```
