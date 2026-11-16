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
## 修改子账户配置

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/merchant/settle/modify

*最近更新时间：2025.01.09*
### 应用场景
已完成子账户开通的商户，若需变更子账户的配置信息，调用此接口。

**适用对象**     
商户需要申请修改子账户结算配置，可调用该接口。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* 公共请求参数

| 参数       | 中文名   | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :-------------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商或商户的huifu_id； <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为总部商户时，此字段填写商户huifu_id |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>                                      |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |


### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | <font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220905</font> |
| huifu_id | 商户汇付Id | String | 18 | Y | 商户号；<font color="green">示例值：6666000109812123</font> |
| upper_huifu_id | 上级汇付Id | String | 18 | Y | 上级商户或渠道商；<font color="green">示例值：6666000109812120</font> |
| acct_id | 子账户号 | String | 16 | Y | <font color="green">示例值：F00598600</font> |
| <span class="extend bba81a50_6402_43a6_a37c_ba656e0f396c">settle_config</span> | 结算规则配置 | String |  | Y | 商户结算规则配置，jsonObject格式 |
| <span class="extend 0abd7349_5f2b_4147_b17b_45cc26cbaa48">card_info</span> | 结算卡信息配置 | String |  | C | 新账户绑定的结算银行账户。jsonObject格式。若结算规则中上送token_no，则card_info不填。 |
| async_return_url | 异步请求地址 | String | 120 | N | 格式：http或https协议请求，为空不推送审核消息。<br/><font color="green">示例值：http://service.example.com/to/path</font> |

<!-- extend:start -->
<!-- div:extend-table bba81a50_6402_43a6_a37c_ba656e0f396c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| settle_status | 状态 | String | 2 | Y | 1:开通 0:关闭；<font color="green">示例值：1</font> |
| settle_cycle | 结算周期 | String | 2 | Y | D1：下个自然日到账， T1：下个工作日到账； <font color="green">示例值：T1</font> |
| min_amt | 起结金额 | String | 14 | N | 起结金额，账户余额大于等于起结金额才会发起结算。不传则不设置起结金额；<br/>单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。<br/><font color="green">示例值：1000.00</font> |
| remained_amt | 留存金额 | String | 14 | N | 留存金额，该部分资金不会结算。不传则不设置留存金额 ；<br/>单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。<br/><font color="green">示例值：1000.00</font> |
| settle_abstract | 结算摘要 | String | 128 | N | 可自定义结算打款备注，支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；不填默认为空；<font color="green">示例值：汇付商城业务</font> |
| out_settle_flag | 手续费外扣标记 | String | 1 | N | 1:外扣，结算时从out_settle_huifuid账户扣手续费 <br/>2:内扣，从结算金额中扣手续费，默认为内扣<br/><font color="green">示例值：2</font> |
| out_settle_huifuid | 结算手续费外扣商户号 | String | 18 | C | 填写承担手续费的汇付商户号；当out_settle_flag=1时必填，否则非必填；<font color="green">示例值：6666000123123123</font> |
| out_settle_acct_type | 结算手续费外扣账户类型 | String | 2 | N | 01：基本户（不填默认取值）；05：充值户；09：营销户；<font color="green">示例值：01</font> |
| settle_pattern | 结算方式 | String | 2 | N | P0：批次结算，指按照指定结算批次号进行资金结算。不填默认P0；<br/>~~P1：定时结算，自定义时间结算是指按照商户指定到账时间进行资金结算。~~<br/>P2:批次定时结算；两种结算方式需二选一。<font color="green">示例值：P1</font> |
| settle_batch_no | 结算批次号 | String | 16 | C | 结算方式为P0：批次结算时必填，即将按指定结算批次号进行资金结算；<font color="green">示例值：100</font>；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| is_priority_receipt | 是否优先到账 | String | 1 | N | 当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效<br/> Y：是，N：否，<font color="green">示例值：Y</font> |
| settle_time | 自定义结算处理时间 | String | 6 | C | 当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定<br/>到账时间，格式：HHmmss；<font color="green">示例值：103000</font> |
| token_no | 卡序列号 | String | 20 | N | 与card_info不可同时传入 |
| fixed_ratio | 节假日结算手续费率 | String | 6 | C | settle_cycle为D1时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；<br>settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；<font color="green">示例值：0.05</font> |
| constant_amt | 节假日结算手续费固定金额 | String | 15 | C | settle_cycle为D1时必填。单位元，需保留小数点后两位。不收费请填写0.00；<br>settle_cycle结算周期为D1时，遇节假日按此费率结算 ；<br/> <font color="green">示例值：1.00</font> |
| workday_fixed_ratio | 工作日结算手续费率 | String | 6 | N | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；<font color="green">示例值：0.05</font> |
| workday_constant_amt | 工作日结算手续费固定金额 | String | 15 | N | 单位元，需保留小数点后两位。不填默认为0.00；<font color="green">示例值：1.00</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 0abd7349_5f2b_4147_b17b_45cc26cbaa48-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| card_type | 结算账户类型 | String | 1 | Y | 0：对公账户 1：对私法人账户 2：对私非法人账户；<font color="green">示例值：0</font><br/>个人商户不支持填写对公账户和对私非法人账户。 |
| card_name | 结算账户名 | String | 128 | Y | 结算银行卡对应的户名；<font color="green">示例值：上海汇付支付有限公司</font><br/>当card_type=0时填写企业名称<br/>当card_type=1时填写法人姓名，对私法人结算银行户名与法人姓名必需一致；<br/>当card_type=2时填写非法人姓名 |
| card_no | 结算账号 | String | 32 | Y | 结算银行卡号，为避免资金结算失败，请正确填写； <font color="green">示例值：98140008801800008888</font><br/>注意：系统会验证卡号所属银行，请准确填写； |
| prov_id | 银行所在省 | String | 6 | Y | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font>；如修改省市要级联修改 |
| area_id | 银行所在市 | String | 6 | Y | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font>；如修改省市要级联修改 |
| bank_code | 银行编号 | String | 8 | C | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) ； <font color="green">示例值：01020000 </font> <br/>当card_type=0时必填 |
| branch_code | 联行号 | String | 12 | C | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) 当card_type=0时必填。<br/><font color="green">示例值：102290026507</font> |
| cert_type | 持卡人证件类型 | String | 2 | C | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》 当card_type=0时为空， 当card_type=1或2时必填；<font color="green">示例值：00</font> |
| cert_no | 持卡人证件号码 | String | 32 | N | 如持卡人证件类型为00：身份证，则填写身份证号码；<font color="green">示例值：310112200001018888</font>。**系统会做格式校验** |
| cert_validity_type | 持卡人证件有效期类型 | String | 1 | N | 1:长期有效，0:非长期有效；<font color="green">示例值：0</font> |
| cert_begin_date | 持卡人证件有效期开始 | String | 8 | N | 日期格式：yyyyMMdd，以北京时间为准；<font color="green">示例值：20220125</font> |
| cert_end_date | 持卡人证件有效期开始 | String | 8 | C | 日期格式：yyyyMMdd，以北京时间为准；<font color="green">示例值：20220125</font>，当cert_validity_type=0时必填；当cert_validity_type=1时为空 |
| mp | 结算人手机号 | String | 11 | N | <font color="green">示例值：18611111111</font> |
| verify_code | *验证码* | String | 6 | N | 结算卡修改需要短信验证码，请先调用[商户短信发送接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shdxfs)；<font  color="green">示例值：851249</font> |
| acct_ids | *适用子账户* | String | 128 | N | 结算卡适用子账户，多个用逗号隔开；<font  color="green">示例值：D02348323,D01236743</font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000106070589",
    "product_id": "ZDTEST",
    "data": {
        "req_seq_id": "SAS20221212074418465924575",
        "req_date": "20221212",
        "huifu_id": "6666000106071234",
        "upper_huifu_id": "6666000106065087",
        "acct_id": "C01571234",
        "async_return_url": "",
        "settle_config": "{\"settle_status\":\"0\",\"settle_cycle\":\"D1\",\"fixed_ratio\":\"66.88\",\"out_settle_acct_type\":\"01\",\"out_settle_flag\":\"1\",\"out_settle_huifuid\":\"6666000106071234\",\"min_amt\":\"1\",\"remained_amt\":\"2\",\"settle_abstract\":\"abstract\",\"settle_batch_no\":\"0\",\"settle_pattern\":\"P0\",\"is_priority_receipt\":\"N\",\"settle_time\":\"211221\",\"constant_amt\":\"66.99\",\"token_no\":\"\"}",
        "card_info": "{\"area_id\":\"310100\",\"card_name\":\"张三\",\"card_no\":\"6225682141111111111\",\"card_type\":\"0\",\"prov_id\":\"310000\",\"bank_code\":\"01030000\",\"branch_code\":\"103290040169\",\"branch_name\":\"中国农业银行股份有限公司XXX支行\",\"cert_begin_date\":\"20220101\",\"cert_end_date\":\"20221212\",\"cert_no\":\"220105198806082098\",\"cert_type\":\"00\",\"cert_validity_type\":\"0\",\"mp\":\"17521216927\"}"
    },
    "sign": "Ygt/OxfLeXYcm3qOVozeuYmmS2k+ApGbrR/U8nRBga8MuEMo7I4KDZDvHNXxRYHf2ZkkiOOtiC/eutH629AZXkdeIwB37ivTHidzkgeEuoyGfvRhxzfIRDVkvTQWdcZB61qEnkErZ6yGUn1gB4pe9sok/Hov4N7VqTdeyRQh4AU2G0N7wnBPWktgc6mRXnARNVW8+XXVsCTpYaV5wNxo6j0kOK/1n64Haeqy2ZfJPDmieKlfV7onXrAioiPtqzBs/vqNWgeVU+29UyylS0g/LgxHBOadsx+D+nm+WbTgiqreSOY1SMJSVgZt4yXPcJ3sL6IxPuXmCMacaOyHVX1fjg=="
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| <span class="extend 07b825d5_de99_40af_bc12_0d591d49ad4a">data</span> | 交易响应内容体 | Object |  | N | 业务返回参数，jsonObject格式 |
| sign | 加签结果 | String | 512 | N | [接口加签验签说明](https://paas.huifu.com/partners/guide/#/api_v2jqyq) |

<!-- extend:start -->
<!-- div:extend-table 07b825d5_de99_40af_bc12_0d591d49ad4a-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 256 | Y | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：处理成功</font> |
| huifu_id | 商户号 | String | 18 | Y | <font color="green">示例值：6666000109812123</font> |
| token_no | 绑卡序列号 | String | 20 | N | 可用于结算与取现；账号开通成功，结算卡绑定失败，该字段不返回值；<font color="green">示例值：10004053462</font> |
<!-- extend:end -->


#### 异步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 网关返回码 | String | 5 | Y | 网关返回码 |
| resp_desc | 网关返回描述 | String | 512 | Y | 网关返回描述 |
| sign | 签名 | String | 2048 | Y | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| <span class="extend c9c17549_a780_4133_8e7b_7f0bed69e942">data</span> | 交易响应内容体 | String |  | N | 业务返回参数，jsonObject格式 |

<!-- extend:start -->
<!-- div:extend-table c9c17549_a780_4133_8e7b_7f0bed69e942-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：处理成功</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | 原请求流水号；<font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date | 请求时间 | String | 8 | Y | 原请求时间yyyyMMdd；<font color="green">示例值：20221213</font> |
| audit_status | 审核结果 | String | 1 | Y | Y：审核通过 N：审核拒绝 F：失败；<font color="green">示例值：Y</font> |
| audit_desc | 审核描述 | String | 512 | N | 审核结果描述；<font color="green">示例值：审核通过</font> |
| product_id | 产品编号 | String | 32 | Y | 汇付产品编号；<font color="green">示例值：YYZY</font> |
| huifu_id | 汇付客户号 | String | 18 | N | 商户号；<font color="green">示例值：6666000109812123</font> |
| apply_no | 申请单号 | String | 18 | N | 汇付返回商户开户业务申请单号；<font color="green">示例值：2022121206429317</font> |
| token_no | 绑卡id | String | 20 | N | 账号开通成功，结算卡绑定失败，该字段不返回值；<font color="green">示例值：10000093623</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "apply_no": "2022121206429317",
        "huifu_id": "6666000106071234",
        "resp_code": "90000000",
        "resp_desc": "审核中"
    },
    "sign": "AGZ0sfDcw+p0eQWGJ9PNEoDRdPCAXQ/QRojfE0i/tZNw6oYZ0mR2Wp4sJonZgGh7OEQgFqDkeGhOoZks5BCy4QFPlOtoE1ObjaDFFDCva+pNG5dJdvQaCAeTpNbIWKf5LcDTlzGgm3pxR20eZQNNpS2iyKENwgaPUJhNlFQKOzpiWeiwGb+203xkoVk5Q1xESnFCZyAuAaOEHbwJq9LU9N2UZrfAuPXR7XcxqybtoHUwvF8W4Zr+jDb1hB66oRbIMNQHmM9LKI1v34VGB40xoyz4rAKGvr2q4fk3ppExkabmMSJi1iKE59yHQd/8ptq3ExgA31hQiq7obMLrI8LITA=="
}
```
