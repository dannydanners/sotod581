Daniel Adan Soto

# Distributed Self-Hosted LLM Platform

RAG-enabled, multi-host LLM deployment using AnythingLLM, vLLM, and Cloudflare Tunnel.

## Base Images 

**Cloudlab Host**
- mintplexlabs/anythingllm
- qdrant/qdrant

**Homelab Host**
- vllm/vllm-openai
- vllm/vllm-openai
- cloudflare/cloudflared

## Architecture

```mermaid
flowchart BT
    subgraph A[Cloudlab]
        A1[AnythingLLM]
        A2[Vector DB]
    end

    CF[Cloudflare Tunnel]
    
    subgraph B[Homelab Inference Server]
        B1[vLLM + Embeddings]
        B2[Cloudflare Tunnel]
    end
    
    A1 -->|HTTP| A2
    A1 -->|HTTPS| CF --> B2
    B1 -->|HTTPS| CF --> A1

