use anyhow::Result;
use reqwest::Client;
use std::time::Duration;

/// Check if an MCP server endpoint is reachable.
pub async fn check_mcp_health(url: &str) -> Result<bool> {
    let client = Client::builder()
        .timeout(Duration::from_secs(5))
        .build()?;
    let response = client.get(url).send().await?;
    Ok(response.status().is_success())
}

/// Fetch remote MCP server status; returns None if URL is invalid or unreachable.
pub async fn fetch_mcp_status(base_url: &str) -> Option<bool> {
    let health_url = format!("{}/health", base_url.trim_end_matches('/'));
    check_mcp_health(&health_url).await.ok()
}
