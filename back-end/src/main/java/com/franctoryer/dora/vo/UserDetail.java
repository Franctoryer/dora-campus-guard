package com.franctoryer.dora.vo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserDetail {
    // 用户 ID
    private Long id;

    // 用户昵称
    private String nickname;

    // 用户年龄
    private Integer age;

    // 用户创建时间
    private Integer createdAt;
}
