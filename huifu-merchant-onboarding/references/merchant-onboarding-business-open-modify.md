# 商户业务开通修改

## 适用范围

用于企业或小微商户进行微信/支付宝补开、部分线上业务开通，或修改已开通支付能力的参数和费率。官方来源：[商户业务开通修改](https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md)，锁定来源 SHA-256 为 `fdeaaa0a40556046d817c70a46c2fe1c71756f8648ffe640db6585ca6f5963a3`。银联、银行卡业务开通仍使用 `merchant-onboarding-business-open.md`；不能把所有“已开通后的补开”统一路由到本接口。

本接口不是首次基础进件，也不是支付下单接口。首次业务开通以及银联、银行卡业务开通使用 `merchant-onboarding-business-open.md`；支付交易交给 `$huifu-pay-integration`。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/modify`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`。
- 同步响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共 434 个节点：请求 372、同步响应 6、异步通知 56。50 组嵌套表、完整路径、类型、长度、Y/N/C 和经过固定规范化、敏感示例脱敏的官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户业务开通修改”；下载原始字节保存在仓库维护来源锁中，不进入发布包。
- 请求 `data.req_seq_id:String(32) Y`、`data.req_date:String(8) Y`、`data.huifu_id:String(18) Y`。其余能力、费率、协议、材料和渠道配置必须按调用方实际修改目标取值，不得从首次开通请求或详情响应整包复制。

## 修改语义与方向隔离

- 本接口用于“修改已开通能力”；同步 `resp_code` 成功只表示本次请求受理或处理结果，不能直接解释为全部能力已可交易。
- `data.async_return_url:String(128) N` 接收申请审核结果；`data.busi_async_return_url:String(128) N` 接收逐业务开通结果；电子协议通知地址位于 `data.agreement_info.agreement_async_return_url`。
- `data.recon_resp_addr:String(256) N` 是交易异步应答地址，不是本接口审核回调，也不能套用支付通知终态逻辑。
- 审核通知、逐业务通知和电子协议通知是三个方向。字段必须分别使用 `async.audit.*`、`async.business.*` 和 `async.agreement.*` 路径。
- 逐业务通知存在 `async.business.ord_id:String(44) N` 时，官方说明的应答是 `RECV_ORD_ID_` + `ord_id`；不得外推到审核或电子协议通知。
- 逐业务通知的 `async.business.reg_result_list[]` 是数组；官网把 `jsonArray` 误拼为 `josnArray`，完整目录已按“集合可能有多条数据”的同一行说明恢复 `[]`，不得扁平化其 14 个子字段。
- `async.business.huifu_id:String(18) Y` 按字段名和中文名是商户号，但官网说明与示例误写为产品号 `YYZY`；标记 `[官方文档口径冲突]`，禁止采用该示例生成或覆盖商户号。
- 电子协议通知的父字段只定义为 `String`，完整路径为 `async.agreement.agreement_info_list.con_stat`；不得因 `_list` 名称或申请状态查询中的同名数组而添加 `[]`。

## 字段生成规则

1. 先在完整字段目录定位本次要修改的能力父对象，再读取该对象全部叶子。
2. 保留官方 `String(JSON Object/Array)` 形态；路径仅在官方类型或说明为 `Array/jsonArray` 时带 `[]`。本接口唯一已登记例外是 `async.business.reg_result_list[]`：原文误拼 `josnArray`，并在同一行明确“集合可能有多条数据”；该例外不得外推。
3. `online_flag/quick_flag/withhold_flag` 仍使用字符串 `Y/N`；不得复制详情查询响应中的 `1/0/空`。
4. 费率、MCC、商户简称、外扣承担方、渠道配置和材料均由调用方或运营提供；官网示例不是默认值。
5. 字段说明命中编码表、XLSX、协议或其他页面时，同时读取 `merchant-onboarding-external-resources.md` 并输出未经改写的原始地址。

## 公共请求头

- `jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.0.1`，双 Skill 默认 `hfps/1.3.4;hfms/1.0.1`。

## SDK 证据

用户提供且已锁定源码树摘要的 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24` 均存在对应封装：

- Java / PHP：`V2MerchantBusiModifyRequest`
- Python：`V2MerchantBusiModifyRequest`，模块 `v2_merchant_busi_modify_request.py`

SDK 类存在只证明路由和请求封装可用，不证明商户权限、费率、材料或审核结果。Java 代码仍必须在任何 SDK 请求前全局设置 `BasePay.debug = false;`。

## 通知边界

除上述 `ord_id` 应答规则外，通知验签原文、HTTP 编码、超时、重试及审核/电子协议 ACK 均为 `[需要官方确认]`。未获得官方脱敏样本前不得生成回调实现。
