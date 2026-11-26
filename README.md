# Eorzea Companion AI

An autonomous AI companion inspired by the world and atmosphere of Eorzea.

The project aims to build a persistent character with a coherent personality, long-term memory, voice interaction, personal goals, and the ability to act autonomously inside a **separate, controlled simulation**.

## Project principles

- **Character first:** identity, personality, relationships, and continuity matter as much as the underlying model.
- **Persistent memory:** preserve meaningful experiences without treating every conversation as permanent memory.
- **Bounded autonomy:** the agent may plan and act within explicitly permitted environments and tools.
- **Cloud-friendly:** keep the core service deployable remotely so the companion does not need to consume the user's PC resources continuously.
- **Safe integration:** this project will not automate, read internal state from, inject into, or control the official Final Fantasy XIV client. Any future in-game integration would require explicit authorization from Square Enix.

## Initial architecture

- Python + FastAPI backend
- Agent core for perception, decisions, and planning
- Personality and character configuration
- Persistent memory (PostgreSQL initially; vector search can be added later)
- Pluggable LLM provider
- Voice interface (speech-to-text and text-to-speech)
- Independent simulation for testing autonomy

See [docs/architecture.md](docs/architecture.md) and [docs/personality.md](docs/personality.md).

## Development roadmap

1. Establish backend and configuration.
2. Implement chat and the first version of the character persona.
3. Add persistent episodic memory.
4. Add goals, planning, and bounded autonomous behavior.
5. Add voice interaction.
6. Build a small independent simulation and evaluate behavior.
7. Deploy the service to a cloud environment.

## Status

Early foundation. Interfaces and implementation details are expected to evolve.
