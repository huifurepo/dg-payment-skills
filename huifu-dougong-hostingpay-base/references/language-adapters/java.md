# Java 适配层

这份文件只讲 Java 接入。  
协议规则不在这里重复写。

## 适配范围

| 项目 | 内容 |
| --- | --- |
| 当前适配 SDK | `dg-java-sdk` `3.0.34`（当前仓库示例基线） |
| 官方文档最新版本 | Java SDK 文档 2026-04-01 已更新到 `3.0.35` |
| 最低运行时 | JDK 1.8+ |
| 初始化入口 | `MerConfig` + `BasePay.initWithMerConfig()` |
| 主要调用方式 | `BasePayClient.request()` |

## 先看哪些文件

- [../sdk-quickstart.md](../sdk-quickstart.md)
- [../tech-spec.md](../tech-spec.md)
- [../async-webhook.md](../async-webhook.md)
- [../../../huifu-dougong-hostingpay-cashier-refund/SKILL.md](../../../huifu-dougong-hostingpay-cashier-refund/SKILL.md)

## Java 特有说明

1. 设置产品号的方法名是 `setProcutId()`。
   这是 SDK 原生方法名，不要改写成 `setProductId()`。
2. Spring Boot 2.x 和 3.x 的 import 不一样。
   2.x 常见是 `javax.*`
   3.x 常见是 `jakarta.*`
3. 当前仓库的异步通知示例使用了 `fastjson`。
   这是 Java 示例选型，不是协议层要求。
4. 有些字段没有独立 setter，要通过 `extendInfoMap` 传入。
5. 退款场景的 `org_req_seq_id` 就属于这一类。
   这个坑已经在退款 skill 里单独标出。

## 不属于这里的内容

- 签名规则：看 [../../../huifu-dougong-pay-shared-base/protocol/signing-v2.md](../../../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- 异步通知规则：看 [../../../huifu-dougong-pay-shared-base/protocol/async-notify.md](../../../huifu-dougong-pay-shared-base/protocol/async-notify.md)
- 其他语言入口：看 [../../../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](../../../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md)
