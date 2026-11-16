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
## 交易确认查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v3/trade/payment/delaytrans/confirmquery

*最近更新时间：2026.06.10*
### 应用场景
商户发起交易确认请求后，可通过本接口主动查询交易确认结果。

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
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>       |
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
| org_req_date | 原请求日期 | String | 8 | Y | 格式为yyyyMMdd，<font color="green">示例值：20220905</font> |
| org_req_seq_id | 原请求流水号 | String | 128 | Y | 交易确认接口的请求流水号；<font color="green">示例值：rQ20211213119875651</font> |
| huifu_id | 商户号 | String | 32 | Y | 开户自动生成；<font color="green">示例值：6666000123123123</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "org_req_date": "20240513",
        "org_req_seq_id": "20240513105825239x0lp7ldbus4sji",
        "huifu_id": "6666000109133323"
    },
    "sign": "UtIw1WpEin8sWIbfOnqe//WrH4odiwas3G4yAssOxDQ8SVVSmZJyyhfrJNy1wI9dDMtSOj2BVMRzHedU75+HkfG0Ei2GUwkfoD7DwQ3crqbf1bMElmGCq3iC0VjDweSkxYfxFDgfO9p+bxWWI9XLaX6zaRnWI4jV9Atyw7jLqCYm5pMiq/Dfaq2qVhXbshHFrwp9RNW1xH6yWm1anjIXhPAfeTiQVRYNsFVMC8UClyvlIRywew26SMZCuINlE4R7u3wvnpQaB6SsOuvLjm23PcqmOGq8tyQKvEN6c62RhGAicaJ6TGB53NlCnFzW2T44g8u52A0hedVU2iykc5i9Pg=="
}
```
### 返回参数


#### 同步返参

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码)  ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：查询成功</font> |
| huifu_id | 商户号 | String | 32 | Y | 斗拱开户时生成；示例值:6666000109812123 |
| org_req_seq_id | 原请求流水号 | String | 128 | Y | <font color="green">示例值：2022082408452985319884</font> |
| trans_stat | 交易状态 | String | 2 | N | P：处理中、S：成功、F：失败；<font color="green">示例值：P</font> |
| unconfirm_amt | 待确认总金额 | String | 14 | N | 待确认总金额；单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| confirmed_amt | 已确认总金额 | String | 14 | N | 已确认总金额；单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| hf_seq_id | 汇付全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| <span class="extend 2c406a7b_ffba_449b_b7d6_17e5b1d9d88c">acct_split_bunch</span> | 分账对象 | String |  | N | 分账明细信息，jsonArray字符串。 |
| remark | 备注 | String | 256 | N | 请求参数里传入，返回参数里原样返回；<font color="green">示例值：备注</font> |

<!-- extend:start -->
<!-- div:extend-table 2c406a7b_ffba_449b_b7d6_17e5b1d9d88c-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| <span class="extend 37b83e7c_c854_4ca8_9c5f_cb9447b48565">acct_infos</span> | 分账明细 | Array |  | N |  |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 37b83e7c_c854_4ca8_9c5f_cb9447b48565-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| div_amt | 分账金额(元) | String | 14 | Y | 单位元，需保留小数点后两位，最低传入0.01；示例值:1.00 |
| huifu_id | 分账接收方ID | String | 32 | Y | 斗拱开户时生成；示例值:6666000109812123 |
| acct_id | 分账接收方账户号 | String | 9 | N | 示例值:F00598600 |
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
        "resp_desc": "成功", 
        "huifu_id": "6666000018328947",
        "org_req_seq_id": "202109232638806002", 
        "trans_stat": "S" 
    }, 
    "sign": "Uc/rTKXc228JF3bhRDEePuF9ROUt7JV2IDhLslsxFchMQ46CxvU8xbifXgyh7eqtY7astNLIA0YvIbdilmZOOty1ig8bJKmekUoyt36i7OsTBYrtSTaEUbBWiIGsSBuIXm9xtDRz+6ped7F6ORJCb54kCwIn5QBRYfevm6hIou/6FlXpme/izmVBh7W8kYBtIVQo3N+uZDFNQmXn0Ny37daYv2RGVBhFVcv0CI9+MpVBn9n+s8nDtp5NtjsLvv+8Op2v5zz2uprYVRgxr31ML/sXylhOa+4rBFRj+11x5Tj9vxdLPKxyvN4HPmPYNXVrHu/SM78TdgSPl9xY970wQg=="
}
```


#### 业务返回码

查看全部 [公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)

| 返回码   | 返回描述                                                     | 处理                       |
| :------- | :----------------------------------------------------------- | :-------------------------- | 
| 00000000 | 查询成功                                                     | 成功                       |
| 10000000 | 请求内容体不能为空                                           | 请求体不能为空             |
| 10000000 | %s不能为空（%s代指具体报错参数名）                           | 检查请求参数是否符合格式   |
| 10000000 | %s长度固定%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度） | 检查请求参数是否符合格式   |
| 10000000 | %s最大长度为%d位（%s代指具体报错参数名、%d代指具体报错参数值的长度） | 检查请求参数是否符合格式   |
| 10000000 | %s的传入枚举[%d]不存在（%s代指具体报错参数名、%d代指具体报错参数的值） | 检查请求参数是否符合格式   |
| 10000000 | %s不符合%d格式（%s代指具体报错参数名、%d代指具体报错参数值的格式） | 检查请求参数是否符合格式   |
| 22000000 | 产品号不存在                                                 | 请检查产品号是否存在       |
| 22000000 | 产品状态异常                                                 | 请检查产品状态             |
| 23000001 | 交易不存在                                                   | 交易不存在                 |
| 23000002 | 该交易商户号与原交易商户号不一致                             | 检查商户号是否与原交易一致 |
| 23000004 | 交易类型不支持                                               | 不支持的配置类型           |


