package com.devtools.messaging;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class KafkaConsumer {

    @KafkaListener(topics = "devtools-events", groupId = "devtools-group")
    public void consume(String message) {
        // Process incoming Kafka messages
    }
}
