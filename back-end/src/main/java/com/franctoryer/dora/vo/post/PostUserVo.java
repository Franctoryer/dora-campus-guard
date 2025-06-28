package com.franctoryer.dora.vo.post;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PostUserVo implements Serializable {
    /**
     * 用户 Id
     */
    private Long uid;

    /**
     * 头像 URL
     */
    private String avatarUrl;

    /**
     * 性别（0 女，1 男，2 保密）
     */
    private Integer gender;

    /**
     * 等级
     */
    private Integer level;

    /**
     * 昵称
     */
    private String nickname;

    /**
     * 是否管理员
     */
    private Boolean isAdmin;

    /**
     * 学校 ID
     */
    private Long schoolId;

    /**
     * 哆啦币
     */
    private Float doraCoin;

    /**
     * 是否隐藏主页
     */
    private Boolean hidePermission;

    /**
     * 是否匿名
     */
    private Boolean isAnonymous;

    /**
     * 是否被举报
     */
    private Boolean eatTip;
}
