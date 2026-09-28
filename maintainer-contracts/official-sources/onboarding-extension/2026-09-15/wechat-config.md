## 微信商户配置
*最近更新时间：2024.9.1*  <!--入参新增micro_sub_appid字段 --><!--请参示例可直接用-->

### 应用场景
支持配置微信公众号和小程序支付的APPID和授权目录；此接口为添加接口，一旦配置成功，不支持修改和删除（微信端不支持删除)。微信限制每种参数最多配置5组。
请检查商户进件的营业执照全称与appid的营业执照全称是否完全一致。

**适用对象**  
需要开通微信公众号和小程序支付的商户。

### 接口说明
* 请求URL：https://api.huifu.com/v2/merchant/busi/config
* 请求方式：POST
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)
  
### 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                  |
| :--------------- | :------------------------ | :------- | :----- | :----- | :-------- |
| sys_id     | 系统号   | String | 32   | Y    |渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font>  |
| product_id | 产品号   | String | 32   | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font> |
| sign       | 加签结果 | String | 512  | Y    | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)  |
| data       | 数据     | String |      | Y    | JSON格式              |
<!--
* 公共返回参数

| 参数 | 中文名         | 定义   | 长度 | 必填 | 说明                 |
| :--------------- | :------------------------ | :------- | :----- | :----- | :-------- |
| sign | 签名           | String | 512  | Y    | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 交易响应内容体 | String |      | N    | 返回参数 json格式    |
-->
### **请求参数**

<style>
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

**data**

| **参数**         | **中文名**                | **定义**| **长度** | **必填**  | **说明**                                                     |
| :--------------- | :------------------------ | :------- | :----- | :----- | :-------- |
| req_seq_id       | 请求流水号                | String   | 32  | Y  | <font color="green">示例值：2021121311173944651</font>  |
| req_date         | 请求日期                  | String  | 8   | Y     | 格式yyyyMMdd，<font color="green">示例值：20210228</font>  |
| huifu_id| 汇付客户Id | String | 18   | Y    |渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font>|
| fee_type         | 业务开通类型              | String       | 2  | Y  | <font color="green">示例值：01</font>；枚举值参见《[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明|
| wx_woa_app_id    | 公众号支付Appid           | String      | 20     | C| 条件必填，<font color="green">示例值：wx3767c5bd01df5061</font> ；wx_woa_app_id 、wx_woa_path、micro_sub_appid和 wx_applet_app_id四者不能同时为空         |
| wx_woa_path      | 微信公众号授权目录        | String    | 512   | C   | 条件必填，<font color="green">示例值：https://paas.huifu.com/shouyintai/demo/h5/</font>；wx_woa_app_id 、wx_woa_path、micro_sub_appid和 wx_applet_app_id四者不能同时为空   |
| wx_woa_secret    | 微信公众号APPID对应的秘钥 | String     | 64  | N    |<font color="green">示例值：64afb60bef3a22ac282aa7880cdaca98</font> |
| wx_applet_app_id | 微信小程序APPID           | String       | 20  | C  | 条件必填，<font color="green">示例值：wx8523175fea790f10</font> ；wx_woa_app_id 、wx_woa_path、micro_sub_appid和 wx_applet_app_id四者不能同时为空         |
| micro_sub_appid | 微信反扫类交易APPID           | String       | 32  | N  | 如需在汇付反扫交易支付完成后获取sub_openid则此参数必传，<font color="green">示例值：wx23175fea790f10</font> ；wx_woa_app_id 、wx_woa_path、micro_sub_appid和 wx_applet_app_id四者不能同时为空         |
| wx_applet_secret | 微信小程序APPID对应的秘钥 | String      | 64 | N   | <font color="green">示例值：1323a4165a662d6e4f9f51b3f7a58e3f</font>   |
| bank_channel_no  | 渠道号                    | String     | 32   | N  | <font color="green">示例值：JQF00001</font>；有值时设置指定值，为空时使用的微信入驻记录；参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo) |
| async_return_url | 异步消息接收地址 | String      | 120 | N   | 为空不推送审核消息。<font color="green">示例值：http://service.example.com/to/path</font>   |

<!--
| product_id       | 产品编号                  | String    | 32 | Y    |汇付侧生成的固定值产品编号，<font color="green">示例值：JCTEST</font>   |
-->
注：必填字段取值“C”代表条件必填；  

##### 请求示例

```json
{
    "sys_id": "6666000108854952",
    "product_id": "YYZY",
    "data": {
        "req_seq_id": "202211101668071566142",
        "req_date": "20221110",
        "huifu_id": "6666000108854952",
        "fee_type": "02",
        "wx_woa_app_id": "wx3767c5bd01df5061",
        "wx_woa_path": "https://paas.huifu.com/shouyin/demo/h5/",
        "wx_woa_secret": "64afb60bef3a22ac282aa7880cdaca98",
        "wx_applet_app_id": "wx8523175fea790f10",
        "wx_applet_secret": "1323a4165a662d6e4f9f51b3f7a58e3f",
        "bank_channel_no": "JQF00001"
    },
    "sign": "Ghc8FKQLPqWFMpHnHV8ZVqNzCvM+/xV7WL8G+V/KtY/PsZtu2+2EABcr2SH1yRSekeTKEJffemRjXmuqTgZwsXnse9JduNRtj9Z/1t1H07V4YzpuWw8NVVT7M9R2Z9djjzsOxTYpdF37QRj3kVbg8mAbFcNDuV1vStLm2pRF7lhq6yGB1Q+GAsW2KxEvwuuUnY1BsmMOmzrx+YH/jZ74dSsmYCdZS/SolHcqsgqbqrNUHR/q1Z6j+UmH+s+2A7WS6TvCPoZEY3XVv8uLysm1U2J/1l/4CSsKgW2PlWIBFqhRJikymUw7No+8Yz89DATcLj/9k5sCv7JzVu0G87/bvw=="
}
```
<!--
		"wechat_pub_num": "wechat_pub_num",
		"async_return_url": "fd",
		"product_id": "JCTEST"
-->
### 返回参数

#### 同步返回

| 参数 | 中文名         | 定义   | 长度 | 必填 | 说明                 |
| :--------------- | :------------------------ | :------- | :----- | :----- | :-------- |
| sign | 签名           | String | 512  | Y    | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 交易响应内容体 | String |      | N    | 返回参数 json格式    |

**data**

| **参数**  | **中文名** | **定义** | **必填** | **长度** | **说明**                            |
| :-------- | :--------- | :------- | :--- | :------- | :---------------------------------- |
| resp_code | 返回码     | String   | Y    | 8        | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 返回描述   | String   | Y    | 512      | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)                        |
| huifu_id  | 汇付ID     | String   | Y    | 18       |<font color="green">示例值：6666000108854952</font>  |

#### 异步返回

| 参数        | 中文名    | 定义     | 长度  | 必填 | 说明          |
| :--------------- | :------------------------ | :------- | :----- | :----- | :-------- |
| resp_code | 网关返回码  | String | 6   | Y  | 网关返回码       |
| resp_desc | 网关返回描述 | String | 512 | Y  | 网关返回描述      |
| sign      | 签名     | String |     | Y  | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)  |
| data      | 业务返回参数 | String |     | N  | JSON        |

**data**

| 参数            | 中文名      | 定义     | 长度  | 必填 | 说明                                   |
| :--------------- | :------------------------ | :------- | :----- | :----- | :-------- |
| sub_resp_code | 业务返回码    | String | 8   | Y  | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)  |
| sub_resp_desc | 业务返回描述   | String | 512 | Y  | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)  |
| req_seq_id    | 请求流水号    | String | 32  | Y  | 原请求流水号；<font color="green">示例值：rQ2021121311651</font>  |
| req_date      | 请求时间     | String | 8   | Y  | 原请求时间yyyyMMdd；<font color="green">示例值：20221121</font>   |
| product_id    | 产品编号     | String | 32  | Y  | 汇付产品编号；<font color="green">示例值：YYZY</font>   |
| huifu_id      | 汇付商户号    | String | 18  | Y  |<font color="green">示例值：6666000108854952</font>   |
| apply_no      | 申请单号     | String | 18  | N  | 汇付返回商户开户业务申请单号；<font color="green">示例值：2022090803023100</font>   |
| <span class="extend result_list">result_list</span>   | 微信配置结果集合 | String |     | N  | jsonArray格式 参考：result_list;          |
| ord_id        | 通知流水号    | String | 44  | N  | 回调方返回应答，应答内容为：”RECV_ORD_ID_”+该ordId；<font color="green">示例值：RECV_ORD_ID_2021121311173944651</font>   |

<!--result_list-->
<!-- extend:start -->
<!-- div:extend-table result_list-table -->

| 参数           | 中文名  | 定义     | 长度  | 必填 | 说明                    |
| :--------------- | :------------------------ | :------- | :----- | :----- | :-------- |
| config_type  | 配置类型 | String | 1   | Y  |  01 -公众号配置  02-小程序配置；<font color="green">示例值：01</font>   |
| config_stat | 配置值  | String | 256 | Y  | S-成功,F-失败，B-部分成功；<font color="green">示例值：S</font>       |
<!-- extend:end -->

##### 返回示例

```json
{
	"data": {
		"resp_desc": "成功",
		"resp_code": "00000000",
		"huifu_id": "6666000003102100"
	}
}
```
