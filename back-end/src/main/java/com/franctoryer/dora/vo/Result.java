package com.franctoryer.dora.vo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Result<T> implements Serializable {
    /**
     * 错误码，-1 表示正常响应
     */
    private Integer errCode;

    /**
     * 错误提示消息
     */
    private String errMsg;

    /**
     * 返回数据
     */
    private Object data;

    /**
     * 正常响应
     * @param data 返回数据
     * @return
     * @param <T>
     */
    public static <T> Result<T> success(T data) {
        return new Result<T>(-1, null, data);
    }

    /**
     * 错误响应
     * @param errCode 错误码
     * @param errMsg 错误提示
     * @return
     * @param <T>
     */
    public static <T> Result<T> fail(Integer errCode, String errMsg) {
        return new Result<T>(errCode, errMsg, null);
    }
}
