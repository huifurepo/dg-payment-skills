# 银联 JS 支付

银联JS支付：消费者在银联云闪付客户端内打开商户的H5页面，并在该H5页面拉起云闪付支付收银台完成支付的支付能力。

## 使用示例

线上收银

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/9c535f77-aaf2-402f-acf8-4489da8f7017.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/41c3053a-ecb3-4152-8853-9378474cad3f.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/4f636636-a5d6-4839-99f5-61e4a125e0da.png" alt="BlockNote image" width="200" />

线下收银

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/10f60255-a6d4-4460-8903-c0e6a857938d.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/abc8f2e4-4bc3-4294-bf85-e8c4e6b3af9a.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/065e5d7a-fecf-4463-872b-01072ab8fb54.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/c45dec6c-291c-4860-ab8f-5418627f2099.png" alt="BlockNote image" width="200" />

## 适用场景

基于云闪付客户端内H5页面的产品能力，既可用于线上场景，也可用于线下场景。

注：该H5页面地址需通过银联侧备案。

## 体验demo

点击 [斗拱收款演示网站](https://paas.huifu.com/docs/start/#/product_demo) 体验完整产品流程

## 业务流程说明

### 支付

1.  消费者在银联云闪付客户端浏览器访问商户的网页，选购商品后进入支付环节；
    
2.  消费者提交支付后，商户侧先调用【获取银联用户标识】接口拿到“用户标识”
    
3.  在调用【聚合支付】接口指定传入“交易类型：银联JS支付”下单并传入该“用户标识”，下单时可根据业务场景需要指定（指定收款子账户等），提交对应指令;
    
4.  下单成功后使用支付链接，商户侧拉起支付，进入到云闪付收银台的支付确认界面，消费者可在该页面确认收款方信息和支付金额；
    
5.  消费者确认订单收款方和金额无误后，点击“支付”会出现验密界面(验证密码或指纹等)，同时在该页面也可选择支付方式；
    
6.  验密付款成功后，会展示支付成功页面，以及完成按钮。
    
7.  针对交易结果，系统会通过异步消息的方式推送商户系统，若未收到推送时，商户也可调用【聚合交易查询】接口主动发起查询。
    

注：若消费者实际未支付，按系统的轮询保障机制规则，2小时后将交易状态置为失败。

### 退款

1.  退款交易支持全额/部分退款，退款期限：360天；
    
2.  退款时手续费会一并退还；
    
3.  退款资金将原路退还至消费者，若商户原交易的收款账户余额不足，则退款失败。
    
4.  针对退款交易结果，系统会通过消息推送通知商户系统，若未收到推送时，商户也可主动发起退款交易查询。
    

## 计费规则

手续费收取，支持按比例收取且支持最低手续费。

退款时退还交易手续费，计算方式向下取整，最后一笔轧差。

## 开通功能和准备材料

1.  完成商户入网且开通银联二维码扫码业务；具体参考 [商户进件](https://paas.huifu.com/doc/lightning/#/guide/jinjian/shanghujj_intro)；
    

## 支付接入

查看 [开发指引](https://paas.huifu.com/docs/lightning/#/jsb/zf/yl_js_intro)

## 分账说明

参考 [订单分账](https://paas.huifu.com/docs/guide/#/zhzjfw/ddfz/ddfz)

## 结算说明

参考 [结算服务](https://paas.huifu.com/doc/guide/#/ythsk/js/zdjs)

## 对账说明

查看 [对账服务](https://paas.huifu.com/docs/guide/#/ythsk/dz/dzd) 获取对账信息