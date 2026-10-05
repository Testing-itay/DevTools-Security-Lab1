package com.devtools.repository;

import com.devtools.model.SearchDocument;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

import java.util.List;

public interface SearchRepository extends ElasticsearchRepository<SearchDocument, String> {

    List<SearchDocument> findByContentContaining(String content);
}
