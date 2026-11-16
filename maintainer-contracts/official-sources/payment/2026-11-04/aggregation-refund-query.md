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
## 交易退款查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v4/trade/payment/scanpay/refundquery

*最近更新时间：2026.05.28*
## 应用场景

商家调用退款接口未收到状态返回，调用本接口查询退款结果。支持微信公众号-T_JSAPI、小程序-T_MINIAPP、微信APP支付-T_APP、支付宝JS-A_JSAPI、支付宝正扫-A_NATIVE、银联二维码正扫-U_NATIVE、银联二维码JS-U_JSAP，以及微信反扫、支付宝反扫、银联二维码反扫交易退款的查询。

## 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sys_id     | 系统号   | String | 32   | Y    | 渠道商/代理商/商户的huifu_id <br />（1）当主体为渠道商/代理商时，此字段填写渠道商/代理商huifu_id； <br />（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font> |
| product_id | 产品号   | String | 32   | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>    |
| sign       | 加签结果 | String | 512  | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)    |
| data       | 请求数据 | JSON   |      | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成；<font color="green">示例值：6666000123123123</font> |
| org_req_date | 退款请求日期 | String | 8 | C | 退款发生的日期，格式为yyyyMMdd，<font color="green">示例值：20220925</font>；</br>传入退款全局流水号时，非必填，其他场景必填； |
| org_hf_seq_id | 退款全局流水号 | String | 128 | C | 退款请求流水号,退款全局流水号,终端订单号三选一不能都为空；<br/><font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_req_seq_id | 退款请求流水号 | String | 128 | C | 退款请求流水号,退款全局流水号,终端订单号三选一不能都为空；<br/><font color="green">示例值：202110210012100005</font> |
| mer_ord_id | 终端订单号 | String | 50 | C | 退款请求流水号,退款全局流水号,终端订单号三选一不能都为空；<br/><font color="green">示例值：16672670833524393</font> |


#### 请求示例

```json
{
  "sys_id": "6666000003100616",
  "product_id": "MYPAY",
  "data": {
    "org_hf_seq_id": "0031000topA250804164514P944c0a842bf00000",
    "huifu_id": "6666000003100616"
  },
  "sign": "VvcUT0WQLfkYsg0dns2qR7yFs/1Z/6YQcOymfRtG8wIdt/tSBNrlbIkI92kTu8p8TXkvZGUh796zOtJO900DsQAcVc0xcjNiFTX8jPDP61SsUJQ3xNbSwFd6dgIAHnlGA=="
}

```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](#业务返回码) |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| org_hf_seq_id | 退款全局流水号 | String | 128 | N | <font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_req_date | 退款请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| org_req_seq_id | 退款请求流水号 | String | 128 | N | <font color="green">示例值：202110210012100005</font> |
| ord_amt | 退款金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| actual_ref_amt | 实际退款金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| trans_date | 交易发生日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| trans_time | 交易发生时间 | String | 6 | N | 格式：HHMMSS；<font color="green">示例值：091010</font> 表示9点10分10秒 |
| trade_type | 交易类型 | String | 20 | N | <font color="green">示例值：TRANS_REFUND</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中；S：成功；F：失败；I: 初始<br/>初始状态很罕见，请联系汇付技术人员处理；<br/><font color="green">示例值：S</font> |
| <span class="showCompleteParams">bank_code</span> | 通道返回码 | String | 64 | N | <font color="green">示例值：01020000</font> |
| bank_message | 通道返回描述 | String | 256 | N | <font color="green">示例值：SUCCESS</font> |
| fee_amount | 手续费金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| trans_finish_time | 退款完成时间 | String | 14 | N | 格式yyyyMMddHHmmss；<font color="green">示例值：20091225091010</font> |
| pay_channel | 交易通道 | String | 1 | N | 枚举值：A-支付宝、T-微信、U-银联二维码、D-数字货币 |
| remark | 备注 | String | 84 | N | 退款时上送的备注，原样返回；<font color="green">示例值：备注</font> |
| <span class="extend c4af6174_0bd2_4546_8ed3_0623c76b4f42">tx_metadata</span> | 	扩展参数集合 | String |  | N | jsonObject字符串 |

<!-- extend:start -->
<!-- div:extend-table c4af6174_0bd2_4546_8ed3_0623c76b4f42-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 9fc7b699_8aeb_4ee7_90df_9906df40c7a5">acct_split_bunch</span> | 分账对象 | String |  | N | 分账对象，jsonObject字符串 |
| <span class="extend 8025ad83_3a7b_476d_b8ca_4e59ed75bcc5">split_fee_info</span> | 分账手续费信息 | String |  | N | 分账手续费信息 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9fc7b699_8aeb_4ee7_90df_9906df40c7a5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 3c95780c_0dc1_4d1a_8340_702508de9265">acct_infos</span> | 分账信息列表 | Array | 2048 | N | 分账信息列表 |
| is_clean_split | 是否净值分账 | String | 1 | N | Y:使用净值分账，仅在percentage_flag=Y时起作用；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3c95780c_0dc1_4d1a_8340_702508de9265-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 商户号 | String | 16 | Y | 分账商户号；<font color="green">示例值：6666000108854952</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8025ad83_3a7b_476d_b8ca_4e59ed75bcc5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| total_split_fee_amt | 分账手续费总金额(元) | String | 14 | N | <font color="green">示例值：0.10</font> |
| split_fee_flag | 分账手续费扣款标志 | Integer | 1 | Y | 1: 外扣 2: 内扣；<font color="green">示例值：1</font> |
| <span class="extend 32ada89b_2c11_4a16_a033_3baf8efab69e">split_fee_details</span> | 分账手续费明细 | Array |  | Y | jsonArray格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 32ada89b_2c11_4a16_a033_3baf8efab69e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| split_fee_amt | 分账手续费金额 | String | 14 | Y | <font color="green">示例值：1.00</font> |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| split_fee_acct_id | 分账手续费承担方账号 | String | 32 | N | <font color="green">示例值：F00598600</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
  "data": {
    "acct_split_bunch": "{}",
    "actual_ref_amt": "0.03",
    "bank_message": "正常结束",
    "combinedpay_fee_amt": "0.00",
    "fee_amount": "0.01",
    "huifu_id": "6666000003100616",
    "ord_amt": "0.03",
    "org_hf_seq_id": "0031000topA250804164514P944c0a842bf00000",
    "org_req_date": "20250804",
    "org_req_seq_id": "202508040442356120tt",
    "pay_channel": "A",
    "remark": "test0001",
    "resp_code": "00000000",
    "resp_desc": "查询成功",
    "trade_type": "TRANS_REFUND",
    "trans_date": "20250804",
    "trans_finish_time": "20250804164515",
    "trans_stat": "S",
    "trans_time": "164514"
  }
}

```


#### 业务返回码

| 返回码   | 返回描述                                                 |
| :------- | :------------------------------------------------------- |
| 00000000 | 查询成功                                                 |
| 10000000 | 入参数据不符合接口要求                                   |
| 20000001 | 并发冲突,请稍后重试                                      |
| 21000000 | 原退款全局流水号,原退款请求流水号,外部订单号不能同时为空 |
| 22000000 | 产品号不存在                                             |
| 22000000 | 产品号状态异常                                           |
| 23000001 | 原交易不存在                                             |
| 99999999 | 系统异常，请稍后重试                                     |

