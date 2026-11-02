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
## 交易结算对账单查询

<span class="request-method post-method">POST</span>https://api.huifu.com/v2/trade/check/filequery

*最近更新时间：2026.05.07*
### 应用场景
本接口支持渠道商/商户查询对账单，需提供渠道商号给运营配置开通对账单功能。

**适用对象**  
  需要交易、结算对账渠道商、商户。  

### 接口说明
* 支持格式：JSON
* 加签验签说明：请参考[接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)；
	* 注：**该接口同步返参file_details是jsonArray，对嵌套的json验签无需排序，详见加验签说明**。

### 公共参数
* 公共请求参数

| 参数       | 中文名   | 定义   | 长度 | 必填 | 说明                  |
| :---------- | :-------- | :------ | :---- | :---- | :--------------------- |
| sys_id     | 系统号   | String | 32   | Y    | 渠道商/商户的huifu_id <br />（1）当主体为渠道商时，此字段填写渠道商huifu_id； <br/>（2）当主体为直连商户时，此字段填写商户huifu_id；<br/><font color="green">示例值：6666000123120000</font>  |
| sign       | 加签结果 | String | 512  | Y    | 签名，对报文整体签名  |
| product_id | 产品号   | String | 32   | Y    | 汇付分配的产品号，<font color="green">示例值：MCS</font>  |
| data       | 数据     | String |      | Y    | JSON格式              |

* 公共返回参数

| 参数                 | 中文名                     | 定义   | 长度 | 必填 | 说明                                                         |
| :------------------- | :------------------------- | :----- | :--- | :--- | :----------------------------------------------------------- |
| sign     | 签名       | String   | 512      | Y        | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq)   |
| data     | 响应内容体 | JSON     |          | N        | 业务返回参数         |


### **请求参数**

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| req_date | 请求日期 | String | 8 | Y | 格式:yyyyMMdd，<font color="green">示例值：20210811</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 请求流水号，<font color="green">示例值：2021091708126665001</font> |
| huifu_id | 汇付客户Id | String | 18 | Y | 渠道与一级代理商的直属商户ID；<font color="green">示例值：6666000123123123</font> |
| file_date | 文件生成日期 | String | 8 | Y | 格式:yyyyMMdd，<font color="green">示例值：20210811</font>；<br/>如果是调接口补生成要填写交易日期+1天（即原对账单生成日期）； |
| bill_type | 文件类型 | String | 128 | N | TRADE_BILL-交易对账单<br/>SPLIT_BILL-分账对账单<br/>WITHDRAWAL_BILL-出金对账单<br/>SETTLE_BILL-结算对账单<br/>TRADE_BILL_MONTH-月交易对账单<br/>SETTLE_BILL_MONTH-月结算对账单<br/>SETTLE_USER_BILL-用户结算对账单<br/>SETTLE_BILL_USER_MONTH-用户月结算对账单</br>SETTLE_FUND_BILL-结算资金对账单<br/>MERGE_BILL-合单支付对账单<br/><font color="green">示例值：TRADE_BILL</font> |


#### 请求示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "file_date": "20240428",
        "bill_type": "TRADE_BILL",
        "req_seq_id": "20240506094347392bzgooscof4vgn0",
        "req_date": "20240506",
        "huifu_id": "6666000109133323"
    },
    "sign": "gUwoKu+SSer6fk/q0A7YFCFVhGjuKjxV+XabE3aennoxxBB+1i7T3AELEvVVstYypUM6kFSmpB4+jrhV3RCgRAfNHVuEH/emVHpF1wDPRTrco27Y1XuEhOviGDPKXRSZpLOXOvN+9xqqnPE+XDVr5Xnr4t31nLWlokgFx4mfTI/2HvCcFu3pY+Km4gYy7S7u4CbLG+BkQHrKAGneI5ZAspFWWNBOYbxb+lx7F6X56pjL/VM7DrNaNcWAvAszT12XyL53kySYrM4GWJKD4Ycwrp8761oRZB/qJFv8LAzd/PKU/4M+oZHBmxgM4RX/l8WbknnEvZoue9CCc1bDX8ED4w=="
}
```
### 返回参数


#### 同步返回参数

**data**

| 参数                     | 中文名                 | <div style="width: 40pt">定义</div>     | <div style="width: 25pt">长度</div> | 必填 | 说明                                                         |
| :----------------------- | :--------------------- | :----- | :--- | :------- | :---------- |
| resp_code | 业务返回码 | String | 8 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：00000000</font> |
| resp_desc | 业务返回描述 | String | 512 | Y | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；<font color="green">示例值：成功</font> |
| req_date | 请求日期 | String | 8 | Y | 原请求信息返回；<font color="green">示例值：20221025</font> |
| req_seq_id | 请求流水号 | String | 128 | Y | 原请求信息返回；<font color="green">示例值：20221107163916760m1lqvgmjmxw8fm</font> |
| <span class="extend 9682af86_1b1f_4a64_95a3_4d30fa13d3d6">file_details</span> | 文件信息 | Array |  | N | 文件生成才会有值 |
| <span class="extend 40280a12_6388_4a92_88f7_047983b2bdfc">task_details</span> | 文件生成任务信息 | Array |  | N | 可以查看还未生成的文件，包含生成文件跑批任务的状态信息 |

<!-- extend:start -->
<!-- div:extend-table 9682af86_1b1f_4a64_95a3_4d30fa13d3d6-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 商户号 | String | 32 | Y | 汇付商户号；<font color="green">示例值：6666000122755200</font> |
| file_date | 文件日期 | String | 8 | Y | 格式:yyyyMMdd；<font color="green">示例值：20221025</font> |
| file_name | 文件名 | String | 64 | Y | 文件名称；<font color="green">示例值：20221025_6666000122755200_order.zip</font> |
| bill_type | 文件类型 | String | 128 | Y | TRADE_BILL-交易对账单<br/>SPLIT_BILL-分账对账单<br/>WITHDRAWAL_BILL-出金对账单<br/>SETTLE_BILL-结算对账单<br/>TRADE_BILL_MONTH-月交易对账单<br/>SETTLE_BILL_MONTH-月结算对账单<br/>SETTLE_USER_BILL-用户结算对账单<br/>SETTLE_BILL_USER_MONTH-用户月结算对账单<br/>SETTLE_FUND_BILL-结算资金对账单<br/><font color="green">示例值：TRADE_BILL</font> |
| download_url | 文件http下载地址 | String | 2048 | Y | <font color="green">示例值：https://file.cloudpnr.com/app-86820a0f-8b13-479b-a466-b261af7290d5%2Fsaturnfile%2F4a76857819a043e187fa6eb1d7ab42e0%2F124a5d9a-53f0-11ed-bc54-0242ac10002.zip?Signature=uf3pVqqTXsm8KDUfYy4XTlXsT2o%3D&Expires=1666664934&OSSAccessKeyId=LTAI6Yzq9tIYS57h</font> |
<!-- extend:end -->

<!-- extend:start -->
<!-- div:extend-table 40280a12_6388_4a92_88f7_047983b2bdfc-table -->
| 参数                 | 中文名        | 定义     | 长度 | 必填 | 说明                                                                                               |
| :---------------- | :------------------- | :----- | :--- | :------- | :----------------------------------------------------------- |
| huifu_id | 商户号 | String | 16 | Y | 汇付商户号；<font color="green">示例值：6666000122755200</font> |
| bill_type | 文件类型 | String | 128 | Y | TRADE_BILL-交易对账单<br/>SPLIT_BILL-分账对账单<br/>WITHDRAWAL_BILL-出金对账单<br/>SETTLE_BILL-结算对账单<br/>TRADE_BILL_MONTH-月交易对账单<br/>SETTLE_BILL_MONTH-月结算对账单<br/>SETTLE_USER_BILL-用户结算对账单<br/>SETTLE_BILL_USER_MONTH-用户月结算对账单<br/><font color="green">示例值：TRADE_BILL</font> |
| file_id | 文件id | String | 128 | N | <font color="green">示例值：57cc7f00-600a-33ab-b614-6221bbf2e529</font> |
| file_name | 文件名 | String | 64 | N | zip原始文件名，http下载后会有临时文件名；<br/><font color="green">示例值：20221025_6666000122755200_order.zip</font> |
| download_url | 文件http下载地址 | String | 256 | N | <font color="green">示例值：https://file.cloudpnr.com/app-86820a0f-8b13-479b-a466-b261af7290d5%2Fsaturnfile%2F4a76857819a043e187fa6eb1d7ab42e0%2F124a5d9a-53f0-11ed-bc54-0242ac10002.zip?Signature=uf3pVqqTXsm8KDUfYy4XTlXsT2o%3D&Expires=1666664934&OSSAccessKeyId=LTAI6Yzq9tIYS57h</font> |
| data_date | 数据日期 | String | 8 | N | 对账文件里的交易发生日期；<font color="green">示例值：20221025</font> |
| task_stat | 跑批任务状态 | String | 2 | N | I:初始化；P:任务处理中；DP:数据处理中；FP:文件处理中；F:失败；S:成功；<br/><font color="green">示例值：S</font> |
| task_start_time | 任务开始时间 | String | 14 | N | <font color="green">示例值：20230701145959</font> |
| task_end_time | 任务结束时间 | String | 14 | N | <font color="green">示例值：20230701145959</font> |
<!-- extend:end -->


##### 返回示例

###### 成功示例
```json
{  
    "data":{  
        "resp_code":"00000000",  
        "resp_desc":"查询成功",  
        "file_details":[  
            {  
                "download_url":"https://file.cloudpnr.com/app-86820a0f-8b13-479b-a466-b261af7290d5%2Fsaturnfile%2F60bdb3fcbe534c25ab80c908578a0c59%2F1161cd50-31e9-11ee-9bd1-0242ac110002.zip?Signature=EIqOPgBSjwS7Iy3UvYQiZYgDm8g%3D&OSSAccessKeyId=LTAI6Yzq9tIYS57h&Expires=1722671156",  
                "file_date":"20230803",  
                "file_id":"f577ea48-033b-3f08-8ae5-994ec0996053",  
                "file_Name":"20230803_6666000111546360_order.zip",  
                "huifu_id":"6666000111546360",  
                "bill_type": "TRADE_BILL"
            }  
        ],  
        "task_details":[  
            {  
                "data_date":"20230802",  
                "download_url":"https://file.cloudpnr.com/app-86820a0f-8b13-479b-a466-b261af7290d5%2Fsaturnfile%2F60bdb3fcbe534c25ab80c908578a0c59%2F1161cd50-31e9-11ee-9bd1-0242ac110002.zip?Expires=1722671156&OSSAccessKeyId=LTAI6Yzq9tIYS57h&Signature=EIqOPgBSjwS7Iy3UvYQiZYgDm8g%3D",  
                "file_id":"f577ea48-033b-3f08-8ae5-994ec0996053",  
                "file_name":"20230803_6666000111546360_order.zip",  
                "bill_type": "TRADE_BILL",
                "huifu_id":"6666000111546360",  
                "task_end_time":"20230803183238",  
                "task_start_time":"20230803183237",  
                "task_stat":"S"  
            }  
        ]  
    },  
    "sign":"fy2NgWhzpKQeoLL6PIv4DeXvAWHWa1ezw7H5EaIm5RhyM3MjzqHThhRoJLfz1xpFh4aDW4T5MQSYz4//es0aHD6OA+ZHO3xZWy8MAxArWHPVHe6ksylRju5nKjCMSAe3ath711twdejcatcm8Fc4Ollaeg1cYmUdA3d79ct5hGTsAQ2ewqRGG5wBUt9X6m0Q8GTnReTgm938B3kHU8RlVQXHf/TGHK8xcMIs5WTH/bRgfbFfvuNrRP8uaKao0q7mmZfVw6NzDzXpTYaTc3p1auYijc2oqo43y3dERSggKV5Z5uQCvbDIfd7hydG2rrLdGppcv51yQmInkIKDu8cmoQ=="  
}
```


#### 补充说明

1. 每日跑批生成上一个工作日或自然日的对账文件，（按T+1/D+1日规则生成）： 
	- 3：00日交易数据、分账对账文件跑批， 建议一小时后取文件；
	<!--5：00正切数据跑批--> 
	- 17：00日结算对账单跑批， 建议一小时后取文件；
	- 17：15出金对账单跑批， 建议一小时后取文件；
3. 若文件信息【file_details】为空，建议查看文件生成任务【task_details】，如果跑批任务状态task_stat为成功，且对账文件为空代表前一日无记录。
4. 接口一次调用返回一个链接，一个链接对应一个zip文件。zip中文件格式为csv。记录超过200000会拆分csv，多个csv会打包为一个zip。



#### 对账文件模板

- ##### 交易数据
1. 下载的文件是一个zip包，里面包含的是同一批次的多个交易数据csv文件；
2. 文件名称说明：【年月日_商户号_order_批次号.csv】，月度文件【年月日_商户号_order_批次号.csv】
3. [交易数据模板下载](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/zhangdan/20220331_66660001103xxxxx_order_1.csv)

- ##### 商户结算对账单
1. 下载的文件是一个zip包，里面包含的是同一批次的多个结算对账单csv文件；
2. 文件名称说明：【年月日_商户号_settle_批次号.csv】，月度文件【年月日_商户号_settle_批次号.csv】
3. [商户结算对账单模板下载](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/zhangdan/20220401_66660001102xxxxx_settle_1.csv)

- ##### 出金对账单
1. 下载的文件是一个zip包，里面包含的是同一批次的多个出金对账单csv文件；
2. 出金是日对账单，下载文件名称：【年月日_商户号_outcash_批次号.csv】
3. [出金对账单模板下载](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/zhangdan/20220331_6666000110_outcash_1.csv)
- ##### 分账对账单
1. 下载的文件是一个zip包，里面包含的是同一批次的多个分账对账单csv文件；
2. 文件名称说明：【年月日_商户号_split_批次号.csv】
3. [分账对账单模板下载](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/zhangdan/20220527_6666000109133323_split_1.csv)
- ##### 用户结算对账单
1.  下载的文件是一个zip包，里面包含的是同一批次的多个用户结算对账单csv文件；
2.  文件名称说明：【年月日_商户号_settleuser_批次号.csv】
3.  [用户结算对账单模板下载](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/zhangdan/20220401_6666000110XXXXXX_settleuser%20_1.csv)
- ##### 全域资金入账明细单
1.  下载的文件是一个zip包，里面包含的是同一批次的多个商户打款对账单csv文件；
2.  文件名称说明：日对账单【年月日_商户号_remittance_批次号.csv】，月对账单【年月_商户号_remittance_批次号.csv】
3.  [商户全域资金入账明细单模板下载](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/zhangdan/202304_6666000003100616_remittance_1.csv)
- ##### 电子账户资金变动明细文件
1.  下载的文件是一个zip包，里面包含的是同一批次的多个商户打款对账单csv文件；
2.  文件名称说明：日对账单【渠道商号+银行英文简称（默认中信citic）+文件类型（3位，默认811）+日期（8位，当前系统日期）_序号（默认：1）.csv】
3. [电子账户资金变动明细文件模板下载](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/zhangdan/4b7c11ca-5476-4d0d-9740-12bd1a1f9b21.zip)
- ##### 结算资金对账单
1.  下载的文件是一个zip包，里面包含的是同一批次的多个用户/商户结算资金对账单EXCEL文件；
2.  文件名称说明：【年月日_商户号_settlefund.xlsx】
3. [结算资金对账单模板下载](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/zhangdan/20250225_6666000109133323__settlefund.xlsx)

