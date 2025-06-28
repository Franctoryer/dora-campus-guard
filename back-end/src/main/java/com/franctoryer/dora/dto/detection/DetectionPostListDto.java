package com.franctoryer.dora.dto.detection;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class DetectionPostListDto implements Serializable {
    /**
     * 页码
     */
    private Integer pageNum;

    /**
     * 每页数量
     */
    @Max(value = 40, message = "每页数量不能超过 40")
    private Integer pageSize;

    /**
     * 预警级别（1，2，3）
     */
    @Min(value = 1, message = "预警级别不合法")
    @Max(value = 3, message = "预警级别不合法")
    private Integer abnormalIndex;
}
