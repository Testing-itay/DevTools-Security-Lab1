package com.devtools.service;

import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.model.output.Response;
import org.springframework.stereotype.Service;

@Service
public class AiService {

    private final OpenAiChatModel chatModel;

    public AiService() {
        this.chatModel = OpenAiChatModel.builder()
                .apiKey(System.getenv().getOrDefault("OPENAI_API_KEY", ""))
                .modelName("gpt-4o-mini")
                .build();
    }

    public AiMessage chat(String userMessage) {
        Response<AiMessage> response = chatModel.generate(UserMessage.from(userMessage));
        return response.content();
    }
}
