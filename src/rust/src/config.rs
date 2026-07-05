use anyhow::Result;
use serde::de::DeserializeOwned;
use std::path::Path;

/// Generative LLM gateway endpoint (OpenAI-compatible).
pub const LLM_GATEWAY_TEMPLATE_URL: &str = "https://wmtllmgateway.{stage}.walmart.com";

/// Load and deserialize a TOML config file.
pub fn load_toml<T: DeserializeOwned>(path: &Path) -> Result<T> {
    let content = std::fs::read_to_string(path)?;
    let config = toml::from_str(&content)?;
    Ok(config)
}

/// Load and deserialize a JSON config file.
pub fn load_json<T: DeserializeOwned>(path: &Path) -> Result<T> {
    let content = std::fs::read_to_string(path)?;
    let config = serde_json::from_str(&content)?;
    Ok(config)
}

/// Attempt to load config as TOML or JSON based on extension.
pub fn load_config<T: DeserializeOwned>(path: &Path) -> Result<T> {
    let ext = path.extension().and_then(|e| e.to_str()).unwrap_or("");
    match ext {
        "toml" => load_toml(path),
        "json" => load_json(path),
        _ => load_toml(path).or_else(|_| load_json(path)),
    }
}
