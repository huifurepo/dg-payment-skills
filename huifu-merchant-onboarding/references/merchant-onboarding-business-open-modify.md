# 商户业务开通修改

## 适用范围

用于企业或小微商户进行微信/支付宝/抖音补开、部分线上业务开通，或修改已开通支付能力的参数和费率。官方来源：[商户业务开通修改](https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md)，官网更新时间 `2026-09-24`，本地活动快照 `2026-10-25`，原文 SHA-256 为 `9e70c875accaecb0d25114f38ab80ee6cbfcc6c0a207c0e0176614ff0d7925bb`。银联、银行卡业务开通仍使用 `merchant-onboarding-business-open.md`；不能把所有“已开通后的补开”统一路由到本接口。

本接口不是首次基础进件，也不是支付下单接口。首次业务开通以及银联、银行卡业务开通使用 `merchant-onboarding-business-open.md`；支付交易交给 `$huifu-pay-integration`。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/modify`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`。
- 同步响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共452个节点：请求 390、同步响应 6、异步通知 56。53 组嵌套表、完整路径、类型、长度、Y/N/C 和经过固定规范化、敏感示例脱敏的官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户业务开通修改”；下载原始字节保存在仓库维护来源锁中，不进入发布包。
- 请求 `data.req_seq_id:String(32) Y`、`data.req_date:String(8) Y`、`data.huifu_id:String(18) Y`。其余能力、费率、协议、材料和渠道配置必须按调用方实际修改目标取值，不得从首次开通请求或详情响应整包复制。

## 修改语义与方向隔离

- 本接口用于“修改已开通能力”；同步 `resp_code` 成功只表示本次请求受理或处理结果，不能直接解释为全部能力已可交易。
- `data.async_return_url:String(128) N` 接收申请审核结果；`data.busi_async_return_url:String(128) N` 接收逐业务开通结果；电子协议通知地址位于 `data.agreement_info.agreement_async_return_url`。
- `data.recon_resp_addr:String(256) N` 是交易异步应答地址，不是本接口审核回调，也不能套用支付通知终态逻辑。
- 审核通知、逐业务通知和电子协议通知是三个方向。字段必须分别使用 `async.audit.*`、`async.business.*` 和 `async.agreement.*` 路径。
- 逐业务通知存在 `async.business.ord_id:String(44) N` 时，官方说明的应答是 `RECV_ORD_ID_` + `ord_id`；不得外推到审核或电子协议通知。
- 逐业务通知的 `async.business.reg_result_list[]` 是数组；最新正式类型为Array（说明仍误拼 `josnArray`），目录按正式数组类型保留 `[]`，不得扁平化其 14 个子字段。
- `async.business.huifu_id:String(18) Y` 按字段名和中文名是商户号，但官网说明与示例误写为产品号 `YYZY`；标记 `[官方文档口径冲突]`，禁止采用该示例生成或覆盖商户号。
- 电子协议通知的父字段现定义为 `Object`，完整路径为 `async.agreement.agreement_info_list.con_stat`；不得因 `_list` 名称或申请状态查询中的同名数组而添加 `[]`。

## 字段生成规则

1. 先在完整字段目录定位本次要修改的能力父对象，再读取该对象全部叶子。
2. 保留官方 `String(JSON Object/Array)` 形态；路径仅在官方类型或说明为 `Array/jsonArray` 时带 `[]`。`async.business.reg_result_list[]` 当前已正式声明Array，不再依赖旧版拼写例外。
3. `online_flag/quick_flag/withhold_flag` 仍使用字符串 `Y/N`；不得复制详情查询响应中的 `1/0/空`。
4. 费率、MCC、商户简称、外扣承担方、渠道配置和材料均由调用方或运营提供；官网示例不是默认值。
5. 字段说明命中编码表、XLSX、协议或其他页面时，同时读取 `merchant-onboarding-external-resources.md` 并输出未经改写的原始地址。
6. `wx_zl_conf.wx_zl_pay_conf_list` 当前是String(512) Y且没有JSON格式说明；不得继续沿用旧数组wire，目录不加[]。其新增sales_info.fee_rate_file_list.file_id/file_type必须保留。`jxf_fee_info/split_ext_info/acct_split_bunch_list` 正式类型改为Object但说明仍有JSON字符串/数组描述，逐路径标记冲突。`agreement_info` 为C；多处子字段由Y改N，仍联读条件说明。
7. 捷行付新增字段与首次业务开通保持同路径合同：`bank_name`、`jxf_fee_info` 五个叶字段、`pay_confirm_flag/pay_confirm_req_url` 必须完整读取；四个 `jxf_bank_info` 字段仅在银行非平安时条件必填。`fee_charge_type` 未在正式表定义，不进入 DTO，`quota_issue_fee_rate` 按两位小数正式说明校验。
8. `online_fee_conf_list[].fee_formula_type:String N` 只在代扣开通时传入，枚举限 `01/02/03/04`，不得从其他费率对象复制同名字段。

## 公共请求头

- `jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.1.0`，双 Skill 默认 `hfps/1.5.0;hfms/1.1.0`。

## SDK 证据

用户提供且已锁定源码树摘要的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 均存在对应封装：

- Java / PHP：`V2MerchantBusiModifyRequest`
- Python：`V2MerchantBusiModifyRequest`，模块 `v2_merchant_busi_modify_request.py`

SDK 类存在只证明路由和请求封装可用，不证明商户权限、费率、材料或审核结果。Java 代码仍必须在任何 SDK 请求前全局设置 `BasePay.debug = false;`。

三个生成类均未声明 `jxf_conf_info`、`online_fee_conf_list` 和新增 `dy_conf_list`，通过请求字段白名单的 exact-key 扩展传入；`dy_conf_list` 按当前正式 String/jsonArray 合同整体序列化一层，不能沿用旧版原生数组形态。扩展后合并会覆盖已声明定位字段，必须先拒绝覆盖再发送。

## 通知边界

除上述 `ord_id` 应答规则外，通知验签原文、HTTP 编码、超时、重试及审核/电子协议 ACK 均为 `[需要官方确认]`。按 `shared-overview.md` 的开发提醒引用本页官方来源，建议核对或咨询汇付官方/交流群；继续 Controller 与业务处理框架，未知协议用 TODO/配置隔离，不编造或等待答复才继续整体开发。

## 2026-10-08 字段复核

`request.data.ali_conf_list[].switch_state` 与 `request.data.wx_conf_list[].switch_state` 均由 N 修为 Y；传入对应配置项时必须提供。支付宝项的“默认1”说明已移除，不能再省略后假定开通。该变更只适用于本接口的这两个完整路径，其他配置组以各自正式表为准。
