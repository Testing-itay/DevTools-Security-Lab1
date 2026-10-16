
using DevToolsLab.Core.Interfaces;

namespace DevToolsLab.Api.Services;

public class ScannerService : IScannerService
{
    public async Task<ScanResult> AnalyzeAsync(string path, CancellationToken cancellationToken = default)
    {
        await Task.Delay(100, cancellationToken);
        var scanId = Guid.NewGuid().ToString("N");
        var findings = new List<ScanFinding>
        {
            new(Guid.NewGuid().ToString("N"), "Info", "Analysis started"),
            new(Guid.NewGuid().ToString("N"), "Low", "Potential improvement detected")
        };
        return new ScanResult(scanId, findings.Count, "Completed");
    }

    public async Task<IReadOnlyList<ScanFinding>> GetFindingsAsync(string scanId, CancellationToken cancellationToken = default)
    {
        await Task.Delay(50, cancellationToken);
        return new List<ScanFinding>
        {
            new(Guid.NewGuid().ToString("N"), "Info", "Finding for scan " + scanId)
        };
    }
}
