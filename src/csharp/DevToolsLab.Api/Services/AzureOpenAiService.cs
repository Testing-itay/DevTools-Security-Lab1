

using Azure;
using Azure.AI.OpenAI;
using DevToolsLab.Core.Interfaces;

namespace DevToolsLab.Api.Services;

public class AzureOpenAiService : IAiService
{
    private readonly OpenAIClient _client;
    private readonly string _deploymentName;

    public AzureOpenAiService(string endpoint, string apiKey, string deploymentName)
    {
        _client = new OpenAIClient(new Uri(endpoint), new AzureKeyCredential(apiKey));
        _deploymentName = deploymentName;
    }

    public async Task<string> GetCompletionAsync(string prompt, CancellationToken cancellationToken = default)
    {
        return await GetCompletionAsync(prompt, "You are a helpful assistant.", cancellationToken);
    }

    public async Task<string> GetCompletionAsync(string prompt, string systemPrompt, CancellationToken cancellationToken = default)
    {
        var chatCompletionsOptions = new ChatCompletionsOptions
        {
            DeploymentName = _deploymentName,
            Messages =
            {
                new ChatRequestSystemMessage(systemPrompt),
                new ChatRequestUserMessage(prompt)
            }
        };

        var response = await _client.GetChatCompletionsAsync(chatCompletionsOptions, cancellationToken);
        var choice = response.Value.Choices[0];
        return choice.Message.Content ?? string.Empty;
    }
}
