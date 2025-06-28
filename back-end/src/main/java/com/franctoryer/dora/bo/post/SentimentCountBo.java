package com.franctoryer.dora.bo.post;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SentimentCountBo implements Serializable {
    /**
     * 标签 ID
     */
    private Long labelId;

    /**
     * 对应标签的文档数
     */
    private Long count;
}
