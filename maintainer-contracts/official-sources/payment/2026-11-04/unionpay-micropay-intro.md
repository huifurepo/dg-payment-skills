# 银联付款码支付

消费者打开云闪付客户端展示付款码，商户使用扫码设备扫描该付款码后完成扣款的支付场景。

## 使用示例

免密支付

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/ca7d12f9-ba8b-4e14-b62a-55436ccf4f12.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/8d9bb197-7fbf-43a1-be26-a1ee126df9cd.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/f429521b-27f4-4e92-81c0-16528a63f632.png" alt="BlockNote image" width="200" />

验密支付

<img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/011f3fab-f552-4a96-875d-c16c503ae4b7.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/b4000f59-952c-4ae9-8080-c1b1f0c10db6.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/3b90ca61-c80d-4eaa-a94a-32db4382fa8b.png" alt="BlockNote image" width="200" /><img src="https://jfile.cloudpnr.com/app-311617f2-d414-4fac-bf65-c0a729310072/14f6afd2-1e32-4702-a49e-961c0835d79a.png" alt="BlockNote image" width="200" />

## 适用场景

主要适用于线下场所面对面收银的场景，例如：便利店、商超综合体、餐饮、医院、学校、电影院、旅游景区等具有明确经营地址的实体场所。付款码支付分为免密支付场景和验密支付场景：

**免密支付场景**

即商户扫描消费者付款码发起扣款后，消费者无需输入密码，扣款直接完成；

**验密支付场景**

即商户扫描消费者付款码发起扣款后，消费者侧需要输入密码核验后，扣款才能完成；

## 体验demo

点击 [斗拱收款演示网站](https://paas.huifu.com/docs/start/#/product_demo) 体验完整产品流程

## 业务流程说明

### 支付

1.  消费者选择付款码支付，预先打开云闪付APP内的付款码；
    
2.  收银员在商户系统操作生成支付订单，用户确认核对支付金额；
    
3.  商户收银员用扫码设备扫描用户的条码/二维码，商户收银系统提交支付；
    
4.  商户侧调用【聚合支付】接口指定“交易类型：银联反扫支付”下单，下单时可根据业务场景需要指定（指定收款子账户等），提交对应指令；
    
5.  下单成功后，银联支付后台系统收到支付请求，根据验证密码规则判断是否验证消费者的支付密码，不需要验证密码的交易直接发起扣款，需要验证密码的交易会弹出密码输入框；
    
6.  支付成功后会弹出成功页面，支付失败会弹出错误提示；
    
7.  针对交易结果，系统会通过异步消息的方式推送商户系统，若未收到推送时，商户也可调用【聚合交易查询】接口主动发起查询。
    

注：若消费者实际未支付，按系统的轮询保障机制规则，24小时后将交易状态置为失败。

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

查看 [开发指引](https://paas.huifu.com/open/doc/lightning/#/guide/zf/yl_kfm_kfzy)

## 分账说明

参考 [订单分账](https://paas.huifu.com/docs/guide/#/zhzjfw/ddfz/ddfz)

## 结算说明

参考 [结算服务](https://paas.huifu.com/docs/guide/#/ythsk/js/zdjs)

## 对账说明

查看 [对账服务](https://paas.huifu.com/docs/guide/#/ythsk/dz/dzd) 获取对账信息