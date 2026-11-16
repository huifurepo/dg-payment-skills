# 微信付款码支付

消费者打开微信客户端，通过“右上角+号->收付款”，或“我->服务→收付款”来展示付款码，商户使用扫码设备扫描该付款码后完成扣款的支付场景。

付款码支付主要用于线下的商超，便利店等有收银设备（pos机），需要快捷收银的支付场景。

## 使用示例

免密场景

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/556707d3-5210-4931-8a33-e077f257590e.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/0d3faefa-60ca-49e4-82b4-4c68e3092e05.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/7edb90ec-564d-479a-adb7-1da4a9ff3cd3.png" alt="BlockNote image" width="200" />

验密场景

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/03fbe9a2-ec71-49f4-96a8-061d0fc2b2c1.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/c206436b-f048-47e5-a62f-d22842666c2e.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/79e6a245-b1d2-4b7a-ab3e-ca5932c402be.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/79e6a245-b1d2-4b7a-ab3e-ca5932c402be.png" alt="BlockNote image" width="200" />

## 适用场景

<img src="https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/lightning/guide/415d6797-a161-4177-8c4d-a3ea5f32c631.png" alt="image.png" />

## 体验demo

点击 [斗拱收款演示网站](https://paas.huifu.com/docs/start/#/product_demo) 体验完整产品流程

## 业务流程说明

### 支付

1.  消费者选择付款码支付，预先打开微信付款码；
    
2.  收银员在商户系统操作生成支付订单，用户确认核对支付金额；
    
3.  商户收银员用扫码设备扫描用户的条码/二维码，商户收银系统提交支付；
    
4.  商户侧调用【聚合支付】接口指定“交易类型：微信反扫支付”下单，下单时可根据业务场景需要指定（禁用信用卡/指定收款子账户等），提交对应指令；
    
5.  下单成功后，微信支付后台系统收到支付请求，根据验证密码规则判断是否验证消费者的支付密码，不需要验证密码的交易直接发起扣款，需要验证密码的交易会弹出密码输入框；
    
6.  支付成功后微信端会弹出成功页面，支付失败会弹出错误提示；
    
7.  针对交易结果，系统会通过异步消息的方式推送商户系统，若未收到推送时，商户也可调用【聚合交易查询】接口主动发起查询。
    

**若商户需要限制消费者支付的时间，有以下两种方式：**

1.  下单时通过交易有效期参数，设置订单的支付结束时间，超过设置的结束时间后，系统会进行关单处理。
    
2.  商户在自己的系统内进行倒计时，超过有效期，可主动发起关单处理。未收到关单结果，可调用查询接口主动发起查询。
    

注：若消费者实际未支付且下单时中未传入有效期，按系统的轮询保障机制规则，3分钟后将交易状态置为失败。

### 退款

1.  退款交易支持全额/部分退款(微信最多支持50次部分退款)，退款期限：360天；
    
2.  退款时手续费会一并退还；
    
3.  退款资金将原路退还至消费者的支付账户（如用户使用银行卡支付，则资金会原路退还到该银行卡账户；使用零钱支付，则资金原路退还到该零钱账户），若商户原交易的收款账户余额不足，则退款失败；
    
4.  针对退款交易结果，系统会通过消息推送通知商户系统，若未收到推送时，商户也可主动发起退款交易查询；
    

## 计费规则

手续费收取，支持按比例收取且支持最低手续费。

退款时退还交易手续费，计算方式向下取整，最后一笔轧差。

## 开通功能和准备材料

1.  准备一个微信应用（公众号或小程序），操作方式：[小程序注册指引](https://kf.qq.com/faq/170109iQBJ3Q170109JbQfiu.html) / [公众号注册指引](https://kf.qq.com/faq/120911VrYVrA151013MfYvYV.html)；
    
2.  完成商户入网且开通微信扫码业务；具体参考 [商户进件](https://paas.huifu.com/doc/lightning/#/guide/jinjian/shanghujj_intro)；
    
3.  完成微信实名认证，配置微信公众号和支付授权目录。具体参考 [商户进件](https://paas.huifu.com/doc/lightning/#/guide/jinjian/shanghujj_intro) 中微信实名认证和微信配置；
    

## 开发接入

查看 [开发指引](https://paas.huifu.com/docs/lightning/#/jsb/zf/wx_fkm_kfzy)

## 分账说明

参考 [订单分账](https://paas.huifu.com/docs/guide/#/zhzjfw/ddfz/ddfz)

## 结算说明

参考 [结算服务](https://paas.huifu.com/doc/guide/#/ythsk/js/zdjs)

## 对账说明

查看 [对账服务](https://paas.huifu.com/docs/guide/#/ythsk/dz/dzd) 获取对账信息