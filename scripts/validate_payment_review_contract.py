#!/usr/bin/env python3
"""Lock high-risk corrections found by the 2026-07-28 payment review."""

from __future__ import annotations

import re
from pathlib import Path

from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "huifu-pay-integration/references"


def read(name: str) -> str:
    return (REFS / name).read_text(encoding="utf-8")


def require(text: str, *needles: str) -> None:
    for needle in needles:
        assert needle in text, f"missing reviewed contract: {needle}"


def forbid(text: str, *needles: str) -> None:
    for needle in needles:
        assert needle not in text, f"stale/forbidden reviewed contract: {needle}"


def validate_current_atomic_fields() -> None:
    """Pin the revised field semantics in the human-facing atomic tables."""
    contracts = {
        "hostingpay-preorder-h5-pc-response.md": {"trans_finish_time": ("String", "13", "N")},
        "hostingpay-preorder-alipay-mini.md": {"trans_finish_time": ("String", "13", "N")},
        "hostingpay-preorder-wechat-mini.md": {"trans_finish_time": ("String", "13", "N"), "req_seq_id": ("String", "64", "Y")},
        "hostingpay-preorder-h5-pc-response-channel.md": {"cash_fee": ("String", "12", "N"), "coupon_fee": ("String", "12", "N"), "coupon_info": ("Object", "-", "N")},
        "hostingpay-query-payment-status-query.md": {"cash_fee": ("String", "12", "N"), "coupon_fee": ("String", "12", "N"), "coupon_info": ("String(JSON Array)", "-", "N")},
        "hostingpay-refund-query.md": {"coupon_info": ("String(JSON Array)", "-", "N"), "spnsrId": ("String", "20", "N"), "type": ("String", "4", "N"), "offstAmt": ("String", "14", "N"), "dy_response": ("String(JSON Object)", "6000", "N"), "trans_finish_time": ("String", "14", "N")},
    }
    for filename, fields in contracts.items():
        seen = set()
        for line in read(filename).splitlines():
            if not line.startswith("|"):
                continue
            cells = [cell.strip().strip('`') for cell in re.split(r'(?<!\\)\|', line.strip('|'))]
            if len(cells) != 6 or cells[0] not in fields:
                continue
            name = cells[0]
            assert tuple(cells[2:5]) == fields[name], (filename, name, cells[2:5])
            seen.add(name)
        assert seen == fields.keys(), (filename, fields.keys()-seen)
    print("current atomic payment tables validated: timestamp, decimal strings, array encoding and optionality")


def main() -> int:
    validate_current_atomic_fields()
    matrix = read("shared-server-sdk-matrix.md")
    require(
        matrix,
        "dg-java-sdk",
        "3.0.41",
        "2.0.31",
        "2.0.28",
        "官方 SDK-only 传输规则",
        "非阻断开发提醒",
        "三种语言的真实请求都使用官方 Request/facade/client",
        "不得手写 HTTP 补位",
        "V2TradeHostingPaymentPreorderDyRequest",
    )
    forbid(matrix, "## 传输安全硬停", "联调/生产可运行代码硬停")

    for filename in (
        "aggregation-java-sdk-quickstart.md",
        "hostingpay-java-sdk-quickstart.md",
    ):
        text = read(filename)
        debug = text.index("BasePay.debug = false;")
        first_init = min(
            position
            for token in ("BasePay.init", "Payment.create", "Payment.query")
            if (position := text.find(token)) >= 0
        )
        assert debug < first_init, f"{filename}: debug must be disabled before SDK use"

    order = read("aggregation-order-request.md")
    require(
        order,
        "| `method_expand` | 交易类型扩展参数 | String(JSON Object) | - | Y |",
        "约 3 分钟后置失败",
        "约 24 小时后置失败",
        "银联不支持",
        "超过一分钟",
    )

    wechat = read("aggregation-order-method-wechat.md")
    require(
        wechat,
        "payment-complete-field-catalog.md",
        "微信反扫 `T_MICROPAY` 请求字段",
        "### `T_MICROPAY` 的 `method_expand.scene_info.store_info`",
        "### `wx_response.promotion_detail[].goods_detail[]`",
    )
    forbid(
        wechat,
        "### `T_APP` 的 `method_expand.scene_info",
        "### `promotion_detail.goods_detail[]`",
    )

    for filename in (
        "hostingpay-preorder-h5-pc-request.md",
        "hostingpay-preorder-alipay-mini.md",
        "hostingpay-preorder-wechat-mini.md",
    ):
        text = read(filename)
        require(text, "channel_no", "String | 32", "pay_scene", "String | 2")

    for filename in (
        "aggregation-query-reconciliation.md",
        "hostingpay-query-reconciliation.md",
    ):
        text = read(filename)
        require(
            text,
            "MERGE_BILL",
            "短时预签名凭据",
            "禁用跨 host 重定向",
            "路径穿越",
        )

    refund = read("aggregation-refund.md")
    require(
        refund,
        "payment-complete-field-catalog.md",
        "不是完整 DTO",
        "`cash_refund_fee`",
        "`refund_coupon_info[]`",
        "`promotion_detail[]`",
        "`refund_amount`",
        "`goods_detail[]`",
        "`refund_amt`",
        "`refund_quantity`",
        "`sub_merchant_id`",
        "`coupon_refund_list[]`",
        "`refund_recv_wallet_id`",
    )

    splitpay = read("hostingpay-query-splitpay.md")
    require(
        splitpay,
        "payment-complete-field-catalog.md",
        "不能按叶字段名合并请求与响应中的 `org_req_seq_id`",
        "## `response.data.trans_list[]`",
        "### `response.data.trans_list[].wx_response.promotion_detail[]`",
        "### `response.data.trans_list[].wx_response.promotion_detail[].goods_detail`",
        "### `response.data.trans_list[].alipay_response.voucher_detail_list[]`",
    )

    refund_query = read("hostingpay-refund-query.md")
    require(
        refund_query,
        "同步响应 data 嵌套参数展开",
        "以下对象全部属于 `response.data`",
        "payment-complete-field-catalog.md",
        "### `response.data.acct_split_bunch`",
        "#### `response.data.acct_split_bunch.acct_infos[]`",
        "### `response.data.split_fee_info`",
        "#### `response.data.split_fee_info.split_fee_details[]`",
        "### `response.data.unionpay_response`",
        "#### `response.data.unionpay_response.coupon_info[]`",
        "旧冲突已关闭",
    )

    hosting_refund = read("hostingpay-refund.md")
    require(
        hosting_refund,
        "| `loan_flag` | String | 2 | N |",
        "| `bank_info_data` | String(JSON Object) | 1024 | C |",
        "| `refund_desc` | String | 200 | N |",
        "| `acct_split_bunch` | String(JSON Object) | 4000 | Y |",
        "| `org_hf_seq_id` | String | 128 | N |",
        "`unionpay_response.coupon_info[]`",
        "`split_fee_info.split_fee_details[]`",
        "| `org_hf_seq_id` | String | 128 | C | 与 `org_req_seq_id` 二选一，不能都为空 |",
        "| `org_req_seq_id` | String | 128 | C | 与 `org_hf_seq_id` 二选一，不能都为空 |",
        "risk_check_data.ip_addr",
        "旧风控示例冲突已关闭",
        "String(JSON Object)",
        "退款异步外层仍标为 `data`",
    )
    for snippet in (
        "| `org_ord_amt` | String | 14 | Y |",
        "| `org_fee_amt` | String | 14 | Y |",
        "| `trans_date` | String | 8 | Y |",
        "| `trans_type` | String | 40 | Y |",
        "| `total_ref_amt` | String | 14 | Y |",
        "| `total_ref_fee_amt` | String | 14 | Y |",
        "| `ref_cut` | String | 14 | Y |",
        "| `acct_split_bunch` | String(JSON Object) | 4000 | Y |",
    ):
        require(hosting_refund, snippet)

    skill = (ROOT / "huifu-pay-integration/SKILL.md").read_text(encoding="utf-8")
    require(
        skill,
        "Lightning Java `1.0.6`",
        "通用 Java `3.0.41`",
        "PHP `2.0.31`",
        "## 官方 SDK-only 传输规则",
        "非阻断开发提醒",
        "真实请求都必须使用对应官方 SDK",
        "不得为了“规避 TLS”",
        "完整 DTO、完整响应、嵌套字段或同名字段核对",
        "references/payment-complete-field-catalog.md",
        "合同定位路径",
        "实际 JSON/解码路径",
        "不把官网展示分组当成 wire key",
        "按当前请求实际加载并参与生成的 Skill 集合取值",
        "仅本 Skill 使用 `hfps/1.5.0`",
        "两个 Skill 都参与当前请求时使用 `hfps/1.5.0;hfms/1.1.0`",
        "顺序固定为支付、进件",
        "官方 `BsPayDemo/loader.php` 与 `Composer/BsPayConfig.php`",
        "加载任何 SDK 文件前固定 `DEBUG=false`",
    )

    header_policy = read("shared-request-header-policy.md")
    require(
        header_policy,
        "仅支付：hfps/1.5.0",
        "支付 + 进件：hfps/1.5.0;hfms/1.1.0",
        "双 Skill 顺序固定为支付、进件",
        "英文分号且不加空格",
        "原样透传该值，不再追加默认值",
    )

    catalog = read("payment-complete-field-catalog.md")
    require(
        catalog,
        "合同定位路径（仅定位，禁止作为 wire/DTO 层级）",
        "wire 字段路径",
        "String(JSON) 解码后路径",
        "只有官方说明明确写出“只为方便文档展示”或本地已记录接口所有者确认的节点才从 wire/解码路径移除",
        "聚合交易查询 `response.data.method_expand` 下的 `T_*` / `A_*` / `U_*` 行是场景分组",
        "聚合查询及退款查询响应中的 `tx_metadata`",
        "[需要官方确认]",
        "官网相对地址原文",
        "已确认的坏锚点会追加规范目标",
        "公共返回码全集",
        "聚合正扫异步返回参数",
        "聚合反扫异步返回参数",
        "异步消息简介",
        "[接入方确认勘误]",
        "应为 `A_MICROPAY: 支付宝付款码`",
        "官网临时签名 URL 示例已省略",
        "指定网银支付首次跳转银行页面需要打开浏览器弹窗限制",
        "参见图片说明",
        "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/",
    )
    forbid(
        catalog,
        "https://paas.huifu.com/partners/api/doc/cpjs/[官网示例图片已省略]",
    )

    query_contract = read("hostingpay-query-payment-status-query.md")
    require(
        query_contract,
        "quick_online_response` 必须标记为 `String（子表编码待确认）`",
        "不得生成固定 JSON decode 路径",
        "| quick_online_response | 快捷网银响应 | String（子表编码待确认） |",
    )
    aggregation_query = read("aggregation-query-payment-query.md")
    require(
        aggregation_query,
        "成功样例专属兼容键（参数表未定义）",
        "buyer_pay_amount",
        "buyer_user_id",
        "invoice_amount",
        "point_amount",
        "send_pay_date",
        "固定 DTO、校验器和业务判断不得依赖这些键",
        "只解码一次",
        "文档场景分组，不是线上返回的 key",
        "直接位于解码后对象的根层",
        "支付宝付款码交易的正式值是 `A_MICROPAY`",
        "当前官网成功示例已经使用该正确值",
        "把支付宝付款码重复写成 `A_NATIVE`",
        "线上字段名是 `response.data.trade_type`",
        "非法 JSON、解码后不是 Object",
        "保留原始值和规范化视图",
        "`buyer_logon_id` 属于账号信息",
    )
    forbid(
        aggregation_query,
        "表格双解码",
        "样例单解码",
        "只有当正式枚举对应的包装键存在时才尝试第二次严格解码",
        "官网也没有给出它与 `A_MICROPAY` 的映射证据",
    )
    common_params = read("aggregation-common-params.md")
    require(
        common_params,
        "本节只描述**聚合下单请求侧**",
        "不得外推到查询响应",
        "查询响应 `response.data.method_expand`",
        "只解码一次且字段单层平铺",
        "https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md",
        "https://paas.huifu.com/partners/api/doc/csfl/api_csfl_mcjs.md",
    )
    async_notify = read("shared-async-notify.md")
    require(
        async_notify,
        "https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md",
        "同时指向同一接口页的“聚合正扫异步返回参数”和“聚合反扫异步返回参数”两套通知参数",
        "验签后按通知 `resp_data.trans_type` 与已匹配原订单的 `trade_type` 核对",
        "请求/同步的 `trade_type` 不能作为通知中已声明字段读取",
        "缺失时可依据已匹配的落库原交易核对",
        "无法匹配或类型冲突时先查单核对",
        "HTTP `500-599` 默认重试 `3` 次",
        "不能把所有错误统一写成“最多 3 次”",
        "不得据此让商户接收端、SDK 或主动请求客户端关闭 TLS",
        "只表示协议字段可省略",
        "生产方案依赖异步通知",
        "上线必备配置",
        "不能使用官网示例 URL 或把示例当默认值",
    )
    error_codes = read("aggregation-error-codes.md")
    require(
        error_codes,
        "https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md",
        "https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md",
        "https://paas.huifu.com/partners/api/doc/csfl/api_csfl_mcjs.md",
        "不是全集",
        "合并查看",
        "`00000000` 不等于“交易最终成功”",
    )
    splitpay_php = read("hostingpay-query-php-scenarios.md")
    require(
        splitpay_php,
        "json_decode($transListRaw, true, 512, JSON_THROW_ON_ERROR)",
        "array_values($transList) !== $transList",
        "`trans_list` 在线上响应中是 `String(JSON Array)`",
    )

    require(
        matrix,
        "## 调试日志硬停",
        "BsPayDemo/loader.php",
        "Composer/BsPayConfig.php",
        "rsa_merch_private_key",
        "加载任何 SDK",
        "DEBUG=false",
    )
    for filename in ("aggregation-php-adapter.md", "hostingpay-php-adapter.md"):
        adapter = read(filename)
        require(
            adapter,
            "🔴 DEBUG 硬停",
            "defined('DEBUG') && DEBUG !== false",
            "define('DEBUG', false)",
            "拒绝启动：PHP SDK DEBUG 已启用",
        )
        assert adapter.index("define('DEBUG', false)") < adapter.index(
            "require_once HUIFU_SDK_ROOT . '/init.php'"
        ), f"{filename}: DEBUG must be fixed before loading the SDK"

    php_network_call = re.compile(
        r"\$(?:payment|client)->"
        r"(?:create|query|close|closeQuery|refund|refundQuery|postRequest)\s*\("
    )
    for filename in (
        "aggregation-php-adapter.md",
        "aggregation-query-php-scenarios.md",
        "hostingpay-php-adapter.md",
        "hostingpay-preorder-php-scenarios.md",
        "hostingpay-query-php-scenarios.md",
        "hostingpay-refund-php-scenarios.md",
    ):
        text = read(filename)
        require(text, "官方", "SDK", "不得")
        executable_lines = [
            line
            for line in text.splitlines()
            if php_network_call.search(line.split("//", 1)[0])
        ]
        assert executable_lines, (
            f"{filename}: missing official PHP SDK network call"
        )

    print("payment review contract validated: security, routing and high-risk fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
