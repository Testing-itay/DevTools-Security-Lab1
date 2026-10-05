use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScanResult {
    pub path: String,
    pub findings: Vec<Finding>,
    pub mcp_servers: Vec<McpServer>,
    pub agent_configs: Vec<AgentConfig>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct McpServer {
    pub name: String,
    pub config_path: String,
    pub healthy: Option<bool>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentConfig {
    pub path: String,
    pub config_type: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Finding {
    pub file_path: String,
    pub finding_type: FindingType,
    pub message: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum FindingType {
    McpConfig,
    AgentConfig,
    SkillFile,
}
