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
## 交易确认

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/payment/delaytrans/confirm

*最近更新时间：2026.09.21*
### 应用场景
支持商户调用本接口，对已有的延时交易订单发起交易确认，以实现交易资金的分配。

**适用对象**    
已开通延时交易功能的商户。
  
### **接口说明**
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
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：2021091708126665001</font> |
| huifu_id | 商户号 | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000109812123</font> |
| org_req_date | 原交易请求日期 | String | 8 | N | 格式为yyyyMMdd，<font color="green">示例值：20091225</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | org_hf_seq_id、（org_req_date、org_req_seq_id）、（org_req_date、org_mer_ord_id）三选一<br/>**余额支付仅支持使用org_req_date+org_req_seq_id进行确认**；<br/><font color="green">示例值：2021091708126665001</font> |
| org_mer_ord_id | 原交易商户订单号 | String | 128 | N | org_hf_seq_id、（org_req_date、org_req_seq_id）、（org_req_date、org_mer_ord_id）三选一<br/><font color="green">示例值：03232109190255105603561</font> |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | org_hf_seq_id、（org_req_date、org_req_seq_id）、（org_req_date、org_mer_ord_id）三选一<br/><font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| <span class="extend 52f71d5e_e993_4c21_9d61_98acd83b0db1">acct_split_bunch</span> | 分账对象 | String | 4000 | N | jsonObject字符串；**为空时按交易时的分账串处理分账资金**； |
| <span class="extend 40338060_7d62_4fe3_86b4_6dcce488e193">risk_check_data</span> | 安全信息 | String | 4000 | N | 安全信息，jsonObject字符串 |
| pay_type | 交易类型 | String | 16 | C | **原交易为快捷支付必填：QUICK_PAY**；<br/>**原交易为余额支付必填：ACCT_PAYMENT**；<br/>原交易为全域资金必填：REMITTANCE_PAY；<br/><font color="green">示例值：ACCT_PAYMENT</font> |
| remark | 备注 | String | 256 | N | 原样返回；<font color="green">示例值：备注</font> |

<!-- extend:start -->
<!-- div:extend-table 52f71d5e_e993_4c21_9d61_98acd83b0db1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| percentage_flag | 百分比分账标志 | String | 1 | N | Y:使用百分比分账；<font color="green">示例值：Y</font> |
| total_div_amt | 分账总金额（元） | String | 14 | C | 本次交易确认总额。需保留小数点后两位<br/>percentage_flag=Y时必填。该金额与分账百分比用来计算分账金额。<font color="green">示例值：10.00</font>； |
| <span class="extend 0e8daec3_b483_4670_aaf5_10b5dbf30d89">acct_infos</span> | 分账明细 | Array | 2048 | N | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0e8daec3_b483_4670_aaf5_10b5dbf30d89-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| percentage_div | 分账百分比% | String | 6 | N | <font color="green">示例值：23.50</font>，表示23.50%。仅在percentage_flag=Y时起作用<br> acct_infos中全部分账百分比只和必须为100.00%。 |
| div_amt | 分账金额(元) | String | 14 | C | 单位元，需保留小数点后两位，最低传入0.01 ，<font color="green">示例值：1.00</font> ，percentage_flag非Y时必填；<br/>percentage_flag=Y时div_amt不填，div_amt=total_div_amt*percentage_div |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000109812123</font> |
| acct_id | 分账接收方账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户；<font color="green">示例值：F00598600</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 40338060_7d62_4fe3_86b4_6dcce488e193-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| ip_addr | ip地址 | String | 32 | N | IP地址、经纬度、基站地址最少要送其中一项；<font color="green">示例值：172.28.52.52</font> |
| base_station | 基站地址 | String | 32 | N | IP地址、经纬度、基站地址最少要送其中一项；<br/>【mcc】+【mnc】+【location_cd】+【lbs_num】<br/>- mcc:移动国家代码，460代表中国；3位长<br/>- mnc：移动网络号码；2位长；<br/>- location_cd：位置区域码，16进制，5位长<br/>- lbs_num：基站编号，16进制，5位长<br/>- 注意若位数不足用空格补足；<br/><font color="green">示例值：460001039217563</font>，其中460（mcc)， 00(mnc)，10392(location_cd)， 17563(lbs_num) |
| latitude | 纬度 | String | 32 | N | 格式：+表示北纬，-表示南纬。纬度整数位不超过2位，小数位不超过6位。<font color="green">示例值：+37.12</font>；<br/>IP地址、经纬度、基站地址最少要送其中一项 |
| longitude | 经度 | String | 32 | N | 格式：+表示东经，-表示西经；经度整数位不超过3位，小数位不超过5位；<font color="green">示例值：-121.213</font>；<br/>IP地址、经纬度、基站地址最少要送其中一项 |
| sub_product | 产品子类 | String | 20 | N | 推广大使、一卡通（智汇管家2.0必填）；<font color="green">示例值：-121.213</font> |
| transfer_type | 转账原因 | String | 2 | N | 01：卡券推广类,02：卡券核销类,03：消费,04：工资代发,05：分润；<font color="green">示例值：03</font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "data": {
        "org_req_date": "20220512",
        "org_req_seq_id": "20220512195832E06521",
        "req_seq_id": "20240513105825239x0lp7ldbus4sji",
        "req_date": "20240513",
        "org_hf_seq_id": "",
        "risk_check_data": "{\"base_station\":\"3\",\"latitude\":\"2\",\"longitude\":\"1\"}",
        "remark": "remark123",
        "huifu_id": "6666000109133323",
        "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000109133323\",\"div_amt\":\"0.01\"}]}"
    },
    "product_id": "YYZY",
    "sign": "J19V4V3iE7Sar9gkrdhWwURqlKCgLTJx2rjQ2k52Uf+FTrfVRPbw5LjxXOPohm/OwNVKEsKqiCIehVuf++NRHGqjRM6lQa7/aXQbK2w0Q47CYIK+O8dWdJGPuk35yT3BmzO37SZLokF1gGBET0MTPETW0UmRhL3+qrEZMc6wDmqtZaluMeaHdvQyqs00JYxVEkt3f1Gw+Tb6d6SEkDSHsvn4OS71IzKzMxAzZDowRiG5wjQWIwWrzgeRg2ZhxFFXOu2zLoYSjDNMxe5t+jBrAhjxGm9Co+76yUv9ys1OZFpStVEs/8y94nkqVIHyRuqLh/0+x+SOq0pB8v5tECO/eQ=="
}
```
### 返回参数


#### 同步返参

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码)  ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：交易成功</font> |
| huifu_id | 商户号 | String | 32 | Y | 示例值:6666000109812123 |
| req_date | 请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20221013</font> |
| req_seq_id | 业务请求流水号 | String | 128 | Y | <font color="green">示例值：2022082408452985319884</font> |
| trans_stat | 交易状态 | String | 1 | Y | P:处理中；S：成功；F：失败；<font color="green">示例值：S</font> |
| hf_seq_id | 全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| unconfirm_amt | 待确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| confirmed_amt | 已确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| acct_resp_code | 账务返回码 | String | 16 | N | <font color="green">示例值：000</font> |
| acct_resp_desc | 账务返回描述 | String | 256 | N | <font color="green">示例值：成功</font> |
| org_mer_ord_id | 原交易商户订单号 | String | 128 | N | <font color="green">示例值：03232109190255105603561</font> |
| org_req_date | 支付交易业务请求时间 | String | 8 | Y | <font color="green">示例值：20221012</font> |
| org_req_seq_id | 支付交易业务请求流水号 | String | 128 | Y | <font color="green">示例值：2022082408452985319883</font> |
| org_hf_seq_id | 支付交易汇付全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00001</font> |
| <span class="extend 3679934b_916b_4538_8b9f_b7fcdaef0e53">acct_split_bunch</span> | 分账对象 | String |  | N | jsonObject字符串 |
| remark | 备注 | String | 256 | N | 请求参数里传入，返回参数里原样返回；<font color="green">示例值：备注</font> |

<!-- extend:start -->
<!-- div:extend-table 3679934b_916b_4538_8b9f_b7fcdaef0e53-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 69a387f7_fec2_43af_b859_fd5d839bb4d9">acct_infos</span> | 分账明细 | Array |  | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 69a387f7_fec2_43af_b859_fd5d839bb4d9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额(元) | String | 14 | Y | 单位元，示例值:1.00 |
| huifu_id | 分账接收方ID | String | 32 | Y | 示例值:6666000109812123 |
| acct_id | 分账接收方账户号 | String | 32 | Y | 示例值:F00598600 |
| split_fee_amt | 分账手续费金额(元) | String | 14 | N | 示例值:0.10 |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | N | 示例值:6666000123120001 |
| split_fee_acct_id | 分账手续费承担方账号 | String | 32 | N | 示例值:F00598600 |
| unconfirm_amt | 待确认金额(元) | String | 14 | N | 示例值:0.10 |
<!-- extend:end -->


#### 异步返参

仅当灵活用工场景且灵活用工平台为汇优财时，传入了异步通知地址时才有异步通知。   

**公共参数：**

| 参数        | 中文名    | 定义     | 长度  | 必填 | 说明              |
| :------- | :------- | :----- | :--- | :--- | :---------------------------------------------------- |
| resp_code | 业务返回码  | string | 8   | Y  | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%ba%bf%e4%b8%8a%e4%ba%a4%e6%98%93%e8%bf%94%e5%9b%9e%e7%a0%81)),<font color="green">示例值：00000000</font>      |
| resp_desc | 业务返回描述 | string | 512 | Y  | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%ba%bf%e4%b8%8a%e4%ba%a4%e6%98%93%e8%bf%94%e5%9b%9e%e7%a0%81))，<font color="green">示例值：交易成功[000]</font>          |
| resp_data | 业务数据   | string |     | Y  | 业务数据，见resp_data |

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 业务请求流水号 | String | 128 | Y | 业务请求流水号 |
| req_date | 业务请求时间yyyyMMdd | String | 8 | Y | 业务请求时间yyyyMMdd |
| huifu_id | 商户号 | String | 32 | Y | 商户号 |
| hf_seq_id | 汇付全局流水号 | String | 128 | Y | 汇付全局流水号 |
| trans_stat | 交易状态 | String | 1 | Y | S：成功，F：失败。 |
| <span class="extend f5e8b635_d008_464c_bfd6_58319713cab9">acct_split_bunch</span> | 分账对象 | Object |  | N | jsonObject字符串 |
| remark | 备注 | String | 256 | N | 请求参数里传入，返回参数里原样返回；<font color="green">示例值：备注</font> |

<!-- extend:start -->
<!-- div:extend-table f5e8b635_d008_464c_bfd6_58319713cab9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 5bda80e6_ae00_4620_9fce_16a1602896a5">acct_infos</span> | 分账明细 | Array |  | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5bda80e6_ae00_4620_9fce_16a1602896a5-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额(元) | String | 14 | Y | 单位元，示例值:1.00 |
| huifu_id | 分账接收方ID | String | 32 | Y | 示例值:6666000109812123 |
| acct_id | 分账接收方账户号 | String | 32 | Y | 示例值:F00598600 |
| split_fee_amt | 分账手续费金额(元) | String | 14 | N | 示例值:0.10 |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | N | 示例值:6666000123120001 |
| split_fee_acct_id | 分账手续费承担方账号 | String | 32 | N | 示例值:F00598600 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "trans_stat": "S",
        "req_date": "20221108",
        "req_seq_id": "20221108349713659620211667900804",
        "huifu_id": "6666000103423237",
        "hf_seq_id": "0035000topA221108174643P967c0a8320000000",
        "acct_resp_code": "000",
        "acct_resp_desc": "成功",
        "unconfirm_amt": "99.69",
        "confirmed_amt": "0.31",
        "org_req_date": "20221108",
        "org_req_seq_id": "2022072724398620211667900766",
        "org_hf_seq_id": "0047default221108174606P607c0a831e100000"        
    },
    "sign": "dqhk+nPakFSn+2HMj+zTL7vff20LFBEwcJMNLoumGKIGsTDft2doQL/GkIb7+TeAuBF/7lGHazvtoE4aKS1WfnlQf2PPVH3ObCEHHoUim5f+oMcZf/gJbzg+Zos9KA/88U6psQK80SP3MwLCLwWqlHLreB77jp9DBZ9o8GZ3nNy3naFhvcRmDo2gGiWYjFjbAlVzVkIjcBmPW7zaVJN/zICT2xfHbFziXUoslOAQIwboRgMCiS2u2ff7R3dRXPUJSUx1g6fiFMlS0DwN29V0vYiayIYys3zZWlFPuVcN+Hwy9/B1vVtuOrTA3DXxgOmMwexvnHzTn0z2QHr3f7fTuA=="
}
```


#### 业务返回码

查看全部 [公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)

| 返回码   | 返回描述                                                     | 处理                                              |
| :------- | :----------------------------------------------------------- | :--------------------------------------- |
| 00000000 | 交易成功                                                     | 业务执行成功                                      |
| 10000000 | 请求内容体不能为空                                           | 请求体内容不可为空                                |
| 10000000 | %s不能为空（%s代指具体报错参数名）                           | 请检查格式                                        |
| 10000000 | %s长度固定%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度） | 检查参数是否有误                                  |
| 10000000 | %s最大长度为%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度） | 检查参数是否有误                                  |
| 10000000 | %s的传入枚举[%d]不存在（%s代指具体报错参数名、%d代指具体报错参数的值） | 检查参数是否有误                                  |
| 10000000 | %s不符合%d格式（%s代指具体报错参数名、%d代指具体报错参数值的格式） | 检查参数是否有误                                  |
| 10000000 | 原交易请求流水号、原交易请求日期组合，原交易商户订单号、原交易请求日期组合与原交易汇付全局流水号不可同时为空| 检查参数是否有误 |
| 20000000 | 重复交易                                                     | 为重复交易，请发起新交易                          |
| 20000001 | 操作过于频繁                                                 | 请稍后重试                                        |
| 21000000 | 原交易请求流水号,原交易请求日期组合与原交易汇付全局流水号二选一必填 | 检查参数是否有误                                  |
| 22000000 | 产品号不存在                                                 | 请检查产品号是否存在                              |
| 22000000 | 产品状态异常                                                 | 请检查产品状态                                    |
| 22000002 | 商户信息不存在                                               | 检查商户信息是否存在                              |
| 22000002 | 商户状态异常                                                 | 检查商户状态                                      |
| 22000003 | 账户信息不存在或者状态异常                                   | 检查账户信息是否存在或者是否有异常                |
| 22000005 | 其他商户分账比例过高                                         | 请调整分账参数                                    |
| 23000001 | **原交易不存在**                                                 | 请确认原交易是否存在                              |
| 23000003 | **确认金额大于可确认金额**   | 请减少确认金额                                    |
| 23000003 | **已无未确认金额**   |  原交易金额已全部确认                                    |
| 23000004 | 需要传入分账串                                               | 请传入分账串                                      |
| 98888888 | 系统错误                                                     | 一般为内部系统错误，请联系对技术运营对接人员处理。|
| 99999999 | 系统异常，请稍后重试                                         | 更新失败，请重试                                  |

