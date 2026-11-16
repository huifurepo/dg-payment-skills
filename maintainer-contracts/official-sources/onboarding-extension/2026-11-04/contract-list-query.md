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
## 协议申请列表查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/agreement/apply/list

*最近更新时间：2026.09.22*
### 应用场景
协议申请列表查询。

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

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准； |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号，同一商户号当天唯一； |
| huifu_id | 汇付商户号 | String | 32 | Y | <font color="green">示例值：6666000109812123</font> |
| agreement_id | 协议编号 | String | 32 | N | <font color="green">示例值：202505210201439711</font> |
| scene_code | 场景类型 | String | 32 | N | MER_REGIST-商户入驻，MER_MODIFY-商户变更，MER_KYC-商户聚合<font color="green">示例值：MER_REGIST</font> |
| sign_status | 协议状态 | String | 32 | N | WAIT_SIGN-待签约</br>SIGNING-签约中</br>SIGN_SUCCESS-签约完成</br>EXPIRE_SIGN-失效</br>SIGN_REJECT-已拒签</br>SIGN_FAIL-签约失败<font color="green">示例值：SIGN_FAIL</font> |
| order_id | 申请单号 | String | 32 | N | <font color="green">示例值：2023062011543931</font> |
| mer_name | 商户名称 | String | 128 | N | <font color="green">示例值：中国建筑工程总公司</font> |
| agreement_type | 协议类型 | String | 18 | Y | ELECT-电子 |
| page_num | 当前页 | String | 10 | Y | <font color="green">示例值：1</font> |
| page_size | 分页大小 | String | 10 | Y | <font color="green">示例值：10</font> |
| product_id | 产品号 | String | 32 | N | <font color="green">示例值：CYL</font> |


#### 请求示例

```json
{
  "product_id": "SPIN",
  "sys_id": "6666000003099901",
  "data": {
    "req_seq_id": "2024042512345673329",
    "req_date": "20240425",
    "scene_code":"MER_KYC",
    "huifu_id": "6666000103334211",
    "agreement_id": "202505210201439711",
    "agreement_type":"ELECT",
    "sign_status":"SIGN_SUCCESS",
    "order_id":"2025052118403054",
    "page_num":"1",
    "page_size":"10"
  },
  "sign": "bv+5P6yuqOZaErHlEDdaB3o1BoOTmiwRElDw1u9kWRksXGamVwjbZTFTv9MjvkGvv4qSqzpdQYQw8hU6IXvg1g+xR838v4PYncm/+RU+R5jPRPxvUGK01ikb4QGU/cv4sDLJ/vZsckMR3nkyJNh/a1OlFd795ZmEBjcI6AKUR4fnD8nZ3buSdjwQMXwyW73ZvtdBTpM/+Jt+FLAwGJ00mexLwfWJl/3nvLxGEFlLXLtZPgIBZlq+9oEZiyZUxfdY/Jv7U3MWQ9Wdr81hAxOyd8dxBoxeuTc++zN1jHpwdoHOfxatfV9WofLQQw5vOeQh9pPHaqM73WpyTX5OV/nbbA=="
}

```
### 返回参数


#### 同步返回参数

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |
* data

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：处理成功</font> |
| total_size | 总条数 | String | 10 | N |  |
| page_num | 当前页 | String | 10 | N |  |
| page_size | 分页大小 | String | 10 | N |  |
| <span class="extend 0a591257_8281_494d_9feb_867035d0f0c1">result_list</span> | 结果列表 | String |  | N | jsonArray格式,若无协议，该字段不返回 |

<!-- extend:start -->
<!-- div:extend-table 0a591257_8281_494d_9feb_867035d0f0c1-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| agreement_id | 协议编号 | String | 32 | N | 协议编号 |
| mer_name | 商户名称 | String | 128 | N | <font color="green">示例值：中国建筑工程总公司</font> |
| huifu_id | 商户号 | String | 32 | N | 商户号 |
| agreement_name | 协议名称 | String | 64 | N | 协议名称 |
| sign_status | 协议状态 | String | 32 | N | WAIT_SIGN-待签约,SIGNING-签约中,SIGN_SUCCESS-签约完成,EXPIRE_SIGN-失效,SIGN_REJECT-已拒签,SIGN_FAIL-签约失败 |
| sign_status_desc | 协议状态描述 | String | 32 | N | <font color="green">示例值：待签约</font> |
| create_time | 创建时间 | String | 16 | N | <font color="green">示例值：20260508184332</font> |
| start_date | 合同有效期起始日 | String | 8 | N | <font color="green">示例值：20260508</font> |
| expiration_date | 合同失效日 | String | 8 | N | <font color="green">示例值：20270508</font> |
| sign_url | 合同签署链接 | String | 128 | N | <font color="green">示例值：https://sl.integrationtest.cloudpnr.com/Jq0UcVHE</font> |
| agreement_type | 协议类型 | String | 32 | N | ELECT-电子<br><font color="green">示例值：ELECT</font> |
| agreement_type_name | 协议类型名称 | String | 500 | N | 电子<br><font color="green">示例值：电子</font> |
| download_url | 下载地址 | String | 256 | N |  |
| scene_code | 场景类型 | String | 32 | N | MER_REGIST-商户入驻、MER_MODIFY-商户变更、MER_KYC-商户聚合 |
| scene_code_desc | 场景类型描述 | String | 64 | N |  |
| order_id | 申请单号 | String | 64 | N | 申请单号 |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_desc": "成功",
        "resp_code": "00000000",
        "total_size": "10",
        "page_num": "1",
        "result_list": [
            {
                "create_time": "20260508184332",
                "sign_status_desc": "签约完成",
                "expiration_date": "20270508",
                "agreement_id": "313716190701473264",
                "scene_code_desc": "商户聚合",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "SIGN_SUCCESS",
                "agreement_name": "结算授权委托书",
                "download_url": "https://testapi.fadada.com/api/viewContract.action?app_id=400932&v=2.0&timestamp=20260508184331&contract_id=313716190701473264&msg_digest=M0U5OUNFRjhEMUVBMzdEMkE3RkNFRjIyRjg0RDIxMzk4RTc5NTJBMg==",
                "huifu_id": "",
                "scene_code": "MER_KYC",
                "mer_name": "中国建筑工程总公司",
                "order_id": "2026050819790886",
                "sign_url": "https://sl.integrationtest.cloudpnr.com/2Tm9gFQG",
                "start_date": "20260508"
            },
            {
                "create_time": "20260508184332",
                "sign_status_desc": "签约完成",
                "expiration_date": "20270508",
                "agreement_id": "313716190701473263",
                "scene_code_desc": "商户聚合",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "SIGN_SUCCESS",
                "agreement_name": "入网协议",
                "download_url": "https://testapi.fadada.com/api/viewContract.action?app_id=400932&v=2.0&timestamp=20260508184331&contract_id=313716190701473263&msg_digest=NjY5QjUxQUJGNjE1QzgxMjE5MkVBOUQ1NjM0Qzg5RThBQTNCM0EzMA==",
                "huifu_id": "6666000103977566",
                "scene_code": "MER_KYC",
                "mer_name": "中国建筑工程总公司",
                "order_id": "2026050819790886",
                "sign_url": "https://sl.integrationtest.cloudpnr.com/2Tm9gFQG",
                "start_date": "20260508"
            },
            {
                "create_time": "20260507174438",
                "sign_status_desc": "待签约",
                "expiration_date": "20270507",
                "agreement_id": "313716180701473011",
                "scene_code_desc": "商户聚合",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "WAIT_SIGN",
                "agreement_name": "结算授权委托书",
                "download_url": "https://testapi.fadada.com/api/viewContract.action?app_id=400932&v=2.0&timestamp=20260507174437&contract_id=313716180701473011&msg_digest=QTVFNzYxNjMyODQzOEI5OEZEREFCNjg0RUU1MjE1REE4QkM5QjlFNg==",
                "huifu_id": "",
                "scene_code": "MER_KYC",
                "mer_name": "中国建筑工程总公司",
                "order_id": "2026050719788512",
                "sign_url": "https://sl.integrationtest.cloudpnr.com/Jq0UcVHE",
                "start_date": "20260507"
            },
            {
                "create_time": "20260507174438",
                "sign_status_desc": "待签约",
                "expiration_date": "20270507",
                "agreement_id": "313716180701473010",
                "scene_code_desc": "商户聚合",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "WAIT_SIGN",
                "agreement_name": "入网协议",
                "download_url": "https://testapi.fadada.com/api/viewContract.action?app_id=400932&v=2.0&timestamp=20260507174437&contract_id=313716180701473010&msg_digest=NTYyM0U2NjkwNzg0QTY0MTQ2M0JEMzc5MUY5QTg0Mzc0QkQ1QjUzRA==",
                "huifu_id": "6666000103977566",
                "scene_code": "MER_KYC",
                "mer_name": "中国建筑工程总公司",
                "order_id": "2026050719788512",
                "sign_url": "https://sl.integrationtest.cloudpnr.com/Jq0UcVHE",
                "start_date": "20260507"
            },
            {
                "create_time": "20250901131838",
                "sign_status_desc": "待签约",
                "expiration_date": "20260901",
                "agreement_id": "313610120701448885",
                "scene_code_desc": "商户入驻",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "WAIT_SIGN",
                "agreement_name": "（无云账户无代发）综合支付服务协议20230816",
                "download_url": "https://testapi.fadada.com/api/viewContract.action?app_id=400932&v=2.0&timestamp=20250901131841&contract_id=313610120701448885&msg_digest=OTFFMzcyMjQ4REI4QjU1NjRDNTdEN0QxNUU5Njk4MzhEODhFRkU4Qg==",
                "huifu_id": "6666000109019630",
                "scene_code": "MER_REGIST",
                "mer_name": "高亮山",
                "order_id": "2025090118780582",
                "sign_url": "https://192.168.4.139:8074/BqUVL578j",
                "start_date": "20250901"
            },
            {
                "create_time": "20250901131745",
                "sign_status_desc": "待签约",
                "expiration_date": "20260901",
                "agreement_id": "313610120701448884",
                "scene_code_desc": "商户入驻",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "WAIT_SIGN",
                "agreement_name": "（无云账户无代发）综合支付服务协议20230816",
                "download_url": "https://testapi.fadada.com/api/viewContract.action?app_id=400932&v=2.0&timestamp=20250901131747&contract_id=313610120701448884&msg_digest=NjM5Q0E5MkJENDYyMkRGRDU1OUFCMDJBQTMyNEVBODQ2OEUzRTlBNw==",
                "huifu_id": "6666000109019628",
                "scene_code": "MER_REGIST",
                "mer_name": "高亮山",
                "order_id": "2025090118780580",
                "sign_url": "https://192.168.4.139:8074/BqUVL578i",
                "start_date": "20250901"
            },
            {
                "create_time": "20250901110606",
                "sign_status_desc": "待签约",
                "expiration_date": "20260901",
                "agreement_id": "313610120701448883",
                "scene_code_desc": "商户入驻",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "WAIT_SIGN",
                "agreement_name": "（无云账户无代发）综合支付服务协议20230816",
                "download_url": "https://testapi.fadada.com/api/viewContract.action?app_id=400932&v=2.0&timestamp=20250901110609&contract_id=313610120701448883&msg_digest=QkI1QUM4Q0E5NUYyRkZCM0MxRjhGQzUwN0NBMEM1N0JCMTY2MjIwRA==",
                "huifu_id": "6666000109019531",
                "scene_code": "MER_REGIST",
                "mer_name": "高亮山",
                "order_id": "2025090118779735",
                "sign_url": "https://192.168.4.139:8074/BqUVL578h",
                "start_date": "20250901"
            },
            {
                "create_time": "20240122165905",
                "sign_status_desc": "待签约",
                "expiration_date": "20250122",
                "agreement_id": "202401220201315278",
                "scene_code_desc": "商户入驻",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "WAIT_SIGN",
                "agreement_name": "（无云账户无代发）综合支付服务协议20230816",
                "download_url": "https://testapi.fadada.com:8443/api/viewContract.action?app_id=400932&v=2.0&timestamp=20240122165909&contract_id=202401220201315278&msg_digest=N0RBMUFGQjQyNUVDM0FDQUQ4OUNENUIxRTIyQ0I2MUJBRDY1RTA5Nw==",
                "huifu_id": "6666000108013940",
                "scene_code": "MER_REGIST",
                "mer_name": "张三的店啊",
                "order_id": "2024012215247049",
                "sign_url": "https://192.168.4.139:8074/8wIkeXXSs",
                "start_date": "20240122"
            },
            {
                "create_time": "20240122133935",
                "sign_status_desc": "待签约",
                "expiration_date": "20250122",
                "agreement_id": "202401220201315240",
                "scene_code_desc": "商户入驻",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "WAIT_SIGN",
                "agreement_name": "（无云账户无代发）综合支付服务协议20230816",
                "download_url": "https://testapi.fadada.com:8443/api/viewContract.action?app_id=400932&v=2.0&timestamp=20240122133939&contract_id=202401220201315240&msg_digest=NTQzODFCMEZEQjRCNDRDMkFBOEZCMDBBRjEwM0Q4OTAzRDcyNjRGQQ==",
                "huifu_id": "6666000108013858",
                "scene_code": "MER_REGIST",
                "mer_name": "张三的店啊",
                "order_id": "2024012215246479",
                "sign_url": "https://192.168.4.139:8074/8wIkeXXrb",
                "start_date": "20240122"
            },
            {
                "create_time": "20240122100544",
                "sign_status_desc": "待签约",
                "expiration_date": "20250122",
                "agreement_id": "202401220201315233",
                "scene_code_desc": "商户入驻",
                "agreement_type": "ELECT",
                "agreement_type_name": "电子",
                "sign_status": "WAIT_SIGN",
                "agreement_name": "（无云账户无代发）综合支付服务协议20230816",
                "download_url": "https://testapi.fadada.com:8443/api/viewContract.action?app_id=400932&v=2.0&timestamp=20240122100548&contract_id=202401220201315233&msg_digest=NjZBNkE3NTZERDVCODJDQTI5MTNGNUIyMkEzNDUwQjM2QjY0RUQzNQ==",
                "huifu_id": "6666000108013650",
                "scene_code": "MER_REGIST",
                "mer_name": "张三的店啊",
                "order_id": "2024012215246291",
                "sign_url": "https://192.168.4.139:8074/8wIkeXXr5",
                "start_date": "20240122"
            }
        ],
        "page_size": "10"
    }
}

```
