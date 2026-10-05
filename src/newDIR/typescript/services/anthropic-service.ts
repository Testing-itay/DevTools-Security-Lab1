import Anthropic from '@anthropic-ai/sdk';
import type { AgentConfig } from '../types';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY ?? '',
});

export async function createMessage(
  messages: Anthropic.MessageParam[],
  config?: AgentConfig
): Promise<Anthropic.Message> {
  return client.messages.create({
    model: 'claude-3-sonnet-20240229',
    max_tokens: config?.maxTokens ?? 1024,
    system: config?.systemPrompt,
    messages,
  });
}
