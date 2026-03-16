package hf.java.test1.ser.biz.service;

import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.exception.BasePayException;
import com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentQueryorderinfoRequest;
import com.huifu.bspay.sdk.opps.core.utils.DateTools;
import com.huifu.bspay.sdk.opps.core.utils.SequenceTools;
import hf.java.test1.ser.util.enums.ResponseEnum;
import hf.java.test1.ser.util.exception.BizException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.Map;

@Slf4j
@Service
public class HostingpayService {

    public Map<String, Object> queryOrderInfo(String huifuId, String orgReqDate, String orgReqSeqId) {
        V2TradeHostingPaymentQueryorderinfoRequest request = getQueryOrderInfoRequest(huifuId, orgReqDate, orgReqSeqId);
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

    private static V2TradeHostingPaymentQueryorderinfoRequest getQueryOrderInfoRequest(String huifuId, String orgReqDate, String orgReqSeqId) {
        V2TradeHostingPaymentQueryorderinfoRequest request = new V2TradeHostingPaymentQueryorderinfoRequest();
        request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
        request.setReqSeqId(SequenceTools.getReqSeqId32());
        request.setHuifuId(huifuId);
        request.setOrgReqDate(orgReqDate);
        request.setOrgReqSeqId(orgReqSeqId);
        return request;
    }
}
