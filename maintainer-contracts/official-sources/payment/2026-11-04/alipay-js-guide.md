## 接入前准备

1.  阅读【产品介绍】，确保已完成【开通功能和准备材料】中内容；
    
2.  按照 [开发接入-接入说明](https://paas.huifu.com/docs/guide/#/kfjr/jrsm) 完成公私钥配置，公共参数获取；了解斗拱开发规范；
    
3.  斗拱为提升开发者体验和效率，向 AI coding 开发者提供 [支付 skill](https://paas.huifu.com/docs/devtools/#/skillsv1_0) 协助开发；
    

## 支付接入流程概览

1.  **调用支付宝收银台:** 商户后端调用 [聚合支付](https://paas.huifu.com/open/doc/lightning/#/api/jhzfxd)，交易类型上送 支付宝JS支付(A_JSAPI)，获取 `pay_info` 后，在支付宝客户端前端页面调用 [my.tradePay](https://open.alipay.com/api/detail?code=I1140300001000013424&index=1) 接口调起支付宝收银台；
    
2.  **下单支付**：当用户取消支付或支付成功后点击"完成"按钮，会返回拉起支付前页面，同时商户前端页面将收到回调，此时商户后端需调用 [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) 确认订单状态，并根据订单状态进行相应的业务逻辑处理（在商户页面向用户展示查询到的订单支付状态、在商户内部系统更新订单状态等）；
    
3.  **支付结果返回**：如果订单支付成功，斗拱系统还会发送 [支付成功回调](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao) 给商户；
    
4.  最后商户可通过[下载交易账单](https://paas.huifu.com/open/doc/lightning/#/api/%E5%AF%B9%E8%B4%A6%E5%8D%95API)进行对账。特殊需要退款的订单，也可调用 [聚合支付退款](https://paas.huifu.com/open/doc/lightning/#/api/jytk) 完成退款。
    

## 详细步骤说明

### 1\. 获取用户标识 user_id

`user_id`：用户在支付宝内的身份标识，不同支付宝应用拥有相同的 `user_id`，主要用途是判断同一个用户，对用户发送客服消息、模板消息等。

商户通过 [获取user_id](https://open.alipay.com/api/detail?code=I1140300001000013424&index=1) 获取用户标识

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/7df18f6b-79a6-423b-a722-0749f799e73d.png" alt="image.png" width="680" />

### 2\. 商户下单

商户通过调用 [聚合支付](https://paas.huifu.com/open/doc/lightning/#/api/jhzfxd) ，交易类型上送支付宝JS支付（A_JSAPI），生成订单并获取预支付ID；

*   `buyer_id`：用户在商户下单的唯一标识（同user_id）；
    
*   `pay_info`：扫码支付信息。调起支付时需要使用该参数，失效后，**商户需要使用原下单参数重新请求**，获取新的支付信息。
    

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/be097b18-faec-4d25-b843-5712bcca47b1.png" alt="image.png" width="728" />

### 3\. 商户调起收银台

1.  商户通过调用[my.tradePay](https://open.alipay.com/api/detail?code=I1140300001000013424&index=1)接口来调起支付宝收银台
    

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/f2b65418-6ff5-47fb-928b-77c717c0ef38.png" alt="image.png" width="707" />

### 4\. 用户支付，获取交易终态

1.  用户在支付宝收银台完成支付/取消支付，返回商户前端页面后，斗拱系统会向商户发送 [支付成功回调](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao)
    
    *   未收到回调时，商户也可调用 [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) 确认订单状态，根据订单状态向用户展示支付结果。
        
2.  若商户需要限制用户支付的时间，有以下两种方式：
    
    *   下单时通过`time_expire`参数，设置订单的支付结束时间，超过设置的结束时间后，商户进行关单处理；
        
    *   商户在自己的系统内进行倒计时，超过有效期，进行关单处理。
        
3.  若因特殊原因需在用户可支付时间范围内关闭订单，商户可通过调用 [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) 确认订单状态。若订单仍是未支付状态，商户可以调用 [聚合支付关单](https://paas.huifu.com/open/doc/lightning/#/api/jygd) 关单，关单后可以将订单当作失败终态处理。
    

### 5\. 退款流程

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
| [获取user_id](https://open.alipay.com/api/detail?code=I1140300001000013424&index=1) | 商户前端可通过该方法获取用户User_ID |
| [my.tradePay](https://open.alipay.com/api/detail?code=I1140300001000013424&index=1) | 商户前端可通过该接口调起支付宝收银台 |
| [聚合支付](https://paas.huifu.com/open/doc/lightning/#/api/jhzfxd) | 商户服务端可通过该接口进行下单并获取pay_info |
| [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) | 商户服务端可通过该接口查询订单状态 |
| [聚合支付关单](https://paas.huifu.com/open/doc/lightning/#/api/jygd) | 商户服务端可通过该接口发起订单关闭请求 |
| [聚合支付关单查询](https://paas.huifu.com/open/doc/lightning/#/api/jygdcx) | 商户服务端可通过该接口查询关单状态 |
| [聚合支付退款](https://paas.huifu.com/open/doc/lightning/#/api/jytk) | 商户服务端可通过该接口发起订单退款请求 |
| [聚合支付退款查询](https://paas.huifu.com/open/doc/lightning/#/api/jytkcx) | 商户服务端可通过该接口查询订单退款状态 |

### Webhook

查看 [Webhook](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao)