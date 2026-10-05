import { NodeSDK } from '@opentelemetry/sdk-node';
import { trace } from '@opentelemetry/api';

const sdk = new NodeSDK({
  serviceName: 'devtools-engine-api',
});

export function initTelemetry(): void {
  sdk.start();
}

export function getTracer(name = 'devtools-engine') {
  return trace.getTracer(name, '1.0.0');
}

export function createSpan(name: string, fn: () => Promise<unknown>): Promise<unknown> {
  const tracer = getTracer();
  return tracer.startActiveSpan(name, async (span) => {
    try {
      const result = await fn();
      span.setStatus({ code: 1 });
      return result;
    } catch (err) {
      span.setStatus({ code: 2, message: String(err) });
      throw err;
    } finally {
      span.end();
    }
  });
}
