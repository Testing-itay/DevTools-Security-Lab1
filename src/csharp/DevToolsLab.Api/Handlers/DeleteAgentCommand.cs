

using MediatR;

namespace DevToolsLab.Api.Handlers;

public record DeleteAgentCommand(string Id) : IRequest<bool>;

public class DeleteAgentHandler : IRequestHandler<DeleteAgentCommand, bool>
{
    private readonly Data.MongoRepository _repository;

    public DeleteAgentHandler(Data.MongoRepository repository) => _repository = repository;

    public async Task<bool> Handle(DeleteAgentCommand request, CancellationToken cancellationToken)
        => await _repository.DeleteAsync(request.Id, cancellationToken);
}
