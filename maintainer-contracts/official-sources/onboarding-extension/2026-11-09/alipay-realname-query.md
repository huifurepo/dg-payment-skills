## 支付宝实名申请单查询
*最近更新时间：2024.9.1* 

### 应用场景
需要开通支付宝支付或报名参与支付宝活动的商户，要先通过支付宝实名认证验证。先调用【[支付宝实名认证申请接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_zfbsmrz)】，支付宝会在3个工作日之内完成审核，之后需要商户的法人或联系人做授权认证。本接口用于查询支付宝审核状态，以及商户经办人授权的状态。

**适用对象**  
已成功入驻支付宝的商户，需要开通支付宝支付权限。

### 接口参数
* 请求URL：https://api.huifu.com/v2/merchant/busi/ali/realname/query
* 请求方式：POST
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

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

<style>
table th:first-of-type {
    width: 17%;
}
table th:nth-of-type(2) {
    width: 15%;
}
table th:nth-of-type(3) {
    width: 10%;
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

#### Data

| 参数             | 中文名   | 定义     | 长度 | 必填 | 说明              |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| req_seq_id     | 请求流水号 | String | 32 | Y  |  <font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date       | 请求日期  | String | 8  | Y  | 必填，请求日期yyyyMMdd，<font color="green">示例值：20220809</font>  |
| huifu_id       | 汇付ID  | String | 18 | Y  | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font> |
| pay_channel_id | 子渠道号  | String | 32 | N  | 如需要填写汇付和渠道商约定的值，参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)；<font color="green">示例值：JQF00001</font> |
| pay_scene      | 支付场景  | String | 2  | N  | 支付宝只支持1-线下扫码；<font color="green">示例值：1</font>|

##### 请求示例

```json
{
    "data": {
        "req_seq_id": "20220822100642399759108",
        "req_date": "20220823",
        "huifu_id": "6666000105418240",
        "pay_channel_id": "10000001",
        "pay_scene": "1"
    },
    "sys_id": "SYS20220818103201681307254",
    "product_id": "ZDTEST",
    "sign": "ihpH1SDnTFUwmFr7Vj5l673sD1T8oAB6Bil3XC6iBJkmSVm4aED3T6ryasPpzbGSkS/CjhkbKx/1Qf0JfeJ54O5N1akFt8F5TPTRhMhj0OO1Gk8EAYRsg0BvQ17A5SFlnAx0aPNxX2uTgyX9y3VSoRapZDIaZnyMisdnI+Eziyw="
}
```

### 响应参数
| 参数             | 中文名    | 定义     | 长度  | 非空 | 说明     |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| resp_code      | 返回码    | String | 8   | Y  | <font color="green">示例值：00000000</font>；参见[交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)  |
| resp_desc      | 返回描述   | String | 512 | Y  |  <font color="green">示例值：成功</font>；参见[交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)|
| order_no       | 意愿申请单号 | String | 64  | N  | <font color="green">示例值：202207011000185133</font>       |
| order_status   | 申请单状态  | String | 64  | N  | 枚举值：<br/>审核中(AUDITING)<br/>待联系人确认(CONTACT_CONFIRM)<br/>待法人确认(LEGAL_CONFIRM)<br/>审核通过(AUDIT_PASS)<br/>审核失败(AUDIT_REJECT)<br/>已冻结(AUDIT_FREEZE)本次申请冻结但仍会返回上次的授权码，可以扫码授权。<br/>已撤回(CANCELED)<br/>未申请(NOT_APPLY)<br/><font color="green">示例值：AUDITING</font>   |
| qrcode         | 二维码图片地址  | String | 128 | N  | 申请单状态处于CONTACT_CONFIRM、LEGAL_CONFIRM返回，商户使用支付宝APP扫码后完成后续确认动作；<br/><font color="green">示例值：https://mobilecodec.alipay.com/show.htm?code=0cb18631uwvja8b7arlcq61</font>   |
| <span class="extend reject_reason">reject_reason</span>  | 审核失败原因 | String |     | N  | jsonArray字符串|
| smid           | 支付宝真实商户号  | String |32  | N  |<font color="green">示例值：2088710120984561</font>  |
| authorize_stat | 经办人授权状态   | String | 20  | N  |已确认（AUTHORIZED）<br/>未确认（UNAUTHORIZED）<br/>已销户（CLOSED）；“已销户”指该商户已销户<br/>smid不存在(SMID_NOT_EXIST)<br/><font color="green">示例值：AUTHORIZED</font>       |
| <span class="extend check_result_list">check_result_list</span>  | 子商户号授权状态集合 | String |   | N | jsonArray字符串 |
<!--#### reject_reason审核失败原因-->
<!-- extend:start -->
<!-- div:extend-table reject_reason-table -->
| 出参名         | 中文名         | 定义     | 长度  | 必填 | 说明                            |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| fail_param  | 审核失败字段      | String | 64  | N  |<font color="green">示例值：cert_number</font>|
| fail_reason | 描述申请单审核失败原因 | String | 128 | N  | <font color="green">示例值：证照编号对应的企业名称、法人名称与录入信息不一致</font>  |

<!-- extend:end -->
<!--#### check_result_list子商户号授权状态集合-->
<!-- extend:start -->
<!-- div:extend-table check_result_list-table -->
| 出参名           | 中文名     | 定义     | 长度 | 必填 | 说明                                                                                        |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| bank_mer_code | 支付宝子商户号 | String | 32 | Y  |<font color="green">示例值:2088610322730727</font>   |
| channel_type  | 通道类型    | String | 1  | Y  | U-银联，N-网联；<font color="green">示例值:N</font>|
| check_result  | 确认状态    | String | 64 | Y  | 已确认(AUTHORIZED)<br/>未确认(UNAUTHORIZED)<br/>已销户(CLOSED)<br/>smid不存在(SMID_NOT_EXIST)<br/><font color="green">示例值:AUTHORIZED</font> |
<!-- extend:end -->
##### 响应示例

```json
{
    "data": {
        "order_no": "202208011001001781",
        "smid": "2088710120984561",
        "order_status": "CANCELED",
        "resp_desc": "成功",
        "qrcode": "https://mobilecodec.alipay.com/show.htm?code=0cb18631uwvja8b7arlcq61",
        "authorize_stat": "UNAUTHORIZED",
        "resp_code": "00000000",
        "reject_reason": ""
    }
}
```