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
## 电子协议签署链接重发

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/agreement/elect/signurl/resend

*最近更新时间：2026.09.17*
### 应用场景
电子合同重发。

### 接口说明
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

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号，同一商户号当天唯一； |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准； |
| huifu_id | 汇付商户号 | String | 32 | Y | 渠道与一级代理商的直属商户ID |
| agreement_id | 协议编号 | String | 32 | Y |  |
| sign_user_email | 个人邮箱 | String | 64 | Y |  |


#### 请求示例

```json
{
  "product_id": "MYPAY",
  "sys_id": "6666000003099901",
  "data": {
    "req_seq_id": "2026070212345673329",
    "req_date": "20260702",
    "huifu_id":"6666000103334211",
    "agreement_id":"130516670601443792", 
    "sign_user_email":"zhangsan@huifu.com"
  },
  "sign": "bv+5P6yuqOZaErHlEDdaB3o1BoOTmiwRElDw1u9kWRksXGamVwjbZTFTv9MjvkGvv4qSqzpdQYQw8hU6IXvg1g+xR838v4PYncm/+RU+R5jPRPxvUGK01ikb4QGU/cv4sDLJ/vZsckMR3nkyJNh/a1OlFd795ZmEBjcI6AKUR4fnD8nZ3buSdjwQMXwyW73ZvtdBTpM/+Jt+FLAwGJ00mexLwfWJl/3nvLxGEFlLXLtZPgIBZlq+9oEZiyZUxfdY/Jv7U3MWQ9Wdr81hAxOyd8dxBoxeuTc++zN1jHpwdoHOfxatfV9WofLQQw5vOeQh9pPHaqM73WpyTX5OV/nbbA=="
}
```
### 返回参数


#### 同步返回参数

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |
* data

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：成功；签约链接从生成起7天有效，如果超过七天请重新发起电子合同重发；</font> |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_desc": "成功",
        "resp_code": "00000000"
    }
}
```
