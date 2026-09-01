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
## 交易分账明细查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/trans/split/query

*最近更新时间：2024.12.20*
[版本说明](https://paas.huifu.com/open/doc/guide/#/api_gxrz)

### 应用场景

商户可通过本接口查询实时/延时交易分账明细。

**适用对象**    
已开通分账功能的商户。   
注意：**只支持180天内的分账记录查询。**
  
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
| hf_seq_id | 分账交易汇付全局流水号 | String | 128 | Y | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| huifu_id | 商户号 | String | 32 | Y | 汇付分配的商户号，<font color="green">示例值：6666000108854952</font> |
| ord_type | 交易类型 | String | 20 | Y | consume：正向交易，refund：反向交易；<font color="green">示例值：consume</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "ord_type": "consume",
        "hf_seq_id": "003500TOP2B230718174911P075ac139ccf00000",
        "huifu_id": "6666000109133323"
    },
    "sign": "fpNFUVcF5FG5jfN53/cLvj0zEU/dVzHUn5N2+U4O3Lbq25F8imPFVjbjcSnk0X49zFGcVzEr4bWktRRcMGsLASk0DUeF+M6RGnSY3OTQVqmHneae7JJG4tsVs+Pxszj95Rya5nrtPNy/+GI1d91JjmQOOlzPq4kriu/PiRF+j3vq1D/OAuB2yYFPCMvKDhPaufnYCRaq0hVpUUZ8exLTjOQQUxRJCGk8mgxG4pcQj+s8Sevq3GEn0cnjqZTHtTNcb/Eoh+UxjzKSJRpOpTBB3GltqAHDKhnUfCDyVyHB1ask4bYG6qODX1aL2ZVlM15jToE2x+120EVGm0se2ug45g=="
}
```
### 返回参数


#### 返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](#业务返回码)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务响应信息 | String | 256 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：成功</font> |
| total_size | 总记录数 | String | 32 | Y | 总计返回条数，<font color="green">示例值：100</font> |
| <span class="extend 5d6bea2e_a13f_4df2_85c1_76fea0ffdf4f">split_trans_responses</span> | 分账交易列表 | Array |  | N |  |

<!-- extend:start -->
<!-- div:extend-table 5d6bea2e_a13f_4df2_85c1_76fea0ffdf4f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| req_seq_id | 请求流水号 | String | 128 | N | <font color="green">示例值：202101171122111</font> |
| req_date | 请求日期 | String | 8 | N | yyyyMMdd；<font color="green">示例值：20221023</font> |
| huifu_id | 出账方商户号 | String | 32 | N | <font color="green">示例值：6666000018328948</font> |
| in_huifu_id | 入账方商户号 | String | 32 | N | <font color="green">示例值：6666000109812123</font> |
| product_id | 产品号 | String | 32 | N | <font color="green">示例值：YYZY</font> |
| org_ord_id | 订单流水号 | String | 128 | N | <font color="green">示例值：2020022719275002429133150</font> |
| trans_ord_id | 汇付交易订单号 | String | 128 | N | <font color="green">示例值：2020022719275002429133150</font> |
| hf_seq_id | 分账交易汇付全局流水号 | String | 128 | N | <font color="green">示例值：00470topo1A211015160805P090ac132fef00000</font> |
| ord_type | 交易类型 | String | 20 | N | consume：正向交易、refund：反向交易；<font color="green">示例值：refund</font> |
| split_amt | 分账金额 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：25.00</font> |
| split_fee_amt | 分账手续费 | String | 14 | N | 单位元，需保留小数点后两位，<font color="green">示例值：1.00</font> |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | N | <font color="green">示例值：6666000109812123</font> |
| split_seq_id | 分账流水号 | String | 128 | N | <font color="green">示例值：20200227194510024291331635678</font> |
| split_type | 分账类型 | String | 20 | N | realTime：实时、delay：延时；<font color="green">示例值：delay</font> |
| trans_finish_time | 分账完成时间 | String | 14 | N | yyyyMMddHHmmss；<font color="green">示例值：20221023112345</font> |
| acct_stat | 账务状态 | String | 1 | N | P：处理中、S：成功、F：失败；<font color="green">示例值：S</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_desc": "成功",
        "resp_code": "00000000",
        "huifu_id": "6666000018328947",
        "total_size": "1",
        "split_trans_responses": "[{\"huifu_id\":\"6666000018328947\",\"in_huifu_id\":\"6666000018328948\",\"trans_ord_id\":\"2020022719275002429133150\",\"ord_type\":\"consume\",\"org_ord_id\":\"2020022719275002429133150\",\"product_id\":\"SPIN\",\"req_date\":\"20200227\",\"req_seq_id\":\"202101171122111\",\"split_amt\":\"0.03\",\"split_seq_id\":\"20200227194510024291331635678\",\"split_type\":\"delay\",\"trans_finish_time\":\"20200211294512\"}]"
    },
    "sign": "ckXkWAEcPP1gGPSr9Vx7iwmj+ikrZECjj0WeCCUwBmwG4XA8Mc0Z5rSGjHYCHaZRZNnSm8wDYVYDRLoksXzZmkUuTJJWiZV40LUD3ULVu1UWpLGqZRGxOXp44m4ltcHl80UHXy1r1vKzfdmSv4QhLqM8v97aQuVWayKvZPbCypt6mdTYHgRJGkbN/xRnP+rIyQBQVR4rha0jKPHtnYhITGixQADDHb08p2dO910QlT9awD5rhzTGEEi0fvDiIMEOBKEPxphfdzFme/QQ274vofUJ7eTFJM7GknMwqT7x6isZa2A0KW5D2k97CmmGdM8ipKavWEd995Arf0QPchyRIA=="
}
```


#### 业务返回码

查看全部 *[公共返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)*

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


