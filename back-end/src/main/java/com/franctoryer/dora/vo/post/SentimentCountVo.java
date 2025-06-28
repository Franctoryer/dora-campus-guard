package com.franctoryer.dora.vo.post;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SentimentCountVo implements Serializable {
    /**
     * 标签 ID
     */
    private Long labelId;

    /**
     * 标签含义
     */
    private String labelName;

    /**
     * 对应标签的文档数
     */
    private Long count;
}
