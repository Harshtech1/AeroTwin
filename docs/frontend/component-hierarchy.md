# AeroTwin Page and Component Hierarchy

This document assigns clear composition and state ownership to each Product Experience Blueprint page. Names describe contracts, not required implementation names. “API dependencies” identifies future frontend resource contracts; Sprint 3 uses fixtures and does not call them.

## Shared layout hierarchy

- **PublicLayout:** brand header, public footer, main content, consent/legal surfaces.
- **AuthLayout:** minimal brand context, centered auth panel, support link, auth status region.
- **AppLayout:** responsive Sidebar, Topbar, notification region, page main, route outlet.
- **ProjectLayout:** project identity/header, readiness/status, project navigation, route outlet.
- **WorkspaceLayout:** workspace header, primary canvas, timeline/control region, inspector/layer region, responsive drawers.

## Landing

- **Purpose:** Explain AeroTwin’s value and guide visitors to authenticate or continue into the product.
- **Parent Layout:** PublicLayout.
- **Child Components:** Hero, ProductValueGrid, WorkflowOverview, CapabilityPreview, Trust/ResearchStatement, PrimaryCallToAction, PublicFooter.
- **Shared Components:** Button, Card, Badge, responsive media, section container.
- **State:** Local disclosure/media state; session presence only to alter the primary destination.
- **API Dependencies:** Optional current-session resource; otherwise none.
- **Future Extensions:** Public demos, case studies, documentation, release highlights. Marketing content must remain separable from authenticated application bundles.

## Dashboard

- **Purpose:** Give an authenticated user a prioritized overview and rapid re-entry into active work.
- **Parent Layout:** AppLayout.
- **Child Components:** WelcomeHeader, ProjectSummaryMetrics, RecentProjects/Flights, ActiveJobPanel, InsightCard, StorageSummary, QuickActions.
- **Shared Components:** StatCard, ProjectCard/Row, StatusChip, Progress, Button, EmptyState, Skeleton.
- **State:** Query-owned dashboard aggregate; URL or local state for simple view preference; no duplicate project cache.
- **API Dependencies:** Current user, dashboard summary, recent projects, active jobs, quota/storage.
- **Future Extensions:** Role-specific widgets, pinned projects, system notices, AI insight explanations.

## Projects

- **Purpose:** Find, filter, sort, create, and manage flight reconstruction projects.
- **Parent Layout:** AppLayout.
- **Child Components:** ProjectsHeader, SearchAndFilters, ProjectViewToggle, ProjectTable/ProjectGrid, BulkActionBar, Pagination, CreateProjectAction.
- **Shared Components:** SearchField, Select, FilterChip, Table, ProjectCard, StatusChip, Dialog, EmptyState, ErrorState, Skeleton.
- **State:** Filters/sort/page/view in validated URL parameters; selection local unless bulk actions cross panels; resources in Query.
- **API Dependencies:** Paginated project collection, project summary statuses, create/rename/archive/delete mutations.
- **Future Extensions:** Shared projects, organizations, saved filters, advanced bulk operations, audit metadata.

## Project Detail

- **Purpose:** Present project identity, source artifacts, processing readiness, milestones, and next valid action.
- **Parent Layout:** ProjectLayout inside AppLayout.
- **Child Components:** ProjectHeader, ProjectStatusSummary, SourceAssetList, ProcessingPipeline, FlightMetadataSummary, ActivityFeed, NextActionPanel.
- **Shared Components:** Breadcrumbs, Card, StatusChip, Progress, Timeline, FileRow, EventCard, Dialog.
- **State:** Project ID from route; project/artifacts/jobs in Query; ephemeral action/dialog state local.
- **API Dependencies:** Project detail, assets, jobs, reconstruction summary, project activity; rename/archive/delete/retry mutations.
- **Future Extensions:** Collaboration, comments, versions, comparison, permissions, export history.

## Upload Wizard

- **Purpose:** Create or enrich a project by safely collecting boarding passes, flight files, and metadata.
- **Parent Layout:** AppLayout for new project; ProjectLayout for adding to an existing project.
- **Child Components:** WizardStepper, SourceTypeChoice, Dropzone, FileQueue, MetadataForm, ValidationSummary, UploadProgress, ReviewAndSubmit, CompletionState.
- **Shared Components:** Form controls, FilePicker, Progress, Alert, Dialog, Button, Stepper, ErrorSummary.
- **State:** Local reducer/form state for steps and unsent metadata; upload task service for progress/cancel; created resources/jobs in Query.
- **API Dependencies:** Upload initialization, multipart/chunk operations, completion, project creation, job status.
- **Future Extensions:** Cloud imports, batch ingestion, camera capture, resumable cross-session upload, checksum deduplication.

## OCR Review

- **Purpose:** Let users verify low-confidence extracted boarding-pass information against its visual source before reconstruction.
- **Parent Layout:** ProjectLayout.
- **Child Components:** OCRReviewHeader, SourceViewer, PageThumbnailRail, FieldGroupList, OCRFieldEditor, ConfidenceLegend, ValidationSummary, ReviewProgress, SubmitCorrectionsBar.
- **Shared Components:** Inspector, Form fields, StatusChip, Badge, SplitPane, ZoomControls, Skeleton, ErrorState, UnsavedChangesDialog.
- **State:** OCR resource in Query; correction draft and field selection in a feature-local store/form; zoom/pan local or viewer adapter state.
- **API Dependencies:** OCR result/pages/field provenance, correction submission, reprocess/status mutation.
- **Future Extensions:** Bounding-box editing, multi-document merge, reviewer assignment, correction audit trail, model feedback.

## Replay Workspace

- **Purpose:** Replay a reconstructed flight against synchronized time, telemetry, events, and geospatial context.
- **Parent Layout:** WorkspaceLayout under ProjectLayout.
- **Child Components:** ReplayCanvas/MapAdapter, PlaybackControls, Timeline, EventTrack, TelemetryOverlay, LayerManager, MapControls, CameraModeControl, ReplayInspector, WorkspaceHeader.
- **Shared Components:** Inspector, Drawer, Tooltip, StatusChip, Progress, EventCard, KeyboardShortcutHelp, ErrorState.
- **State:** Project and artifacts in Query; playbackStore for clock/control; mapStore for serializable view intent; selected event/time may be URL-backed; engine internals remain in adapter.
- **API Dependencies:** Reconstruction manifest, trajectory segments, event set, environmental layers, processing status.
- **Future Extensions:** Cesium renderer, weather/terrain, comparisons, annotations, camera tracks, synchronized narration and audio.

## Analysis Workspace

- **Purpose:** Explore flight metrics, anomalies, environment, and events with synchronized visual evidence.
- **Parent Layout:** WorkspaceLayout under ProjectLayout.
- **Child Components:** AnalysisToolbar, MetricSelector, ChartGrid, SynchronizedChart, EventList, MapContextPanel, AnalysisInspector, RangeBrush, ExportAction.
- **Shared Components:** ChartFrame, Legend, Timeline, EventCard, Table, Filter controls, Skeleton, ErrorState.
- **State:** Query for analysis series/events; range, metric, event in URL; chart hover local; map/playback coordination in scoped stores where needed.
- **API Dependencies:** Analysis manifest, downsampled metric series, event/anomaly details, export job.
- **Future Extensions:** Custom calculations, saved views, comparison, annotations, notebook/report export, AI explanations.

## Story Editor

- **Purpose:** Arrange selected events, camera perspectives, annotations, and narration into an authored flight story.
- **Parent Layout:** WorkspaceLayout under ProjectLayout.
- **Child Components:** StoryOutline, SceneList, StoryCanvas/Preview, SceneInspector, NarrationEditor, AssetPicker, StoryPlaybackControls, SaveStatus, Publish/ExportDialog.
- **Shared Components:** StoryCard, Inspector, Timeline, Form controls, Dialog, Progress, Notification, EmptyState.
- **State:** Saved story/revision in Query; editable draft, selection, ordering, undo/redo in storyDraftStore; preview playback in playbackStore; dirty state blocks unsafe exit.
- **API Dependencies:** Story detail/version, project events/assets, save/publish/export mutations and job status.
- **Future Extensions:** AI narration, collaboration, templates, voice selection, branching stories, revision history, video export.

## Library

- **Purpose:** Browse reusable projects, stories, exports, templates, and other saved artifacts according to product policy.
- **Parent Layout:** AppLayout.
- **Child Components:** LibraryHeader, SearchAndFilters, CollectionTabs, AssetGrid/List, AssetPreview, MetadataInspector, BulkActions, Pagination.
- **Shared Components:** SearchField, FilterChip, Card, Table, Badge, StatusChip, Dialog, EmptyState, Skeleton.
- **State:** Search/filter/sort/page in URL; resources in Query; preview selection local or URL-backed when shareable.
- **API Dependencies:** Paginated library collection, asset metadata, favorite/tag/archive/download mutations.
- **Future Extensions:** Shared collections, templates marketplace, organization assets, licensing, semantic search.

## Settings

- **Purpose:** Manage personal identity, accessibility preferences, workspace defaults, security, storage, and integrations.
- **Parent Layout:** AppLayout with nested settings navigation.
- **Child Components:** SettingsNavigation, ProfileForm, PreferenceForm, AccessibilityPreferences, WorkspaceDefaults, SecuritySessions, StorageManagement, IntegrationList.
- **Shared Components:** Form controls, Card, Tabs/side navigation, Switch, Dialog, Alert, SaveBar, Skeleton.
- **State:** Settings resources in Query; form drafts local; theme/accessibility Context reflects confirmed preferences; URL selects subsection.
- **API Dependencies:** User profile/preferences, workspace settings, active sessions, storage quota, integrations; update/revoke mutations.
- **Future Extensions:** Teams/roles, billing, data retention, API keys, notification rules, enterprise policy controls.

## Authentication

- **Purpose:** Establish, recover, verify, and terminate a secure user session.
- **Parent Layout:** AuthLayout; callback/status screens may use a minimal RootLayout.
- **Child Components:** LoginForm, PasswordField, IdentityProviderButtons, RecoveryForm, ResetForm, VerificationStatus, AuthError, LegalLinks.
- **Shared Components:** Form controls, Button, Alert, Progress, PasswordRequirements, Accessibility announcements.
- **State:** Session resource in Query exposed through Auth Context; form/touched/errors local; safe `returnTo` in URL.
- **API Dependencies:** Session, login, logout, provider callback, recovery, reset, verification.
- **Future Extensions:** MFA/passkeys, SSO, invitations, step-up authentication, device trust.

## Composition constraints

- Page modules compose; they do not become component libraries.
- A child used by two features is promoted only after its domain assumptions are removed.
- Workspace components communicate through explicit state/actions and engine ports, not component refs spanning siblings.
- Every page must define populated, initial-loading, background-refresh, empty, offline, forbidden, not-found, and unexpected-error behavior where applicable.
