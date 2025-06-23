package com.franctoryer.dora.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 用户数据表
 */
@TableName(value = "users", schema = "public")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class User {

    /**
     * 用户 ID
     */
    @TableId(type = IdType.AUTO)
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

    /**
     * 抓取时间
     */
    private LocalDateTime crawledAt;

    /**
     * 用户指纹（SHA-256）
     */
    private String fingerprint;

    /**
     * item 类型（post/user）
     */
    private String itemType;
}