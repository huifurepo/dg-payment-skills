# 凭据使用规则与存放边界

本文档适用于所有业务 Skill（聚合支付和托管支付）。

## 凭据角色说明

业务 Skill 的 metadata 中列出的 `HUIFU_PRODUCT_ID`、`HUIFU_SYS_ID`、`HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 等配置项，用于让**接入方应用**在运行时完成汇付 SDK 初始化，并在应用侧完成请求签名和响应验签。

## 存放边界

- 本仓库内的 Skill 均为**文档型 Skill**，只声明接入方应用需要准备哪些配置
- Skill 包内不会保存、落库、缓存、回传、打印或持久化任何商户凭据
- 安装或阅读 Skill 不会触发任何凭据采集、网络上传、文件写入或本地持久化动作
- 真实使用发生在接入方应用代码运行时

## 接入方应做到

- 凭据应由接入方项目的环境变量、CI/CD Secret 或密钥管理系统持有
- 开发和联调阶段务必使用联调专用密钥，不要提供生产密钥
- 日志中避免打印完整密钥信息
- RSA 私钥切勿上传到代码仓库
- 上线前应确认生产密钥只存在于受控运行环境中

## 语言适配说明

当前仓库内的完整代码示例以 Java 为主，其他语言先通过基础 Skill 的语言适配入口接入。详见 [server-sdk-matrix.md](../runtime/server-sdk-matrix.md)。

## metadata 中 config 声明的设计说明

业务 Skill 的 metadata 中会重复列出基础 Skill 已声明的配置项。这是有意为之：部分 Skill 平台在解析依赖时不会自动合并上游 config 需求，重复声明保证单独安装某个业务 Skill 时平台也能正确提示所需配置。
