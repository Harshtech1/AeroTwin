# ADR-0002: Adoption of FastAPI for Backend Service

## Status
Proposed / Approved

## Context
The AeroTwin platform requires a backend API capable of:
1. Orchestrating long-running simulations and asynchronous tasks (e.g. video rendering, terrain mesh processing).
2. Offering highly responsive endpoints for interactive 3D map client synchronization.
3. Automatically validating and documenting endpoints for consumption by AI agent tools and frontends.

## Decision
We select **FastAPI** as our core backend application framework:
- Built-in asynchronous capability (`async/await`) leveraging ASGI.
- Seamless automatic schema generation via OpenAPI, satisfying auto-documentation requirements.
- Integration of Pydantic for validation, parsing, and settings serialization.
- High performance, matching or exceeding Node.js and Go in common benchmarks.

## Consequences
- **Pros:**
  - Fast development cycle with automatic interactive documentation (Swagger UI).
  - Out-of-the-box asynchronous support, crucial for coordinate stream processing and real-time simulations.
  - Native integration with modern Python type-hinting, facilitating static analysis and IDE safety.
- **Cons:**
  - Relatively thin framework; structure must be manually constructed (e.g. folder layout, dependency injection patterns, database session tracking) compared to full-featured frameworks like Django.
