# material3-figma

> Claude skill for working with the [Material 3 Design Kit](https://www.figma.com/community/file/1035203688168086460/material-3-design-kit) in Figma

Gives Claude expert knowledge of Google's official Material Design 3 component library for Figma. Covers the full component catalog with exact Figma names, variant properties, design tokens, and idiomatic workflows for inserting and configuring M3 components via the Figma MCP.

---

## Installation

```bash
npx skills add dlimkin/agent-skills --skill material3-figma
```

---

## What the skill covers

Claude applies the skill automatically whenever Material Design 3 or M3 components are mentioned in a Figma context — no explicit invocation needed.

### Actions
- Buttons — Filled, Filled Tonal, Elevated, Outlined, Text (all states)
- FAB — Small, Standard, Large, Extended (all color variants)
- Icon Buttons — Standard, Filled, Filled Tonal, Outlined
- Segmented Button — 2–5 options, per-segment selection

### Containment
- Cards — Elevated, Filled, Outlined (all interaction states)
- Dialogs — Basic, Full-screen
- Bottom Sheets and Side Sheets — Modal and Standard
- Carousel — Hero, Multi-browse, Uncontained

### Chips
- Assist, Filter, Input, Suggestion chips
- Leading/trailing icons, selected state, elevated variant

### Lists
- 1-, 2-, and 3-line items
- Leading elements — Icon, Avatar, Image, Video, Checkbox, Radio, Switch
- Trailing elements — Icon, Text, Checkbox, Radio, Switch

### Navigation
- Bottom App Bar, Navigation Bar, Navigation Drawer (Modal + Standard)
- Navigation Rail, Top App Bar (Small, Center, Medium, Large)
- Tabs — Primary and Secondary, with icon and badge support

### Selection & Input
- Checkbox, Radio Button, Switch, Slider (Continuous, Discrete, Range)
- Text Fields — Filled and Outlined, with all state and icon combos
- Date Pickers — Docked, Modal, Modal Input, Date Range
- Time Pickers — Dial and Input
- Search Bar and Search View
- Menus and Menu Items

### Communication
- Badges — Small (dot) and Large (count)
- Progress Indicators — Linear and Circular, Determinate and Indeterminate
- Snackbar — 1-line and 2-line, with action and icon

### Design Tokens
- All 29+ color roles (`md.sys.color.*`) with light/dark baseline values
- Full 15-style typography scale (`md.sys.typescale.*`)
- Shape corner tokens — None through Full (0dp → 50%)
- Elevation levels 0–5 and state layer opacities

---

## Skill structure

```
material3-figma/
├── SKILL.md                          # Overview, MCP workflow, quick reference tables
└── references/
    ├── components.md                 # Full catalog — Figma names, variants, properties, specs
    └── tokens.md                     # Color roles, typography scale, shape, elevation, layout grid
```

---

## Example prompts

```
Add a filled button with an icon to the current Figma frame
```

```
Insert a navigation bar with 4 destinations, second one active
```

```
Place an outlined text field with error state and supporting text
```

```
What are the exact variant properties for a filter chip in selected state?
```

```
Add an elevated card and set corner radius using the correct M3 shape token
```

---

## Compatibility

| | |
|---|---|
| Figma file | [Material 3 Design Kit](https://www.figma.com/community/file/1035203688168086460) |
| File key | `1035203688168086460` |
| Integration | Figma MCP |
| Design system | [m3.material.io](https://m3.material.io/components) |
| Maintained by | Google |
