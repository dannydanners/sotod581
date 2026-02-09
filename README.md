Daniel Adan Soto

# Distributed Self-Hosted LLM Platform

RAG-enabled, multi-host LLM deployment using AnythingLLM, vLLM, and Cloudflare Tunnel.

## Base Images 

Cloudlab Host
    mintplexlabs/anythingllm
    qdrant/qdrant
Homelab Host
    vllm/vllm-openai
    vllm/vllm-openai
    cloudflare/cloudflared

## Architecture

```mermaid
flowchart TD
  %% Client
  U[User Browser]

  %% Cloudflare
  CF_EDGE[Cloudflare\nDNS / TLS / WAF]
  CF_TUNNEL[Cloudflare Tunnel\nRouting]

  U -->|HTTPS 443| CF_EDGE

  %% Application Stack
  subgraph A[Application Stack]
    ING[Document Ingestion\nUpload / Parse / Chunk]
    ALLM[AnythingLLM\nUI + RAG Orchestrator]
    VDB[(Vector Database\nQdrant / pgvector)]

    ING --> ALLM
    ALLM -->|upsert / search| VDB
  end

  CF_EDGE -->|anythingllm.mydomain.com| ALLM

  %% Inference Stack
  subgraph B[Inference Stack]
    CFL[cloudflared\nTunnel Agent]
    EMB[Embedding Server\nOpenAI-compatible]
    VLLM[vLLM Chat Server\nOpenAI-compatible]

    CFL --> EMB
    CFL --> VLLM
  end

  %% RAG – Ingestion
  ALLM -->|POST /v1/embeddings\nBearer EMB_API_KEY| CF_TUNNEL
  CF_TUNNEL -->|embeddings.mydomain.com| CFL
  EMB -->|vectors| ALLM
  ALLM -->|store vectors| VDB

  %% RAG – Query
  ALLM -->|POST /v1/embeddings (query)\nBearer EMB_API_KEY| CF_TUNNEL
  ALLM -->|similarity search (top-k)| VDB
  VDB -->|relevant chunks| ALLM

  ALLM -->|POST /v1/chat/completions\nBearer VLLM_API_KEY| CF_TUNNEL
  CF_TUNNEL -->|vllm.mydomain.com| CFL
  VLLM -->|completion| ALLM
  ALLM -->|streamed response| U