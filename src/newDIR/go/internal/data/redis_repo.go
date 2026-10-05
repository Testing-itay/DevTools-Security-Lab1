package data

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
)

// RedisRepo provides Redis cache operations.
type RedisRepo struct {
	client *redis.Client
}

// NewRedisRepo creates a new RedisRepo.
func NewRedisRepo(client *redis.Client) *RedisRepo {
	return &RedisRepo{client: client}
}

// Set stores a value with TTL.
func (r *RedisRepo) Set(ctx context.Context, key, value string, ttl time.Duration) error {
	return r.client.Set(ctx, key, value, ttl).Err()
}

// Get retrieves a value by key.
func (r *RedisRepo) Get(ctx context.Context, key string) (string, error) {
	return r.client.Get(ctx, key).Result()
}

// Delete removes a key.
func (r *RedisRepo) Delete(ctx context.Context, key string) error {
	return r.client.Del(ctx, key).Err()
}

// Exists checks if a key exists.
func (r *RedisRepo) Exists(ctx context.Context, key string) (bool, error) {
	n, err := r.client.Exists(ctx, key).Result()
	return n > 0, err
}
