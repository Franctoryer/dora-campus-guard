package com.franctoryer.dora.vo.detection;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class DetectionPostListVo implements Serializable {
    /**
     * 帖子 ID
     */
    private Long id;

    /**
     * 帖子正文
     */
    private String content;

    /**
     * 是否匿名
     */
    private Boolean isAnonymous;

    /**
     * 是否精选
     */
    private Boolean isDistinguished;

    /**
     * 图片 URL（逗号分隔）
     */
    private String pictureUrls;

    /**
     * 是否有风险
     */
    private Boolean risky;

    /**
     * 话题 ID
     */
    private Long topicId;

    /**
     * 评论数
     */
    private Integer commentSum;

    /**
     * 点赞数
     */
    private Integer likeSum;

    /**
     * 热度
     */
    private Integer hot;

    /**
     * 举报数
     */
    private Integer tipSum;

    /**
     * 转发数
     */
    private Integer forwardSum;

    /**
     * 蹲数
     */
    private Integer dunNum;

    /**
     * 是否收费
     */
    private Boolean isFee;

    /**
     * 来源
     */
    private Integer origin;

    /**
     * 广告等级
     */
    private Integer adLevel;

    /**
     * 发布时间
     */
    private LocalDateTime publishedAt;

    /**
     * 是否曾经置顶
     */
    private Boolean isEverTop;

    /**
     * 曾经置顶结束时间
     */
    private LocalDateTime everTopEndTime;

    /**
     * 情感标签
     */
    private Integer sentimentLabel;

    /**
     * 情感预测的置信度
     */
    private Float sentimentConfidence;

    /**
     * 异常指数（0 表示正常、1 表示低级、2 表示中级、3 表示高级）
     */
    private Integer abnormalIndex;

    /**
     * 发帖者 ID
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
}
