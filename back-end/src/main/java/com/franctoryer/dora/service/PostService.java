package com.franctoryer.dora.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.franctoryer.dora.dto.detection.DetectionPostListDto;
import com.franctoryer.dora.dto.post.KeywordTrendDto;
import com.franctoryer.dora.dto.post.PostContentSearchDto;
import com.franctoryer.dora.dto.post.SentimentDistributionDto;
import com.franctoryer.dora.vo.detection.DetectionPostListVo;
import com.franctoryer.dora.vo.post.KeywordTrendVo;
import com.franctoryer.dora.vo.post.PostListVo;
import com.franctoryer.dora.vo.post.SentimentCountVo;
import org.springframework.data.domain.Page;

import java.util.List;


public interface PostService {
    /**
     * 根据关键词等参数查询帖子列表
     * @param postContentSearchDto 查询参数（关键词、情感类型等）
     * @return 帖子列表
     */
    Page<PostListVo> searchByContent(PostContentSearchDto postContentSearchDto);

    /**
     * 获取查询结果的情感分布
     * @param sentimentDistributionDto 查询参数（不包括情感类型和分页参数）
     * @return 帖子情感分布
     */
    List<SentimentCountVo> getSentimentDistribution(SentimentDistributionDto sentimentDistributionDto);

    /**
     * 查询一个关键词的讨论趋势
     * @param keywordTrendDto 查询参数
     * @return 关键词随时间的讨论趋势
     */
    List<KeywordTrendVo> getKeywordTrend(KeywordTrendDto keywordTrendDto);

    /**
     * 获取异常的帖子列表
     * @param dto 分页参数
     * @return 帖子列表
     */
    IPage<DetectionPostListVo> getDetectionPostPage(DetectionPostListDto dto);
}
