# 微信小程序支付

小程序支付：商户通过微信小程序向用户提供商品或服务，消费者在微信小程序内通过微信支付完成付款。

## 使用示例

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/46dc6c40-8391-49f2-b64b-6eee34685420.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/b29deff0-5ac8-4613-979d-319b15d218cc.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/bb639f42-0b54-484b-85a2-9cbd725bd028.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/626e7dd4-f3ea-4550-af21-eaecd1fbee0b.png" alt="BlockNote image" width="200" />

## 适用场景

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/206647da-0000-4893-ad86-49a56b18806b.png" alt="image.png" width="785" />

## 体验demo

点击 [斗拱收款演示网站](https://paas.huifu.com/docs/start/#/product_demo) 体验完整产品流程

## 业务流程说明

### **支付**

1.  消费者进入商户微信小程序，选择商品下单，确认购买，进入支付环节；
    
2.  消费者提交支付后，商户侧调用【聚合支付】接口指定“交易类型：微信小程序支付”下单，下单时可根据业务场景需要指定（禁用信用卡/指定收款子账户等），提交对应指令;
    
3.  下单成功后商户侧拉起支付，进入到微信收银台的支付确认界面，用户可在该页面确认收款方信息和支付金额；
    
4.  消费者确认订单收款方和金额无误后，点击“支付”会出现验密界面(验证密码或指纹等)，同时在该页面也可选择支付方式；
    
5.  验密付款成功后，微信会展示支付成功页面，以及“完成”按钮。
    
6.  针对交易结果，系统会通过异步消息的方式推送商户系统，若未收到推送时，商户也可调用【聚合交易查询】接口主动发起查询。
    
7.  消费者点击“完成”后会返回到商户小程序中，商户小程序根据支付结果向用户展示订单支付结果。
    

**若商户需要限制消费者支付的时间，有以下两种方式：**

1.  下单时通过交易有效期参数，设置订单的支付结束时间，超过设置的结束时间后，系统会进行关单处理。
    
2.  商户在自己的系统内进行倒计时，超过有效期，可主动发起关单处理。未收到关单结果，可调用查询接口主动发起查询。
    

注：若消费者实际未支付且下单时中未传入有效期，按系统的轮询保障机制规则，2小时后将交易状态置为失败。

### 退款

1.  退款交易支持全额/部分退款(微信最多支持50次部分退款)，退款期限：360天；
    
2.  退款时手续费会一并退还；
    
3.  退款资金将原路退还至消费者的支付账户（如用户使用银行卡支付，则资金会原路退还到该银行卡账户；使用零钱支付，则资金原路退还到该零钱账户），若商户原交易的收款账户余额不足，则退款失败；
    
4.  针对退款交易结果，系统会通过消息推送通知商户系统，若未收到推送时，商户也可主动发起退款交易查询；
    

## 计费规则

手续费收取，支持按比例收取且支持最低手续费。

退款时退还交易手续费，计算方式向下取整，最后一笔轧差。

## 开通功能和准备材料

1.  准备一个微信小程序，参考 [小程序注册指引](https://kf.qq.com/faq/170109iQBJ3Q170109JbQfiu.html)；
    
2.  完成商户入网且开通微信扫码业务；具体参考  [商户进件](https://paas.huifu.com/open/doc/lightning/#/guide/jinjian/shanghujj_intro)
    
3.  完成微信实名认证，配置微信公众号和支付授权目录。具体参考  [商户进件](https://paas.huifu.com/open/doc/lightning/#/guide/jinjian/shanghujj_intro) 中微信实名认证和微信配置；
    

## 开发接入

查看 [开发指引](https://paas.huifu.com/docs/lightning/#/jsb/zf/wx_xcx_kfzy)

## 分账说明

参考 [订单分账](https://paas.huifu.com/docs/guide/#/zhzjfw/ddfz/ddfz)

## 结算说明

参考 [结算服务](https://paas.huifu.com/docs/guide/#/ythsk/js/zdjs)

## 对账说明

查看 [对账服务](https://paas.huifu.com/docs/guide/#/ythsk/dz/dzd) 获取对账信息