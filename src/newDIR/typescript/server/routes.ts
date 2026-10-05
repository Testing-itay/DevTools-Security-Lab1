import type { Express } from 'express';
import { jwtAuth } from '../auth/passport-config';
import {
  createAgentService,
  getAgentService,
  updateAgentService,
  deleteAgentService,
} from '../services/agent-service';
import { createChatCompletion } from '../services/openai-service';
import { createMessage } from '../services/anthropic-service';
import { runChain } from '../services/langchain-service';
import { createPaymentIntent } from '../payments/stripe-service';

export function registerRoutes(app: Express): void {
  app.get('/health', (_req, res) => res.json({ status: 'ok' }));

  app.post('/agents', jwtAuth, async (req, res) => {
    const { name, model, provider, config } = req.body;
    const agent = await createAgentService(name, model, provider, config);
    res.status(201).json(agent);
  });

  app.get('/agents/:id', jwtAuth, async (req, res) => {
    const agent = await getAgentService(req.params.id);
    if (!agent) return res.status(404).json({ error: 'Not found' });
    res.json(agent);
  });

  app.patch('/agents/:id', jwtAuth, async (req, res) => {
    const agent = await updateAgentService(req.params.id, req.body);
    if (!agent) return res.status(404).json({ error: 'Not found' });
    res.json(agent);
  });

  app.delete('/agents/:id', jwtAuth, async (req, res) => {
    const ok = await deleteAgentService(req.params.id);
    res.status(ok ? 204 : 404).send();
  });

  app.post('/chat/openai', jwtAuth, async (req, res) => {
    const { messages, config } = req.body;
    const completion = await createChatCompletion(messages, config);
    res.json(completion);
  });

  app.post('/chat/anthropic', jwtAuth, async (req, res) => {
    const { messages, config } = req.body;
    const message = await createMessage(messages, config);
    res.json(message);
  });

  app.post('/chat/langchain', jwtAuth, async (req, res) => {
    const { input, config } = req.body;
    const output = await runChain(input, config);
    res.json({ output });
  });

  app.post('/payments/intent', jwtAuth, async (req, res) => {
    const { amount, currency, metadata } = req.body;
    const intent = await createPaymentIntent(amount, currency, metadata);
    res.json({ clientSecret: intent.client_secret });
  });
}
