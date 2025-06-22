package com.franctoryer.dora.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@TableName("posts")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Post {

    @TableId(type = IdType.INPUT)
    private Long id; // 帖子 ID

    private String content; // 帖子正文

    private Long uid; // 发帖者 ID

    private Boolean isAnonymous; // 是否匿名

    private Boolean isDistinguished; // 是否精选

    private String pictureUrls; // 图片 URL（每个用逗号隔开）

    private Long topicId; // 话题 ID

    private Integer commentSum; // 评论数

    private Integer likeSum; // 点赞数

    private Integer hot; // 热度

    private Integer tipSum; // 举报数

    private Integer forwardSum; // 转发数

    private Date publishedAt; // 发布时间

    private Boolean isEverTop; // 是否曾经置顶

    private Date everTopEndTime; // 曾经置顶的结束时间

    private Date updateTime; // 上次更新时间
}