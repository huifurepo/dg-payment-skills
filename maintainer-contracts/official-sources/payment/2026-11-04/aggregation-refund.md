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
## 交易退款

<span class="request-method post-method">POST</span>https://api.huifu.com/v4/trade/payment/scanpay/refund

*最近更新时间：2026.06.05*
## 接口说明

交易发生之后一段时间内，由于用户或者商户的原因需要退款时，商户可以通过本接口将支付款退还给用户，退款成功资金将原路返回。支持 T_JSAPI：微信JS支付、
T_MINIAPP:  微信小程序支付、T_MICROPAY：微信付款码支付、A_JSAPI: 支付宝JS支付、A_NATIVE: 支付宝正扫、A_NATIVE: 支付宝付款码、U_JSAPI: 银联JS支付、U_NATIVE: 银联正扫支付、U_MICROPAY: 银联付款码 

支持最大退款期限：
* 微信：360天
* 支付宝：360天
* 银联二维码：360天

## 公共参数

* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000108854952</font> |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220925</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944175651</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font> |
| ord_amt | 申请退款金额 | String | 14 | Y | 单位元，需保留小数点后两位；<font color="green">示例值：1.00</font>，最低传入0.01<br/>**注意：如果是原交易是延时交易，退款金额必须小于等于待确认金额** |
| org_req_date | 原交易请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20220925</font> |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；<br/><font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_party_order_id | 原交易微信支付宝的商户单号 | String | 64 | N | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；<br/><font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；<br/><font color="green">示例值：202110210012100005</font> |
| remark | 备注 | String | 84 | N | 原样返回；<font color="green">示例值：备注</font> |
| notify_url | 异步通知地址 | String | 512 | N | <font color="green">示例值： http://service.example.com/to/path</font> |
| <span class="extend 9b895fc1_72fa_46ac_926e_544ee399c240">tx_metadata</span> | 扩展参数集合 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |

<!-- extend:start -->
<!-- div:extend-table 9b895fc1_72fa_46ac_926e_544ee399c240-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 929f8899_e792_4cbc_a0b8_0c722375081c">acct_split_bunch</span> | 分账对象 | String | 2048 | N | 分账信息，jsonObject字符串 |
| <span class="extend 5aa673f5_49a9_4b28_a1bb_c2fdc751995d">combinedpay_data</span> | 补贴支付信息 | String |  | N | jsonArray字符串；参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| <span class="extend 2f826ba1_18df_4b50_bdf0_eea610b55d52">terminal_device_data</span> | 设备信息 | String | 2048 | N | 设备信息，jsonObject字符串 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 929f8899_e792_4cbc_a0b8_0c722375081c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 99a44d9a_113e_486f_b2f5_a71e003eda58">acct_infos</span> | 分账信息列表 | Array | 2048 | N | 分账明细 |
| <span class="extend 8d42f4ef_bcaf_497e_96da_0e3cfb7b9a64 showCompleteParams">confirm_acct_infos</span> | 交易确认分账信息列表 | Array | 2048 | N | 交易确认分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 99a44d9a_113e_486f_b2f5_a71e003eda58-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000108854952</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8d42f4ef_bcaf_497e_96da_0e3cfb7b9a64-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| confirm_hf_seq_id  | 交易确认单号 | String | 128 | Y |  |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000108854952</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5aa673f5_49a9_4b28_a1bb_c2fdc751995d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 汇付商户号 | String | 32 | Y | 渠道与一级代理商的直属商户ID |
| user_type | 补贴方类型 | String | 32 | Y | channel-渠道，merchant-总部商户，agent-代理，mertomer-商户；<font color="green">示例值：channel</font> |
| acct_id | 补贴方账户号 | String | 32 | Y | 营销补贴方账户号；<font color="green">示例值：F00598600</font> |
| amount | 补贴金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2f826ba1_18df_4b50_bdf0_eea610b55d52-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| device_type | 设备类型 | String | 2 | N | 1:手机，2:平板，3:手表，4:PC；<font color="green">示例值：1</font> |
| device_ip | 交易设备IP | String | 64 | N | 用于标识交易设备IP地址，绑卡设备所在的公网IP，可用于定位所属地区，<br/>不是wifi连接时的局域网IP。<br/><font color="green">示例值：10.10.0.1</font>（IPv4）；目前暂传IPv4格式。<br/>ABCD&#58;EF01&#58;2345&#58;6789&#58;ABCD&#58;EF01&#58;2345&#58;6789（IPv6）； |
| device_mac | 交易设备MAC | String | 64 | N | <font color="green">示例值：F0E1D2C3B4A5</font> |
| device_imei | 交易设备IMEI | String | 64 | N | 移动终端设备的唯一标识；<font color="green">示例值：460030912121001</font> |
| device_imsi | 交易设备IMSI | String | 64 | N | <font color="green">示例值：460030912121001</font> |
| device_icc_id | 交易设备ICCID | String | 64 | N | <font color="green">示例值：898600680113F0123014</font> |
| device_wifi_mac | 交易设备WIFIMAC | String | 64 | N | <font color="green">示例值：968778695A4B</font> |
| device_gps | 交易设备GPS | String | 64 | N | <font color="green">示例值：20.346790,-4.654321</font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "data": {
        "huifu_id": "66660000000001",
        "ord_amt": "100.00",
        "org_hf_seq_id": "002900TOP2B2601111111111103ac139cb800000",
        "org_req_date": "20260521",
        "req_date": "20260601",
        "req_seq_id": "2026060111111111102",
        "terminal_device_data":{
            "device_type":"1",
            "device_ip":"10.10.12.128"
        }
    },
    "product_id": "SPIN",
    "sign": "ieJEQJqWH2DCPpOiccE4dW+SxglxzVhrEXBW+JhTe5NQB/b0PaDzX6mzVdBUx3EHQ2g==",
    "sys_id": "66660000000001"
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](#业务返回码) |
| product_id | 产品号 | String | 32 | Y | 交易时传入，原样返回；<font color="green">示例值：YYZY</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A221019132207P068ac1362af00000</font> |
| org_req_date | 原交易请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | <font color="green">示例值：rQ202112131149875651</font> |
| trans_date | 退款交易发生日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| trans_time | 退款交易发生时间 | String | 6 | N | 格式：HHMMSS，<font color="green">示例值：091010 </font> 代表9点10分10秒 |
| trans_finish_time | 退款完成时间 | String | 14 | N | 格式yyyyMMddHHmmss；<font color="green">示例值：20091225091010</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；<font color="green">示例值：S</font> |
| ord_amt | 退款金额（元） | String | 14 | Y | 需保留小数点后两位；<font color="green">示例值：1.00</font>，最低传入0.01 |
| actual_ref_amt | 实际退款金额（元） | String | 14 | N | 需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| remark | 备注 | String | 84 | N | 原样返回；<font color="green">示例值：备注</font> |
| bank_message | 通道返回描述 | String | 256 | N | <font color="green">示例值：SUCCESS</font> |
| fund_freeze_stat | 资金冻结状态 | String | 16 | N | FREEZE：冻结；UNFREEZE：解冻；<font color="green">示例值：UNFREEZE</font><br>退款发生时，对应原交易的资金冻结状态。 |
| pay_channel | 交易通道 | String | 1 | N | 枚举值：A-支付宝、T-微信、U-银联二维码、D-数字货币 |
| fee_amount | 退款返还手续费 | String | 14 | N | 单位元，保留小数点后两位，<font color="green">示例值：1.00</font> |
| trade_type | 交易类型	 | String |  | N | TRANS_REFUND：交易退款；目前仅该一个枚举值；<br/><font color="green">示例值：TRANS_REFUND</font> |
| <span class="extend d2f8aee7_022a_4a96_8dbe_8f42dc7ae768">tx_metadata</span> | 扩展参数集合 | String |  | N | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |

<!-- extend:start -->
<!-- div:extend-table d2f8aee7_022a_4a96_8dbe_8f42dc7ae768-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 8dd58974_125a_43a9_b323_fc5cc73255f0">acct_split_bunch</span> | 分账信息 | String | 2048 | N | jsonObject字符串 |
| <span class="extend c9bef933_430b_4f91_8979_ed81663b93fd">combinedpay_data</span> | 补贴支付信息 | String |  | N | jsonArray字符串；参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8dd58974_125a_43a9_b323_fc5cc73255f0-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend adb4d78d_4586_43c7_95e6_cc665048e471">acct_infos</span> | 分账明细 | Array | 2048 | N | 分账明细 |
| <span class="extend be23e0ae_ca3b_4cc0_9f32_caa0bc55031c showCompleteParams">confirm_acct_infos</span> | 交易确认分账信息列表 | Array | 2048 | N | 交易确认分账明细 |
| fee_amount | 退款返还手续费 | String | 14 | N | 单位元，保留小数点后两位，<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table adb4d78d_4586_43c7_95e6_cc665048e471-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000108854952</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table be23e0ae_ca3b_4cc0_9f32_caa0bc55031c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| confirm_hf_seq_id  | 交易确认单号 | String | 128 | Y |  |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000108854952</font> |
| confirm_refund_status | 交易确认退款状态 | String | 1 | N | 交易确认退款状态P/S /F ,P:说明该笔交易确认退款为处理中，返回为空代表不走交易确认退款 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c9bef933_430b_4f91_8979_ed81663b93fd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴方汇付编号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font> |
| user_type | 补贴方类型 | String | 32 | Y | 补贴方类型：channel-渠道，branch-总部/分支机构，agent-代理；<font color="green">示例值：channel</font> |
| acct_id | 补贴方账户号 | String | 32 | Y | 营销补贴方账户号；<font color="green">示例值：F00598600</font> |
| amount | 补贴金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
  "data": {
    "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000103334211\"}],\"fee_amount\":\"0.00\"}",
    "bank_message": "",
    "fee_amount": "0.00",
    "fund_freeze_stat": "FREEZE",
    "huifu_id": "6666000103334211",
    "product_id": "MYPAY",
    "ord_amt": "0.01",
    "org_hf_seq_id": "0029000topA250901150535P324c0a8408000000",
    "org_req_date": "20250901",
    "org_req_seq_id": "20250901test900001tt11zzaazz11",
    "pay_channel": "T",
    "remark": "退款",
    "resp_code": "00000100",
    "resp_desc": "交易处理中",
    "trade_type": "TRANS_REFUND",
    "trans_date": "20250901",
    "trans_stat": "P",
    "trans_time": "153948"
  }
}

```


#### 异步返回参数

异步返回报文有两种不同的类型：间联模式与直联模式。如果商户业务开通时做了微信直连配置（wx_zl_conf），则属于直联模式。否则就是间联模式。 

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](#业务返回码) |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| req_date | 请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：rQ202112131117394413651</font> |
| hf_seq_id | 全局流水号 | String | 128 | N | <font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_req_date | 原交易请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | <font color="green">示例值：</font> |
| org_ord_amt | 原交易订单金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| org_fee_amt | 原交易手续费 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| trans_date | 退款交易发生日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| trans_time | 退款交易发生时间 | String | 6 | N | 格式：HHMMSS，<font color="green">示例值：091010</font>9点10分10秒 |
| trans_finish_time | 退款完成时间 | String | 14 | N | 格式yyyyMMddHHmmss；<font color="green">示例值：20091225091010</font> |
| trans_type | 交易类型 | String | 40 | Y | TRANS_REFUND：交易退款；目前仅该一个枚举值；<br/><font color="green">示例值：TRANS_REFUND</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；<font color="green">示例值：</font> |
| ord_amt | 退款金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| actual_ref_amt | 实际退款金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| total_ref_amt | 原交易累计退款金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| total_ref_fee_amt | 原交易累计退款手续费金额 | String | 14 | Y | 单位元，<font color="green">示例值：1.00</font>；注意：退还手续费规则参见[说明文档](https://paas.huifu.com/open/doc/api/#/api_tksxfsm) |
| ref_cut | 累计退款次数 | String | 14 | Y | <font color="green">示例值：1</font> |
| <span class="extend bfda948a_cf4f_4961_a5a5_00567b44b06a">acct_split_bunch</span> | 分账信息 | Object | 4000 | Y | 分账信息 |
| party_order_id | 微信支付宝的商户单号 | String | 64 | N | <font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| <span class="extend c0524304_d1bb_4bd6_a5ad_1d990879f351">wx_response</span> | 微信返回的响应报文 | Object | 6000 | N |  |
| <span class="extend 3978a498_6f63_4923_a919_b37013ebd31d">dc_response</span> | 数字人民币响应报文 | Object | 2048 | N | jsonObject格式 |
| <span class="extend 015ed20a_d764_485c_af99_28c1940b4ab6">combinedpay_data</span> | 补贴支付信息 | Array |  | N | 参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| <span class="extend b364ab81_3870_4efe_a855_cab3de743cbf">combinedpay_data_fee_info</span> | 补贴支付手续费承担方信息 | String |  | N | jsonObject字符串 |
| remark | 备注 | String | 1500 | N | 原样返回；<font color="green">示例值：备注</font> |
| <span class="showCompleteParams">bank_code</span> | 通道返回码 | String | 64 | N | <font color="green">示例值：01020000</font> |
| bank_message | 通道返回描述 | String | 256 | N | <font color="green">示例值：SUCCESS</font> |
| <span class="extend 59c592f7_f82c_435c_b757_9aa7d7e8f555">unionpay_response</span> | 银联返回的响应报文 | Object | 6000 | N | Json格式 |
| fund_freeze_stat | 资金冻结状态 | String | 16 | N | FREEZE：冻结；UNFREEZE：解冻；<font color="green">示例值：UNFREEZE</font><br>退款发生时，对应原交易的资金冻结状态。 |
| <span class="extend d1348e76_03db_465e_8b9d_58f306e37864">trans_fee_ref_allowance_info</span> | 手续费补贴返还信息 | Object |  | N | 手续费补贴返还信息对象，jsonObject字符串 |
| pay_channel | 交易通道 | String | 1 | N | 枚举值：A-支付宝、T-微信、U-银联二维码、D-数字货币 |
| <span class="showCompleteParams">is_confirm_refund_flag</span> | 是否已延迟分账 | String |  | N | 是否已延迟分账 Y: 是， N-否 默认N |
| is_refund_fee_flag | 是否退还手续费 | String | 1 | N | 是否退还手续费，支付宝直连场景下返回,Y或者空: 退费，N-不退费 |

<!-- extend:start -->
<!-- div:extend-table bfda948a_cf4f_4961_a5a5_00567b44b06a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 58cb7ca8_bbce_4365_8689_c09305923625">acct_infos</span> | 分账明细 | Array | 2048 | N | 分账明细 |
| <span class="extend 1d026b2d_caa7_47c0_b557_6079a3f7752a showCompleteParams">confirm_acct_infos</span> | 交易确认分账信息列表 | Array | 2048 | N | 交易确认分账明细 |
| fee_amt | 退款返还手续费 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 58cb7ca8_bbce_4365_8689_c09305923625-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000108854952</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 1d026b2d_caa7_47c0_b557_6079a3f7752a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| confirm_hf_seq_id  | 交易确认单号 | String | 128 | Y |  |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000108854952</font> |
| confirm_refund_status | 交易确认退款状态 | String | 1 | N | 交易确认退款状态P/S /F ,P:说明该笔交易确认退款为处理中，返回为空代表不走交易确认退款 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table c0524304_d1bb_4bd6_a5ad_1d990879f351-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_appid | 子商户公众账号ID | String | 32 | N | <font color="green">示例值：wx8888888888888888</font> |
| sub_mch_id | 子商户号 | String | 32 | N | <font color="green">示例值：1800008315</font> |
| org_out_trans_id | 微信订单号 | String | 32 | N | <font color="green">示例值：20201030189770</font> |
| out_trans_id | 微信退款单号 | String | 32 | N | <font color="green">示例值：6545342375</font> |
| cash_fee | 现金支付金额 | String | 12 | N | 现金支付金额订单现金支付金额，单位:元；<font color="green">示例值：1.00</font> |
| cash_refund_fee | 现金退款金额 | String | 12 | N | 单位:元；<font color="green">示例值：1.00</font> |
| coupon_refund_fee | 代金券退款总金额 | String | 12 | N | 单位:元；<font color="green">示例值：1.00</font> |
| coupon_refund_count | 退款代金券使用数量 | Integer | 12 | N | <font color="green">示例值：1</font> |
| <span class="extend 2ffb4fd6_2250_4bf4_9fcd_e75958154619">refund_coupon_info</span> | 退款代金券信息 | Array | 1024 | N | 退款代金券信息 |
| <span class="extend bec62fe9_9f2d_4a18_93b2_91d8f477822e">promotion_detail</span> | 优惠详情 | Array |  | N | 优惠详情 |
| user_received_account | 退款入账账户 | String | 64 | N | 取当前退款单的退款入账方</br>1）退回银行卡：{银行名称}{卡类型}{卡尾号}  (示例：招商银行信用卡0403）</br>2）退回支付用户零钱：支付用户零钱</br>3）退还商户：商户基本账户商户结算银行账户</br>4）退回支付用户零钱通：支付用户零钱通 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2ffb4fd6_2250_4bf4_9fcd_e75958154619-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| coupon_type | 代金券类型 | String | 8 | N | CASH--充值代金券<br/>NO_CASH---非充值代金券<br/>订单使用代金券时有返回，<font color="green">示例值：NO_CASH</font> |
| coupon_refund_id | 退款代金券ID | String | 20 | N | <font color="green">示例值：4058934532</font> |
| coupon_refund_fee | 单个退款代金券支付金额 | String | 11 | N | 单位:元，<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bec62fe9_9f2d_4a18_93b2_91d8f477822e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| promotion_id | 券ID | String | 32 | Y | 券或者立减优惠id；<font color="green">示例值：4058934532</font> |
| scope | 优惠范围 | String | 32 | N | GLOBAL- 全场代金券<br/>SINGLE- 单品优惠<br/><font color="green">示例值：SINGLE</font> |
| type | 优惠类型 | String | 32 | N | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）<br/>DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）<br/><font color="green">示例值：DISCOUNT</font> |
| refund_amount | 代金券退款金额 | String | 32 | N | 单位:元，<font color="green">示例值：1.00</font> |
| amount | 代金券面额 | String | 32 | N | 用户享受优惠的金额，单位:元，<font color="green">示例值：1.00</font> |
| <span class="extend 442712ae_9730_49d0_9977_2006719e40f8">goods_detail</span> | 商品列表 | Array |  | N | 仅使用单品优惠退款时返回，商品列表 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 442712ae_9730_49d0_9977_2006719e40f8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| goods_id | 商品编码 | String | 32 | Y | 商户系统的商品编码。由半角的大小写字母、数字、中划线、下划线中的一种或几种组成，<font color="green">示例值：6934572310301</font> |
| wxpay_goods_id | 微信支付商品编码 | String | 32 | N | 微信支付定义的统一商品编号（没有可不传）；<font color="green">示例值：</font> |
| goods_name | 商品名称 | String | 14 | N | <font color="green">示例值：华为手机</font> |
| refund_amt | 商品退款金额 | String | 11 | Y | <font color="green">示例值：1.00</font> |
| refund_quantity | 商品退款数量 | Integer | 11 | Y | <font color="green">示例值：1</font>。 |
| price | 商品单价 | String | 11 | Y | 单位为：元。<font color="green">示例值：50.00</font>。如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，则活动商品的单价应为原单价-50元； |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3978a498_6f63_4923_a919_b37013ebd31d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| merchant_id | 商户号 | String | 35 | N | <font color="green">示例值：S5088295305</font> |
| sub_merchant_id | 子商户号 | String | 35 | N | <font color="green">示例值：58000001</font> |
| openid | 用户标识 | String | 64 | N | <font color="green">示例值：oGhiSxIAPtEnPfe9Xo000000B</font> |
| sub_openid | 用户子标识 | String | 64 | N | <font color="green">示例值：oWNHX5RNaCUmZR</font> |
| custom_bank_code | 客户所属运营机构代码 | String | 14 | N | <font color="green">示例值：</font> |
| custom_bank_name | 客户所属运营机构名称 | String | 70 | N | <font color="green">示例值：</font> |
| coupon_refund_count | 退款代金券使用数量 | String | 3 | N | <font color="green">示例值：2</font> |
| <span class="extend cf5f27f2_6e15_4bdb_b92c_f15d55270490">coupon_refund_list</span> | 退款代金券集合 | Array | 2048 | N |  |
| refund_recv_wallet_id | 退款入账钱包ID | String | 22 | N | <font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table cf5f27f2_6e15_4bdb_b92c_f15d55270490-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| id | 退款代金券ID | String | 40 | N | <font color="green">示例值：</font> |
| type | 退款代金券类型 | String | 8 | N | <font color="green">示例值：</font> |
| amount | 单个退款代金券支付金额 | String | 14 | N | 单位：元；<font color="green">示例值：</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 015ed20a_d764_485c_af99_28c1940b4ab6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴方汇付编号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font> |
| user_type | 补贴方类型 | String | 32 | Y | 补贴方类型：channel-渠道，branch-总部/分支机构，agent-代理；<font color="green">示例值：channel</font> |
| acct_id | 补贴方账户号 | String | 32 | Y | 营销补贴方账户号；<font color="green">示例值：F00598600</font> |
| amount | 补贴金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table b364ab81_3870_4efe_a855_cab3de743cbf-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 补贴支付手续费承担方汇付编号 | String | 32 | N | <font color="green">示例值：6666000123120001</font> |
| acct_id | 补贴支付手续费承担方账户号 | String | 32 | N | 补贴支付手续费承担方账户号；<font color="green">示例值：F00598610</font> |
| combinedpay_fee_amt | 补贴支付手续费金额 | String | 14 | N | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； <font color="green">示例值：1.01</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 59c592f7_f82c_435c_b757_9aa7d7e8f555-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 12d466cd_8c46_4f9d_9a63_7fd37c84a8cd">coupon_info</span> | 银联优惠信息 | String |  | N | 银联使用优惠活动时出现，jsonArray格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 12d466cd_8c46_4f9d_9a63_7fd37c84a8cd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font> |
| type | 项目类型 | String | 4 | Y | DD01：随机立减<br>CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券<br>CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券<br><font color="green">示例值：DD01</font>  |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；单位元；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table d1348e76_03db_465e_8b9d_58f306e37864-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| receivable_ref_fee_amt | 退款返还总手续费 | String | 16 | Y | 退款返还总手续费， <font color="green">示例值：5.00</font> |
| actual_ref_fee_amt | 退款返还商户手续费 | String | 16 | Y | 退款返还商户手续费金额，<font color="green">示例值：1.00</font> |
| allowance_ref_fee_amt | 退款返还补贴手续费 | String | 16 | Y | 退款返还补贴手续费金额，<font color="green">示例值：4.00</font> |
<!-- extend:end -->


#### 业务返回码

| 返回码   |返回描述                                   |
| :------- | :----------------------------------------- |
| 00000000 |交易成功                                   |
| 00000100 |交易处理中                                 |
| 10000000 |入参数据不符合接口要求                     |
| 20000001 |并发冲突,请稍后重试                        |
| 21000000 |**原交易请求流水号,原交易微信支付宝的商户单号,原交易全局流水号不能同时为空**                   |
| 21000000 |数字货币交易退款原因必填                   |
| 22000000 |产品号不存在                               |
| 22000000 |产品号状态异常                             |
| 22000002 |商户信息不存在                             |
| 22000002 |商户状态异常                               |
| 22000003 |账户信息不存在                             |
| 22000004 |暂未开通退款权限                           |
| 22000004 |暂未开通分账退款权限                       |
| 22000005 |结算配置信息不存在                         |
| 23000000 |原交易未入账,不能发起退款                  |
| 23000001 |**原交易不存在**                               |
| 23000002 |退款手续费承担方和原交易手续费承担方不一致 |
| 23000003 |**申请退款金额大于可退余额**                   |
| 23000003 |退款金额大于待确认金额                     |
| 23000003 |手续费退款金额大于可退手续费金额           |
| 23000003 |申请退款金额大于可退款余额                 |
| 23000003 |退款分账金额总和必须等于退款订单金额       |
| 23000003 |账户余额不足                               |
| 23000004 |不支持预授权撤销类交易;                    |
| 23000004 |不支持刷卡撤销类交易                       |
| 23000004 |优惠交易不支持部分退款                     |
| 23000004 |该交易为部分退款，需传入分账串             |
| 23000004 |优惠退款不支持传入分账串                   |
| 23000004 |分账串信息与原交易不匹配                   |
| 90000000 |业务执行失败，**可用余额不足**                               |
| 90000000 |交易存在风险                               |
| 98888888 |系统错误                                   |
| 99999999 |系统异常,请稍后重试                        |

