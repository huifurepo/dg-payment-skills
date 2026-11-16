## 商户状态变更
*最近更新时间：2024.9.1* 

### 应用场景
服务商需要发起商户状态变更时，比如对商户资金和交易做拦截场景可以调此接口。  
商户状态变更需要斗拱系统审核，可以通过[申请单状态查询接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_sqdztcx)获取状态；   
关闭后商户不能再登录斗拱控台。上级渠道、代理仍可以查询历史交易记录。  

**适用对象**  
渠道商管理商户；

### 接口说明
* 请求URL：https://api.huifu.com/v2/merchant/busi/modify/busistatus
* 请求方式：POST
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)

### 公共参数
* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                                                         |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| sys_id     | 系统号   | String | 32       | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<font color="green">示例值：6666000123120000</font> |
| product_id | 产品号   | String | 32       | Y    | 汇付分配的产品号，<font color="green">示例值：YYZY</font>       |
| sign       | 加签结果 | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data       | 数据     | Json   |          | Y    | 业务请求参数，具体值参考API文档                              |

* 公共返回参数

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明                                                         |
| :--- | :--------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |

### **请求参数**

#### Data
| 参数                | 中文名    | 定义     | 长度  | 必填 | 说明                              |
| :--------- | :------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| req_date          | 请求日期   | string | 8   | Y  | 请求时间 yyyyMMdd；<font color="green">示例值：20220921</font>                   |
| req_seq_id        | 请求流水号  | string | 32  | Y  | 请求流水号；<font color="green">示例值：2022012614120615001</font>                           |
| huifu_id| 汇付客户Id | String | 18   | Y    |渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font>|
| status            | 状态     | String | 1   | Y  | 1:开通 0:关闭；<font color="green">示例值：1</font><br/>注：支持关闭后再次打开；      |
| upd_status_reason | 状态变更原因 | String | 512 | Y  | <font color="green">示例值：注销</font> |
<!--袁佳说这个字段不要了
| <span class="extend file_list">file_list</span>         | 文件列表   | String |     | N  | jsonArray字符串，参考“file_list元素内容”  |

<!--##### file_list
<!-- extend:start 
<!-- div:extend-table file_list-table 

| 参数        | 中文名       | 定义     | 长度  | 必填 | 说明             |
| :--------- | :------- | :----- | :------- | :--- | :----------------------------------------------------------- |
| file_type | 文件类型      | String | 8   | Y  | 文件类型:参考文件类型枚举  |
| file_id   | 文件jfileID | String | 128 | Y  | 上传文件时返回的文件id；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e530</font>   |
| file_name | 文件名称      | String | 64  | N  | <font color="green">示例值：变更申请.jpg</font>           |

<!-- extend:end -->

##### 请求示例

```json
{
    "sys_id": "6666000104054032",
    "data": {
        "req_seq_id": "rQ2022040602553834979297533840",
        "req_date": "20220406",
        "huifu_id": "6666000105488078",
        "status": "0",
        "upd_status_reason": "注销"
    },
    "sign": "oar0sZGYzmhVhsCw1IrVcaPmwnRMOisHcp7ZF4uNTKZGfctUCL2ym61amT+45YLMH4ToAkBgUCkUKqipeuKoyxdIwxbPefCP12KvMiaovioHI0cnb4TxRBUCKaSgb19kD6Oq4P62HhwA1nh7fsfzqsGxntP74IPQe38gdniqDng=",
    "product_id": "JCTEST"
}
```


### 返回参数

#### **data(同步返回参数)**

| 参数        | 中文名  | 定义     | 长度  | 必填 | 说明      |
| :--------- | :------- | :----- | :------- | :--- | :------------------- |
| resp_code | 返回码  | String | 8   | Y  | [返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81)   |
| resp_desc | 返回描述 | String | 512 | Y  | [返回码描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81)  |
| apply_no  | 申请单号  | String | 128 | N  | <font color="green">示例值：2022090803023100</font>     |


#### 返回示例

```json
{
    "data": {
        "resp_desc": "审核中",
        "apply_no": "2022090803023100",
        "resp_code": "90000000"
    }
}
```
