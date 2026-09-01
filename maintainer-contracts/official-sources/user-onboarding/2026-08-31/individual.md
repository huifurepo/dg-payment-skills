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
## 个人用户基本信息开户

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/basicdata/indv

*最近更新时间：2026.08.25*
### 应用场景
服务商或商户为旗下的个人用户开户，开户后该用户可使用多方分账及结算功能。

**适用对象**   
  需要为旗下个人用户开户的服务商或商户

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


### **注意** 
- [file_list]：证件类型是身份证的，会做姓名与身份证号的实名认证；


### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_seq_id | 请求流水号 | String | 32 | Y | <font color="green">示例值：rQ2021121311173944134649875651</font> |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220905</font> |
| name | 个人姓名 | String | 32 | Y | <font color="green">示例值：张三</font> |
| cert_type | 个人证件类型 | String | 2 | Y | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；<font color="green">示例值：00</font> |
| cert_no | 个人证件号码 | String | 32 | Y | <font color="green">示例值：320926198312024023</font> |
| cert_validity_type | 个人证件有效期类型 | String | 1 | Y | 1:长期有效 0:非长期有效；<font color="green">示例值：0</font> |
| cert_begin_date | 个人证件有效期开始日期 | String | 8 | Y | 日期格式：yyyyMMdd；<font color="green">示例值：20220909</font> |
| cert_end_date | 个人证件有效期截止日期 | String | 8 | N | 日期格式：yyyyMMdd; <font color="green">示例值：20330909</font> ；长期有效时可不填，非长期有效必填 |
| cert_nationality | 个人国籍 | String | 50 | C | 个人证件类型为外国人居留证时，必填，参见《[国籍编码](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/area/%E5%9B%BD%E7%B1%8D.xlsx)》<font color="green">示例值：CHN</font> |
| mobile_no | 手机号 | String | 11 | Y | <font color="green">示例值：13917354627</font> |
| email | 电子邮箱 | String | 64 | N | <font color="green">示例值：carl.chen@huifu.com</font> |
| login_name | 管理员账号 | String | 32 | N | <font color="green">示例值：Lg2022022201394910571</font> |
| sms_send_flag | 是否发送短信标识 | String | 1 | N | Y:发送短信通知，N：不发送短信通知。默认不发送短信通知。<font color="green">示例值：Y</font> |
| expand_id | 拓展方字段 | String | 18 | N | 如果该商户是第三方展业的可以填写拓展方的huifu_id;<font color="green">示例值：6666000123123123</font> |
| <span class="extend 1d983068_3bcd_43e6_b57a_414597cfea3f">file_list</span> | 文件列表 | Object |  | N | jsonArray格式 |
| address | 地址 | String | 256 | C | 开通中信E管家必填；开通电子回单必填 |
| mcc | 所属行业 | String | 7 | N | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；<font color="green">示例值：5311</font>；<br/>当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| prov_id | 省 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> ；如修改省市区要级联修改；<br/>当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| area_id | 市 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310100</font> ；如修改省市区要级联修改；<br/>当用户业务入驻修改，电子回单配置开关为开通时，需填写 |
| district_id | 区 | String | 6 | N | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310101</font> ；如修改省市区要级联修改；<br/>当用户业务入驻修改，电子回单配置开关为开通时，需填写 |

<!-- extend:start -->
<!-- div:extend-table 1d983068_3bcd_43e6_b57a_414597cfea3f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 8 | Y | 参见[文件类型](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；<font color="green">示例值：F85</font> |
| file_id | 文件jfileID | String | 128 | Y | [图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)生成的fileId；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_name | 文件名称 | String | 128 | N | <font color="green">示例值：test42001.jpg</font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "6666000123120000",
    "data": {
        "req_seq_id": "rQ2022022201394949297117235403",
        "req_date": "20220222",
        "name": "个人用户名称3657",
        "cert_type": "00",
        "cert_no": "321084198912066512",
        "cert_validity_type": "1",
        "cert_begin_date": "20200117",
        "cert_end_date": "20400117",
        "mobile_no": "13764462205",
        "email": "jeff.peng@huifu.com",
        "login_name": "Lg2022022201394910571",
        "sms_send_flag": "Y",
        "expand_id": "",
        "file_list": [
            {
                "file_id": "2022022201394949297117211",
                "file_name": "企业营业执照1.jpg",
                "file_type": "F04"
            }
        ]
    },
    "sign": "RK2hWGe7HSDH4Vkr5M+Uazia306qA9ATD+qOXaQMpSdp5AmQN0egWbFc2m2yuGFuPrC46AessYL5yt2BHG/DuJ4+SvywesfU8C/znzN2s4x5oGLJZ0Hv36Ry915MX2yJhL3tWqiNOgmMxsFkiM8LxBRmXzgMbtZ0yBqaa5CMN68=",
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
| login_name | 管理员账号 | String | 32 | N | <font color="green">示例值：Lg2022022201394910571</font> |
| login_password | 管理员密码 | String | 18 | N | 传login_name的时候要返回初始密码；<font color="green">示例值：cwqq304903</font> |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "resp_desc": "成功",
        "resp_code": "00000000",
        "huifu_id": "6666000104482986",
        "login_name": "Lg2022022201394910571",
        "login_password": "Bb4agbdg"
    },
    "sign": "HaiZ1R4DW1XzukHFeOkfbO4IyTpZF7l8wkjJD9zX12G9ewFiKArMUWZJVY0K7wyKf0aDAEPHSuqFFQJ8XGVZaszT26J3GzUXHLgtegDz3tsbPog25Yne2pHCUtJogSr/jaXFbEHHahdEmj8R3vVd5FTnzCxpExyCeP0ZiPNmMwGGZn8HsrL/S7kFP2k1Gk02HTXdcm0GdwrfDbpNH/AEg8riOsYo7yYjfRmAXbIpvKmw/EampDPxrNGIedmyuQyPLfyCN3NiqZWcXyYjd4Ka1TuFJR07GNicBhEe0ggyNYt8zdevVAHCOsRnFklOCon+/EF4kb3PpQDTjb//TLpdGw=="
}

```
