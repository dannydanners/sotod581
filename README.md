Daniel Adan Soto

# Distributed Self-Hosted LLM Platform

RAG-enabled, multi-host LLM deployment using AnythingLLM, vLLM, and Cloudflare Tunnel.

## Base Images 

Cloudlab Host:
   - mintplexlabs/anythingllm
   - qdrant/qdrant
Homelab Host:
    - vllm/vllm-openai
    - vllm/vllm-openai
    - cloudflare/cloudflared

## Architecture

```mermaid
flowchart TD
    subgraph A[Cloudlab]
        A1[AnythingLLM + Vector DB]
        A2[Cloudflare Tunnel]
    end

    CF[Cloudflare Tunnel]
    
    subgraph B[Homelab Inference Server]
        B1[vLLM]
        B2[Embeddings]
    end
  
    A --> CF --> B
    B --> CF --> A
