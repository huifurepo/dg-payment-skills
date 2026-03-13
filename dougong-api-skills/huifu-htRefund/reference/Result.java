package hf.java.test1.ser.biz.dto;

import hf.java.test1.ser.util.enums.ResponseEnum;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.MDC;
import hf.java.test1.ser.util.constant.Constants;

@Data
public class Result<T> {

    private String respCode;
    private String respDesc;
    private String uniqueId;
    private T data;

    public static <T> Result<T> ok() {
        return new Result<T>().respCode(ResponseEnum.SUCCESS.getRespCode()).respDesc(ResponseEnum.SUCCESS.getRespDesc());
    }

    public static <T> Result<T> ok(T payload) {
        return new Result<T>().respCode(ResponseEnum.SUCCESS.getRespCode()).respDesc(ResponseEnum.SUCCESS.getRespDesc()).payload(payload);
    }

    public static <T> Result<T> fail(ResponseEnum ResponseEnum) {
        return new Result<T>().respCode(ResponseEnum.getRespCode()).respDesc(ResponseEnum.getRespDesc());
    }

    public static <T> Result<T> fail(String code, String message) {
        return new Result<T>().respCode(ResponseEnum.BUSI_CHECK_ERROR.getRespCode()).respDesc(message);
    }

    private Result<T> respCode(String respCode) {
        this.respCode = respCode;
        return this;
    }

    private Result<T> respDesc(String respDesc) {
        this.respDesc = respDesc;
        return this;
    }

    private Result<T> uniqueId(String uniqueId) {
        this.uniqueId = uniqueId;
        return this;
    }

    private Result<T> payload(T payload) {
        this.data = payload;
        return this;
    }

    public String getUniqueId() {
        if (StringUtils.isBlank(uniqueId)) {
            uniqueId = MDC.get(Constants.TRACE_ID);
        }
        return uniqueId;
    }
}
