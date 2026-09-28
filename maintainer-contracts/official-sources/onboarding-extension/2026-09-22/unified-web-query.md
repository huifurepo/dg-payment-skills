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
## 统一进件页面版查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/busi/status/query

*最近更新时间：2026.09.20*
*最近更新时间：2024.9.1* 
### 应用场景

服务商通过[商户统一进件（页面版）接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtyjjweb)进件后，可以通过本接口查询进件状态。


**适用对象**    
服务商希望通过汇付页面为商户完成汇付开户以及微信支付宝入驻，简化进件流程的开发。
  
### 接口说明
* 请求URL：https://api.huifu.com/v2/merchant/busi/status/query
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

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明|
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 请求时间 yyyyMMdd；<font color="green">示例值：20220915</font>   |
| store_id | 门店号 | String | 64 | Y | 门店号，<font color="green">示例值：SH001</font> |
| upper_huifu_id | 渠道商号 | String | 18 | N | sys_id为商户时，需传入，传入的值为商户统一进件时传入的upper_huifu_id <font color="green">示例值：6666000123123123</font> |


#### 请求示例

```json
{
    "data":{  
        "req_seq_id":"20230315839039744",  
        "req_date":"20230315",  
        "store_id":"yu653454308"  
    },  
    "sys_id":"6666000104483105",  
    "sign":"tV/wmpht7rRqjEodbApJgwUgRz8whOuc8OydOykDC599HC4iQxd/VJcj5I+oFSP/Tk1yyU4byULq2Wz08at1BdG9M6fAjbhcaFphZokazOmoYZywwpvqbz8ISzcpOm+MpRzj43k9Gj4la5Q22Z1W2oh6HBf88tzvVY+d1rOM37835mQ3h6+Rz7TchByVaN/zPRaUiMVzVX9E3vD+Msu2vqvZw0tCKSXdzMsuT15Zn7hKLjFy6R5u0lOaSNNq+lrI5YuEKPFofmMc8jeGTloNzao7+Z2ieTE5FO3HnzXZenMdxa/6fn6JnJ2gGELPixxfRqhkfFu3nn4RATCTatDsxg==",  
    "product_id":"ZDTEST"  
}
```
### 返回参数


#### 成功

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| channel_huifu_id | 渠道商汇付id | String | 18 | Y | <font color="green">示例值：6666000108854952</font>  |
| store_id | 门店号 | String | 64 | Y | <font color="green">示例值：SH001</font> |
| huifu_id | 汇付号 | String | 18 | Y | <font color="green">示例值：6666000108854955</font> |
| check_status | 审核状态 | String | 1 | N | Y：审核成功，N:审核拒绝，P:审核中<font color="green">示例值：Y</font> |
| head_office_flag | 商户身份 | String | 1 | N | 1：总部商户， 0：下级商户； 为空则为普通商户 <font color="green">示例值：1</font> |
| head_huifu_id | 上级汇付Id | String | 18 | N | head_office_flag为0时返回； <font color="green">示例值：6666000108854955</font> |
| use_chains_flag | 使用上级微信、支付宝商户号发起交易 | String | 8 | N | 1 微信+支付宝 2 不使用 3 微信 4 支付宝； <font color="green">示例值：1</font> |
| <span class="extend ea03a3f5_fda7_44a4_b800_7a4e5cd7890f">wx_pay_config_info</span> | 微信支付实体 | String |  | N | jsonArray格式字符串 |
| <span class="extend 80a7a814_a972_48a2_84f1_2322b00692c4">wx_real_name_list</span> | 微信实名实体 | String |  | N | jsonArray格式字符串 |
| <span class="extend 451cc53f_6b25_4345_bbba_8a300041e68e">ali_pay_config_info</span> | 支付宝支付实体 | String |  | N | jsonArray格式字符串 |
| <span class="extend b9fcc89e_8389_49d4_a1e8_f0160b3befff">ali_real_name_list</span> | 支付宝实名实体 | String |  | N | jsonArray格式字符串 |
| <span class="extend 9a303162_6905_4558_a17a_f4dce3a1bdee">agreement_info_list</span> | 协议信息 | String |  | N | jsonArray格式字符串 |

<!-- extend:start -->
<!-- div:extend-table ea03a3f5_fda7_44a4_b800_7a4e5cd7890f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| wx_pay_be_swept_down | 微信被扫支付线下 | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font>  |
| wx_pay_be_swept_down_rate | 微信被扫支付线下费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
| wx_public_account_down | 微信公众号支付线下 | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font> |
| wx_public_account_down_rate | 微信公众号支付线下费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
| wx_public_account_up | 微信公众号支付线上 | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font> |
| wx_public_account_up_rate | 微信公众号支付线上费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
| wx_small_program_down | 微信小程序线下  | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font> |
| wx_small_program_down_rate | 微信小程序线下费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
| wx_small_program_up | 微信小程序线上 | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font> |
| wx_small_program_up_rate | 微信小程序线上费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 80a7a814_a972_48a2_84f1_2322b00692c4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 场景 | String | 1 | Y | 参见《[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》 |
| authorize_stat | 授权状态 | String | 8 | Y | 1：授权成功；0：授权失败；<font color="green">示例值：1</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 451cc53f_6b25_4345_bbba_8a300041e68e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| ali_pay_be_swept_down | 支付宝被扫支付线下  | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font> |
| ali_pay_be_swept_down_rate | 支付宝被扫支付线下费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
| ali_master_sweep_down | 支付宝主扫支付线下 | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font> |
| ali_master_sweep_down_rate | 支付宝主扫支付线下费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
| ali_small_program_down | 支付宝小程序支付线下 | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font> |
| ali_small_program_down_rate | 支付宝小程序支付线下费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
| ali_small_program_up | 支付宝小程序线上 | String | 1 | Y | Y：已开通，N:未开通；<font color="green">示例值：Y</font> |
| ali_small_program_up_rate | 支付宝小程序线上费率(%) | String | 8 | N | <font color="green">示例值：0.6</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b9fcc89e_8389_49d4_a1e8_f0160b3befff-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 场景 | String | 1 | Y | 1-线下扫码；<font color="green">示例值：1</font>  |
| authorize_stat | 授权状态 | String | 8 | Y | 1：授权成功；0：授权失败；<font color="green">示例值：1</font>  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9a303162_6905_4558_a17a_f4dce3a1bdee-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_type | 协议类型 | String | 1 | N | 0-电子协议 |
| agreement_link | 协议签署链接 | String | 512 | N |  |
| agreement_no | 协议号 | String | 32 | N | <font color="green">示例值：3245234</font> |
| agreement_name | 协议名称 | String | 128 | N |  |
| con_stat | 合同状态 | String | 2 | N | 电子协议类型会返回以下值： 2：创建合同异常 3：待签约 4：签约中 5：签约完成(电子协议只有签约完成才能做交易) 6：已失效 7：已拒签 8：签约失败 <font color="green">示例值：5</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "成功",
        "channel_huifu_id": "6666000104483105",
        "store_id": "202303111364",
        "huifu_id": "6666000106678906",
        "check_status": "Y",
        "wx_pay_config_info": "{\"wx_pay_be_swept_down\":\"N\",\"wx_pay_be_swept_down_rate\":\"\",\"wx_public_account_down\":\"N\",\"wx_public_account_down_rate\":\"\",\"wx_public_account_up\":\"Y\",\"wx_public_account_up_rate\":\"2.00%\",\"wx_small_program_down\":\"N\",\"wx_small_program_down_rate\":\"\",\"wx_small_program_up\":\"N\",\"wx_small_program_up_rate\":\"\"}",
        "wx_real_name_list": "[{\"authorize_stat\":\"0\",\"pay_scene\":\"01\"}]",
        "ali_pay_config_info": "{\"ali_master_sweep_down\":\"N\",\"ali_master_sweep_down_rate\":\"\",\"ali_pay_be_swept_down\":\"N\",\"ali_pay_be_swept_down_rate\":\"\",\"ali_small_program_down\":\"Y\",\"ali_small_program_down_rate\":\"3.00%\",\"ali_small_program_up\":\"N\",\"ali_small_program_up_rate\":\"\"}",
        "ali_real_name_list": "[{\"authorize_stat\":\"0\",\"pay_scene\":\"1\"}]"
    },
    "sign": "Uvuo5KzpPKnEhHFY19y/7O6YS81A+nQuP3xMKJytT4hQdLwOss/dYOQ3EIYXYQwZyb4bk6JrA65GJU4bo159FFk4z25YrHCdPoTHB3sRKs2yyE0NL+4hEdW4Ykp8gCVidV3BopwSRHwm1hABNVfBdWB5qSWVtuCMqusdnbIl/f4="
}
```
