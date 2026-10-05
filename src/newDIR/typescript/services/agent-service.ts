import type { Agent, AgentConfig } from '../types';
import { createAgent, getAgentById, updateAgent, deleteAgent } from '../data/mongo-repository';

export async function createAgentService(
  name: string,
  model: string,
  provider: Agent['provider'],
  config?: AgentConfig
): Promise<Agent> {
  return createAgent({ name, model, provider, config: config ?? {} });
}

export async function getAgentService(id: string): Promise<Agent | null> {
  return getAgentById(id);
}

export async function updateAgentService(
  id: string,
  updates: Partial<Pick<Agent, 'name' | 'model' | 'config'>>
): Promise<Agent | null> {
  return updateAgent(id, updates);
}

export async function deleteAgentService(id: string): Promise<boolean> {
  return deleteAgent(id);
}
