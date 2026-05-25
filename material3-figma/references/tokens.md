# Material 3 Design Tokens — Figma Reference

## Color System

### Color Roles (md.sys.color)

| Role | Light value (baseline) | Usage |
|---|---|---|
| `primary` | #6750A4 | Key UI elements, buttons |
| `on-primary` | #FFFFFF | Text/icons on primary |
| `primary-container` | #EADDFF | Containers with less emphasis |
| `on-primary-container` | #21005D | Text on primary container |
| `secondary` | #625B71 | Less prominent elements |
| `on-secondary` | #FFFFFF | Text/icons on secondary |
| `secondary-container` | #E8DEF8 | Secondary containers |
| `on-secondary-container` | #1D192B | Text on secondary container |
| `tertiary` | #7D5260 | Contrasting accents |
| `on-tertiary` | #FFFFFF | Text/icons on tertiary |
| `tertiary-container` | #FFD8E4 | Tertiary containers |
| `on-tertiary-container` | #31111D | Text on tertiary container |
| `error` | #B3261E | Error states |
| `on-error` | #FFFFFF | Text/icons on error |
| `error-container` | #F9DEDC | Error containers |
| `on-error-container` | #410E0B | Text on error container |
| `background` | #FFFBFE | Page background |
| `on-background` | #1C1B1F | Text on background |
| `surface` | #FFFBFE | Card, sheet surfaces |
| `on-surface` | #1C1B1F | Text on surface |
| `surface-variant` | #E7E0EC | Alternative surfaces |
| `on-surface-variant` | #49454F | Text on surface variant |
| `outline` | #79747E | Borders, dividers |
| `outline-variant` | #CAC4D0 | Subtle borders |
| `inverse-surface` | #313033 | Snackbar background |
| `inverse-on-surface` | #F4EFF4 | Text on inverse surface |
| `inverse-primary` | #D0BCFF | Links on inverse surface |
| `shadow` | #000000 | Shadows |
| `scrim` | #000000 | Overlay/modal scrim |

### Figma Variable Collection Names
- `Light theme` / `Dark theme` — mode-specific color values
- Token path in Figma: `Material Theme / md.sys.color / [role]`

---

## Typography Scale (md.sys.typescale)

| Style | Font | Weight | Size | Line height | Letter spacing |
|---|---|---|---|---|---|
| `display-large` | Roboto | 400 | 57sp | 64sp | -0.25px |
| `display-medium` | Roboto | 400 | 45sp | 52sp | 0 |
| `display-small` | Roboto | 400 | 36sp | 44sp | 0 |
| `headline-large` | Roboto | 400 | 32sp | 40sp | 0 |
| `headline-medium` | Roboto | 400 | 28sp | 36sp | 0 |
| `headline-small` | Roboto | 400 | 24sp | 32sp | 0 |
| `title-large` | Roboto | 400 | 22sp | 28sp | 0 |
| `title-medium` | Roboto | 500 | 16sp | 24sp | +0.15px |
| `title-small` | Roboto | 500 | 14sp | 20sp | +0.1px |
| `body-large` | Roboto | 400 | 16sp | 24sp | +0.5px |
| `body-medium` | Roboto | 400 | 14sp | 20sp | +0.25px |
| `body-small` | Roboto | 400 | 12sp | 16sp | +0.4px |
| `label-large` | Roboto | 500 | 14sp | 20sp | +0.1px |
| `label-medium` | Roboto | 500 | 12sp | 16sp | +0.5px |
| `label-small` | Roboto | 500 | 11sp | 16sp | +0.5px |

---

## Shape System (md.sys.shape)

| Token | Corner radius | Used on |
|---|---|---|
| `corner-none` | 0dp | — |
| `corner-extra-small` | 4dp | Menus, snackbars, text fields |
| `corner-extra-small-top` | 4dp top only | Filled text field |
| `corner-small` | 8dp | Chips, rich tooltips |
| `corner-medium` | 12dp | Cards, small FAB |
| `corner-large` | 16dp | Navigation drawer, FAB, carousel items |
| `corner-extra-large` | 28dp | Large FAB, dialogs, bottom sheets |
| `corner-full` | 50% | Buttons, badges, sliders, search bar |

---

## Elevation (md.sys.elevation)

| Level | dp value | Used on |
|---|---|---|
| `level0` | 0dp | Flat surfaces (filled card, bottom sheet) |
| `level1` | 1dp | Elevated card, nav drawer |
| `level2` | 3dp | FAB (resting) |
| `level3` | 6dp | FAB (pressed), dialogs |
| `level4` | 8dp | Navigation bar, bottom app bar |
| `level5` | 12dp | Top app bar (scrolled) |

---

## State Layer Opacity

| State | Opacity |
|---|---|
| Hover | 8% |
| Focus | 12% |
| Press | 12% |
| Drag | 16% |
| Disabled container | 12% |
| Disabled content | 38% |

---

## Spacing & Layout Grid

| Breakpoint | Width | Columns | Gutters | Margins |
|---|---|---|---|---|
| Compact (phone) | 0–599dp | 4 | 16dp | 16dp |
| Medium (tablet) | 600–1239dp | 8 or 12 | 24dp | 24dp |
| Expanded (desktop) | 1240dp+ | 12 | 24dp | 24dp |
