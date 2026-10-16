

namespace DevToolsLab.Core.Interfaces;

public interface IAiService
{
    Task<string> GetCompletionAsync(string prompt, CancellationToken cancellationToken = default);
    Task<string> GetCompletionAsync(string prompt, string systemPrompt, CancellationToken cancellationToken = default);
}
