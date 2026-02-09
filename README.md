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

## Architecture

```mermaid
flowchart TD
  A[AnythingLLM + Vector DB]
  T[Cloudflare Tunnel]
  B[vLLM + Embeddings]

  A --> T --> B
  B --> T --> A
