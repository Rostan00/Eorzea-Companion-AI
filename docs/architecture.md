# Architecture

## Goals

The companion should feel like a continuous character rather than a stateless chatbot. It should be available through a lightweight client while its reasoning, memory, and scheduled work can run remotely.

## High-level components

```text
Desktop / Web Client
  |  chat, voice, notifications
  v
FastAPI Backend
  |
  +-- Agent Core
  |     +-- Perception / context assembly
  |     +-- Decision and policy layer
  |     +-- Planner / goal manager
  |
  +-- Character
  |     +-- Identity and persona
  |     +-- Emotional / relationship state
  |
  +-- Memory
  |     +-- Episodic memories
  |     +-- Semantic facts
  |     +-- Retrieval and summarization
  |
  +-- LLM Provider Adapter
  |
  +-- Tools / Independent Simulation
        +-- Explicitly allowlisted actions
        +-- Observable state and action results

PostgreSQL stores durable state. Optional vector search can be introduced after the basic memory model works.
```

## Proposed stack

| Area | Initial choice | Reason |
|---|---|---|
| API | Python, FastAPI | Simple async API and mature ecosystem |
| Agent logic | Plain Python modules | Keep behavior inspectable before adding frameworks |
| Database | PostgreSQL | Durable relational state |
| LLM | Provider adapter | Avoid coupling the project to one model vendor |
| Client | Web first; desktop wrapper later | Fast iteration |
| Voice | Separate STT and TTS adapters | Providers can be swapped independently |
| Deployment | Docker | Reproducible local and cloud environments |

## Autonomy cycle

1. Observe the current conversation or simulation state.
2. Build a compact context from persona, memory, and current goals.
3. Decide whether a response or action is appropriate.
4. Check the action against permissions and safety rules.
5. Execute only an allowlisted action in the independent simulation.
6. Record the outcome and decide whether it is worth remembering.

## Safety boundary

The system is designed for conversation and independent simulation. It must not automate gameplay, inspect process memory, inject code, send inputs, or otherwise control the official FFXIV client. A future integration with that client is out of scope unless Square Enix explicitly authorizes it.

## First implementation milestone

Create a minimal FastAPI service with:
- health endpoint;
- chat endpoint;
- loadable persona configuration;
- a provider interface with a mock implementation;
- tests for the API and policy boundary.

Memory, voice, and autonomous simulation should be added incrementally after this foundation is testable.
