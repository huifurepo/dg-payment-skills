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
## 结算记录查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/basicdata/settlement/query

*最近更新时间：2026.11.04*
### 应用场景
商户可查询在汇付的所有结算记录及状态。

**适用对象**   
需要确认结算状态以及所有结算记录明细的商户，可调用该功能。查询时间范围100天。<!--戴辉江说支持100天查询-->

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| **参数**   | **中文名** | <div style="width: 40pt">**定义**</div>     | <div style="width: 25pt">**长度**</div>  | **必填** | **说明**                                                     |
| :--------- | :--------- | :------- | :------- | :------- | :----------------------------------------------------------- |
| sys_id     | 系统号     | String   | 32       | Y        | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id<br/><font color="green">示例值：6666000108854952</font> |
| product_id | 产品号     | String   | 32       | Y        | 汇付分配的产品号，<font color="green">示例值：YYZY</font> |
| sign       | 加签结果   | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)|
| data       | 请求数据   | JSON     |          | Y        | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | <div style="width: 40pt">**定义**</div>     | <div style="width: 25pt">**长度**</div> | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数，具体请参考下方接口返回参数                     |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 业务申请编号，同一商户号当天唯一，<br/><font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 请求时间yyyyMMdd，<font color="green">示例值：20220125</font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属商户ID；<br/><font color="green">示例值：6666000123123123</font> |
| begin_date | 结算开始日期 | String | 8 | Y | 起始日期yyyyMMdd，<font color="green">示例值：20220125</font> |
| end_date | 结算结束日期 | String | 8 | Y | 结束日期yyyyMMdd，<font color="green">示例值：20220125</font>；<br/>注：交易开始和结束日期需小于等于7天 |
| page_size | 分页条数 | String |  | Y | 最大50，最小1；<font color="green">示例值：10</font> |
| settle_cycle | 结算方式 | String | 2 | N | D1，T1，不传默认查询所有；<font color="green">示例值：T1</font> |
| page_num | 分页页码 | String |  | N | 不传则默认为第1页；<font color="green">示例值：2</font> |
| trans_stat | 交易状态 | String | 1 | N | I：初始化/处理中，S：成功，F：失败，P：处理中(锁定)；<br/>空白则未返回交易状态；<font color="green">示例值：S</font> |


#### 请求示例

```json
{
  "sys_id": "6666000107803321",
  "product_id": "EDUSTD",
  "data": {
    "req_seq_id": "rQ2021121311091597477647830088",
    "req_date": "20220116",
    "huifu_id": "6666000111938435",
    "begin_date": "20200810",
    "end_date": "20200810",
    "page_size": "10",
    "settle_cycle": "",
    "page_num": "1",
    "trans_stat": "I"
  },
  "sign": "CPiOcv4Rw1hvePkocm6Eev6XbTRVx3aFtUq9WrVzRBEEFgeCFTMNNFsXFBwYrvu9VpWzZGyV9klZF2kmFIFITmnid4YWtX/AEQI9iNUei0wDATXiUKdnm6B4i+qpV1VmvLhIfcENUVwBViiVtVUC+F1b2gq11ZWwvOQJ8E0AFAE="
}

```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：成功</font> |
| result_count | 查询结果总条数 | String |  | Y | 若无则返回0；<font color="green">示例值：100</font> |
| page_size | 分页条数 | String |  | Y | <font color="green">示例值：10</font> |
| page_num | 分页页码 | String |  | Y | <font color="green">示例值：2</font> |
| <span class="extend 10aa2806_a7c8_418a_b0bd_22ca45acf8f6">trans_log_result_list</span> | 结算信息结果列表 | String |  | N | jsonArray字符串 |

<!-- extend:start -->
<!-- div:extend-table 10aa2806_a7c8_418a_b0bd_22ca45acf8f6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| trans_id | 结算流水编号 | String | 16 | Y | 当天唯一，<font color="green">示例值：1000335187840801</font> |
| trans_date | 结算日期 | String | 8 | Y | 结算日期yyyyMMdd，<font color="green">示例值：20220125</font> |
| huifu_id | 结算汇付商户号 | String | 18 | N | 该笔结算对应的汇付商户号；<font color="green">示例值：6666000111938435</font> |
| settle_cycle | 结算方式 | String | 2 | N | D1，T1，默认查询所有；<font color="green">示例值：T1</font> |
| card_no | 银行卡号(掩码) | String | 64 | N | <font color="green">示例值：622262*********8994</font> |
| card_name | 银行户名 | String | 64 | N | <font color="green">示例值：张三</font> |
| bank_code | 银行编码 | String | 10 | N | [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；<font color="green">示例值：01040000</font> |
| trans_amt | 交易金额（元） | String | 16 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00，最大16位有效数字 |
| fee_amt | 结算手续费（元） | String | 16 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.00，最大16位有效数字 |
| fee_cust_id | 手续费汇付商户号 | String | 16 | N | 该笔结算手续费扣除对应的汇付商户号；<font color="green">示例值：6666000111938435</font> |
| trans_stat | 结算状态 | String | 1 | N | I:处理中 F:结算失败 S:结算成功，为空则未返回结算状态；<font color="green">示例值：S</font> |
| settle_type | 结算类型 | String | 1 | N | 0:对公结算 1:对私法人结算 2:对私非法人结算 3:虚拟户结算；<font color="green">示例值：0</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 商户在基本信息入驻时编辑的结算摘要；<font color="green">示例值：货款</font> |
| settle_batch_no | 结算批次号 | String | 12 | N | 0：0点昨日余额结算批次，非优先到账批则预计到账时间10:30<br/>100：1点余额结算批次，优先到账则预计到账时间06:50，非优先到账批则预计到账时间10:30<br/>200：2点余额结算批次，优先到账则预计到账时间06:50，非优先到账批则预计到账时间10:30<br/>300：3点余额结算批次，优先到账则预计到账时间06:50，非优先到账批则预计到账时间10:30<br/>400：4点余额结算批次，优先到账则预计到账时间06:50，非优先到账批则预计到账时间10:30<br/>500：5点余额结算批次，优先到账则预计到账时间06:50，非优先到账批则预计到账时间10:30<br/>600：6点余额结算批次，预计到账时间10:30<br/>700：7点余额结算批次，预计到账时间10:30<br/>800：8点余额结算批次，预计到账时间10:30<br/>900：9点余额结算批次，预计到账时间10:30<br/>1000：10点余额结算批次，预计到账时间14:00<br/>1100：11点余额结算批次，预计到账时间14:00<br/>1200：12点余额结算批次，预计到账时间14:00<br/>无值则结算昨日全部余额<br/><font color="green">示例值：100</font> |
| settle_desc | 结算信息 | String | 255 | N | 结算失败原因；<font color="green">示例值：</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
  "data": {
    "resp_desc": "成功",
    "resp_code": "00000000",
    "result_count": 1,
    "page_size": 10,
    "page_num": 1,
    "trans_log_result_list": [
      {
        "trans_id": "1000335187840700",
        "trans_stat": "I",
        "huifu_id": "6666000103208314",
        "settle_cycle": "T1",
        "card_no": "622262*********8994",
        "card_name": "王家三",
        "bank_code": "01030000",
        "trans_amt": "70.13",
        "fee_amt": "1.00",
        "fee_cust_id": "6666000103208314",
        "trans_date": "20200810",
        "settle_type": "2",
        "settle_abstract": "结算摘要",
        "settle_batch_no": "0"
      }
    ]
  }
}

```


#### webhook说明

斗拱结算完成后发送webhook结算通知事件【[statement.day](https://paas.huifu.com/open/doc/devtools/#/webhook/mb_jiesuan)】。webhook事件可以灵活配置多个接收端用于驱动业务流程。比如webhook结算消息发给财务系统入账等等。  
[webhook的使用参见说明](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao?id=%e5%a6%82%e4%bd%95%e4%bd%bf%e7%94%a8webhook)；

