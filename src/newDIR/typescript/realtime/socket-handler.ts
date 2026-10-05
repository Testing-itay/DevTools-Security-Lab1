import { Server as SocketServer } from 'socket.io';
import type { Server as HttpServer } from 'http';

let io: SocketServer | null = null;

export function initSocketHandler(httpServer: HttpServer): SocketServer {
  io = new SocketServer(httpServer, {
    cors: { origin: process.env.CORS_ORIGIN ?? '*' },
  });

  io.on('connection', (socket) => {
    socket.on('join:agent', (agentId: string) => {
      socket.join(`agent:${agentId}`);
    });

    socket.on('analysis:request', (payload: { agentId: string; input: string }) => {
      socket.to(`agent:${payload.agentId}`).emit('analysis:request', payload);
    });
  });

  return io;
}

export function getSocketServer(): SocketServer | null {
  return io;
}

export function emitToAgent(agentId: string, event: string, data: unknown): void {
  io?.to(`agent:${agentId}`).emit(event, data);
}
