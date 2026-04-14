---
name: huifu-dougong-hostingpay-checkout-js
display_name: 汇付支付斗拱前端收银台 JS SDK
description: "汇付支付托管支付前端收银台 JS SDK Skill：覆盖 @dg-elements/js-sdk 安装、HFPay 初始化、checkout 组件、单支付按钮、createPreOrder 约定、pre_order_type 映射和回调处理。当开发者需要在 H5/PC 页面集成汇付托管收银台前端能力时使用。触发词：JS SDK、前端收银台、HFPay、checkout 组件、微信支付按钮、支付宝支付按钮。"
version: 1.1.0
author: "jiaxiang.li | 内容版权：上海汇付支付有限公司"
homepage: https://paas.huifu.com/open/home/index.html
license: CC-BY-NC-4.0
compatibility:
  - openclaw
dependencies:
  - huifu-dougong-hostingpay-base
  - huifu-dougong-hostingpay-cashier-preorder
metadata:
  openclaw:
    requires:
      config:
        - HUIFU_PROJECT_ID
        - HUIFU_PROJECT_TITLE
        - HUIFU_CALLBACK_URL
---

> **版权声明**：本 Skill 内容来源于上海汇付支付有限公司官方开放平台文档，版权归属上海汇付支付有限公司。如有疑问可咨询汇付支付客服：400-820-2819 / cs@huifu.com
>
> **Source**: Official Open Platform documentation of Shanghai Huifu Payment Co., Ltd.
>
> **Copyright**: Shanghai Huifu Payment Co., Ltd.

---

# 汇付斗拱支付前端收银台 JS SDK

这个 Skill 只负责前端收银台接入。  
服务端预下单、查单和退款，不在这里实现。

> 想看更细的接入边界，请从 [references/README.md](references/README.md) 开始，里面补了主链路、`createPreOrder` 契约、组件模式、回调确认和框架集成提示。

## 适配版本与复核信息

| 项目 | 内容 |
| --- | --- |
| Skill 版本 | `1.1.0` |
| 当前适配 SDK | 收银台 JS SDK `v1.0.0`（npm 包：`@dg-elements/js-sdk`） |
| 最后复核日期 | `2026-04-08` |
| 官方文档来源 | 汇付开放平台收银台 JS SDK 文档、托管支付预下单接口文档 |

## 先分清职责

| 能力 | 对应 Skill | 负责什么 |
| --- | --- | --- |
| 公共凭据、签名、异步通知规则 | [huifu-dougong-hostingpay-base](../huifu-dougong-hostingpay-base/SKILL.md) | 托管支付公共基座 |
| 服务端预下单接口 | [huifu-dougong-hostingpay-cashier-preorder](../huifu-dougong-hostingpay-cashier-preorder/SKILL.md) | 创建 `pre_order_id`、返回 `req_seq_id` / `req_date` |
| 前端收银台 JS SDK | 当前 Skill | 渲染收银台组件、拉起支付、处理前端回调 |
| 支付结果二次确认 | [huifu-dougong-hostingpay-cashier-query](../huifu-dougong-hostingpay-cashier-query/SKILL.md) | 查单确认最终状态 |

## 运行边界

这个 Skill 是前端能力说明。  
它不会持有商户私钥，也不会直接请求汇付签名网关。

前端只做两件事：

1. 调用你自己的服务端 `createPreOrder` 接口
2. 把服务端返回的预下单结果交给 JS SDK

像 `HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 这类密钥，只能留在服务端。  
浏览器端不要放任何签名密钥。

## 协议规则入口

如果你要确认签名和异步通知规则，先看共享资料：

- [signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- [async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md)

## 触发词

- "前端收银台"、"JS SDK"、"HFPay"
- "checkout 组件"、"支付按钮"、"支付宝按钮"、"微信按钮"
- "H5 支付页面"、"PC 收银台"
- "createPreOrder"、"pre_order_type"

## 参考资料地图

- 主链路先看 [references/integration-flow.md](references/integration-flow.md)
- `createPreOrder` 返回格式看 [references/create-preorder-contract.md](references/create-preorder-contract.md)
- 组件模式选择看 [references/component-modes.md](references/component-modes.md)
- 前端 callback 与查单确认边界看 [references/callback-and-confirmation.md](references/callback-and-confirmation.md)
- React / Vue / 原生 JS 集成提示看 [references/framework-integration-notes.md](references/framework-integration-notes.md)

## 适用场景

| 场景 | 用什么组件 | 适合什么情况 |
| --- | --- | --- |
| 完整收银台页面 | `checkout` | 一个区域同时展示多种支付方式 |
| 单独支付宝按钮 | `alipay` | 页面自己排版，只要支付宝入口 |
| 单独微信按钮 | `wechatpay` | 页面自己排版，只要微信入口 |
| 单独云闪付按钮 | `unionpay` | 页面自己排版，只要云闪付入口 |

## 接入顺序

```text
1. 服务端接好 cashier-order 预下单
2. 前端安装 @dg-elements/js-sdk
3. 定义 createPreOrder
4. 初始化 HFPay
5. 渲染 checkout 或单支付按钮
6. 收到回调后调用 cashier-query 做最终确认
```

## 第 1 步：服务端先接好预下单

前端 SDK 不能直接创建支付订单。  
你必须先有自己的服务端接口，并且这个接口内部已经调用：

- [huifu-dougong-hostingpay-cashier-preorder](../huifu-dougong-hostingpay-cashier-preorder/SKILL.md)

服务端接口至少要返回这 4 个字段：

```json
{
  "pre_order_id": "P202604080001",
  "req_seq_id": "202604081530001234",
  "huifu_id": "6666000109133323",
  "req_date": "20260408"
}
```

## 第 2 步：安装 SDK

官方文档当前给出的 npm 安装命令是：

```bash
npm install @dg-elements/js-sdk
```

也可以按官方文档下载浏览器版脚本包。

## 第 3 步：引入 HFPay

官方示例里，初始化入口是 `HFPay`。  
官方文档当前示例安装包名和导入路径写法并不完全一致，示例如下：

```js
import { HFPay } from "dg-element";
```

如果你的工程里安装后导出入口不同，以实际安装结果为准。  
但初始化对象和调用方式，仍然看 `HFPay`。

## 第 4 步：判断环境

如果你要做单支付按钮，建议先判断当前环境。  
官方示例是直接看浏览器 UA。

```js
function isWXJS() {
  return navigator.userAgent.toLowerCase().includes("micromessenger");
}

function isAliPayJS() {
  return navigator.userAgent.toLowerCase().includes("alipayclient");
}

function isUnionPayJS() {
  return navigator.userAgent.toLowerCase().includes("unionpay");
}

function isWebEnv() {
  return !/Android|webOS|iPhone|iPod|Phone|Mobile|OpenHarmony|BlackBerry/i.test(
    navigator.userAgent
  );
}
```

## 第 5 步：定义 `createPreOrder`

`createPreOrder` 是整个前端接入的关键。  
JS SDK 不帮你生成订单，它只会回调你提供的 `createPreOrder` 方法。

### 方法职责

- 向你自己的服务端发起预下单请求
- 服务端内部调用 `cashier-order`
- 把返回值整理成 JS SDK 需要的格式

### 返回格式

必须返回下面这几个字段：

- `pre_order_id`
- `req_seq_id`
- `huifu_id`
- `req_date`

### 示例

```js
async function createPreOrder(selectedType) {
  const requestBody = {
    trans_amt: document.getElementById("amount").value,
    goods_desc: "会员充值",
    pre_order_type: "1",
    hosting_data: {
      project_id: window.__CHECKOUT_PROJECT_ID__,
      project_title: window.__CHECKOUT_PROJECT_TITLE__,
      callback_url: window.__CHECKOUT_CALLBACK_URL__,
    },
  };

  if (isAliPayJS() || isWXJS() || isUnionPayJS() || isWebEnv()) {
    requestBody.pre_order_type = "1";
  } else if (selectedType === "alipay") {
    requestBody.pre_order_type = "2";
    requestBody.app_data = {
      app_schema: "your-app-schema",
    };
  } else if (selectedType === "wechatpay") {
    requestBody.pre_order_type = "3";
    requestBody.miniapp_data = {
      need_scheme: "Y",
    };
  }

  const response = await fetch("/api/hostingpay/preorder", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  const data = await response.json();
  return {
    pre_order_id: data.pre_order_id,
    req_seq_id: data.req_seq_id,
    huifu_id: data.huifu_id,
    req_date: data.req_date,
  };
}
```

## `pre_order_type` 和服务端场景的对应关系

这里一定要和服务端 `cashier-order` 对齐。

| `pre_order_type` | 服务端场景 | 什么时候用 |
| --- | --- | --- |
| `1` | H5 / PC 预下单 | H5 页面、PC 页面，或当前环境已经在支付 App 内 |
| `2` | 支付宝小程序预下单 | 非支付宝内环境下，前端决定走支付宝托管小程序 |
| `3` | 微信小程序预下单 | 非微信内环境下，前端决定走微信托管小程序 |

有两个要点：

1. `pre_order_type` 不是前端随便写的，它决定服务端走哪一类预下单报文
2. 前端一旦切换支付方式，服务端也要跟着切到对应的 `app_data` 或 `miniapp_data`

## 第 6 步：初始化 `HFPay`

```js
const { error, hfPay } = await HFPay();

if (error) {
  throw error;
}
```

如果这里初始化失败，直接在前端报错并停止。  
不要伪造一个“默认可支付”的降级流程。

## 第 7 步：渲染 `checkout` 组件

完整收银台适合一个区域承载多种支付方式。

```js
function callback(result) {
  console.log("checkout callback:", result);
}

const element = hfPay.component("checkout", {
  createPreOrder,
  callback,
});

if (element) {
  element.mount("#checkout-container");
}
```

## 第 8 步：渲染单支付按钮

如果你只想展示一个支付按钮，可以直接传组件类型：

- `alipay`
- `wechatpay`
- `unionpay`

```js
const wechatButton = hfPay.component("wechatpay", {
  createPreOrder,
  callback,
});

if (wechatButton) {
  wechatButton.mount("#wechat-button");
}
```

## 回调怎么处理

官方公开示例里，回调结构是这样的：

```json
{
  "type": "payment_data",
  "data": {
    "transStat": "1",
    "huifuId": "6666000109133323",
    "reqSeqId": "1753150933645",
    "reqDate": "20250722",
    "respDesc": "操作成功"
  }
}
```

### 建议处理方式

| 前端状态 | 怎么处理 |
| --- | --- |
| SDK 初始化失败 | 直接提示用户，阻断支付入口 |
| 拉起失败 / 环境不支持 | 前端提示错误，可允许重试 |
| 收到 `payment_data` | 记录 `reqSeqId` / `reqDate`，然后调用后端查单 |
| 用户主动关闭或取消 | 只更新前端提示，不直接改业务订单状态 |

这里最重要的一点是：

**前端回调不等于最终支付成功。**

页面侧拿到成功提示后，后端仍然要调用：

- [huifu-dougong-hostingpay-cashier-query](../huifu-dougong-hostingpay-cashier-query/SKILL.md)

去查最终状态。

## H5 和 PC 的展示差异

| 环境 | 常见表现 |
| --- | --- |
| H5 浏览器 | 根据环境展示对应支付方式，必要时跳转托管小程序 |
| 支付 App 内 | 一般只展示当前环境支持的支付方式 |
| PC 浏览器 | 常见是展示支付二维码，用户手机扫码完成支付 |

前端页面看到的表现会变，但 `createPreOrder -> HFPay -> callback -> 查询确认` 这条主链路不变。

## 常见坑

1. 前端直接请求汇付网关。这样做不对。预下单必须走你自己的服务端。
2. 浏览器里放 RSA 私钥。这样做不允许。
3. `pre_order_type` 和服务端场景没对齐。结果会导致预下单报文和前端拉起方式不匹配。
4. 只看前端回调，不做后端查单。这样很容易把处理中误判成成功。
5. 页面里自己拼假的 `pre_order_id`。这个值必须来自服务端真实预下单结果。

## 参考入口

| 文件 | 用途 |
| --- | --- |
| [references/README.md](references/README.md) | checkout-js 补充阅读地图 |
| [references/integration-flow.md](references/integration-flow.md) | 前端页面、服务端预下单、JS SDK、查单确认主链路 |
| [references/create-preorder-contract.md](references/create-preorder-contract.md) | `createPreOrder` 契约、返回格式与 `pre_order_type` 决策 |
| [references/component-modes.md](references/component-modes.md) | `checkout` 与单支付按钮模式选择 |
| [references/callback-and-confirmation.md](references/callback-and-confirmation.md) | 前端 callback 与最终状态确认边界 |
| [references/framework-integration-notes.md](references/framework-integration-notes.md) | React / Vue / 原生 JS 集成提示 |
| [../huifu-dougong-pay-shared-base/runtime/frontend-sdk-matrix.md](../huifu-dougong-pay-shared-base/runtime/frontend-sdk-matrix.md) | 前端 SDK 能力矩阵 |
| [../huifu-dougong-pay-shared-base/protocol/signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md) | 协议签名规则 |
| [../huifu-dougong-pay-shared-base/protocol/async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md) | 异步通知规则 |
| [../huifu-dougong-hostingpay-cashier-preorder/SKILL.md](../huifu-dougong-hostingpay-cashier-preorder/SKILL.md) | 服务端预下单 |
| [../huifu-dougong-hostingpay-cashier-query/SKILL.md](../huifu-dougong-hostingpay-cashier-query/SKILL.md) | 支付后查单确认 |

---

> 版权声明与联系方式见 [copyright-notice.md](../huifu-dougong-pay-shared-base/governance/copyright-notice.md)
