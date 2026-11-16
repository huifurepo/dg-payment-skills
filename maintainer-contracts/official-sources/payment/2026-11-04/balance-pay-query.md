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
## 余额支付查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/acctpayment/pay/query

*最近更新时间：2026.09.21*
### 应用场景
本接口用于查询商户单笔余额支付交易状态及明细。

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
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 商户号 | String | 32 | Y | 发起方商户号；<font color="green">示例值：6666000109812123</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 原交易请求日期，格式：yyyyMMdd；<font color="green">示例值：20221023</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | 与org_hf_seq_id二选一；<font color="green">示例值：2021091708126665001</font> |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | 与org_req_seq_id二选一；<br/><font color="green">示例值：003500TOP2B211021163242P447ac132fd200000</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "org_req_date": "20240515",
        "org_req_seq_id": "20240515132857954fk8wpk2hvwnnfw",
        "org_hf_seq_id": "",
        "huifu_id": "6666000109133323"
    },
    "sign": "OL4KoawZQy4GUTKiuhDWZ2k+btm+hnGY0ep/TadzhtZqOJZGjX7Y2xNEgK4tEmoJQRNYQGzALgNjyMm72YAu/WzCWv/7nRu9Jq30ZXF85O9lzXqoIjjXDwvh8PwMmEXG/s65lBHjdQ1g/C3CEy87DUpNKXYFIcdc5hk2cAXuO5Plctjq6/zy7nAaMCE1xrVRMqGn0J+dL2a0f6nIcCLBmoAlXaoBeV5VCxEiDWu5UjEiHfMoD/kk47fV/u9BR2Mjv5xyN4giYKp1GPKrMqsfHmpsI5wc1+s5Tg9zFamzRkarrMUIWXEiwowKV+fLRuGf91qCmHML6HT36DVu81gmEQ=="
}
```
### 返回参数


#### 同步响应参数

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](#业务返回码)  ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：交易成功</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | Y | 业务请求流水号(发起余额支付请求流水号)；<br/><font color="green">示例值：2022082408452985319884</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 原交易请求日期，格式：yyyyMMdd，<font color="green">示例值：20221013</font> |
| huifu_id | 商户号 | String | 32 | Y | 发起方商户号；示例值：6666000108854952 |
| ord_amt | 支付金额 | String | 14 | Y | <font color="green">示例值：23.00</font> |
| <span class="extend 58e2e764_a5de_4cb4_b5e3_c64159387a3b">acct_split_bunch</span> | 分账对象 | String |  | N | 分账信息，jsonObject字符串。余额支付支持付款给多账户。<br/>如余额支付100元，支付给A账户60元，支付给B账户40元。 |
| out_huifu_id | 出款商户号 | String | 32 | N | <font color="green">示例值：6666000108854953</font> |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | 汇付返回的流水号；<br/><font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| trans_stat | 交易状态 | String | 1 | Y | P:处理中；S：成功；F：失败；C：完成（灵活用工余额支付特有，需查看分账交易状态）；示例值：S |
| trans_finish_time | 交易完成时间 | String | 14 | Y | 格式：yyyyMMddHHmmss；<font color="green">示例值：20211021163242</font> |
| remark | 备注 | String | 256 | N | <font color="green">示例值：备注</font> |
| good_desc | 商品描述 | String | 256 | N | <font color="green">示例值：商品描述</font> |
| delay_acct_flag | 延时标记 | String | 1 | N | 是否延时交易，Y为延迟，N为不延迟，不传默认N；<font color="green">示例值：N</font> |
| trans_fee_take_flag | 手续费承担方标识 | String | 4 | C | 余额支付手续费承担方标识；商户余额支付扣收规则为接口指定承担方时必填！枚举值：<br/>OUT：出款方；<br/>IN：分账接受方。<br/><font color="green">示例值：IN</font> |
| unconfirm_amt | 待确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| confirmed_amt | 已确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |

<!-- extend:start -->
<!-- div:extend-table 58e2e764_a5de_4cb4_b5e3_c64159387a3b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 9724d702_e07f_496b_a765_9cf7696d3077">acct_infos</span> | 分账明细 | Array |  | N | acct_infos |
| fee_huifu_id | 手续费承担方商户号 | String | 32 | N | <font color="green">示例值：6666000108854952</font> |
| fee_acct_id | 手续费承担方账户号 | String | 32 | N | <font color="green">示例值：F00598600</font> |
| fee_amt | 手续费金额 | String | 14 | Y | 单位:元，保留两位小数。<font color="green">示例值：1.23</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 9724d702_e07f_496b_a765_9cf7696d3077-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font>，最低传入0.01 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户自动生成编号；<font color="green">示例值：6666000109812123</font> |
| trans_stat | 分账交易状态 | String | 1 | N | 分账交易状态。灵活用工余额支付交易状态为C时，需查看分账交易状态 |
| fee_amt | 手续费金额 | String | 14 | N | 手续费金额，单位:元。仅在分账接受方承担手续费时返回。 <font color="green">示例值：0.02</font> |
| unconfirm_amt | 未确认金额 | String | 14 | N | 未确认金额:元。 <font color="green">示例值：0.02</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "org_req_seq_id": "202110210012100005",
        "org_req_date": "20211021",
        "huifu_id": "6666000018344461",
        "ord_amt": "0.01",
        "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000018344461\"}]}",
        "out_huifu_id": "6666000018344461",
        "org_hf_seq_id": "",
        "trans_stat": "S",
        "trans_finish_time": "20211021163243",
        "remark": "",
        "good_desc": ""
    },
    "sign": "jAd67Y1U2sxczVri84lipa0LcSag6ZYP6yrCnYW3RgqCB2mB2JXymiDZvX+yriMyqUcyztwamA4got/mPVkrhXjTsXKPQZ8BnejoZ5TEnQvf8S52eKyM7KI3nErSDyJf9vLGF3qyKeH6DzFqbZZ3Rhk4Ty+nGJJx59l+dodXALv/3OF29HjqwqykLGFxorRbd7lZ6+EUdcxyeO1h9Tnb68aAhiwiR4HzzgvIsngbpG+0RIvadtVhQ0cEYw7kZJ0uWxRknPurxM2ZV2BXjNagNdlyZ8zeMfK+FOyQOTFmN1PhcVQmSS4S3KEBzBwz8SadL4WiTcyFWGEBC9aXU2+1sw=="
}
```


#### 业务返回码

* 查看全部 [公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)

| <div style="width: 80pt">返回码</div>   | 返回描述                                         | 处理                       |
| :------- | :---------------------------------------------- | :----------------------- |
| 00000000 | 查询成功                                         |参考trans_stat值确定交易状态|
| 10000000 | 表示请求参数校验存在问题   |返回描述会告知参数校验失败的原因，更改对应字段后再次发起请求即可  |
| 21000000 | 原交易请求流水号、原交易汇付全局流水号二选一必填 | 检查参数是否缺少           |
| 22000000 | 产品号不存在                                     | 检查产品号参数             |
| 22000000 | 产品状态异常                                     | 检查产品号参数             |
| 22000003 | 账户信息不存在或者状态异常                       | 检查一下账户配置           |
| 23000001 | 无法查到订单信息                                     | 根据传入订单信息无法查到对应订单，请检查传参信息 |
| 23000003 | 取现金额不足以支付内扣手续费                     |                            |
| 98888888 | 系统错误                                         |请提供接口URL及请求参数，联系斗拱运维处理|
| 其他返回码 |                                          |若无明确trans_stat字段表明交易状态，可联系斗拱运维人工查看|

