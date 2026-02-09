Daniel Adan Soto

# Distributed Self-Hosted LLM Platform
RAG-enabled, multi-host LLM deployment using AnythingLLM, vLLM, and Cloudflare Tunnel.

flowchart LR
  %% =========================
  %% Clients / Edge
  %% =========================
  U[User Browser] -->|HTTPS 443| CF[Cloudflare]

  %% =========================
  %% Application Stack (Host A)
  %% =========================
  subgraph A[Application Stack]
    ALLM[AnythingLLM\nUI + RAG Orchestrator]
    VDB[(Vector Database\n(Qdrant / pgvector))]
    ING[Document Ingestion\nUpload / Parse / Chunk]

    ING --> ALLM
    ALLM -->|upsert / search| VDB
  end

  CF -->|anythingllm.mydomain.com| ALLM

  %% =========================
  %% Inference Stack (Host B)
  %% =========================
  subgraph B[Inference Stack]
    CFL[Cloudflare Tunnel Agent]
    VLLM[vLLM Chat Server\nOpenAI-compatible]
    EMB[Embedding Server\nOpenAI-compatible]

    CFL --> VLLM
    CFL --> EMB
  end

  %% =========================
  %% RAG - Ingestion Path
  %% =========================
  ALLM -->|POST /v1/embeddings\nBearer EMB_API_KEY| CF
  CF -->|embeddings.mydomain.com| CFL
  EMB -->|vectors| ALLM
  ALLM -->|store vectors| VDB

  %% =========================
  %% RAG - Query Path
  %% =========================
  ALLM -->|POST /v1/embeddings (query)\nBearer EMB_API_KEY| CF
  ALLM -->|similarity search (top-k)| VDB
  VDB -->|relevant chunks| ALLM

  ALLM -->|POST /v1/chat/completions\nBearer VLLM_API_KEY| CF
  CF -->|vllm.mydomain.com| CFL
  VLLM -->|completion| ALLM
  ALLM -->|streamed response| U

Base Images:
    Cloudlab Host
        mintplexlabs/anythingllm
        qdrant/qdrant
    Homelab Host
        vllm/vllm-openai
        vllm/vllm-openai
        cloudflare/cloudflared