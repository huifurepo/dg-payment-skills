## 微信配置查询
*最近更新时间：2024.12.30* 

### 应用场景
提供微信商户配置查询接口。

**适用对象**    
开通微信公众号和小程序支付的商户。

### 接口说明
* 请求URL：https://api.huifu.com/v2/merchant/busi/config/query
* 请求方式：POST
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)
  
### 公共参数

* 公共请求参数

| 参数       | 中文名   | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :-------------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商或商户的huifu_id； <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为总部商户时，此字段填写商户huifu_id |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>                                      |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名         | 定义   | 长度 | 必填 | 说明                 |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| sign | 签名           | String | 512  | Y    | 签名，对报文整体签名 |
| data | 交易响应内容体 | String |      | N    | 返回参数 json格式    |


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

| 参数            | 中文名     | 定义  | 长度 | 必填  | 说明             |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| req_seq_id      | 请求流水号 | String  | 32 | Y     |<font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date        | 请求时间   | String  | 8 | Y    | 格式yyyyMMdd，<font color="green">示例值：20210228</font>  |
| huifu_id| 汇付客户Id | String | 18   | Y    |渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font>|
| bank_channel_no | 渠道号     | String    | 32| N | <font color="green">示例值：JQF00001</font>；参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)  |

##### 请求示例

```json
{
        "sys_id": "6666000108854952",
        "product_id": "YYZY",
        "data": {
        "req_seq_id": "202211111668073286240",
        "req_date": "20221111",
        "huifu_id": "6666000108854952",
        "bank_channel_no": ""
    },
        "sign": "Z1wmTfpNdQcDLVHaF4bKbyjTC+ZhIkRnQS+4G+W2EJTHRTNi5ymjJreTGgXv97iBzP3aOPKcMmJgbjAR97u+E6KGmpN84AMKTmKVread1znrRmeMKVVBsakDU3EEbF8NTQGY1SffxpJY6bb1/w7XmrnzN66Kip6NaluFUnqyQRI="
}
```

### 返回参数

**同步返回参数data**

| 参数                    | 中文名       | 定义   | 必填 | 长度 | 说明                                    |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| resp_code               | 返回码       | String | Y    | 8    | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)     |
| resp_desc               | 返回描述     | String | Y    | 512  | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| <span class="extend atu_config_bo_list">atu_config_bo_list</span>   | 配置信息     | String   | N    |      | jsonArray格式                                |
| <span class="extend atu_config_bo_fail_list">atu_config_bo_fail_list</span>|配置失败信息 | String   | N    |      | jsonArray格式；配置失败信息仅返回最新一条  |

<!--配置信息-->
<!-- extend:start -->
<!-- div:extend-table atu_config_bo_list-table -->

| 参数             | 中文名             | 定义   | 必填 | 长度 | 说明                                                         |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| fee_type         | 业务开通类型       | String | N    | 2    | <font color="green">示例值：01</font>；参见《[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明|
| wx_applet_app_id | 微信小程序APPID    | String | N    | 20   |<font color="green">示例值：wx8523175fea790f10</font> |
| wx_woa_app_id    | 公众号支付APPID    | String | N    | 512  | <font color="green">示例值：wx3767c5bd01df5061</font>    |
| wx_woa_path      | 微信公众号授权目录 | String | N    | 512  | <font color="green">示例值：https://paas.huifu.com/shouyintai/demo/h5/</font>|
| micro_sub_appid | 微信反扫类交易APPID   | String | 32  | N  | <font color="green">示例值：wx23175fea790f10</font> ；|
| bank_channel_no  | 渠道号             | String | N    | 32   | <font color="green">示例值：JQF00001</font>|
| <span class="extend wx_config_list">wx_config_list</span>   | 微信配置结果集     | String |  N    |    | jsonArray格式 参考：wx_config_list 微信配置结果集            |
<!-- extend:end -->

<!--微信配置结果集 -->
<!-- extend:start -->
<!-- div:extend-table wx_config_list-table -->

| 参数         | 中文名   | 定义   | 长度 | 必填 | 说明 |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| config_type  | 配置类型 | String | 1    | Y    | 1-小程序appId， 2-公众号appId， 3-授权目录， 4-关注的公众号，5-微信反扫类交易appId；<font color="green">示例值：1</font>； |
| config_value | 配置值   | String | 256  | Y    | 对应配置类型参数值 |
| control_flag | 管控标识    | String | 1  | N    | Y-管控中,N-已解控，为空时无管控                                                      |
| control_time | 管控/解控时间 | String | 20 | N    | 管控/解控时间：yyyy-MM-dd HH:mm:ss格式，当controlFlag为Y时为管控时间，当controlFlag为N时为解控时间 |
<!-- extend:end -->

<!--配置失败信息 -->
<!-- extend:start -->
<!-- div:extend-table atu_config_bo_fail_list-table -->

| 参数             | 中文名                    | 定义   | 长度 | 必填 | 说明             |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| fee_type         | 业务开通类型              | String | 2    | N    | 参见《[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明 |
| wx_applet_app_id | 微信小程序APPID           | String | 20   | N    | <font color="green">示例值：wx8523175fea790f10</font>                                              |
| wx_woa_app_id    | 公众号支付APPID           | String | 512  | N    | <font color="green">示例值：wx3767c5bd01df5061</font>                                              |
| wx_woa_path      | 微信公众号授权目录        | String | 512  | N    | <font color="green">示例值：https://paas.huifu.com/shouyintai/demo/h5/</font>|
| bank_channel_no  | 渠道号                    | String | 32   | N    |<font color="green">示例值：JQF00001</font> |
| business_desc    | 业务失败描述信息          | String | 512  | N    | 业务失败描述信息                                             |
| bank_message     | 微信/支付宝侧失败描述信息 | String | 512  | N    | 微信/支付宝侧失败描述信息                                    |
<!-- extend:end -->

#### 返回示例
```json
{
    "atu_config_bo_fail_list": "[{\"bank_channel_no\":\"10000001\",\"bank_message\":\"{\\\"path\\\":\\\"当前已 配置公众号支付支付域名个数已达上限，如需额外配置，请联系客服处理\\\"}\",\"business_desc\":\"{\\\"path\\\":\\\" 当前已配置公众号支付支付域名个数已达上限，如需额外配置，请联系客服处理\\\"}\",\"fee_type\":\"01\",\"wx_applet_app_id\":\"\",\"wx_woa_app_id\":\"\",\"wx_woa_path\":\"https://api.huifu.com/\"}]",
    "atu_config_bo_list": "[{\"bank_channel_no\":\"10000001\",\"fee_type\":\"01\",\"wx_applet_app_id\":\"wx852v3175fe90f170\",\"wx_config_list\":[{\"config_type\":\"3\",\"config_value\":\"https://api.huifu.com/\"},{\"config_type\":\"3\",\"config_value\":\"https://api.huifu.com/h5/\"},{\"config_type\":\"3\",\"config_value\":\"https://paas.huifu.com/che/\"},{\"config_type\":\"3\",\"config_value\":\"https://paas.huifu.com/che/\"},{\"config_type\":\"3\",\"config_value\":\"https://spin.cloudpnr.com\"},{\"config_type\":\"1\",\"config_value\":\"wx31dfd765c5b00617\"},{\"config_type\":\"1\",\"config_value\":\"wxdd6612b66dd131ab\"},{\"config_type\":\"1\",\"config_value\":\"wx85275fe90a731f10\"}],\"wx_woa_app_id\":\"wx3c5bd0171df50667\",\"wx_woa_path\":\"https://paas.huifu.com/che\"},{\"bank_channel_no\":\"10000001\",\"fee_type\":\"02\",\"wx_applet_app_id\":\"\",\"wx_config_list\":[{\"config_type\":\"3\",\"config_value\":\"https://api.huifu.com/\"},{\"config_type\":\"3\",\"config_value\":\"https://paas.huifu.com/che/\"},{\"config_type\":\"3\",\"config_value\":\"https://paas.huifu.com/che\"},{\"config_type\":\"1\",\"config_value\":\"wx31dc5bd01f506767\"}],\"wx_woa_app_id\":\"wx31d0506176f7c5bd\",\"wx_woa_path\":\"https://paas.huifu.com/che/\"}]",
    "resp_code": "00000000",
    "resp_desc": "成功"
}
```
