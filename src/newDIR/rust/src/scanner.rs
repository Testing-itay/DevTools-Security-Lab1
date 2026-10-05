use crate::models::{AgentConfig, Finding, FindingType, McpServer, ScanResult};
use anyhow::Result;
use regex::Regex;
use std::path::Path;
use tokio::task::spawn_blocking;
use walkdir::WalkDir;

const MCP_PATTERN: &str = r"(?i)mcp.*\.(toml|json)$";
const AGENT_PATTERN: &str = r"(?i)(agents?|\.cursorrules|AGENTS\.md)$";
const SKILL_PATTERN: &str = r"(?i)skills?/.*\.md$";

/// Scan a directory for dev tool configs and return findings.
pub async fn scan_path(root: &Path) -> Result<ScanResult> {
    let root = root.to_path_buf();
    let result = spawn_blocking(move || {
        let mcp_re = Regex::new(MCP_PATTERN).unwrap();
        let agent_re = Regex::new(AGENT_PATTERN).unwrap();
        let skill_re = Regex::new(SKILL_PATTERN).unwrap();

        let mut findings = Vec::new();
        let mut mcp_paths = Vec::new();
        let mut agent_paths = Vec::new();

        for entry in WalkDir::new(&root)
            .follow_links(false)
            .into_iter()
            .filter_map(|e| e.ok())
        {
            let path = entry.path();
            if !path.is_file() {
                continue;
            }
            let path_str = path.to_string_lossy();

            if mcp_re.is_match(&path_str) {
                findings.push(Finding {
                    file_path: path_str.to_string(),
                    finding_type: FindingType::McpConfig,
                    message: "MCP server config detected".into(),
                });
                mcp_paths.push(path_str.to_string());
            } else if agent_re.is_match(&path_str) {
                findings.push(Finding {
                    file_path: path_str.to_string(),
                    finding_type: FindingType::AgentConfig,
                    message: "Agent config detected".into(),
                });
                agent_paths.push(path_str.to_string());
            } else if skill_re.is_match(&path_str) {
                findings.push(Finding {
                    file_path: path_str.to_string(),
                    finding_type: FindingType::SkillFile,
                    message: "Skill file detected".into(),
                });
            }
        }

        let mcp_servers = mcp_paths
            .into_iter()
            .map(|p| McpServer {
                name: Path::new(&p)
                    .file_stem()
                    .and_then(|s| s.to_str())
                    .unwrap_or("unknown")
                    .to_string(),
                config_path: p,
                healthy: None,
            })
            .collect();

        let agent_configs = agent_paths
            .into_iter()
            .map(|p| AgentConfig {
                path: p.clone(),
                config_type: Path::new(&p)
                    .file_name()
                    .and_then(|s| s.to_str())
                    .unwrap_or("config")
                    .to_string(),
            })
            .collect();

        ScanResult {
            path: root.to_string_lossy().to_string(),
            findings,
            mcp_servers,
            agent_configs,
        }
    })
    .await?;

    Ok(result)
}
