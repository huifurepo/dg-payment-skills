# huifu-pay-integration-1.3.0-r4 sample pack

This directory is the checked-in location for deidentified production or joint-debug samples used to derive local-sandbox fixtures.

Rules:
- Only deidentified samples may be committed here.
- Every sample must pass `scripts/validate_local_sandbox_samples.py`.
- Raw samples in this directory must never be embedded into the sandbox binary or public source release archives.
- Derived fixtures may be generated into the r4 contract bundle with `scripts/import_local_sandbox_samples.py --write`.

Current state: deidentified production and joint-debug samples have been added:
- `samples/aggregation-alipay-micropay-success.json` covers an Alipay aggregation `A_MICROPAY` successful payment flow with `auth_code`, Alipay channel response fields, and successful query projection evidence.
- `samples/aggregation-alipay-native-success.json` covers an Alipay aggregation lightning `A_NATIVE` scan-payment flow with top-level split-account create fields, sync `qr_code`, Alipay success projection, split fee, async notify, and `pay.ali_qr` Webhook evidence.
- `samples/aggregation-alipay-jsapi-success.json` covers an Alipay aggregation `A_JSAPI` JS payment flow with top-level `acct_split_bunch`, `method_expand.buyer_id`, sync `pay_info.tradeNO`, Alipay success projection, split fee, async notify, and `pay.ali_js` Webhook evidence.
- `samples/aggregation-unionpay-native-success.json` covers a UnionPay aggregation `U_NATIVE` positive-scan flow with top-level create fields such as `remark`/`time_expire`, sync `qr_code` response, successful query projection, async notify, and Webhook evidence.
- `samples/aggregation-unionpay-micropay-success.json` covers a UnionPay aggregation `U_MICROPAY` successful payment flow with `auth_code`, UnionPay channel response fields, coupon projection, and successful query evidence.
- `samples/aggregation-wechat-native-success.json` covers a WeChat aggregation `T_JSAPI` public-account payment flow with top-level create fields, `method_expand.sub_appid/sub_openid`, sync `pay_info`, query-side `method_expand`/`payment_fee`/`acct_split_bunch` string projection, async notify, and Webhook evidence.
- `samples/aggregation-wechat-micropay-success.json` covers a WeChat aggregation `T_MICROPAY` payment-code flow with `method_expand.auth_code`, `delay_acct_flag`, `terminal_device_data`, sync `method_expand` channel fields, and successful `wx_response` projection evidence.
- `samples/aggregation-refund-channel-success.json` covers an aggregation Alipay lightning channel refund flow with `org_hf_seq_id` refund request locating the original payment, synchronous `00000100/P` processing response, refund-query not-found `23000001`, refund-query success, `acct_split_bunch`, merchant notify, and `refund.standard` Webhook evidence.
- `samples/aggregation-close-channel-success.json` covers an aggregation channel close flow for an unpaid order with close request, sync processing response, and successful close-query projection.
- `samples/hosting-close-channel-success.json` covers a Hosting close flow after preorder with close request, sync close response, and `queryorderinfo` close_stat projection.
- `samples/hosting-refund-channel-success.json` covers a Hosting channel refund success flow with original transaction projection, refund request, sync response, successful refund query projection, refund notify, merchant notify, and Webhook v2 submission evidence.
- `samples/hosting-splitpay-query-success.json` covers a Hosting splitpay query response from deidentified production evidence where the query succeeds and the order-level state is already refunded (`order_stat=3`); the canonical `hosting-splitpay-query-success` fixture separately covers the non-refunded successful payment state (`order_stat=1`).
- `samples/hosting-alipay-mini-success.json` covers a Hosting Alipay mini flow with `pre_order_type=2`, `app_data`, preorder response, query projection, merchant notify, and Webhook evidence.
- `samples/hosting-wechat-mini-success.json` covers a Hosting WeChat mini flow with `pre_order_type=3`, `miniapp_data`, preorder response, successful query projection, merchant notify, and Webhook evidence.
- `samples/hosting-h5pc-alipay-success.json` covers a Hosting Alipay flow with `alipay_data`, preorder/payment responses, Alipay channel response fields, merchant notify, and Webhook evidence.
- `samples/hosting-h5pc-douyin-success.json` covers a Hosting H5/PC Douyin direct preorder flow with `dy_data`, downstream TOP `dyData`, and Douyin `payInfo`/`jump_url` channel response fields.
- `samples/hosting-h5pc-terminal-success.json` covers a Hosting terminal-device flow with `terminal_device_data`, preorder/payment responses, successful response projection, merchant notify, and Webhook evidence.
- `samples/hosting-h5pc-unionpay-success.json` covers a Hosting H5/PC UnionPay flow with `unionpay_data`, preorder/payment responses, UnionPay channel response fields, successful query projection, merchant notify, and Webhook evidence.
- `samples/hosting-h5pc-wechat-success.json` covers a Hosting H5/PC WeChat `pre_order_type=1` flow with `wx_data`, preorder response, representative successful query projection, merchant notify, and Webhook evidence.

Remaining r4 production-equivalence gaps stay marked as `requires_production_sample` until more validated samples are imported.
