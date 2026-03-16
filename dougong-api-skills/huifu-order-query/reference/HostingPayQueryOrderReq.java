package hf.java.test1.ser.biz.dto.hostingpay;

import hf.java.test1.ser.biz.dto.BaseRequest;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
public class HostingPayQueryOrderReq extends BaseRequest {
    private String huifuId;
    private String orgReqDate;
    private String orgReqSeqId;
}
