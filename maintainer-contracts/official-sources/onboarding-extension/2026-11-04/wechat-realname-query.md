# 微信实名认证状态查询
*最近更新时间：2024.9.1* 
### 应用场景
用于查询商户微信实名认证状态。由于微信实名认证分两个阶段：
1. 实名认证申请
2. 商户授权   

两个阶段都有各自的状态，所以接口会返回两个状态，参见下文。

**适用对象**    
开通微信支付权限的商户

### 接口参数
* 请求URL：https://api.huifu.com/v2/merchant/busi/realname/query
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

| 参数           | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------- | :--------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| req_seq_id     | 请求流水号 | String | 32   | Y    | <font color="green">示例值：rQ2021121311173944134649875651</font>  |
| req_date       | 请求日期   | String | 8    | Y    | 必填，请求日期yyyyMMdd，<font color="green">示例值：20220809</font>|
| huifu_id       | 汇付Id     | String | 18   | Y    | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font>；**请确认该商户已成功入驻微信** |
| pay_channel_id | 子渠道号   | String | 32   | N    | 如需要填写汇付和渠道商约定的值，参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)；<font color="green">示例值：JQF00001</font>|
| pay_scene      | 支付场景   | String | 2    | N    | <font color="green">示例值：01</font>；参见《[微信业务开通类型](http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明 |

#### 请求示例

```java
{
    "sys_id": "6666000123120000",
    "data": {
        "req_seq_id": "rQ2021121311173944134649875651",
        "req_date": "20211213",
        "huifu_id": "6666000104051220",
        "pay_channel_id": "JQF00001",
        "pay_scene": "02"
    },
    "sign": "ihpH1SDnTFUwmFr7Vj5l673sD1T8oAB6Bil3XC6iBJkmSVm4aED3T6ryasPpzbGSkS/CjhkbKx/1Qf0JfeJ54O5N1akFt8F5TPTRhMhj0OO1Gk8EAYRsg0BvQ17A5SFlnAx0aPNxX2uTgyX9y3VSoRapZDIaZnyMisdnI+Eziyw=",
    "product_id": "HSK"
}
```

### 响应参数

| 参数           | 中文名                 | 定义   | 长度 | 必填 | 说明                                                         |
| :------------- | :--------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| resp_code      | 业务响应码             | String | 8    | Y    | <font color="green">示例值：00000000</font>；参见[交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)   |
| resp_desc      | 业务响应信息           | String | 512  | Y    |  <font color="green">示例值：成功</font>；参见[交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| huifu_id       | 汇付ID                 | String | 18   | Y    |<font color="green">示例值：6666000123123123</font> |
| applyment_stat | 微信实名认证申请单状态 | String | 32   | N    | [参见下文说明](#微信实名认证申请单状态)；<font color="green">示例值：APPLYMENT_STATE_PASSED</font> |
| authorize_stat | 实名授权状态               | String | 16   | N    | 授权状态 1：授权成功；0：授权失败；<font color="green">示例值：1</font>                            |
| pay_channel_id | 子渠道号               | String | 32   | N    | <font color="green">示例值：JQF00001</font> |
| pay_scene      | 支付场景               | String | 2    | N    | <font color="green">示例值：01</font> |
| qrcode_data    | 授权二维码             | String | 1000 | N    | 1、当申请单状态为APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT、<br/>APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON、<br/>APPLYMENT_STATE_PASSED、<br/>APPLYMENT_STATE_FREEZED时，会返回二维码图片。<br/>2、使用base64解码该字段，可得到图片二进制数据。<br/>  3、可用img标签直接加载该图片。<br/>  <font color="green">示例值：&lt;img src="data:image/png;base64,iVBORw0KGgoAAAANSU=" style="display: block;"&#62;<font>|
| reject_param   | 驳回参数               | String | 1000 | N    | 当申请单状态为“审核驳回”时，会返回该字段，标识被驳回的字段名。<br/>多个参数名以“\|”分割；<font color="green">示例值：licence_number\|cert_number</font>  |
| reject_reason  | 驳回原因               | String | 1000 | N    | 当申请单状态为“审核驳回”时，会返回该字段，表示驳回原因。 |
| smid           | 微信真实商户号         | String | 32   | N    | <font color="green">示例值：538005664</font>  |


#### 微信实名认证申请单状态
| 参数值      | 中文名   |  说明              |
| :--------- | :-------  | :------------------- |
|APPLYMENT_STATE_EDITTING|编辑中|可能在提交申请时发生错误导致，可用同一个业务申请编号重新提交  |
|APPLYMENT_STATE_WAITTING_FOR_AUDIT|审核中|请耐心等待1~2个工作日，微信支付将会完成审核  |
|APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT|待确认联系信息|请扫描微信支付返回的小程序码确认联系信息(此过程可修改超级管理员手机号)  |
|APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON|待账户验证|请扫描微信支付返回的小程序码在小程序端完成账户验证  |
|APPLYMENT_STATE_PASSED|审核通过|请扫描微信支付返回的小程序码在小程序端完成授权流程  |
|APPLYMENT_STATE_REJECTED|审核驳回|请按照驳回原因修改申请资料，并更换业务申请编码，重新提交申请  |
|APPLYMENT_STATE_FREEZED|已冻结|可能是该主体已完成过入驻，请查看驳回原因，并通知驳回原因中指定的联系人扫描微信支付返回的小程序码在小程序端完成授权流程  |
|APPLYMENT_STATE_CANCELED|已作废|表示申请单已被撤销，无需再对其进行操作  |
|APPLYMENT_STATE_NOAPPLY|未申请|   |

#### 响应示例

```json
{  
    "data":{  
        "resp_code":"00000000",  
        "resp_desc":"成功",  
        "huifu_id":"6666000104854510",  
        "applyment_stat":"APPLYMENT_STATE_REJECTED",  
        "authorize_stat":"0",  
        "pay_channel_id":"JP00001",  
        "pay_scene":"01",  
        "reject_param":"licence_number|cert_number",  
        "reject_reason":"暂未查询到该营业执照注册号，请检查营业执照注册号是否填写正确。（若贵司为新注册，建议等待5~10个工作日再试；若贵司不是个体工商户或企业，请返回并重新选择主体类型）",  
        "smid":"511299000"  
    },  
    "sign":"fddWzUQRTi5S4MiISrrxnRmHOjoJ7QNt4r6PlLGI4mnvxojOsLY1sAumH8ejdYsRvpZk+9rk8Sylbzx7lqUkXAYzJ/qLDBmSzK8uONkUEqDDeIZA1ifKVp3+l+Z3Bbn3a/tLi8Y4mEa6Xtk1h+wi6jiGsnOvaqsPOi9aOMFWsW4="  
}
```