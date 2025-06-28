package com.franctoryer.dora.service;

import com.franctoryer.dora.dto.detection.DetectionSummaryDto;
import com.franctoryer.dora.vo.detection.DetectionSummaryVo;

public interface DetectionService {
    /**
     * @param detectionSummaryDto
     * @return
     */
    DetectionSummaryVo getDetectionSummary(DetectionSummaryDto detectionSummaryDto);
}
