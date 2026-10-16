

using DevToolsLab.Api.Models;
using MediatR;

namespace DevToolsLab.Api.Handlers;

public record CreateAgentCommand(Agent Agent) : IRequest<Agent>;

public class CreateAgentHandler : IRequestHandler<CreateAgentCommand, Agent>
{
    private readonly Data.MongoRepository _repository;

    public CreateAgentHandler(Data.MongoRepository repository) => _repository = repository;

    public async Task<Agent> Handle(CreateAgentCommand request, CancellationToken cancellationToken)
        => await _repository.CreateAsync(request.Agent, cancellationToken);
}
