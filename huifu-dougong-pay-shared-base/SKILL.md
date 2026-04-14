---
name: huifu-dougong-pay-shared-base
display_name: 汇付支付斗拱共享基础资料
description: "汇付支付斗拱共享基础资料 Skill：集中收纳签名规则、异步通知规则、服务端多语言 SDK 矩阵、前端 JS SDK 矩阵和发布治理清单。适合作为聚合支付与托管支付两个体系的公共入口。触发词：签名规则、异步通知、多语言 SDK、发布检查、共享基础资料。"
version: 1.1.0
author: "jiaxiang.li | 内容版权：上海汇付支付有限公司"
homepage: https://paas.huifu.com/open/home/index.html
license: CC-BY-NC-4.0
compatibility:
  - openclaw
---

> **版权声明**：本 Skill 内容来源于上海汇付支付有限公司官方开放平台文档，版权归属上海汇付支付有限公司。如有疑问可咨询汇付支付客服：400-820-2819 / cs@huifu.com
>
> **Source**: Official Open Platform documentation of Shanghai Huifu Payment Co., Ltd.
>
> **Copyright**: Shanghai Huifu Payment Co., Ltd.

---

# 汇付斗拱支付共享基础资料

这个 Skill 不负责某一个具体接口。  
它负责放两条支付路径都会反复用到的公共资料，也是整个仓库的共享协议 / 治理 / 契约入口。

## 适配版本与复核信息

| 项目 | 内容 |
| --- | --- |
| Skill 版本 | `1.1.0` |
| 当前适配范围 | 聚合支付 + 托管支付共享协议层、运行时矩阵、治理清单 |
| 最后复核日期 | `2026-04-08` |
| 官方文档来源 | 汇付开放平台加验签说明、异步消息说明、Java SDK 文档、收银台 JS SDK 文档 |

## 适用场景

| 你要解决什么 | 先看哪里 |
| --- | --- |
| 从 README 选择产品线 / 开发任务 / 技术栈后的共享入口 | 当前 Skill |
| 签名规则 | [protocol/signing-v2.md](protocol/signing-v2.md) |
| 异步通知规则 | [protocol/async-notify.md](protocol/async-notify.md) |
| 服务端多语言 SDK 入口 | [runtime/server-sdk-matrix.md](runtime/server-sdk-matrix.md) |
| 前端 JS SDK 入口 | [runtime/frontend-sdk-matrix.md](runtime/frontend-sdk-matrix.md) |
| 发布前检查 | [governance/release-checklist.md](governance/release-checklist.md) |
| 版本治理 | [governance/versioning-policy.md](governance/versioning-policy.md) |

## 这份 Skill 的定位

它是共享资料层，也是整个仓库的公共契约入口。  
README 负责帮助你先按产品线、开发任务、技术栈选择入口；一旦确定了方向，就应该先回到这里确认共享协议、运行时矩阵和发布治理规则。

对应的两条基础入口是：

- [../huifu-dougong-aggregation-base/SKILL.md](../huifu-dougong-aggregation-base/SKILL.md)
- [../huifu-dougong-hostingpay-base/SKILL.md](../huifu-dougong-hostingpay-base/SKILL.md)

## 推荐阅读顺序

```text
1. 先从 README 选择产品线 / 开发任务 / 技术栈
2. 再看 shared-base 中的协议规则、运行时矩阵和治理清单
3. 最后进入对应 scenario skill
```

## 目录说明

### `protocol/`

- `signing-v2.md`：V2 签名和验签规则
- `async-notify.md`：异步通知、幂等、应答格式和回调限制

### `runtime/`

- `server-sdk-matrix.md`：Java、PHP、C#、Python、Go 服务端 SDK 矩阵
- `frontend-sdk-matrix.md`：前端 JS SDK 矩阵，说明商户侧页面如何承接组件化收银台

### `governance/`

- `versioning-policy.md`：版本治理规则
- `release-checklist.md`：发布自检清单

## 阅读顺序

```text
1. 先从 README 选择产品线 / 开发任务 / 技术栈
2. 再看 protocol/
3. 接着看 runtime/
4. 最后按业务进入 aggregation / hostingpay skill
```

## 使用边界

1. 这份 Skill 只提供共享资料，不持有任何商户密钥。
2. 这份 Skill 不是业务接口 skill，不直接回答具体下单字段怎么传。
3. 如果进入具体业务场景，要继续看对应的 order / query / refund skill。

---

> 版权声明与联系方式见 [copyright-notice.md](governance/copyright-notice.md)
