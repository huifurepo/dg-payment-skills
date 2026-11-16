## 接入前准备

1.  阅读【产品介绍】，确保已完成【开通功能和准备材料】中内容；
    
2.  按照 [开发接入-接入说明](https://paas.huifu.com/docs/guide/#/kfjr/jrsm) 完成公私钥配置，公共参数获取；了解斗拱开发规范；
    
3.  斗拱为提升开发者体验和效率，向 AI coding 开发者提供 [支付 skill](https://paas.huifu.com/docs/devtools/#/skillsv1_0) 协助开发；
    

## 接入流程概览

1.  商户使用扫码设备读取用户云闪付客户端付款码条码` auth_code`，并上送到商户后端；
    
2.  商户后端调用 [聚合支付](https://paas.huifu.com/open/doc/lightning/#/api/jhzfxd)，交易类型上送支付宝付款码支付（A_MICROPAY），并上送 `auth_code`，支付宝系统得到支付请求之后会对请求进行验证，验证通过后判断当前用户是否需要输入密码；
    
    1.  如果需要输入密码：用户支付宝客户端跳出输入密码提示并完成密码输入。正确输入密码显示支付成功；
        
    2.  如无需输入密码，将会显示支付成功；
        
3.  商户后端需调用 [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) 接口确认订单状态，并根据订单状态进行相应的业务逻辑处理（在商户内部系统更新订单状态等），
    
4.  **支付结果返回**：如果订单支付成功，斗拱系统还会发送 [支付成功回调](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao) 给商户；
    
5.  最后商户可通过 [下载交易账单](https://paas.huifu.com/open/doc/lightning/#/api/%E5%AF%B9%E8%B4%A6%E5%8D%95API) 进行对账。特殊需要退款的订单，也可调用 [聚合支付退款](https://paas.huifu.com/open/doc/lightning/#/api/jytk) 完成退款。
    

## 详细步骤说明

### **1\. 获取 auth_code**

商户通过扫码设备读取用户云闪付客户端付款码条码`auth_code`

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/331a0272-acdd-42fe-bdcd-b7c1dd964e79.png" alt="image.png" width="221" />

### **2\. 用户下单**

商户通过调用 [聚合支付](https://paas.huifu.com/open/doc/lightning/#/api/jhzfxd)，交易类型上送支付宝付款码支付：

*   `auth_code`：用户云闪付客户端上付款条码。
    

### **3\. 交易终态处理**

用户在支付宝App完成支付/取消支付，斗拱系统会向商户发送 [支付成功回调](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao)；

未收到回调时，商户也可调用 [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) 确认订单状态，根据订单状态向用户展示支付结果。

### 4\. 退款流程

*   完整的交易流程还要包括退款。由于用户或者商户的原因需要退款时，商户可以通过调用 [聚合支付退款](https://paas.huifu.com/open/doc/lightning/#/api/jytk) 将支付款退还给用户。关注以下请参：
    

| **参数** | **中文名** | **必填** | **说明** |
| --- | --- | --- | --- |
| org_req_date | 原交易请求日期 | Y   | 用户发起支付的日期 |
| org_req_seq_id | 原交易请求流水号 | C   | 商户系统发给斗拱的指令流水号 |
| org_hf_seq_id | 原交易全局流水号 | C   | 汇付生成的系统流水号 |
| org_party_order_id | 原交易微信支付宝的商户单号 | C   | 该笔交易在微信支付宝端的流水号 |
| ord_amt | 申请退款金额 | Y   | 退款金额<=原交易金额 |

*   原交易请求流水号、原交易全局流水号、原交易微信支付宝的商户单号三选一即可；
    
*   退款金额不能大于交易金额；由于接口支持多次部分退款，多次退款场景下退款总额不能高于原交易金额；
    
*   退款也是以异步返回的成功或失败状态为最终结果；
    
*   退款成功资金将原路返回。一些特殊场景下退款时效可能比较长，注意接口描述文档中的退款时效说明
    

## 涉及 API

| 功能  | 说明  |
| --- | --- |
| [聚合支付](https://paas.huifu.com/open/doc/lightning/#/api/jhzfxd) | 商户服务端可通过该接口进行下单并获取pay_info |
| [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) | 商户服务端可通过该接口查询订单状态 |
| [聚合支付关单](https://paas.huifu.com/open/doc/lightning/#/api/jygd) | 商户服务端可通过该接口发起订单关闭请求 |
| [聚合支付关单查询](https://paas.huifu.com/open/doc/lightning/#/api/jygdcx) | 商户服务端可通过该接口查询关单状态 |
| [聚合支付退款](https://paas.huifu.com/open/doc/lightning/#/api/jytk) | 商户服务端可通过该接口发起订单退款请求 |
| [聚合支付退款查询](https://paas.huifu.com/open/doc/lightning/#/api/jytkcx) | 商户服务端可通过该接口查询订单退款状态 |

### Webhook

查看[Webhook](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao)