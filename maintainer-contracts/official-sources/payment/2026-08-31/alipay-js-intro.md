# 支付宝 JS 支付

指商家在支付宝客户端中，通过调用支付宝JSAPI接口，在支付场景中唤起支付宝收银台完成收款的一款支付产品。

## 使用示例

线下收银

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/a1ec47b2-ea0c-432b-88a4-d71f5f3025d9.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/f25874aa-0bf2-41e0-a2d4-dcd7bb7391c4.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/836ab8ee-de28-4fc0-b8a9-5635ea860472.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/e9929c42-4870-4204-a14c-cd12041bf5a0.png" alt="BlockNote image" width="200" />

小程序收银

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/031d059c-b15d-45cc-93ed-c96be2d998c1.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/5bb17f34-4e4d-4ab9-91a7-86a05e8d47d8.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/50b53efc-a263-47c9-b97d-435d8c1b28f0.png" alt="BlockNote image" width="200" />

## 适用场景

主要适用于：

*   线下场所面对面收银：门店展示台牌二维码，用户扫描二维码后完成支付
    
*   小程序场景：通过支付宝小程序向用户提供商品或服务，消费者在小程序内完成付款
    

## 体验demo

点击 [斗拱收款演示网站](https://paas.huifu.com/docs/start/#/product_demo) 体验完整产品流程

## 业务流程说明

### 支付

1.  消费者在支付宝客户端浏览器访问商户页面，选择商品后进入支付环节；
    
2.  消费者提交支付后，商户侧调用【聚合支付】接口指定“交易类型：支付宝JS支付”下单，下单时可根据业务场景需要指定（禁用信用卡/指定收款子账户等），提交对应指令;
    
3.  下单成功后商户侧拉起支付，进入到支付宝收银台的支付确认界面，用户可在该页面确认收款方信息和支付金额；
    
4.  消费者确认订单收款方和金额无误后，提交付款会出现验密界面(验证密码或指纹等)；
    
5.  支付成功后支付宝端会弹出成功页面，支付失败会弹出错误提示；
    
6.  针对交易结果，系统会通过异步消息的方式推送商户系统，若未收到推送时，商户也可调用【聚合交易查询】接口主动发起查询；
    

**若商户需要限制消费者支付的时间，有以下两种方式：**

1.  下单时通过交易有效期参数，设置订单的支付结束时间，超过设置的结束时间后，系统会进行关单处理。
    
2.  商户在自己的系统内进行倒计时，超过有效期，可主动发起关单处理。未收到关单结果，可调用查询接口主动发起查询。
    

注：若消费者实际未支付且下单时中未传入有效期，按系统的轮询保障机制规则，2小时后将交易状态置为失败。

### 退款

1.  退款交易支持全额/部分退款，退款期限：360天；
    
2.  退款时手续费会一并退还；
    
3.  退款资金将原路退还至消费者，若商户原交易的收款账户余额不足，则退款失败；
    
4.  针对退款交易结果，系统会通过消息推送通知商户系统，若未收到推送时，商户也可主动发起退款交易查询；
    

## 计费规则

手续费收取，支持按比例收取且支持最低手续费。

退款时退还交易手续费，计算方式向下取整，最后一笔轧差。

## 开通功能和准备材料

1.  完成商户入网且开通支付宝扫码业务；具体参考 [商户进件](https://paas.huifu.com/doc/lightning/#/guide/jinjian/shanghujj_intro)；
    
2.  完成支付宝实名认证；
    

## 开发接入

查看 [开发指引](https://paas.huifu.com/docs/lightning/#/jsb/zf/zfb_js_kfzy)

## 分账说明

参考 [订单分账](https://paas.huifu.com/docs/guide/#/zhzjfw/ddfz/ddfz)

## 结算说明

参考 [结算服务](https://paas.huifu.com/doc/guide/#/ythsk/js/zdjs)

## 对账说明

查看 [对账服务](https://paas.huifu.com/docs/guide/#/ythsk/dz/dzd) 获取对账信息