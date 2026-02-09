Daniel Adan Soto

# Distributed Self-Hosted LLM Platform
RAG-enabled, multi-host LLM deployment using AnythingLLM, vLLM, and Cloudflare Tunnel.

flowchart TD
  %% Clients / Edge
  U[User Browser]
  CF[Cloudflare]

  U -->|HTTPS 443| CF

  %% Application Stack (Host A)
  subgraph A[Application Stack]
    ING[Document Ingestion\nUpload / Parse / Chunk]
    ALLM[AnythingLLM\nUI + RAG Orchestrator]
    VDB[(Vector Database\n(Qdrant / pgvector))]

    ING --> ALLM
    ALLM -->|upsert / search| VDB
  end

  CF -->|anythingllm.mydomain.com| ALLM

  %% Inference Stack (Host B)
  subgraph B[Inference Stack]
    CFL[cloudflared\nTunnel Agent]
    EMB[Embedding Server\nOpenAI-compatible]
    VLLM[vLLM Chat Server\nOpenAI-compatible]

    CFL --> EMB
    CFL --> VLLM
  end

  %% RAG - Ingestion Path
  ALLM -->|POST /v1/embeddings\nBearer EMB_API_KEY| CF
  CF -->|embeddings.mydomain.com| CFL
  EMB -->|vectors| ALLM
  ALLM -->|store vectors| VDB

  %% RAG - Query Path
  ALLM -->|POST /v1/embeddings (query)\nBearer EMB_API_KEY| CF
  ALLM -->|similarity search (top-k)| VDB
  VDB -->|relevant chunks| ALLM

  ALLM -->|POST /v1/chat/completions\nBearer VLLM_API_KEY| CF
  CF -->|vllm.mydomain.com| CFL
  VLLM -->|completion| ALLM
  ALLM -->|streamed response| U

# Base Images:
    Cloudlab Host
        mintplexlabs/anythingllm
        qdrant/qdrant
    Homelab Host
        vllm/vllm-openai
        vllm/vllm-openai
        cloudflare/cloudflared