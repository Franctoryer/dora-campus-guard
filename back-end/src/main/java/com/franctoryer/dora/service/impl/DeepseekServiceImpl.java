package com.franctoryer.dora.service.impl;

import com.franctoryer.dora.service.DeepseekService;
import lombok.extern.slf4j.Slf4j;
import org.apache.http.HttpHeaders;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.core.io.buffer.DataBufferUtils;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

@Slf4j
@Service
public class DeepseekServiceImpl implements DeepseekService {
    private final WebClient webClient;

    public DeepseekServiceImpl(@Value("${deepseek.api.key}") String apiKey) {
        this.webClient = WebClient.builder()
                .baseUrl("https://api.deepseek.com")
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }
    /**
     * 传入 prompt , 流式写入响应
     *
     * @param messages
     * @param onMessage
     */
    @Override
    public void streamChat(List<Map<String, String>> messages, Consumer<String> onMessage, Runnable onComplete) {
        Map<String, Object> body = Map.of(
                "model", "deepseek-chat",
                "messages", messages,
                "stream", true
        );
        log.info("StreamChat 启动了 ....");

        webClient.post()
                .uri("/chat/completions")
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(body)
                .retrieve()
                .bodyToFlux(DataBuffer.class)
                .flatMap(dataBuffer -> {
                    byte[] bytes = new byte[dataBuffer.readableByteCount()];
                    dataBuffer.read(bytes);
                    DataBufferUtils.release(dataBuffer); // 释放内存
                    String chunk = new String(bytes); // 这才是实际的内容
                    log.info("Raw chunk content: {}", chunk);
                    return Flux.fromArray(chunk.split("\n")); // 按行分割
                })
                .filter(line -> line.startsWith("data: "))
                .map(line -> line.substring(6).trim())
                .takeWhile(line -> !line.equals("[DONE]"))
                .doOnNext(data -> {
                    log.info("接收到 Chunk" + data);
                    onMessage.accept(data);
                })
                .doOnComplete(() -> {
                    log.info("DeepSeek 输出结束");
                    onComplete.run();
                })
                .doOnError(Throwable::printStackTrace)
                .subscribe();
    }
}
