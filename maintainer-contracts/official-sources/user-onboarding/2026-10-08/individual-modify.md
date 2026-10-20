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
## 个人用户基本信息修改

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/basicdata/indv/modify

*最近更新时间：2026.09.04*
### 应用场景
使用本接口可完成个人用户信息修改，可用于维护分账用户，快捷交易用户等。

**适用对象**    
  渠道商或商户开通的个人用户

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
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | 请求流水号，同一商户号当天唯一；<font color="green">示例值：2022012614120615001</font> |
| req_date | 请求日期 | String | 8 | Y | 日期格式：yyyyMMdd，以北京时间为准；<font color="green">示例值：20220125 </font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 当前用户的huifu_id；<font color="green">示例值：6666000123123123</font> |
| cert_validity_type | 个人证件有效期类型 | String | 1 | N | 1:长期有效；0:非长期有效；<font color="green">示例值：0</font> |
| cert_begin_date | 个人证件有效期开始日期 | String | 8 | N | 日期格式：yyyyMMdd  <font color="green">示例值：20220125 </font> |
| cert_end_date | 个人证件有效期截止日期 | String | 8 | N | 日期格式：yyyyMMdd;  长期有效时可不填；<font color="green">示例值：20220125 </font> |
| email | 电子邮箱 | String | 64 | N | 电子邮箱；<font color="green">示例值：carl.chen@huifu.com </font> |
| mobile_no | 手机号 | String | 11 | N | 手机号，11位数字 <font color="green">示例值：13917145190 </font> |
| <span class="extend cfff4e1f_af2f_41b2_ba99_554f5d7c21dd">file_list</span> | 文件列表 | String |  | N | jsonArray格式 |
| address | 地址 | String | 256 | N | 开通中信E管家必填；开通电子回单必填 |
| mcc | 所属行业 | String | 7 | N | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；<font color="green">示例值：5311</font>；<br/>当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| prov_id | 省 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> ；如修改省市区要级联修改；<br/>当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| area_id | 市 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font> ；如修改省市区要级联修改；<br/>当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| district_id | 区 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310101</font> ；如修改省市区要级联修改；<br/>当用户业务入驻修改，电子回单配置开关为开通时，需填写 |

<!-- extend:start -->
<!-- div:extend-table cfff4e1f_af2f_41b2_ba99_554f5d7c21dd-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 8 | Y | 请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx) |
| file_id | 文件jfileID | String | 64 | Y | 调[商户图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)时返回的文件id；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_name | 文件名称 | String | 64 | N | 格式：图片名.jpg；<font color="green">示例值：营业执照.jpg </font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "data": {
        "req_seq_id": "rQ2022081604155873074160844394",
        "req_date": "20220816",
        "huifu_id": "6666000103854106",
        "cert_validity_type": "1",
        "cert_begin_date": "20200111",
        "cert_end_date": "20400111",
        "email": "jeff.peng@huifu.com",
        "mobile_no": "15556622000"
    },
    "product_id": "JCTEST",
    "sys_id": "ssproxy_dev",
    "sign": "AqMS69SpVvtzFj6z8yjBaYqEUhH6dWuchbnFSkE6OSCBwbb8FRQBR+F+cbM1j5FCuk3dWaa1WpUiqXlwPjT8OtuHYa5pB3pRgC3px+8A1833C/a4RUIj+DVYwFfbOQrORgS9BHzZlG6hKkJoTSoDAyeAKSbbT9/TEDgQubizHPQ="
}

```
### 返回参数


#### 成功

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 返回码 | String | 8 | Y | [交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 返回描述 | String | 512 | Y | [交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| huifu_id | 汇付ID | String | 18 | N | <font color="green">示例值：6666000123123123</font> |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_desc": "成功",
        "resp_code": "00000000",
        "huifu_id": "6666000103850526"
    },
    "sign": "HaiZ1R4DW1XzukHFeOkfbO4IyTpZF7l8wkjJD9zX12G9ewFiKArMUWZJVY0K7wyKf0aDAEPHSuqFFQJ8XGVZaszT26J3GzUXHLgtegDz3tsbPog25Yne2pHCUtJogSr/jaXFbEHHahdEmj8R3vVd5FTnzCxpExyCeP0ZiPNmMwGGZn8HsrL/S7kFP2k1Gk02HTXdcm0GdwrfDbpNH/AEg8riOsYo7yYjfRmAXbIpvKmw/EampDPxrNGIedmyuQyPLfyCN3NiqZWcXyYjd4Ka1TuFJR07GNicBhEe0ggyNYt8zdevVAHCOsRnFklOCon+/EF4kb3PpQDTjb//TLpdGw=="
}
```
