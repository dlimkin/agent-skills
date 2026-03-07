# Capacitor Plugins Skill

A skill for AI coding agents that teaches how to create, structure, and publish Capacitor plugins — including native iOS (Swift) and Android (Kotlin) implementations, permissions, events, and migration from Cordova.

## Installation

```bash
npx skills add dlimkin/agent-skills --skill capacitor-plugins
```

## What this skill does

- Scaffolds plugins using the official `npm init @capacitor/plugin` generator
- Defines TypeScript interfaces before touching any native code
- Implements iOS plugins in Swift (bridge + implementation pattern)
- Implements Android plugins in Kotlin with `@CapacitorPlugin` and `@PluginMethod`
- Handles permissions on both platforms
- Fires native events to JavaScript with `notifyListeners`
- Registers local (in-app) plugins in native projects
- Publishes global plugins to npm
- Migrates existing Cordova plugins to Capacitor

## Covered Topics

| Topic | Description |
|-------|-------------|
| Scaffolding | `npm init @capacitor/plugin` with all CLI options |
| Project structure | Folder layout for src, ios, android, example-app |
| TypeScript definitions | `definitions.ts` interface — always defined first |
| Web fallback | `WebPlugin` implementation for browser/PWA |
| iOS (Swift) | Bridge class, implementation class, dependencies (CocoaPods / SPM) |
| Android (Kotlin) | `@CapacitorPlugin`, `@PluginMethod`, `@PermissionCallback` |
| Permissions | `checkPermissions` / `requestPermissions` on both platforms |
| Events | `notifyListeners` on native, `addListener` on JS side |
| Local plugins | Registering in `MainActivity.kt` and `AppDelegate.swift` |
| Publishing | `npm run build && npm publish`, docgen for README |
| Cordova migration | Step-by-step strategy, plugin replacement table, config.xml mapping |
| Cordova rewrite | Porting native code from Cordova plugin to Capacitor structure |

## Links

- [Capacitor Plugin Docs](https://capacitorjs.com/docs/plugins)
- [Creating Plugins](https://capacitorjs.com/docs/plugins/creating-plugins)
- [iOS Plugin Guide](https://capacitorjs.com/docs/plugins/ios)
- [Android Plugin Guide](https://capacitorjs.com/docs/plugins/android)
- [Migrating from Cordova](https://capacitorjs.com/docs/cordova/migrating-from-cordova-to-capacitor)
- [Capacitor Community Plugins](https://github.com/capacitor-community)
