# 后端调用汇付斗拱sdk技能目录

本目录包含汇付托管支付相关的三个技能接口，供开发者在不同场景下使用。

## 技能列表

| 技能                                       | 功能 | 引导关键词 | 接口路径 |
|------------------------------------------|------|-----------|---------|
| [huifu-preorder](./huifu-preorder)       | 预下单 - 创建支付预订单，返回支付页面URL | 预下单、支付预下单、托管支付、/hfpay/preOrder | `/hfpay/preOrder` |
| [huifu-order-query](./huifu-order-query) | 订单查询 - 查询订单支付状态和详细信息 | 订单查询、支付查询、查询订单、/hfpay/queryorderinfo | `/hfpay/queryorderinfo` |
| [huifu-htRefund](./huifu-refund)         | 退款 - 对已支付订单发起退款申请 | 退款、支付退款、订单退款、refund、htRefund | `/hfpay/htRefund` |

## 通用前置检查

使用任何技能前，需确保项目已安装汇付SDK依赖：

```xml
<dependency>
    <groupId>com.huifu.bspay.sdk</groupId>
    <artifactId>dg-java-sdk</artifactId>
    <version>${dg-java-sdk.version}</version>
</dependency>
```

安装后执行 `mvn clean install` 刷新项目。

## 使用场景说明

| 场景 | 使用技能              |
|-----|-------------------|
| 用户发起支付，创建预订单 | huifu-preorder    |
| 查询订单支付状态 | huifu-order-query |
| 支付成功后需要退款 | huifu-htRefund    |

## 技能详情

各技能的详细说明、请求参数、实现步骤请查看对应目录下的 `SKILL.md` 文件。
