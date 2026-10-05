package messaging

import (
	"context"
	"time"

	"github.com/segmentio/kafka-go"
)

// Producer wraps a Kafka producer.
type Producer struct {
	writer *kafka.Writer
}

// NewProducer creates a new Kafka producer.
func NewProducer(brokers []string, topic string) *Producer {
	return &Producer{
		writer: &kafka.Writer{
			Addr:     kafka.TCP(brokers...),
			Topic:    topic,
			Balancer: &kafka.LeastBytes{},
		},
	}
}

// Produce sends a message to Kafka.
func (p *Producer) Produce(ctx context.Context, key, value []byte) error {
	return p.writer.WriteMessages(ctx, kafka.Message{
		Key:   key,
		Value: value,
		Time:  time.Now(),
	})
}

// Close closes the producer.
func (p *Producer) Close() error {
	return p.writer.Close()
}

// Consumer wraps a Kafka consumer.
type Consumer struct {
	reader *kafka.Reader
}

// NewConsumer creates a new Kafka consumer.
func NewConsumer(brokers []string, topic, groupID string) *Consumer {
	return &Consumer{
		reader: kafka.NewReader(kafka.ReaderConfig{
			Brokers: brokers,
			Topic:   topic,
			GroupID: groupID,
		}),
	}
}

// Consume reads a message from Kafka.
func (c *Consumer) Consume(ctx context.Context) (kafka.Message, error) {
	return c.reader.ReadMessage(ctx)
}

// Close closes the consumer.
func (c *Consumer) Close() error {
	return c.reader.Close()
}
