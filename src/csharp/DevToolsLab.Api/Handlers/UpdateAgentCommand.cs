

using MediatR;

namespace DevToolsLab.Api.Handlers;

public record UpdateAgentCommand(Models.Agent Agent) : IRequest<bool>;

public class UpdateAgentHandler : IRequestHandler<UpdateAgentCommand, bool>
{
    private readonly Data.MongoRepository _repository;

    public UpdateAgentHandler(Data.MongoRepository repository) => _repository = repository;

    public async Task<bool> Handle(UpdateAgentCommand request, CancellationToken cancellationToken)
        => await _repository.UpdateAsync(request.Agent, cancellationToken);
}
