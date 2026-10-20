# 银联正扫支付

指商家在银联侧下单生成订单二维码，用户使用云闪付APP“扫一扫”完成付款的一款支付产品。

## 使用示例

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/81ecdd51-46f7-4a00-a141-1d394b65ee19.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/b923d936-5643-4df5-91f7-b09caeb60649.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/1d9e0dfc-98f0-4921-8e6a-82291c3d15c1.png" alt="BlockNote image" width="200" />

## **适用场**景

主要适用于实体店单品或订单、媒体广告支付等场景。

## 体验demo

点击 [斗拱收款演示网站](https://paas.huifu.com/docs/start/#/product_demo) 体验完整产品流程

## 业务流程说明

### 支付

1.  商家调用【聚合支付】接口指定“交易类型：银联正扫支付”下单，下单时可根据业务场景需要指定（指定收款子账户等），提交对应指令；
    
2.  下单成功会返回该订单的二维码链接串，商户系统需要通过二维码生成工具获得最终的订单二维码图片，用于消费者扫描购买；
    
3.  消费者使用云闪付APP“扫一扫”进行扫码后，进入到支付确认界面，消费者可在该页面确认支付信息；
    
4.  消费者确认订单收款方和金额无误后，提交付款会出现验密界面(验证密码或指纹等)；
    
5.  支付成功后会弹出成功页面，支付失败会弹出错误提示；
    
6.  针对交易结果，系统会通过异步消息的方式推送商户系统，若未收到推送时，商户也可调用【聚合交易查询】接口主动发起查询；
    

注：

*   生成的二维码被扫过一次后，订单即会创建，不能再次被扫。
    
*   若消费者实际未支付，按系统的轮询保障机制规则，消费者扫码2小时后将交易状态置为失败；
    

### 退款

1.  退款交易支持全额/部分退款，退款期限：360天；
    
2.  退款时手续费会一并退还；
    
3.  退款资金将原路退还至消费者，若商户原交易的收款账户余额不足，则退款失败；
    
4.  针对退款交易结果，系统会通过消息推送通知商户系统，若未收到推送时，商户也可主动发起退款交易查询；
    

## 计费规则

手续费收取，支持按比例收取且支持最低手续费。

退款时退还交易手续费，计算方式向下取整，最后一笔轧差。

## 开通功能和准备材料

1.  完成商户入网且开通银联二维码扫码业务；具体参考 [商户进件](https://paas.huifu.com/doc/lightning/#/guide/jinjian/shanghujj_intro)；
    

## 支付接入

查看 [开发指引](https://paas.huifu.com/docs/lightning/#/jsb/zf/yl_zs_kfzy)

## 分账说明

参考 [订单分账](https://paas.huifu.com/docs/guide/#/zhzjfw/ddfz/ddfz)

## 结算说明

参考 [结算服务](https://paas.huifu.com/doc/guide/#/ythsk/js/zdjs)

## 对账说明

查看 [对账服务](https://paas.huifu.com/docs/guide/#/ythsk/dz/dzd) 获取对账信息