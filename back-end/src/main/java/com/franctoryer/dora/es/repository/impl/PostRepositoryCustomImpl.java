package com.franctoryer.dora.es.repository.impl;

import com.franctoryer.dora.es.entity.PostEsEntity;
import com.franctoryer.dora.es.repository.PostRepositoryCustom;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.elasticsearch.client.elc.NativeQuery;
import org.springframework.data.elasticsearch.client.elc.NativeQueryBuilder;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.data.elasticsearch.core.query.HighlightQuery;
import org.springframework.data.elasticsearch.core.query.Query;
import org.springframework.data.elasticsearch.core.query.highlight.Highlight;
import org.springframework.data.elasticsearch.core.query.highlight.HighlightField;
import org.springframework.data.elasticsearch.core.query.highlight.HighlightParameters;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import java.util.List;

@Component
@RequiredArgsConstructor
public class PostRepositoryCustomImpl implements PostRepositoryCustom {

    private final ElasticsearchOperations elasticsearchOperations;

    @Override
    public Page<PostEsEntity> findByContentContaining(String keyword, Integer schoolId, Pageable pageable) {
        // 高亮配置
        HighlightField highlightField = new HighlightField("content");
        HighlightParameters highlightParameters = HighlightParameters.builder()
                .withPreTags("<em>")
                .withPostTags("</em>")
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

            return b;
        }));

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
}
