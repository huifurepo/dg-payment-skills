# 接入流程

接入斗拱支付前，请阅读并按照如下步骤操作

## 步骤一：入网签约

在开发接入前，需按照文档说明在斗拱完成进件签约流程；

商户进件查看：[商户进件指引](https://paas.huifu.com/docs/lightning/#/jsb/jinjian/shanghujj_intro)；

服务商进件查看：[服务商进件指引](https://paas.huifu.com/docs/lightning/#/jsb/jinjian/qudaoshangjj_intro)；

## 步骤二：支付接入

1.  极速版 将几种常用支付产品 API 聚合为一个 [聚合支付 API](https://paas.huifu.com/docs/lightning/#/api/jhzfxd)；
    
2.  以下是聚合支付包含支付产品。可通过阅读不同产品的【产品介绍】，了解产品的适用场景，需要准备的申请材料；可阅读每个产品的【开发指引】进行接入：
    
    *   [微信公众号支付](https://paas.huifu.com/docs/lightning/#/jsb/zf/wx_gzh_intro)
        
    *   [微信小程序支付](https://paas.huifu.com/docs/lightning/#/jsb/zf/wx_xcx_intro)
        
    *   [微信付款码支付](https://paas.huifu.com/docs/lightning/#/jsb/zf/wx_fkm_intro)
        
    *   [支付宝 JS 支付](https://paas.huifu.com/docs/lightning/#/jsb/zf/zfb_js_intro)
        
    *   [支付宝正扫支付](https://paas.huifu.com/docs/lightning/#/jsb/zf/zfb_zs_intro)
        
    *   [支付宝付款码支付](https://paas.huifu.com/docs/lightning/#/jsb/zf/zfb_fkm_intro)
        
    *   [银联 JS 支付](https://paas.huifu.com/docs/lightning/#/jsb/zf/yl_js_intro)
        
    *   [银联正扫支付](https://paas.huifu.com/doc/lightning/#/guide/zf/yl_zs_intro)
        
    *   [银联付款码支付](https://paas.huifu.com/docs/lightning/#/jsb/zf/yl_fkm_intro)
        
3.  可通过 [斗拱收款演示网站](https://paas.huifu.com/docs/start/#/product_demo) 体验不同支付产品流程；
    
4.  斗拱为提升开发者体验和效率，向 AI coding 开发者提供 [支付 skill](https://paas.huifu.com/docs/devtools/#/skillsv1_0) 协助开发；
    
5.  接入过程中如遇到问题，可查看[【帮助中心】](https://paas.huifu.com/help/dev_guide/#/zf/wx/xcx)寻求解决方案，也可使用 [斗拱智能助手](https://paas.huifu.com/ai/chat?marketId=jointdebugging) 快速检索；
    

## 步骤三：后台使用

1.  开发者登录 [开发者工作台](https://paas.huifu.com/open/doc/lightning/#/guide/zf/yl_fkm_intro) 进行开发以及获取平台最新动态。【开发者工作台】提供大量开发所需开发工具，如：密钥信息，日志查询，应用管理等；
    
2.  服务商登录 [合作伙伴控台](https://dashboard.huifu.com/partners/login?from=api) 管理日常业务，开通或变更业务；
    
3.  商户登录 [商户控台](https://dashboard.huifu.com/customers/login?from=api) 管理日常业务，开通或变更业务；