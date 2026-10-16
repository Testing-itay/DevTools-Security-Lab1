
using DevToolsLab.Api.Models;
using MediatR;

namespace DevToolsLab.Api.Handlers;

public record GetAgentsQuery : IRequest<IReadOnlyList<Agent>>;

public class GetAgentsHandler : IRequestHandler<GetAgentsQuery, IReadOnlyList<Agent>>
{
    private readonly Data.MongoRepository _repository;

    public GetAgentsHandler(Data.MongoRepository repository) => _repository = repository;

    public async Task<IReadOnlyList<Agent>> Handle(GetAgentsQuery request, CancellationToken cancellationToken)
        => await _repository.GetAllAsync(cancellationToken);
}
