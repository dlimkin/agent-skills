---
name: ionic-components
description: Use Ionic Framework UI components instead of custom HTML/CSS when building interfaces. Prefer ion- tags, use Ionic CSS variables for colors, use Ionicons for icons, and only fall back to custom styles when no Ionic equivalent exists.
---

# Ionic Components Skill

## Component Priority
When building any UI element, always prefer Ionic components over custom HTML/CSS.

1. **Check Ionic first** — before creating any UI block, verify if an Ionic component
   exists for the use case
2. **Use Ionic component** if available — with proper `ion-` tags and Ionic properties
3. **Custom HTML/CSS only** if Ionic has no equivalent component or lacks required functionality

## Looking Up Components
When unsure if an Ionic component exists or how to use it:
1. **Context7 first** (if available) — resolve `ionic` and fetch relevant docs
2. **Fallback** — check https://ionicframework.com/docs/components directly

---

## Icons — Ionicons
Always use Ionicons for icons. Browse available icons at https://ionic.io/ionicons

### Setup
If using Ionic Framework — Ionicons is included by default, no setup needed.

Without Ionic Framework, add before closing `</body>`:
```html
<script type="module" src="https://unpkg.com/ionicons@latest/dist/ionicons/ionicons.esm.js"></script>
<script nomodule src="https://unpkg.com/ionicons@latest/dist/ionicons/ionicons.js"></script>
```

### Basic Usage
```html
<ion-icon name="heart"></ion-icon>
```

### Variants
Each icon has three variants:
```html
<ion-icon name="heart"></ion-icon>          <!-- filled (default) -->
<ion-icon name="heart-outline"></ion-icon>  <!-- outline -->
<ion-icon name="heart-sharp"></ion-icon>    <!-- sharp -->
```

Use `outline` for iOS-style, `sharp` for MD/Android-style, or let the platform decide:
```html
<ion-icon ios="heart-outline" md="heart-sharp"></ion-icon>
```

### Size
```html
<ion-icon name="heart" size="small"></ion-icon>
<ion-icon name="heart" size="large"></ion-icon>
```

Or via CSS (use multiples of 8):
```css
ion-icon {
  font-size: 32px;
}
```

### Color
Use Ionic CSS variables:
```css
ion-icon {
  color: var(--ion-color-primary);
}
```

### Stroke Width (outline variant only)
```css
ion-icon {
  --ionicon-stroke-width: 16px; /* default is 32px */
}
```

### Accessibility
Decorative icons — hide from assistive technology:
```html
<ion-icon name="heart" aria-hidden="true"></ion-icon>
```

Interactive icons — add a label:
```html
<ion-icon name="heart" aria-label="Favorite"></ion-icon>
```

Icon inside a button — label the button, hide the icon:
```html
<ion-button aria-label="Favorite">
  <ion-icon name="heart" aria-hidden="true"></ion-icon>
</ion-button>
```

### Icon in ion-item
```html
<ion-item>
  <ion-icon name="person-outline" slot="start" aria-hidden="true"></ion-icon>
  <ion-label>Profile</ion-label>
</ion-item>
```

---

## Ionic CSS Variables
Never use hardcoded colors. Always use Ionic CSS variables:

Common variables:
- `--ion-color-primary`, `--ion-color-secondary`, `--ion-color-tertiary`
- `--ion-color-success`, `--ion-color-warning`, `--ion-color-danger`
- `--ion-color-light`, `--ion-color-medium`, `--ion-color-dark`
- `--ion-background-color`, `--ion-text-color`
- `--ion-font-family`

## Custom Styles
If custom styles are needed:
- Use Ionic CSS variables for all colors and typography
- Follow Ionic's spacing scale where possible
- Scope styles to component to avoid conflicts

---

## Examples

### Button
✅ Correct:
```html
<ion-button expand="block" color="primary">Submit</ion-button>
<ion-button fill="outline" color="danger">Delete</ion-button>
```
❌ Incorrect:
```html
<button style="background: #3880ff; color: white; width: 100%">Submit</button>
```

### Input
✅ Correct:
```html
<ion-input label="Email" type="email" placeholder="Enter email"></ion-input>
<ion-textarea label="Message" rows="4"></ion-textarea>
```
❌ Incorrect:
```html
<input type="email" placeholder="Email" class="my-input" />
```

### List
✅ Correct:
```html
<ion-list>
  <ion-item>
    <ion-label>Item 1</ion-label>
  </ion-item>
  <ion-item>
    <ion-icon name="person-outline" slot="start" aria-hidden="true"></ion-icon>
    <ion-label>Item with icon</ion-label>
  </ion-item>
</ion-list>
```
❌ Incorrect:
```html
<ul class="my-list">
  <li>Item 1</li>
</ul>
```

### Card
✅ Correct:
```html
<ion-card>
  <ion-card-header>
    <ion-card-title>Title</ion-card-title>
    <ion-card-subtitle>Subtitle</ion-card-subtitle>
  </ion-card-header>
  <ion-card-content>
    Content goes here
  </ion-card-content>
</ion-card>
```
❌ Incorrect:
```html
<div class="card" style="border-radius: 8px; box-shadow: ...">
  <div class="card-title">Title</div>
</div>
```

### Colors
✅ Correct:
```css
color: var(--ion-color-primary);
background: var(--ion-color-light);
border-color: var(--ion-color-medium);
```
❌ Incorrect:
```css
color: #3880ff;
background: #f4f5f8;
border-color: #92949c;
```

### Icons
✅ Correct:
```html
<!-- Decorative -->
<ion-icon name="star-outline" aria-hidden="true"></ion-icon>

<!-- Interactive -->
<ion-icon name="close" aria-label="Close dialog"></ion-icon>

<!-- In button -->
<ion-button aria-label="Add item">
  <ion-icon name="add-outline" aria-hidden="true"></ion-icon>
</ion-button>
```
❌ Incorrect:
```html
<img src="./icons/star.png" />
<i class="fa fa-star"></i>
```
