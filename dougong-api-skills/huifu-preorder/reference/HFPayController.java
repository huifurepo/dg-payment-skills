package hf.java.test1.ser.application.hfpay;

import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.config.MerConfig;
import com.huifu.bspay.sdk.opps.core.net.BasePayRequest;
import com.huifu.bspay.sdk.opps.core.utils.DateTools;
import com.huifu.bspay.sdk.opps.core.utils.SequenceTools;
import hf.java.test1.ser.biz.dto.Result;
import hf.java.test1.ser.biz.dto.hostingpay.HostingpayPreOrderReq;
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

    @PostMapping(value = "/preOrder", produces = "application/json", consumes = "application/json")
    @ResponseBody
    public Result<Map<String, Object>> preOrder(@RequestBody HostingpayPreOrderReq req) throws Exception {
        MerConfig merConfig = new MerConfig();
        merConfig.setProcutId(PRODUCT_ID);
        merConfig.setSysId(SYS_ID);
        merConfig.setRsaPrivateKey(RSA_PRIVATE_KEY);
        merConfig.setRsaPublicKey(RSA_PUBLIC_KEY);
        BasePay.initWithMerConfig(merConfig);

        Map<String, Object> paramsInfo = new HashMap<>();
        paramsInfo.put("req_date", DateTools.getCurrentDateYYYYMMDD());
        paramsInfo.put("req_seq_id", SequenceTools.getReqSeqId32());
        paramsInfo.put("huifu_id", req.getHuifuId());
        paramsInfo.put("trans_amt", req.getTransAmt());
        paramsInfo.put("goods_desc", req.getGoodsDesc());
        paramsInfo.put("pre_order_type", "1");
        paramsInfo.put("hosting_data", "{\"project_title\":\"收银台标题\",\"project_id\":\"PROJECTID2023101225142567\",\"private_info\":\"商户私有信息test\",\"callback_url\":\"https://paas.huifu.com\"}");
        paramsInfo.put("delay_acct_flag", "N");
        paramsInfo.put("notify_url", "https://callback.service.com/xx");

        Map<String, Object> response = BasePayRequest.requestBasePay("v2/trade/hosting/payment/preorder", paramsInfo, null, false);
        log.info("pre order result:" + response);
        return Result.ok(response);
    }
}
