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
## 统一收银台交易关单

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/close

*最近更新时间：2026.04.22*

### 应用场景
统一收银台交易关单接口，适用于微信、支付宝、云闪付交易，快捷网银待后续支持

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
| req_seq_id | 请求流水号 | String | 64 | Y | 同一huifu_id下当天唯一；示例值：rQ2021121311173944 |
| req_date | 请求日期 | String | 8 | Y | 请求格式：yyyyMMdd；示例值：20221023 |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成示例值：6666000123123123 |
| org_req_date | 原请求日期 | String | 8 | Y | 请求格式：yyyyMMdd；示例值：20221023 |
| org_req_seq_id | 原请求流水号 | String | 64 | Y | 同一huifu_id下当天唯一；示例值：rQ2021121311173944 |

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
| resp_code | 业务响应码 | String | 8 | Y | 参见业务返回码；示例值：00000000 |
| resp_desc | 业务响应信息 | String | 512 | Y | 参见业务返回码；示例值：交易成功 |
| req_seq_id | 请求流水号 | String | 64 | Y | 交易时传入原样返回，示例值：rQ2021121311173944134649875651 |
| req_date | 请求日期 | String | 8 | Y | 交易时传入，原样返回，示例值：20220905 |
| huifu_id | 商户号 | String | 32 | Y | 示例值：6666000123123123 |
| org_req_date | 原请求日期 | String | 8 | Y | 格式为yyyyMMdd，示例值：20221023 |
| org_req_seq_id | 原请求流水号 | String | 64 | Y | 示例值：rQ20221010134649875651 |
| org_trans_stat | 原交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；示例值：S |
| close_stat | 关单状态 | String | 1 | Y | P：处理中、S：成功、F：失败；示例值：S |


#### 异步返回参数

**resp_data**    

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | 参见业务返回码；示例值：00000000 |
| resp_desc | 业务响应信息 | String | 512 | Y | 参见业务返回码；示例值：交易成功 |
| huifu_id | 商户号 | String | 32 | Y | 示例值：6666000123123123 |
| org_req_date | 原请求日期 | String | 8 | Y | 格式为yyyyMMdd，示例值：20221023 |
| org_req_seq_id | 原请求流水号 | String | 64 | Y | 示例值：rQ20221010134649875651 |
| org_trans_stat | 原交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；示例值：S |
| close_stat | 关单状态 | String | 1 | Y | S：成功、F：失败；示例值：S |


#### 业务返回码

常见错误码：

| <div style="width: 55pt">返回码</div>    | 返回描述                                                   | 
| :------- | :--------------------------------------------------------- | 
| 00000000 | 交易成功           |
| 00000100 | 交易处理中          |
| 10000000 | 无效参数           |
| 99999999 | 系统异常，请稍后重试     |
| 99010003 | 交易不存在          |
| 30000001 | 原交易已经终态，不允许关单  |
| 30000001 | 关单状态为终态，不能重复关单 |

