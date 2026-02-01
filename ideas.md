# AI/ML Portfolio Project Ideas

## Current Portfolio Summary

Your existing projects demonstrate:
- **news-sentiment-comparison**: Full-stack (FastAPI + React/TS + MongoDB) with LLM-powered sentiment scoring
- **mcp_nethealth_chatbot**: AI agent with OpenAI + MCP protocol for network monitoring
- **go-monitor**: Go + Prometheus/Grafana observability stack
- **DevOps**: Terraform, Ansible, Docker, Kubernetes demos
- **Network automation**: Netmiko tools, preflight validators

**Strengths**: Backend APIs, MongoDB, LLM integration, DevOps/infra, Go, Python
**Gaps to fill**: RAG systems, vector DBs, ML pipelines, on-device ML, agentic workflows

---

## Top 3 High-Impact Features for news-sentiment-comparison

### 1. RAG-Powered News Q&A Endpoint (2-3 days)

Add a `/ask` endpoint that lets users query historical news with natural language.

**Why it stands out**: RAG is the #1 skill employers want right now. Shows you understand embeddings, vector search, and retrieval pipelines.

**Implementation steps**:
1. Add `chromadb` or `qdrant-client` to requirements
2. Create embeddings for stored headlines using `text-embedding-3-small` (cheap, fast)
3. Store embeddings in vector DB alongside MongoDB metadata
4. New endpoint: `POST /ask` with query like "What positive tech news happened last week?"
5. Retrieve top-k similar headlines → feed to LLM with context → return answer with sources

**Files to modify**:
- `news_sentiment/database.py` - add vector store integration
- `news_sentiment/api/routes.py` - add `/ask` endpoint
- New file: `news_sentiment/rag.py` - RAG retrieval logic

**Stack**: OpenAI embeddings + ChromaDB + existing Groq/OpenAI for generation

---

### 2. Trend Anomaly Detection with Explanation (1-2 days)

Auto-detect unusual sentiment shifts and generate AI explanations.

**Why it stands out**: Shows ML intuition (anomaly detection) + LLM reasoning = practical AI ops.

**Implementation steps**:
1. Calculate rolling 7-day sentiment averages per source
2. Flag days where sentiment deviates >2 std from rolling mean
3. When anomaly detected, call LLM: "Sentiment dropped 40% for Fox News on Jan 20. Headlines: [...]. Explain likely cause."
4. New endpoint: `GET /anomalies?days=30` returns anomalies with AI-generated explanations
5. Store explanations in MongoDB for dashboard display

**Files to modify**:
- `news_sentiment/collector.py` - add anomaly detection after daily collection
- `news_sentiment/api/routes.py` - add `/anomalies` endpoint
- `frontend/src/components/AnomalyAlert.tsx` - display anomalies in UI

---

### 3. Multi-Model Sentiment Comparison (1 day)

Compare LLM sentiment scores against a local transformer model.

**Why it stands out**: Shows you understand model evaluation, local inference, and cost optimization.

**Implementation steps**:
1. Add `transformers` + `torch` (or use `cardiffnlp/twitter-roberta-base-sentiment`)
2. Run headlines through both LLM and local model
3. Store both scores, track correlation over time
4. New endpoint: `GET /model-comparison` shows agreement rate, divergence examples
5. Dashboard panel showing "LLM vs Local Model" correlation chart

**Bonus**: Add logic to only call expensive LLM when local model confidence is low (cost optimization story for interviews)

---

## Top 3 New Project Ideas

### 1. `rag-docs-assistant` — RAG Over Your Own Codebase (3-4 days)

A CLI/API that indexes a GitHub repo and answers questions about it.

**Why it stands out**: Every AI company needs this. Shows production RAG skills.

**Features**:
- `python index.py --repo https://github.com/user/repo` clones and indexes
- Chunks code files intelligently (by function/class, not arbitrary splits)
- Stores in Qdrant/Chroma with metadata (file path, language, last modified)
- `python ask.py "How does the auth middleware work?"` returns answer + file references
- FastAPI wrapper: `POST /ask` for integration

**Tech stack**: 
- LangChain or LlamaIndex for chunking/retrieval
- Qdrant (free cloud tier) or ChromaDB (local)
- OpenAI or Groq for generation
- Tree-sitter for code-aware chunking (impressive detail)

**Repo structure**:
```
rag-docs-assistant/
├── indexer/
│   ├── chunker.py      # Code-aware chunking
│   ├── embedder.py     # Embedding generation
│   └── store.py        # Vector DB operations
├── retriever/
│   └── rag.py          # Query + retrieve + generate
├── api/
│   └── main.py         # FastAPI endpoints
├── cli.py              # CLI interface
└── README.md
```

---

### 2. `ml-deploy-pipeline` — End-to-End ML Model Serving (3-4 days)

Deploy a simple model with proper MLOps practices.

**Why it stands out**: Bridges your DevOps skills with ML. Shows you can ship models, not just train them.

**Features**:
- Train a simple model (sentiment classifier or text embedder)
- Package with Docker, serve via FastAPI
- Add model versioning (MLflow or simple Git tags)
- Prometheus metrics: latency, throughput, prediction distribution
- Kubernetes manifests for deployment
- GitHub Actions CI/CD: test → build → push → deploy

**Tech stack**:
- scikit-learn or HuggingFace transformers
- FastAPI + Uvicorn
- MLflow for experiment tracking
- Docker + K8s (leverage your existing k8s skills)
- Prometheus + Grafana (leverage your go-monitor work)

**Repo structure**:
```
ml-deploy-pipeline/
├── model/
│   ├── train.py
│   └── serve.py
├── api/
│   └── main.py
├── monitoring/
│   ├── prometheus.yml
│   └── grafana-dashboard.json
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── Dockerfile
├── MLproject           # MLflow config
└── .github/workflows/
    └── deploy.yml
```

---

### 3. `ios-ml-demo` — On-Device CoreML App (2-3 days)

Swift/SwiftUI app with on-device ML inference.

**Why it stands out**: Differentiator. Few backend devs can demo mobile + ML. Apple is hiring heavily for on-device AI.

**Features**:
- Simple image classification or text sentiment app
- Convert HuggingFace model to CoreML using `coremltools`
- SwiftUI interface with camera/text input
- Show inference time (prove it's on-device, not API)
- Compare on-device vs API latency in UI

**Implementation**:
1. Export a small model (MobileNet or DistilBERT) to CoreML format
2. Create Xcode project with SwiftUI
3. Load `.mlmodel`, run inference on user input
4. Display results with latency metrics

**Repo structure**:
```
ios-ml-demo/
├── MLDemo/
│   ├── MLDemoApp.swift
│   ├── ContentView.swift
│   ├── MLManager.swift      # CoreML inference wrapper
│   └── Models/
│       └── SentimentClassifier.mlmodel
├── scripts/
│   └── convert_to_coreml.py  # Model conversion script
└── README.md
```

---

## Quick Wins (< 1 day each)

### Add to Existing Projects

| Project | Enhancement | Time | Impact |
|---------|------------|------|--------|
| news-sentiment | Add `/embed` endpoint returning headline embeddings | 2 hrs | Shows embedding knowledge |
| news-sentiment | Streaming responses with SSE for long LLM calls | 3 hrs | Modern AI UX pattern |
| mcp_nethealth | Add conversation memory (store chat in MongoDB) | 2 hrs | Shows agentic memory |
| go-monitor | Add AI-generated alert summaries via OpenAI | 3 hrs | AIOps story |

### New Micro-Projects

| Project | Description | Time |
|---------|-------------|------|
| `embedding-visualizer` | Upload text, visualize embeddings with UMAP/t-SNE in browser | 4 hrs |
| `prompt-tester` | API to A/B test prompts, track which performs better | 4 hrs |
| `llm-cost-calculator` | CLI that estimates OpenAI/Anthropic costs for a codebase | 2 hrs |

---

## Priority Ranking for This Week

If you have limited time, here's the order I'd recommend:

1. **RAG endpoint for news-sentiment** (highest ROI — RAG is the hottest skill)
2. **rag-docs-assistant** (standalone project, very portfolio-worthy)
3. **Anomaly detection** (quick win, shows ML intuition)
4. **ios-ml-demo** (differentiator if applying to Apple/mobile-focused roles)

---

## Interview Talking Points These Enable

- "I built a RAG system that indexes news articles and answers natural language queries with source citations"
- "I implemented anomaly detection that automatically explains sentiment shifts using LLM reasoning"
- "I deployed an ML model with full observability — Prometheus metrics, Grafana dashboards, K8s autoscaling"
- "I converted a HuggingFace model to CoreML and built a Swift app that runs inference on-device in under 50ms"

---

## Resources

- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [ChromaDB Quickstart](https://docs.trychroma.com/getting-started)
- [CoreML Tools](https://apple.github.io/coremltools/docs-guides/)
- [MLflow Quickstart](https://mlflow.org/docs/latest/quickstart.html)
- [HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers)
