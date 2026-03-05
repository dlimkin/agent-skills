---
name: angular-animations
description: Use Angular's modern animate.enter and animate.leave APIs for element animations. Prefer CSS-based animations over the legacy @angular/animations package. Apply correct patterns for enter/leave, state transitions, and route animations.
---

# Angular Animations Skill

## Approach Priority
1. **`animate.enter` / `animate.leave`** — modern Angular API, prefer for element enter/leave
2. **CSS classes + signals** — for state-based animations (open/closed, toggle)
3. **View Transitions API** — for route transitions
4. **Legacy `@angular/animations`** — only if already used in the project; do not introduce in new code

---

## animate.enter

Animates an element as it **enters** the DOM. Angular adds the specified CSS class when the element appears, then removes it once the animation completes.

```html
<!-- Static class -->
@if (isShown()) {
  <div animate.enter="enter-animation">
    Content
  </div>
}

<!-- Dynamic binding -->
@if (isShown()) {
  <div [animate.enter]="enterClass()">
    Content
  </div>
}
```

```css
/* Keyframe animation */
.enter-animation {
  animation: slide-fade 300ms ease-out;
}

@keyframes slide-fade {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Using CSS transitions instead of keyframes:**
When using transitions, `animate.enter` applies the *target* state. Use `@starting-style` to define the *from* state:
```css
.enter-transition {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 300ms ease-out, transform 300ms ease-out;
}

@starting-style {
  .enter-transition {
    opacity: 0;
    transform: translateY(12px);
  }
}
```

**NOTE:** Angular removes the class only after the **longest** animation on the element completes.

---

## animate.leave

Animates an element as it **leaves** the DOM. Angular adds the class, waits for the animation to finish, then removes the element.

```html
@if (isShown()) {
  <div animate.leave="leaving">
    Content
  </div>
}
```

```css
.leaving {
  opacity: 0;
  transform: translateY(12px);
  transition:
    opacity 300ms ease-in,
    transform 300ms ease-in;
}
```

### ⚠️ Element removal order — critical rule
`animate.leave` **only works** on the element being directly removed. It will **not** animate if placed on a *descendant* of the removed element — the parent removal takes the entire subtree immediately.

```html
<!-- ❌ Wrong — child animate.leave will NOT run -->
@if (isShown()) {
  <div class="parent">
    <div animate.leave="leaving">Content</div>
  </div>
}

<!-- ✅ Correct — animate.leave on the removed element itself -->
@if (isShown()) {
  <div animate.leave="leaving">Content</div>
}
```

---

## Using Functions and Third-party Libraries

Both `animate.enter` and `animate.leave` support event binding syntax for function calls or libraries like GSAP, anime.js, etc.

```ts
import { AnimationCallbackEvent, Component, signal } from '@angular/core';

export class MyComponent {
  isShown = signal(false);

  onLeave(event: AnimationCallbackEvent) {
    // Example with GSAP:
    // gsap.to(event.target, {
    //   duration: 0.5,
    //   opacity: 0,
    //   y: 20,
    //   onComplete: () => event.animationComplete()
    // });

    // Always call animationComplete() when done
    event.animationComplete();
  }
}
```

```html
@if (isShown()) {
  <div (animate.leave)="onLeave($event)">Content</div>
}
```

**IMPORTANT:** When using `(animate.leave)` with a function, you **must** call `event.animationComplete()` — otherwise Angular will remove the element after a 4-second fallback delay.

To configure the fallback timeout:
```ts
{ provide: MAX_ANIMATION_TIMEOUT, useValue: 6000 } // ms
```

---

## State-based Animations (CSS classes + signals)

For toggling between two states (open/closed, expanded/collapsed), use CSS classes driven by signals:

```ts
export class AccordionComponent {
  isOpen = signal(false);
  toggle() { this.isOpen.update(v => !v); }
}
```

```html
<div [class.open]="isOpen()" [class.closed]="!isOpen()" class="panel">
  Content
</div>
```

```css
.panel {
  transition: all 300ms ease-in-out;
}
.open {
  height: 200px;
  opacity: 1;
}
.closed {
  height: 0;
  opacity: 0;
}
```

### Animating to auto height
Use `grid-template-rows` trick for unknown heights:
```css
.container {
  display: grid;
  grid-template-rows: 0fr;
  overflow: hidden;
  transition: grid-template-rows 300ms ease-in-out;
}
.container.open {
  grid-template-rows: 1fr;
}
.container .content {
  min-height: 0;
}
```

---

## Route Transition Animations

Use the **View Transitions API** for route animations (Angular developer preview):

```ts
// app.config.ts
import { provideRouter, withViewTransitions } from '@angular/router';

export const appConfig = {
  providers: [
    provideRouter(routes, withViewTransitions())
  ]
};
```

```css
/* CSS — target transition pseudo-elements */
::view-transition-old(root) {
  animation: fade-out 200ms ease-in;
}
::view-transition-new(root) {
  animation: fade-in 200ms ease-out;
}

@keyframes fade-out {
  to { opacity: 0; }
}
@keyframes fade-in {
  from { opacity: 0; }
}
```

---

## Timing and Easing Reference

```css
/* Duration recommendations */
--duration-instant:  100ms;   /* micro-interactions */
--duration-fast:     200ms;   /* buttons, toggles */
--duration-normal:   300ms;   /* panels, modals */
--duration-slow:     500ms;   /* page transitions */

/* Common easing */
ease-in-out   /* general purpose */
ease-out      /* elements entering */
ease-in       /* elements leaving */
cubic-bezier(0.34, 1.56, 0.64, 1) /* spring/bounce effect */
```

---

## Testing

By default, TestBed **disables** animations. To test animations in browser/e2e tests:

```ts
TestBed.configureTestingModule({
  animationsEnabled: true
});
```

---

## Do NOT Use (Legacy)
Avoid introducing `@angular/animations` package in new code. Do not use:
- `BrowserAnimationsModule`
- `trigger()`, `state()`, `transition()`, `animate()` from `@angular/animations`
- `[@trigger]` binding syntax

These are legacy APIs. Use `animate.enter`, `animate.leave`, and CSS instead.

Exception: if the existing codebase already uses `@angular/animations`, do not mix — legacy and new APIs **cannot be used in the same component**.
