import { Kafka, Producer, Consumer } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'devtools-engine',
  brokers: (process.env.KAFKA_BROKERS ?? 'localhost:9092').split(','),
});

let producer: Producer | null = null;
let consumer: Consumer | null = null;

export async function getProducer(): Promise<Producer> {
  if (!producer) {
    producer = kafka.producer();
    await producer.connect();
  }
  return producer;
}

export async function getConsumer(groupId: string): Promise<Consumer> {
  if (!consumer) {
    consumer = kafka.consumer({ groupId });
    await consumer.connect();
  }
  return consumer;
}

export async function produceEvent(topic: string, key: string, value: string): Promise<void> {
  const p = await getProducer();
  await p.send({ topic, messages: [{ key, value }] });
}

export async function subscribeToTopic(
  topic: string,
  handler: (message: { key: string; value: string }) => Promise<void>
): Promise<void> {
  const c = await getConsumer('devtools-engine-group');
  await c.subscribe({ topic, fromBeginning: true });
  await c.run({
    eachMessage: async ({ message }) => {
      await handler({
        key: message.key?.toString() ?? '',
        value: message.value?.toString() ?? '',
      });
    },
  });
}
