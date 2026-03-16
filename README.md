# 斗拱接口skills v1.0使用指引

本指南将帮助你快速上手使用汇付斗拱接口 Skills，实现高效的业务对接。

---

## 一、Skills 简介

Skills 是基于 AI 大模型的代码生成技能，可以根据你的自然语言需求，自动生成符合项目规范的接口调用代码。

### 技能包分类

| 技能包 | 适用场景 | 技术栈 | 推荐程度 |
| --- | --- | --- | --- |
| **dougong-api-skills** | 后端接口对接 | Java | 强烈推荐安装 |
| **dougong-web-skills** | 前端调用后端 API | JS/Vue/React | 按需选装 |

### 技能清单

#### 后端 Skills（Java）

| 技能 | 功能 | 触发关键词 |
| --- | --- | --- |
| huifu-preorder | H5/PC 预下单接口 | 预下单、支付预下单、托管支付、/hfpay/preOrder |
| huifu-order-query | 托管交易查询 | 订单查询、支付查询、查询订单、/hfpay/queryorderinfo |
| huifu-refund | 托管交易退款 | 退款、支付退款、订单退款、/hfpay/htRefund |

#### 前端 Skills（可选）

| 技能 | 功能 | 框架支持 |
| --- | --- | --- |
| huifu-prepay-api | 预下单前端调用 | JavaScript / Vue3 / React |
| huifu-query-api | 交易查询前端调用 | JavaScript / Vue3 / React |
| huifu-refund-api | 退款前端调用 | JavaScript / Vue3 / React |

---

## 二、安装配置

### 手动安装

将 Skills 目录复制到 AI 工具的技能目录：

| AI 工具 | 安装路径 |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Trae | `~/.trae/skills/` |
| OpenClaw | `~/.openclaw/workspace/skills` |

```bash
# 示例：将 skills 复制到 Claude Code
cp -r dougong-api-skills ~/.claude/skills/
cp -r dougong-web-skills ~/.claude/skills/

```

### 验证安装

安装完成后，在 AI 对话中输入 `/` 或 `@`，搜索 "huifu" 或 "斗拱"，确认技能已被识别。

---

## 三、快速开始

### 后端对接示例

**场景：需要在项目中接入汇付支付预下单功能**

在 AI 工具中直接描述你的需求：

```plaintext
我需要接入汇付支付预下单接口，创建支付预订单

```

AI 会自动触发 `huifu-preorder` 技能，按以下流程帮助你：

1.  **前置检查** - 确认项目已安装 `dg-java-sdk` 依赖
    
2.  **代码生成** - 根据项目实际情况生成适配代码
    
3.  **参数替换** - 你只需要替换商户号、密钥信息，金额等关键参数
    

### 前端对接示例

**场景：前端需要调用支付预下单接口**

```plaintext
请帮我生成调用汇付预下单API的前端代码，使用Vue3

```

AI 会自动使用 `huifu-prepay-api` 技能生成对应的 Vue3/React/JavaScript 代码。

---

## 四、目录结构

```plaintext
汇付开发skill技能/
├── 斗拱接口skills v1.0使用指引.md    # 本文件
├── dougong-api-skills/              # 后端技能包
│   ├── README.md
│   ├── huifu-preorder/              # 预下单技能
│   │   ├── SKILL.md                 # 技能定义文件
│   │   └── reference/               # 参考示例
│   │       ├── HFPayController.java
│   │       ├── HostingpayPreOrderReq.java
│   │       └── Result.java
│   ├── huifu-order-query/           # 订单查询技能
│   │   ├── SKILL.md
│   │   └── reference/
│   └── huifu-refund/                # 退款技能
│       ├── SKILL.md
│       └── reference/
│
└── dougong-web-skills/              # 前端技能包
    ├── README.md
    ├── huifu-prepay-api/            # 预下单前端
    │   ├── SKILL.md
    │   └── reference/
    │       ├── javascript-example.md
    │       ├── vue3-example.md
    │       └── react-example.md
    ├── huifu-query-api/             # 查询前端
    │   ├── SKILL.md
    │   └── reference/
    └── huifu-refund-api/            # 退款前端
        ├── SKILL.md
        └── reference/

```
---

## 五、常见问题

### Q1: Skills 触发不了怎么办？

1.  确认 Skills 已正确安装到对应目录
    
2.  重启 AI 工具使其加载新技能
    
3.  使用明确的触发关键词（见技能清单）
    
### Q2: 生成的代码报依赖错误？

后端 Skills 使用前需要确认项目已安装汇付 SDK：

```xml
<!-- pom.xml -->
<dependency>
    <groupId>com.huifu.bspay.sdk</groupId>
    <artifactId>dg-java-sdk</artifactId>
    <version>${dg-java-sdk.version}</version>
</dependency>

```

### Q3: 前端代码需要安装额外依赖吗？

前端 Skills 生成的代码基于原生 `fetch` 或对应框架的标准写法，通常不需要额外安装依赖。

---

## 六、使用优势

相比传统 SDK 对接，Skills 的优势：

1.  **智能适配** - AI 根据你项目的实际情况调整代码
    
2.  **降低心智负担** - 无需阅读复杂的 SDK 文档
    
3.  **快速上手** - 只需替换关键业务参数即可使用
    
4.  **前后端一体** - 同时提供后端接口和前端调用示例
    

---

## 七、反馈与支持

如果你在使用过程中遇到问题或有改进建议，请联系汇付技术支持团队。