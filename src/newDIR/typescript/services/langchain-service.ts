import { ChatOpenAI } from '@langchain/openai';
import { StringOutputParser } from '@langchain/core/output_parsers';
import type { AgentConfig } from '../types';

export async function runChain(input: string, config?: AgentConfig): Promise<string> {
  const llm = new ChatOpenAI({
    modelName: 'gpt-4',
    temperature: config?.temperature ?? 0.7,
    maxTokens: config?.maxTokens ?? 1024,
  });
  const outputParser = new StringOutputParser();
  const response = await llm.invoke(input);
  return outputParser.invoke(response);
}
