package com.franctoryer.dora.dto.post;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;

import java.io.Serializable;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SentimentDistributionDto implements Serializable {
    /**
     * 关键词
     */
    @Length(max = 50, message = "关键词不能超过 50 个字符")
    private String keyword;

    /**
     * 话题 ID
     */
    private Integer topicId;

    /**
     * 开始时间
     */
    private LocalDateTime startTime;

    /**
     * 结束时间
     */
    private LocalDateTime endTime;
}
