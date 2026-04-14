# references

本目录汇总 `huifu-dougong-hostingpay-checkout-js` 的补充参考文档，重点补 checkout-js 最容易接错的几层边界，而不是重复主 `SKILL.md` 的整篇内容。

## 阅读地图

| 文件 | 解决什么问题 |
|------|-------------|
| [integration-flow.md](integration-flow.md) | 前端页面、服务端预下单、JS SDK、查单确认如何串成主链路 |
| [create-preorder-contract.md](create-preorder-contract.md) | `createPreOrder` 的入参、返回字段、`pre_order_type` 决策与常见错误 |
| [component-modes.md](component-modes.md) | `checkout` 与单支付按钮模式怎么选 |
| [callback-and-confirmation.md](callback-and-confirmation.md) | 前端 callback 为什么不能直接当成支付成功 |
| [framework-integration-notes.md](framework-integration-notes.md) | React / Vue / 原生 JS 集成时的最小边界提示 |

## 推荐阅读顺序

1. 先看 [integration-flow.md](integration-flow.md)
2. 再看 [create-preorder-contract.md](create-preorder-contract.md)
3. 根据页面形态看 [component-modes.md](component-modes.md)
4. 支付结果处理看 [callback-and-confirmation.md](callback-and-confirmation.md)
5. 最后按技术栈看 [framework-integration-notes.md](framework-integration-notes.md)

## 与其他 Skill 的关系

- 服务端预下单： [../../huifu-dougong-hostingpay-cashier-preorder/SKILL.md](../../huifu-dougong-hostingpay-cashier-preorder/SKILL.md)
- 服务端查单： [../../huifu-dougong-hostingpay-cashier-query/SKILL.md](../../huifu-dougong-hostingpay-cashier-query/SKILL.md)
- 托管支付公共规则： [../../huifu-dougong-hostingpay-base/SKILL.md](../../huifu-dougong-hostingpay-base/SKILL.md)
- 共享前端矩阵： [../../huifu-dougong-pay-shared-base/runtime/frontend-sdk-matrix.md](../../huifu-dougong-pay-shared-base/runtime/frontend-sdk-matrix.md)
