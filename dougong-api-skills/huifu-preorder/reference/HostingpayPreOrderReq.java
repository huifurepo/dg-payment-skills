package hf.java.test1.ser.biz.dto.hostingpay;

import lombok.Data;
import lombok.EqualsAndHashCode;
import hf.java.test1.ser.biz.dto.BaseRequest;

@Data
@EqualsAndHashCode(callSuper = false)
public class HostingpayPreOrderReq extends BaseRequest {
    private String huifuId;
    private String transAmt;
    private String goodsDesc;
}
