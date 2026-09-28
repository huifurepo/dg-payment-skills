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
## 商户多费率配置

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/busi/multiFee/config

*最近更新时间：2026.09.04*
### 应用场景
商户成功开通微信、支付宝功能后，可使用此接口配置多费率

**适用对象**  
已开通成功获得huifu_id的商户；

### 接口说明 
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

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                           

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号，同一商户号当天唯一； |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准； |
| huifu_id | 汇付商户号 | String | 18 | Y | 渠道与一级代理商的直属商户ID |
| <span class="extend 68db0e04_66e1_454d_aa1f_2b18146396e7">wx_conf_list</span> | 微信配置对象列表 | String |  | N | jsonArray格式，微信配置对象列表、支付宝配置对象列表不可同时为空 |
| <span class="extend 8632f047_d868_454e_83e6_fd07c58fc164">ali_conf_list</span> | 支付宝配置对象列表 | String |  | N | jsonArray格式，微信配置对象列表、支付宝配置对象列表不可同时为空 |

<!-- extend:start -->
<!-- div:extend-table 68db0e04_66e1_454d_aa1f_2b18146396e7-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1：线下反扫； 2：线下公众号； 3：线下小程序； 4：线上公众号； 5：线上小程序； 12：线上反扫； 示例值：1 |
| fee_rate | 手续费底价（%） | String | 6 | Y | 数字类型，大于等于0,保留2位小数；示例值：0.38 |
| fee_sign | 手续费场景标识 | String | 32 | N | 支付功能+场景维度生成的费率唯一标识，传入时支持修改 示例值：155677 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8632f047_d868_454e_83e6_fd07c58fc164-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 1：线下扫码； 2：线上扫码； 示例值：1 |
| fee_rate | 手续费底价（%） | String | 6 | Y | 数字类型，大于等于0,保留2位小数；示例值：0.38 |
| fee_sign | 手续费场景标识 | String | 32 | N | 支付功能+场景维度生成的费率唯一标识，传入时支持修改 示例值：155677 |
<!-- extend:end -->

### 返回参数


#### 成功

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| req_seq_id | 请求流水号 | String | 32 | Y | 原样返回请求参数的请求流水号；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 原请求时间yyyyMMdd；<font color="green">示例值：20220912</font> |
| conf_status | 配置状态 | String | 1 | Y | Y：成功 F：失败 |
| <span class="extend a427c7dc_ffdb_47c1_b736_3baf6b4ae09a">conf_list</span> | 配置信息 | String |  | N | jsonArray格式，配置成功时返回 |

<!-- extend:start -->
<!-- div:extend-table a427c7dc_ffdb_47c1_b736_3baf6b4ae09a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| pay_scene | 支付场景 | String | 2 | Y | 支付功能为W：微信时返回 1：线下反扫； 2：线下公众号； 3：线下小程序； 4：线上公众号； 5：线上小程序； 12：线上反扫； 支付功能为A：支付宝时返回 1：线下扫码； 2：线上扫码； 示例值：1 |
| fee_rate | 手续费底价（%） | String | 6 | Y | 数字类型，大于等于0,保留2位小数；示例值：0.38 |
| fee_sign | 手续费场景标识 | String | 32 | Y | 支付功能+场景维度生成的费率唯一标识，交易时支持传入 示例值：155677 |
| pay_way | 支付功能 | String | 1 | Y | A：支付宝 W：微信 示例值：A |
<!-- extend:end -->
