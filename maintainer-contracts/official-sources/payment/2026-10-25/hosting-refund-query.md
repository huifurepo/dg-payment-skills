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
## 统一收银台交易退款查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/queryRefundInfo

*最近更新时间：2026.10.13*
### 应用场景
通过统一收银台交易退款接口进行退款，都可以通过本接口查询。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共请求参数

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sys_id     | 系统号     | String   | 32       | Y        | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font>  |
| product_id | 产品号     | String   | 32       | Y        | 汇付分配的产品号，<font color="green">示例值：YYZY</font>    |
| sign       | 加签结果   | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)|
| data       | 请求数据   | JSON     |          | Y        | 业务请求参数，具体值参考API文档                              |


### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944</font> |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成；<font color="green">示例值：6666000123123123</font> |
| org_req_date | 退款请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20221023</font> |
| org_hf_seq_id | 退款全局流水号 | String | 128 | C | 退款请求流水号/退款全局流水号二选一不能都为空；<br><font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_req_seq_id | 退款请求流水号 | String | 128 | C | 退款请求流水号/退款全局流水号二选一不能都为空；<br><font color="green">示例值：202110210012100005</font> |


#### 请求示例

```json
{  
    "sys_id": "6666000123123123",
    "product_id":"MYPAY",  
    "data":{  
        "req_date":"20231102",  
        "req_seq_id":"20231102q111302328123112121122121112",  
        "huifu_id":"6666000003100616",  
        "org_hf_seq_id":"",  
        "org_req_seq_id":"52022070919803411999411514",  
        "org_req_date":"20240229"  
    },  
    "sign": "dJCZn/tVUuzKh13ACOAcCSl/E6OvR018DXX1FZjqXVjQ5qpezzsEK7CJZRo91QFioC4EF/kI1ju04wlCBrRus7+/axbIXJlCAsNBR4Ixwz6N0gc1V8U0zB3jsDfOXYZleJKhcju3M+bJJ/5ne+LbvKhP8L0R3Fpc4+P7PH5Vf2Of7DDwyWApqstr75IppK/h8JedI8yt1lfQD5d2AEg5n8aGAmGMyy9V17UfcH153BSqP8gsJACKlkfEep2hQnR+2MG+wwvkfZReQKcpR3NgMAlGpcxyFRUF3X1nor/Cz5N9rxZW2IjNHmVZ9EMcIJKdby55RLkBf3b2kYZrCaHCTQ=="
}
```
### 返回参数


#### 同步返回参数

**公共返回参数**

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)   |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tkcx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tkcx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；<font color="green">示例值：操作成功</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220925</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944175651</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| org_hf_seq_id | 退款全局流水号 | String | 128 | N | <font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_req_date | 退款请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| org_req_seq_id | 退款请求流水号 | String | 128 | N | <font color="green">示例值：202110210012100005</font> |
| ord_amt | 退款金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| actual_ref_amt | 实际退款金额 | String | 14 | N | 扫码退款返回，<font color="green">示例值：1.00</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中；S：成功；F：失败；I: 初始<br>初始状态很罕见，请联系汇付技术人员处理；<br><font color="green">示例值：S</font> |
| bank_code | 通道返回码 | String | 64 | N | <font color="green">示例值：01020000</font> |
| bank_message | 通道返回描述 | String | 256 | N | <font color="green">示例值：SUCCESS</font> |
| fee_amt | 退款返还手续费 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| <span class="extend 12b39d00_efc2_4131_9625_abb7cd443868">acct_split_bunch</span> | 分账对象 | String |  | N | 分账对象，jsonObject字符串 |
| <span class="extend 9572b26f_326d_4c5f_8d83_d10b3198a766">split_fee_info</span> | 分账手续费信息 | String |  | N | 分账手续费信息，jsonObject字符串 |
| org_party_order_id | 原交易用户账单上的商户订单号 | String | 64 | N | 扫码退款返回；<font color="green">示例值：H2022050711225100912503288</font> |
| remark | 备注 | String | 84 | N | 扫码退款返回；<font color="green">示例值：备注</font> |
| loan_flag | 是否垫资退款 | String | 2 | N | Y 是垫资出款， N 是普通出款，为空默认N；<font color="green">示例值： N</font><br>注意：延时交易退款在【交易确认退款】接口中设置loan_flag为垫资，<br/>本接口不可再次设置垫资。 |
| loan_undertaker | 垫资承担者 | String | 32 | N | 垫资方的huifu_id；<font color="green">示例值：6666000123123123</font><br/>为空则各自承担。不为空走第三方垫资，目前支持商户垫资； |
| loan_acct_type | 垫资账户类型 | String | 2 | N | 01:基本户, 05: 充值户, 默认充值户；<font color="green">示例值：01</font> |
| org_out_order_id | 原外部订单号 | String | 128 | N | 扫码退款返回；<font color="green">示例值：H2022050711225100912503288</font> |
| <span class="extend f2608321_70a2_422f_8bb8_9b78ed1c844d">unionpay_response</span> | 银联返回的响应报文 | String | 6000 | N | 扫码退款返回，同扫码退款查询接口，jsonObject字符串 |
| <span class="extend 1775314c_9876_4227_b8e5_b0b858d184b9">dy_response</span> | 抖音返回的响应报文 | String | 6000 | N | 抖音返回的响应报文，jsonObject字符串 |
| trans_finish_time | 退款完成时间 | String | 14 | N | 格式yyyyMMddHHmmss；<font color="green">示例值：20091225091010</font> |
| <span class="extend 9709647c_76d7_481f_b000_58d54cf712b9">sub_orders_response</span> | 退款子单返回信息列表 | String |  | N | jsonArray格式字符串；合单支付的订单返回该字段 |

<!-- extend:start -->
<!-- div:extend-table 12b39d00_efc2_4131_9625_abb7cd443868-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 3e268e44_2e52_462b_b85a_6d77e6dfaf0b">acct_infos</span> | 分账明细 | Array | 2048 | Y | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3e268e44_2e52_462b_b85a_6d77e6dfaf0b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>；最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| acct_id | 账户号 | String | 16 | N | <font color="green">示例值：F00598600</font> |
| part_loan_amt | 垫资金额 | String | 12 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01；<br/>注：若由第三方全额垫资，则不传该字段 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9572b26f_326d_4c5f_8d83_d10b3198a766-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| total_split_fee_amt | 分账手续费总金额(元) | String | 14 | N | 单位元 |
| split_fee_flag | 分账手续费扣款标志 | String | 1 | N | 1: 外扣 2: 内扣 |
| <span class="extend 355bd3ce_f2a0_488e_a89a_ef82b9e3b4fb">split_fee_details</span> | 分账手续费明细 | Array |  | N | 分账手续费明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 355bd3ce_f2a0_488e_a89a_ef82b9e3b4fb-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| split_fee_amt | 分账手续费金额(元) | String | 14 | Y | 单位元 |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | 斗拱开户时生成；示例值：6666000108854952 |
| split_fee_acct_id | 分账手续费承担方账号 | String | 16 | Y | 分账手续费承担方账号；<font color="green">示例值：F00598600</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f2608321_70a2_422f_8bb8_9b78ed1c844d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend bbcb2bc3_24b1_42e1_a0e3_9c6ab65555e4">coupon_info</span> | 银联优惠信息 | String |  | N | 银联使用优惠活动时出现，jsonArray字符串格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bbcb2bc3_24b1_42e1_a0e3_9c6ab65555e4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
| spnsrId | 出资方 | String | 20 | N | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font> |
| type | 项目类型 | String | 4 | N | DD01：随机立减， CP01：抵金券；<font color="green">示例值：DD01</font> |
| offstAmt | 抵消交易金额 | String | 14 | N | 不能为全0；单位元；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1775314c_9876_4227_b8e5_b0b858d184b9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| org_out_trans_id | 抖音原交易订单号 | String | 32 | N | <font color="green">示例值：20201030189770</font> |
| out_trans_id | 抖音退款单号 | String | 32 | N | <font color="green">示例值：6545342375</font> |
| payer_refund | 用户退款金额 | String | 12 | N | 退款给用户的金额，不包含所有优惠券金额 ，单位:元；<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9709647c_76d7_481f_b000_58d54cf712b9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_huifu_id | 退款子单商户号 | String | 32 | N | <font color="green">示例值：6666000108854952</font> |
| sub_req_date | 退款子单请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| sub_req_seq_id | 退款子单请求流水号 | String | 128 | N | <font color="green">示例值：rQ202112131117394413651</font> |
| sub_hf_seq_id | 退款子单全局流水号 | String | 128 | N | <font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| sub_org_req_date | 原子单交易请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| sub_org_req_seq_id | 原子单交易请求流水号 | String | 128 | N | <font color="green">示例值：</font> |
| sub_org_ord_amt | 原子单交易订单金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| sub_org_fee_amt | 原子单交易手续费 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| sub_trans_date | 子单退款交易发生日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| sub_ord_amt | 子单退款金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| sub_actual_ref_amt | 子单实际退款金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| sub_total_ref_amt | 原子单交易累计退款金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| sub_total_ref_fee_amt | 原子单交易累计退款手续费金额 | String | 14 | N | 单位元，<font color="green">示例值：1.00</font>；注意：退还手续费规则参见[说明文档](https://paas.huifu.com/open/doc/api/#/api_tksxfsm) |
| sub_ref_cut | 子单累计退款次数 | String | 14 | N | <font color="green">示例值：1</font> |
| <span class="extend 65ee35a6_76b5_445f_822d_f60884a35b06">acct_split_bunch</span> | 分账信息 | String | 4000 | N | 分账信息 |
| <span class="extend e8506075_4979_447d_9720_d0d9c480d7b5">split_fee_info</span> | 分账手续费信息 | String |  | N | 分账手续费信息 |
| sub_remark | 子单备注 | String | 1500 | N | 原样返回；<font color="green">示例值：子单备注</font> |
| fund_freeze_stat | 资金冻结状态 | String | 16 | N | FREEZE：冻结；UNFREEZE：解冻；<font color="green">示例值：UNFREEZE</font><br>退款发生时，对应原交易的资金冻结状态。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 65ee35a6_76b5_445f_822d_f60884a35b06-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 25a81496_2923_424c_9e83_1c7eb7dbf5ce">acct_infos</span> | 分账明细 | String | 2048 | N | 分账明细 |
| fee_amt | 退款返还手续费 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 25a81496_2923_424c_9e83_1c7eb7dbf5ce-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000108854952</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e8506075_4979_447d_9720_d0d9c480d7b5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| total_split_fee_amt | 分账手续费总金额(元) | String | 14 | N | <font color="green">示例值：0.10</font> |
| split_fee_flag | 分账手续费扣款标志 | Integer | 1 | Y | 1: 外扣 2: 内扣；<font color="green">示例值：1</font> |
| <span class="extend 0701de1f_a641_45ad_bb7d_2f28e34d9805">split_fee_details</span> | 分账手续费明细 | String |  | Y | jsonArray格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0701de1f_a641_45ad_bb7d_2f28e34d9805-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| split_fee_amt | 分账手续费金额 | String | 14 | Y | <font color="green">示例值：1.00</font> |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| split_fee_acct_id | 分账手续费承担方账号 | String | 9 | N | <font color="green">示例值：F00598600</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{  
    "data":{  
        "resp_code":"00000000",  
        "resp_desc":"操作成功",  
        "huifu_id":"6666000003100616",  
        "org_hf_seq_id":"0056default240305162924Pa41a9ac1984fd843",  
        "org_req_date":"20240229",  
        "org_req_seq_id":"52022070919803411999411514",  
        "ord_amt":"0.01",  
        "actual_ref_amt":"",  
        "trans_stat":"S",  
        "bank_code":"00",  
        "bank_message":"交易成功",  
        "fee_amt":"0.00",  
        "acct_split_bunch": "{\"acct_infos\":[{\"acct_id\":\"B00164310\",\"div_amt\":\"0.01\",\"huifu_id\":\"6666000003100616\"}]}",
        "split_fee_info": "{\"total_split_fee_amt\":0}", 
        "org_party_order_id":"202403051611224y3v28C1Y0",  
        "org_out_order_id":"20240305161117defaultit671658378",  
        "req_date":"20231102",  
        "req_seq_id":"20231102q111302328123112121122121112"  
    }  
}
```
