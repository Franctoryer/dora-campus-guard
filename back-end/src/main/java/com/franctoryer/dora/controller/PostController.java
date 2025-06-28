package com.franctoryer.dora.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.franctoryer.dora.dto.post.KeywordTrendDto;
import com.franctoryer.dora.dto.post.PostContentSearchDto;
import com.franctoryer.dora.dto.post.SentimentDistributionDto;
import com.franctoryer.dora.service.DeepseekService;
import com.franctoryer.dora.service.PostService;
import com.franctoryer.dora.vo.Result;
import com.franctoryer.dora.vo.post.KeywordTrendVo;
import com.franctoryer.dora.vo.post.PostListVo;
import com.franctoryer.dora.vo.post.SentimentCountVo;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CountDownLatch;

@RestController
@RequiredArgsConstructor
@RequestMapping("/rest/post")
@Slf4j
public class PostController {
    /**
     * 帖子相关业务逻辑
     */
    private final PostService postService;

    /**
     * DeepSeek API 服务
     */
    private final DeepseekService deepseekService;

    /**
     * 根据关键词、情感类型、话题类型、时间范围分页查询帖子（查 es）
     * @param postContentSearchDto 查询参数
     * @return 帖子列表
     */
    @GetMapping("/search")
    public Result<Page<PostListVo>> searchByContent(@Validated PostContentSearchDto postContentSearchDto) {
        return Result.success(
                postService.searchByContent(postContentSearchDto)
        );
    }

    /**
     * 根据关键词、话题类型、时间范围查询帖子的情感分布（es 聚合查询）
     * @return 情感分布
     */
    @GetMapping("/sentiment-distribution")
    public Result<List<SentimentCountVo>> getSentimentDistribution(@Validated SentimentDistributionDto sentimentDistributionDto) {
        List<SentimentCountVo> sentimentCountVos = postService.getSentimentDistribution(sentimentDistributionDto);
        return Result.success(sentimentCountVos);
    }

    /**
     * 查询关键词的讨论趋势
     * @return 讨论趋势
     */
    @GetMapping("/keyword-trend")
    public Result<List<KeywordTrendVo>> getKeywordTrend(@Validated KeywordTrendDto keywordTrendDto) {
        List<KeywordTrendVo> keywordTrendVos = postService.getKeywordTrend(keywordTrendDto);
        return Result.success(keywordTrendVos);
    }

    /**
     * 获取某一帖子的详情
     * @param postId 帖子 ID
     * @return 帖子详情
     */
    @GetMapping("/{postId}/detail")
    public Result<?> getPostDetail(@PathVariable Integer postId) {
        return null;
    }

    /**
     * 查询结果 AI 总结
     * @param postContentSearchDto 查询参数
     * @return AI 总结
     */
    @GetMapping("search-summary")
    public SseEmitter getSearchSummary(@Validated PostContentSearchDto postContentSearchDto) {
        SseEmitter emitter = new SseEmitter();

        new Thread(() -> {
            try {
                List<PostListVo> postListVos = postService.searchByContent(postContentSearchDto).getContent();
                ObjectMapper objectMapper = new ObjectMapper();
                String context = objectMapper.writeValueAsString(postListVos);

                List<Map<String, String>> messages = List.of(
                        Map.of("role", "system", "content", "你是一个校圈舆情分析的AI助手，你需要对用户的搜索结果进行总结，总结精简凝练，不超过 300字"),
                        Map.of("role", "user", "content", "以下是部分查询结果，请根据这些查询结果简要概括校圈对该关键词的总体舆论情况：\n" + context)
                );

                CountDownLatch latch = new CountDownLatch(1);

                // DeepSeek 流式调用
                deepseekService.streamChat(messages, chunk -> {
                    try {
                        log.info("发送数据：" + chunk);
                        emitter.send(SseEmitter.event().data(chunk));
                    } catch (IOException  e) {
                        emitter.completeWithError(e);
                        latch.countDown();
                    }
                }, () -> {
                    // DeepSeek 流结束后调用
                    try {
                        emitter.send(SseEmitter.event().data("[DONE]"));
                    } catch (IOException e) {
                        emitter.completeWithError(e);
                    }
                    emitter.complete();
                    latch.countDown(); // ✅ 结束标志
                });

                latch.await(); // ✅ 等待 deepseek 流式调用结束

            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        }).start();

        return emitter;
    }

}
