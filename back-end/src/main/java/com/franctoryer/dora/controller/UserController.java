package com.franctoryer.dora.controller;

import com.franctoryer.dora.entity.User;
import com.franctoryer.dora.service.UserService;
import com.franctoryer.dora.vo.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/rest/user")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    /**
     * 根据 uid 查询用户详情
     * @param uid 用户 ID
     * @return 用户详情
     */
    @GetMapping("/{uid}/detail")
    public Result<User> getDetailByUid(@PathVariable Long uid) {
        User userDetail = userService.getDetailByUid(uid);
        return Result.success(userDetail);
    }
}
