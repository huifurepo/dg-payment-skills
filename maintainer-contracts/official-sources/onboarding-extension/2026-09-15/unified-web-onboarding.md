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
## 商户统一进件（页面版）

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/url/forward

*最近更新时间：2026.07.27*
### 应用场景

服务商通过此接口获取商户进件页面地址，商户通过进件页面实现汇付开户、业务开通、微信/支付宝入驻、微信/支付宝实名认证以及与汇付签约等功能，支持商家类型：企业/个体工商户、小微商户。   
需要注意：一些场景或业务功能的开通需要人工审核，审核通过前即使交易功能开通也会存在交易限额。汇付会尽快完成审核，审核通过后恢复正常交易额度。

**适用对象**    
服务商希望通过汇付页面为商户完成汇付开户以及微信支付宝入驻，简化进件流程的开发。  
**注意：调用接口前渠道商需登录控台配置费率模板。**
  
### 接口说明
* 请求URL：https://api.huifu.com/v2/merchant/url/forward
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


### **同步返参**

**公共返回参数**

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明|
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |


### **异步返参**

**公共返回参数**

| 参数           | 中文名          | <div style="width: 40pt">定义</div>     | 长度 | 必填 | 说明             |
| :------- | :--------- | :------- | :------- | :------- | :------------------- |
| resp_code | 网关返回码  | String | 6   | Y  |[网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#%E7%BD%91%E5%85%B3%E8%BF%94%E5%9B%9E%E7%A0%81)  |
| resp_desc | 网关返回描述 | String | 512 | Y  |  网关返回描述      |
| sign      | 签名     | String |     | Y  | 签名，对报文整体签名  |
| data      | 业务返回参数 | String |     | N  | JSON        |


### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 请求时间 yyyyMMdd；<font color="green">示例值：20220915</font>  |
| upper_huifu_id | 渠道商号 | String | 18 | C | 汇付分配的渠道商号，该商户进件完成后将隶属该渠道商/代理商<br/>sys_id主体为渠道商时填写； <br/>sys_id主体为总部商户时选填；<br/><font color="green">示例值：6666000123123123</font>  |
| phone | 手机号 | String | 11 | N |  手机号；<font color="green">示例值：13917352618 |
| store_id | 门店号 | String | 64 | Y | 门店号，<font color="green">示例值：SH001 |
| expires | 跳转地址失效时间 | String | 5 | N | 单位秒；<font color="green">示例值：50000 |
| back_page_url | 返回页面URL | String | 256 | N | 进件完成后回跳指定页面。http或https开头；<br/><font color="green">示例值：http://service.huifu.com/xxx?grantsId=xx&encryptMsg=xxxx</font>  |
| async_receive_url | 异步接收URL | String | 256 | N | 消息接收地址，<font color="green">示例值：http://service.example.com/to/path |
| template_id | 模版编号 | String | 20 | N | 服务商控制台，商户入驻费率模版列表中模版编号；<font color="green">示例值：155677 |
| head_office_flag | 商户身份 | String | 1 | N | 1：总部商户， 0：下级商户； 不传默认普通商户。示例值：0 开通下级商户时，所选的上级商户需要有开通商户权限，需先调用[“开通下级商户权限配置接口”](https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt_xjshpz) |
| head_huifu_id | 上级汇付Id | String | 18 | N | 如果head_office_flag=0，则字段必填，如果head_office_flag=1，上级汇付Id不可传 |
| use_chains_flag | 使用上级微信、支付宝商户号发起交易 | String | 8 | N | 1是 2 否；<font color="green">示例值：2</font>; 1 微信+支付宝 2 不使用 3 微信 4 支付宝； 使用上级微信、支付宝商户号需对应开通微信、支付宝功能； |
| micro_biz_type | 小微经营类型 | String | 32 | N | MICRO_TYPE_STORE-门店场所,MICRO_TYPE_MOBILE-流动经营/便民服务,MICRO_TYPE_ONLINE-线上商品/服务交易;不传默认为MICRO_TYPE_MOBILE<font color="green">示例值：MICRO_TYPE_STORE |


#### 请求示例

```json
{
    "sys_id": "6666000108290240",
    "data": {
        "req_seq_id": "2022012614120615001",
        "req_date": "20220915",
        "upper_huifu_id": "6666000108290240",
        "phone": "13917352618",
        "store_id": "store128",
        "template_id": "155625",
        "expires": "50000"
    },
    "sign": "ePPIuy1ubTqumryLZl+2nXIX+9058Bdhg/07NrG5eXLn9msfKLapxwvE2yhhqU3xSdBtpZR9V93WNkhmzZnfBxBQqZCZLVwgNzxSBZa98nEWa3er1ZVguRo2DYJEUvxj17t0RZkELo+84bwNNRPD9GMyt4hKtvEeSJKJ8w+o+N0=",
    "product_id": "ZDTEST"
}
```
### 返回参数


#### 同步返回

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | 业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | 业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| req_seq_id | 请求流水号 | String | 32 | N | 原请求流水号；<font color="green">示例值：2022012614120615001 |
| req_date | 请求时间	 | String | 8 | N | 原请求时间yyyyMMdd；<font color="green">示例值：20220912 |
| product_id | 产品号	 | String | 32 | N | 汇付分配的产品号，<font color="green">示例值：MCS |
| url | 跳转地址	 | String | 32 | Y | 商户进件页面跳转地址；http或https开头； <font color="green">示例值：http://service.huifu.com/xxx?grantsId=xx&encryptMsg=xxxx |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_desc": "成功",
        "req_seq_id": "2022012614120615001",
        "product_id": "ZDTEST",
        "req_date": "20220915",
        "resp_code": "000000",
        "url": "http://service.huifu.com/xxx?grantsId=xx&encryptMsg=xxxx"
    },
    "sign": "ePPIuy1ubTqumryLZl+2nXIX+9058Bdhg/07NrG5eXLn9msfKLapxwvE2yhhqU3xSdBtpZR9V93WNkhmzZnfBxBQqZCZLVwgNzxSBZa98nEWa3er1ZVguRo2DYJEUvxj17t0RZkELo+84bwNNRPD9GMyt4hKtvEeSJKJ8w+o+N0="
}

```


#### 汇付审核异步data

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81)   |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | 业务返回描述 |
| req_seq_id | 请求流水号 | String | 32 | Y | <font color="green">示例值：2022012614120615001 |
| req_date | 请求日期 | String | 32 | Y | 请求时间yyyyMMdd；<font color="green">示例值：20220912 |
| product_id | 产品编号 | String | 32 | Y | <font color="green">示例值：YYZY |
| huifu_id | 商户汇付Id | String | 18 | Y |  参见同步返回的huifu_id；<font color="green">示例值：6666000105215341 |
| apply_no | 申请单 | String | 18 | Y | 与同步返回的申请单号相同；<font color="green">示例值：202209120038432 |
| audit_status | 审核状态 | String | 1 | Y | Y：审核通过 N：审核拒绝；<font color="green">示例值：Y |
| audit_desc | 审核状态描述 | String | 256 | N | <font color="green">示例值： |
| token_no | 取现卡序列号 | String | 20 | N | 填写了卡配置信息，审核通过后有值，交易时用到；<font color="green">示例值：10000919331 |
| store_id | 门店号 | String | 64 | Y | 商户门店号；<font color="green">示例值：SH001</font> |


#### 业务开通异步data

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81)   |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | 业务返回描述 |
| req_seq_id | 请求流水号 | String | 32 | Y | 原请求流水号；<font color="green">示例值：2022012614120615001 |
| req_date | 请求日期 | String | 8 | Y | 原请求时间yyyyMMdd；<font color="green">示例值：20220912 |
| product_id | 产品编号	 | String | 32 | Y | 固定值产品编号；<font color="green">示例值：YYZY |
| huifu_id | 汇付客户号	 | String | 18 | Y | 参见同步返回的huifu_id；<font color="green">示例值：6666000105215341 |
| apply_no | 申请单号	 | String | 18 | N | 汇付返回商户开户业务申请单号；<font color="green">示例值：202209120038432 |
| store_id | 门店号	 | String | 64 | Y | 商户门店号；<font color="green">示例值：SH001 |
| notify_type | 通知类型	 | String | 1 | Y | W:微信 A：支付宝 U:银联二维码 B:刷卡；<font color="green">示例值：W |
| ord_id | 通知流水号 | String | 44 | N | 回调方返回应答，应答内容为：”RECV_ORD_ID_”+该ordId |
| <span class="extend fd236071_3468_4be0_90d4_1c729689854b">reg_result_list</span> | 入驻结果集合 | Object |  | N | jsonArray格式；notify_type等于U或者B时，此集合最多只有一条数据; notify_type等于A或者W时，此集合可能有多条数据 |

<!-- extend:start -->
<!-- div:extend-table fd236071_3468_4be0_90d4_1c729689854b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 费率类型	 | String | 2 | N | 请求参数pay_scene；参见《[微信支付场景](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》说明；<font color="green">示例值：1 |
| business_stat	 | 业务开通状态	 | String | 1 | Y | S-成功，F-失败；<font color="green">示例值：S</font> |
| business_desc | 业务开通描述	 | String | 200 | N | 业务开通描述 |
| sub_mer_id | 二级商户号	 | String | 32 | N | 银联商户号或者微信/支付宝二级商户号；<font color="green">示例值：A1035134718828858326</font> |
| sub_mer_name	 | 二级商户名称	 | String | 50 | N |  <font color="green">示例值：上海汇付支付有限公司</font>        |
| pay_channel_id | 渠道号	 | String | 50 | N | <font color="green">示例值：JP00001</font>  |
| bank_mer_code | 真实商户号	 | String | 20 | N | <font color="green">示例值：2088431912900000</font> |
| wx_real_name_flag | 实名入驻标识	 | String | 1 | N |  Y-微信/支付宝实名认证，N-非微信/支付宝 实名认证；<br/>用于区分微信/支付宝配置和微信/支付宝实名；<br/>当notify_type是W/A时返回；<font color="green">示例值：Y</font>    |
<!-- extend:end -->
