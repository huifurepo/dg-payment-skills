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
## 企业用户基本信息修改

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/user/basicdata/ent/modify

*最近更新时间：2026.02.05*
### 应用场景
企业用户信息需要变更或修改可调用本接口完成。

**适用对象**
  服务商或商户

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


### **注意** 
- 如要修改法人证件，则legal_cert_type、legal_cert_validity_type、legal_cert_begin_date、legal_cert_end_date  必需按要求同步填写，否则校验会失败；

### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 格式yyyyMMdd；<font color="green">示例值：20220905</font> |
| req_seq_id | 请求流水号 | String | 32 | Y | <font color="green">示例值：rQ2021121311173944134649875651</font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font> |
| reg_name | 企业用户名称 | String | 128 | N | <font color="green">示例值：上海汇付支付有限公司</font>；<br/>注：修改名称前请联系汇付运营做白名单处理，否则会校验失败 |
| short_name | 经营简称 | String | 20 | N | <font color="green">示例值：汇付天下 </font> |
| ent_type | 公司类型 | String | 1 | N | 1:政府机构 2:国营企业 3:私营企业 4:外资企业 5:个体工商户 6:其它组织 7:事业单位 8:集体经济；<font color="green">示例值：2</font> |
| legal_name | 法人姓名 | String | 32 | N | <font color="green">示例值：张三 </font> |
| legal_cert_type | 法人证件类型 | String | 2 | N | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》；<font color="green">示例值：00</font> |
| legal_cert_no | 法人证件号码 | String | 32 | N | <font color="green">示例值：320936198512025017</font> |
| legal_cert_validity_type | 法人证件有效期类型 | String | 1 | N | 1:长期有效； 0:非长期有效。<font color="green">示例值：0</font> |
| legal_cert_begin_date | 法人证件有效期开始日期 | String | 8 | N | 日期格式：yyyyMMdd；<font color="green">示例值：20220905</font> |
| legal_cert_end_date | 法人证件有效期截止日期 | String | 8 | N | 日期格式：yyyyMMdd; 长期有效时可不填；<font color="green">示例值：20320905</font> |
| legal_cert_nationality | 法人国籍 | String | 50 | C | 法人的证件类型为外国人居留证时，必填，参见《[国籍编码](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/area/%E5%9B%BD%E7%B1%8D.xlsx)》<font color="green">示例值：CHN</font> |
| contact_name | 管理员姓名 | String | 32 | N | <font color="green">示例值：张三三 </font> |
| contact_email | 管理员电子邮箱 | String | 64 | N | <font color="green">示例值：carl.chen@huifu.com </font> |
| contact_mobile | 管理员手机号 | String | 11 | N | <font color="green">示例值：13918453627 </font> |
| license_validity_type | 证照有效期类型 | String | 1 | N | 1:长期有效 0:非长期有效；<font color="green">示例值：0</font> |
| license_begin_date | 证照有效期起始日期 | String | 8 | N | 日期格式：yyyyMMdd；<font color="green">示例值：20220905</font> |
| license_end_date | 证照有效期结束日期 | String | 8 | N | 日期格式：yyyyMMdd; 长期有效时可不填；<font color="green">示例值：20320905</font> |
| reg_prov_id | 注册地址(省) | String | 6 | N | 注册地址(省)，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；<font color="green">示例值：310000</font> |
| reg_area_id | 注册地址(市) | String | 8 | N | 注册地址(市)，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310100</font> |
| reg_district_id | 注册地址(区) | String | 12 | N | 注册地址(区)，请参考：[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；<font color="green">示例值：310101</font> |
| reg_detail | 注册地址(详细信息) | String | 256 | N | 汉字以2个字符计算；<font color="green">示例值：上海市徐汇区XX路XX号</font> |
| <span class="extend a4993046_fe4b_4f64_8178_70b32dc1185f">file_list</span> | 文件列表 | String |  | N | jsonArray格式 |
| mcc | 所属行业 | String | 7 | N | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；<font color="green">示例值：5311</font>；当用户业务入驻修改，电子回单配置开关为开通时，需填写 |

<!-- extend:start -->
<!-- div:extend-table a4993046_fe4b_4f64_8178_70b32dc1185f-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| file_type | 文件类型 | String | 8 | Y | 请参考：[文件类型枚举](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；<font color="green">示例值：F85</font> |
| file_id | 文件jfileID | String | 128 | Y | 参考 [商户图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 的返参file_id；<font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_name | 文件名称 | String | 128 | N | <font color="green">示例值：test42001.jpg</font> |
<!-- extend:end -->


#### 请求示例

```json
{
    "sys_id": "ssproxy_dev",
    "data": {
        "req_seq_id": "rQ2022101704445050060493042514",
        "req_date": "20221017",
        "huifu_id": "6666000103862211",
        "short_name": "企业商户测试22",
        "license_validity_type": "1",
        "license_begin_date": "20200117",
        "license_end_date": "20400117",
        "reg_prov_id": "310000",
        "reg_area_id": "310100",
        "reg_district_id": "310104",
        "reg_detail": "上海市宜山路",
        "legal_name": "陈立一",
        "legal_cert_type": "00",
        "legal_cert_no": "370684198903061000",
        "legal_cert_validity_type": "0",
        "legal_cert_begin_date": "20121010",
        "legal_cert_end_date": "20301010",
        "contact_name": "花朵",
        "contact_mobile": "13764462000",
        "contact_email": "chang@huifu.com",
        "file_list": "[{\"file_id\":\"71da066c-5d15-3658-a86d-4e85ee67808a\",\"file_name\":\"企业营业执照1.jpg\",\"file_type\":\"F01\"}]"
    },
    "sign": "EHu2semzH0+EIxNcuQpVMo4QicO0+6TEowpYUzSR41RmlkQNWWr11u3nfovOHBrECPG5CU/mO5SPx6mjBRT5Cp0jvWGntXGW7byDZ2AbOMCtBNyAqhZ1EkKSZUuwGXNRgOFRz2Hatki79XwkPdgfGsNrbWiktDklPFeg3ypVql0=",
    "product_id": "JCTEST"
}

```
### 返回参数


#### 同步返回参数

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务响应码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| resp_desc | 业务响应信息 | String | 512 | Y | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| huifu_id | 汇付ID | String | 18 | N | 生成返回汇付企业用户ID；<font color="green">示例值：6666000123123123</font> |


##### 返回示例

###### 成功示例
```json
{
    "data": {
        "huifu_id": "6666000103862211",
        "resp_code": "00000000",
        "resp_desc": "成功"
    },
    "sign": "HaiZ1R4DW1XzukHFeOkfbO4IyTpZF7l8wkjJD9zX12G9ewFiKArMUWZJVY0K7wyKf0aDAEPHSuqFFQJ8XGVZaszT26J3GzUXHLgtegDz3tsbPog25Yne2pHCUtJogSr/jaXFbEHHahdEmj8R3vVd5FTnzCxpExyCeP0ZiPNmMwGGZn8HsrL/S7kFP2k1Gk02HTXdcm0GdwrfDbpNH/AEg8riOsYo7yYjfRmAXbIpvKmw/EampDPxrNGIedmyuQyPLfyCN3NiqZWcXyYjd4Ka1TuFJR07GNicBhEe0ggyNYt8zdevVAHCOsRnFklOCon+/EF4kb3PpQDTjb//TLpdGw=="
}

```
