# ClarityForge

> "Your rigorous thinking partner. Audit biases, simulate outcomes, calibrate judgment."

## Overview

ClarityForge is a production-grade AI-powered thinking partner that helps founders, strategists, and analysts make better decisions by:

- **Auditing cognitive biases** - Detects 15+ common cognitive biases in your reasoning
- **Simulating decision outcomes** - What-if scenario modeling with probability ranges
- **Calibrating judgment over time** - Tracks prediction accuracy and bias patterns

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS |
| **UI Components** | shadcn/ui + Radix primitives |
| **Interactive Maps** | React Flow |
| **Backend** | Python (FastAPI) |
| **AI Orchestration** | LangChain + custom agents |
| **AI Providers** | OpenAI, Anthropic, Groq, Ollama |
| **Database** | PostgreSQL (Supabase) |
| **Caching** | Redis (Upstash) |

## Project Structure

```
clarityforge/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # FastAPI backend
├── packages/
│   ├── shared/       # Shared types and AI providers
│   └── ui/           # Shared UI components
├── .github/
│   └── workflows/    # CI/CD pipelines
└── turbo.json        # Turborepo config
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- pnpm 8+

### Installation

```bash
# Clone the repository
git clone https://github.com/Heisdawrld/ClarityForge.git
cd ClarityForge

# Install dependencies
pnpm install

# Set up environment variables
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env
```

### Development

```bash
# Run all apps in development mode
pnpm dev

# Run specific app
pnpm --filter web dev
pnpm --filter api dev
```

## Features

### Phase 1: Foundation
- [x] Monorepo structure with Turborepo
- [x] TypeScript strict mode
- [x] FastAPI backend with Pydantic v2
- [x] Authentication system (JWT)
- [x] CI/CD pipeline

### Phase 2: Core Reasoning
- [x] AI Provider abstraction (OpenAI, Anthropic, Groq, Ollama)
- [x] Reasoning session pipeline
- [x] Bias taxonomy (15+ cognitive biases)
- [x] React Flow reasoning workspace

### Phase 3: Judgment Ledger
- [x] Session CRUD API
- [x] Outcome tracking
- [ ] Calibration dashboard

### Phase 4: Polish & Launch
- [ ] Simulation engine
- [ ] Export system (PDF reports)
- [ ] Performance optimization
- [ ] Monitoring & observability

## License

MIT