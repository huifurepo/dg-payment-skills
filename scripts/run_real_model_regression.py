#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = REPO_ROOT / "scripts" / "huifu-payment-test-prompts.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / ".tmp" / "real-model-regression"
DEFAULT_TIMEOUT_SECONDS = 300
SMOKE_CASE_IDS = (1, 8, 15, 24, 26, 34, 35, 36, 37, 38, 47, 54)
ASCII_WORKSPACE_MARKER = ".real-model-regression-workspace"


@dataclass(frozen=True)
class CaseRule:
    required_groups: tuple[tuple[str, ...], ...]
    forbidden: tuple[str, ...] = ()


@dataclass(frozen=True)
class PromptCase:
    case_id: int
    prompt: str
    expected: str


@dataclass
class CaseResult:
    case_id: int
    passed: bool
    missing: list[str]
    forbidden_hits: list[str]
    policy_errors: list[str]
    output_path: Path
    returncode: int


REFERENCE_EVIDENCE_TERMS = ("本轮实际使用", "实际使用", "实际读取", "本地依据", "已读 references", "已读取 references")
REFERENCE_FILE_NAMES = frozenset(
    path.name for path in (REPO_ROOT / "huifu-pay-integration" / "references").glob("*.md")
)
REFERENCE_FILE_NAME_LOOKUP = {name.lower(): name for name in REFERENCE_FILE_NAMES}
REFERENCE_MENTION_PATTERN = re.compile(r"(?:(?:huifu-pay-integration/)?references/)?([A-Za-z0-9_.-]+\.md)")
MAX_LISTED_REFERENCES = 5
PHP_TEMPLATE_FORBIDDEN = (
    r"\bnew\s+\\?hostingclient\b",
    r"\bclass\s+\\?hostingclient\b",
    r"\bnew\s+\\?aggregationclient\b",
    r"\bclass\s+\\?aggregationclient\b",
    r"\bcurl\s*_\s*init\s*\(",
    r"\bcurl\s*_\s*setopt\s*\(",
)
CHECKOUT_INSTALL_FORBIDDEN = (
    r"\bnpm\s+install\b",
    r"\bpnpm\s+add\b",
    r"\byarn\s+add\b",
    r"<\s*script\b[^>]*\bsrc\s*=",
)
CHECKOUT_CALLBACK_FORBIDDEN = (
    r"callback\s*成功\s*(就是|即|等于)\s*最终成功",
    r"前端回调\s*成功\s*(就是|即|等于)\s*最终成功",
    r"(?<!不)可以\s*直接\s*改订单(为)?支付成功",
    r"(?<!不)可\s*直接\s*改订单(为)?支付成功",
    r"即可\s*改订单成功",
)
BYPASS_SIGNING_FORBIDDEN = (
    r"\breturn\s+true\s*;",
    r"\bskip\s*verify\b",
    r"\bskip[_\s-]*verify\b",
    r"\bverify\s*=\s*false\b",
    r"关闭\s*验签",
    r"验签\s*关闭",
)
OFFICIAL_REMOTE_URL_FORBIDDEN = (
    r"https?://paas\.huifu\.com/",
)
VERSION_CHECK_FORBIDDEN = (
    r"我已.*(联网|实时).*确认",
    r"已经.*(联网|实时).*检查.*最新版",
    r"https?://",
)

RULES: dict[int, CaseRule] = {
    1: CaseRule((("shared-overview",), ("copilot-onboarding",), ("copilot-solution-selection",), ("Java",), ("聚合支付", "托管支付", "H5"))),
    2: CaseRule((("aggregation-refund",), ("aggregation-php-adapter",), ("aggregation-query-php-scenarios",), ("Payment::refund", "refundQuery"), ("skill_source", "MerConfig.skill_source")), PHP_TEMPLATE_FORBIDDEN),
    3: CaseRule((("checkout-js",), ("checkout-js-callback-and-confirmation",), ("hostingpay-query",), ("hostingpay-async-webhook",), ("前端回调不等于", "前端回调不能", "不是最终成功", "callback 只传", "不改终态", "不能直接改已支付", "不要直接改订单为已支付", "不要信前端 callback")), CHECKOUT_CALLBACK_FORBIDDEN),
    4: CaseRule((("checkout-js",), ("checkout-js-integration-flow", "checkout-js-create-preorder-contract"), ("checkout-js-callback-and-confirmation",), ("hostingpay-async-webhook",), ("跳过", "不再读", "暂时不要读")), CHECKOUT_CALLBACK_FORBIDDEN),
    5: CaseRule((("jpt-x-skill-source",), ("jpt-x-skill-huifu_id",), ("HTTP 请求头", "HTTP 头", "请求头"), ("MerConfig.skill_source",), ("自动",))),
    6: CaseRule((("Java",), ("MerConfig.setSkillSource",), ("jpt-x-skill-source",), ("jpt-x-skill-huifu_id",), ("huifu_id",))),
    7: CaseRule((("huifurepo/dg-php-sdk", "dg-php-sdk"), ("BsPayClient::postRequest",), ("request 类", "request类", "V2TradeHostingPaymentPreorderH5Request"), ("skill_source",)), PHP_TEMPLATE_FORBIDDEN),
    8: CaseRule((("硬检查点",), ("checkout-js",), ("不能单独", "不能直接", "不能只靠前端"), ("托管预下单",), ("查单", "异步通知")), CHECKOUT_INSTALL_FORBIDDEN),
    9: CaseRule((("aggregation-order",), ("aggregation-php-adapter",), ("aggregation-query-php-scenarios",), ("Payment::create", "$payment->create", "->create("), ("TradePaymentCreateRequest",)), PHP_TEMPLATE_FORBIDDEN),
    10: CaseRule((("aggregation-query",), ("aggregation-php-adapter",), ("aggregation-query-php-scenarios",), ("Payment::query", "$payment->query", "->query("), ("close()", "closeQuery", "$payment->close", "->close("), ("落库", "持久化")), PHP_TEMPLATE_FORBIDDEN),
    11: CaseRule((("BsPayClient::postRequest", "$client->postRequest"), ("V2TradeCheckFilequeryRequest",), ("aggregation-query",), ("aggregation-php-adapter",), ("aggregation-query-php-scenarios",)), PHP_TEMPLATE_FORBIDDEN),
    12: CaseRule((("dg-java-sdk",), ("V2TradeCheckFilequeryRequest",), ("aggregation-query",), ("aggregation-query-reconciliation",), ("手写 HTTP", "不要给")), ("HttpClientUtils.sendPost(",)),
    13: CaseRule((("hostingpay-refund",), ("hostingpay-refund-query",), ("req_date",), ("req_seq_id",), ("huifu_id",), ("ord_amt",), ("org_req_date",), ("loan_flag", "垫资"), ("risk_check_data",), ("bank_info_data", "银行大额"))),
    14: CaseRule((("aggregation-refund",), ("aggregation-refund-query",), ("不传 `tx_metadata`", "不传 tx_metadata", "不要传 `tx_metadata`", "不要包 `tx_metadata`", "不要包 tx_metadata"), ("acct_split_bunch",), ("combinedpay_data",), ("device_type=4", "device_type`=4", "device_type` 为 `4"), ("org_hf_seq_id",), ("org_req_seq_id",), ("mer_ord_id",))),
    15: CaseRule((("huifurepo/dg-php-sdk",), ("2.0.27",), ("composer require",), ("composer update", "--with-all-dependencies"), ("api.github.com/repos/huifurepo/bspay-php-sdk/zipball", "备用下载", "GitHub"), ("BsPaySdk/init.php", "init.php"), ("BsPay::init",), ("skill_source",), ("HUIFU_SDK_ROOT",), ("HUIFU_SYS_ID",), ("HUIFU_RSA_PRIVATE_KEY",), ("require_once",), ("request 类", "request类", "TradePaymentCreateRequest")), PHP_TEMPLATE_FORBIDDEN),
    16: CaseRule((REFERENCE_EVIDENCE_TERMS, ("接入判断卡",), ("首次接入",), ("聚合支付",), ("Java",), ("用户类型",), ("产品线",), ("阶段",), ("技术栈",), ("端形态",), ("当前目标", "目标：", "目标:"), ("还缺", "缺少", "待补", "补齐"))),
    17: CaseRule((REFERENCE_EVIDENCE_TERMS, ("copilot-existing-system",), ("存量系统", "增量接入"), ("建议新增",), ("建议保留",), ("人工确认",), ("落库字段", "落库"), ("风险点", "风险"), ("回归检查", "回归"), ("不重写", "不直接替换"), ("callback", "前端回调", "同步受理"))),
    18: CaseRule((REFERENCE_EVIDENCE_TERMS, ("托管支付",), ("H5/PC", "H5 / PC"), ("project_id",), ("托管项目状态", "项目状态"), ("notify_url",), ("callback_url",), ("查单", "异步通知"), ("方案卡",), ("存量系统", "存量"))),
    19: CaseRule((REFERENCE_EVIDENCE_TERMS, ("resp_code=00000000", "00000000"), ("受理", "处理成功"), ("不等于", "不是"), ("交易终态", "最终状态"), ("trans_stat",), ("查单", "异步通知"))),
    20: CaseRule((REFERENCE_EVIDENCE_TERMS, ("问题排查卡",), ("notify_type",), ("交易异步",), ("账务异步",), ("hf_seq_id",), ("幂等",), ("不能直接判断", "不要直接判断", "不等于重复扣款", "不一定重复扣款"))),
    21: CaseRule((REFERENCE_EVIDENCE_TERMS, ("参数检查卡",), ("阻断", "不能继续", "先修复"), ("time_expire",), ("未来时间",), ("req_seq_id",), ("重复",), ("修复", "重新生成"))),
    22: CaseRule((REFERENCE_EVIDENCE_TERMS, ("退款查询",), ("退款交易自身", "退款请求流水", "退款流水"), ("原支付",), ("不能混用", "不要混用"), ("平台流水",), ("落库",))),
    23: CaseRule((REFERENCE_EVIDENCE_TERMS, ("存量",), ("异步通知",), ("验签",), ("解析",), ("幂等",), ("状态保护",), ("只执行一次", "只能执行一次"), ("验证方式", "回归检查", "验证"))),
    24: CaseRule((REFERENCE_EVIDENCE_TERMS, ("拒绝", "不能", "不提供"), ("绕过验签", "跳过验签"), ("代码",), ("验签",), ("幂等", "idempotent", "isProcessed"), ("查单", "异步通知", "queryService.query", "query("), ("最终确认", "最终状态", "查单确认", "异步通知确认", "补偿确认", "查单/补偿确认", "QueryResult", "queryService.query")), BYPASS_SIGNING_FORBIDDEN),
    25: CaseRule((REFERENCE_EVIDENCE_TERMS, ("不定责", "不能定责"), ("升级人工",), ("环境",), ("SDK 版本", "SDK版本"), ("脱敏",), ("请求",), ("响应",), ("流水",), ("时间",), ("日志",), ("影响范围", "业务影响"), ("已做动作", "已执行动作"))),
    26: CaseRule((REFERENCE_EVIDENCE_TERMS, ("上线检查卡",), ("通用上线", "通用检查", "上线检查卡"), ("存量系统", "存量"), ("必测项", "必测"), ("灰度",), ("回滚",), ("日志脱敏", "脱敏"), ("callback", "前端回调"), ("退款",), ("查单",), ("异步通知",), ("project_id",), ("notify_url",), ("托管项目状态", "项目状态"), ("不定责", "不能定责"), ("密钥",))),
    27: CaseRule((REFERENCE_EVIDENCE_TERMS, ("official-service-source-index",), ("花呗分期", "分期支付"), ("不覆盖", "转人工", "需转"), ("不生成完整", "不输出完整", "不提供完整", "不能直接给"), ("可联调代码", "完整模板", "可联调模板"), ("买家侧能力", "商户开通状态", "开通"), ("测试环境", "报错", "流水", "联调参数")), OFFICIAL_REMOTE_URL_FORBIDDEN),
    28: CaseRule((REFERENCE_EVIDENCE_TERMS, ("official-service-source-index",), ("大额支付", "银行大额", "大额"), ("部分覆盖", "资料准备", "字段位置", "整理材料"), ("限额",), ("准入",), ("资质",), ("定责", "不定责", "失败责任", "不自动归因"), ("不能自动判断", "不自动判断", "不能给结论", "不能承诺", "不能直接给"), ("升级人工", "人工材料", "商务", "运营", "合规", "汇付支持")), OFFICIAL_REMOTE_URL_FORBIDDEN),
    29: CaseRule((REFERENCE_EVIDENCE_TERMS, ("official-service-source-index",), ("URL 未注册", "redirect_uri"), ("配置", "渠道权限"), ("域名",), ("appid", "app id"), ("notify_url", "callback_url", "回跳地址"), ("控台",), ("运营", "商务", "人工")), OFFICIAL_REMOTE_URL_FORBIDDEN),
    30: CaseRule((REFERENCE_EVIDENCE_TERMS, ("official-service-source-index",), ("实时", "最新口径", "最新政策"), ("不内置实时官网抓取", "不支持实时官网抓取", "不能实时抓取", "没有实时官网抓取"), ("费率",), ("合规", "政策审批"), ("通道准入",), ("人工", "联网核验")), OFFICIAL_REMOTE_URL_FORBIDDEN),
    31: CaseRule((REFERENCE_EVIDENCE_TERMS, ("接入判断卡",), ("聚合支付",), ("Java",), ("shared-overview",), ("copilot-onboarding",), ("aggregation-quickstart", "aggregation-customer-preparation", "aggregation-base", "aggregation-order"), ("用户类型", "产品线", "阶段")), (r"official-service-source-index",) + OFFICIAL_REMOTE_URL_FORBIDDEN),
    32: CaseRule((REFERENCE_EVIDENCE_TERMS, ("skill-version-policy",), ("1.3.0",), ("不能主动联网检查", "不主动联网检查", "不能主动推送", "不会主动推送", "不内置后台联网版本检查", "不能主动提醒", "不能主动后台提醒升级"), ("用户触发", "询问版本", "问到版本", "升级问题", "明确问版本", "问版本/升级", "请求了当前", "由你触发查询"), ("Git", "git pull", "拉取"), ("整体覆盖", "发布包", "替换 Skill 目录"), ("重新加载", "重启"), ("SKILL.md",), ("维护者", "维护方")), VERSION_CHECK_FORBIDDEN),
    33: CaseRule((REFERENCE_EVIDENCE_TERMS, ("checkout-js",), ("checkout-js-callback-and-confirmation", "callback/confirmation", "callback"), ("hostingpay-async-webhook", "异步通知", "最终确认"), ("已完成", "已经跑通", "已跑通", "前置"), ("跳过", "不重新列", "不再列", "不需要重跑", "已跳过"), ("quickstart", "base", "preorder", "query")), (r"(?<!不)触发\s*硬检查点", r"references/hostingpay-quickstart\.md", r"references/hostingpay-base\.md", r"references/hostingpay-preorder\.md", r"references/hostingpay-query\.md")),
    34: CaseRule((REFERENCE_EVIDENCE_TERMS, ("shared-request-field-preservation",), ("req_seq_id", "setReqSeqId", "ReqSeqId"), ("req_date", "setReqDate", "ReqDate"), ("保留入参", "原样映射"), ("缺失或非法时显式报错", "缺失或非法要显式报错", "缺失或非法就显式报错"), ("不要", "不能"), ("覆盖", "重写", "重新生成"))),
    35: CaseRule((REFERENCE_EVIDENCE_TERMS, ("hostingpay-preorder-douyin-direct",), ("hostingpay-preorder",), ("pre_order_type=4", "pre_order_type`=4", "pre_order_type` 为 `4", "pre_order_type 是 4", "pre_order_type` 固定 `4", "pre_order_type` 固定传 `4", "pre_order_type` 固定传 4"), ("dy_data",), ("sub_appid",), ("busi_scene",), ("payer_client_ip",), ("jump_url",), ("不等于", "不能当", "不是", "只表示", "只用于", "不要看"), ("异步通知", "查单", "最终状态", "最终确认"))),
    36: CaseRule((REFERENCE_EVIDENCE_TERMS, ("hostingpay-query-splitpay",), ("hostingpay-query",), ("hostingpay-preorder-wechat-mini",), ("splitpay/query",), ("org_req_date",), ("org_req_seq_id",), ("trans_list",), ("trans_stat",), ("普通", "queryorderinfo"), ("不能", "不要", "不等同"))),
    37: CaseRule((REFERENCE_EVIDENCE_TERMS, ("aggregation-query-trade-close",), ("aggregation-query-close-query",), ("merge_flag",), ("Y", "合单"), ("主单",), ("N", "空", "非合单"), ("子单",), ("org_req_date",), ("org_hf_seq_id",), ("org_req_seq_id",), ("二选一", "或 `org_hf_seq_id`", "或 org_hf_seq_id"), ("trans_stat",))),
    38: CaseRule((REFERENCE_EVIDENCE_TERMS, ("aggregation-query-reconciliation",), ("aggregation-query",), ("file_date",), ("bill_type",), ("MERGE_BILL",), ("file_name",), ("file_Name",), ("兼容",), ("task_stat",), ("I/P/DP/FP/F/S", "I", "DP", "FP", "S"))),
    39: CaseRule((REFERENCE_EVIDENCE_TERMS, ("hostingpay-preorder-douyin-direct",), ("pre_order_type=4", "pre_order_type`=4", "pre_order_type` 为 `4"), ("托管预下单", "预下单 request", "共用端点"), ("H5/PC", "pre_order_type=1"), ("dy_data",), ("不要", "不能", "不可"), ("抖音直连",))),
    40: CaseRule((REFERENCE_EVIDENCE_TERMS, ("hostingpay-preorder-douyin-direct",), ("jump_url",), ("不等于", "不能当", "不是"), ("最终状态", "最终确认", "交易终态"), ("异步通知",), ("查单", "补偿查询"))),
    41: CaseRule((REFERENCE_EVIDENCE_TERMS, ("hostingpay-query-splitpay",), ("splitpay/query",), ("queryorderinfo", "普通托管查单"), ("不能", "不要", "不应"), ("org_req_date",), ("org_req_seq_id",), ("trans_list",))),
    42: CaseRule((REFERENCE_EVIDENCE_TERMS, ("hostingpay-query-splitpay",), ("order_stat",), ("trans_list",), ("trans_stat",), ("子交易", "拆单明细"), ("不能只看", "不要只看", "不够"))),
    43: CaseRule((REFERENCE_EVIDENCE_TERMS, ("shared-request-field-preservation",), ("Java",), ("req_seq_id",), ("req_date",), ("notify_url",), ("project_id",), ("原样映射", "保留入参"), ("不要", "不能"), ("重新生成", "覆盖"))),
    44: CaseRule((REFERENCE_EVIDENCE_TERMS, ("shared-request-field-preservation",), ("PHP",), ("req_seq_id",), ("req_date",), ("ord_amt", "金额"), ("org_req_date",), ("org_req_seq_id",), ("原样映射", "保留入参"), ("不要", "不能"), ("重新生成", "覆盖"))),
    45: CaseRule((REFERENCE_EVIDENCE_TERMS, ("hostingpay-python-adapter",), ("Python",), ("dy_data",), ("json.dumps", "JSON 字符串", "JSON字符串"), ("dict",), ("不要直接传", "不能直接传", "不要传 Python dict"))),
    46: CaseRule((REFERENCE_EVIDENCE_TERMS, ("shared-server-sdk-matrix",), ("hostingpay-preorder-douyin-direct",), ("hostingpay-query-splitpay",), ("托管预下单", "共用 `preorder`", "共用 preorder", "pre_order_type=4"), ("V2TradeHostingPaymentPreorderH5Request",), ("独立 Request 类", "独立 request 类", "独立抖音", "独立抖音 SDK 类"), ("抖音直连",), ("没有独立", "无独立", "不是独立", "不要生成"), ("Java",), ("PHP",), ("Python",), ("V2TradeHostingPaymentSplitpayQueryRequest",), ("均有", "都有", "三语言"), ("不能编造", "不要编造", "不存在的类", "Dypreorder", "Douyin", "不是独立抖音 SDK 类", "不是独立抖音 Request 类"))),
    47: CaseRule((REFERENCE_EVIDENCE_TERMS, ("merchant-onboarding-faq",), ("copilot-troubleshooting-playbooks",), ("接口权限认证失败", "20003"), ("sys_id",), ("数据权限认证失败",), ("product_id",), ("huifu_id",), ("upper_huifu_id",), ("该路由下未配置可用通道", "路由"), ("channel_no", "pay_channel", "pay_scene")), (r"直接换.*huifu_id", r"随便换.*huifu_id", r"随便改.*product_id") + OFFICIAL_REMOTE_URL_FORBIDDEN),
    48: CaseRule((REFERENCE_EVIDENCE_TERMS, ("merchant-onboarding-faq",), ("aggregation-customer-preparation", "hostingpay-customer-preparation", "aggregation-order-method-wechat", "aggregation-order"), ("sub_mch_id",), ("sub_appid",), ("sub_openid",), ("绑定",), ("同一个", "对应", "不能混用", "不可混用"), ("URL 未注册", "url 未注册", "redirect_uri"), ("授权目录", "授权域名"), ("延迟", "/", "生效")), (r"可以伪造.{0,16}openid", r"直接伪造.{0,16}openid", r"绕过.{0,16}渠道配置") + OFFICIAL_REMOTE_URL_FORBIDDEN),
    49: CaseRule((REFERENCE_EVIDENCE_TERMS, ("shared-webhook-signing",), ("merchant-onboarding-faq",), ("copilot-troubleshooting-playbooks",), ("sign",), ("URL", "query", "查询参数"), ("原始请求体", "raw_body", "原始 body"), ("endpoint key", "endpoint_key", "终端密钥"), ("统一接收", "下属机构"), ("notify_url", "Webhook"), ("不混用", "不能混用", "区分", "不是一套", "两类入口")), BYPASS_SIGNING_FORBIDDEN + OFFICIAL_REMOTE_URL_FORBIDDEN),
    50: CaseRule((REFERENCE_EVIDENCE_TERMS, ("merchant-onboarding-faq",), ("copilot-troubleshooting-playbooks",), ("退款一直处理中", "处理中"), ("退款查询", "轮询"), ("不换流水", "不要换流水", "不能换流水"), ("请求频率过高", "频率"), ("降频", "等待终态"), ("延时分账", "确认退款", "已确认部分", "未确认部分"))),
    51: CaseRule((REFERENCE_EVIDENCE_TERMS, ("merchant-onboarding-faq",), ("official-service-source-index",), ("对账文件", "对账"), ("配置", "开通"), ("跑批", "任务状态", "task_stat"), ("DM", "取现"), ("发票",), ("转人工", "运营", "税务"), ("不写支付代码", "不是代码", "不由代码", "不能写代码解决", "不是支付接口字段")), OFFICIAL_REMOTE_URL_FORBIDDEN),
    52: CaseRule((REFERENCE_EVIDENCE_TERMS, ("merchant-onboarding-faq",), ("copilot-troubleshooting-playbooks",), ("huifu_id",), ("账户已创建", "账号已创建", "账户创建"), ("业务开通",), ("token_no", "银行卡", "结算", "取现"), ("实名", "补齐资料"), ("不等于", "不能等同", "不代表", "不能当成"), ("交易可用", "可交易"))),
    53: CaseRule((REFERENCE_EVIDENCE_TERMS, ("hostingpay-faq",), ("hostingpay-refund",), ("setProductId",), ("3.0.38", "最新"), ("setProcutId",), ("不要再生成", "不要再用", "旧文档", "旧"), ("extendInfoMap",), ("org_req_seq_id",), ("setExtendInfo",), ("不是 SDK bug", "不应说这是 SDK bug", "不是 bug", "不按 SDK bug", "不直接按 SDK bug"))),
    54: CaseRule((REFERENCE_EVIDENCE_TERMS, ("copilot-existing-system",), ("存量业务系统首次接汇付", "存量系统增量接入", "存量系统"), ("第一次接汇付",), ("不能", "不应", "不要"), ("非存量", "不是存量"), ("建议新增",), ("建议保留",), ("人工确认",), ("落库字段", "落库"), ("风险点", "风险"), ("回归检查", "回归"), ("不重写", "不直接替换"))),
    55: CaseRule((REFERENCE_EVIDENCE_TERMS, ("copilot-troubleshooting-playbooks",), ("official-service-source-index",), ("AI 技能包技术支持", "技术支持"), ("https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support",), ("脱敏",), ("问题描述",), ("环境",), ("接口路径",), ("SDK 版本", "SDK版本"), ("请求",), ("响应",), ("流水",), ("时间",), ("日志",), ("影响范围",), ("已执行动作", "已做动作"), ("真实密钥", "敏感数据", "生产敏感"))),
}


def main() -> int:
    args = parse_args()
    if args.skip_run and args.output_dir is None:
        print("--skip-run requires --output-dir with existing case outputs.", file=sys.stderr)
        return 2
    cases = select_cases(load_cases(), args.case, args.smoke)
    if not cases:
        print("No regression cases selected; check --case values.", file=sys.stderr)
        return 2
    output_dir = make_output_dir(args.output_dir)
    workspace = REPO_ROOT if args.skip_run else prepare_regression_workspace(output_dir, args.workspace)
    results = [run_case(case, output_dir, workspace, args) for case in cases]
    write_summary(output_dir, results)
    print_summary(output_dir, results)
    return 0 if all(result.passed for result in results) else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run real-model regression for huifu skill prompts.")
    parser.add_argument("--case", type=int, action="append", help="Run only selected case id. Can repeat.")
    parser.add_argument("--smoke", action="store_true", help=f"Run smoke cases only: {', '.join(map(str, SMOKE_CASE_IDS))}.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for raw outputs and summary.")
    parser.add_argument("--workspace", type=Path, default=None, help="Optional temporary workspace path for codex exec.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--model", default=None, help="Optional model override for codex exec.")
    parser.add_argument("--codex-executable", default=None, help="Optional codex executable path. Can also use CODEX_EXECUTABLE.")
    parser.add_argument("--skip-run", action="store_true", help="Evaluate existing outputs in output dir.")
    return parser.parse_args()


def load_cases() -> list[PromptCase]:
    data = json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))
    return [PromptCase(int(item["id"]), item["prompt"], item["expected"]) for item in data]


def select_cases(cases: list[PromptCase], selected: list[int] | None, smoke: bool) -> list[PromptCase]:
    if smoke:
        selected = [*(selected or []), *SMOKE_CASE_IDS]
    if not selected:
        return cases
    selected_set = set(selected)
    return [case for case in cases if case.case_id in selected_set]


def make_output_dir(output_dir: Path | None) -> Path:
    if output_dir is not None:
        target = output_dir if output_dir.is_absolute() else REPO_ROOT / output_dir
        target.mkdir(parents=True, exist_ok=True)
        return target
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = DEFAULT_OUTPUT_ROOT / stamp
    target.mkdir(parents=True, exist_ok=True)
    return target


def prepare_regression_workspace(output_dir: Path, workspace: Path | None) -> Path:
    if workspace is None:
        base_dir = output_dir / "workspaces"
        base_dir.mkdir(parents=True, exist_ok=True)
        workspace = Path(tempfile.mkdtemp(prefix="hf-payment-skills-", dir=base_dir))
        workspace.rmdir()
    else:
        workspace = workspace if workspace.is_absolute() else REPO_ROOT / workspace
    if workspace.is_symlink():
        target = workspace.resolve(strict=False)
        if target != REPO_ROOT:
            raise RuntimeError(f"regression workspace symlink points to {target}")
        workspace.unlink()
    if workspace.exists():
        marker = workspace / ASCII_WORKSPACE_MARKER
        if not marker.exists():
            raise RuntimeError(f"regression workspace exists without marker: {workspace}")
        shutil.rmtree(workspace)
    shutil.copytree(REPO_ROOT, workspace, ignore=ignore_workspace_entry)
    (workspace / ASCII_WORKSPACE_MARKER).write_text(str(REPO_ROOT) + "\n", encoding="utf-8")
    return workspace


def ignore_workspace_entry(path: str, names: list[str]) -> set[str]:
    ignored = {".git", ".tmp", "__pycache__"}
    return {name for name in names if name in ignored or name.endswith(".7z")}


def run_case(case: PromptCase, output_dir: Path, workspace: Path, args: argparse.Namespace) -> CaseResult:
    output_path = output_dir / f"case-{case.case_id:02d}.txt"
    returncode = 0
    if args.skip_run:
        text = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        return evaluate_case(case, text, output_path, 0)
    model_output_path = workspace / output_path.relative_to(REPO_ROOT)
    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    command = build_command(case, model_output_path, workspace, args.model, args.codex_executable)
    try:
        result = subprocess.run(
            command,
            cwd=workspace,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=args.timeout,
            check=False,
        )
        returncode = result.returncode
        if model_output_path.exists():
            output_path.write_text(model_output_path.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            output_path.write_text(format_process_output(result), encoding="utf-8")
    except subprocess.TimeoutExpired as exc:
        returncode = 124
        output_path.write_text(format_timeout_output(exc, args.timeout), encoding="utf-8")
    except OSError as exc:
        returncode = 127 if isinstance(exc, FileNotFoundError) else 126
        output_path.write_text(format_execution_error(exc, command), encoding="utf-8")
    text = output_path.read_text(encoding="utf-8")
    return evaluate_case(case, text, output_path, returncode)


def build_command(
    case: PromptCase,
    output_path: Path,
    workspace: Path,
    model: str | None,
    codex_executable: str | None,
) -> list[str]:
    command = [
        resolve_codex_executable(codex_executable),
        "exec",
        "--cd",
        str(workspace),
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "--full-auto",
        "--ephemeral",
        "--color",
        "never",
        "--output-last-message",
        str(output_path),
    ]
    if model:
        command.extend(["--model", model])
    command.append(build_prompt(case))
    return command


def resolve_codex_executable(override: str | None = None) -> str:
    if override:
        return override
    env_override = os.environ.get("CODEX_EXECUTABLE")
    if env_override:
        return env_override
    if sys.platform == "win32":
        codex_exe = shutil.which("codex.exe")
        if codex_exe:
            return codex_exe
    return shutil.which("codex") or "codex"


def build_prompt(case: PromptCase) -> str:
    return (
        "你是回归受测模型。必须先读取 `huifu-pay-integration/SKILL.md`，"
        "再按该 skill 的路由读取最少必要的 `huifu-pay-integration/references/*.md`。"
        "禁止凭通用支付经验回答；最终回答必须用“本轮实际使用 references：”列出不超过 5 份实际读取的 reference 文件名、关键 SDK 类或方法。"
        "暂不读、暂不推荐、禁止动作里不要列具体 .md 文件名。"
        "可以读取本地文件；禁止修改文件、联网或执行真实支付请求。"
        "回答控制在 500 字以内，只输出最终回答正文。\n\n"
        f"用户问题：{case.prompt}"
    )


def evaluate_case(case: PromptCase, text: str, output_path: Path, returncode: int) -> CaseResult:
    rule = RULES.get(case.case_id)
    if rule is None:
        return CaseResult(case.case_id, False, [f"missing RULES entry for case {case.case_id}"], [], [], output_path, returncode)
    required_groups = (REFERENCE_EVIDENCE_TERMS,) + tuple(
        group for group in rule.required_groups if group != REFERENCE_EVIDENCE_TERMS
    )
    missing = ["/".join(group) for group in required_groups if not contains_any(text, group)]
    reference_paths = extract_reference_mentions(text)
    policy_errors = []
    if len(reference_paths) > MAX_LISTED_REFERENCES:
        policy_errors.append(f"too many references listed: {len(reference_paths)} > {MAX_LISTED_REFERENCES}")
    forbidden_hits = forbidden_matches(text, rule.forbidden)
    passed = returncode == 0 and not missing and not forbidden_hits and not policy_errors
    return CaseResult(case.case_id, passed, missing, forbidden_hits, policy_errors, output_path, returncode)


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def extract_reference_mentions(text: str) -> list[str]:
    normalized_text = text.replace("\\", "/")
    mentions = set()
    for match in REFERENCE_MENTION_PATTERN.finditer(normalized_text):
        name = REFERENCE_FILE_NAME_LOOKUP.get(match.group(1).lower())
        if name:
            mentions.add(f"references/{name}")
    return sorted(mentions)


def forbidden_matches(text: str, patterns: tuple[str, ...]) -> list[str]:
    normalized_text = normalize_forbidden_text(text)
    return [pattern for pattern in patterns if re.search(pattern, normalized_text, flags=re.I)]


def normalize_forbidden_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def format_process_output(result: subprocess.CompletedProcess[str]) -> str:
    parts = [
        f"[returncode] {result.returncode}",
        "[stdout]",
        result.stdout.strip(),
        "[stderr]",
        result.stderr.strip(),
    ]
    return "\n".join(parts).strip() + "\n"


def format_timeout_output(exc: subprocess.TimeoutExpired, timeout: int) -> str:
    stdout = decode_timeout_stream(exc.stdout)
    stderr = decode_timeout_stream(exc.stderr)
    parts = [
        "[returncode] 124",
        f"[timeout] {timeout}",
        "[stdout]",
        stdout.strip(),
        "[stderr]",
        stderr.strip(),
    ]
    return "\n".join(parts).strip() + "\n"


def format_execution_error(exc: OSError, command: list[str]) -> str:
    parts = [
        "[returncode] 127" if isinstance(exc, FileNotFoundError) else "[returncode] 126",
        "[exec_error]",
        f"{type(exc).__name__}: {exc}",
        "[command]",
        " ".join(command[:3]) + " ...",
    ]
    return "\n".join(parts).strip() + "\n"


def decode_timeout_stream(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def write_summary(output_dir: Path, results: list[CaseResult]) -> None:
    payload = [
        {
            "id": result.case_id,
            "passed": result.passed,
            "missing": result.missing,
            "forbidden_hits": result.forbidden_hits,
            "policy_errors": result.policy_errors,
            "returncode": result.returncode,
            "output": str(result.output_path.relative_to(REPO_ROOT)),
        }
        for result in results
    ]
    (output_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_summary(output_dir: Path, results: list[CaseResult]) -> None:
    passed = sum(1 for result in results if result.passed)
    print(f"Real model regression: {passed}/{len(results)} passed")
    print(f"Output dir: {output_dir.relative_to(REPO_ROOT)}")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        details = []
        if result.returncode != 0:
            details.append(f"returncode={result.returncode}")
        if result.missing:
            details.append("missing=" + ", ".join(result.missing))
        if result.forbidden_hits:
            details.append("forbidden=" + ", ".join(result.forbidden_hits))
        if result.policy_errors:
            details.append("policy=" + ", ".join(result.policy_errors))
        suffix = " | " + "; ".join(details) if details else ""
        print(f"{status} case-{result.case_id:02d}{suffix}")


if __name__ == "__main__":
    sys.exit(main())
