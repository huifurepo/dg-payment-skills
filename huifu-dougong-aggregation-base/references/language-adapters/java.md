# Java 适配层

这份文件只讲 Java 接入。  
协议规则不在这里重复写。

## 适配范围

| 项目 | 内容 |
| --- | --- |
| 当前适配 SDK | `dg-lightning-sdk` `1.0.3` |
| 最低运行时 | JDK 1.8+ |
| 初始化入口 | `MerConfig` + `BasePay.initWithMerConfig()` |
| 主要调用方式 | `Factory.Payment.Common()` |

## 先看哪些文件

- [../sdk-quickstart.md](../sdk-quickstart.md)
- [../tech-spec.md](../tech-spec.md)
- [../async-webhook.md](../async-webhook.md)

## Java 特有说明

1. Lightning SDK 的产品号方法名是 `setProductId()`，这里拼写正常。
2. Spring Boot 2.x 和 3.x 的 import 不一样。
   2.x 常见是 `javax.annotation.PostConstruct`
   3.x 常见是 `jakarta.annotation.PostConstruct`
3. 当前仓库的异步通知示例使用了 `fastjson`。
   这是 Java 示例选型，不是协议层要求。
4. `method_expand`、`acct_split_bunch`、`terminal_device_data`、`tx_metadata` 这类字段，仍然建议先在业务层建对象，再在 SDK 边界统一序列化。

## 不属于这里的内容

- 签名规则：看 [../../../huifu-dougong-pay-shared-base/protocol/signing-v2.md](../../../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- 异步通知规则：看 [../../../huifu-dougong-pay-shared-base/protocol/async-notify.md](../../../huifu-dougong-pay-shared-base/protocol/async-notify.md)
- 其他语言入口：看 [../../../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](../../../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md)
