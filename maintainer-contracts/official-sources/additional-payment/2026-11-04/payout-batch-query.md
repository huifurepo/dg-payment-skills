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
## 批量出金交易查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/batchtranslog/query

*最近更新时间：2026.07.20*
### 应用场景
当出现需要批量查询斗拱账户出款到银行账户记录时可以调用此接口。查询的类型包括银行卡代发与取现。

**适用对象**    
有交易订单生成的斗拱客户。
  
### 接口说明
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
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 商户号 | String | 32 | Y | 汇付分配的商户号，<font color="green">示例值：6666000108854952</font> |
| begin_date | 开始日期 | String | 8 | Y | 格式:yyyyMMdd；<font color="green">示例值：20221213</font> |
| end_date | 结束日期 | String | 8 | Y | 格式:yyyyMMdd；<font color="green">示例值：20221213</font> |
| batch_trans_type | 交易类型 | String | 20 | N | SURROGATE-银行卡代发<br/>ENCHASHMENT-取现<br/>TSENCHASHMENT-TS结算<br/>不传默认银行卡代发、取现都查； <font color="green">示例值：ENCHASHMENT</font> |
| page_num | 分页页码 | String |  | N | 默认1；<font color="green">示例值：5</font> |
| page_size | 分页条数 | String |  | N | 默认10；<font color="green">示例值：10</font> |
| payment_hf_seq_id | 原支付全局流水号 | String | 128 | N | TS结算查询使用，对应为原交易的hf_seq_id；该值不为空时，商户号；开始日期；结束日期，非必填。 |


#### 请求示例

```json
{
  "sys_id": "TOP",
  "product_id": "HSK",
  "data": {
    "huifu_id": "6666000000041651",
    "begin_date": "20230315",
    "end_date": "20230316",
    "batch_trans_type": "",
    "page_num": "1",
    "page_size": "10"
  },
  "sign": "JlsLF3ILEhgcEjnVr+bHxhaXnbxFQBlmaHaYHYnCPTRXhJnDHuAGp7NezUhtMdCNevVUUA3uYbjSfpVw9ny1FYUv9HAYDQ1fL8TCpNDPHFCabEqtepoAgYbuV+lkQUyV+h/oGi/Uct4lcELGnZ7DVvjc/TspWc1mkJAL54bcPjZfqsQvMT8oTc7562fO163/Cnkc0p8fQvgIk8h3EaiAV0LShdKEkQOay/3GvTlpK6alHlxPd6HlQAnX+wkACTvd0T8SlJ5rYOmZQ1voNjcOzCX0TUw3xlWdQfyXaeK++bcN4wOXlsYGwIN7wY4Tf4TEuI1Mfzo4P28eqm2wfOBD6A=="
}

```
### 返回参数


#### 返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#业务返回码)；<font color="green">示例值：成功</font> |
| page_num | 分页页码 | String | 4 | Y | <font color="green">示例值：1</font> |
| page_size | 分页条数 | String | 4 | Y | <font color="green">示例值：11</font> |
| result_count | 查询结果总条数 | String |  | Y | <font color="green">示例值：10</font> |
| <span class="extend bc545557_6fc6_4e74_b7fb_9f2b5a695944">trans_log_result_list</span> | 交易信息结果列表 | Array |  | N |  |

<!-- extend:start -->
<!-- div:extend-table bc545557_6fc6_4e74_b7fb_9f2b5a695944-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| batch_trans_type | 交易类型 | String | 20 | N | SURROGATE-银行卡代发、ENCHASHMENT-取现、TSENCHASHMENT-TS结算；<font color="green">示例值：ENCHASHMENT</font> |
| cash_amt | 交易金额 | String | 14 | Y | 单位：元；保留两位小数；<font color="green">示例值：1.00</font> |
| fee_amt | 手续费金额 | String | 14 | Y | 单位：元；保留两位小数；<font color="green">示例值：1.00</font> |
| org_hf_seq_id | 原交易返回的全局流水号 | String | 128 | Y | <font color="green">示例值：0030000topB230316111634P778c0a8314500000</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20230301</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | Y | <font color="green">示例值：202109167745558220003</font> |
| trans_status | 交易状态 | String | 1 | Y | S：成功； F：失败； P：处理中；<font color="green">示例值：S</font> |
| remark | 备注 | String | 1000 | N | <font color="green">示例值：红包取现</font> |
| trans_desc | 交易描述 | String | 256 | N | <font color="green">示例值：用户取现</font> |
| huifu_id | 汇付商户号 | String | 32 | N | 汇付分配的商户号，示例值：6666000108854952 |
| acct_id | 账户号 | String | 32 | N | 账户号，示例值：F00598600 |
| bank_name | 银行名称 | String | 60 | N | 示例值：中国工商银行 |
| card_no | 银行卡号 | String | 64 | N | 示例值：621214*****0146 |
| card_name | 银行户名 | String | 60 | N | 示例值：盈盈超市112 |
| fee_flag | 手续费收取方式 | String | 1 | N | 1外扣，2内扣 |
| fee_huifu_id | 手续费客户号 | String | 32 | N | 示例值：6666000108854952 |
| fee_acct_id | 手续费账户号 | String | 32 | N | 示例值：F00598600 |
| payment_hf_seq_id | 原支付全局流水号 | String | 128 | N | 示例值：0030000topB230316111634P778c0a8314500000 |
| re_exchange | 退汇状态 | String | 1 | N | Y-已退汇；<font color="green">默认为空，该字段为Y时代表已退汇</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
  "data": {
    "resp_code": "00000000",
    "resp_desc": "成功",
    "page_num": 1,
    "page_size": 2,
    "result_count": 51,
    "trans_log_result_list": "[{\"batch_trans_type\":\"SURROGATE\",\"cash_amt\":\"1.00\",\"fee_amt\":\"0.00\",\"org_hf_seq_id\":\"HFPYA6666000000041651P504919113505701888\",\"org_req_date\":\"20230315\",\"org_req_seq_id\":\"fap001504919113588539392\",\"remark\":\"\",\"trans_desc\":\"\",\"trans_status\":\"F\"},{\"batch_trans_type\":\"SURROGATE\",\"cash_amt\":\"1.00\",\"fee_amt\":\"1.00\",\"org_hf_seq_id\":\"HFPYA6666000000041651P504919074951659520\",\"org_req_date\":\"20230315\",\"org_req_seq_id\":\"fap001504919075080634368\",\"remark\":\"\",\"trans_desc\":\"\",\"trans_status\":\"F\"}]"
  }
}

```
