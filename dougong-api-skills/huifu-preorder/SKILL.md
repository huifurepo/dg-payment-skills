---
name: huifu-preorder
description: "[后端项目使用]汇付H5/PC预下单接口技能。用于创建支付预订单，返回支付页面URL。当用户提到预下单、支付预下单、托管支付、/hfpay/preOrder时触发。"
---

# 汇付预下单接口

## 引导词

当开发者提到以下关键词时，本技能将被触发：

- 预下单、支付预下单、托管支付
- /hfpay/preOrder
- 汇付预支付、创建支付订单
- 托管支付预下单

## 前置检查（重要）

在开始编写代码之前，必须先检查项目是否已安装汇付SDK依赖。

### 步骤1：检查依赖

检查项目的 pom.xml 文件中是否包含 `dg-java-sdk` 依赖：

```xml
<dependency>
    <groupId>com.huifu.bspay.sdk</groupId>
    <artifactId>dg-java-sdk</artifactId>
    <version>3.0.34</version>
</dependency>
```

### 步骤2：安装依赖（如未安装）

如果项目中没有该依赖，需要先在 pom.xml 中添加上述依赖，然后执行 Maven 安装：

```bash
mvn clean install
```

或在 IDE 中刷新 Maven 项目。

### 步骤3：验证依赖

确认以下类可以正常导入：
- `com.huifu.bspay.sdk.opps.core.BasePay`
- `com.huifu.bspay.sdk.opps.core.config.MerConfig`
- `com.huifu.bspay.sdk.opps.client.BasePayClient`
- `com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentPreorderH5Request`
- `com.huifu.bspay.sdk.opps.core.utils.DateTools`
- `com.huifu.bspay.sdk.opps.core.utils.SequenceTools`

**只有完成以上前置检查后，才能继续按照 reference 目录中的示例代码进行开发。**

## 接口说明

| 属性 | 值 |
|-----|-----|
| 接口路径 | `/hfpay/preOrder` |
| 请求方式 | POST |
| Content-Type | application/json |
| 汇付API端点 | `v2/trade/hosting/payment/preorder` |

## 功能说明

创建支付预订单，返回支付页面URL或支付参数，用于后续支付流程。

## 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| huifuId | String | 是 | 商户号 |
| transAmt | String | 是 | 交易金额（单位：元） |
| goodsDesc | String | 是 | 商品描述 |

## 架构设计

采用分层架构实现：

```
Controller层 (HFPayController)
    ├── 初始化商户配置 (MerConfig)
    ├── 调用Service层方法
    └── 返回统一响应结果

Service层 (HostingpayService)
    ├── 组装SDK Request对象
    ├── 调用汇付API (BasePayClient.request)
    └── 异常处理与业务逻辑

DTO层
    └── HostingpayPreOrderReq: 请求参数封装
```

## 实现步骤

1. 创建请求DTO类 `HostingpayPreOrderReq`
2. 在Service层实现 `preOrder` 方法
3. 在Controller层注入Service并调用

## 代码示例

详见 reference 目录下的示例代码文件。

## 注意事项

1. pre_order_type 参数说明：
   - 1：H5/PC预先下单
   - 2：支付宝小程序
   - 3：微信小程序
2. 需要正确配置 notify_url 以接收支付结果异步通知
3. hosting_data 为半支付托管扩展参数，需根据实际项目配置
4. 使用 `V2TradeHostingPaymentPreorderH5Request` 对象组装请求参数
5. 通过 `BasePayClient.request()` 方法发起API调用
