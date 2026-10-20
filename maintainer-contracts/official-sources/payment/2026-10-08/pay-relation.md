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
## 付款关系提交

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/payrelation/apply

*最近更新时间：2025.02.25*
### 应用场景
本接口适用于须预先维护付款关系后才可正常发起余额支付的商户。

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
| out_huifu_id | 出款方商户号 | String | 32 | Y | <font color="green">示例值：6666000109812123</font> |
| req_date | 请求日期 | String | 8 | Y | 格式为YYYYMMDD，<font color="green">示例值：20221023</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | <font color="green">示例值：2021091708126665001</font> |
| <span class="extend a4340f0d_9f43_4de0_910e_c4522943e67d">pay_relations</span> | 付款关系明细 | String |  | Y | 付款关系，jsonArray |

<!-- extend:start -->
<!-- div:extend-table a4340f0d_9f43_4de0_910e_c4522943e67d-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| in_huifu_id | 入账方商户号 | String | 32 | Y | <font color="green">示例值：6666000109812123</font> |
| apply_type | 操作类型 | String | 3 | Y | ADD:新增；DEL:删除；<font color="green">示例值：ADD</font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000108854952",
    "product_id": "SPIN",
    "data": {
        "req_seq_id": "202403180012100005",
        "req_date": "20240318",
        "out_huifu_id": "6666000105253412",
        "pay_relations": [
            {
                "in_huifu_id": "6666000104558835",
                "apply_type": "ADD"
            },
            {
                "in_huifu_id": "6666000104633243",
                "apply_type": "DEL"
            }
        ]
    },
    "sign": "Du47+1HbFq7PYJzJw3PYYrRbJzyuMFG84RwzDwehGFbGy6H1KJSWwrd0TPO2nyk3TZM7p92DIasQAnFd/S9ztNCbHN+C+8W6yt0FHAtv7i6FuAefi1pYvS601bvGdVQf9qPEuPrmTriHmtF/vXImKMacK96bpbuVgaYFLew//v7HxwSgDUWq7yT5nC2Q+MpOS6M/RrQfMwopUBTKfvrkx6dc/B+nLoDwuZ5sJ6NxZieXzRsiadUAv9AQeupcG1ZjUBH3hH4ZrjIhM1UW85Ij23lqP4UtDlDKWTRlMgBeS7YySAYJhz6ab8lpi02r8ed6n7PvHMYoo4jVm6h8Ky6fRw=="
}
```
### 返回参数


#### 同步响应参数

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](#业务返回码)  ；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](#业务返回码)；<font color="green">示例值：交易成功</font> |
| req_date | 请求日期 | String | 8 | Y | 格式为YYYYMMDD，<font color="green">示例值：20221013</font> |
| req_seq_id | 业务请求流水号 | String | 128 | Y | <font color="green">示例值：2022082408452985319884</font> |
| out_huifu_id | 出款方商户号 | String | 32 | Y | <font color="green">示例值：6666000108854952</font> |
| <span class="extend 5d85c2df_d3e1_496e_aa8b_4a36855bff84">pay_relations</span> | 付款关系明细 | String |  | Y | 付款关系，jsonArry |
| confirm_url | 付款关系确认页面URL | String | 128 | N | <font color="green">示例值：https://spin-test.cloudpnr.com/balance/?hfSeqId=0035000topB240314153727P590c0a8309800000</font> |

<!-- extend:start -->
<!-- div:extend-table 5d85c2df_d3e1_496e_aa8b_4a36855bff84-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| in_huifu_id | 入账方商户号 | String | 32 | Y | <font color="green">示例值：6666000123123123</font> |
| apply_type | 操作类型 | String | 3 | Y | ADD:新增；DEL:删除；<font color="green">示例值：ADD</font> |
| in_mer_name | 入账方商户名称 | String | 128 | N | <font color="green">示例值：上海汇付支付服务公司</font> |
| apply_stat | 提交状态 | String | 1 | Y | S=成功；F=失败；<font color="green">示例值：S</font> |
| apply_desc | 提交状态描述 | String | 32 | N | <font color="green">示例值：待删除入账方不在付款关系中</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "confirm_url": "https://spin-test.cloudpnr.com/balance/?hfSeqId=0035000topB240314153727P590c0a8309800000",
        "out_huifu_id": "6666000105253412",
        "pay_relations": "[{\"apply_stat\":\"S\",\"apply_type\":\"ADD\",\"in_huifu_id\":\"6666000104558835\",\"in_mer_name\":\"商户注册1\"},{\"apply_desc\":\"待删除入账方不在付款关系中\",\"apply_stat\":\"F\",\"apply_type\":\"DEL\",\"in_huifu_id\":\"6666000104633243\"}]",
        "req_date": "20240314",
        "req_seq_id": "20211710401847",
        "resp_code": "00000100",
        "resp_desc": "付款关系提交成功，等待确认"
    },
    "sign": "gWt0tyu/dOsU0mizxnV+DowPn77a2EMdmNpO4P6QhMOE2zGiY1l1VOP9if7Xez7XPKPACyJDYMNT48HMxHBqcefWHwn1Dj6/EEp4HCXqdMilIaK67jvP7wmsmPYhWG8bm7dGZNMFkHizAE4YGG1eNYdUZ3PR8ZAh1fkOsFkIQyatxv0e1mSIRRtj62kdx97dnmxd7IUgeng8tbrdTk/UiTOm5ItlJ0Z0jt9DUPDWMuESLyKfP+fQJdHFdMTZkqQHVoCLn4t7sW9XXTB1zyiFkyDeMHkInk7tF2w979p6oxb4sYPLkCxskwCfraz2YhRv+v01ByN4wn5DjLl4zLw0tQ=="
}
```
