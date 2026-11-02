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
## 用户申请单状态查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/apply/query

*最近更新时间：2026.09.24*
### 应用场景
查询用户非同名对公结算卡审核信息。

**适用对象**   
  斗拱服务商或商户；

### 接口说明 
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)


### **公共参数**

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
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/customers/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                              

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属**用户ID**；<font color="green">示例值：6666000123120000</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号（业务申请编号），同一商户号当天唯一，<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220905</font> |
| apply_no | 申请单号 | String | 18 | Y | 汇付返回的申请单号；<font color="green">示例值：2024022934731647</font> |


#### 请求示例

```json
{  
    "sys_id":"6666000123710608",  
    "product_id":"SPIN",  
    "data":{  
        "apply_no":"2024022934731647",  
        "huifu_id":"6666000146954398",  
        "req_date":"20231206",  
        "req_seq_id":"rQ20240228070205559168"  
    },  
    "sign": "AHTW/j+t2Y2pjjfdaP8Fqbl/ryiMHCjKnZvakP1JfxRInc7z3RMflIFS+0jTAsTVT0GMO4Dzf/o55rslD/pFlrmZqxmYByC/6rjXOy5SmfdkRNM75gpJwgF7JGFfPMB4ZWPGpZmB+A60aC04s3ujDeZxSbn0Q9IkuPSeAuAHToY="
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| apply_reason | 审核意见 | String | 512 | N | 审核意见 |
| apply_status | 申请单审核状态 | String | 1 | N | Y:审核通过 P:审核中 N审核拒绝 F:系统处理失败；<font color="green">示例值：Y</font> |
| huifu_id | 用户号 | String | 18 | N | 汇付分配的用户号；<font color="green">示例值：6666000123120000</font> |
| <span class="extend a38cfe88_1765_433e_afad_aa4ccbf5af87">agreement_info_list</span> | 协议信息 | String |  | N | 签署电子协议时返回 jsonArray格式 |

<!-- extend:start -->
<!-- div:extend-table a38cfe88_1765_433e_afad_aa4ccbf5af87-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_id | 协议编号	 | String | 64 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：313710350701485557</font> |
| agreement_name | 协议名称	 | String | 256 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：斗拱平台用户支付服务协议</font> |
| con_stat | 合同状态	 | String | 2 | N | 电子协议类型会返回以下值：<br>2：创建合同异常<br>3：待签约<br>4：签约中<br>5：签约完成(电子协议只有签约完成才能做交易)<br>6：已失效<br>7：已拒签<br>8：签约失败<br><font color="green">示例值：5</font> |
| agreement_type | 协议类型	 | String | 1 | N | 0-电子协议 |
| agreement_link | 协议签署连接	 | String | 1024 | N | 申请实名且签署电子协议时返回；<font color="green">示例值：https://sl.integrationtest.cloudpnr.com/TsK8e649</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{  
    "data": {
        "apply_reason": "",
        "resp_desc": "成功",
        "resp_code": "00000000",
        "apply_status": "Y",
        "agreement_info_list": "[{\"agreement_id\":\"313710350701485557\",\"agreement_link\":\"https://sl.integrationtest.cloudpnr.com/TsK8e649\",\"agreement_name\":\"斗拱平台用户支付服务协议 V1.0 20260905\",\"agreement_type\":\"0\",\"con_stat\":\"5\"}]",
        "huifu_id": "6666000109507317"
    },  
    "sign":"hl+Bv+zKXsZ+Dk3PSjUsLXMlEeoc25VBNFOcAnu5riQ0TPBEJ4KPKboQZk9hFi8DqMF05D2qowaEnla2DbKIiRpx0wOKJhoCiS1F+PiD0H08UZPhWsfjmQsgYG3O4IrTgKsLbL0YGBBHAL9Xujx7vGrxTvaCGO4aH8Hx+3+iIHZubMllXLYsQzeux31piOZY9FBEnb+OcWIFWdUnCwi3LHdioK/HeXgylz7loKp0dGUlXrpyfh4cwJ2g6/DDzxkSGmWA8rRDmk0QiMMre8lwLGZ8GzBrhL5wcxnhW/Nwtv77ognpOZAcRjJmTM/KWRHYHx5Xy6bj2YJhXhtFBaH6cA=="  
}
```
