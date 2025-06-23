package com.franctoryer.dora.service.impl;

import com.franctoryer.dora.dto.post.PostContentSearchDto;
import com.franctoryer.dora.es.entity.PostEsEntity;
import com.franctoryer.dora.es.repository.PostRepository;
import com.franctoryer.dora.service.PostService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class PostServiceImpl implements PostService {
    private final PostRepository postRepository;

    /**
     * 根据关键词分页查询
     * @param postContentSearchDto 分页参数
     * @return 一页帖子
     */
    @Override
    public Page<PostEsEntity> searchByContent(PostContentSearchDto postContentSearchDto) {
        // 关键词
        String keyword = postContentSearchDto.getKeyword();
        // 页码
        Integer page = postContentSearchDto.getPage();
        // 每页数量
        Integer size = postContentSearchDto.getSize();
        Pageable pageable = PageRequest.of(page, size);

        return postRepository.findByContentContaining(keyword, 16, pageable);
    }
}
