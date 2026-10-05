package com.devtools.repository;

import com.devtools.model.Agent;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface AgentRepository extends MongoRepository<Agent, String> {

    List<Agent> findByStatus(String status);
}
