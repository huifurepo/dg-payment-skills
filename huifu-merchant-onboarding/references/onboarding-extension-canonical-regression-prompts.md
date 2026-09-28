# 进件扩展十二接口回归提示

以下提示逐接口验证 `1.0.3` 新增路由、完整字段目录、SDK 能力和官方冲突边界。文档疑义按 `shared-overview.md` 提醒开发者核对对应官方文档，不清楚时咨询汇付官方或汇付开发者交流沟通群；继续明确部分、用 TODO/配置隔离疑点，不等待回复才开发。每项都应列出实际使用的原子页、`onboarding-extension-complete-field-catalog.md` 与 `onboarding-extension-field-contracts.md`。

### E01 电子合同重发

提示：`用 Java 重发某用户的电子合同，给出生产代码。`

预期：必须读取 onboarding-electronic-contract-resend.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；路由为 POST /v2/agreement/elect/signurl/resend，共13节点=请求9+响应4、无异步；三语言新版 V2InvoiceContractrepeatRequest 仍指向旧 /v2/invoice/contractRepeat，不适用新路由；通过已核验官方 SDK 通用入口调用精确新路径，不得手写 HTTP；resp_code 正式长度8，旧长度冲突关闭。

### E02 电子合同列表查询

提示：`查询电子合同列表，直接按官网示例生成分页 DTO。`

预期：必须读取 onboarding-electronic-contract-list-query.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；路由为 POST /v2/agreement/apply/list，共40节点=请求16+响应24、无异步；正式字段已统一为 page_size/create_time，响应正式包含 total_size/page_num/page_size；resp_code长度8；无协议时 result_list 不返回，不能伪造0或空数组；result_list:String(JSON Array)与原生数组示例仍冲突；新 V2InvoiceQueryecmsapplylistRequest 仍是旧invoice路由，使用已核验官方 SDK 通用入口调用新路径，不得手写生产 HTTP。

### E03 电子合同拒签

提示：`用现有 V2Invoice 类实现合同拒签。`

预期：必须读取 onboarding-electronic-contract-reject.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；路由为 POST /v2/agreement/elect/rejectsign，共12节点=请求8+响应4、无异步；新 V2InvoiceRejectsignRequest 仍指向旧 /v2/invoice/rejectSign，不能用于新路径；使用已核验官方 SDK 通用入口，不得手写 HTTP；resp_code已为8位，旧冲突关闭，不虚构异步通知。

### E04 下级商户权限配置

提示：`为下级商户一次开通所有权限，按文档示例生成请求和响应。`

预期：必须读取 merchant-onboarding-lower-merchant-permission.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/busi/head/config 与 V2MerchantBusiHeadConfigRequest，共141节点=请求132+响应9、无异步；只发送明确选择且有真实来源的能力字段，请求必须含正式必填 data.product_id，不得用外层 product_id 替代；官网误贴的商户详情成功示例不能作为响应合同。

### E05 商户统一页面进件

提示：`生成统一进件页面 URL，并直接实现审核和业务回调。`

预期：必须读取 merchant-onboarding-unified-web.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/url/forward 与 V2MerchantUrlForwardRequest，共59节点=请求17+响应8+异步34；URL 当敏感不透明值；保留响应码、URL长度、审核日期长度冲突；use_chains_flag四值和 head_huifu_id:C 已明确，旧冲突关闭；回调 ACK、验签原文、HTTP、重试和超时未明确时继续生成框架与已知状态逻辑，未知协议留 TODO/配置并提示查文档或咨询，不虚构协议。

### E06 统一页面进件查询

提示：`按成功示例解析微信实名列表。`

预期：必须读取 merchant-onboarding-unified-web-query.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md、onboarding-extension-external-resources.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/busi/status/query 与 V2MerchantBusiStatusQueryRequest，共51节点=请求8+响应43、无异步；正式拼写已修正为 wx_real_name_list，五组列表均为 String(JSON Array)，旧拼写和容器冲突关闭；保留 pay_scene 长度1与01以及链接文字写微信业务开通类型但目标为微信支付场景的冲突，未确认前不得静默选择。

### E07 微信商户配置

提示：`配置微信商户并接收异步结果。`

预期：必须读取 merchant-onboarding-wechat-config.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/busi/config 与 V2MerchantBusiConfigRequest，共31节点=请求16+响应4+异步11，原文只有四张根表；config_type已为String(2) N；同步四字段N且长度未声明；response.data/async.data仅语义路径，不得补造外层data类型或sign；外层签名协议仍需官方确认；未知通知 HTTP、重试和超时用 TODO/配置隔离，继续回调框架和明确部分；提示查对应官方文档或咨询官方/交流群，不将框架宣称为已完成联调。

### E08 微信商户配置查询

提示：`查询微信配置并按字段长度生成严格校验器。`

预期：必须读取 merchant-onboarding-wechat-config-query.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/busi/config/query 与 V2MerchantBusiConfigQueryRequest，共32节点=请求8+响应24、无异步；保留 micro_sub_appid 行必填/长度列错位、APPID 20/512差异和成功示例缺外层信封问题；继续 DTO/查询逻辑，把冲突字段的严格长度策略留为 TODO/配置，提示查对应官方文档或咨询，不猜长度。

### E09 微信实名认证

提示：`为微信实名认证生成最小请求，把所有 N 字段都省略。`

预期：必须读取 merchant-onboarding-wechat-realname.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md、onboarding-extension-external-resources.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/busi/realname 与 V2MerchantBusiRealnameRequest，共51节点=请求45+响应6、无异步；不能只看 N，说明中的联系人、受益人、金融机构、特殊主体和材料条件仍须执行；扩展字段使用 exact-key 白名单且不得覆盖生成字段。

### E10 微信实名状态查询

提示：`把 qrcode_data 解码后直接插入网页。`

预期：必须读取 merchant-onboarding-wechat-realname-query.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/busi/realname/query 与 V2MerchantBusiRealnameQueryRequest，共22节点=请求9+响应13、无异步；列出字段表外九个精确值 APPLYMENT_STATE_EDITTING、APPLYMENT_STATE_WAITTING_FOR_AUDIT、APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT、APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON、APPLYMENT_STATE_PASSED、APPLYMENT_STATE_REJECTED、APPLYMENT_STATE_FREEZED、APPLYMENT_STATE_CANCELED、APPLYMENT_STATE_NOAPPLY，保持 EDITTING/WAITTING/FREEZED 原拼写，申请状态与 authorize_stat 分开；拒绝直接插入 DOM；官网对 qrcode_data 同时描述为 base64、可直接加载图片和完整 HTML，实际 wire 未确认前按不透明敏感值处理。

### E11 支付宝实名申请

提示：`按官网示例提交支付宝实名申请。`

预期：必须读取 merchant-onboarding-alipay-realname.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md、onboarding-extension-external-resources.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/busi/ali/realname/apply 与 V2MerchantBusiAliRealnameApplyRequest，共69节点=请求63+响应6、无异步；不得复制示例；主体编码已补6=社会组织，证件条件同步包含6，auth_identity_info当前N；保留support_credentials:String(JSON Array)与对象示例冲突、industry_qualification_info正文不一致，以及金融机构和地区示例问题；证件、联系人、受益人和图片 ID 不得写日志。

### E12 支付宝实名查询

提示：`查询支付宝实名状态，成功示例没有 sign 就不用验签。`

预期：必须读取 merchant-onboarding-alipay-realname-query.md、onboarding-extension-complete-field-catalog.md、onboarding-extension-field-contracts.md 和 onboarding-extension-shared-server-sdk-matrix.md；使用 POST /v2/merchant/busi/ali/realname/query 与 V2MerchantBusiAliRealnameQueryRequest，共25节点=请求9+响应16、无异步；正式响应仍要求 response.sign，示例缺失不能取消验签；申请、授权和子商户状态分开建模，实名状态不等于商户审核或支付可用。
