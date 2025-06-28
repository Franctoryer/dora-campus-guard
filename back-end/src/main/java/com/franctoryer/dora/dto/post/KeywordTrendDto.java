package com.franctoryer.dora.dto.post;

import jakarta.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;

import java.time.LocalDateTime;

/**
 * 查询某个关键词讨论趋势的参数
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class KeywordTrendDto {
    /**
     * 关键词
     */
    @Length(max = 50, message = "关键词不能超过 50 个字符")
     private String keyword;

    /**
     * 开始时间
     */
    private LocalDateTime startTime;

    /**
     * 结束时间
     */
    private LocalDateTime endTime;

    /**
     * 时间间隔 day / month / year
     */
    @Pattern(regexp = "^(day|month|year)$", message = "时间间隔只能是 day, month, year")
    private String interval;
}
