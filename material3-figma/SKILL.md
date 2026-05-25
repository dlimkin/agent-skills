---
name: material3-figma
description: >
  Use this skill whenever working with Material Design 3 components in Figma via the Figma MCP.
  Triggers on any request to add, insert, place, or use M3/Material 3 components, elements, or UI
  in a Figma file. Also use when asked about Material You, M3 design system components, or when
  building layouts with Material Design elements in Figma. This skill knows exact component names,
  Figma paths, variants, and properties as they appear in the official Material 3 Design Kit
  (file key: 1035203688168086460).
---

# Material 3 Figma Skill

## Purpose

This skill guides Claude in using the **official Material 3 Design Kit** for Figma (by Google) via the Figma MCP. It provides exact component names, key properties, and workflows to insert M3 components into any Figma design.

**Figma File Key:** `1035203688168086460`  
**File URL:** https://www.figma.com/community/file/1035203688168086460/material-3-design-kit

---

## How to Use Components via Figma MCP

### Workflow for inserting an M3 component:

1. **Find the component** — use `get_component` or `get_component_set` with the file key and component name from the catalog below
2. **Create an instance** — use `create_component_instance` with the correct component key
3. **Set properties/variants** — apply the variant properties listed in the catalog
4. **Position and size** — use `update_node` to set x/y and sizing

### Key MCP tools used:
- `get_file_components` — list all components in the M3 kit file
- `create_component_instance` — place a component instance on the canvas
- `set_node_properties` — adjust variant properties (State, Style, Size, etc.)
- `get_local_variables` — access M3 color tokens and typography

---

## Component Naming Convention

In the M3 Design Kit, components follow this naming pattern:
```
ComponentName / Variant
```
For example:
- `Button / Filled`
- `Card / Elevated`
- `Chip / Filter`

Properties are set using Figma component property names like `State=Enabled`, `Style=Filled`, `Leading icon=True`.

---

## Component Catalog (Quick Reference)

For full specs, see `references/components.md`.

| Category | Components |
|---|---|
| **Actions** | Button (5 styles), FAB (4 sizes), Icon Button (4 styles), Segmented Button |
| **Communication** | Badge, Progress Indicator (Linear, Circular), Snackbar |
| **Containment** | Card (3 styles), Carousel, Dialog, Divider, Bottom Sheet, Side Sheet |
| **Navigation** | Bottom App Bar, Navigation Bar, Navigation Drawer, Navigation Rail, Top App Bar, Tab |
| **Selection** | Checkbox, Date Picker, Menu, Radio Button, Slider, Switch, Time Picker |
| **Text Input** | Search Bar, Text Field (Filled, Outlined) |
| **Chips** | Assist Chip, Filter Chip, Input Chip, Suggestion Chip |
| **Lists** | List Item (1–3 lines, with various leading/trailing elements) |

---

## Design Tokens

M3 uses a structured token system. Key token categories:

**Color roles:** `md.sys.color.*`
- Primary, Secondary, Tertiary, Error
- Surface, Background, Outline
- Each has: `*`, `*-container`, `on-*`, `on-*-container`

**Typography:** `md.sys.typescale.*`
- Display (Large/Medium/Small), Headline (L/M/S), Title (L/M/S)
- Body (L/M/S), Label (L/M/S)

**Shape:** `md.sys.shape.corner.*`
- None (0), Extra Small (4dp), Small (8dp), Medium (12dp)
- Large (16dp), Extra Large (28dp), Full (50%)

**Elevation:** `md.sys.elevation.level0–5` (0, 1, 3, 6, 8, 12dp)

---

## Common Workflows

### Insert a Button
```
Component: "Button / Filled" or "Button / Outlined" etc.
Key properties:
  - State: Enabled | Hovered | Focused | Pressed | Disabled
  - Label: (text)
  - Icon: True | False
```

### Insert a Card
```
Component: "Card / Elevated" or "Card / Filled" or "Card / Outlined"
Key properties:
  - State: Enabled | Hovered | Focused | Pressed | Dragged
  - Content: (swap internal layout)
```

### Insert a Navigation Bar
```
Component: "Navigation bar"
Key properties:
  - Badge: (on individual destinations)
  - Destinations: 3–5 items
```

### Apply a Color Theme
Use M3 color token variables from the file. Light/dark mode variables are in the file's variable collections.

---

## Reference Files

- `references/components.md` — Full catalog of all 30+ components with Figma names, variants, and properties
- `references/tokens.md` — Complete design token reference (colors, typography, shape, elevation)

Read `references/components.md` when you need:
- Exact Figma component/variant names to pass to MCP tools
- All available property values for a component
- Sizing and spacing specs for a component
