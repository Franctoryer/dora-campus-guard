package com.franctoryer.dora.vo.post;

import com.franctoryer.dora.es.entity.PostEsEntity;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PostListVo implements Serializable {
    /**
     * 帖子信息
     */
    private PostEsEntity post;

    /**
     * 用户信息
     */
    private PostUserVo user;
}
