package com.franctoryer.dora.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.franctoryer.dora.entity.User;
import com.franctoryer.dora.mapper.UserMapper;
import com.franctoryer.dora.service.UserService;
import com.franctoryer.dora.vo.post.PostUserVo;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserMapper userMapper;

    /**
     * @param uid 用户 ID
     * @return 用户详情
     */
    @Override
    public User getDetailByUid(Long uid) {
        return userMapper.selectById(uid);
    }

    /**
     * 根据用户 ID 集合批量查询用户详情（解决 N + 1）
     *
     * @param uids 用户 ID 列表
     * @return 用户详情列表
     */
    @Override
    public List<PostUserVo> getDetailByUids(List<Long> uids) {
        LambdaQueryWrapper<User> queryWrapper = new LambdaQueryWrapper<User>()
                .in(User::getUid, uids)
                .select(
                        User::getUid,
                        User::getAvatarUrl,
                        User::getGender,
                        User::getLevel,
                        User::getNickname,
                        User::getIsAdmin,
                        User::getSchoolId,
                        User::getDoraCoin,
                        User::getHidePermission,
                        User::getIsAnonymous,
                        User::getEatTip
                );
        List<User> userList = userMapper.selectList(queryWrapper);
        // 返回结果
        List<PostUserVo> userVos = new ArrayList<>();
        userList.forEach(user -> {
            PostUserVo userVo = new PostUserVo();
            BeanUtils.copyProperties(user, userVo);
            userVos.add(userVo);
        });

        return userVos;
    }

}
