package hf.java.test1.ser.application.hfpay;

import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.config.MerConfig;
import hf.java.test1.ser.biz.dto.Result;
import hf.java.test1.ser.biz.dto.hostingpay.HostingpayPreOrderReq;
import hf.java.test1.ser.biz.service.HostingpayService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Controller
@RequestMapping("/hfpay")
@Slf4j
public class HFPayController {

    public static final String PRODUCT_ID = "YOUR_PRODUCT_ID";
    public static final String SYS_ID = "YOUR_SYS_ID";
    public static final String RSA_PRIVATE_KEY = "YOUR_RSA_PRIVATE_KEY";
    public static final String RSA_PUBLIC_KEY = "YOUR_RSA_PUBLIC_KEY";

    @Autowired
    private HostingpayService hostingpayService;

    @PostMapping(value = "/preOrder", produces = "application/json", consumes = "application/json")
    @ResponseBody
    public Result<Map<String, Object>> preOrder(@RequestBody HostingpayPreOrderReq req) throws Exception {
        MerConfig merConfig = new MerConfig();
        merConfig.setProcutId(PRODUCT_ID);
        merConfig.setSysId(SYS_ID);
        merConfig.setRsaPrivateKey(RSA_PRIVATE_KEY);
        merConfig.setRsaPublicKey(RSA_PUBLIC_KEY);
        BasePay.initWithMerConfig(merConfig);

        Map<String, Object> response = hostingpayService.preOrder(req.getHuifuId(), req.getTransAmt(), req.getGoodsDesc());
        log.info("pre order result:" + response);
        return Result.ok(response);
    }
}
