# ADR-0001: Clean Architecture Pattern for Backend

## Status
Proposed / Approved

## Context
AeroTwin is planned as a research-grade, portfolio-quality digital twin platform. Over time, it will incorporate diverse external domains (ADS-B trajectory feeds, GFS weather models, terrain mesh generators) and multi-modal AI systems (vision, audio, OCR, and agents). To prevent early coupling to specific framework components, database libraries, or AI SDK providers, the project requires an architecture that separates concerns, encapsulates domain business rules, and supports decoupled testing.

## Decision
We adopt **Clean Architecture** patterns for the Python backend:
- The core business entities live in `domain/` layer.
- Repository abstractions (interfaces) in `repositories/` isolate data queries from database driver details.
- Application use-cases and workflows are orchestrated in `services/`.
- Concrete ORM configurations reside in `models/` layer, mapping SQL structures to standard domain models.
- Delivery interfaces (FastAPI HTTP endpoints) reside in `api/v1/endpoints/` and depend only on service abstractions.

## Consequences
- **Pros:**
  - High degree of testability: domain logic and services can be unit tested without requiring real PostgreSQL database engines or active third-party APIs.
  - Flexibility: changing the database, migrating from standard PostgreSQL to PostGIS, or switching AI frameworks does not require modifying domain rules.
  - Consistent team workflows: developers can work in parallel on models, controllers, and services with a standardized separation of concerns.
- **Cons:**
  - Slightly higher initial boilerplate code (mapping between domain entities, ORM models, and Pydantic schemas).
