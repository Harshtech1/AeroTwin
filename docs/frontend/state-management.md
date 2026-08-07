# Frontend State Management

## Decision summary

AeroTwin uses the smallest state mechanism that satisfies ownership and lifecycle requirements. The hierarchy is: derive first, keep local second, encode in URL when shareable, use TanStack Query for server state, use Context for stable capabilities, and use Zustand only for complex client state with multiple independent consumers.

| State class | Owner | Examples |
|---|---|---|
| Server state | TanStack Query | projects, OCR results, events, stories, jobs, current user |
| Global capability | React Context | auth facade, theme, feature flags, service instances |
| Shareable navigation state | Router URL | filters, tab, selected event, time range, library query |
| High-frequency client state | Zustand | playback clock, map camera/layers, workspace panels, draft session |
| Local state | component/reducer | input value, disclosure, focused row, wizard UI before submission |

## React Context

Use Context for values that are logically ambient, stable in identity, and change infrequently. Approved contexts are authentication facade, theme, feature flags, notification dispatch, and injected service adapters. Context must not become a generic application store. Split contexts by update frequency and expose narrow hooks that throw a clear error when used outside their provider.

Do not put project collections, live playback time, map camera state, forms, or API responses in Context: those cause broad rerenders and erase lifecycle semantics.

## TanStack Query

TanStack Query is the exclusive owner of remote resources. Each feature owns:

- a hierarchical query-key factory;
- DTO-to-domain adapters;
- query option factories usable by routes and components;
- mutation options with explicit invalidation or cache reconciliation;
- stale, retention, retry, polling, and cancellation policy.

Keys use stable primitives only. Lists include normalized filters; details include resource ID/version; telemetry includes time range/resolution. Unauthorized errors never retry. Validation/conflict errors do not retry. Transient network and server errors use capped exponential backoff. Active jobs poll adaptively and stop on terminal state, loss of authorization, or when policy says background observation is unnecessary.

Prefetch in route loaders or on user intent. SSR cache hydration is not required for the initial Vite SPA, but query definitions must remain framework-agnostic enough to support it later.

## Zustand

Use separate stores by runtime concern rather than one root store:

- `playbackStore`: position, duration, rate, status, loop range, following mode;
- `mapStore`: camera intent, selected layer IDs, visibility, tool mode, selected feature;
- `workspaceStore`: panel visibility/size and inspector tab;
- `storyDraftStore`: transient ordered scenes, selection, local undo/redo metadata.

Stores expose actions and selectors, not mutable internals. High-frequency clock/camera updates must not force full-page renders. A store is reset when project identity changes, logout occurs, or the owning workspace unmounts as specified. Persist only harmless user preferences; never persist tokens, raw boarding passes, OCR payloads, or telemetry by default.

TanStack Query remains authoritative for saved stories and server jobs. Zustand may hold an editable draft with an explicit base revision and dirty flag; save mutations reconcile it.

## State by domain

### Global state

Only authentication capability, theme, notifications, feature flags, and release/config information are globally accessible. Project context is route-derived and loaded via Query rather than globally duplicated.

### Server state

Projects, files, OCR fields, reconstructions, event sets, analyses, stories, library items, and settings records use Query. Mutations either invalidate the minimum hierarchy or update cache from the authoritative response.

### Local state

Use component state for hover/focus, field visibility, non-shareable tabs, disclosure, and isolated pending intent. Use a reducer for multi-step local transitions such as a wizard before server submission. Form libraries may own field/touched/error state; do not mirror every field in Zustand.

### UI state

Transient overlays are locally owned unless launched globally. Toasts use a notification provider. Shareable filters belong in URL parameters. Workspace panel arrangement belongs in `workspaceStore`; optional persistence is namespaced and versioned.

### Playback state

The replay clock adapter produces time updates; the playback store holds control state and selected time. Server telemetry remains in Query/worker-managed buffers. Commands are deterministic: play, pause, seek, step, change rate, set loop. Reduced-motion and visibility policies can pause nonessential animation without altering saved project data.

### Map state

The map engine owns rendering internals. The map store holds serializable user intent, not Cesium objects: camera target, layer IDs, selection IDs, active tool, and display preferences. URL state may mirror selected event/time for share links. Never place viewer instances, DOM nodes, promises, or huge coordinate arrays in the store.

### Authentication state

The current session is server state in Query. Context exposes `user`, `status`, `login`, `logout`, and capability checks without duplicating the response. Sensitive credentials remain in HTTP-only cookies. Logout coordinates query cache clearing and store resets.

## Consistency and concurrency

- Mutations carry entity revision/version where backend support exists.
- Conflict responses present a compare/reload path rather than silently overwriting.
- Story autosave is debounced, serialized, and revision-aware.
- Route changes cancel irrelevant in-flight reads through `AbortSignal`.
- Project switches reset project-scoped stores before rendering the next workspace.
- Derived data is selected/memoized; it is not synchronized through effects.

## Testing

Test pure store actions and selectors without React, Query behavior with a fresh QueryClient per test, and Context facades through public hooks. Integration tests verify logout clearing, project switching, optimistic rollback, job polling termination, and URL restoration. Tests use API contract fixtures at the transport boundary rather than mocking implementation hooks.
