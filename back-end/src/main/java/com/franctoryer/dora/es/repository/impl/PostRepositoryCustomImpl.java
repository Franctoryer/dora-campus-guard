package com.franctoryer.dora.es.repository.impl;

import co.elastic.clients.elasticsearch._types.SortOrder;
import co.elastic.clients.elasticsearch._types.aggregations.*;
import com.franctoryer.dora.bo.post.SentimentCountBo;
import com.franctoryer.dora.es.entity.PostEsEntity;
import com.franctoryer.dora.es.repository.PostRepositoryCustom;
import com.franctoryer.dora.util.TimeUtil;
import com.franctoryer.dora.vo.detection.DetectionSummaryVo;
import com.franctoryer.dora.vo.post.KeywordTrendVo;
import lombok.RequiredArgsConstructor;
import org.elasticsearch.client.RestClient;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.elasticsearch.client.elc.ElasticsearchAggregation;
import org.springframework.data.elasticsearch.client.elc.ElasticsearchAggregations;
import org.springframework.data.elasticsearch.client.elc.NativeQuery;
import org.springframework.data.elasticsearch.client.elc.NativeQueryBuilder;
import org.springframework.data.elasticsearch.core.AggregationsContainer;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.data.elasticsearch.core.query.HighlightQuery;
import org.springframework.data.elasticsearch.core.query.Query;
import org.springframework.data.elasticsearch.core.query.highlight.Highlight;
import org.springframework.data.elasticsearch.core.query.highlight.HighlightField;
import org.springframework.data.elasticsearch.core.query.highlight.HighlightParameters;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

@Component
@RequiredArgsConstructor
public class PostRepositoryCustomImpl implements PostRepositoryCustom {

    private final ElasticsearchOperations elasticsearchOperations;
    private final RestClient elasticsearchRestClient;

    @Override
    public Page<PostEsEntity> findByContentContaining(String keyword, Integer schoolId, Pageable pageable, Integer sentimentLabel, Integer topicId, LocalDateTime startTime, LocalDateTime endTime) {
        // 高亮配置
        HighlightField highlightField = new HighlightField("content");
        HighlightParameters highlightParameters = HighlightParameters.builder()
                .withPreTags("<b class=\"keyword\">")
                .withPostTags("</b>")
                .build();
        Highlight highlight = new Highlight(highlightParameters, List.of(highlightField));
        HighlightQuery highlightQuery = new HighlightQuery(highlight, PostEsEntity.class);

        NativeQueryBuilder queryBuilder = NativeQuery.builder();
        // 构造 bool 查询
        queryBuilder.withQuery(q -> q.bool(b -> {
            // 动态添加 match（当 keyword 非空时）
            if (StringUtils.hasText(keyword)) {
                b.must(m -> m.match(match -> match
                        .field("content")
                        .analyzer("ik_max_word")
                        .query(keyword)
                ));
            }

            // 添加 filter：school_id 不为空时才加
            if (schoolId != null) {
                b.filter(f -> f.term(t -> t
                        .field("school_id")
                        .value(schoolId)
                ));
            }

            // 根据情感标签筛选
            if (sentimentLabel != null) {
                b.filter(f -> f.term( t -> t
                        .field("sentiment_label")
                        .value(sentimentLabel)
                ));
            }

            // 根据话题筛选
            if (topicId != null) {
                b.filter(f -> f.term(t -> t
                        .field("topic_id")
                        .value(topicId)
                ));
            }

            // 根据时间筛选
            if (startTime != null || endTime != null) {
                b.filter(f -> f.range(r -> r.date(rd -> {
                    rd = rd.field("published_at");
                    if (startTime != null) {
                        rd.gte(startTime.format(DateTimeFormatter.ISO_DATE_TIME));
                    }
                    if (endTime != null) {
                        rd.lte(endTime.format(DateTimeFormatter.ISO_DATE_TIME));
                    }

                    return rd;
                })));
            }


            return b;
        }));

        // 如果 keyword 为空，加排序
        if (!StringUtils.hasText(keyword)) {
            queryBuilder.withSort(s -> s.field(f -> f.field("published_at").order(SortOrder.Desc)));
        }

        // 其他部分：高亮、分页
        queryBuilder.withHighlightQuery(highlightQuery);
        queryBuilder.withPageable(pageable);

        // 构建最终 Query
        Query query = queryBuilder.build();

        SearchHits<PostEsEntity> hits = elasticsearchOperations.search(query, PostEsEntity.class);
        List<PostEsEntity> content = hits.stream().map(hit -> {
            PostEsEntity entity = hit.getContent();

            // 提取高亮字段
            List<String> highlights = hit.getHighlightFields().get("content");
            if (highlights != null && !highlights.isEmpty()) {
                entity.setContent(highlights.get(0)); // 用高亮内容替换原内容
            }

            return entity;
        }).toList();

        return new PageImpl<>(content, pageable, hits.getTotalHits());
    }

    @Override
    public List<SentimentCountBo> getSentimentDistribution(String keyword, Integer schoolId, Integer topicId, LocalDateTime startTime, LocalDateTime endTime) {
        NativeQueryBuilder queryBuilder = NativeQuery.builder();
        // 构造 bool 查询
        queryBuilder.withQuery(q -> q.bool(b -> {
            // 动态添加 match（当 keyword 非空时）
            if (StringUtils.hasText(keyword)) {
                b.must(m -> m.match(match -> match
                        .field("content")
                        .analyzer("ik_max_word")
                        .query(keyword)
                ));
            }

            // 添加 filter：school_id 不为空时才加
            if (schoolId != null) {
                b.filter(f -> f.term(t -> t
                        .field("school_id")
                        .value(schoolId)
                ));
            }

            // 根据话题筛选
            if (topicId != null) {
                b.filter(f -> f.term(t -> t
                        .field("topic_id")
                        .value(topicId)
                ));
            }

            // 根据时间筛选
            if (startTime != null || endTime != null) {
                b.filter(f -> f.range(r -> r.date(rd -> {
                    rd = rd.field("published_at");
                    if (startTime != null) {
                        rd.gte(startTime.format(DateTimeFormatter.ISO_DATE_TIME));
                    }
                    if (endTime != null) {
                        rd.lte(endTime.format(DateTimeFormatter.ISO_DATE_TIME));
                    }

                    return rd;
                })));
            }


            return b;
        }));

        // 构造 聚合查询
        Aggregation aggregation = Aggregation.of(a -> a
                .terms(t -> t
                        .field("sentiment_label")
                        .size(10)
                )
        );
        queryBuilder.withAggregation("sentiment_distribution", aggregation);

        // 不返回文档，只聚合
        queryBuilder.withMaxResults(0);

        // 构造最终的查询
        Query query = queryBuilder.build();

        // 查询结果
        SearchHits<PostEsEntity> searchHits = elasticsearchOperations.search(query, PostEsEntity.class);
        // 获取聚合结果
        AggregationsContainer<?> aggregationsContainer = searchHits.getAggregations();

        // 强转为实际类型
        ElasticsearchAggregations aggregations = (ElasticsearchAggregations) aggregationsContainer;
        // 拿到单个聚合（根据 queryBuilder.withAggregation(...) 里定义的名字）
        if (aggregations == null) {
            return List.of();
        }
        ElasticsearchAggregation agg = aggregations.get("sentiment_distribution");
        // 拿到 Elasticsearch Java Client 的 Aggregate 对象
        if (agg == null) {
            return List.of();
        }
        Aggregate aggregate = agg.aggregation().getAggregate();
        // 最后的结果
        List<SentimentCountBo> sentimentCountBoList = new ArrayList<>();
        // 判断是否是 Long 类型的 Item
        if (aggregate.isLterms()) {
            LongTermsAggregate lterms = aggregate.lterms();
            for (LongTermsBucket bucket : lterms.buckets().array()) {
                long label = bucket.key();
                long count = bucket.docCount();
                sentimentCountBoList.add(new SentimentCountBo(label, count));
            }

        }

        return sentimentCountBoList;
    }

    @Override
    public List<KeywordTrendVo> getKeywordTrend(String keyword, LocalDateTime startTime, LocalDateTime endTime, String interval, Integer schoolId) {
        NativeQueryBuilder queryBuilder = NativeQuery.builder();

        // 构造 bool 查询
        queryBuilder.withQuery(q -> q.bool(b -> {
            // 动态添加 match（当 keyword 非空时）
            if (StringUtils.hasText(keyword)) {
                b.must(m -> m.match(match -> match
                        .field("content")
                        .analyzer("ik_max_word")
                        .query(keyword)
                ));
            }

            // 添加 filter：school_id 不为空时才加
            if (schoolId != null) {
                b.filter(f -> f.term(t -> t
                        .field("school_id")
                        .value(schoolId)
                ));
            }

            // 根据时间筛选
            if (startTime != null || endTime != null) {
                b.filter(f -> f.range(r -> r.date(rd -> {
                    rd = rd.field("published_at");
                    if (startTime != null) {
                        rd.gte(startTime.format(DateTimeFormatter.ISO_DATE_TIME));
                    }
                    if (endTime != null) {
                        rd.lte(endTime.format(DateTimeFormatter.ISO_DATE_TIME));
                    }

                    return rd;
                })));
            }
            return b;
        }));

        // 构造聚合查询：按时间间隔分组
        Aggregation aggregation = Aggregation.of(a -> a
                .dateHistogram(dh -> dh
                        .field("published_at")
                        .calendarInterval(TimeUtil.convertStrToCalendar(interval)) // 例如 "day", "month"
                        .format("yyyy-MM-dd")
                        .timeZone("+08:00")
                )
        );
        queryBuilder.withAggregation("time_trend", aggregation);

        // 只查聚合
        queryBuilder.withMaxResults(0);

        // 构建并查询
        Query query = queryBuilder.build();
        SearchHits<PostEsEntity> hits = elasticsearchOperations.search(query, PostEsEntity.class);

        AggregationsContainer<?> aggregationsContainer = hits.getAggregations();
        if (aggregationsContainer == null) return List.of();

        ElasticsearchAggregations aggregations = (ElasticsearchAggregations) aggregationsContainer;
        ElasticsearchAggregation trendAgg = aggregations.get("time_trend");
        if (trendAgg == null) return List.of();

        Aggregate aggregate = trendAgg.aggregation().getAggregate();
        List<KeywordTrendVo> result = new ArrayList<>();

        if (aggregate.isDateHistogram()) {
            DateHistogramAggregate dateHistogram = aggregate.dateHistogram();
            for (DateHistogramBucket bucket : dateHistogram.buckets().array()) {
                String date = bucket.keyAsString(); // 格式化后的日期字符串
                long count = bucket.docCount();
                result.add(new KeywordTrendVo(date, count));
            }
        }

        return result;
    }

    /**
     * 获取一段时间内的预警个数情况
     *
     * @param startTime 开始时间
     * @param endTime   结束时间
     * @return 总预警数、低级、中级、高级预警个数
     */
    @Override
    public DetectionSummaryVo getDetectionSummary(LocalDateTime startTime, LocalDateTime endTime) {
        NativeQueryBuilder queryBuilder = NativeQuery.builder();

        // 时间过滤条件
        queryBuilder.withQuery(q -> q.bool(b -> {
            if (startTime != null || endTime != null) {
                b.filter(f -> f.range(r -> r.date(rd -> {
                    rd = rd.field("published_at");
                    if (startTime != null) {
                        rd.gte(startTime.format(DateTimeFormatter.ISO_DATE_TIME));
                    }
                    if (endTime != null) {
                        rd.lte(endTime.format(DateTimeFormatter.ISO_DATE_TIME));
                    }
                    return rd;
                })));
            }
            return b;
        }));

        // 聚合 abnormal_index 字段
        Aggregation agg = Aggregation.of(a -> a
                .terms(t -> t
                        .field("abnormal_index")
                        .size(10) // 足够覆盖 0~3
                )
        );
        queryBuilder.withAggregation("abnormal_distribution", agg);

        // 不查文档
        queryBuilder.withMaxResults(0);

        // 执行查询
        Query query = queryBuilder.build();
        SearchHits<PostEsEntity> hits = elasticsearchOperations.search(query, PostEsEntity.class);

        AggregationsContainer<?> aggregationsContainer = hits.getAggregations();
        if (aggregationsContainer == null) return new DetectionSummaryVo(0L, 0L, 0L, 0L);

        ElasticsearchAggregations aggregations = (ElasticsearchAggregations) aggregationsContainer;
        ElasticsearchAggregation abnormalAgg = aggregations.get("abnormal_distribution");
        if (abnormalAgg == null) return new DetectionSummaryVo(0L, 0L, 0L, 0L);

        Aggregate aggregate = abnormalAgg.aggregation().getAggregate();

        // 初始化计数
        long low = 0L, medium = 0L, high = 0L;

        if (aggregate.isLterms()) {
            LongTermsAggregate lterms = aggregate.lterms();
            for (LongTermsBucket bucket : lterms.buckets().array()) {
                long key = bucket.key(); // abnormal_index
                long count = bucket.docCount();
                switch ((int) key) {
                    case 1 -> low = count;
                    case 2 -> medium = count;
                    case 3 -> high = count;
                    default -> {
                        // 忽略 0
                    }
                }
            }
        }

        long total = low + medium + high;
        return new DetectionSummaryVo(low, medium, high, total);
    }
}

