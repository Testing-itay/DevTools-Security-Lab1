mod config;
mod http_client;
mod models;
mod scanner;

use anyhow::Result;
use clap::Parser;
use scanner::scan_path;
use std::path::PathBuf;
use tracing_subscriber::EnvFilter;

#[derive(Parser)]
#[command(name = "devtools-scanner")]
#[command(about = "Scan and analyze developer tool configurations")]
struct Args {
    /// Root path to scan
    #[arg(short, long, default_value = ".")]
    path: PathBuf,

    /// Output format: json or text
    #[arg(short, long, default_value = "text")]
    format: String,

    /// Enable verbose logging
    #[arg(short, long)]
    verbose: bool,
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = Args::parse();

    let filter = if args.verbose {
        EnvFilter::new("debug")
    } else {
        EnvFilter::new("warn")
    };
    tracing_subscriber::fmt().with_env_filter(filter).init();

    let result = scan_path(&args.path).await?;

    match args.format.as_str() {
        "json" => println!("{}", serde_json::to_string_pretty(&result)?),
        _ => {
            println!("Scan: {}", result.path);
            for f in &result.findings {
                println!("  [{}] {} - {}", f.file_path, format!("{:?}", f.finding_type), f.message);
            }
        }
    }

    Ok(())
}
