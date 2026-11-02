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
## 统一收银台交易退款

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/hosting/payment/htRefund

*最近更新时间：2026.10.13*
### 应用场景
通过统一收银台预下单接口发起的交易可以通过本接口退款。

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
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220925</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944175651</font> |
| huifu_id | 商户号 | String | 32 | Y | 开户后自动生成；<font color="green">示例值：6666000123123123</font> |
| ord_amt | 申请退款金额 | String | 14 | Y | 单位元，需保留小数点后两位；<font color="green">示例值：1.00</font>，最低传入0.01<br>注意：如果是原交易是延时交易，退款金额必须小于等于待确认金额 |
| org_req_date | 原交易请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20220925</font> |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；<br>拆单支付场景下，org_hf_seq_id，org_party_order_id二选一；<br/><font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_party_order_id | 原交易微信支付宝的商户单号 | String | 64 | N | 扫码交易退款字段；org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；<br>拆单支付场景下，org_hf_seq_id，org_party_order_id二选一；<br><font color="green">示例值：03232109190255105603561</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；<br><font color="green">示例值：202110210012100005</font> |
| <span class="extend 49056c85_ad90_4b4f_b10e_9184a2a9ef46">acct_split_bunch</span> | 分账对象 | String | 2048 | N | 分账信息，jsonObject字符串 |
| remark | 备注 | String | 84 | N | 原样返回；<font color="green">示例值：备注</font> |
| loan_flag | 是否垫资退款 | String | 2 | N | Y 是垫资出款， N 是普通出款，为空默认N；<font color="green">示例值： N</font><br>注意：延时交易退款在【交易确认退款】接口中设置loan_flag为垫资，<br/>本接口不可再次设置垫资。 |
| loan_undertaker | 垫资承担者 | String | 32 | N | 垫资方的huifu_id；<font color="green">示例值：6666000123123123</font><br/>为空则各自承担。不为空走第三方垫资，目前支持商户垫资； |
| loan_acct_type | 垫资账户类型 | String | 2 | N | 01:基本户, 05: 充值户, 默认充值户；<font color="green">示例值：01</font> |
| <span class="extend 23e26cf0_945b_48fa_956a_9cf1d9de0bc2">risk_check_data</span> | 安全信息 | String | 2048 | C | 线上交易退款必填，参见线上退款接口；jsonObject字符串 |
| <span class="extend 2a00d4ed_bc62_4d72_a543_f7981bbb91a4">terminal_device_data</span> | 设备信息 | String | 2048 | C | 线上交易退款必填，参见线上退款接口；jsonObject字符串 |
| notify_url | 异步通知地址 | String | 512 | N | <font color="green">示例值： http://service.example.com/to/path</font> |
| <span class="extend 8715a51e_6c3f_4b4c_8220_f0c99a839c2e">bank_info_data</span> | 大额转账支付账户信息数据 | String | 1024 | C | jsonObject格式；银行大额转账支付交易退款申请时必填 |
| <span class="extend 5557f4f4_ccc0_4255_820e_ee2ef2fae63c">dy_data</span> | 抖音拓展参数集合 | String | 2048 | N | jsonObject字符串 |
| <span class="extend 71c30c76_c15b_427e_b5f1_38660e74cae2">sub_orders_request</span> | 子单退款信息列表 | String |  | N | jsonArray字符串，合单支付的订单该字段必填 |

<!-- extend:start -->
<!-- div:extend-table 49056c85_ad90_4b4f_b10e_9184a2a9ef46-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 8c84d690_642f_48ce_8b4c_5b44e6f1441c">acct_infos</span> | 分账明细 | Array | 2048 | N | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8c84d690_642f_48ce_8b4c_5b44e6f1441c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120001</font> |
| part_loan_amt | 垫资金额 | String | 12 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01；<br/>注：若由第三方全额垫资，则不传该字段 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 23e26cf0_945b_48fa_956a_9cf1d9de0bc2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| ip_addr | ip地址 | String | 32 | N | IP地址、经纬度、基站地址最少要送其中一项；<font color="green">示例值：172.28.52.52</font> |
| base_station | 基站地址 | String | 64 | N | 【mcc】+【mnc】+【location_cd】+【lbs_num】<br/>- mcc:移动国家代码，460代表中国；3位长<br/>- mnc：移动网络号码；2位长；<br/>- location_cd：位置区域码，16进制，5位长<br/>- lbs_num：基站编号，16进制，5位长<br/>- 注意若位数不足用空格补足；<br/><font color="green">示例值：460001039217563</font>，其中460（mcc)， 00(mnc)，10392(location_cd)， 17563(lbs_num) |
| latitude | 纬度 | String | 20 | N | 格式：+表示北纬，-表示南纬。纬度整数位不超过2位，小数位不超过6位。<font color="green">示例值：+37.12</font>；<br/>IP地址、经纬度、基站地址最少要送其中一项 |
| longitude | 经度 | String | 20 | N | 格式：+表示东经，-表示西经；经度整数位不超过3位，小数位不超过5位；<font color="green">示例值：-121.213</font>；<br/>IP地址、经纬度、基站地址最少要送其中一项 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2a00d4ed_bc62_4d72_a543_f7981bbb91a4-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| device_type | 设备类型 | String | 2 | N | 1:  手机，2:  平板，3:  手表，4:  PC；<font color="green">示例值：1</font> |
| device_ip | 交易设备IP | String | 64 | N | 绑卡设备所在的公网IP，可用于定位所属地区，不是wifi连接时的局域网IP。<br/>ABCD&#58;EF01&#58;2345&#58;6789&#58;ABCD&#58;EF01&#58;2345&#58;6789（IPv6）；<!--<br/>0123&#58;4567&#58;89AB&#58;CDEF&#58;0123&#58;4567&#58;10.10.0.10（IPv6）；--><br/>目前暂传IPv4格式。<font color="green">示例值：10.10.0.1</font>（IPv4）； |
| device_mac | 交易设备MAC | String | 64 | N | <font color="green">示例值：F0E1D2C3B4A5</font> |
| device_gps | 交易设备GPS | String | 64 | N | <font color="green">示例值：20.346790,-4.654321</font> |
| device_imei | 交易设备IMEI | String | 64 | N | 移动终端设备的唯一标识；<font color="green">示例值：460030912121001</font> |
| device_imsi | 交易设备IMSI | String | 64 | N | <font color="green">示例值：460030912121001</font> |
| device_icc_id | 交易设备ICCID | String | 64 | N | <font color="green">示例值：898600680113F0123014</font> |
| device_wifi_mac | 交易设备WIFIMAC | String | 64 | N | <font color="green">示例值：968778695A4B</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8715a51e_6c3f_4b4c_8220_f0c99a839c2e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| province | 省份 | String | 4 | C | 付款方为对公账户时必填，参见省市地区码；示例值：0013 |
| area | 地区 | String | 4 | C | 付款方为对公账户时必填，参见省市地区码；示例值：1301 |
| bank_code | 银行编号 | String | 8 | C | 付款方为对公账户时必填，参考：银行编码； 示例值：01040000 |
| correspondent_code | 联行号 | String | 30 | C | 付款方为对公账户时必填，参见：银行支行编码； 示例值：102290026507 |
| card_acct_type | 付款方账户类型 | String | 1 | N | 对公:E，对私:P；默认：P，示例值：P |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5557f4f4_ccc0_4255_820e_ee2ef2fae63c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| refund_desc | 退款原因 | String | 200 | N | 会在下发给用户的退款消息中体现退款原因 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 71c30c76_c15b_427e_b5f1_38660e74cae2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_req_date | 子单请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220925</font> |
| sub_req_seq_id | 子单请求流水号 | String | 128 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：rQ2021121311173944175651</font> |
| sub_huifu_id | 子单商户号 | String | 32 | Y | <font color="green">示例值：6666000123120001</font> |
| sub_ord_amt | 子单申请退款金额 | String | 14 | Y | 单位元，需保留小数点后两位；<font color="green">示例值：1.00</font>，最低传入0.01<br/>**注意：如果原交易是延时交易，退款金额必须小于等于待确认金额** |
| org_sub_req_date | 原子单交易请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20220925</font> |
| org_sub_hf_seq_id | 原子单交易全局流水号 | String | 128 | N | org_sub_hf_seq_id，org_sub_req_seq_id二选一；<br/><font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_sub_req_seq_id | 原子单交易请求流水号 | String | 128 | N | org_sub_hf_seq_id，org_sub_req_seq_id二选一；<br/><font color="green">示例值：202110210012100005</font> |
| <span class="extend e42dd76d_256b_4a45_95b4_3b74f719c75c">acct_split_bunch</span> | 分账对象 | String | 2048 | N | 分账信息，jsonObject字符串 |
| sub_remark | 子单备注 | String | 84 | N | 原样返回；<font color="green">示例值：子单备注</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table e42dd76d_256b_4a45_95b4_3b74f719c75c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 8fc59e80_664a_4493_b9a0_796467c8a91a">acct_infos</span> | 分账信息列表 | String | 2048 | N | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8fc59e80_664a_4493_b9a0_796467c8a91a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000108854952</font> |
<!-- extend:end -->


#### 请求示例

```json
{  
    "sys_id": "6666000123123123",
    "product_id":"MYPAY",  
    "data":{  
        "huifu_id":"6666000003100616",  
        "req_date":"20240229",  
        "req_seq_id":"52022070919803411999411514",  
        "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.12\",\"huifu_id\":\"6666000003100616\"}]}",
        "ord_amt":"0.01",  
        "org_hf_seq_id":"",  
        "org_party_order_id":"",  
        "org_req_seq_id":"202207099803123123199941",  
        "org_req_date":"20240229",  
        "risk_check_data": "{\"ip_addr\":\"127.0.0.1\"}",
        "terminal_device_data": "{\"device_type\":\"4\"}",
        "notify_url":"http://www.baidu.com"  
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
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81) ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；<font color="green">示例值：交易成功</font> |
| product_id | 产品号 | String | 32 | Y | 交易时传入，原样返回；<font color="green">示例值：YYZY</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| req_date | 请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 交易时传入，原样返回；<font color="green">示例值：rQ2021121311173944134649875651</font> |
| hf_seq_id | 全局流水号 | String | 128 | N | 扫码交易返回；<font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_req_date | 原交易请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | <font color="green">示例值：rQ202112131149875651</font> |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | 线上交易返回；<font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| trans_time | 退款交易发生时间 | String | 14 | N | 扫码交易返回；<font color="green">示例值：20091225091010</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；示例值：S；<font color="green">示例值：S</font> |
| ord_amt | 退款金额（元） | String | 14 | Y | 需保留小数点后两位；<font color="green">示例值：1.00</font>，最低传入0.01 |
| actual_ref_amt | 实际退款金额（元） | String | 14 | N | 扫码交易返回；<font color="green">示例值：100.00</font> |
| <span class="extend 3e822e2a_f469_4b9a_bba4_2244831c171f">acct_split_bunch</span> | 分账信息 | String | 2048 | N | 分账信息，jsonObject字符串 |
| <span class="extend bc748439_93c3_46b0_96de_a1bbeb0d9ce5">unionpay_response</span> | 银联返回的响应报文 | String | 6000 | N | JsonObject字符串格式；扫码交易返回，参见扫码交易退款接口 |
| <span class="extend ced9d9eb_d301_4a56_a305_70102ca95c78">dy_response</span> | 抖音返回的响应报文 | String | 6000 | N | jsonObject字符串 |
| remark | 备注 | String | 84 | N | 原样返回；<font color="green">示例值：备注</font> |
| bank_code | 通道返回码 | String | 64 | N | <font color="green">示例值：01020000</font> |
| bank_message | 通道返回描述 | String | 256 | N | <font color="green">示例值：SUCCESS</font> |
| fee_amt | 退款返还手续费 | String | 14 | N | 线上交易返回；<font color="green">示例值：1.00</font> |

<!-- extend:start -->
<!-- div:extend-table 3e822e2a_f469_4b9a_bba4_2244831c171f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 5b4c5f34_2604_4e03_8c25_c37646486872">acct_infos</span> | 分账明细 | Array | 2048 | N | 分账明细 |
| fee_amt | 退款返还手续费 | String | 14 | N | 单位元，保留小数点后两位，<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5b4c5f34_2604_4e03_8c25_c37646486872-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table bc748439_93c3_46b0_96de_a1bbeb0d9ce5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 7fdafc4a_f473_43f4_bc2f_0ff86c77fc4f">coupon_info</span> | 银联优惠信息 | String |  | N | 银联使用优惠活动时出现，jsonArray格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 7fdafc4a_f473_43f4_bc2f_0ff86c77fc4f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font> |
| type | 项目类型 | String | 4 | Y | DD01：随机立减， CP01：抵金券；<font color="green">示例值：DD01</font> |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；单位元；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ced9d9eb_d301_4a56_a305_70102ca95c78-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| org_out_trans_id | 抖音原交易订单号 | String | 32 | N | <font color="green">示例值：20201030189770</font> |
| out_trans_id | 抖音退款单号 | String | 32 | N | <font color="green">示例值：6545342375</font> |
| payer_refund | 用户退款金额 | String | 12 | N | 退款给用户的金额，不包含所有优惠券金额 ，单位:元；<font color="green">示例值：1.00</font> |
<!-- extend:end -->


#### 异步返回参数

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81) ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；<font color="green">示例值：交易成功</font> |
| huifu_id | 商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| mer_name | 商户名称 | String | 128 | Y | 线上交易返回；<font color="green">示例值：上海汇付支付服务公司</font> |
| req_date | 请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：rQ202112131117394413651</font> |
| hf_seq_id | 全局流水号 | String | 128 | N | <font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| org_req_date | 原交易请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | <font color="green">示例值：rQ202112131149875651</font> |
| org_ord_amt | 原交易订单金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| org_fee_amt | 原交易手续费 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| trans_date | 退款交易发生日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220925</font> |
| trans_time | 退款交易发生时间 | String | 6 | N | 格式：HHMMSS，<font color="green">示例值：091010</font>；9点10分10秒 |
| trans_finish_time | 退款完成时间 | String | 14 | N | 格式yyyyMMddHHmmss；<font color="green">示例值：20091225091010</font> |
| trans_type | 交易类型 | String | 40 | Y | TRANS_REFUND：交易退款；目前仅该一个枚举值；<br><font color="green">示例值：TRANS_REFUND</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；<font color="green">示例值：S</font> |
| ord_amt | 退款金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| actual_ref_amt | 实际退款金额 | String | 14 | N | 扫码交易返回；<font color="green">示例值：111.00</font> |
| total_ref_amt | 原交易累计退款金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| total_ref_fee_amt | 原交易累计退款手续费金额 | String | 14 | Y | 单位元，<font color="green">示例值：1.00</font>；注意：退还手续费规则参见[说明文档](https://paas.huifu.com/open/doc/api/#/api_tksxfsm) |
| ref_cut | 累计退款次数 | String | 14 | Y | <font color="green">示例值：1</font> |
| <span class="extend 32b491d1_97c5_445e_bbf0_e1490ae6da34">acct_split_bunch</span> | 分账信息 | String | 4000 | Y | 与同步返参的相同 |
| <span class="extend 2ae81694_b46b_48c5_b835_c8198bef83f9">split_fee_info</span> | 分账手续费信息 | String | 2048 | N | 线上交易返回 |
| party_order_id | 微信支付宝的商户单号 | String | 64 | N | <font color="green">示例值：03232109190255105603561</font>；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| fee_amt | 退款返还手续费 | String | 14 | N | 线上交易返回 |
| remark | 备注 | String | 84 | N | 原样返回；<font color="green">示例值：备注</font> |
| bank_code | 通道返回码 | String | 64 | N | <font color="green">示例值：01020000</font> |
| bank_message | 通道返回描述 | String | 256 | N | <font color="green">示例值：SUCCESS</font> |
| <span class="extend 854d65be_c59e_490a_b7e7_1c7b2c739143">unionpay_response</span> | 银联返回的响应报文 | String | 6000 | N | JsonObject格式； |
| <span class="extend ef14142f_024b_4876_96f9_dd4bf6f3df38">dy_response</span> | 抖音返回的响应报文 | String | 6000 | N | jsonObject字符串 |
| bank_id | 银行编号 | String | 32 | N | 线上交易返回；<font color="green">示例值：</font> |
| bank_name | 银行名称 | String | 128 | N | 线上交易返回；<font color="green">示例值：</font> |

<!-- extend:start -->
<!-- div:extend-table 32b491d1_97c5_445e_bbf0_e1490ae6da34-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 6510538c_f53d_4d16_a13c_53cbd7bf7d4e">acct_infos</span> | 分账明细 | Array | 2048 | N | 分账明细 |
| fee_amt | 退款返还手续费 | String | 14 | N | 单位元，保留小数点后两位，<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6510538c_f53d_4d16_a13c_53cbd7bf7d4e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120001</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 2ae81694_b46b_48c5_b835_c8198bef83f9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| split_fee_flag | 分账手续费扣款标志 | String | 1 | Y | 1:外扣 2:内扣；<font color="green">示例值：1</font> |
| total_split_fee_amt | 总分账手续费金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| <span class="extend 6a7f7fd3_9bee_47bf_961c_5101a0c11dd2">split_fee_details</span> | 分账手续费明细 | Array | 2048 | Y | 分账手续费明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 6a7f7fd3_9bee_47bf_961c_5101a0c11dd2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| split_fee_amt | 分账手续费金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000123120001</font> |
| split_fee_acct_id | 分账手续费承担方账号 | String | 16 | N | <font color="green">示例值：F00598600</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 854d65be_c59e_490a_b7e7_1c7b2c739143-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 84108b70_95eb_470a_821b_dce94561ca2f">coupon_info</span> | 银联优惠信息 | String |  | N | 银联使用优惠活动时出现，jsonArray格式 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 84108b70_95eb_470a_821b_dce94561ca2f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| addnInfo | 附加信息 | String | 100 | N | 内容自定义；<font color="green">示例值：附加信息</font> |
| spnsrId | 出资方 | String | 20 | Y | 00010000：银联出资<br/>付款方作为出资方：填写8位付款方机构代码<br/>商户作为出资方：填写15位商户代码<br/><font color="green">示例值：00010000</font> |
| type | 项目类型 | String | 4 | Y | DD01：随机立减， CP01：抵金券；<font color="green">示例值：DD01</font> |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全0；单位元；<font color="green">示例值：1.00</font> |
| id | 项目编号 | String | 40 | N | 用于票券编号等，格式自定义；<font color="green">示例值：938434221</font> |
| desc | 项目简称 | String | 40 | N | 优惠活动简称，可用于展示、打单等；<font color="green">示例值：中秋优惠促销</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table ef14142f_024b_4876_96f9_dd4bf6f3df38-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| org_out_trans_id | 抖音原交易订单号 | String | 32 | N | <font color="green">示例值：20201030189770</font> |
| out_trans_id | 抖音退款单号 | String | 32 | N | <font color="green">示例值：6545342375</font> |
| payer_refund | 用户退款金额 | String | 12 | N | 退款给用户的金额，不包含所有优惠券金额 ，单位:元；<font color="green">示例值：1.00</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{  
    "data":{  
        "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.12\",\"huifu_id\":\"6666000003100616\"}]}",
        "actual_ref_amt":"",  
        "bank_code":"00000000",  
        "bank_message":"成功",  
        "hf_seq_id":"0056default240305162924Pa41a9ac1984fd843",  
        "huifu_id":"6666000003100616",  
        "mer_name":"顺顺利利的简称tes",  
        "ord_amt":"0.01",  
        "org_hf_seq_id":"0056default240305161117P559c0a8209b00000",  
        "org_req_date":"20240229",  
        "org_req_seq_id":"202207099803123123199941",  
        "req_date":"20240229",  
        "req_seq_id":"52022070919803411999411514",  
        "trans_stat":"S",  
        "trans_time":"20240305162924"  
    }  
}
```
