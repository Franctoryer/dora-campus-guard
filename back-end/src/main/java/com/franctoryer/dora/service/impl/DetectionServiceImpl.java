package com.franctoryer.dora.service.impl;

import com.franctoryer.dora.dto.detection.DetectionSummaryDto;
import com.franctoryer.dora.es.repository.PostRepository;
import com.franctoryer.dora.service.DetectionService;
import com.franctoryer.dora.vo.detection.DetectionSummaryVo;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class DetectionServiceImpl implements DetectionService {
    private final PostRepository postRepository;
    /**
     * @param detectionSummaryDto
     * @return
     */
    @Override
    public DetectionSummaryVo getDetectionSummary(DetectionSummaryDto detectionSummaryDto) {
        return postRepository.getDetectionSummary(
              detectionSummaryDto.getStartTime(),
              detectionSummaryDto.getEndTime()
        );
    }
}
