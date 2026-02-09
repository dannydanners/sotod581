# Technical Report  
## Distributed Self-Hosted LLM Platform

---

## Chapter 1: Vision and System Overview

### 1.1 Project Vision

The goal of this project is to design and deploy a **distributed, self-hosted Large Language Model (LLM) platform** that supports **retrieval-augmented generation (RAG)** while maintaining full control over data, inference, and infrastructure.

Rather than relying on a monolithic or third-party hosted LLM service, the system separates responsibilities across multiple hosts to improve **security, scalability, and operational flexibility**. The platform is intended to support knowledge-grounded question answering over private document collections while minimizing external exposure and avoiding vendor lock-in.

The system is guided by the following design principles:

- **Separation of Concerns**  
  User interaction, knowledge storage, and model inference are deployed as independent services.

- **Private Connectivity**  
  Communication between hosts occurs exclusively through a secure tunnel without exposing inference services directly to the public internet.

- **Extensibility**  
  Models, embedding services, and vector databases can be replaced or upgraded without redesigning the overall system.

---

### 1.2 High-Level Architecture

The platform consists of two primary hosts:

- **Host A (Application Host)**  
  Responsible for user interaction, document ingestion, and vector storage.

- **Host B (Inference Host)**  
  Responsible for embedding generation and LLM inference.

A **Cloudflare Tunnel** provides secure connectivity between the two hosts, allowing the application host to access inference services without opening inbound firewall ports.

At a high level, the system operates as follows:

1. Users interact with the system through a web-based interface.
2. Documents are ingested and converted into vector embeddings.
3. Queries retrieve relevant context from the vector database.
4. Retrieved context is sent to the inference host for response generation.
5. Generated responses are returned to the user.

This architecture follows cloud-native design principles, isolating compute-intensive inference workloads from user-facing services while maintaining secure communication between components.

---

## Chapter 2: Technical Design and Implementation

### 2.1 Application Host (Host A)

Host A runs the application and storage components of the platform. 

Responsibilities:
- Handling user interaction
- Document ingestion and preprocessing
- Vector storage and similarity search
- Orchestrating retrieval-augmented generation workflows

The primary services deployed on Host A are:

- **AnythingLLM**  
  Provides the user interface and coordinates the RAG pipeline, including document ingestion, embedding requests, and prompt construction.

- **Vector Database (Qdrant)**  
  Stores vector embeddings and supports similarity search operations.

Communication between AnythingLLM and the vector database occurs locally over the Docker network using standard HTTP/TCP connections.

---

### 2.2 Inference Host (Host B)

Host B is dedicated to model execution and embedding generation. It is isolated from direct user access and does not expose any inbound network ports.

The inference host runs the following services:

- **vLLM (Chat Inference Service)**  
  Executes the primary language model used to generate responses.

- **Embedding Service**  
  Runs as a separate container to generate embeddings for both document ingestion and query processing.

- **Cloudflare Tunnel Agent (`cloudflared`)**  
  Maintains an outbound-only secure connection that allows Host A to reach inference services through HTTPS endpoints.

Separating the embedding service and chat inference into different containers allows each workload to be tuned and managed independently.

---

### 2.3 Secure Host-to-Host Communication

All communication between Host A and Host B occurs through **Cloudflare Tunnel**. This design removes the need for inbound firewall rules on the inference host and significantly reduces the attack surface.

Key characteristics:

- Outbound-only connectivity from Host B
- Encrypted HTTPS communication
- API key authentication for inference endpoints
- Clear separation between application and inference responsibilities

From Host A’s perspective, inference services appear as standard HTTPS endpoints, while Cloudflare routes traffic through the tunnel to the appropriate services on Host B.

---

### 2.4 Retrieval-Augmented Generation Workflow

The system implements retrieval-augmented generation in two phases.

#### Document Ingestion Phase

1. Documents are uploaded through the application interface.
2. Text is extracted, chunked, and sent to the embedding service.
3. Generated embeddings are stored in the vector database along with metadata.

#### Query Processing Phase

1. A user submits a query.
2. The query is embedded using the embedding service.
3. Similar vectors are retrieved from the vector database.
4. Retrieved context is combined with the user query.
5. The prompt is sent to the LLM inference service.
6. The generated response is returned to the user.

Enables responses grounded in private, up-to-date data.

---

### 2.5 Summary

The proposed system satisfies the technical requirements by combining self-hosted infrastructure with cloud-native design principles. By separating application logic, storage, and inference across distinct hosts and connecting them through a secure tunnel, the platform achieves flexibility, security, and scalability while supporting advanced RAG-based workloads.