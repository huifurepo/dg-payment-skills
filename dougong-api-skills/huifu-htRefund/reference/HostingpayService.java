package hf.java.test1.ser.biz.service;

import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.exception.BasePayException;
import com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentHtrefundRequest;
import com.huifu.bspay.sdk.opps.core.utils.DateTools;
import com.huifu.bspay.sdk.opps.core.utils.SequenceTools;
import hf.java.test1.ser.util.enums.ResponseEnum;
import hf.java.test1.ser.util.exception.BizException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@Service
public class HostingpayService {

    public Map<String, Object> htRefund(String huifuId, String ordAmt, String orgReqDate, String orgReqSeqId) {
        V2TradeHostingPaymentHtrefundRequest request = getHtRefundRequest(huifuId, ordAmt, orgReqDate, orgReqSeqId);
        Map<String, Object> response;
        try {
            response = BasePayClient.request(request, false);
            return response;
        } catch (BasePayException e) {
            throw new BizException(ResponseEnum.SYSTEM_ERROR);
        } catch (IllegalAccessException e) {
            throw new BizException(ResponseEnum.SYSTEM_ERROR);
        }
    }

    private static V2TradeHostingPaymentHtrefundRequest getHtRefundRequest(String huifuId, String ordAmt, String orgReqDate, String orgReqSeqId) {
        V2TradeHostingPaymentHtrefundRequest request = new V2TradeHostingPaymentHtrefundRequest();
        request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
        request.setReqSeqId(SequenceTools.getReqSeqId32());
        request.setHuifuId(huifuId);
        request.setOrdAmt(ordAmt);
        request.setOrgReqDate(orgReqDate);

        Map<String, Object> extendInfoMap = getHtRefundExtendInfos(orgReqSeqId);
        request.setExtendInfo(extendInfoMap);
        return request;
    }

    private static Map<String, Object> getHtRefundExtendInfos(String orgReqSeqId) {
        Map<String, Object> extendInfoMap = new HashMap<>(4);
        extendInfoMap.put("org_req_seq_id", orgReqSeqId);
        extendInfoMap.put("risk_check_data", "");
        extendInfoMap.put("terminal_device_data", "{\"device_type\":\"4\"}");
        extendInfoMap.put("bank_info_data", "");
        extendInfoMap.put("notify_url", "http://www.baidu.com");
        return extendInfoMap;
    }
}
