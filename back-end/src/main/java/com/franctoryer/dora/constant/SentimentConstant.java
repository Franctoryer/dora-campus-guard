package com.franctoryer.dora.constant;

import java.util.Map;

/**
 * 情感相关常量类
 */
public class SentimentConstant {
    /**
     * 情感字典（标签 -> 标签含义）
     */
    public static Map<Long, String> SENTIMENT_LABEL_MAP = Map.of(
            0L, "悲伤",
            1L, "失望",
            2L, "讨厌",
            3L, "平和",
            4L, "疑惑",
            5L, "开心",
            6L, "期待"
    );
}
