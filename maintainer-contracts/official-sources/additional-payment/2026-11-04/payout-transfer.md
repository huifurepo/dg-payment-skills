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
## 银行卡代发

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/settlement/surrogate

*最近更新时间：2026.07.09*
### 应用场景
商户从汇付账户代发至指定银行卡中。代发资金需先通过控台充值/调用[网银充值接口](https://paas.huifu.com/open/doc/api/#/wy/api_wypc)充值至商户基本户。    
[出金交易查询接口](http://paas.huifu.com/open/doc/api/#/jyjs/qx/api_cjjycx)可以查询代发交易记录。

**适用对象**  
商户需开通代发功能权限。

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
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：2021091708126665001</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20211123</font> |
| huifu_id | 商户号 | String | 32 | Y | 斗拱分配的商户号，<font color="green">示例值：6666000109812000</font> |
| acct_id | 账户号 | String | 32 | N | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，<font color="green">示例值：F00598600</font> |
| cash_amt | 代发金额 | String | 14 | Y | 单位元，需保留小数点后两位，<font color="green">示例值：5.00</font> |
| purpose_desc | 代发用途描述 | String | 255 | Y | <font color="green">示例值：退款</font> |
| province | 省份 | String | 4 | C | 选填，参见[代发省市地区码](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/area/%E6%96%97%E6%8B%B1%E4%BB%A3%E5%8F%91%E7%9C%81%E4%BB%BD%E5%9C%B0%E5%8C%BA%E7%BC%96%E7%A0%81.xlsx)；<font color="green">示例值：0013</font><br/>对公代发(省份+地区)与联行号信息二选一填入；对私代发非必填； |
| area | 地区 | String | 4 | C | 选填，参见[代发省市地区码](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/area/%E6%96%97%E6%8B%B1%E4%BB%A3%E5%8F%91%E7%9C%81%E4%BB%BD%E5%9C%B0%E5%8C%BA%E7%BC%96%E7%A0%81.xlsx)；<font color="green">示例值：1301</font><br/>对公代发(省份+地区)与联行号信息二选一填入；对私代发非必填； |
| bank_code | 银行编号 | String | 8 | C | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)； <font color="green"><br/> 选填 ，card_acct_type=E 时必填， 示例值：01040000</font> |
| correspondent_code | 联行号 | String | 30 | C | 选填，参见：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) <font color="green">示例值：102290026507</font><br/>对公代发(省份+地区)与联行号信息二选一填入；对私代发非必填； |
| subbranch_bank_name | 支行名 | String | 60 | N | <font color="green">示例值：中国工商银行股份有限公司上海市中山北路支行</font> |
| bank_account_name | 银行卡用户名 | String | 60 | Y | <font color="green">示例值：上海汇付支付服务公司</font> |
| card_acct_type | 对公对私标识 | String | 1 | Y | 对公:E，对私:P；<font color="green">示例值：E</font> |
| bank_card_no_crypt | 银行账号密文 | String | 512 | Y | 使用斗拱系统的公钥对银行账号进行RSA加密得到秘文；<br/><font color="green">示例值：b9LE5RccVVLChrHgo9lvp……PhWhjKrWg2NPfbe0mkQ==</font> |
| certificate_no_crypt | 证件号密文 | String | 512 | Y | 使用斗拱系统的公钥对证件号进行RSA加密得到秘文；<br/><font color="green">示例值：b9LE5RccVVLChrHgo9lvp……PhWhjKrWg2NPfbe0mkQ</font> |
| certificate_type | 证件类型 | String | 2 | C | 对私必填，类型<br/>01：身份证<br/>03：护照（国内）<br/>09：外国人居留证<br/>15：港澳台居住证<br/>16：回乡证<br/>17：台胞证<br/> |
| into_acct_date_type | 到账日期类型 | String | 3 | Y | T0：当日到账； T1：T1次工作日到账； D1：次自然日到账；<font color="green">示例值：T1</font> |
| notify_url | 异步通知地址 | String | 128 | N | 接受异步通知的http服务地址，<font color="green">示例值：http://www.service.com/getresp</font> |


#### 请求示例

```json
{
  "sys_id": "6666000109812000",
  "product_id": "HFPAY",
  "data": {
    "req_seq_id": "7091d516-95f8-4ef2-86c4-30b6c4ee560e",
    "req_date": "20220825",
    "huifu_id": "6666000000041651",
    "cash_amt": "9.00",
    "purpose_desc": "v2测试用",
    "province": "0278",
    "area": "2619",
    "bank_code": "01020000",
    "correspondent_code": "correspondentCode",
    "subbranch_bank_name": "subbranchBankName",
    "bank_account_name": "王大锤",
    "card_acct_type": "E",
    "bank_acct_three_in_one": "dfa",
    "bank_card_no_crypt": "fM3G4fV8dfyA9GvSPckj7DM/0ZPgIuTrCj5chjRP2np/j+5xBkDp+hGLSskALgMijL837blhwVwfpPstkR2t+0aLtRLC1IpggVKKbNefoqcahF2a4zh+YssAulOoQ6T7DDWTjaa0qzILmLV+J/CCW6ioE+pdsBlGKee7Cc0iD6VqAjkSmnx2kWadz9CpaH8ayvyivdkc87SHsSgexQ5scyZdkGYSpXtRf/rSTcfsf5Q3NP+uKA6lJ0hnESiCw/1POoszJrSlGT2U7jpQLDWVENKcW06bReKxQuAdxFaX4DqkwbQeN5nzHvYh14IU8KrZZDAoiCx12x+IcHIVB2tBmw==",
    "certificate_no_crypt": "cw8BlH40+weHiFnIonCiSak1wWeCiRWpMF1cBHhuE+vagzKT37MRvouVboLnaWwIry3joQOoVJipDTPpzAMGVrbLQTdtZoHhgyynnD3MS0NTPch2W4i9dO3/ikLylbs2HitUlCThXEX7DIrIbLLYZ7zzeYUyXAs6dKlehMNxAaF4utJpxV84tB3ZmCKKFairE6+al4Id+/c7536G0j5lKn7lWSawl8A1UEbMMmHFvydGEBgaCAmvu0WEx7llhtPl1GpJnwqieAt9u+lM0cjUGEYfw54/JnmEF3uVuHqjco/EAMKmWiqONqCT4ptBLlOiT15FUejK0iFiUrS0Y3ytMg==",
    "certificate_type": "01",
    "mobile_no_crypt": "Uc2rjt3iqQMIjUubLKvrE4ynG2XoZDXl4sSqHB7xFvz6EyhS+WMm+tp7WLzG97PqdsmlfURRLjmSR3u98Zz0HV7wO4zvUwdOMzA1rX2Ab9Cz6eKHBWwkRpEn8zmq3KdsHpifKd5y6/MuEyXJ6tdKjBrmXTn3Ut6goz+yhUcPbvV4HEMCybRmF9YTvblb7Yk8trMHjOkq6J6EIEfQL3X07WTNpseCtuYF/j5tNws4boezEmOnS2hNkneMR+OfRaZ6UndFAMHd/Lj9fY2mscpPnWNACtmsD2nh0Z8ziwzCYnYAH2EV988cSq2vi3fkgCtd5b8zNGp+XJBefPaK7Vcp+w==",
    "into_acct_date_type": "T0",
    "notify_url": "http://www.gangcai.com",
    "risk_check_data": "{\"subUserType\":\"02\"}"
  },
  "sign": "PRTcr5o2oF2UdXNU7o9vglrkOn4b08VZ3DdLhxL76z1Zml+CFLXpbXR8xIWeTFmOhXm95vSxG/mKXR5fWxaznh6FDVQdNx/CxLfrRhX4VfcLNLTlqtEZ99zZDrD/BPzA16cAdVVnolMbMqv6xXEra+GFGtxcjOyvoRzcdSAWdOo="
}

```
### 返回参数


#### 同步响应参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| hf_seq_id | 全局流水号 | String | 128 | Y | <font color="green">示例值：0030default220825182711P099ac1f343f00000</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：2022012614120615001</font> |
| resp_code | 业务返回码 | String | 8 | Y | 参见[业务返回码](#业务返回码)，<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回信息](#业务返回码)，<font color="green">示例值：受理成功</font> |
| trans_stat | 交易状态 | String | 1 | Y | S：成功 F：失败 P：处理中；<font color="green">示例值：P</font> |


#### 异步响应参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | 固定返回码，<font color="green">示例值：10000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回信息](#业务返回码)；<font color="green">示例值：处理成功</font> |
| <span class="extend a0c75335_ee19_4a54_a897_b3dc47b723c9">resp_data</span> | 业务返回参数 | String |  | N | json格式； |
| sign | 签名 | String | 255 | Y | 签名，对报文整体签名 |

<!-- extend:start -->
<!-- div:extend-table a0c75335_ee19_4a54_a897_b3dc47b723c9-table -->
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
| re_exchange | 退汇状态 | String | 1 | N | Y-已退汇；<font color="green">默认为空，该字段为Y时代表已退汇</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "hf_seq_id": "0030default220825182711P099ac1f343f00000",
        "req_date": "20220825",
        "req_seq_id": "7091d516-95f8-4ef2-86c4-30b6c4ee560e",
        "resp_code": "00000000",
        "resp_desc": "受理成功",
        "trans_stat": "P"
    }
}
```


#### 业务返回码

| 返回码      | 返回描述                                                                                                      |
|:---------|:--------------------------------------------------------------------------------------------------------|
| 10000000 | %s不能为空<br/>%s长度固定%d位<br/>%s最大长度为%d位<br/>%s的传入枚举(%s)不存在<br/>%s不符合xx格式<br/>%s解密失败<br/>注：%s代指报错参数名，%d代指字段长度  |
| 22000000 | 产品号不存在                                                                                                    |
| 22000000 | 产品号状态异常                                                                                                   |
| 20000000 | 重复交易                                                                                                      |
| 22000002 | 商户信息不存在                                                                                                   |
| 22000002 | 商户状态异常                                                                                                    |
| 22000005 | 银行卡序列号信息不存在                                                                                               |
| 22000003 | 账户信息不存在                                                                                                   |
| 23000004 | 延迟户不可作为代发出账方 充值户不可作为代发出账方                                                                                 |
| 22000004 | 暂未开通代发权限                                                                                                  |
| 22000003 | 手续费账户信息不存在                                                                                                |
| 23000004 | 延迟户不能作为手续费承担方                                                                                             |
| 22000005 | 手续费费率未配置                                                                                                  |
| 22000005 | 手续费计算错误                                                                                                   |
| 23000003 | 代发金额不足以支付内扣手续费                                                                                            |
| 90000000 | 交易存在风险                                                                                                    |
| 00000000     | 受理成功                                                                                                      |
| 90000000 | 业务执行失败 |
| 90000000 | 部分成功（交易中间态） |
| 98888888 | 系统错误                                                                                                      |

