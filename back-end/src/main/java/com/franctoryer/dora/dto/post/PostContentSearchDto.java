package com.franctoryer.dora.dto.post;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PostContentSearchDto {
    /**
     * 关键词
     */
    @Length(max = 50, message = "关键词不能超过 50 个字符")
    private String keyword;

    /**
     * 页码
     */
    private Integer page;

    /**
     * 每页数量
     */
    @Max(value = 40, message = "每页数量不能超过 40")
    private Integer size;

    /**
     * 情感标签
     */
    @Min(value = 0, message = "标签值不合法")
    @Max(value = 6, message = "标签值不合法")
    private Integer sentimentLabel;

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
