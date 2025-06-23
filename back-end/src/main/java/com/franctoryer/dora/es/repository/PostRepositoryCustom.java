package com.franctoryer.dora.es.repository;

import com.franctoryer.dora.es.entity.PostEsEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface PostRepositoryCustom {
    /**
     * @param keyword 关键词
     * @param pageable 分页参数
     * @return 帖子列表
     */
    Page<PostEsEntity> findByContentContaining(String keyword, Integer schoolId, Pageable pageable);
}
