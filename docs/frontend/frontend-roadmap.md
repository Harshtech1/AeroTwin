# Sprint 3 Frontend Roadmap

This roadmap decomposes the Frontend Foundation into independently reviewable increments. It deliberately excludes Cesium implementation and backend feature integration. Contract fixtures and adapters may be defined, but no production endpoint behavior is changed.

## Sprint 3.1 — Architecture and quality foundations

### Objectives

Establish boundaries, conventions, routing skeleton, test strategy, and runtime configuration so parallel work does not conflict.

### Deliverables

- Approved architecture, routing, state, hierarchy, and component inventory documents.
- Feature-first target folders and public API conventions.
- Route manifest and layout contracts.
- Typed environment/configuration contract.
- Testing pyramid, accessibility checklist, import-boundary rules, and ADR proposals.

### Acceptance criteria

- Every planned page has one owning module and parent layout.
- Dependency direction and forbidden imports are documented and enforceable.
- State ownership decisions cover server, URL, global, workspace, map, and playback state.
- No secret is proposed for browser exposure.
- Open architectural decisions have named ADR owners.

### Dependencies

Product Experience Blueprint; ADR-0001 and ADR-0003; backend envelope/request-ID conventions.

### Estimated complexity

**Medium** — low implementation volume, high coordination impact.

## Sprint 3.2 — Design system and application shell

### Objectives

Create the accessible visual primitives and responsive shell needed by all product pages.

### Deliverables

- Token architecture for color, typography, spacing, radius, elevation, motion, and breakpoints.
- Core primitives: buttons, inputs, cards, badges, dialogs, menus, tables, skeletons, empty/error states.
- Public, auth, application, project, and workspace layouts.
- Sidebar, topbar, responsive navigation, notification surface.
- Component documentation and interaction/accessibility tests.

### Acceptance criteria

- Components meet inventory contracts and WCAG 2.2 AA expectations.
- Keyboard, focus, reduced-motion, compact/wide layouts, and touch targets are verified.
- No page owns a duplicate primitive.
- Visual variants use tokens rather than one-off values.
- Shell supports route outlets without feature knowledge.

### Dependencies

Sprint 3.1 conventions; finalized design tokens and approved shadcn/ui integration strategy.

### Estimated complexity

**High** — broad shared surface and high regression radius.

## Sprint 3.3 — Core navigation pages

### Objectives

Build route composition for Landing, Authentication, Dashboard, Projects, Project Detail, Library, and Settings using fixtures and shared primitives.

### Deliverables

- Lazy route modules, guards, page metadata, and route error boundaries.
- Responsive page compositions for all core navigation pages.
- Typed fixture repository mirroring proposed frontend domain models.
- Empty, loading, error, permission, and populated states.
- Search/filter URL-state behavior for Projects and Library.

### Acceptance criteria

- Direct navigation and browser history work for every route.
- Protected routes do not flash before session resolution.
- All page states are keyboard accessible and responsive.
- Pages contain composition only; fixture access follows the same adapter boundary planned for Query.
- No backend call is made.

### Dependencies

Sprint 3.2 shell/component library; authentication and project contract review.

### Estimated complexity

**High** — many routes, moderate behavior, substantial state coverage.

## Sprint 3.4 — Ingestion and review workflow

### Objectives

Build the Upload Wizard and OCR Review experience as testable state machines using local fixtures, without implementing OCR or changing APIs.

### Deliverables

- Upload wizard step model, validation, file queue, progress/cancellation presentation, and recovery states.
- OCR review field grouping, source-image/field coordination, confidence states, keyboard workflow, and correction draft model.
- Unsaved-change protection and resumable UI policy.
- Contract proposals for upload/job/OCR resources for backend review.

### Acceptance criteria

- Wizard transitions are deterministic and test-covered.
- Unsupported, oversized, duplicate, failed, and cancelled file states are represented.
- OCR fields expose source, confidence, validation, and correction status without color-only communication.
- Draft corrections survive safe in-route navigation according to policy.
- No OCR processing or production API request is implemented.

### Dependencies

Sprint 3.2 forms/progress/dialogs; Sprint 3.3 project context; approved fixture contracts.

### Estimated complexity

**High** — workflow state, validation, and accessibility complexity.

## Sprint 3.5 — Workspace UI contracts and hardening

### Objectives

Define and assemble Replay, Analysis, and Story workspace UI boundaries without Cesium or backend integration, then harden the whole Sprint 3 surface.

### Deliverables

- Workspace layout, inspector, timeline, playback controls, layer manager, map-control placeholders, event cards, chart containers, and story cards.
- Serializable playback/map/story state contracts and fake adapters.
- Route-level lazy boundaries and bundle budgets.
- Accessibility, responsive, performance, and browser test pass.
- Contributor playbook and ownership map for later Cesium, OCR, reconstruction, and simulation teams.

### Acceptance criteria

- Workspaces function with deterministic fixtures and no map engine.
- Playback controls are keyboard operable and expose accessible state.
- Compact layouts move panels into accessible drawers/sheets.
- Heavy future dependencies have explicit lazy adapter seams.
- Lint, type check, unit, interaction, accessibility, and route smoke suites pass.
- Sprint 4+ logic, Cesium, and backend calls remain out of scope.

### Dependencies

Sprints 3.1–3.4; future engine interface reviews; performance budgets.

### Estimated complexity

**Very high** — multiple dense workspaces plus cross-cutting hardening.

## Sequencing gate

A sprint slice may begin in parallel only after the contracts it consumes are approved. Shared primitives are merged before page-specific use; page teams must not create private substitutes to avoid waiting. Any change to the Product Experience Blueprint returns to product/design review rather than being silently resolved in implementation.
