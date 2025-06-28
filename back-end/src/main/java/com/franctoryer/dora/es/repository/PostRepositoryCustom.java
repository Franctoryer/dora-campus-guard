package com.franctoryer.dora.es.repository;

import com.franctoryer.dora.bo.post.SentimentCountBo;
import com.franctoryer.dora.es.entity.PostEsEntity;
import com.franctoryer.dora.vo.detection.DetectionSummaryVo;
import com.franctoryer.dora.vo.post.KeywordTrendVo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.time.LocalDateTime;
import java.util.List;

public interface PostRepositoryCustom {
    /**
     * 查询帖子列表
     * @param keyword 关键词
     * @param schoolId 学校 ID（暂时只有上财 16）
     * @param pageable 分页参数
     * @param sentimentLabel 情感标签
     * @param topicId 话题 ID
     * @param startTime 开始时间
     * @param endTime 结束时间
     * @return 帖子列表
     */
    Page<PostEsEntity> findByContentContaining(String keyword, Integer schoolId, Pageable pageable, Integer sentimentLabel, Integer topicId, LocalDateTime startTime, LocalDateTime endTime);

    /**
     * 查询一定条件下的帖子情感分布
     * @param keyword 关键词
     * @param schoolId 学校 ID（暂时只有上财 16）
     * @param topicId 话题 ID
     * @param startTime 开始时间
     * @param endTime 结束时间
     * @return 情感分布
     */
    List<SentimentCountBo> getSentimentDistribution(String keyword, Integer schoolId, Integer topicId, LocalDateTime startTime, LocalDateTime endTime);

    /**
     * 查询某个关键词的讨论趋势
     * @param keyword 关键词
     * @param startTime 开始时间
     * @param endTime 结束时间
     * @param interval 时间间隔
     * @param schoolId 学校 ID
     * @return 每个一段时间关键词对应的帖子个数
     */
    List<KeywordTrendVo> getKeywordTrend(String keyword, LocalDateTime startTime, LocalDateTime endTime, String interval, Integer schoolId);

    /**
     * 获取一段时间内的预警个数情况
     * @param startTime 开始时间
     * @param endTime 结束时间
     * @return 总预警数、低级、中级、高级预警个数
     */
    DetectionSummaryVo getDetectionSummary(LocalDateTime startTime, LocalDateTime endTime);
}
