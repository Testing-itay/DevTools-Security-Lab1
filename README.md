# DevTools Engine

A multi-service AI development platform for code analysis, agent orchestration, and developer tool management.

## Description

DevTools Engine is an enterprise-grade platform that brings together AI-powered code analysis, intelligent agent orchestration, and comprehensive developer tool management. Built with a polyglot architecture, it leverages the strengths of multiple languages and frameworks to deliver a unified development experience.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DevTools Engine Platform                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  Python API (FastAPI)     │  Node.js Services (Express)  │  Go Scanner       │
│  - REST/GraphQL APIs      │  - Real-time orchestration   │  - Security scan  │
│  - ML model serving       │  - WebSocket handlers        │  - Code analysis  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Java Analytics (Spring)  │  C# Core (ASP.NET)           │  Rust CLI         │
│  - Metrics aggregation    │  - Core business logic       │  - Fast tooling   │
│  - Reporting engine       │  - Plugin framework          │  - Dev experience │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Service Components

| Component | Language | Purpose |
|-----------|----------|---------|
| **API Gateway** | Python | FastAPI-based REST and GraphQL APIs, ML model inference |
| **Orchestration** | Node.js | Express services for agent coordination, real-time events |
| **Scanner** | Go | High-performance security and code analysis via Gin |
| **Analytics** | Java | Spring Boot metrics, reporting, and data aggregation |
| **Core** | C# | ASP.NET Core business logic and plugin architecture |
| **CLI** | Rust | Fast, memory-safe developer tooling and automation |

## Tech Stack

### Languages & Frameworks
- **Python 3.11+** — FastAPI, Pydantic, asyncio
- **Node.js 20+** — Express, TypeScript
- **Go 1.21+** — Gin, standard library
- **Java 17+** — Spring Boot, Maven/Gradle
- **C# 12** — ASP.NET Core 8
- **Rust** — Tokio, clap, serde

### Infrastructure
- **Terraform** — Infrastructure as Code
- **Docker** — Containerization
- **Kubernetes** — Orchestration (optional)

### AI & ML
- Model serving via Python API
- Agent orchestration via Node.js
- Code analysis pipelines

## Getting Started

### Prerequisites

- **Python 3.11+** — [python.org](https://www.python.org/)
- **Node.js 20+** — [nodejs.org](https://nodejs.org/)
- **Go 1.21+** — [go.dev](https://go.dev/)
- **Java 17+** — [adoptium.net](https://adoptium.net/)
- **.NET 8** — [dotnet.microsoft.com](https://dotnet.microsoft.com/)
- **Rust** — [rustup.rs](https://rustup.rs/)
- **Docker** (optional) — [docker.com](https://www.docker.com/)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/devtools-engine.git
   cd devtools-engine
   ```

2. **Python API**
   ```bash
   cd api/python && pip install -r requirements.txt && uvicorn main:app --reload
   ```

3. **Node.js Services**
   ```bash
   cd services/node && npm install && npm run dev
   ```

4. **Go Scanner**
   ```bash
   cd scanner/go && go build && ./scanner
   ```

5. **Java Analytics**
   ```bash
   cd analytics/java && ./mvnw spring-boot:run
   ```

6. **C# Core**
   ```bash
   cd core/csharp && dotnet run
   ```

7. **Rust CLI**
   ```bash
   cd cli/rust && cargo build --release && ./target/release/devtools-cli
   ```

## Project Structure

```
devtools-engine/
├── api/
│   └── python/              # FastAPI REST/GraphQL API
├── services/
│   └── node/                # Express orchestration services
├── scanner/
│   └── go/                  # Go security & code scanner
├── analytics/
│   └── java/                # Spring Boot analytics
├── core/
│   └── csharp/              # ASP.NET Core core logic
├── cli/
│   └── rust/                # Rust CLI tooling
├── infrastructure/
│   └── terraform/           # IaC definitions
├── .claude/                 # Claude AI config
├── .cursor/                 # Cursor IDE config
├── .codex/                  # Codex AI config
├── .gemini/                 # Gemini AI config
├── .github/                 # GitHub workflows & Copilot
└── plugins/                 # Agent plugin packages
```

Agent plugin layouts and their expected detection outcomes are documented in
[AGENT_PLUGIN_FIXTURES.md](AGENT_PLUGIN_FIXTURES.md).

## License

MIT License — see [LICENSE](LICENSE) for details.
