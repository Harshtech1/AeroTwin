# Frontend Routing Architecture

## Canonical route map

```text
/                              Landing (public; authenticated users may continue to dashboard)
/login                         Login (public-only)
/auth                          Auth flow index/status
/auth/callback                 Identity-provider callback
/auth/verify-email             Email verification
/auth/recover                  Password recovery request
/auth/reset                    Password reset completion
/dashboard                     Dashboard (authenticated)
/projects                      Project collection (authenticated)
/projects/new                  Upload Wizard / project creation (authenticated)
/projects/:projectId           Project Detail (authenticated + project access)
/projects/:projectId/upload    Add source files / Upload Wizard
/projects/:projectId/ocr       OCR Review
/projects/:projectId/replay    Replay Workspace
/projects/:projectId/analyze   Analysis Workspace
/projects/:projectId/story     Story Editor
/library                       Library
/settings                      Settings index
/settings/profile              Profile
/settings/preferences          Preferences and accessibility
/settings/workspace            Workspace configuration
/settings/security             Security and sessions
/*                             Not Found
```

`projectId` is an opaque identifier. Routes never infer domain meaning from its shape. The parser rejects missing/invalid parameters before queries execute.

## Nested layout tree

```text
RootRoute (config, telemetry, global error boundary)
├── PublicLayout
│   └── /
├── AuthLayout
│   ├── /login
│   └── /auth/*
└── ProtectedRoute (session guard)
    ├── AppLayout (Sidebar, Topbar, outlet)
    │   ├── /dashboard
    │   ├── /projects
    │   ├── /projects/new
    │   ├── /library
    │   └── /settings/*
    └── ProjectAccessRoute (project loader + access guard)
        └── ProjectLayout (project context/header, outlet)
            ├── /projects/:projectId
            ├── /projects/:projectId/upload
            ├── /projects/:projectId/ocr
            └── WorkspaceLayout
                ├── /projects/:projectId/replay
                ├── /projects/:projectId/analyze
                └── /projects/:projectId/story
```

The project layout may visually nest inside the app shell for detail/upload/OCR, while immersive workspace routes render a full-viewport variant. This is a layout policy, not a duplicated route.

## Route responsibilities

- **Loader/guard:** parse parameters, verify session/project access, prefetch critical query, and redirect when required.
- **Page:** compose feature components and establish page metadata.
- **Error boundary:** translate not found, forbidden, offline, and unexpected failures into route-appropriate recovery.
- **Action/mutation:** remains in feature hooks unless a router action materially improves progressive flow.

Guards wait for session bootstrap. They do not flash protected content. Authorization failures show access-denied or redirect according to product policy; they are not presented as generic missing pages unless security policy requires it.

## Search parameters

Typed schemas own parsing and serialization. Unknown parameters are ignored or preserved only by explicit policy. Suggested parameters:

- Projects: `q`, `status`, `sort`, `page`.
- Project detail: `tab` only if subsections are not child routes.
- Replay: `t`, `event`, `layers`, `view` for durable deep links; high-frequency playback updates use history replacement and are throttled.
- Analysis: `metric`, `range`, `event`.
- Story: `scene`, `preview`.
- Library: `q`, `type`, `sort`, `page`.
- Login: `returnTo` restricted to same-origin internal routes.

## Navigation behavior

Route links use semantic anchors and active-state semantics. Page transitions set the document title, move focus to the route heading, and announce meaningful navigation. Back/forward restores filters and selections. Destructive or unsaved draft exits use a route blocker with accessible confirmation; blockers are limited to genuinely dirty state.

## Code splitting and prefetching

Every major page is a lazy route module. Replay, analysis, and story workspaces each form independent chunks. Vendor-heavy capabilities within them are loaded only when needed. Hover/focus/touch-intent may prefetch route code and critical query data when network conditions allow. Chunk-load failures offer one guarded reload path and preserve safe draft data where possible.

## Route access matrix

| Route family | Anonymous | Authenticated | Project access required |
|---|---:|---:|---:|
| Landing | Yes | Yes | No |
| Login/auth | Yes | Redirect/status | No |
| Dashboard/projects/library/settings | Redirect | Yes | No |
| Project detail/upload/OCR | Redirect | Yes | Yes |
| Replay/analysis/story | Redirect | Yes | Yes plus artifact readiness |

Readiness guards do not pretend incomplete processing is authorization failure. They render the relevant job/progress state and provide the valid next action.

## Not-found and legacy policy

Unknown routes render a global not-found page with safe navigation. Missing project resources render a project-aware not-found state. If route names change, maintain an explicit redirect table for published deep links; redirects replace history and preserve only validated query parameters.
