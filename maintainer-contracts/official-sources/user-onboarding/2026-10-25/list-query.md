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
## 用户列表查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/list/query

*最近更新时间：2026.09.04*
### 应用场景
支持通过证件号查询用户列表信息；

**适用对象**    
  通过证件号查询用户；

### 接口说明 
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)


### **公共参数**

* 公共请求参数

| 参数       | 中文名   | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :-------------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商或商户的huifu_id； <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为总部商户时，此字段填写商户huifu_id |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>                                      |
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
| legal_cert_no | 法人证件号 | String | 32 | Y | <font color="green">示例值：320926198512025019</font> |
| upper_huifu_id | 上级汇付ID | String | 18 | N | 若传入，则只查询该huifu_id下的用户信息；<br/><font color="green">示例值：6666000123120000</font> |
| req_date | 请求日期 | String | 8 | Y | 请求时间格式yyyyMMdd；<font color="green">示例值：20220905</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号；<font color="green">示例值：2022012614120615001</font> |


#### 请求示例

```json
{
    "sys_id": "6666000107737638",
    "product_id": "JCTEST",
    "data": {
        "req_seq_id": "1233245",
        "req_date": "20240418",
        "legal_cert_no": "130224198806083798"
    },
    "sign": "AHTW/j+t2Y2pjjfdaP8Fqbl/ryiMHCjKnZvakP1JfxRInc7z3RMflIFS+0jTAsTVT0GMO4Dzf/o55rslD/pFlrmZqxmYByC/6rjXOy5SmfdkRNM75gpJwgF7JGFfPMB4ZWPGpZmB+A60aC04s3ujDeZxSbn0Q9IkuPSeAuAHToY="
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| <span class="extend 573b1f26_77c3_4d70_9b96_92511e9e7f9f">user_list_info_list</span> | 用户详情列表 | String |  | N | jsonArray格式 |

<!-- extend:start -->
<!-- div:extend-table 573b1f26_77c3_4d70_9b96_92511e9e7f9f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 汇付ID | String | 18 | N | <font color="green">示例值：6666000123120000</font> |
| name | 用户名称 | String | 128 | N | <font color="green">示例值：上海汇付支付有限公司</font> |
| cust_type | 用户类型 | String | 2 | N | 1：企业用户，2：个人用户<br><font color="green">示例值：1</font> |
| upper_huifu_id | 上级汇付ID | String | 18 | N | <font color="green">示例值：6666000123120000</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "user_list_info_list": [
            {
                "cust_type": "2",
                "name": "成鹏",
                "huifu_id": "6666000108072842",
                "upper_huifu_id": "6666000107755175"
            },
            {
                "cust_type": "1",
                "name": "交通银行股份有限公司",
                "huifu_id": "6666000108013915",
                "upper_huifu_id": "6666000107755175"
            },
            {
                "cust_type": "2",
                "name": "任德奇",
                "huifu_id": "6666000108013912",
                "upper_huifu_id": "6666000107755175"
            }
        ],
        "resp_desc": "成功",
        "resp_code": "00000000"
    },
    "sign": "AHTW/j+t2Y2pjjfdaP8Fqbl/ryiMHCjKnZvakP1JfxRInc7z3RMflIFS+0jTAsTVT0GMO4Dzf/o55rslD/pFlrmZqxmYByC/6rjXOy5SmfdkRNM75gpJwgF7JGFfPMB4ZWPGpZmB+A60aC04s3ujDeZxSbn0Q9IkuPSeAuAHToY="
}
```
