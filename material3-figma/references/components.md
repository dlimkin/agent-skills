# Material 3 Component Catalog — Figma Names & Properties

Source: Official M3 Design Kit (file key: `1035203688168086460`)

## Table of Contents

1. [Buttons](#buttons)
2. [FAB (Floating Action Button)](#fab)
3. [Icon Button](#icon-button)
4. [Segmented Button](#segmented-button)
5. [Cards](#cards)
6. [Chips](#chips)
7. [Lists](#lists)
8. [Navigation](#navigation)
9. [Text Fields](#text-fields)
10. [Selection Controls](#selection-controls)
11. [Dialogs & Sheets](#dialogs--sheets)
12. [Progress Indicators](#progress-indicators)
13. [Communication](#communication)
14. [Date & Time Pickers](#date--time-pickers)
15. [Menus](#menus)
16. [Tabs](#tabs)
17. [Search](#search)
18. [Divider](#divider)
19. [Carousel](#carousel)

---

## Buttons

### Common Button (5 styles)

**Figma component names:**
- `Button / Filled`
- `Button / Filled tonal`
- `Button / Elevated`
- `Button / Outlined`
- `Button / Text`

**Properties:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Icon | `True`, `False` |
| Label text | (string) |

**Specs:**
- Height: 40dp
- Corner radius: Full (20dp)
- Min width: 48dp, Horizontal padding: 24dp (16dp with icon)
- Icon size: 18dp

---

## FAB

### Floating Action Button

**Figma component names:**
- `FAB / Small` — 40dp
- `FAB / FAB` (Medium/Standard) — 56dp
- `FAB / Large` — 96dp
- `FAB / Extended FAB` — 56dp height, variable width

**Properties:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed` |
| Color | `Surface`, `Primary`, `Secondary`, `Tertiary` |
| Icon | (swap component) |
| Label text (Extended only) | (string) |

**Corner radius:**
- Small: 12dp (Medium shape)
- FAB: 16dp (Large shape)
- Large: 28dp (Extra Large shape)
- Extended: 16dp (Large shape)

---

## Icon Button

**Figma component names:**
- `Icon button / Standard`
- `Icon button / Filled`
- `Icon button / Filled tonal`
- `Icon button / Outlined`

**Properties:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Selected | `True`, `False` |
| Icon | (swap component) |

**Specs:**
- Size: 40×40dp
- Icon size: 24dp

---

## Segmented Button

**Figma component names:**
- `Segmented button / 2-option`
- `Segmented button / 3-option`
- `Segmented button / 4-option`
- `Segmented button / 5-option`

**Properties:**
| Property | Values |
|---|---|
| State (per segment) | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Selected (per segment) | `True`, `False` |
| Icon (per segment) | `True`, `False` |
| Label (per segment) | (string) |

**Specs:**
- Height: 40dp
- Corner radius: Full (20dp)

---

## Cards

**Figma component names:**
- `Card / Elevated`
- `Card / Filled`
- `Card / Outlined`

**Properties:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Dragged`, `Disabled` |

**Specs:**
- Corner radius: 12dp (Medium shape)
- Padding: 16dp
- Elevated: elevation level 1 (1dp shadow)
- Outlined: 1dp border (Outline color token)

---

## Chips

### Assist Chip
**Figma component name:** `Chip / Assist`

### Filter Chip
**Figma component name:** `Chip / Filter`

### Input Chip
**Figma component name:** `Chip / Input`

### Suggestion Chip
**Figma component name:** `Chip / Suggestion`

**Properties (all chip types):**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Selected (Filter/Input) | `True`, `False` |
| Leading icon | `True`, `False` |
| Trailing icon (Input) | `True`, `False` |
| Elevated (Assist/Suggestion) | `True`, `False` |
| Label | (string) |

**Specs:**
- Height: 32dp
- Corner radius: Full (16dp)
- Horizontal padding: 16dp (8dp with icon)
- Icon size: 18dp

---

## Lists

**Figma component name:** `List item`

**Properties:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Lines | `1-line`, `2-line`, `3-line` |
| Leading | `None`, `Icon`, `Avatar`, `Image`, `Video`, `Checkbox`, `Radio button`, `Switch` |
| Trailing | `None`, `Icon`, `Text`, `Checkbox`, `Radio button`, `Switch` |
| Overline | `True`, `False` |

**Specs:**
- 1-line height: 56dp
- 2-line height: 72dp
- 3-line height: 88dp
- Horizontal padding: 16dp
- Leading/trailing element size: 24dp (icon)

---

## Navigation

### Bottom App Bar
**Figma component name:** `Bottom app bar`

**Properties:**
| Property | Values |
|---|---|
| FAB | `True`, `False` |
| Action 1–4 | icon swap |

**Specs:**
- Height: 80dp
- FAB: 56dp

---

### Navigation Bar
**Figma component name:** `Navigation bar`

**Properties:**
| Property | Values |
|---|---|
| Destinations | 3, 4, or 5 destination items |
| Active destination | (which tab is selected) |

**Per destination item properties:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Active | `True`, `False` |
| Badge | `None`, `Small`, `Large` |
| Label | (string) |
| Icon | (swap) |

**Specs:**
- Height: 80dp
- Active indicator: 64×32dp pill
- Icon size: 24dp

---

### Navigation Drawer
**Figma component names:**
- `Navigation drawer / Modal` — overlays content
- `Navigation drawer / Standard` — side by side with content

**Properties:**
| Property | Values |
|---|---|
| Header | `True`, `False` |

**Per destination item:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Active | `True`, `False` |
| Badge | `None`, `Small`, `Large` |
| Leading icon | `True`, `False` |
| Trailing icon | `True`, `False` |

**Specs:**
- Width: 360dp
- Corner radius (modal): 0dp left, 16dp right

---

### Navigation Rail
**Figma component name:** `Navigation rail`

**Properties:**
| Property | Values |
|---|---|
| FAB | `True`, `False` |
| Menu icon | `True`, `False` |

**Per destination:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed` |
| Active | `True`, `False` |
| Badge | `None`, `Small`, `Large` |
| Label | (string) |

**Specs:**
- Width: 80dp
- Active indicator: 56×32dp pill

---

### Top App Bar
**Figma component names:**
- `Top app bar / Center-aligned`
- `Top app bar / Small`
- `Top app bar / Medium`
- `Top app bar / Large`

**Properties:**
| Property | Values |
|---|---|
| Scroll state | `Default`, `Scrolled` |
| Leading icon | `True`, `False` |
| Trailing icons | 0–3 icons |

**Specs:**
- Small/Center height: 64dp
- Medium height: 112dp
- Large height: 152dp

---

### Tabs

**Figma component names:**
- `Tabs / Primary`
- `Tabs / Secondary`

**Per tab item:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Active | `True`, `False` |
| Icon | `True`, `False` |
| Label | (string) |
| Badge | `None`, `Small`, `Large` |

**Specs:**
- Tab height: 48dp (icon only), 48dp (label only), 64dp (both)
- Indicator: 3dp underline (Primary) or full-width (Secondary)

---

## Text Fields

**Figma component names:**
- `Text field / Filled`
- `Text field / Outlined`

**Properties:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Error`, `Disabled` |
| Populated | `True`, `False` |
| Leading icon | `True`, `False` |
| Trailing icon | `True`, `False` |
| Supporting text | `True`, `False` |
| Character count | `True`, `False` |
| Label | (string) |
| Placeholder | (string) |
| Supporting text | (string) |

**Specs:**
- Height: 56dp
- Corner radius: Extra Small top (4dp), 0dp bottom — Filled
- Corner radius: Extra Small (4dp) all — Outlined
- Horizontal padding: 16dp

---

## Selection Controls

### Checkbox
**Figma component name:** `Checkbox`

| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Selected | `Unselected`, `Selected`, `Indeterminate` |

Size: 18dp

---

### Radio Button
**Figma component name:** `Radio button`

| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Selected | `True`, `False` |

Size: 20dp

---

### Switch
**Figma component name:** `Switch`

| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Selected | `True`, `False` |
| Icon | `True`, `False` |

Size: 52×32dp

---

### Slider
**Figma component names:**
- `Slider / Continuous`
- `Slider / Discrete`
- `Slider / Centered`
- `Slider / Range`

| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |

---

## Dialogs & Sheets

### Dialog
**Figma component names:**
- `Dialog / Basic`
- `Dialog / Full-screen`

**Properties:**
| Property | Values |
|---|---|
| Icon | `True`, `False` |
| Title | (string) |
| Supporting text | (string) |
| Button layout | `Vertical`, `Horizontal` |

**Specs:**
- Width: 280–560dp
- Corner radius: 28dp (Extra Large shape)

---

### Bottom Sheet
**Figma component names:**
- `Bottom sheet / Modal` — overlays content
- `Bottom sheet / Standard` — persistent

**Specs:**
- Corner radius: 28dp top left, 28dp top right
- Drag handle: 32×4dp

---

### Side Sheet
**Figma component names:**
- `Side sheet / Modal`
- `Side sheet / Standard`

**Specs:**
- Width: 256–400dp
- Corner radius (modal): 16dp left side

---

## Progress Indicators

### Linear Progress Indicator
**Figma component name:** `Progress indicator / Linear`

| Property | Values |
|---|---|
| Type | `Determinate`, `Indeterminate` |
| Value | 0–100% |

**Specs:**
- Height: 4dp
- Corner radius: Full

---

### Circular Progress Indicator
**Figma component name:** `Progress indicator / Circular`

| Property | Values |
|---|---|
| Type | `Determinate`, `Indeterminate` |
| Value | 0–100% |
| Size | `Small` (24dp), `Medium` (48dp) |

---

## Communication

### Badge
**Figma component names:**
- `Badge / Small` — dot, 6dp
- `Badge / Large` — number, 16dp

| Property | Values |
|---|---|
| Count | (number, Large only) |

Used as overlay on icons, typically in navigation.

---

### Snackbar
**Figma component names:**
- `Snackbar / 1-line`
- `Snackbar / 2-line`

| Property | Values |
|---|---|
| Action | `True`, `False` |
| Icon | `True`, `False` |
| Supporting text | (string) |
| Action label | (string) |

**Specs:**
- Min width: 288dp, Max width: 568dp
- Height: 48dp (1-line), 68dp (2-line)
- Corner radius: 4dp (Extra Small shape)

---

## Date & Time Pickers

### Date Picker
**Figma component names:**
- `Date picker / Docked` — inline calendar
- `Date picker / Modal` — dialog with calendar
- `Date picker / Modal input` — dialog with text input
- `Date range picker / Modal` — dialog for range selection

| Property | Values |
|---|---|
| Show year selection | `True`, `False` |

---

### Time Picker
**Figma component names:**
- `Time picker / Dial` — clock dial
- `Time picker / Input` — text input

| Property | Values |
|---|---|
| Format | `12h`, `24h` |

---

## Menus

**Figma component names:**
- `Menu` — standard dropdown menu
- `Menu item` — individual item within a menu

**Menu item properties:**
| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Pressed`, `Disabled` |
| Leading icon | `True`, `False` |
| Trailing icon | `True`, `False` |
| Trailing text | `True`, `False` |
| Divider above | `True`, `False` |
| Label | (string) |

**Specs:**
- Item height: 48dp
- Horizontal padding: 12dp
- Corner radius: 4dp (menu container)
- Min width: 112dp, Max width: 280dp

---

## Search

**Figma component names:**
- `Search bar` — full-width search input bar
- `Search view` — expanded search with results

| Property | Values |
|---|---|
| State | `Enabled`, `Hovered`, `Focused`, `Disabled` |
| Leading icon | `True`, `False` |
| Trailing icon | `True`, `False` |
| Avatar | `True`, `False` |
| Placeholder | (string) |

**Specs:**
- Height: 56dp
- Corner radius: Full (28dp)

---

## Divider

**Figma component names:**
- `Divider / Full-width`
- `Divider / Inset` — offset from leading edge
- `Divider / Middle inset` — offset both sides

**Specs:**
- Height: 1dp
- Color: Outline-variant token

---

## Carousel

**Figma component names:**
- `Carousel / Hero` — single large featured item
- `Carousel / Multi-browse` — multiple items visible
- `Carousel / Uncontained` — items extend beyond container

**Specs:**
- Item corner radius: 16dp (Large shape)
- Spacing between items: 8dp
