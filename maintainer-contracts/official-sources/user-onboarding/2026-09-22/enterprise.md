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
## 企业用户基本信息开户

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/basicdata/ent

*最近更新时间：2026.09.21*
### 应用场景
服务商或商户为旗下的企业用户开户，开户后该用户可使用多方分账及结算功能。

**适用对象**    
  需要为旗下企业用户开户的服务商或商户

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

| 参数 | 中文名     | 定义   | 长度 | 必填 | 说明|
| :--- | :--------- | :----- | :------- | :--- | :------------- |
| sign | 签名       | String | 512      | Y    | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| data | 响应内容体 | Json   |          | N    | 业务返回参数                                                 |


### **注意** 
- 系统会做法人姓名与身份证号的实名认证，请正确填写；
- 必填类型“C”代表条件必填；

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | <font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220905</font> |
| reg_name | 企业用户名称 | String | 128 | Y | <font color="green">示例值：上海汇付支付有限公司</font> |
| short_name | 经营简称 | String | 20 | N | 20位英文字符或10个汉字；<font color="green">示例值：汇付天下</font> |
| license_code | 营业执照编号 | String | 18 | Y | <font color="green">示例值：92650109MA79R8E308</font> |
| license_validity_type | 证照有效期类型 | String | 1 | Y | 1:长期有效 0:非长期有效；<font color="green">示例值：0</font> |
| license_begin_date | 证照有效期起始日期 | String | 8 | Y | 日期格式：yyyyMMdd；<font color="green">示例值：20220905</font> |
| license_end_date | 证照有效期结束日期 | String | 8 | C | 日期格式：yyyyMMdd; 非长期有效时必填；<font color="green">示例值：20320905</font> |
| reg_prov_id | 注册地址(省) | String | 6 | Y | <font color="green">示例值：310000</font>，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| reg_area_id | 注册地址(市) | String | 8 | Y | <font color="green">示例值：310100</font>，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| reg_district_id | 注册地址(区) | String | 12 | Y | <font color="green">示例值：310101</font>，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) |
| reg_detail | 注册地址(详细信息) | String | 256 | Y | <font color="green">示例值：上海市徐汇区宜山路700号普天信息产业园2期C5栋</font> |
| legal_name | 法人姓名 | String | 32 | Y | 32位英文字符或16个汉字；<font color="green">示例值：张三</font> |
| legal_cert_type | 法人证件类型 | String | 2 | Y | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。<font color="green">示例值：00</font> |
| legal_cert_no | 法人证件号码 | String | 20 | Y | <font color="green">示例值：320906197412025012</font> |
| legal_cert_validity_type | 法人证件有效期类型 | String | 1 | Y | 1:长期有效 0:非长期有效；<font color="green">示例值：0</font> |
| legal_cert_begin_date | 法人证件有效期开始日期 | String | 8 | Y | 日期格式：yyyyMMdd；<font color="green">示例值：20220905</font> |
| legal_cert_end_date | 法人证件有效期截止日期 | String | 8 | C | 日期格式：yyyyMMdd; 非长期有效时必填，长期有效为空；<font color="green">示例值：20320905</font> |
| legal_cert_nationality | 法人国籍 | String | 50 | C | 法人的证件类型为外国人居留证时，必填，参见《[国籍编码](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/area/%E5%9B%BD%E7%B1%8D.xlsx)》<font color="green">示例值：CHN</font> |
| contact_name | 管理员姓名 | String | 32 | Y | 32位英文字符或16个汉字；<font color="green">示例值：李四</font> |
| contact_mobile | 管理员手机号 | String | 11 | Y | <font color="green">示例值：13916536278</font> |
| contact_email | 管理员电子邮箱 | String | 64 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| login_name | 管理员账号 | String | 32 | C | 如需短信通知则必填；升级LV3必填<font color="green">示例值：Lg20220222013747</font> |
| operator_id | 操作员 | String | 32 | N | <font color="green">示例值：Lg20220222013747</font> |
| sms_send_flag | 是否发送短信标识 | String | 1 | N | 入驻成功后短信通知商户联系人，<br/> Y：发送短信通知（联系人手机号）；如需短信通知则login_name必填；<br/>N：不发送短信通知；默认；<br/><font color="green">示例值：Y</font> |
| expand_id | 扩展方字段 | String | 18 | N | 如果该商户是第三方展业的可以填写拓展方的huifu_id；<br/><font color="green">示例值：6666000123123123</font> |
| <span class="extend c9c32bf2_1c7f_4ec1_8d9b_67368273db45">file_list</span> | 文件列表 | String |  | N | jsonArray格式 |
| ent_type | 公司类型 | String | 1 | Y | 1:政府机构 2:国营企业 3:私营企业 4:外资企业 5:个体工商户 6:其它组织 7:事业单位 8:集体经济；<font color="green">示例值：2</font> |
| mcc | 所属行业 | String | 7 | N | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；<font color="green">示例值：5311</font>；当用户业务入驻修改，电子回单配置开关为开通时，需填写 |

<!-- extend:start -->
<!-- div:extend-table c9c32bf2_1c7f_4ec1_8d9b_67368273db45-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 8 | Y | 请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；<font color="green">示例值：F01</font> |
| file_id | 文件jfileID | String | 128 | Y | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font>；[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)返回的file_id字段 |
| file_name | 文件名称 | String | 128 | N | 128位英文字符或64个汉字；<font color="green">示例值：营业执照.jpg</font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "ssproxy_dev",
    "data": {
        "req_seq_id": "rQ2022022201374713975829624302",
        "req_date": "20220222",
        "reg_name": "企业商户名称8225",
        "short_name": "企业商户",
        "license_code": "20220222013747149",
        "license_validity_type": "1",
        "license_begin_date": "20200117",
        "license_end_date": "20400117",
        "reg_prov_id": "310000",
        "reg_area_id": "310100",
        "reg_district_id": "310104",
        "reg_detail": "上海市宜山路",
        "legal_name": "陈立五",
        "legal_cert_type": "00",
        "legal_cert_no": "321084198912066582",
        "legal_cert_validity_type": "1",
        "legal_cert_begin_date": "20120801",
        "legal_cert_end_date": "20300801",
        "contact_name": "小的",
        "contact_mobile": "13764462211",
        "contact_email": "jeff.peng@huifu.com",
        "login_name": "Lg2022022201374721361",
        "operator_id": "",
        "sms_send_flag": "Y",
        "expand_id": ""
    },
    "sign": "QCDaEHNEmhONTCoySTzbkpZ3UPYxWADLGVIBUBeKMfcLMz41Cvjp3BKHjpCVyzht0qEfd8VgejD4uNn/LAjfsjAJYPjml1xiqaBszd1rS0y/UmH03df5lJ6Sp36qmOMIMO7pVJdaI4tFF8dQ6N47R0R2uckd6gRK88rFCnfJZjI=",
    "product_id": "JCTEST"
}
```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| huifu_id | 汇付ID | String | 18 | N | <font color="green">示例值：6666000123123123</font> |
| login_name | 管理员账号 | String | 32 | N | <font color="green">示例值：lg20230413</font> |
| login_password | 管理员密码 | String | 18 | N | 传login_name的时候返回初始密码；<font color="green">示例值：6666000123123123</font> |


##### 返回示例

###### 成功示例
```json
{  
    "data":{  
        "login_name":"Lg2022022201374721361",  
        "login_password":"7bDeaefa",  
        "resp_desc":"成功",  
        "resp_code":"00000000",  
        "huifu_id":"6666000104482981"  
    },
    "sign": "HaiZ1R4DW1XzukHFeOkfbO4IyTpZF7l8wkjJD9zX12G9ewFiKArMUWZJVY0K7wyKf0aDAEPHSuqFFQJ8XGVZaszT26J3GzUXHLgtegDz3tsbPog25Yne2pHCUtJogSr/jaXFbEHHahdEmj8R3vVd5FTnzCxpExyCeP0ZiPNmMwGGZn8HsrL/S7kFP2k1Gk02HTXdcm0GdwrfDbpNH/AEg8riOsYo7yYjfRmAXbIpvKmw/EampDPxrNGIedmyuQyPLfyCN3NiqZWcXyYjd4Ka1TuFJR07GNicBhEe0ggyNYt8zdevVAHCOsRnFklOCon+/EF4kb3PpQDTjb//TLpdGw=="
}

```
