package com.franctoryer.dora.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;


@TableName("users")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class User {

    @TableId
    private Long uid; // 用户 ID

    private String avatarUrl; // 用户头像 URL

    private Integer gender; // 性别：0-男，1-女，2-未知

    private Integer level; // 等级

    private String nickname; // 昵称

    private Boolean isAdmin; // 是否是管理员

    private Double doraValue; // 哆啦值

    private Double doraCoin; // 哆啦币

    private String likes; // 被哪些人关注（建议用 JSON 字符串或逗号分隔）

    private Boolean hidePermission; // 是否隐藏主页

    private Boolean isAnonymous; // 是否匿名

    private Date createdAt; // 创建时间

    private Date updatedAt; // 更新时间
}