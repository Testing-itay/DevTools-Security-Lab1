


using DevToolsLab.Api.Handlers;
using DevToolsLab.Api.Models;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace DevToolsLab.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AgentsController : ControllerBase
{
    private readonly IMediator _mediator;

    public AgentsController(IMediator mediator) => _mediator = mediator;

    [HttpGet]
    public async Task<ActionResult<IReadOnlyList<Agent>>> GetAll(CancellationToken ct)
        => Ok(await _mediator.Send(new GetAgentsQuery(), ct));

    [HttpGet("{id}")]
    public async Task<ActionResult<Agent>> GetById(string id, CancellationToken ct)
    {
        var agent = await _mediator.Send(new GetAgentByIdQuery(id), ct);
        return agent is null ? NotFound() : Ok(agent);
    }

    [HttpPost]
    public async Task<ActionResult<Agent>> Create([FromBody] Agent agent, CancellationToken ct)
    {
        var created = await _mediator.Send(new CreateAgentCommand(agent), ct);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(string id, [FromBody] Agent agent, CancellationToken ct)
    {
        agent.Id = id;
        return await _mediator.Send(new UpdateAgentCommand(agent), ct) ? NoContent() : NotFound();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(string id, CancellationToken ct)
        => await _mediator.Send(new DeleteAgentCommand(id), ct) ? NoContent() : NotFound();
}
