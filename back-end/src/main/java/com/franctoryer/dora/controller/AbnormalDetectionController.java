package com.franctoryer.dora.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.franctoryer.dora.dto.detection.DetectionPostListDto;
import com.franctoryer.dora.dto.detection.DetectionSummaryDto;
import com.franctoryer.dora.service.DetectionService;
import com.franctoryer.dora.service.PostService;
import com.franctoryer.dora.vo.Result;
import com.franctoryer.dora.vo.detection.DetectionPostListVo;
import com.franctoryer.dora.vo.detection.DetectionSummaryVo;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 异常预警相关接口
 */
@RestController
@RequiredArgsConstructor
@RequestMapping("/rest/detection")
public class AbnormalDetectionController {

    private final PostService postService;
    private final DetectionService detectionService;

    /**
     * 获取一段时间内的舆情总结，总预警个数、低级、中级、高级的预警个数
     * @return
     */
    @GetMapping("/detection-summary")
    public Result<DetectionSummaryVo> getDetectionSummary(@Validated DetectionSummaryDto detectionSummaryDto) {
        return Result.success(
                detectionService.getDetectionSummary(detectionSummaryDto)
        );
    }

    /**
     * 获取异常的帖子列表
     * @return 异常的帖子列表
     */
    @GetMapping("/abnormal-post-list")
    public Result<IPage<DetectionPostListVo>> getAbnormalPostList(@Validated DetectionPostListDto detectionPostListDto) {
        return Result.success(
                postService.getDetectionPostPage(detectionPostListDto)
        );
    }
}
