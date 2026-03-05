# Angular Animations Skill

A skill for AI coding agents that teaches modern Angular animation patterns using `animate.enter`, `animate.leave`, and CSS — without the legacy `@angular/animations` package.

## Installation

```bash
npx skills add dlimkin/agent-skills --skill angular-animations
```

## What this skill does

- Prefers `animate.enter` / `animate.leave` over legacy `@angular/animations`
- Uses CSS keyframes and transitions for all animations
- Applies correct patterns for state-based animations with signals
- Sets up route transitions via the View Transitions API
- Warns about the element removal order gotcha with `animate.leave`
- Enforces correct use of `animationComplete()` when integrating third-party libraries like GSAP

## Covered Topics

| Topic | Description |
|-------|-------------|
| `animate.enter` | Animate elements entering the DOM |
| `animate.leave` | Animate elements leaving the DOM |
| CSS transitions vs keyframes | When to use each and how to pair with `@starting-style` |
| Dynamic bindings | `[animate.enter]` with signals |
| Third-party libraries | GSAP, anime.js integration via `AnimationCallbackEvent` |
| State animations | Toggle open/closed with CSS classes and signals |
| Height auto | `grid-template-rows` technique for unknown heights |
| Route transitions | View Transitions API with `withViewTransitions()` |
| Testing | Enabling animations in TestBed |
| Legacy ban | Do not use `@angular/animations` in new code |

## Links

- [Angular Animations Guide](https://angular.dev/guide/animations)
- [Route Transition Animations](https://angular.dev/guide/routing/route-transition-animations)
