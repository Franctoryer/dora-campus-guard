package com.franctoryer.dora.service.impl;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.franctoryer.dora.bo.post.SentimentCountBo;
import com.franctoryer.dora.constant.SentimentConstant;
import com.franctoryer.dora.dto.detection.DetectionPostListDto;
import com.franctoryer.dora.dto.post.KeywordTrendDto;
import com.franctoryer.dora.dto.post.PostContentSearchDto;
import com.franctoryer.dora.dto.post.SentimentDistributionDto;
import com.franctoryer.dora.es.entity.PostEsEntity;
import com.franctoryer.dora.es.repository.PostRepository;
import com.franctoryer.dora.mapper.PostMapper;
import com.franctoryer.dora.mapper.UserMapper;
import com.franctoryer.dora.service.PostService;
import com.franctoryer.dora.service.UserService;
import com.franctoryer.dora.vo.detection.DetectionPostListVo;
import com.franctoryer.dora.vo.post.KeywordTrendVo;
import com.franctoryer.dora.vo.post.PostListVo;
import com.franctoryer.dora.vo.post.PostUserVo;
import com.franctoryer.dora.vo.post.SentimentCountVo;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class PostServiceImpl implements PostService {
    private final PostRepository postRepository;
    private final UserMapper userMapper;
    private final UserService userService;
    private final PostMapper postMapper;

    /**
     * 根据关键词分页查询
     * @param postContentSearchDto 分页参数
     * @return 一页帖子
     */
    @Override
    public Page<PostListVo> searchByContent(PostContentSearchDto postContentSearchDto) {
        // 关键词
        String keyword = postContentSearchDto.getKeyword();
        // 分页参数（页码、每页数量）
        Integer page = postContentSearchDto.getPage();
        Integer size = postContentSearchDto.getSize();
        if (page == null) page = 0;  // 默认页码，防止空指针报错
        if (size == null) size = 10; // 默认每页数量
        Pageable pageable = PageRequest.of(page, size);
        // 情感标签
        Integer sentimentLabel = postContentSearchDto.getSentimentLabel();
        // 话题 ID
        Integer topicId = postContentSearchDto.getTopicId();
        // 开始时间和结束时间
        LocalDateTime startTime = postContentSearchDto.getStartTime();
        LocalDateTime endTime = postContentSearchDto.getEndTime();

        Page<PostEsEntity> postEsEntities = postRepository.findByContentContaining(keyword, 16, pageable, sentimentLabel, topicId, startTime, endTime);
        // 查用户信息
        List<PostEsEntity> postList = postEsEntities.getContent();
        if (postList.isEmpty()) {
            return new PageImpl<PostListVo>(List.of(), postEsEntities.getPageable(), postEsEntities.getTotalElements());
        }
        List<Long> uids = postList.stream()
                .map(PostEsEntity::getUid)
                .filter(Objects::nonNull)
                .distinct()
                .toList();
        List<PostUserVo> userList = userService.getDetailByUids(uids);
        // 把用户信息转成 map
        Map<Long, PostUserVo> userMap = userList.stream().collect(Collectors.toMap(PostUserVo::getUid, Function.identity()));

        // 将用户信息插入帖子数据
        List<PostListVo> postListVos = new ArrayList<>();
        postList.forEach(postEsEntity -> {
            postListVos.add(new PostListVo(postEsEntity, userMap.get(postEsEntity.getUid())));
        });

        // 返回分页结果
        return new PageImpl<PostListVo>(
                postListVos,
                postEsEntities.getPageable(),
                postEsEntities.getTotalElements()
        );
    }

    @Override
    public List<SentimentCountVo> getSentimentDistribution(SentimentDistributionDto sentimentDistributionDto) {
        // 解析查询参数
        String keyword = sentimentDistributionDto.getKeyword();
        Integer topicId = sentimentDistributionDto.getTopicId();
        LocalDateTime startTime = sentimentDistributionDto.getStartTime();
        LocalDateTime endTime = sentimentDistributionDto.getEndTime();
        // 查 ES，获取情感分布
        List<SentimentCountBo> sentimentDistributionBos = postRepository.getSentimentDistribution(keyword, 16, topicId, startTime, endTime);
        // 返回结果
        List<SentimentCountVo> sentimentCountVos = new ArrayList<>();
        // 增加 labelName 参数
        for (SentimentCountBo sentimentCountBo : sentimentDistributionBos) {
            long labelId = sentimentCountBo.getLabelId();
            long count = sentimentCountBo.getCount();
            String labelName = SentimentConstant.SENTIMENT_LABEL_MAP.get(labelId);

            sentimentCountVos.add(new SentimentCountVo(labelId, labelName, count));
        }

        return sentimentCountVos;
    }

    @Override
    public List<KeywordTrendVo> getKeywordTrend(KeywordTrendDto keywordTrendDto) {
        // 解析查询参数
        String keyword = keywordTrendDto.getKeyword();
        String interval = keywordTrendDto.getInterval();
        LocalDateTime startTime = keywordTrendDto.getStartTime();
        LocalDateTime endTime = keywordTrendDto.getEndTime();
        return postRepository.getKeywordTrend(keyword, startTime, endTime, interval, 16);
    }

    /**
     * 获取异常的帖子列表
     *
     * @param dto 分页参数
     * @return 帖子列表
     */
    @Override
    public IPage<DetectionPostListVo> getDetectionPostPage(DetectionPostListDto dto) {
        com.baomidou.mybatisplus.extension.plugins.pagination.Page<DetectionPostListVo> page = com.baomidou.mybatisplus.extension.plugins.pagination.Page.of(dto.getPageNum(), dto.getPageSize());
        return postMapper.selectDetectionPostPage(page, dto.getAbnormalIndex());
    }
}
