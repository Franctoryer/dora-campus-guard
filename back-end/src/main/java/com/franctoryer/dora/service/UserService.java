package com.franctoryer.dora.service;

import com.franctoryer.dora.entity.User;
import com.franctoryer.dora.vo.post.PostUserVo;

import java.util.List;

public interface UserService {
    /**
     * 获取某个用户的详情
     * @param uid 用户 ID
     * @return 用户详情
     */
    User getDetailByUid(Long uid);

    /**
     * 根据用户 ID 集合批量查询用户详情（解决 N + 1）
     * @param uids 用户 ID 列表
     * @return 用户详情列表
     */
    List<PostUserVo> getDetailByUids(List<Long> uids);
}
