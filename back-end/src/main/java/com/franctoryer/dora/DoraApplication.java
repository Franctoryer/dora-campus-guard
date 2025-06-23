package com.franctoryer.dora;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.elasticsearch.repository.config.EnableElasticsearchRepositories;
import org.springframework.data.repository.query.QueryLookupStrategy;

@SpringBootApplication
@MapperScan("com.franctoryer.dora.mapper")
@EnableElasticsearchRepositories(
		basePackages = "com.franctoryer.dora.es.repository",
		queryLookupStrategy = QueryLookupStrategy.Key.CREATE_IF_NOT_FOUND
)
public class DoraApplication {

	public static void main(String[] args) {
		SpringApplication.run(DoraApplication.class, args);
	}

}
