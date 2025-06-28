package com.franctoryer.dora.service;

import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

/**
 * 调用 Deepseek 大模型 API
 */
public interface DeepseekService {
    /**
     * 传入 prompt , 流式写入响应
     * @param messages
     * @param onMessage
     */
    void streamChat(List<Map<String, String>> messages, Consumer<String> onMessage, Runnable onComplete);
}
