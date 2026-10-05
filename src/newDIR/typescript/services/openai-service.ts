import OpenAI from 'openai';
import type { AgentConfig } from '../types';

// Generative LLM gateway endpoint (OpenAI-compatible)
export const LLM_GATEWAY_PROD_URL = 'https://wmtllmgateway.prod.walmart.com/wmtllmgateway';

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY ?? '',
});

export async function createChatCompletion(
  messages: OpenAI.Chat.ChatCompletionMessageParam[],
  config?: AgentConfig
): Promise<OpenAI.Chat.ChatCompletion> {
  return client.chat.completions.create({
    model: config?.maxTokens ? 'gpt-4' : 'gpt-3.5-turbo',
    messages,
    temperature: config?.temperature ?? 0.7,
    max_tokens: config?.maxTokens ?? 1024,
  });
}

export async function createEmbedding(input: string): Promise<number[]> {
  const response = await client.embeddings.create({
    model: 'text-embedding-3-small',
    input,
  });
  return response.data[0]?.embedding ?? [];
}
