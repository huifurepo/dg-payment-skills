## 接入前准备

1.  阅读【产品介绍】，确保已完成【开通功能和准备材料】中内容；
    
2.  开发者需要先到 [微信公众平台](https://mp.weixin.qq.com/)中的「设置与开发 - 账号设置 - 功能设置」的配置选项中，修改「网页授权域名」；将微信校验文件放到服务器根目录下；
    
3.  按照 [开发接入-接入说明](https://paas.huifu.com/docs/guide/#/kfjr/jrsm) 完成公私钥配置，公共参数获取；了解斗拱开发规范；
    
4.  斗拱为提升开发者体验和效率，向 AI coding 开发者提供 [支付 skill](https://paas.huifu.com/docs/devtools/#/skillsv1_0) 协助开发；
    

## 接入流程概览

1.  **调用微信收银台**：商户后端调用 [V4聚合支付](https://paas.huifu.com/open/doc/lightning/#/api/jhzfxd)，交易类型上送微信公众号支付，获取`pay_info`后，在微信客户端前端页面调用 [WeixinJSBridge](https://pay.weixin.qq.com/doc/v3/merchant/4012791857) 对象方法调起微信收银台；
    
2.  **下单支付**：当用户取消支付或支付成功后点击"完成"按钮，会返回拉起支付前页面，同时商户前端页面将收到回调，此时商户后端需调用 [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) 确认订单状态，并根据订单状态进行相应的业务逻辑处理（在商户页面向用户展示查询到的订单支付状态、在商户内部系统更新订单状态等）；
    
3.  **支付结果返回**：如果订单支付成功，斗拱系统还会发送 [支付成功回调通知](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao) 给商户；
    
4.  最后商户可通过 [下载交易账单](https://paas.huifu.com/open/doc/lightning/#/api/%E5%AF%B9%E8%B4%A6%E5%8D%95API) 进行对账。特殊需要退款的订单，也可调用 [聚合支付退款](https://paas.huifu.com/open/doc/lightning/#/api/jytk) 完成退款。
    

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/5660f3be-6554-4997-8350-e79e94ff65b3.png" alt="8363007f-dacf-467e-8987-81ffa4c61333.png" width="857" />

## 详细步骤说明

### **1\. 通过用户授权获取用户** **openid**               <strong>&nbsp;</strong>

**openid**：用户在公众号内的身份标识，不同公众号拥有不同的 openid ，主要用途是判断同一个用户，对用户发送客服消息、模版消息等；授权说明见微信官方链接： [网页授权](https://developers.weixin.qq.com/doc/service/guide/h5/auth)

1.  浏览器跳转 [微信网页授权](https://developers.weixin.qq.com/doc/service/guide/h5/auth.html) 地址获取 code。传入参数： `appid` = 微信公众号AppID，` redirect_uri` = 回调地址，`response_type="code"`，`scope="snsapi_base"`(只为获取 openid 的话静默授权就可以，无需用户同意，不弹出授权页面，只能获取用户 open_id,)，返回 `code`；
    

```json
<a target="_blank" rel="noopener noreferrer nofollow" href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect">https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect</a>
```

2.  获取 access_token 和 opneid：调用 获取用户信息接口，传入` code` 之后， 获取用户信息 openid 和 access_token
    

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/7803cae2-cc65-4c73-be6a-2b162705c27a.png" alt="0ed8c1d0-dec1-4c06-9c40-606a47a7e28f.png" width="389" />
```json
/* 请求参数 */
url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
params = {
        'appid': app_id,
        'secret': 'wx_secret',
        'code': wx_code,
        'grant_type': 'authorization_code',
}

/* 获取openid */
resp = requests.get(url, params, timeout=15)
result_dict = json.loads(resp.text)
openid=result_dict.get('openid')

```

### 2\. 用户下单

1.  商户通过调用 [V4聚合支付](https://paas.huifu.com/open/doc/lightning/#/api/jhzfxd) ，将接口应答的支付信息 pay_info 返回前端页面
    

*   `trade_type` ：选 `T_JSAPI`；
    
*   `sub_openid`：用户在商户下单的 appid 下唯一标识，商户获取 openid 后上送到汇付 `sub_openid `字段；
    
*   `pay_info`：扫码支付信息。调起支付时需要使用该参数，失效后，**商户需要使用原下单参数重新请求**，获取新的支付信息；
    

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/5a66de75-e402-4dff-9015-d40d0ed74815.png" alt="5c5e7a27-5f98-41c6-9c68-d5b2f39c8f4f.png" width="794" />

### **3\. 商户调起收银台，发起支付**

商户通过调用 [WeixinJSBridge](https://pay.weixin.qq.com/doc/v3/merchant/4012791857) 对象方法来调起微信收银台，详情参考 [JSAPI调起支付](https://pay.weixin.qq.com/doc/v3/merchant/4012791857)。商户调起微信收银台前，请确保已在商户平台配置好授权域名

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/2ab0c0cd-61cc-4f5e-ab87-a0c734088ee8.png" alt="7687d0df-360d-4550-964f-a4c0608f66e1.png" width="789" />
```json
/**
 * 调起微信支付
 * @param {Object} payInfo - 从后端获取的支付信息
 * @param {string} payInfo.appId - 微信公众号appId
 * @param {string} payInfo.timeStamp - 时间戳
 * @param {string} payInfo.nonceStr - 随机字符串
 * @param {string} payInfo.package - 统一下单接口返回的prepay_id参数值，格式：prepay_id=***
 * @param {string} payInfo.signType - 签名类型，默认为RSA
 * @param {string} payInfo.paySign - 签名
 */
function invokeWeixinPay(payInfo) {
    // 检查是否在微信浏览器环境
    if (typeof WeixinJSBridge === "undefined") {
        alert('请在微信浏览器中打开此页面');
        return;
    }
    
    // 调起微信支付
    WeixinJSBridge.invoke('getBrandWCPayRequest', {
        "appId": payInfo.appId,           // 公众号ID
        "timeStamp": payInfo.timeStamp,   // 时间戳
        "nonceStr": payInfo.nonceStr,     // 随机串
        "package": payInfo.package,       // 统一下单接口返回的prepay_id参数值
        "signType": payInfo.signType,     // 微信签名方式
        "paySign": payInfo.paySign        // 微信签名
    }, function(res) {
        // 支付完成后的回调处理
        if (res.err_msg === "get_brand_wcpay_request:ok") {
            // 支付成功，但需要调用后端查询接口确认最终状态
            console.log('支付成功，正在确认订单状态...');
            checkOrderStatus();
        } else if (res.err_msg === "get_brand_wcpay_request:cancel") {
            // 用户取消支付
            console.log('用户取消支付');
            handlePaymentCancel();
        } else {
            // 支付失败
            console.log('支付失败：' + res.err_msg);
            handlePaymentError(res.err_msg);
        }
    });
}

/**
 * 检查订单状态
 */
function checkOrderStatus() {
    // 调用后端查询订单状态接口
    fetch('/api/payment/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            orderId: currentOrderId  // 当前订单ID
        })
    })
    .then(response =&amp;amp;amp;amp;amp;amp;gt; response.json())
    .then(data =&amp;amp;amp;amp;amp;amp;gt; {
        if (data.success &amp;amp;amp;amp;amp;amp;amp;&amp;amp;amp;amp;amp;amp;amp; data.orderStatus === 'PAID') {
            // 订单支付成功
            showPaymentSuccess();
        } else {
            // 订单未支付成功，可能需要重新查询或处理
            showPaymentPending();
        }
    })
    .catch(error =&amp;amp;amp;amp;amp;amp;gt; {
        console.error('查询订单状态失败:', error);
        showPaymentError();
    });
}

/**
 * 处理支付取消
 */
function handlePaymentCancel() {
    // 显示取消支付的提示
    alert('支付已取消');
    // 可以跳转到订单页面或其他处理
}

/**
 * 处理支付错误
 */
function handlePaymentError(errorMsg) {
    // 显示支付错误信息
    alert('支付失败：' + errorMsg);
    // 可以提供重新支付的选项
}

/**
 * 显示支付成功页面
 */
function showPaymentSuccess() {
    // 跳转到支付成功页面或显示成功信息
    window.location.href = '/payment/success';
}

/**
 * 显示支付待确认状态
 */
function showPaymentPending() {
    // 显示支付状态确认中的信息
    alert('支付状态确认中，请稍后...');
    // 可以设置定时器继续查询
    setTimeout(checkOrderStatus, 3000);
}

/**
 * 显示支付错误页面
 */
function showPaymentError() {
    // 显示支付错误页面
    alert('支付状态查询失败，请联系客服');
}

// 页面加载完成后，检查微信JS-SDK是否可用
document.addEventListener('DOMContentLoaded', function() {
    if (typeof WeixinJSBridge === "undefined") {
        // 如果WeixinJSBridge未定义，监听其加载完成事件
        if (document.addEventListener) {
            document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
        } else if (document.attachEvent) {
            document.attachEvent('WeixinJSBridgeReady', onBridgeReady);
            document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
        }
    } else {
        onBridgeReady();
    }
});

function onBridgeReady() {
    console.log('微信JS-SDK已准备就绪');
    // 可以在这里初始化支付相关的UI
}

```

### 4\. 完整代码示例

*   **服务端代码**
    

```json
/**
 * 完整的支付流程示例
 */
class WeixinPayment {
    constructor(orderId) {
        this.orderId = orderId;
        this.maxRetryCount = 3;  // 最大重试次数
        this.retryCount = 0;
    }
    
    /**
     * 开始支付流程
     */
    async startPayment() {
        try {
            // 1. 调用后端获取支付信息
            const payInfo = await this.getPayInfo();
            
            // 2. 调起微信支付
            this.invokeWeixinPay(payInfo);
            
        } catch (error) {
            console.error('支付流程启动失败:', error);
            this.handleError('支付初始化失败，请重试');
        }
    }
    
    /**
     * 获取支付信息，调用后台，由后台发起汇付SDK聚合交易下单
     */
    async getPayInfo() {
        const response = await fetch('/api/payment/prepare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                orderId: this.orderId
            })
        });
        
        if (!response.ok) {
            throw new Error('获取支付信息失败');
        }
        
        const result = await response.json();
        if (!result.success) {
            throw new Error(result.message || '获取支付信息失败');
        }
        
        return result.data;
    }
    
    /**
     * 调起微信支付
     */
    invokeWeixinPay(payInfo) {
        if (typeof WeixinJSBridge === "undefined") {
            this.handleError('请在微信浏览器中打开此页面');
            return;
        }
        
        WeixinJSBridge.invoke('getBrandWCPayRequest', payInfo, (res) =&amp;amp;amp;amp;amp;amp;gt; {
            this.handlePaymentResult(res);
        });
    }
    
    /**
     * 处理支付结果
     */
    async handlePaymentResult(res) {
        switch (res.err_msg) {
            case "get_brand_wcpay_request:ok":
                // 支付成功，查询订单状态确认
                await this.verifyPaymentStatus();
                break;
            case "get_brand_wcpay_request:cancel":
                this.handleCancel();
                break;
            default:
                this.handleError('支付失败：' + res.err_msg);
                break;
        }
    }
    
    /**
     * 验证支付状态
     */
    async verifyPaymentStatus() {
        try {
            const response = await fetch('/api/payment/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    orderId: this.orderId
                })
            });
            
            const result = await response.json();
            
            if (result.success &amp;amp;amp;amp;amp;amp;amp;&amp;amp;amp;amp;amp;amp;amp; result.data.status === 'PAID') {
                this.handleSuccess();
            } else if (this.retryCount &amp;amp;amp;amp;amp;amp;lt; this.maxRetryCount) {
                // 重试查询
                this.retryCount++;
                setTimeout(() =&amp;amp;amp;amp;amp;amp;gt; this.verifyPaymentStatus(), 2000);
            } else {
                this.handleError('支付状态确认超时，请联系客服');
            }
            
        } catch (error) {
            console.error('查询支付状态失败:', error);
            this.handleError('支付状态查询失败');
        }
    }
    
    /**
     * 处理支付成功
     */
    handleSuccess() {
        // 显示成功信息
        alert('支付成功！');
        // 跳转到成功页面
        window.location.href = '/payment/success?orderId=' + this.orderId;
    }
    
    /**
     * 处理支付取消
     */
    handleCancel() {
        alert('支付已取消');
        // 可以返回订单页面或提供重新支付选项
    }
    
    /**
     * 处理错误
     */
    handleError(message) {
        alert(message);
        console.error('支付错误:', message);
    }
}

// 使用示例
// const payment = new WeixinPayment('ORDER_123456');
// payment.startPayment();

```

*   **前端代码**
    

```json
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信支付</title>
</head>
<body>
    <div class="payment-container">
        <h2>订单支付</h2>
        <div class="order-info">
            <p>订单号：<span id="orderId"></span></p>
            <p>支付金额：<span id="amount"></span>元</p>
        </div>
        <button id="payBtn" class="pay-button">立即支付</button>
    </div>
    
    <script>
        // 页面初始化
        document.addEventListener('DOMContentLoaded', function() {
            const orderId = getUrlParameter('orderId');
            const amount = getUrlParameter('amount');
            
            document.getElementById('orderId').textContent = orderId;
            document.getElementById('amount').textContent = amount;
            
            // 绑定支付按钮事件
            document.getElementById('payBtn').addEventListener('click', function() {
                const payment = new WeixinPayment(orderId);
                payment.startPayment();
            });
        });
        
        // 获取URL参数
        function getUrlParameter(name) {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(name);
        }
    </script>
</body>
</html>

```

### **5\. 交易终态处理**

1.  用户在微信收银台完成支付/取消支付，返回商户前端页面后，斗拱系统会向商户发送 [支付成功回调](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao)
    
    *   未收到回调时，商户也可调用 [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) 确认订单状态，根据订单状态向用户展示支付结果。
        
2.  若商户需要限制用户支付的时间，有以下两种方式：
    
    *   下单时通过`time_expire`参数，设置订单的支付结束时间，超过设置的结束时间后，商户进行关单处理；
        
    *   商户在自己的系统内进行倒计时，超过有效期，进行关单处理。
        
3.  若因特殊原因需在用户可支付时间范围内关闭订单，商户可通过调用 [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/jyddcx) 确认订单状态。若订单仍是未支付状态，商户可以调用 [聚合支付关单](https://paas.huifu.com/open/doc/lightning/#/api/jygd) 关单，关单后可以将订单当作失败终态处理。
    

### 6\. 退款流程

*   完整的交易流程还要包括退款。由于用户或者商户的原因需要退款时，商户可以通过调用接口将支付款退还给用户。微信、支付宝、银联云闪付参见 [聚合支付退款](https://paas.huifu.com/open/doc/lightning/#/api/jytk)，关注以下请参：
    

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

| 类型  | 功能  | 说明  |
| --- | --- | --- |
| API | [公众号获取OpenID](https://developers.weixin.qq.com/doc/service/guide/h5/) | 商户前端可通过该方法获取用户OpenID |
| API | [WeixinJSBridge](https://pay.weixin.qq.com/doc/v3/merchant/4012791857) | 商户前端可通过该方法调起微信收银台 |
| API | [聚合支付下单](https://paas.huifu.com/open/doc/lightning/#/api/%E8%81%9A%E5%90%88%E6%94%AF%E4%BB%98%E4%B8%8B%E5%8D%95) | 商户服务端可通过该接口进行下单并获取pay_info |
| API | [聚合支付查询](https://paas.huifu.com/open/doc/lightning/#/api/%E8%81%9A%E5%90%88%E4%BA%A4%E6%98%93%E6%9F%A5%E8%AF%A2) | 商户服务端可通过该接口查询订单状态 |
| API | [聚合支付关单](https://paas.huifu.com/open/doc/lightning/#/api/%E8%81%9A%E5%90%88%E4%BA%A4%E6%98%93%E5%85%B3%E5%8D%95) | 商户服务端可通过该接口发起订单关闭请求 |
| API | [聚合支付关单查询](https://paas.huifu.com/open/doc/lightning/#/api/%E8%81%9A%E5%90%88%E4%BA%A4%E6%98%93%E5%85%B3%E5%8D%95%E6%9F%A5%E8%AF%A2) | 商户服务端可通过该接口查询关单状态 |
| API | [聚合支付退款](https://paas.huifu.com/open/doc/lightning/#/api/%E4%BA%A4%E6%98%93%E9%80%80%E6%AC%BE) | 商户服务端可通过该接口发起订单退款请求 |
| API | [聚合支付退款查询](https://paas.huifu.com/open/doc/lightning/#/api/%E4%BA%A4%E6%98%93%E9%80%80%E6%AC%BE%E6%9F%A5%E8%AF%A2) | 商户服务端可通过该接口查询订单退款状态 |

## Webhook

查看 [Webhook](https://paas.huifu.com/open/doc/devtools/#/webhook/webhook_jieshao)