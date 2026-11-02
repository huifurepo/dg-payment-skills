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
## 交易确认退款

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/payment/delaytrans/confirmrefund

*最近更新时间：2025.03.06*
### 应用场景
商户可在交易确认成功后，调用本接口将已确认的订单金额退回至原商户账户。

**适用对象**    
开通延迟交易功能的商户。

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
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20210917</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一huifu_id下当天唯一；<font color="green">示例值：2021091708126665001</font> |
| huifu_id | 商户号 | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000109812123</font> |
| org_req_date | 原交易请求日期 | String | 8 | Y | 指交易确认请求日期，格式为yyyyMMdd，<font color="green">示例值：20210917</font> |
| org_req_seq_id | 原交易请求流水号 | String | 128 | Y | 指交易确认请求流水号，<font color="green">示例值：2021091708126665002</font> |
| <span class="extend 52147df8_6c69_4d86_b930_5a431b675f29">acct_split_bunch</span> | 分账对象 | String | 4000 | N | 分账信息，jsonObject字符串。 |
| loan_flag | 是否垫资退款 | String | 2 | N | Y 是垫资出款， N 是普通出款， 为空默认N；<font color="green">示例值：N</font> |
| loan_undertaker | 垫资承担者 | String | 32 | N | 垫资方的huifu_id；为空: 各自承担。不为空走第三方垫资。<br/><font color="green">示例值：6666000109812123</font><br/>目前支持商户垫资。**垫资方一定参与了交易分账，否则不支持垫资**。 |
| loan_acct_type | 垫资账户类型 | String | 2 | N | 01:基本户, 05: 充值户, 默认充值户；<font color="green">示例值：05</font> |
| remark | 备注 | String | 256 | N | <font color="green">示例值：备注</font> |

<!-- extend:start -->
<!-- div:extend-table 52147df8_6c69_4d86_b930_5a431b675f29-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 8b3eddea_b847_4c7f_905e_858f0050be27">acct_infos</span> | 分账明细 | Array |  | N | 分账明细 |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 8b3eddea_b847_4c7f_905e_858f0050be27-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；<font color="green">示例值：6666000109812123</font> |
| div_amt | 分账金额(元) | String | 14 | Y | 被分账商户退款金额；保留两位小数，<font color="green">示例值：1.00</font>，最低传入0.01 |
| part_loan_amt | 垫资金额(元) | String | 12 | N | 垫资方退款金额；保留两位小数，<font color="green">示例值：1.00</font>，最低传入0.01；<br/>注：若指定了垫资方且由垫资方全额垫资，则该字段为空 |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "org_req_date": "20240513",
        "org_req_seq_id": "20240513105825239x0lp7ldbus4sji",
        "req_seq_id": "20240513112056652yl1b9dxx6hae9b",
        "req_date": "20240513",
        "huifu_id": "6666000109133323",
        "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000109133323\",\"div_amt\":\"0.01\"}]}"
    },
    "sign": "gZjn3P83X/aEb2IFQKr4GLbLZ6g5AukwWNSoKTNP2g5Lb5gE2mDOZHIdUCyVAc6x1f9394VDeUwzykCkyTz/YJdk7vIR3ki0e7ghcp1oy7ht3N/cnk89kJuJIIByyXp2XPnVOivkENtfSbSxksG+YQpmxbJiFbgcovJySSATc2MhRMCl2WReZcxRSZslWMPuHrIti5rkz08X2xdOEvVw8dbyLdNwNhveeexuXw1u9QzihhlME/4GGGy3gJtrN7f5UCluex19FXHQV8XIWk5A1iREXICIxqqaOcfoUNxL1fRxgGSknN0sUzlFChaQtw3tKtqofSXEhwYuNQzHMlcENg=="
}
```
### 返回参数


#### 同步返参

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码)  ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：交易成功</font> |
| trans_stat | 交易状态 | String | 1 | Y | P：处理中、S：成功、F：失败；<font color="green">示例值：S</font> |
| hf_seq_id | 全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| req_date | 请求日期 | String | 8 | Y | 交易时传入，原样返回；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 交易时传入，原样返回；<font color="green">示例值：2021091708126665001</font> |
| huifu_id | 商户号 | String | 32 | Y | 示例值:6666000109812123 |
| org_req_seq_id | 原交易请求流水号 | String | 128 | Y | <font color="green">示例值：2021091708126665001</font> |
| unconfirm_amt | 待确认总金额 | String | 14 | N | 待确认总金额；单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| confirmed_amt | 已确认总金额 | String | 14 | N | 已确认总金额；单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| org_req_date | 支付交易业务请求时间 | String | 8 | Y | <font color="green">示例值：20210917</font> |
| org_hf_seq_id | 支付交易汇付全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00001</font> |
| <span class="extend e3ffacc9_3cb8_4227_9206_676dc6bdad46">acct_split_bunch</span> | 分账对象 | String |  | N | jsonObject字符串 |
| remark | 备注 | String | 256 | N | 请求参数里传入，返回参数里原样返回；<font color="green">示例值：备注</font> |
| loan_flag | 是否垫资退款 | String | 2 | N | Y 是垫资出款， N 是普通出款, 按请求原样返回 |
| loan_undertaker | 垫资承担者 | String | 32 | N | 垫资方的huifu_id, 按请求原样返回 |
| loan_acct_type | 垫资账户类型 | String | 2 | N | 01:基本户, 05: 充值户, 按请求原样返回 |

<!-- extend:start -->
<!-- div:extend-table e3ffacc9_3cb8_4227_9206_676dc6bdad46-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 3b714b50_a323_4382_ad7f_0a7c8d8c5f8f">acct_infos</span> | 分账明细 | Array |  | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 3b714b50_a323_4382_ad7f_0a7c8d8c5f8f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额(元) | String | 14 | Y | 单位元，示例值:1.00 |
| huifu_id | 分账接收方ID | String | 32 | Y | 示例值:6666000109812123 |
| acct_id | 分账接收方账户号 | String | 32 | Y | 示例值:F00598600 |
| split_fee_amt | 分账手续费金额(元) | String | 14 | N | 示例值:0.10 |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | N | 示例值:6666000123120001 |
| split_fee_acct_id | 分账手续费承担方账号 | String | 32 | N | 示例值:F00598600 |
| part_loan_amt | 垫资金额(元) | String | 12 | N | 垫资方退款金额；保留两位小数 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "交易成功",
        "trans_stat": "S",
        "hf_seq_id": "0031000topA221108195341P273c0a831f000000",
        "req_date": "20221108",
        "req_seq_id": "20220609022195520211667908421",
        "huifu_id": "6666000103423237",
        "org_req_seq_id": "2022072724398620211667900766",
        "loan_flag": "N",
        "unconfirm_amt": "99.68",
        "confirmed_amt": "0.32",
        "org_req_date": "20221108",
        "org_hf_seq_id": "0047default221108174606P607c0a831e100000"        
    }
}
```


#### 业务返回码

* 查看全部 [公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)

| 返回码 | 返回描述     | 处理                                               |
| :------- | :----------------------------------------------------------- | :-------------------------------------------------- |
| 00000000 | 交易成功                                                     |                                                    |
| 00000100 | 交易正在处理中                                               | 交易正在处理，请等待处理结束后再进行               |
| 10000000 | 请求内容体不能为空                                           | 检查参数是否符合要求                               |
| 10000000 | %s不能为空（%s代指具体报错参数名）                           | 检查参数是否符合要求                               |
| 10000000 | %s长度固定%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度） | 检查参数是否符合要求                               |
| 10000000 | %s最大长度为%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度） | 检查参数是否符合要求                               |
| 10000000 | %s的传入枚举[%d]不存在（%s代指具体报错参数名、%d代指具体报错参数的值） | 检查参数是否符合要求                               |
| 10000000 | %s不符合%d格式（%s代指具体报错参数名、%d代指具体报错参数值的格式） | 检查参数是否符合要求                               |
| 20000001 | 操作过于频繁                                                 | 歇一会再试试                                       |
| 22000000 | 产品号不存在                                                 | 找不到产品号                                       |
| 22000000 | 产品号状态异常                                               | 打开产品号使用权限                                 |
| 22000002 | 商户信息不存在                                               | 检查商户信息配置                                   |
| 22000002 | 商户状态异常                                                 | 请确认交易状态                                     |
| 22000003 | 账户信息不存在                                               | 请检查账户信息                                     |
| 23000000 | 原交易未入账                                                 | 原交易未成功，请检查                               |
| 23000001 | 原交易不存在                                                 | 请确认原交易信息是否填错                           |
| 23000003 | 申请退款金额大于可退款余额                                   | 不可全额退款，尝试减小金额                         |
| 23000003 | 手续费退款金额大于可退手续费金额                             | 请检查原交易可返还手续费是否充足                   |
| 23000004 | 该交易商户号与原交易商户号不一致                             | 请核对原交易号与此次申请商户号                     |
| 23000004 | 分账串信息与原交易不匹配                                     | 请检查原交易分账串与此次申请分账串是否匹配         |
| 23000004 | 原分账交易带手续费，不支持部分退款                           | 请全额退款                                         |
| 98888888 | 系统错误                                                     | 一般为内部系统错误，请联系对技术运营对接人员处理。 |
| 99999999 | 系统异常，请稍后重试                                         | 稍后重试                                           |

