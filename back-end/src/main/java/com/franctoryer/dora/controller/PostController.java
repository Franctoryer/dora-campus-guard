package com.franctoryer.dora.controller;

import com.franctoryer.dora.dto.post.PostContentSearchDto;
import com.franctoryer.dora.es.entity.PostEsEntity;
import com.franctoryer.dora.service.PostService;
import com.franctoryer.dora.vo.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/rest/posts")
public class PostController {
    private final PostService postService;

    /**
     * 根据关键词分页查询帖子
     * @param postContentSearchDto 查询参数
     * @return
     */
    @GetMapping("/search")
    public Result<Page<PostEsEntity>> searchByContent(@Validated PostContentSearchDto postContentSearchDto) {
        return Result.success(
                postService.searchByContent(postContentSearchDto)
        );
    }
}
