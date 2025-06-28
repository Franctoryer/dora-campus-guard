package com.franctoryer.dora.es.entity;


import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

import java.io.Serializable;

/**
 * Elasticsearch 帖子实体类
 */
@Data
@Document(indexName = "posts")
public class PostEsEntity implements Serializable {
    /**
     * 帖子 ID
     */
    @Id
    @Field(type = FieldType.Long)
    private Long id;

    /**
     * 帖子正文
     */
    @Field(type = FieldType.Text, analyzer = "ik_max_word", searchAnalyzer = "ik_max_word", name = "content")
    private String content;

    /**
     * 发帖者 ID
     */
    @Field(type = FieldType.Long, name = "uid")
    private Long uid;

    /**
     * 是否匿名
     */
    @Field(type = FieldType.Boolean, name = "is_anonymous")
    private Boolean isAnonymous;

    /**
     * 是否精选
     */
    @Field(type = FieldType.Boolean, name = "is_distinguished")
    private Boolean isDistinguished;

    /**
     * 是否有风险
     */
    @Field(type = FieldType.Boolean, name = "risky")
    private Boolean risky;

    /**
     * 话题 ID
     */
    @Field(type = FieldType.Long, name = "topic_id")
    private Long topicId;

    /**
     * 评论数
     */
    @Field(type = FieldType.Integer, name = "comment_sum")
    private Integer commentSum;

    /**
     * 点赞数
     */
    @Field(type = FieldType.Integer, name = "like_sum")
    private Integer likeSum;

    /**
     * 热度
     */
    @Field(type = FieldType.Integer, name = "hot")
    private Integer hot;

    /**
     * 举报数
     */
    @Field(type = FieldType.Integer, name = "tip_sum")
    private Integer tipSum;

    /**
     * 转发数
     */
    @Field(type = FieldType.Integer, name = "forward_sum")
    private Integer forwardSum;

    /**
     * 蹲数
     */
    @Field(type = FieldType.Integer, name = "dun_num")
    private Integer dunNum;

    /**
     * 学校 ID
     */
    @Field(type = FieldType.Long, name = "school_id")
    private Long schoolId;

    /**
     * 发布时间
     */
    @Field(type = FieldType.Date, name = "published_at")
    private String publishedAt;

    /**
     * 是否曾经置顶
     */
    @Field(type = FieldType.Boolean, name = "is_ever_top")
    private Boolean isEverTop;

    /**
     * 曾经置顶结束时间
     */
    @Field(type = FieldType.Date, name = "ever_top_end_time")
    private String everTopEndTime;

    /**
     * 情感标签
     */
    @Field(type = FieldType.Integer, name = "sentiment_label")
    private Integer sentimentLabel;

    /**
     * 情感预测置信度
     */
    @Field(type = FieldType.Float, name = "sentiment_confidence")
    private Float sentimentConfidence;

    /**
     * 异常指数
     */
    @Field(type = FieldType.Integer, name = "abnormal_index")
    private Integer abnormalIndex;
}