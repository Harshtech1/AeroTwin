# AeroTwin UI Component Inventory

## Library conventions

All components use typed public props, forward relevant refs, accept semantic attributes, and support controlled/uncontrolled use only where that distinction is intentional. Visual styling uses design tokens. “Dependencies” names conceptual primitives or approved libraries, not an instruction to install packages. Components must meet WCAG 2.2 AA, preserve visible focus, support zoom/reflow, and respect reduced motion.

## Actions and containers

### Button
- **Props:** `children`, `variant`, `size`, `type`, `disabled`, `loading`, `leadingIcon`, `trailingIcon`, native button attributes; IconButton additionally requires `accessibleLabel`.
- **Variants:** primary, secondary, outline, ghost, destructive, link; icon-only.
- **States:** default, hover, active, focus-visible, disabled, pending.
- **Accessibility:** Semantic button; loading retains name, exposes busy state, and prevents duplicate submission; icon-only always named; minimum touch target.
- **Dependencies:** shadcn Button foundation, icon system, Spinner.

### Card
- **Props:** `as`, header/title/description, footer/actions, interactive, selected, children.
- **Variants:** surface, elevated, outlined, muted, metric, interactive.
- **States:** default, hover/focus for interactive, selected, disabled, loading.
- **Accessibility:** Not interactive by default; interactive card has one semantic target and avoids nested controls; heading level is caller-owned.
- **Dependencies:** design tokens, optional Skeleton.

### Dialog and Modals
- **Props:** `open`, `onOpenChange`, title, description, children, footer, initialFocus, size, dismissPolicy.
- **Variants:** standard dialog, confirmation, destructive confirmation, full-screen compact modal, alert dialog.
- **States:** opening, open, pending action, error, closing.
- **Accessibility:** Label/description, focus trap and return, Escape policy, inert background, no click-away for destructive/pending operations, scroll containment.
- **Dependencies:** Radix/shadcn Dialog or AlertDialog, Button, ErrorMessage. “Modal” is a usage pattern over these primitives, not a second competing implementation.

## Data display

### Table
- **Props:** typed columns/rows, row key, caption, sort, selection, pagination, row action, density, empty/loading/error renderers.
- **Variants:** standard, compact, selectable, virtualized.
- **States:** loading, empty, populated, sorted, selected, refreshing, error.
- **Accessibility:** Semantic table and caption; sortable headers announce state; selection controls named; keyboard support for interactive grids only when grid behavior is truly needed; compact alternative on narrow screens.
- **Dependencies:** table model such as TanStack Table, Checkbox, Pagination, Skeleton.

### Charts
- **Props:** series, axes, units, domain/range, interaction callbacks, annotations, legend, accessible title/description, tabular fallback.
- **Variants:** line, area, scatter, altitude profile, weather band, compact sparkline.
- **States:** loading, no data, partial, interactive selection, error.
- **Accessibility:** Text summary and data-table/download alternative; patterns/labels beyond color; keyboard-accessible inspection where feasible; tooltips not pointer-only.
- **Dependencies:** selected chart adapter, ResizeObserver, design tokens; adapter prevents vendor types leaking into features.

### Badge
- **Props:** children, tone, size, icon.
- **Variants:** neutral, info, positive, caution, critical, accent.
- **States:** static; optional removable only as a separate chip pattern.
- **Accessibility:** Text conveys meaning; decorative icon hidden; never sole status signal.
- **Dependencies:** tokens, Icon.

### Status Chip
- **Props:** status enum, label override, size, showIcon.
- **Variants:** project/job/OCR/story semantic mappings.
- **States:** queued, running, ready, needs-review, failed, paused, archived and domain-approved additions.
- **Accessibility:** Human-readable text and icon; animated running state respects reduced motion; status changes announced only when actionable.
- **Dependencies:** Badge, status-to-presentation mapping.

### Event Card
- **Props:** event ID/type/title/time/severity/summary, selected, onSelect, actions.
- **Variants:** compact timeline, detailed inspector, anomaly, milestone.
- **States:** default, selected, acknowledged, loading details, unavailable.
- **Accessibility:** Semantic time, explicit severity text, one clear selection control, actions independently named.
- **Dependencies:** Card, StatusChip, Icon, time formatter.

### Story Card
- **Props:** story/scene identity, title, thumbnail, duration, status, modified time, actions, draggable metadata when editor-owned.
- **Variants:** library, scene, template, compact.
- **States:** draft, saved, publishing, published, failed, selected, dragging.
- **Accessibility:** Image alternative, status text, keyboard reordering with announcements, menu named by story/scene.
- **Dependencies:** Card, StatusChip, Menu, aspect-ratio media.

## Navigation and workspace structure

### Sidebar
- **Props:** navigation groups/items, active item, collapsed/open state, user/workspace slot, onNavigate.
- **Variants:** persistent wide, collapsed rail, compact drawer.
- **States:** open, collapsed, overlay, item active/disabled/badged.
- **Accessibility:** `nav` with label, semantic links and `aria-current`, drawer focus management, active state not color-only.
- **Dependencies:** Router link, Drawer/Sheet, Icon, Tooltip.

### Topbar
- **Props:** title/breadcrumb slot, search, actions, notification/user menus, mobile navigation trigger.
- **Variants:** application, project, workspace/minimal.
- **States:** normal, search expanded, menus open, offline/job indicator.
- **Accessibility:** Header landmark; labelled controls; menus keyboard operable; logical focus order.
- **Dependencies:** Button, Menu, SearchField, Breadcrumbs, Notifications.

### Inspector
- **Props:** title, tabs/sections, open, width, onResize/onClose, footer, selection context.
- **Variants:** right panel, left panel, compact bottom sheet, read-only/editor.
- **States:** empty selection, populated, loading, error, resizing, collapsed.
- **Accessibility:** Complementary landmark with label; focus moves only on explicit open intent; resize has keyboard alternative; sheet follows dialog semantics when modal.
- **Dependencies:** Tabs, Accordion, ResizablePanel adapter, Sheet, EmptyState.

### Timeline
- **Props:** duration/range, current time, tracks, events, selection, zoom, onSeek/onRangeChange, formatters.
- **Variants:** replay, event-only, story, compact scrubber.
- **States:** loading, ready, playing, seeking, zoomed, range-selected, disabled.
- **Accessibility:** Slider semantics for playhead, keyboard step/page/home/end, announced formatted value, event list alternative, adequate target sizes.
- **Dependencies:** playback state contract, virtualized track renderer where needed, Tooltip.

### Playback Controls
- **Props:** status, currentTime, duration, rate, loop, capabilities, command callbacks.
- **Variants:** full, compact, story preview.
- **States:** idle, loading/buffering, playing, paused, ended, error, disabled.
- **Accessibility:** Every icon control named; play/pause state conveyed; shortcuts documented and avoid form conflicts; time exposed as text; motion/autoplay user-controlled.
- **Dependencies:** Button/IconButton, Slider, Select, playback store facade.

### Map Controls
- **Props:** available tools, active tool, compass/camera state, onCommand, disabled reasons.
- **Variants:** standard stack, compact dock, keyboard palette.
- **States:** inactive, active tool, disabled/unavailable, loading terrain/layer.
- **Accessibility:** Named buttons with tool pressed state; keyboard equivalents; non-map alternative for essential information.
- **Dependencies:** Button, Tooltip, engine port—not Cesium types.

### Layer Manager
- **Props:** layer tree, visibility, opacity, order, availability, callbacks.
- **Variants:** inspector section, floating panel, compact sheet.
- **States:** loading, visible/hidden, partially visible group, unavailable, reordering.
- **Accessibility:** Hierarchical labels, checkbox semantics, keyboard reorder, numeric opacity control, unavailable reason.
- **Dependencies:** Checkbox, Slider, Tree/Accordion, drag-and-drop adapter with keyboard support.

## Forms

### Form primitives
- **Props:** common `name`, `label`, `description`, `required`, `disabled`, `error`, control-specific value/default and change/blur props.
- **Variants:** TextField, TextArea, Select/Combobox, Checkbox, RadioGroup, Switch, Date/Time, FilePicker, SearchField.
- **States:** pristine, focused, dirty, invalid, disabled, read-only, pending.
- **Accessibility:** Explicit label/control association; description and error IDs; required/invalid semantics; error summary; autocomplete/input mode; no placeholder-only labels.
- **Dependencies:** shadcn/Radix primitives, form adapter, validation schema.

### Notifications
- **Props:** title, description, tone, action, duration, persistent, onDismiss.
- **Variants:** toast, inline alert, banner, notification-center item.
- **States:** info, success, caution, critical, pending/offline.
- **Accessibility:** Polite status for routine updates, alert only for urgent failures; pause timeout on hover/focus; persistent access to consequential notices; dismiss named.
- **Dependencies:** Toast/Alert primitive, notification provider.

### Progress
- **Props:** value/max or indeterminate, label, detail, status, cancellable action.
- **Variants:** bar, circular, step progress, job progress, upload row.
- **States:** queued, indeterminate, progressing, paused, complete, failed, cancelled.
- **Accessibility:** Native/ARIA progress semantics, visible label and value where meaningful, terminal text; animation reduced.
- **Dependencies:** Progress primitive, StatusChip.

## Feedback states

### Skeleton Loader
- **Props:** shape, lines/count, dimensions, accessible label at containing region.
- **Variants:** text, card, table/list row, chart, workspace.
- **States:** loading only.
- **Accessibility:** Decorative skeletons hidden; container exposes one loading status; no rapid shimmer under reduced motion; geometry matches final layout.
- **Dependencies:** tokens and reduced-motion preference.

### Error State
- **Props:** category, title, message, requestId, primary/secondary recovery actions, details policy.
- **Variants:** inline, card, page, route crash, offline, forbidden, not found.
- **States:** recoverable, retrying, terminal.
- **Accessibility:** Appropriate heading, actionable controls, focus on route-level errors, safe copyable request ID; no raw stack or sensitive data.
- **Dependencies:** Alert, Button, normalized error model.

### Empty State
- **Props:** title, description, illustration/icon, primary/secondary action, contextual help.
- **Variants:** first-use, filtered-no-results, no-selection, no-permission-content.
- **States:** static.
- **Accessibility:** Clear heading and next action; decorative art hidden; filtered state explains reset behavior.
- **Dependencies:** Button, Icon/approved illustration.

## Accessibility helpers

### VisuallyHidden
- **Props:** children, focusable option only for skip links.
- **Variants:** visually hidden content, SkipLink.
- **States:** SkipLink becomes visible on focus.
- **Accessibility:** Must remain in accessibility tree and avoid clipping bugs.
- **Dependencies:** CSS utility.

### LiveRegion
- **Props:** message, politeness, atomic, clear delay.
- **Variants:** polite status, assertive error.
- **States:** idle/announcing.
- **Accessibility:** Deduplicate messages; never announce high-frequency playback ticks.
- **Dependencies:** none.

### Focus and keyboard helpers
- **Props:** focus target/reference, shortcut definition, scope, enabled state.
- **Variants:** FocusReturn, RouteFocusManager, KeyboardShortcut, FocusTrap via dialog primitives.
- **States:** active/inactive scope.
- **Accessibility:** Never steal focus on background refresh; shortcuts are discoverable, remappable where required, and inactive during text entry unless explicitly safe.
- **Dependencies:** router, dialog primitives, stable event hook.

## Ownership and extension rules

Shared components contain no Project, Flight, OCR, or Story API calls. Domain wrappers map entity data into shared props. New variants require design-system review; arbitrary boolean combinations are rejected in favor of explicit variants. Every component ships with representative states, keyboard tests, automated accessibility checks, and responsive documentation before it is considered stable.
