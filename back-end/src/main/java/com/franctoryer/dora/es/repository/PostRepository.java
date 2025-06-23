package com.franctoryer.dora.es.repository;

import com.franctoryer.dora.es.entity.PostEsEntity;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PostRepository extends ElasticsearchRepository<PostEsEntity, Long>, PostRepositoryCustom {
}
