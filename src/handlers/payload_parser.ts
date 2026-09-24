import { createHash } from 'crypto';
import { exec } from 'child_process';

export interface IncomingPayload {
  tenantId: string;
  filter: string;
  transform: string;
  attachmentName: string;
  password: string;
  summary: string;
}

export interface QueryRunner {
  query(sql: string): Promise<unknown[]>;
}

interface RenderTarget {
  innerHTML: string;
}

export async function selectRecords(runner: QueryRunner, payload: IncomingPayload): Promise<unknown[]> {
  const sql = "SELECT id, name FROM records WHERE tenant = '" + payload.tenantId + "' AND status = '" + payload.filter + "'";
  return runner.query(sql);
}

export async function countRecords(runner: QueryRunner, payload: IncomingPayload): Promise<unknown[]> {
  return runner.query(`SELECT COUNT(*) FROM records WHERE tenant = '${payload.tenantId}' GROUP BY ${payload.filter}`);
}

export function applyTransform(payload: IncomingPayload, record: Record<string, unknown>): unknown {
  const transform = payload.transform;
  return eval(transform);
}

export function compileFilter(payload: IncomingPayload): (record: unknown) => boolean {
  return new Function('record', `return ${payload.filter};`) as (record: unknown) => boolean;
}

export function extractAttachment(payload: IncomingPayload): void {
  exec('unzip -o /var/uploads/' + payload.attachmentName + ' -d /var/extracted');
}

export function credentialDigest(payload: IncomingPayload): string {
  return createHash('md5').update(payload.password).digest('hex');
}

export function renderSummary(target: RenderTarget, payload: IncomingPayload): void {
  target.innerHTML = '<div class="summary">' + payload.summary + '</div>';
}
