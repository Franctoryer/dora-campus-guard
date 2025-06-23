package com.franctoryer.dora.service;

import com.franctoryer.dora.dto.post.PostContentSearchDto;
import com.franctoryer.dora.es.entity.PostEsEntity;
import org.springframework.data.domain.Page;


public interface PostService {
    Page<PostEsEntity> searchByContent(PostContentSearchDto postContentSearchDto);
}
