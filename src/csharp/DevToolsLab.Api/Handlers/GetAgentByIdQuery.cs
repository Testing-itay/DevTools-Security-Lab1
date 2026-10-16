

using DevToolsLab.Api.Models;
using MediatR;

namespace DevToolsLab.Api.Handlers;

public record GetAgentByIdQuery(string Id) : IRequest<Agent?>;

public class GetAgentByIdHandler : IRequestHandler<GetAgentByIdQuery, Agent?>
{
    private readonly Data.MongoRepository _repository;

    public GetAgentByIdHandler(Data.MongoRepository repository) => _repository = repository;

    public async Task<Agent?> Handle(GetAgentByIdQuery request, CancellationToken cancellationToken)
        => await _repository.GetByIdAsync(request.Id, cancellationToken);
}
