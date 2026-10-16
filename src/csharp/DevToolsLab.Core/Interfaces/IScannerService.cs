


namespace DevToolsLab.Core.Interfaces;

public interface IScannerService
{
    Task<ScanResult> AnalyzeAsync(string path, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<ScanFinding>> GetFindingsAsync(string scanId, CancellationToken cancellationToken = default);
}

public record ScanResult(string ScanId, int FindingCount, string Status);

public record ScanFinding(string Id, string Severity, string Message);
