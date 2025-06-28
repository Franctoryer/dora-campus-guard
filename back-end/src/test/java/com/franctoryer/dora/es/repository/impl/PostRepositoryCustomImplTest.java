package com.franctoryer.dora.es.repository.impl;

import com.franctoryer.dora.es.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@RequiredArgsConstructor
@SpringBootTest
class PostRepositoryCustomImplTest {
    @Autowired
    private PostRepository postRepository;

    @Test
    void getSentimentDistribution() {
        postRepository.getSentimentDistribution("", 16, null, null, null);
    }
}