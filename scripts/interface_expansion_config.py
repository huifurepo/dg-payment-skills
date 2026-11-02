"""Reviewed ownership and source positions for the 2026-10-25 API additions."""
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = "2026-10-25"
PAYMENT = "huifu-pay-integration"
ONBOARDING = "huifu-merchant-onboarding"
VERSIONS = {PAYMENT: ("1.4.0", "1.5.0"), ONBOARDING: ("1.0.5", "1.1.0")}
CATALOGS = {PAYMENT: "payment-extension-complete-field-catalog.md", ONBOARDING: "merchant-account-complete-field-catalog.md"}
LOCKS = {name: f"maintainer-contracts/{name}-additional-source-lock-{DATE}.json" for name in VERSIONS}
COMMON = (("请求信封", "request"), ("同步响应信封", "response"), ("请求 data", "request.data"), ("同步响应 data", "response.data"))
ACCOUNT = (("请求信封", "request"), ("请求 data", "request.data"), ("同步响应信封及 data", "response"))


@dataclass(frozen=True)
class Interface:
    key: str
    title: str
    skill: str
    url: str
    route: str
    surfaces: tuple
    request_class: str | None
    module: str | None

    @property
    def filename(self):
        return self.key + (".json" if self.url.endswith(".json") else ".md")

    @property
    def reference(self):
        return self.key + ".md"


INTERFACES = (
    Interface("delay-confirm", "交易确认", PAYMENT, "https://paas.huifu.com/partners/api/doc/smzf/api_jyqr.md", "/v2/trade/payment/delaytrans/confirm", COMMON + (("异步信封", "async"), ("异步 resp_data", "async.resp_data")), "V2TradePaymentDelaytransConfirmRequest", "v2_trade_payment_delaytrans_confirm"),
    Interface("delay-confirm-query", "交易确认查询", PAYMENT, "https://paas.huifu.com/partners/api/doc/smzf/api_jyqrcx.md", "/v3/trade/payment/delaytrans/confirmquery", COMMON, "V3TradePaymentDelaytransConfirmqueryRequest", "v3_trade_payment_delaytrans_confirmquery"),
    Interface("delay-confirm-refund", "交易确认退款", PAYMENT, "https://paas.huifu.com/partners/api/doc/smzf/api_jyqrtk.md", "/v2/trade/payment/delaytrans/confirmrefund", COMMON, "V2TradePaymentDelaytransConfirmrefundRequest", "v2_trade_payment_delaytrans_confirmrefund"),
    Interface("delay-confirm-refund-query", "交易确认退款查询", PAYMENT, "https://paas.huifu.com/navigator/ossApi/api_jyqrtkcq.json", "/v2/trade/payment/delaytrans/confirmrefundquery", (("正式请求 data", "request.data"),), "V2TradePaymentDelaytransConfirmrefundqueryRequest", "v2_trade_payment_delaytrans_confirmrefundquery"),
    Interface("account-subaccount-open", "子账户开通配置", ONBOARDING, "https://paas.huifu.com/partners/api/doc/zhgl/api_zhgl_zhpz_kyc.md", "/v2/merchant/settle/config", ACCOUNT + (("审核异步信封及 data", "async"),), "V2MerchantSettleConfigRequest", "v2_merchant_settle_config"),
    Interface("account-subaccount-modify", "修改子账户配置", ONBOARDING, "https://paas.huifu.com/partners/api/doc/zhgl/api_zhgl_xgzh_kyc.md", "/v2/merchant/settle/modify", ACCOUNT + (("审核异步信封及 data", "async"),), "V2MerchantSettleModifyRequest", "v2_merchant_settle_modify"),
    Interface("account-balance-query", "账户余额信息查询", PAYMENT, "https://paas.huifu.com/partners/api/doc/jyjs/api_jyjs_yuexxcx.md", "/v2/trade/acctpayment/balance/query", ACCOUNT, "V2TradeAcctpaymentBalanceQueryRequest", "v2_trade_acctpayment_balance_query"),
    Interface("account-ledger-query", "账务流水查询", PAYMENT, "https://paas.huifu.com/partners/api/doc/yuer/api_acctlscx.md", "/v2/trade/acctpayment/acctlog/query", ACCOUNT, "V2TradeAcctpaymentAcctlogQueryRequest", "v2_trade_acctpayment_acctlog_query"),
    Interface("account-ledger-summary-query", "账务流水汇总结果查询", PAYMENT, "https://paas.huifu.com/partners/api/doc/zhy/api_acct_log_summary.md", "/v2/trade/acctpayment/acctlog/summary", ACCOUNT, None, None),
)
