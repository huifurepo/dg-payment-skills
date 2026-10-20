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
## 余额支付退款

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/acctpayment/refund

*最近更新时间：2025.02.25*
### 应用场景
本API为后台版接口，用于支持余额支付成功交易的全额或部分退款。

**适用对象**   
已开通余额支付相关功能的商户。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| **参数**   | **中文名** | **定义** | **长度** | **必填** | **说明**                                                     |
| :--------- | :--------- | :------- | :------- | :------- | :----------------------------------------------------------- |
| sys_id     | 系统号     | String   | 32       | Y        | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id<br/><font color="green">示例值：6666000108854952</font> |
| product_id | 产品号     | String   | 32       | Y        | 汇付分配的产品号，<font color="green">示例值：YYZY</font> |
| sign       | 加签结果   | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)|
| data       | 请求数据   | JSON     |          | Y        | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| **参数** | **中文名** | **定义** | **长度** | **必填** | **说明**             |
| :------- | :--------- | :------- | :------- | :------- | :------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：2021091708126665001</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20221023</font> |
| huifu_id | 商户号 | String | 32 | Y | 发起方商户号，示例值：6666000109812123 |
| org_req_date | 原余额支付请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20221023</font> |
| org_req_seq_id | 原余额支付请求流水号 | String | 128 | C | org_hf_seq_id和orgReqSeqId二选一；<br/><font color="green">示例值：2021091708126665001</font> |
| org_hf_seq_id | 原余额支付支付全局流水号 | String | 128 | C | org_hf_seq_id和orgReqSeqId二选一；<br/><font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| ord_amt | 退款金额 | String | 14 | Y | <font color="green">示例值：10.00</font> |
| <span class="extend 9128befd_e598_46c7_8e5b_5db4cb062ef2">acct_split_bunch</span> | 分账对象 | String |  | N | 分账信息，jsonObject字符串。余额支付分账给一个商户或多个商户，退款时也支持从多个商户分账退款。<br/>每个商户退款金额不能超过原入账金额。 |
| <span class="extend 506673b0_6401_4081_8309_18c73b5747ba">risk_check_data</span> | 安全信息 | String |  | N | jsonObject字符串。例如:"{"subProduct":"","transferType":""}" |
| remark | 备注 | String | 256 | N | <font color="green">示例值：备注</font> |

<!-- extend:start -->
<!-- div:extend-table 9128befd_e598_46c7_8e5b_5db4cb062ef2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 26f8ea3a_f58d_4562_894b_3b3360aa8987">acct_infos</span> | 退账明细 | Array |  | Y | 退款明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 26f8ea3a_f58d_4562_894b_3b3360aa8987-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 退款金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ,最低传入0.01 |
| huifu_id | 退款方ID | String | 32 | Y | 开户自动生成编号；<font color="green">示例值：6666000108854952</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 506673b0_6401_4081_8309_18c73b5747ba-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_product | 产品子类 | String | 20 | N | <font color="green">示例值：1</font> |
| transfer_type | 转账原因 | String | 2 | Y | 01：卡券推广类；02：卡券核销类；03：消费；04：工资代发；05：分润；<font color="green">示例值：01</font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "data": {
        "org_req_date": "20240515",
        "org_req_seq_id": "20240515132857954fk8wpk2hvwnnfw",
        "ord_amt": "0.01",
        "req_seq_id": "20240515134124629vmalwxl5nxajgd",
        "req_date": "20240515",
        "org_hf_seq_id": "",
        "remark": "1234567890",
        "risk_check_data": "{\"transfer_type\":\"04\",\"sub_product\":\"卡券推广类\"}",
        "huifu_id": "6666000109133323"
    },
    "product_id": "YYZY",
    "sign": "ip/PBG+Wyx++ocULyzpaomO83R+YFDZBW2rtVQC1pcAOGqLYOGmVpjMNZ/fd1Frv18dbpeICLVNP878NGtu8GtQMKP28mEawIpuUtEY1s9dUXfYRotWtychAZ1ZOwLQLKPrWqLNB0EFrpALunKBr1KDZyLW+70oRyoc/cxuPbpjxmCSU2OPwzTDKRCFmUYSaoevpQw/AHJcxJYwP2X3rVk96TCmy7+V+xzDBSR6YAq/PKmXKg+vO1/4Csx8JrqYIghU/6KfFLJz7Epu45ntryWV2ufUBLHoWj8KQjb/IeCC3gCapCMOzjvXCFmSEYbRTSOFn8jk25/IsI6wzOhT4Ng=="
}
```
### 返回参数


#### 同步响应参数

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](#业务返回码)  ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：交易成功</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 业务请求流水号；<font color="green">示例值：2022082408452985319884</font> |
| req_date | 请求日期 | String | 8 | Y | 请求日期。格式：yyyyMMdd，<font color="green">示例值：20221013</font> |
| huifu_id | 商户号 | String | 32 | Y | 发起方商户号；示例值：6666000108854952 |
| product_id | 产品号 | String | 32 | Y | 接入时提供；<font color="green">示例值：YYZY</font> |
| hf_seq_id | 全局流水号 | String | 40 | N | 汇付返回流水号；<font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| ord_amt | 退款金额 | String | 14 | Y | <font color="green">示例值：20.00</font> |
| org_req_date | 原余额支付请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20221103</font> |
| org_req_seq_id | 原余额支付请求流水号 | String | 128 | Y | <font color="green">示例值：2022082408452985319883</font> |
| org_hf_seq_id | 原余额支付支付全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00001</font> |
| trans_stat | 交易状态 | String | 1 | N | P:处理中；S：成功；F：失败；<font color="green">示例值：S</font> |
| trans_finish_time | 退款完成时间 | String | 14 | Y | 格式yyyyMMddHHmmss；<font color="green">示例值：20221104132334</font> |
| <span class="extend f0a953fd_70a7_460f_80db_a8dbb569f621">acct_split_bunch</span> | 退款分账串 | String |  | N | 分账信息，jsonObject字符串。<br/>余额支付分账给一个商户或多个商户，退款时也支持从多个商户分账退款。<br/>每个商户退款金额不能超过原入账金额。 |
| remark | 备注 | String | 256 | N | <font color="green">示例值：备注</font> |

<!-- extend:start -->
<!-- div:extend-table f0a953fd_70a7_460f_80db_a8dbb569f621-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend ab4a5a57_48eb_45be_8311_37b0e1ea4731">acct_infos</span> | 退账明细 | Array |  | Y | 退款明细 |
| fee_huifu_id | 手续费承担方商户号 | String | 16 | N | <font color="green">示例值：6666000123123123</font> |
| fee_acct_id | 手续费承担方账户号 | String | 32 | N | <font color="green">示例值：A28356961</font> |
| fee_amt | 手续费 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ab4a5a57_48eb_45be_8311_37b0e1ea4731-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 退款金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ,最低传入0.01 |
| huifu_id | 退款方ID | String | 32 | Y | 开户自动生成编号；<font color="green">示例值：6666000108854952</font> |
| acct_id | 账户号 | String | 32 | N | 分账账户号；<font color="green">示例值：F00598600</font> |
| fee_amt | 手续费金额 | String | 14 | N | 单位:元。仅在分账接受方承担手续费时返回。 <font color="green">示例值：0.02</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "req_date": "20211021",
        "req_seq_id": "20211021787214848332",
        "huifu_id": "6666000018344461",
        "product_id": "SPIN",
        "ord_amt": "0.01",
        "org_req_date": "20211021",
        "org_hf_seq_id": "",
        "org_req_seq_id": "202110210012100005",
        "trans_stat": "S",
        "trans_finish_time": "20211021164131",
        "remark": "1234567890"
    },
    "sign": "gWt0tyu/dOsU0mizxnV+DowPn77a2EMdmNpO4P6QhMOE2zGiY1l1VOP9if7Xez7XPKPACyJDYMNT48HMxHBqcefWHwn1Dj6/EEp4HCXqdMilIaK67jvP7wmsmPYhWG8bm7dGZNMFkHizAE4YGG1eNYdUZ3PR8ZAh1fkOsFkIQyatxv0e1mSIRRtj62kdx97dnmxd7IUgeng8tbrdTk/UiTOm5ItlJ0Z0jt9DUPDWMuESLyKfP+fQJdHFdMTZkqQHVoCLn4t7sW9XXTB1zyiFkyDeMHkInk7tF2w979p6oxb4sYPLkCxskwCfraz2YhRv+v01ByN4wn5DjLl4zLw0tQ=="
}
```


#### 业务返回码

* 查看全部 *[公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)*

| 返回码   | 返回描述                                                     | 处理                                        |
| :-------- | :------------------------------------------------------------ | :------------------------------------------- |
| 10000000 | %s不能为空 <br />%s长度固定%d位 <br />%s最大长度为%d位 <br />%s的传入枚举(%s)不存在 <br />%s不符合xx格式 <br />%s解密失败<br />（%s代指报错参数名、%d代指字段长度） | 入参数据不符合接口要求,参考接口文档调整入参 |
| 22000000 | 产品号不存在                                                 | 确认产品号对应的产品信息是否正常            |
| 22000000 | 产品号状态异常                                               | 确认产品号对应的产品信息是否正常            |
| 20000000 | 重复交易                                                     | 重复的交易，建议重新生成请求流水号发起请求  |
| 22000003 | 钱包账户信息不存在                                           |                                             |
| 23000004 | 暂不支持通过全局流水号退款                                   |                                             |
| 23000001 | 原交易不存在                                                 | 请检查录入的原交易订单信息是否正确          |
| 23000002 | 该交易商户号与原交易商户号不一致                             |                                             |
| 23000000 | 原余额支付交易未成功，暂不支持退款                           |                                             |
| 23000003 | 申请退款金额大于可退余额                                     |                                             |
| 22000004 | 暂未开通退款权限                                             | 确认商户开通了退款权限                      |
| 23000003 | 手续费退款金额大于可退手续费金额                             |                                             |
| 23000003 | 退款金额大于待确认金额                                       |                                             |
| 23000002 | 退款手续费承担方和原交易手续费承担方不一致                   |                                             |
| 23000003 | 退款分账金额不能大于可退分账金额                             |                                             |
| 23000004 | 分账串信息与原交易不匹配                                     |                                             |
| 23000003 | 退款分账串金额总和必须等于退款订单金额                       |                                             |
| 20000001 | 并发冲突，请稍后重试                                         |                                             |
| 90000000 | 交易存在风险                                                 | 交易被风控系统拦截                          |
| 90000000 | 业务执行失败                                                 |                                             |
| 00000000 | 退款成功                                                     |                                             |
| 00000100 | 交易处理中                                                   |                                             |
| 98888888 | 系统错误                                                     |                                             |

