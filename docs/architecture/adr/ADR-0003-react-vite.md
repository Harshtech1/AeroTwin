# ADR-0003: Adoption of React and Vite for Frontend Client

## Status
Proposed / Approved

## Context
The AeroTwin frontend needs to:
1. Render highly interactive 3D map views (via Cesium, Mapbox, or custom WebGL/WebGPU renderers).
2. Maintain complex client-side state across timeline controls, OCR boarding pass inputs, and AI chat narration boxes.
3. Start up instantly and hot-reload changes during developer iteration.

## Decision
We select **React** with **TypeScript** and **Vite** as the frontend build toolchain:
- **React:** Large ecosystem for map wrappers, declarative UI rendering, and robust feature component design.
- **TypeScript:** Prevents type-mismatch bugs across large geospatial coordinate interfaces and entity configurations.
- **Vite:** Offers near-instantaneous hot module replacement (HMR) using native ES modules.
- **Tailwind CSS v4:** Modern utility-first CSS framework configured inline for rapid visual development.

## Consequences
- **Pros:**
  - Fast developer feedback loops.
  - Type-safe communication with the backend APIs via shared schema descriptions.
  - Easily scalable directory structures utilizing the `features/` modular approach.
- **Cons:**
  - Client-side routing and state management libraries must be carefully selected and integrated as the scale increases.
