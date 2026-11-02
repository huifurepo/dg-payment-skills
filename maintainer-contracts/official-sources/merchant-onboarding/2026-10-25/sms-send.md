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
## 商户短信发送

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/basicdata/sms/send

*最近更新时间：2026.09.18*
### 应用场景
在一些场景下需要确认用户本人意愿时可以通过发送短信的方式来验证。

**适用对象**  
修改结算卡需要原持卡人知晓并同意时，可以发送短信。  

### 接口说明
* 请求方式：POST
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | <font color="green">示例值：2022012614120615001</font> |
| req_date | 请求时间 | String | 8 | Y | 请求时间格式yyyyMMdd；<font color="green">示例值：20220903</font> |
| huifu_id | 商户汇付Id | String | 18 | Y | 斗拱分配的商户号；<font color="green">示例值：6666000123123123</font> |
| phone | 手机号 | String | 11 | C | verify_type='elecAcctSign'时，手机号为空，系统自动取联系人手机号; <font color="green">示例值：13911111111</font> |
| verify_type | 验证类型 | String | 32 | Y | 枚举：结算卡变更-settleBankChange；中信E管家签约-elecAcctSign; <font color="green">示例值：settleBankChange</font> |
| operation_type | 操作类型 | String | 32 | C | verify_type='elecAcctSign'时必填；枚举值：sendSmsCode-发送验证码；identitySmsCode-验证码核实；<font color="green">示例值：sendSmsCode</font> |
| verify_code | 验证码 | String | 6 | C | verify_type='elecAcctSign'且operation_type='identitySmsCode'时必填；<font color="green">示例值：123456</font> |
| elec_acct_sign_seq_id | 中信签约流水号 | String | 64 | C | verify_type='elecAcctSign'且operation_type='identitySmsCode'时必填；值为中信E管家签约发送短信时返回值；<font color="green">示例值：EMSSBPG2504284593690058431260676</font> |


#### 请求示例

```json
{
    "data": {
        "req_seq_id": "20221013796820257",
        "req_date": "20221013",
        "huifu_id": "6666000105013599",
        "phone": "13917111111",
        "verify_type": "settleBankChange"
    },
    "sys_id": "6666000105013599",
    "product_id": "ZDTEST",
    "sign": "U2yBzISEWzQ6bWXKgwsc7ULke66bNjDi1Kxq22Zdgs/r6aQ3dJKRvQZlRXBUDvG/mCDfqv1EqcNqd0g0jU57yXQTdk2dv9BTK2bqp4GDvg4uCOUfsjuhpvkotyN9m6kqSJfmwLggsCE7Cvy3ga1MwFixbL9iKjtfl2njrcADXIais8mraAB0OrFSvx25Q8w+RJg4OAHaR+cMZyZbpOjZpGkGxvtxo8So9fd8gqE2K2r0hjSMISErDOtivhUrF5+Xm33/CEkJCa/F4ejTtapvyz+z/J8D6err2wJcOCnmRs/X5QiaHjeCLC+tJxeIhlEIZWNh6sfaJxf3YFXpe1G5Lw=="
}
```
### 返回参数


#### 成功

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| verify_type | 验证类型 | String | 32 | N | 枚举：结算卡变更-settleBankChange；中信E管家签约-elecAcctSign; <font color="green">示例值：settleBankChange</font> |
| operation_type | 操作类型 | String | 32 | N | 枚举值：sendSmsCode-发送验证码；identitySmsCode-验证码核实；<font color="green">示例值：sendSmsCode</font> |
| elec_acct_sign_seq_id | 中信签约短信流水号 | String | 64 | N | verify_type='elecAcctSign'且operation_type='sendSmsCode'时；中信E管家签约发送短信时返回值；<font color="green">示例值：EMSSBPG2504284593690058431260676</font> |
| phone | 手机号 | String | 11 | N | 手机号；<font color="green">示例值：13787465677</font> |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "成功"
    },
    "sign": "K7IqpKGVWP2VsbpX9Qwwahf+wSYzJTN+d9ufO+PdHOFdnI/bWgUKQFkOG1t1wcrPD/89kOF2KeT76aPxS9W73Ue2Io/R5Zl89zn93cd1WHCC5WrpzaGjaF5m0uSBfF6Vpci56aGhn3ywah/xlEUYVH4i3dWdMr0uGlTYmieXU1o="
}
```
