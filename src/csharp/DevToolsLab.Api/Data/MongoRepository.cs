
using DevToolsLab.Api.Models;
using MongoDB.Driver;

namespace DevToolsLab.Api.Data;

public class MongoRepository
{
    private readonly IMongoCollection<Agent> _collection;

    public MongoRepository(IMongoDatabase database)
    {
        _collection = database.GetCollection<Agent>("agents");
    }

    public async Task<Agent?> GetByIdAsync(string id, CancellationToken cancellationToken = default)
    {
        var filter = Builders<Agent>.Filter.Eq(a => a.Id, id);
        return await _collection.Find(filter).FirstOrDefaultAsync(cancellationToken);
    }

    public async Task<IReadOnlyList<Agent>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        return await _collection.Find(_ => true).ToListAsync(cancellationToken);
    }

    public async Task<Agent> CreateAsync(Agent agent, CancellationToken cancellationToken = default)
    {
        agent.Id = Guid.NewGuid().ToString("N");
        await _collection.InsertOneAsync(agent, cancellationToken: cancellationToken);
        return agent;
    }

    public async Task<bool> UpdateAsync(Agent agent, CancellationToken cancellationToken = default)
    {
        var filter = Builders<Agent>.Filter.Eq(a => a.Id, agent.Id);
        var result = await _collection.ReplaceOneAsync(filter, agent, cancellationToken: cancellationToken);
        return result.ModifiedCount > 0;
    }

    public async Task<bool> DeleteAsync(string id, CancellationToken cancellationToken = default)
    {
        var filter = Builders<Agent>.Filter.Eq(a => a.Id, id);
        var result = await _collection.DeleteOneAsync(filter, cancellationToken);
        return result.DeletedCount > 0;
    }
}
