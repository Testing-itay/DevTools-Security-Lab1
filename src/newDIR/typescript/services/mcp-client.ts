import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

let mcpClient: Client | null = null;

export async function getMcpClient(transport?: StdioClientTransport): Promise<Client> {
  if (mcpClient) return mcpClient;
  const clientTransport = transport ?? new StdioClientTransport({
    command: 'npx',
    args: ['-y', '@modelcontextprotocol/server-stdio'],
  });
  mcpClient = new Client({ name: 'devtools-engine', version: '1.0.0' });
  await mcpClient.connect(clientTransport);
  return mcpClient;
}

export async function listMcpTools(): Promise<unknown[]> {
  const client = await getMcpClient();
  const result = await client.listTools();
  return result.tools ?? [];
}
