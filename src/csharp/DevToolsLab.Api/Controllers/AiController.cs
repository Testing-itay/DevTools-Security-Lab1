


using Azure;
using Azure.AI.OpenAI;
using Microsoft.AspNetCore.Mvc;

namespace DevToolsLab.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AiController : ControllerBase
{
    private readonly OpenAIClient _client;
    private readonly string _deploymentName;

    public AiController(IConfiguration config)
    {
        var endpoint = config["AzureOpenAI:Endpoint"] ?? "https://example.openai.azure.com/";
        var apiKey = config["AzureOpenAI:ApiKey"] ?? "";
        _deploymentName = config["AzureOpenAI:DeploymentName"] ?? "gpt-4";
        _client = new OpenAIClient(new Uri(endpoint), new AzureKeyCredential(apiKey));
    }

    [HttpPost("chat")]
    public async Task<ActionResult<string>> Chat([FromBody] ChatRequest request, CancellationToken ct)
    {
        var options = new ChatCompletionsOptions
        {
            DeploymentName = _deploymentName,
            Messages = { new ChatRequestUserMessage(request.Message) }
        };
        var response = await _client.GetChatCompletionsAsync(options, ct);
        var content = response.Value.Choices[0].Message.Content ?? "";
        return Ok(new { content });
    }

    public record ChatRequest(string Message);
}
