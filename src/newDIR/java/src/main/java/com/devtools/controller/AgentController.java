package com.devtools.controller;

import com.devtools.model.Agent;
import com.devtools.repository.AgentRepository;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@RestController
@RequestMapping("/api/agents")
public class AgentController {

    private final AgentRepository agentRepository;

    public AgentController(AgentRepository agentRepository) {
        this.agentRepository = agentRepository;
    }

    @GetMapping
    public List<Agent> getAll() {
        return agentRepository.findAll();
    }

    @GetMapping("/{id}")
    public Agent getById(@PathVariable String id) {
        return agentRepository.findById(id).orElseThrow();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Agent create(@RequestBody Agent agent) {
        return agentRepository.save(agent);
    }

    @PutMapping("/{id}")
    public Agent update(@PathVariable String id, @RequestBody Agent agent) {
        agent.setId(id);
        return agentRepository.save(agent);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable String id) {
        agentRepository.deleteById(id);
    }
}
