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
## 余额支付

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/acctpayment/pay

*最近更新时间：2026.09.23*
### 应用场景
本接口用于商户使用预存金额进行交易。

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
| huifu_id | 发起方商户号 | String | 32 | N | 该字段已废弃，新接入商户不建议使用；<br/>历史商户已用此参数，后续余额支付、查询、退款、交易确认接口仍以参数值为准 |
| out_huifu_id | 出款方商户号 | String | 32 | Y | 出款方商户号，<font color="green">示例值：6666000109812124</font> |
| ord_amt | 支付金额 | String | 14 | Y | 单元：元。保留两位小数。<font color="green">示例值：1.23</font> |
| good_desc | 商品描述 | String | 256 | N | <font color="green">示例值：商品描述</font> |
| remark | 备注 | String | 256 | N | <font color="green">示例值：备注</font> |
| delay_acct_flag | 是否延迟分账 | String | 1 | N | Y 为延迟，N为不延迟，不传默认N；<font color="green">示例值：Y</font> |
| <span class="extend 024aa3d3_c4cb_4d76_9720_303f7da3852d">acct_split_bunch</span> | 分账对象 | String |  | Y | json格式；余额支付支持付款给多账户。<br/>如余额支付100元，支付给A账户60元，支付给B账户40元。 |
| <span class="extend 5065d14f_06e9_4d96_95ea_638c013b3f66">risk_check_data</span> | 安全信息 | String |  | Y | json格式；示例: {"subProduct":"","transferType":""} |
| out_acct_id | 出款方账户号 | String | 32 | N | 只支持基本户和现金户；<font color="green">示例值：F00598600</font> |
| fund_type | 资金类型 | String | 16 | C | 资金类型。支付渠道为中信E管家时，资金类型必填（[详见说明](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)） |
| acct_channel | 支付渠道 | String | 8 | N | 支付渠道。HUIFU=汇付账务(默认)；ZXE=中信E管家 |
| trans_fee_take_flag | 手续费承担方标识 | String | 4 | C | 余额支付手续费承担方标识；商户余额支付扣收规则为接口指定承担方时必填！枚举值：<br/>OUT：出款方；<br/>IN：分账接受方。<br/><font color="green">示例值：IN</font> |
| verify_type | 余额支付安全核验方式 | String | 16 | N | SMS-短信验证 |
| verify_value | 核验值 | String | 64 | C | verify_type不为空时必填。当verify_type=SMS时，填写用户收到的短信验证码 |
| imaxn_pay | 支付类型 | String | 10 | N | SURETY_PAY:延迟交易 |
| imax_pay_callback_url | 验证成功后跳转地址 | String | 512 | N | 验证成功后跳转地址，无时不显示返回按钮。在交易参与方有用户，且用户是LV3时生效。 |
| notify_url | 异步通知地址 | String | 256 | N | 异步通知地址，在交易参与方有用户，且用户是LV3时生效。 |

<!-- extend:start -->
<!-- div:extend-table 024aa3d3_c4cb_4d76_9720_303f7da3852d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend db32d472_da11_4089_be37_8d3f9e03f03e">acct_infos</span> | 分账明细 | Array |  | N |  |
| percentage_flag | 百分比分账标志 | String | 1 | N | Y:使用百分比分账；<font color="green">示例值：Y</font> |
| is_clean_split | 是否净值分账 | String | 1 | N | Y:使用净值分账，仅在交易手续费由出款方承担且使用百分比分账时起作用；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table db32d472_da11_4089_be37_8d3f9e03f03e-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ,最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 开户自动生成编号；<font color="green">示例值：6666000108854952</font> |
| acct_id | 账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：F00598600</font> |
| percentage_div | 分账百分比% | String | 6 | N | <font color="green">示例值：23.50</font>，表示23.50%。仅在percentage_flag=Y时起作用<br> acct_infos中全部分账百分比之和必须为100.00%。 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 5065d14f_06e9_4d96_95ea_638c013b3f66-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_product | 产品子类 | String | 20 | N | <font color="green">示例值：1</font> |
| transfer_type | 转账原因 | String | 2 | Y | 01：卡券推广类；02：卡券核销类；03：消费；04：工资代发；05：分润；06：灵活用工；<font color="green">示例值：01</font> |
| latitude | 纬度 | String | 32 | N | 格式：+表示北纬，-表示南纬。纬度整数位不超过2位，小数位不超过6位。<font color="green">示例值：+37.12</font><br/>IP地址、经纬度、基站地址最少要送其中一项 |
| longitude | 经度 | String | 32 | N | 格式：+表示东经，-表示西经；经度整数位不超过3位，小数位不超过5位；<font color="green">示例值：-121.213</font><br/>IP地址、经纬度、基站地址最少要送其中一项 |
| base_station | 基站地址 | String | 32 | N | 【mcc】+【mnc】+【location_cd】+【lbs_num】<br/>- mcc:移动国家代码，460代表中国；3位长<br/>- mnc：移动网络号码；2位长；<br/>- location_cd：位置区域码，16进制，5位长<br/>- lbs_num：基站编号，16进制，5位长<br/>- 注意若位数不足用空格补足；<br/><font color="green">示例值：460001039217563</font>，460（mcc)， 00(mnc)，10392(location_cd)， 17563(lbs_num) <br/>经纬度、基站地址、IP地址三组信息至少填写一组 |
| ip_addr | IP地址 | String | 32 | N | <font color="green">示例值：172.28.52.52</font>；经纬度、基站地址、IP地址三组信息至少填写一组 |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "ord_amt": "0.01",
        "req_seq_id": "20240515132857954fk8wpk2hvwnnfw",
        "req_date": "20240515",
        "risk_check_data": "{\"transfer_type\":\"04\",\"sub_product\":\"1\"}",
        "out_huifu_id": "6666000109133323",
        "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000109133323\",\"div_amt\":\"0.01\"}]}"
    },
    "sign": "XS2o/+V6zyIcMm0xc7un8CCe8n3DKjWqRyzMNK29rQipgjFnNR3NG7MMcBoE9GwS6oFGWF03v97wd6CfaFP6wYPlwHiGUmYCu1mBk6T+XKGh6NFRr7sHoTetNSSzkICqTe7XzHAEVdNlW7jWL8Bjx6UmyveqY8tE0DBWyvjpkgE07bM07Dn3YPDPx3HWkcs0/HHuCPcdb/qFQGETgEwIcdyBe6wHBtn5uwPbYLgqUw08jbzjdt59qgUJG+S1mn0jCcaeayTFKhH1Ee4u7+DeqZQBKNvBfHPCY0hgMBibZhR2CQwaAJkrerOv87AuAnw1LG4e3/643/Vj9GbGU/2GJA=="
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
| out_huifu_id | 出款商户号 | String | 32 | N | 出款方商户号；<font color="green">示例值：6666000108854953</font> |
| ord_amt | 支付金额 | String | 14 | Y | <font color="green">示例值：200.00</font> |
| <span class="extend ec03a4d0_c009_40b8_aaa4_2694d4eb4433">acct_split_bunch</span> | 分账对象 | String |  | Y | json格式。余额支付支持付款给多账户。<br/>如余额支付100元，支付给A账户60元，支付给B账户40元。 |
| hf_seq_id | 全局流水号 | String | 128 | N | 汇付返回流水号；<font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| good_desc | 商品描述 | String | 256 | N | <font color="green">示例值：商品描述</font> |
| trans_stat | 交易状态 | String | 1 | N | P:处理中；S：成功；F：失败；示例值：S |
| trans_finish_time | 交易完成时间 | String | 14 | N | 余额支付完成时间，格式：yyyyMMddHHmmss；<font color="green">示例值：20211021163242</font> |
| remark | 备注 | String | 256 | N | <font color="green">示例值：备注</font> |
| out_acct_id | 出款方账户号 | String | 32 | N | <font color="green">示例值：F00598600</font> |
| fund_type | 资金类型 | String | 16 | C | 资金类型。支付渠道为中信E管家时，资金类型必填（[详见说明](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)） |
| acct_channel | 支付渠道 | String | 8 | N | 支付渠道。HUIFU=汇付账务(默认)；ZXE=中信E管家 |
| trans_fee_take_flag | 手续费承担方标识 | String | 4 | C | 余额支付手续费承担方标识；商户余额支付扣收规则为接口指定承担方时必填！枚举值：<br/>OUT：出款方；<br/>IN：分账接受方。<br/><font color="green">示例值：IN</font> |
| unconfirm_amt | 待确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| confirmed_amt | 已确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| jump_url | 支付密码验证跳转地址 | String | 512 | N | 交易参与方有用户，且用户是LV3时返回。商户引导用户跳转该地址完成验证。链接有效期5分钟。 |

<!-- extend:start -->
<!-- div:extend-table ec03a4d0_c009_40b8_aaa4_2694d4eb4433-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 640ca224_2b46_48d6_afd1_66cfcef478c9">acct_infos</span> | 分账明细 | Array |  | N |  |
| fee_huifu_id | 手续费承担方商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| fee_acct_id | 手续费承担方账户号 | String | 32 | N | <font color="green">示例值：F00598600</font> |
| fee_amt | 手续费金额 | String | 14 | N | 单位:元，保留两位小数。<font color="green">示例值：1.23</font> |
| is_clean_split | 是否净值分账 | String | 1 | N | Y:使用净值分账，仅在交易手续费由出款方承担且使用百分比分账时起作用；<font color="green">示例值：Y</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 640ca224_2b46_48d6_afd1_66cfcef478c9-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，灵活用工以异步返回的金额为准<font color="green">示例值：1.00</font> ,最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 开户自动生成编号；<font color="green">示例值：6666000108854952</font> |
| acct_id | 账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：F00598600</font> |
| trans_stat | 交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；灵工用工场景，以异步返回的交易状态为准<font color="green">示例值：P</font> |
| fee_amt | 手续费金额 | String | 14 | N | 手续费金额，单位:元。仅在分账接受方承担手续费时返回。 <font color="green">示例值：0.02</font> |
| unconfirm_amt | 待确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "req_seq_id": "202110210012100005",
        "req_date": "20211021",
        "huifu_id": "6666000018344461",
        "out_huifu_id": "6666000018344461",
        "ord_amt": "0.01",
        "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000018344461\"}]}",
        "hf_seq_id": "003500TOP2B211021163242P447ac132fd200000",
        "trans_finish_time": "20211021163242",
        "trans_stat": "S"
    },
    "sign": "JOM+IXkaXHqVSNhXxPjrt+lQzj/85Ky32j1sdmOotc4JZcPRYX7IofUHGHw3iLAwELBmjW8/CSK1nx+aMUIQ1ALqhyYvBLxNiD2fL17XhWEhlUllzsSQCI00mS6po3/uGefmSl3f7i3JhM+Huc0i97A5U7ebUIvVUEigk+sV/VNTm1CWWRzClVF9rLVQCvYPsQDLOi3ejCZ29W5SMLircNPq7YmPC35lzqHt91LFpZDudtqo3E0Tjgyop2+8OR+VRQ2gx6xvbmq92dRE3+zHzrxZ1gqPDO3zGSr/gwq6/3Ha8Op45Fkr9F4s6G6QBcx44BVnlKyGMKiYvzYE2I3h3g=="
}
```


#### 异步返回参数

仅当灵活用工场景且灵活用工平台为汇优财时，或者交易参与方有用户且用户是LV3，传入了异步通知地址时才有异步通知。


**公共参数：**

| 参数        | 中文名    | 定义     | 长度  | 必填 | 说明              |
| :------- | :------- | :----- | :--- | :--- | :---------------------------------------------------- |
| resp_code | 业务返回码  | string | 8   | Y  | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%ba%bf%e4%b8%8a%e4%ba%a4%e6%98%93%e8%bf%94%e5%9b%9e%e7%a0%81), <font color="green">示例值：00000000</font>      |
| resp_desc | 业务返回描述 | string | 512 | Y  | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%ba%bf%e4%b8%8a%e4%ba%a4%e6%98%93%e8%bf%94%e5%9b%9e%e7%a0%81)；<font color="green">示例值：交易成功</font>        |
| resp_data | 业务数据   | string |     | Y  | 业务数据，见resp_data |

**resp_data：**  

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 业务请求时间YYYYMMDD（发起余额支付请求时间）YYYYMMDD |
| req_seq_id | 交易请求流水号 | String | 128 | Y | 业务请求流水号(发起余额支付请求流水号) |
| hf_seq_id | 全局流水号 | String | 128 | N | 汇付返回流水号 |
| product_id | 产品号 | String | 64 | Y | 产品号 |
| huifu_id | 商户号 | String | 32 | Y | 发起方商户号 |
| ord_amt | 订单金额 | String | 14 | Y | 订单金额 |
| trans_type | 交易类型 | String | 32 | Y | 余额支付：ACCT_PAYMENT |
| trans_stat | 交易状态 | String | 1 | Y | PSF P:处理中；S：成功；F：失败；C：完成。 状态为完成时，需查看分账对象中每个分账的具体状态 |
| <span class="extend 1be936b3_eee8_4eee_a1c9_6481c00cbc92">acct_split_bunch</span> | 分账对象 | Object |  | Y | 分账对象，jsonObject字符串 |

<!-- extend:start -->
<!-- div:extend-table 1be936b3_eee8_4eee_a1c9_6481c00cbc92-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 84bcf3af_c65c_4e28_9f48_a42559384bfa">acct_infos</span> | 分账明细 | Array |  | N |  |
| fee_huifu_id | 手续费承担方商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| fee_acct_id | 手续费承担方账户号 | String | 32 | N | <font color="green">示例值：F00598600</font> |
| fee_amt | 手续费金额 | String | 14 | N | 单位:元，保留两位小数。<font color="green">示例值：1.23</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 84bcf3af_c65c_4e28_9f48_a42559384bfa-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> ,最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 开户自动生成编号；<font color="green">示例值：6666000108854952</font> |
| acct_id | 账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：F00598600</font> |
| trans_stat | 分账交易状态 | String | 1 | N | P：处理中、S：成功、F：失败；灵活用工余额支付交易状态为C时，需查看分账交易状态；<font color="green">示例值：P</font> |
| fee_amt | 手续费金额 | String | 14 | N | 手续费金额，单位:元。仅在分账接受方承担手续费时返回。 <font color="green">示例值：0.02</font> |
<!-- extend:end -->


#### 业务返回码

查看全部[公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)

| 返回码   | 返回描述                                                   | 处理                                               |
| :-------- | :---------------------------------------------------------- | :-------------------------------------------------- |
| 00000000 | 交易处理完成                          |参考trans_stat值确定交易状态  |
| 00000100 | 交易处理未完成   |通过余额支付查询接口获取交易处理结果   |
| 10000000 | 请求参数校验存在问题      | 返回描述会告知参数校验失败的原因，更改对应字段后再次发起请求即可 |
| 21000000 | 手续费账户类型传入钱包类型,手续费商户号必须填写            | 填写手续费用户号                                   |
| 21000000 | 分账入款账户存在钱包类型，出款账户类型必须是钱包类型       | 分账入款账户存在钱包类型，出款账户类型须是钱包类型 |
| 22000000 | 产品号不存在                                               | productId不存在或状态异常                          |
| 22000002 | 商户配置信息校验失败                 |返回描述会告知业务校验失败的原因    |
| 22000003 | 账户信息不存在或者状态异常                                 | 账户配置错误                                       |
| 22000004 | 业务校验失败                                       | 返回描述会告知业务校验失败的原因                                   |
| 22000005 | 调用钱包系统检查配置不存在                                 |                                                    |
| 22000005 | 商户支付交易业务配置为空或多条                             | 检查商户支付交易业务配置                           |
| 22000005 | 交易手续费外扣标记只能是外扣和内扣                         | 商户支付交易业务配置中OutFeeFlag不合法             |
| 22000005 | 手续费费率未配置                                           | 检查手续费费率                                     |
| 22000005 | 手续费计算错误                                             | 检查手续费计算                                     |
| 23000002 | 出款方不从属于交易发起方                                   | 发起方和出款方从属校验失败                         |
| 23000003 | 分账金额总和必须等于交易金额                               | 检查订单金额与分账串总金额是否一致                 |
| 23000003 | 交易金额不足以支付内扣手续费                               | 内扣时分账金额须大于手续费金额                     |
| 23000003 | 取现金额不足以支付内扣手续费                               |                                                    |
| 23000004 | 内扣交易，手续费承担方必须参与分账                         | 检查SSP 配置内扣                                   |
| 90000000 | 交易处理失败  |参考trans_stat值确定交易状态，返回描述会告知处理失败的原因   |
| 98888888 | 系统错误             |请提供接口URL及请求参数，联系斗拱运维处理  |
| 其他返回码 |              |若无明确trans_stat字段表明交易状态，可调用余额支付查询接口获取交易状态。<br/>或需要联系斗拱运维人工查看 |

