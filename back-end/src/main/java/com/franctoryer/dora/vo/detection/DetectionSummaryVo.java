package com.franctoryer.dora.vo.detection;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class DetectionSummaryVo {
    /**
     * 低级预警个数
     */
    private Long lowCount;

    /**
     * 中级预警个数
     */
    private Long mediumCount;

    /**
     * 高级预警个数
     */
    private Long highCount;

    /**
     * 总预警数
     */
    private Long total;
}
