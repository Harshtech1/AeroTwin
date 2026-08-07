# AeroTwin Frontend Technical Architecture

**Status:** Approved engineering blueprint
**Scope:** Product Experience Blueprint implementation
**Stack baseline:** React, TypeScript, Vite, Tailwind CSS v4, shadcn/ui, Motion, TanStack Query, Zustand

## 1. Overall frontend architecture and principles

AeroTwin is a long-lived, workflow-heavy application, not a collection of screens. The frontend follows a **feature-first modular monolith** with explicit boundaries. Product features own their UI, state, query definitions, adapters, and tests. Shared code contains only genuinely cross-feature capabilities.

Dependency direction is:

`app -> pages/routes -> features -> entities -> shared`

Imports must never point upward. Features must not import other features directly; orchestration belongs in a page or application workflow. The API transport must not leak generated DTOs into view components. Cesium, charting, OCR, and media implementations are replaceable adapters behind feature contracts.

### Boundary rules

- `app` composes providers, router, authentication bootstrap, and global error boundaries.
- `pages` compose features for one route; they contain no reusable domain logic.
- `features` represent user capabilities such as upload, OCR review, replay, analysis, and story editing.
- `entities` contain domain display models and entity-level components such as Project or FlightEvent.
- `shared` contains the design system, transport, generic hooks, utilities, and configuration.
- Cross-feature workflows communicate through route state, typed service results, query invalidation, or narrowly scoped shared stores—not feature-to-feature imports.
- No business decision belongs in a presentational component.

## 2. Target folder organization

```text
frontend/src/
├── app/                         # Composition root only
│   ├── providers/               # Query, auth, theme, notifications
│   ├── router/                  # Route tree, guards, lazy boundaries
│   ├── errors/                  # Root/route error boundaries
│   └── config/                  # Runtime-safe application config
├── pages/                       # Route-level composition
│   ├── landing/
│   ├── dashboard/
│   ├── projects/
│   ├── upload/
│   ├── ocr-review/
│   ├── replay/
│   ├── analysis/
│   ├── story/
│   ├── library/
│   ├── settings/
│   └── authentication/
├── features/
│   ├── auth/
│   ├── project-management/
│   ├── flight-upload/
│   ├── ocr-review/
│   ├── replay/
│   ├── analysis/
│   ├── story-editor/
│   ├── library/
│   └── preferences/
├── entities/                    # Project, asset, event, story, user
├── shared/
│   ├── api/                     # HTTP client, envelope, errors, contracts
│   ├── components/              # Product-agnostic component library
│   ├── hooks/                   # Generic reusable hooks
│   ├── layouts/                 # Public, auth, app, project, workspace
│   ├── services/                # Telemetry, logging, files, feature flags
│   ├── styles/                  # Tokens and global styles
│   ├── types/                   # Truly global types only
│   ├── utils/
│   └── test/
└── main.tsx
```

Each feature exposes a deliberate public API through its root barrel. Deep imports across boundaries are prohibited. A feature may contain `api`, `components`, `hooks`, `model`, `services`, `store`, `types`, and `test` subfolders as needed; empty ceremonial folders are discouraged.

## 3. Routing architecture

Use React Router with a declarative route tree and route-level lazy modules. Public, authentication, application, project, and immersive workspace layouts are nested. Authentication and project access are loader/guard concerns, not effects inside pages. Route parameters are parsed and validated once at the boundary. Search parameters are the source of truth for shareable filters, selected tabs, time ranges, and library queries. Full details are in [routing.md](./routing.md).

## 4. Layout hierarchy

```text
RootBoundary
├── PublicLayout -> Landing
├── AuthLayout -> Login / callback / recovery
└── AuthenticatedLayout
    ├── AppLayout (Sidebar + Topbar + content) -> Dashboard, Projects, Library, Settings
    └── ProjectLayout (Project header + tabs)
        ├── Project Detail / Upload / OCR Review
        └── WorkspaceLayout (full viewport + panels)
            ├── Replay Workspace
            ├── Analysis Workspace
            └── Story Editor
```

Workspace routes intentionally escape the normal constrained content width. They retain project context and global escape navigation while prioritizing map, timeline, canvas, and inspector surfaces.

## 5. State management strategy

- **Local React state:** ephemeral component state, uncontrolled interaction details, open/closed state owned by one subtree.
- **React Context:** stable capabilities and low-frequency cross-tree values such as authenticated identity, theme, feature flags, and service injection.
- **TanStack Query:** all remote/server state, caching, background refresh, mutations, invalidation, and polling.
- **Zustand:** high-frequency or independently consumed client state, especially replay, map, panel layout, and draft editor sessions.
- **URL state:** navigation, shareable filters, selected project section, and durable workspace selections.

Server responses must never be copied wholesale into Zustand. Derived values are computed with selectors. Detailed ownership rules are in [state-management.md](./state-management.md).

## 6. API layer architecture

The API layer has four stages:

1. **Transport:** one configured fetch-compatible client handles base URL, credentials, timeout/abort, request ID propagation, content negotiation, and envelope decoding.
2. **Contracts:** endpoint request/response DTOs reflect the backend contract and are runtime-validated at trust boundaries when practical.
3. **Adapters:** pure mappers convert transport DTOs to frontend domain/view models and back.
4. **Query definitions:** features expose stable query-key factories, query options, and mutation options.

Endpoint paths, headers, and envelope details exist in one place. Components never invoke `fetch`, inspect HTTP status codes, or know backend casing. Cancellation uses `AbortSignal`. Uploads use a dedicated transport supporting progress and cancellation. Long-running OCR/reconstruction/simulation jobs are represented as resources and observed through bounded polling until the backend offers a push channel.

The current backend returns a standard response envelope and request IDs; the frontend should preserve those IDs on normalized errors for support correlation. API versioning remains under `/api/v1` and is configuration-driven.

## 7. Service layer

Services coordinate browser or vendor capabilities that are not server state:

- authentication session coordination;
- upload validation and multipart preparation;
- telemetry/error reporting with redaction;
- feature flags;
- storage abstraction for non-sensitive preferences;
- file download/export;
- map engine adapter (future);
- media/replay clock adapter;
- narration preview adapter (future).

Services are interfaces at feature boundaries and concrete adapters at the composition root. They must be deterministic where possible and independently testable. Domain rules remain in feature/entity models rather than generic services.

## 8. Reusable hooks

Global hooks are limited to product-agnostic browser behavior: media query, reduced motion, focus return, keyboard shortcut, debounced value, previous value, document title, online status, and stable event callbacks. Feature hooks stay within their owning feature. Hooks do not hide navigation unexpectedly or combine unrelated responsibilities. Query hooks return normalized domain results rather than raw transport responses.

## 9. Authentication flow

1. Bootstrap requests the current session using secure, HTTP-only cookie credentials; tokens are not stored in local storage.
2. While unresolved, render the application bootstrap skeleton rather than protected content.
3. Public-only and protected guards redirect with a validated internal `returnTo` location.
4. Login submits through the auth mutation; success refreshes the session query and replaces history at `returnTo`.
5. A single-flight refresh/session recovery path prevents request storms.
6. A definitive unauthorized response clears cached private data, resets client stores, and redirects to login.
7. Logout calls the server, clears all user-scoped queries/stores, and navigates to the public surface.
8. Authorization is enforced by the backend; frontend capability checks only shape the experience.

OAuth callback, email verification, and password recovery live under `/auth/*` and never accept arbitrary external redirects.

## 10. Errors, loading, and recovery

Errors use a normalized discriminated model: `network`, `unauthorized`, `forbidden`, `notFound`, `validation`, `conflict`, `rateLimit`, `server`, `cancelled`, and `unknown`. Each carries a safe message, retryability, field details where relevant, and request ID. Global boundaries handle boot/chunk failures; route boundaries handle page failures; components handle expected mutation and validation errors.

Loading is progressive:

- bootstrap shell skeleton for session/router initialization;
- route-level fallback for lazy bundles;
- shape-matched skeletons for first load;
- retained content plus subtle progress for background refresh;
- localized pending state for mutations;
- explicit job progress for uploads, OCR, and reconstruction.

Never replace usable cached content with a full-page spinner. Empty, error, permission, offline, and not-found states are distinct.

## 11. Optimistic updates and cache strategy

Optimism is allowed only for fast, reversible, low-conflict actions: renaming, starring, tagging, preference toggles, and local story ordering. Before mutation, cancel relevant queries and snapshot cache; update optimistically; restore on error; reconcile with the authoritative response on settlement. Upload, OCR correction submission, reconstruction, deletion, export, and simulation jobs are not optimistically declared complete.

Query keys are hierarchical and centrally generated per feature, for example project collection -> project detail -> project assets. Defaults:

- identity/session: short stale time, refetch on focus;
- project lists/details: moderate stale time, invalidate after mutation;
- immutable processed artifacts: long stale time;
- active jobs: adaptive polling while active, stop when terminal/hidden;
- map/telemetry ranges: keyed by project, version, range, and resolution with bounded retention.

Persisted server cache is deferred until offline requirements exist. Sensitive user or project payloads must not be written to browser persistence by default.

## 12. Environment configuration

Only variables prefixed for Vite exposure may enter the browser bundle. A typed configuration module validates required values on startup. Proposed public variables include API base URL, application environment, release identifier, telemetry endpoint, and public Cesium asset configuration when its sprint begins. Secrets—including AI keys and private map credentials—remain server-side. Development, test, staging, and production use the same artifact where deployment infrastructure can inject runtime config; otherwise each build validates environment-specific values. Feature flags are explicit, typed, and default-safe.

## 13. Responsive architecture

Start mobile-first with design-token breakpoints rather than device names. Each page defines behavior at **compact**, **medium**, and **wide** capabilities:

- Sidebar becomes a modal navigation drawer on compact screens.
- Dense tables become prioritized lists or horizontally managed grids, never unreadably compressed.
- Workspace inspector and layers become bottom sheets/drawers on compact screens.
- Playback controls remain reachable and safe-area aware.
- Touch targets are at least 44 by 44 CSS pixels.
- Map/canvas surfaces use `ResizeObserver`; layout state does not depend on fixed viewport assumptions.

Container queries are preferred for reusable components whose behavior depends on their allocated region.

## 14. Accessibility architecture

Target WCAG 2.2 AA. Every route has one main landmark and unique heading; layout navigation is labelled; route changes move focus to the page heading and announce the new title. All workflows are keyboard operable. Dialogs trap focus and restore it. Error summaries link to invalid fields. Status is never color-only. Charts and maps provide textual summaries and data-table alternatives. Timeline and playback controls expose names, values, shortcuts, and live-state changes without excessive announcements. Motion respects `prefers-reduced-motion`; autoplay is opt-in and pausable. Automated checks supplement—not replace—keyboard and screen-reader review.

## 15. Performance, code splitting, lazy loading, and bundle optimization

- Route modules are split at page boundaries; heavy editors are split again at capability boundaries.
- Cesium, charting, OCR preview, export, and rich-text/editor packages load only in routes that require them.
- Prefetch likely next-route code on intent, subject to connection/save-data signals.
- Virtualize large project, event, and telemetry lists.
- Memoize only measured hot paths; Zustand selectors must be narrow.
- Keep raw telemetry out of React render state; use typed arrays/workers and downsample for charts.
- Offload parsing, interpolation preparation, and large transformations to Web Workers.
- Lazy-load images with explicit dimensions; use optimized formats and avoid decorative bitmap payloads above the fold.
- Establish route-level bundle budgets and inspect Vite output in CI. Avoid duplicate date, icon, and utility libraries.

## 16. Future scalability and governance

The modular monolith can grow without micro-frontends. Extract a package only when it has independent consumers, ownership, or release cadence. New features require a declared owner, public API, query keys, route, accessibility notes, and tests. Architecture linting should enforce import direction and ban cross-feature deep imports. Significant decisions—router adoption, server state, Zustand, generated API contracts, authentication mechanism, Cesium boundary, worker protocol, and editor model—require ADRs before implementation.

### Definition of architectural compliance

A change is compliant when it respects dependency direction, has one state owner, does not bypass transport/adapters, handles all user-visible states, meets keyboard/accessibility requirements, keeps heavy dependencies lazy, and remains within its feature boundary.
