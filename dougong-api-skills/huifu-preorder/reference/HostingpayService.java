package hf.java.test1.ser.biz.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.exception.BasePayException;
import com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentPreorderH5Request;
import com.huifu.bspay.sdk.opps.core.utils.DateTools;
import com.huifu.bspay.sdk.opps.core.utils.SequenceTools;
import hf.java.test1.ser.util.enums.ResponseEnum;
import hf.java.test1.ser.util.exception.BizException;
import hf.java.test1.ser.util.spring.SpringUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@Service
public class HostingpayService {

    public Map<String, Object> preOrder(String huifuId, String amt, String goodsDesc) {
        V2TradeHostingPaymentPreorderH5Request request = getPreOrderRequest(huifuId, amt, goodsDesc);
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

    private static V2TradeHostingPaymentPreorderH5Request getPreOrderRequest(String huifuId, String transAmt, String goodsDesc) {
        V2TradeHostingPaymentPreorderH5Request request = new V2TradeHostingPaymentPreorderH5Request();
        request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
        request.setReqSeqId(SequenceTools.getReqSeqId32());
        request.setHuifuId(huifuId);
        request.setTransAmt(transAmt);
        request.setGoodsDesc(goodsDesc);
        request.setPreOrderType("1");
        request.setHostingData(getHostingData());
        Map<String, Object> extendInfoMap = getExtendInfos();
        request.setExtendInfo(extendInfoMap);
        return request;
    }

    private static String getHostingData() {
        ObjectNode dto = SpringUtil.getBean(ObjectMapper.class).createObjectNode();
        dto.put("project_title", "收银台标题");
        dto.put("project_id", "PROJECTID2023101225142567");
        dto.put("callback_url", "https://paas.huifu.com");
        dto.put("private_info", "商户私有信息test");
        return dto.toString();
    }

    private static Map<String, Object> getExtendInfos() {
        Map<String, Object> extendInfoMap = new HashMap<>(4);
        extendInfoMap.put("delay_acct_flag", "N");
        return extendInfoMap;
    }
}
