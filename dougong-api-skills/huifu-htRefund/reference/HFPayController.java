package hf.java.test1.ser.application.hfpay;

import com.alibaba.fastjson.JSONObject;
import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.config.MerConfig;
import com.huifu.bspay.sdk.opps.core.net.BasePayRequest;
import com.huifu.bspay.sdk.opps.core.utils.DateTools;
import com.huifu.bspay.sdk.opps.core.utils.SequenceTools;
import hf.java.test1.ser.biz.dto.Result;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@Controller
@RequestMapping("/hfpay")
@Slf4j
public class HFPayController {

    public static final String PRODUCT_ID = "YOUR_PRODUCT_ID";
    public static final String SYS_ID = "YOUR_SYS_ID";
    public static final String RSA_PRIVATE_KEY = "YOUR_RSA_PRIVATE_KEY";
    public static final String RSA_PUBLIC_KEY = "YOUR_RSA_PUBLIC_KEY";

    @PostMapping(value = "/htRefund", produces = "application/json", consumes = "application/json")
    @ResponseBody
    public Result<Map<String, Object>> htRefund(@RequestBody JSONObject req) throws Exception {
        MerConfig merConfig = new MerConfig();
        merConfig.setProcutId(PRODUCT_ID);
        merConfig.setSysId(SYS_ID);
        merConfig.setRsaPrivateKey(RSA_PRIVATE_KEY);
        merConfig.setRsaPublicKey(RSA_PUBLIC_KEY);
        BasePay.initWithMerConfig(merConfig);

        Map<String, Object> paramsInfo = new HashMap<>();
        paramsInfo.put("req_date", DateTools.getCurrentDateYYYYMMDD());
        paramsInfo.put("req_seq_id", SequenceTools.getReqSeqId32());
        paramsInfo.put("huifu_id", req.getString("huifuId"));
        paramsInfo.put("ord_amt", req.getString("ord_amt"));
        paramsInfo.put("org_req_date", req.getString("org_req_date"));
        paramsInfo.put("risk_check_data", "");
        paramsInfo.put("terminal_device_data", "{\"device_type\":\"4\"}");
        paramsInfo.put("bank_info_data", "");
        paramsInfo.put("org_req_seq_id", req.getString("org_req_seq_id"));
        paramsInfo.put("notify_url", "http://www.baidu.com");

        Map<String, Object> response = BasePayRequest.requestBasePay("v2/trade/hosting/payment/htRefund", paramsInfo, null, false);
        log.info("htRefund response:{}", response);
        return Result.ok(response);
    }
}
