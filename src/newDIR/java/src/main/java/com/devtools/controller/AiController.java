package com.devtools.controller;

import com.devtools.service.AiService;
import dev.langchain4j.data.message.AiMessage;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/ai")
public class AiController {

    private final AiService aiService;

    public AiController(AiService aiService) {
        this.aiService = aiService;
    }

    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        AiMessage response = aiService.chat(request.message());
        return new ChatResponse(response.text());
    }

    public record ChatRequest(String message) {}
    public record ChatResponse(String response) {}
}
