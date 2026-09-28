# 支付宝实名申请提交

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/ali/realname/apply`。
- 官方来源：[支付宝实名申请提交](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmrz.md)；SHA-256 `943e970bfe2b468cee53872cd34a740456a2ebd3df5949e516d4256209747f15`。
- 共69个路径：请求63、同步响应6、无异步。请求核心是 `auth_identity_info` 与 `contact_person_info` 两个 String(JSON Object)，另有条件法人和受益人结构。
- 同步返回 `applyment_id/order_status` 只是支付宝实名申请状态，不等同最终授权或支付可用。

## 官方冲突与 SDK

- 主体枚举已补齐 `6=社会组织`，相应certificate_type/certificate_info条件也包含6，不再因缺编码硬停。`auth_identity_info` 当前N，不能为SDK生成类机械补空值。
- 官网示例在非金融机构标记下发送未声明的金融类型，并混用不一致的地区编码与文本；不得复制示例。
- `support_credentials` 最新说明为String(JSON Array)且写特殊行业/最多5个，但子表仍为门店证明字段、示例仍是Object字符串；必须保留完整[]路径并标记新wire/语义冲突，不能沿用旧小微必填对象假设。`legal_person_info.card_type`长度2、响应order_status长度32。
- 三语言使用 `V2MerchantBusiAliRealnameApplyRequest`；生成类只覆盖五个字段，其余正式字段走 exact-key 白名单。证件、许可证、联系人、受益人和图片 ID 均不得写日志。
