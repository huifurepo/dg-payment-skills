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
## 取现

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/settlement/encashment

*最近更新时间：2026.07.09*
### 应用场景
用于商户、用户、渠道商从汇付账户取现到事先绑定的取现银行卡中。

**适用对象**     
商户需开通取现功能权限。

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数

* ##### 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                  |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| sys_id     | 系统号   | String | 32   | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font>  |
| sign       | 加签结果 | String | 512  | Y    | 签名，对报文整体签名  |
| product_id | 产品号   | String | 32   | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>  |
| data       | 数据     | String |      | Y    | JSON格式              |


* ##### 公共返回参数

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)   |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20210917</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：2021091708126665001</font> |
| cash_amt | 取现金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| huifu_id | 取现方ID号 | String | 32 | Y | 提现发起方的汇付ID。支持已配置取现规则的商户、用户。<br/><font color="green">示例值：6666000109812123</font> |
| acct_id | 账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户；<br/><font color="green">示例值：F00598600</font> |
| into_acct_date_type | 到账日期类型 | String | 3 | Y | D0：当日到账；当日交易资金当天可取现到账；<br/>T1：次工作日到账；<br/>D1：次自然日到账；<br/>DM：当日到账；到账资金不包括当天的交易资金；<br/><font color="green">示例值：D0</font> |
| token_no | 取现卡序列号 | String | 20 | Y | 绑定取现卡后可获取取现卡序列号；<font color="green">示例值：10004053462</font> |
| enchashment_channel | 取现渠道 | String | 2 | N | 00：汇付（为空默认）； 10：中信e账通；<font color="green">示例值：00</font> |
| fee_type | 中信e账通手续费承担方 | String | 1 | N | 1：总部承担；2：自身承担。默认为2。 |
| remark | 备注 | String | 100 | N | <font color="green">示例值：备注</font> |
| notify_url | 异步通知地址 | String | 128 | N | <font color="green">示例值：http://service.example.com/to/path</font> |


#### 请求示例

```json
{
  "sys_id": "6666000109812123",
  "product_id": "SPIN",
  "data": {
    "req_seq_id": "202109160899013231200005",
    "req_date": "20210916",
    "huifu_id": "6666000021291985",
    "cash_amt": "0.01",
    "into_acct_date_type": "T0",
    "notify_url": "http://www.gangcai.com",
    "enchashment_channel": "00",
    "token_no": "10004053462"
  }
}

```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | 参见[业务返回码](#业务返回码)，<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回信息](#业务返回码)，<font color="green">示例值：处理成功</font> |
| req_date | 请求日期 | String | 8 | N | 格式：yyyyMMdd；<font color="green">示例值：20211123</font> |
| req_seq_id | 请求流水号 | String | 128 | N | <font color="green">示例值：202109160899013231200005</font> |
| hf_seq_id | 汇付全局流水号 | String | 128 | N | <font color="green">示例值：002900TOP3A221112165433P410ac139c1300001</font> |
| trans_stat | 交易状态 | String | 1 | Y | S：成功  F：失败  P：处理中；<font color="green">示例值：S</font> |
| huifu_id | 商户号/机构号 | String | 32 | N | 汇付分配的商户号/机构号，<font color="green">示例值：6666000109812123</font> |
| acct_id | 账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户；<font color="green">示例值：F00598600</font> |


#### 异步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | 固定返回码，<font color="green">示例值：10000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回信息](#业务返回码)；<font color="green">示例值：处理成功</font> |
| <span class="extend 70bc7529_7e18_47c5_9d2a_7a8b0cb0d1a8">resp_data</span> | 业务返回参数 | String |  | N | json格式； |
| sign | 签名 | String | 255 | Y | 签名，对报文整体签名 |

<!-- extend:start -->
<!-- div:extend-table 70bc7529_7e18_47c5_9d2a_7a8b0cb0d1a8-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| sub_resp_code | 业务返回码 | String | 8 | Y | 参见[业务返回码](#业务返回码)，<font color="green">示例值：00000000</font> |
| sub_resp_desc | 业务返回描述 | String | 512 | Y | [业务返回信息](#业务返回码)，<font color="green">示例值：处理成功</font> |
| req_seq_id | 业务请求流水号 | String | 128 | Y | <font color="green">示例值：202109160899013231200005</font> |
| req_date | 业务请求时间 | String | 8 | Y | 格式：yyyyMMdd；<font color="green">示例值：20211123</font> |
| hf_seq_id | 汇付全局流水号 | String | 128 | N | <font color="green">示例值：002900TOP3A221112165433P410ac139c1300001</font> |
| trans_status | 交易状态 | String | 1 | N | S:成功；F:失败；P:处理中；<font color="green">示例值：S</font> |
| acct_status | 账务状态 | String | 1 | N | S:成功；F:失败；P:处理中；B:回账成功；<br/><font color="green">示例值：S</font> |
| channel_status | 通道状态 | String | 1 | N | S:成功；F:失败；P:处理中；<font color="green">示例值：S</font> |
| fee_amt | 手续费 | String | 14 | Y | 单位：元。<font color="green">示例值：1.23</font> |
| cash_amt | 取现金额 | String | 14 | Y | 单位：元。<font color="green">示例值：1.23</font> |
| msg_type | 消息类型 | String | 8 | N | 01:通道；02:账务；<font color="green">示例值：01</font> |
| payment_hf_seq_id | 原支付全局流水号 | String | 128 | N | 示例值：0030000topB230316111634P778c0a8314500000 |
| huifu_id | 取现方ID号 | String | 32 | N | 示例值：6666000109812123 |
| acct_id | 账户号 | String | 32 | N | 示例值：F00598600 |
| trans_type | 交易类型 | String | 20 | N | ENCHASHMENT-取现、TSENCHASHMENT-TS结算；<font color="green">示例值：ENCHASHMENT</font> |
| re_exchange | 退汇状态 | String | 1 | N | Y-已退汇；<font color="green">默认为空，该字段为Y时代表已退汇</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
  "resp_code": "00000000",
  "req_date": "20210916",
  "hf_seq_id": "00300TOP1GR210916200303P402ac13262200000",
  "req_seq_id": "202109160899013231200005",
  "resp_desc": "成功",
  "trans_stat": "P"
}

```


#### 业务返回码

| 返回码   | 返回描述                                                     |
| :------- | :-----------------------------------------------------------  |
| 00000000 | 受理成功                                                     |
| 10000000 | %s不能为空；如：取现卡序列号/请求流水号不能为空<br />%s长度固定%d位<br />%s最大长度为%d位<br />%s的传入枚举(%s)不存在<br />%s不符合xx格式 <br />%s解密失败<br />注：%s代指报错参数名，%d代指字段长度 |
| 22000000 | 产品号不存在                                                 |
| 22000000 | 产品号状态异常                                               |
| 20000000 | 重复交易                                                     |
| 22000002 | 商户信息不存在                                               |
| 22000002 | 商户状态异常                                                 |
| 22000003 | 账户信息不存在                                               |
| 22000004 | 暂未开通取现权限                                             |
| 22000003 | 手续费账户信息不存在                                         |
| 22000005 | 取现卡序列号信息不存在                                     |
| 22000005 | 手续费费率未配置                                             |
| 22000005 | 手续费计算错误                                               |
| 23000003 | 取现金额不足以支付内扣手续费                                 |
| 23000004 | 延迟户不可作为取现出账方     充值户不可作为取现出账方        |
| 23000004 | 延迟户不能作为手续费承担方                                   |
| 90000000 | 交易存在风险                                                 |
| 90000000 | 业务执行失败                                                 |
| 90000000 | 部分成功（交易中间态） |
| 98888888 | 系统错误                                                     |

