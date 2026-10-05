import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL ?? 'redis://localhost:6379');

export async function getCached<T>(key: string): Promise<T | null> {
  const value = await redis.get(key);
  return value ? (JSON.parse(value) as T) : null;
}

export async function setCache(key: string, value: unknown, ttlSeconds = 3600): Promise<void> {
  await redis.setex(key, ttlSeconds, JSON.stringify(value));
}

export async function deleteCache(key: string): Promise<void> {
  await redis.del(key);
}

export function getRedisClient(): Redis {
  return redis;
}
