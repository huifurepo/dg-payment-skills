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
## 余额支付退款查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/acctpayment/refund/query

*最近更新时间：2026.04.27*
### 应用场景
本API为后台版接口，用于查询商户单笔余额支付退款状态及明细。

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
| org_req_seq_id | 退款请求流水号 | String | 128 | Y | <font color="green">示例值：2021091708126665001</font> |
| org_req_date | 余额支付退款请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20210917</font> |
| huifu_id | 商户号 | String | 32 | Y | 发起方商户号；<font color="green">示例值：6666000109812123</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "org_req_seq_id": "20240515134124629vmalwxl5nxajgd",
        "org_req_date": "20240515",
        "huifu_id": "6666000109133323"
    },
    "sign": "iB042GiwO+Rt+hw9dObx2B1Gc6d2X/fAsUoA4TOrjmaxUQTjjSezd6GTInLcucUKtNdxgZ7PMqgJVsv27sD4nCfL0LKU86DoLc4IxX2ZvAiCihiMZ5vmlG+mxkxZd7cCQdITP4JA26zty/5EpuUxUfiyYA2N8xS2NbjcYUYtAt3dvB4s7pjbYYAG5gej70UBADPIQxfyCMnCAQkHOt6bQdNxvO6Sk7lKvdc3QgFg/RQGmY31SS3z6yLkKF1Fl4JnHpiv/g1+u4eExE6SoQxnVN+aoyB/VG9T1EaFNtILMP5kTggha6SGJlG17MFRkUT4KW0KXcgHEAv1MssH2wJA6A=="
}
```
### 返回参数


#### 同步响应参数

**data **

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](#业务返回码)  ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：交易成功</font> |
| org_req_seq_id | 退款请求流水号 | String | 128 | N | <font color="green">示例值：2022082408452985319884</font> |
| org_req_date | 余额支付退款请求日期 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20210917</font> |
| org_hf_seq_id | 原余额支付退款全局流水号 | String | 40 | N | 原余额支付退款全局流水号 |
| huifu_id | 商户号 | String | 32 | Y | 退款请求发起方商户号；示例值：6666000109812123 |
| product_id | 产品号 | String | 32 | Y | 产品号，接入时提供；<font color="green">示例值：YYZY</font> |
| ord_amt | 退款金额 | String | 14 | Y | 需保留小数点后两位，<font color="green">示例值：10.00</font>最低传入0.01 |
| trans_stat | 交易状态 | String | 1 | Y | P:处理中；S：成功；F：失败；<font color="green">示例值：S</font> |
| trans_finish_time | 退款完成时间 | String | 14 | Y | 格式yyyyMMddHHmmss；<font color="green">示例值：20221023112343</font> |
| <span class="extend d7f54618_de37_4101_8821_639e0a559d3b">acct_split_bunch</span> | 分账对象 | String |  | N | 分账信息，jsonObject字符串。 |
| remark | 备注 | String | 45 | N | <font color="green">示例值：备注</font> |
| unconfirm_amt | 待确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| confirmed_amt | 已确认总金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |

<!-- extend:start -->
<!-- div:extend-table d7f54618_de37_4101_8821_639e0a559d3b-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend f73cd0be_5975_4cd2_bb0b_63631b8d44f2">acct_infos</span> | 退账明细 | Array |  | Y | 退款信息 |
| fee_huifu_id | 手续费承担方商户号 | String | 16 | N | <font color="green">示例值：6666000123123123</font> |
| fee_acct_id | 手续费承担方账户号 | String | 32 | N | <font color="green">示例值：A28356961</font> |
| fee_amt | 手续费 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table f73cd0be_5975_4cd2_bb0b_63631b8d44f2-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 退款金额 | String | 14 | Y | <font color="green">示例值：9.00</font> |
| huifu_id | 退账方商户号 | String | 32 | Y | <font color="green">示例值：6666000109812123</font> |
| acct_id | 账户号 | String | 32 | N | 分账账户号；<font color="green">示例值：F00598600</font> |
| fee_amt | 手续费金额 | String | 14 | N | 手续费金额，单位:元。仅在分账接受方承担手续费时返回。 <font color="green">示例值：0.02</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "org_req_date": "20211021",
        "org_req_seq_id": "20211021787214848332",
        "huifu_id": "6666000018344461",
        "product_id": "SPIN",
        "ord_amt": "0.01",
        "trans_stat": "S",
        "trans_finish_time": "20211021164132",
        "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000018344461\"}]}",
        "remark": "1234567890"
    },
    "sign": "W/KTIUpn0syFTvz3JA59edacfrUadIe4YJBE2WSGXA1BP0sfijnAu0PxSIDaXVapCXym+wM3n5g8ntgIpsKqX47Fhmg8+S79kA7yNbW17VI43pQaPKXaB3mZwiz6y8v+JwJdGNu6aXIjBPfH22fN6/dpwyMoOawQY+2ytJmq3m+cTPr/9e32Hm5yuwWXg+Tb7qBFopdApNg0UoLwVStfEsCgQqgoVQAvPwEEecid05BW1xte+HsW5pvqYnI0dxMKc3hgMrv/CWeiU1viQjkRDFgQ3EtMSt83qqgwKlTE6jRGLh3dbfSLAuh+K7TlvDpYTvWeD9Rmr3fjzb0kx6Nq9w=="
}
```


#### 业务返回码

* 查看全部 [公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)

| 返回码   | 返回描述                                                     | 处理                                        |
| :-------- | :------------------------------------------------------------ | :------------------------------------------- |
| 10000000 | %s不能为空 <br />%s长度固定%d位 <br />%s最大长度为%d位 <br />%s的传入枚举(%s)不存在 <br />%s不符合xx格式 %s解密失败 <br />（%s代指报错参数名、%d代指字段长度） | 入参数据不符合接口要求,参考接口文档调整入参 |
| 22000000 | 产品号不存在                                                 | 确认产品号对应的产品信息是否正常            |
| 22000000 | 产品号状态异常                                               | 确认产品号对应的产品信息是否正常            |
| 23000004 | 暂不支持通过全局流水查询                                     |                                             |
| 98888888 | 系统错误                                                     |                                             |
| 23000001 | 原交易不存在                                                 |                                             |
| 00000000 | 查询成功                                                     |                                             |

