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
## 余额支付发送短信验证码

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/sms/verifycode/send

*最近更新时间：2025.07.18*
### 应用场景
本接口用于余额支付前发送短信验证码，保证余额支付安全。

**适用对象**    
已开通余额支付相关功能的商户，操作之前需要短信验证。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)
* 同一个手机号一分钟之内只能请求一次
* 同一个出款方商户号在一个业务类型下短信验证码五分钟有效

### 公共参数

* 公共请求参数

| **参数**   | **中文名** | **定义** | **长度** | **必填** | **说明**                                                     |
| :--------- | :--------- | :------- | :------- | :------- | :----------------------------------------------------------- |
| sys_id     | 系统号     | String   | 32       | Y        | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id<br/><font color="green">示例值：6666000108854952</font> |
| product_id | 产品号     | String   | 32       | Y        | 汇付分配的产品号，<font color="green">示例值：YYZY</font> |
| sign       | 加签结果   | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)|
| data       | 请求数据   | JSON     |          | Y        | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| **参数** | **中文名** | **定义** | **长度** | **必填** | **说明**             |
| :------- | :--------- | :------- | :------- | :------- | :------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |



### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：2021091708126665001</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20221023</font> |
| out_huifu_id | 出款方商户号 | String | 32 | Y | 出款方商户号，<font color="green">示例值：6666000109812124</font> |
| mobile_no | 接收验证码的手机号 | String | 11 | Y | 需为11位数字；示例值：18611111111 |
| trans_type | 业务类型 | String | 256 | Y | 业务类型，ACCT_PAYMENT-余额支付 |


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "req_date": "20240515",
        "req_seq_id": "202405151328579541k8wpk2hvwnnfw",
        "out_huifu_id": "6666000109133323",
        "mobile_no": "18111111111",
        "trans_type": "ACCT_PAYMENT"
    },
    "sign": "XS2o/+V6zyICMm0xc7un8CCe8n3DKjwQRyzMNK29rQ1pgjFnNR3NG7MMcBoE9GwS6oFGWF03v97wd6CfaFP6wYP LwH1GUmYCu1mBk6T+"
}
```
### 返回参数


#### 同步响应参数

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](#业务返回码)  ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：交易成功</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 业务请求流水号；<font color="green">示例值：2022082408452985319884</font> |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "req_seq_id": "202405151328579541k8wpk2hvwnnfw",
        "resp_code": "00000000",
        "resp_desc": "短信验证码发送成功"
    },
    "sign": "JOM+IXkaXHqVSNhXxPjrt+lQzj/85Ky32j1sdmOotc4JZcPRYX7IofUHGHw3iLAwELBmjW8/CSK1nx+aMUIQ1ALqhyYvBLxNiD2fL17XhWEhlUllzsSQCI00mS6po3/uGefmSl3f7i3JhM+Huc0i97A5U7ebUIvVUEigk+sV/VNTm1CWWRzClVF9rLVQCvYPsQDLOi3ejCZ29W5SMLircNPq7YmPC35lzqHt91LFpZDudtqo3E0Tjgyop2+8OR+VRQ2gx6xvbmq92dRE3+zHzrxZ1gqPDO3zGSr/gwq6/3Ha8Op45Fkr9F4s6G6QBcx44BVnlKyGMKiYvzYE2I3h3g=="
}
```


#### 业务返回码

查看全部[公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)

| 返回码   | 返回描述                                                   | 处理                                               |
| :-------- | :---------------------------------------------------------- | :-------------------------------------------------- |
| 00000000 | 交易处理完成                          |参考trans_stat值确定交易状态  |
| 10000000 | 请求参数校验存在问题      | 返回描述会告知参数校验失败的原因，更改对应字段后再次发起请求即可 |
| 22000000 | 产品号不存在                                               | productId不存在或状态异常                          |
| 22000002 | 商户配置信息校验失败                 |返回描述会告知业务校验失败的原因    |
| 22000003 | 账户信息不存在或者状态异常                                 | 账户配置错误                                       |
| 22000004 | 业务校验失败                                       | 返回描述会告知业务校验失败的原因                                   |
| 98888888 | 系统错误             |请提供接口URL及请求参数，联系斗拱运维处理  |
| 其他返回码 |              |若无明确trans_stat字段表明交易状态，可调用余额支付查询接口获取交易状态。<br/>或需要联系斗拱运维人工查看 |

