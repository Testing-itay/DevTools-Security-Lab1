
using StackExchange.Redis;

namespace DevToolsLab.Api.Data;

public class RedisCache
{
    private readonly IDatabase _db;

    public RedisCache(IConnectionMultiplexer connection)
    {
        _db = connection.GetDatabase();
    }

    public async Task<string?> GetAsync(string key, CancellationToken cancellationToken = default)
    {
        return await _db.StringGetAsync(key);
    }

    public async Task SetAsync(string key, string value, TimeSpan? expiry = null, CancellationToken cancellationToken = default)
    {
        await _db.StringSetAsync(key, value, expiry);
    }

    public async Task<bool> DeleteAsync(string key, CancellationToken cancellationToken = default)
    {
        return await _db.KeyDeleteAsync(key);
    }
}
