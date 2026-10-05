import mongoose from 'mongoose';
import type { Agent, AgentConfig } from '../types';

const AgentConfigSchema = new mongoose.Schema({
  temperature: Number,
  maxTokens: Number,
  systemPrompt: String,
});

const AgentSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    model: { type: String, required: true },
    provider: { type: String, enum: ['openai', 'anthropic', 'langchain'], required: true },
    config: { type: AgentConfigSchema, default: {} },
  },
  { timestamps: true }
);

const AgentModel = mongoose.model<Agent & mongoose.Document>('Agent', AgentSchema);

export async function connectMongo(uri: string): Promise<void> {
  await mongoose.connect(uri);
}

export async function createAgent(data: {
  name: string;
  model: string;
  provider: Agent['provider'];
  config?: AgentConfig;
}): Promise<Agent> {
  const doc = await AgentModel.create(data);
  const obj = doc.toObject() as unknown as Record<string, unknown>;
  return {
    ...obj,
    id: String(obj._id),
    createdAt: obj.createdAt as Date,
    updatedAt: obj.updatedAt as Date,
  } as Agent;
}

export async function getAgentById(id: string): Promise<Agent | null> {
  const doc = await AgentModel.findById(id);
  if (!doc) return null;
  const obj = doc.toObject() as unknown as Record<string, unknown>;
  return { ...obj, id: String(obj._id) } as Agent;
}

export async function updateAgent(
  id: string,
  updates: Partial<Pick<Agent, 'name' | 'model' | 'config'>>
): Promise<Agent | null> {
  const doc = await AgentModel.findByIdAndUpdate(id, updates, { new: true });
  if (!doc) return null;
  const obj = doc.toObject() as unknown as Record<string, unknown>;
  return { ...obj, id: String(obj._id) } as Agent;
}

export async function deleteAgent(id: string): Promise<boolean> {
  const result = await AgentModel.findByIdAndDelete(id);
  return !!result;
}
