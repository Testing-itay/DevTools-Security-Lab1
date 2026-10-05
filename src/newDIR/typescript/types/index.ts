export interface Agent {
  id: string;
  name: string;
  model: string;
  provider: 'openai' | 'anthropic' | 'langchain';
  config: AgentConfig;
  createdAt: Date;
  updatedAt: Date;
}

export interface AgentConfig {
  temperature?: number;
  maxTokens?: number;
  systemPrompt?: string;
}

export interface AnalysisResult {
  id: string;
  agentId: string;
  input: string;
  output: string;
  tokensUsed?: number;
  latencyMs?: number;
  timestamp: Date;
}

export interface Config {
  port: number;
  mongoUri: string;
  redisUrl: string;
  openaiApiKey?: string;
  anthropicApiKey?: string;
  stripeSecretKey?: string;
  sentryDsn?: string;
}

export interface JwtPayload {
  sub: string;
  email?: string;
  iat?: number;
  exp?: number;
}
