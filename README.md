Daniel Adan Soto

# Distributed Self-Hosted LLM Platform

RAG-enabled, multi-host LLM deployment using AnythingLLM, vLLM, and Cloudflare Tunnel.

## Architecture

```mermaid
flowchart BT
    subgraph A[Cloudlab]
        A1[AnythingLLM]
        A2[Vector DB]

        A1 --> |HTTP| A2
    end

    CF[Cloudflare Tunnel]
    
    subgraph B[Homelab Inference Server]
        B1[vLLM]
        B2[Embeddings]
        B3[cloudflared]

        B3 --> B2
        B3 --> B1
    end
    
    A1 -->|HTTPS| CF
    CF --> B3

    B1 -->|HTTPS| CF
    CF --> A1
```

## Base Images 

**Cloudlab Host**
- mintplexlabs/anythingllm
- qdrant/qdrant

**Homelab Host**
- vllm/vllm-openai
- vllm/vllm-openai
- cloudflare/cloudflared
