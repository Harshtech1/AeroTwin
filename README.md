# AeroTwin

> AI-powered Digital Twin Platform for Flight Reconstruction, Geospatial Analytics, and Intelligent Flight Narration.

---

## Project Status

| Phase | Milestone | Status | Description |
| :--- | :--- | :---: | :--- |
| **Sprint 1** | Project Initialization | ✔ | Skeleton structure, config management, Docker environment |
| **Sprint 2** | Backend Foundation | ⏳ | FastAPI base, DB connections, migration runner |
| **Sprint 3** | Frontend Foundation | ⏳ | React layout, design system setup, Map/Cesium integration |
| **Sprint 4** | Boarding Pass OCR | ⏳ | Vision & OCR module to extract ticket & metadata |
| **Sprint 5** | Flight Reconstruction | ⏳ | Interpolation engine for historical ADS-B flight trajectories |
| **Sprint 6** | Weather & Terrain Engine | ⏳ | PostGIS spatial queries, terrain extraction, and GFS weather |
| **Sprint 7** | Digital Twin Simulation | ⏳ | Interactive 3D replay, camera paths, event timeline engine |
| **Sprint 8** | AI Narrator | ⏳ | Multi-modal flight narration using LLMs (LangGraph) |
| **Sprint 9** | Deployment | ⏳ | Production Docker optimization, CI/CD, hosting |

---

## Project Overview

AeroTwin is a research-grade, portfolio-quality platform designed to reconstruct commercial flights using historical trajectory data, weather models, terrain maps, satellite imagery, and multi-modal AI models. 

Unlike a generic flight tracking clone, AeroTwin builds a high-fidelity **Digital Twin** of a flight event, synthesizing geospatial telemetry with dynamic environmental metrics to generate rich interactive 3D simulations and intelligent, context-aware flight narrations.

---

## Vision

To bridge the gap between complex geospatial flight data and intuitive human understanding. By leveraging state-of-the-art AI orchestration and 3D geospatial rendering, AeroTwin aims to provide safety investigators, aviation enthusiasts, and data scientists with a cohesive platform to replay, analyze, and automatically narrate historical flight journeys.

---

## Folder Structure

The project conforms to clean architecture principles and a feature-based frontend model:

```text
AeroTwin/
├── .github/                # GitHub workflows & CI configuration
├── ai/                     # AI & ML specific workloads
│   ├── agents/             # LangGraph & orchestration agents
│   ├── embeddings/         # Text & token embedding generation
│   ├── models/             # Custom & fine-tuned model loaders
│   ├── narrator/           # Flight narration logic
│   ├── ocr/                # Ticket & boarding pass OCR logic
│   ├── pipelines/          # End-to-end inference pipelines
│   ├── prompts/            # Structured prompts & LLM templates
│   └── vision/             # Image & video processing models
├── backend/                # Python FastAPI clean architecture backend
│   ├── app/                # Main application package
│   │   ├── api/            # API routing & endpoints
│   │   │   ├── v1/         # API version 1 routers
│   │   │   │   └── endpoints/
│   │   │   └── routers.py  # Root API router aggregates
│   │   ├── core/           # Security, auth, and global helpers
│   │   ├── config/         # Environment & Pydantic settings loading
│   │   ├── constants/      # Static domain configurations
│   │   ├── domain/         # Core business logic models & entities
│   │   ├── models/         # Database ORM models
│   │   ├── schemas/        # Request/response validation schemas
│   │   ├── repositories/   # Database query abstractions
│   │   ├── services/       # Service layer handling domain execution
│   │   ├── shared/         # Common libraries shared across layers
│   │   │   ├── exceptions/ # Domain and system exception handlers
│   │   │   ├── logging/    # Standard logger specifications
│   │   │   ├── responses/  # HTTP standard structure responses
│   │   │   ├── enums/      # Global project enums
│   │   │   └── types/      # Base Python typings
│   │   ├── database/       # Connection pooling & session generators
│   │   ├── middleware/     # Custom HTTP middleware hooks
│   │   ├── startup/        # Startup check routines & event hooks
│   │   ├── utils/          # Standard utility helper scripts
│   │   ├── dependencies/   # FastAPI route dependables
│   │   └── main.py         # App entrypoint
│   ├── tests/              # Pytest testing suite
│   └── requirements.txt    # Python requirements
├── frontend/               # React + TypeScript + Vite frontend
│   ├── src/                # Source code
│   │   ├── api/            # Query & networking abstractions
│   │   ├── assets/         # Static imagery & SVGs
│   │   ├── components/     # Globally shared UI components
│   │   ├── features/       # Feature-scoped logic (Map, Timeline, OCR, etc.)
│   │   ├── hooks/          # Reusable custom hooks
│   │   ├── layouts/        # Layout blueprints
│   │   ├── pages/          # Full page view screens
│   │   ├── services/       # Data-transform and processing services
│   │   ├── styles/         # Global styles and Tailwind configuration
│   │   ├── types/          # Shared TypeScript type definitions
│   │   └── utils/          # Common TS utility helpers
├── configs/                # Central environment configs (YAML)
├── data/                   # Data pipeline structure
│   ├── raw/                # Immutable source telemetry
│   │   ├── airports/
│   │   ├── terrain/
│   │   ├── weather/
│   │   ├── satellite/
│   │   └── trajectory/
│   ├── processed/          # Parsed and structured telemetry
│   ├── external/           # Auxiliary static GIS maps
│   ├── cache/              # Local cache layers
│   └── exports/            # Rendered video or report outputs
├── docker/                 # Service Dockerfiles
├── docs/                   # Documentation and ADRs
│   └── architecture/       
│       └── adr/            # Architecture Decision Records
├── notebooks/              # Jupyter notebooks for data analysis & research
├── scripts/                # Operations scripts
│   ├── setup/
│   ├── maintenance/
│   ├── data/
│   └── deployment/
├── docker-compose.yml      # Multi-container local deployment
├── LICENSE                 # License file
├── .gitignore              # Multi-framework ignores file
└── .env.example            # Environment skeleton reference
```

---

## Technology Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Alembic, PostgreSQL, Pydantic Settings, Uvicorn
- **Frontend:** React, TypeScript, Vite, TailwindCSS (v4)
- **AI:** LangGraph (future), OpenAI / Gemini API integration, OCR (Tesseract / Vision LLMs)
- **Deployment:** Docker, Docker Compose
- **Version Control:** Git

---

## Development Roadmap

For detail, see the [Sprint Status](#project-status). The roadmap focuses on establishing a robust backend repository pattern, a React feature modular frontend, high-fidelity spatial interpolation, and multi-modal AI narration pipelines.

AeroTwin's future digital twin core is centered on a **Simulation Engine** comprised of:
1. **Replay Engine:** Chronological trajectory replay using spatiotemporal interpolation.
2. **Camera Engine:** Dynamic virtual cinematic camera tracks mapping to flights.
3. **Timeline Engine:** Aggregates telemetry timestamps with real-time weather and event feeds.
4. **Event Engine:** Evaluates anomalies, takeoff/landing triggers, and altitude deviation triggers.

---

## Contribution Guide

1. Clone the repository and establish your `.env` settings.
2. Run migrations to setup the database schema.
3. Use the defined Docker Compose files for quick service orchestration.
4. Follow PEP8, Black, and isort guidelines for Python code format.
5. Create structured ADRs for any significant architectural updates.

---

## Future Modules

- **Cesium 3D Terrain:** Integrating 3D terrain and satellite mesh layers.
- **Flight Voice Reconstructed Audio:** TTS synthesis for flight pilot-ATC transcript narration.
