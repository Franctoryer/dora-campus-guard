package com.franctoryer.dora.vo.post;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class KeywordTrendVo implements Serializable {
    /**
     * 时间字符串
     */
    private String dateTime;

    /**
     * 文档个数（讨论热度）
     */
    private Long count;
}
