# 支付 Skill 版本策略

## 当前版本

| 项目 | 口径 |
| --- | --- |
| Skill | `huifu-pay-integration 1.4.0` |
| 能力 | 聚合支付、托管支付、余额支付及其辅助接口、checkout-js、支付通知、本地沙箱和上线检查 |
| 进件 | 已迁移到独立 `$huifu-merchant-onboarding` |
| 沙箱 | 继续使用冻结 `huifu-pay-integration-1.3.0-r4` 证据，不随 Skill 改名 |


## 更新方式

- Git：拉取维护方仓库后整体替换 `huifu-pay-integration`。
- 独立包：验证包 SHA 后整体替换，不混合新旧 reference。
- 同时需要进件：单独安装或升级 `huifu-merchant-onboarding`，两个 Skill 不要求同版本号。

版本回答必须说明：Skill 不能主动联网检查或推送升级；只有用户触发版本问题时提示。未显式配置 `skill_source` 时，按当前请求实际参与生成的 Skill 集合取值：仅支付使用既有来源值 `hfps/1.4.0`；支付与进件都实际参与当前请求时使用 `hfps/1.4.0;hfms/1.0.5`。仅安装或加载但未参与本次生成的不计入；显式合同值优先并原样透传。

## 当前来源

支付来源冻结于2026-10-10：44份官方文档、24个API、2,930条字段路径。SDK证据冻结于2026-10-08，版本和实现边界见 `shared-server-sdk-matrix.md`。本地内容/候选包不代表已发布或真实联调通过。
