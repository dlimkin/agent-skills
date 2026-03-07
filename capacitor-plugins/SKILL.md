---
name: capacitor-plugins
description: Create, structure, and publish Capacitor plugins with native iOS (Swift) and Android (Kotlin) implementations. Includes TypeScript interface definition, web fallback, permissions, events, and migration from Cordova plugins.
---

# Capacitor Plugins Skill

## Plugin Types

| Type | Description |
|------|-------------|
| **Local** | Lives inside your app's native project — not published to npm |
| **Global** | Standalone npm package, reusable across any Capacitor app |

---

## Scaffolding

Generate a new plugin using the official CLI:

```bash
npm init @capacitor/plugin@latest
```

With options (non-interactive):
```bash
npm init @capacitor/plugin@latest \
  --name capacitor-my-plugin \
  --package-id com.mycompany.plugins.myplugin \
  --class-name MyPlugin \
  --repo https://github.com/myuser/capacitor-my-plugin \
  --author "Name <name@example.com>" \
  --license MIT \
  --description "My Capacitor plugin" \
  --android-lang kotlin
```

Generated structure:
```
capacitor-my-plugin/
├── src/
│   ├── definitions.ts     # TypeScript interface (public API)
│   ├── index.ts           # Entry point
│   └── web.ts             # Web/PWA fallback implementation
├── ios/
│   └── Sources/MyPlugin/
│       ├── MyPlugin.swift          # CAPPlugin class (bridge)
│       └── MyPluginImplementation.swift  # Logic (NSObject)
├── android/
│   └── src/main/java/.../
│       └── MyPlugin.kt    # Android implementation
├── example-app/           # Test app (excluded from npm publish)
├── package.json
└── MyPlugin.podspec
```

---

## Step 1 — Define the TypeScript Interface

Always start here. Define all methods and types in `src/definitions.ts`:

```ts
export interface MyPluginOptions {
  value: string;
  timeout?: number;
}

export interface MyPluginResult {
  result: string;
  timestamp: number;
}

export interface MyPlugin {
  /**
   * Does something useful.
   *
   * @since 1.0.0
   */
  doSomething(options: MyPluginOptions): Promise<MyPluginResult>;

  /**
   * Check permissions.
   *
   * @since 1.0.0
   */
  checkPermissions(): Promise<PermissionStatus>;

  /**
   * Request permissions.
   *
   * @since 1.0.0
   */
  requestPermissions(): Promise<PermissionStatus>;

  /**
   * Listen for native events.
   *
   * @since 1.0.0
   */
  addListener(
    eventName: 'myEvent',
    listenerFunc: (event: MyEventData) => void,
  ): Promise<PluginListenerHandle>;

  removeAllListeners(): Promise<void>;
}

export interface MyEventData {
  value: string;
}

export type PermissionStatus = {
  myFeature: PermissionState; // 'granted' | 'denied' | 'prompt'
};
```

---

## Step 2 — Web Implementation

`src/web.ts` — fallback for browser/PWA:

```ts
import { WebPlugin } from '@capacitor/core';
import type { MyPlugin, MyPluginOptions, MyPluginResult } from './definitions';

export class MyPluginWeb extends WebPlugin implements MyPlugin {
  async doSomething(options: MyPluginOptions): Promise<MyPluginResult> {
    console.log('doSomething called with', options);
    return {
      result: options.value,
      timestamp: Date.now(),
    };
  }

  async checkPermissions(): Promise<PermissionStatus> {
    return { myFeature: 'granted' };
  }

  async requestPermissions(): Promise<PermissionStatus> {
    return { myFeature: 'granted' };
  }
}
```

---

## Step 3 — iOS Implementation (Swift)

### Bridge class — `ios/Sources/MyPlugin/MyPlugin.swift`

```swift
import Foundation
import Capacitor

@objc(MyPlugin)
public class MyPlugin: CAPPlugin, CAPBridgedPlugin {
  public let identifier = "MyPlugin"
  public let jsName = "MyPlugin"

  public let pluginMethods: [CAPPluginMethod] = [
    CAPPluginMethod(name: "doSomething", returnType: CAPPluginReturnPromise),
    CAPPluginMethod(name: "checkPermissions", returnType: CAPPluginReturnPromise),
    CAPPluginMethod(name: "requestPermissions", returnType: CAPPluginReturnPromise),
  ]

  private let implementation = MyPluginImplementation()

  @objc func doSomething(_ call: CAPPluginCall) {
    guard let value = call.getString("value") else {
      call.reject("Missing value parameter")
      return
    }

    let result = implementation.doSomething(value: value)

    call.resolve([
      "result": result,
      "timestamp": Int(Date().timeIntervalSince1970 * 1000),
    ])
  }

  @objc override public func checkPermissions(_ call: CAPPluginCall) {
    call.resolve(["myFeature": implementation.checkPermissions()])
  }

  @objc override public func requestPermissions(_ call: CAPPluginCall) {
    implementation.requestPermissions { [weak self] status in
      call.resolve(["myFeature": status])
    }
  }
}
```

### Logic class — `ios/Sources/MyPlugin/MyPluginImplementation.swift`

```swift
import Foundation

@objc public class MyPluginImplementation: NSObject {
  @objc public func doSomething(value: String) -> String {
    return "Processed: \(value)"
  }

  @objc public func checkPermissions() -> String {
    // Check actual permission status here
    return "granted"
  }

  @objc public func requestPermissions(completion: @escaping (String) -> Void) {
    // Request permissions and call completion
    completion("granted")
  }
}
```

### iOS Dependencies

CocoaPods (`.podspec`):
```ruby
s.dependency 'Capacitor'
s.dependency 'FirebaseFirestore', '~> 11.8'
```

Swift Package Manager (`Package.swift`):
```swift
.package(url: "https://github.com/firebase/firebase-ios-sdk.git", from: "11.8.0")
```

---

## Step 4 — Android Implementation (Kotlin)

`android/src/main/java/com/mycompany/plugins/myplugin/MyPlugin.kt`:

```kotlin
package com.mycompany.plugins.myplugin

import com.getcapacitor.JSObject
import com.getcapacitor.Plugin
import com.getcapacitor.PluginCall
import com.getcapacitor.PluginMethod
import com.getcapacitor.annotation.CapacitorPlugin
import com.getcapacitor.annotation.Permission

@CapacitorPlugin(
  name = "MyPlugin",
  permissions = [
    Permission(
      alias = "myFeature",
      strings = [android.Manifest.permission.CAMERA]
    )
  ]
)
class MyPlugin : Plugin() {

  private val implementation = MyPluginImplementation()

  @PluginMethod
  fun doSomething(call: PluginCall) {
    val value = call.getString("value") ?: run {
      call.reject("Missing value parameter")
      return
    }

    val result = implementation.doSomething(value)

    val ret = JSObject()
    ret.put("result", result)
    ret.put("timestamp", System.currentTimeMillis())
    call.resolve(ret)
  }

  @PluginMethod
  override fun checkPermissions(call: PluginCall) {
    val ret = JSObject()
    ret.put("myFeature", getPermissionState("myFeature").toString().lowercase())
    call.resolve(ret)
  }

  @PluginMethod
  override fun requestPermissions(call: PluginCall) {
    requestAllPermissions(call, "permissionsCallback")
  }

  @PermissionCallback
  private fun permissionsCallback(call: PluginCall) {
    checkPermissions(call)
  }
}
```

`MyPluginImplementation.kt`:
```kotlin
class MyPluginImplementation {
  fun doSomething(value: String): String {
    return "Processed: $value"
  }
}
```

---

## Firing Events to JavaScript

### iOS
```swift
notifyListeners("myEvent", data: ["value": "hello from native"])
```

### Android
```kotlin
val data = JSObject()
data.put("value", "hello from native")
notifyListeners("myEvent", data)
```

### JavaScript (consuming events)
```ts
import { MyPlugin } from 'capacitor-my-plugin';

const listener = await MyPlugin.addListener('myEvent', (event) => {
  console.log('Received:', event.value);
});

// Later:
await listener.remove();
// Or:
await MyPlugin.removeAllListeners();
```

---

## Local Plugin (in-app, not published)

Register manually in the native projects:

**iOS** — `AppDelegate.swift`:
```swift
import Capacitor
import MyLocalPlugin // if separated

// In application(_:didFinishLaunchingWithOptions:)
// Register inline in capacitor.config.ts is not needed;
// just add the class to the native project
```

**Android** — `MainActivity.kt`:
```kotlin
class MainActivity : BridgeActivity() {
  override fun registerPlugins(bridge: Bridge) {
    super.registerPlugins(bridge)
    bridge.registerPlugin(MyLocalPlugin::class.java)
  }
}
```

---

## Build & Sync

```bash
# Build TypeScript
npm run build

# Sync with native projects (run inside your app, not the plugin)
npx cap sync

# Verify plugin was detected
# Expected output: [info] Found 1 Capacitor plugin for android: - my-plugin (1.0.0)
```

---

## Documentation

The plugin template includes `@capacitor/docgen`. JSDoc comments in `definitions.ts` are auto-generated into `README.md` on build:

```ts
/**
 * Opens the camera.
 *
 * @since 1.0.0
 * @platform ios, android
 */
openCamera(options: CameraOptions): Promise<CameraResult>;
```

Run manually:
```bash
npx docgen --api MyPlugin --output-readme README.md
```

---

## Publishing to npm

```bash
npm run build
npm publish
```

The `example-app/` folder is automatically excluded via `.npmignore`.

---

## Migrating from Cordova

### Strategy

Do not rewrite everything at once. Follow this order:

1. **Audit** existing Cordova plugins — remove unused ones first
2. **Replace** with official Capacitor equivalents where available
3. **Keep** Cordova plugins that still work in Capacitor (most do)
4. **Rewrite** only plugins that are broken or incompatible

### Step-by-step Migration

```bash
# 1. Install Capacitor in existing Cordova/Ionic project
npm install @capacitor/core @capacitor/cli
npm install @capacitor/app @capacitor/haptics @capacitor/keyboard @capacitor/status-bar

# 2. Initialize (reads Bundle ID and app name from config.xml)
npx cap init

# 3. Build web assets first (required before adding platforms)
npm run build # or ionic build

# 4. Add native platforms
npx cap add ios
npx cap add android
# Capacitor auto-installs existing Cordova plugins from package.json
```

### Replacing Cordova Plugins

| Cordova | Capacitor equivalent |
|---------|---------------------|
| `cordova-plugin-camera` | `@capacitor/camera` |
| `cordova-plugin-file` | `@capacitor/filesystem` |
| `cordova-plugin-geolocation` | `@capacitor/geolocation` |
| `cordova-plugin-network-information` | `@capacitor/network` |
| `cordova-plugin-device` | `@capacitor/device` |
| `cordova-plugin-statusbar` | `@capacitor/status-bar` |
| `cordova-plugin-splashscreen` | `@capacitor/splash-screen` |
| `cordova-plugin-push` | `@capacitor/push-notifications` |
| `cordova-plugin-inappbrowser` | `@capacitor/browser` |
| `cordova-sqlite-storage` | `@capacitor-community/sqlite` |

After replacing:
```bash
npm uninstall cordova-plugin-name
npx cap sync [android|ios]
```

### config.xml → capacitor.config.ts

Cordova preferences from `config.xml` map to `capacitor.config.ts`:

```ts
// capacitor.config.ts
const config: CapacitorConfig = {
  cordova: {
    preferences: {
      DisableDeploy: 'true',
      CameraUsesGeolocation: 'true',
    },
  },
};
```

Permissions defined in `plugin.xml` are automatically added to `AndroidManifest.xml` and `Info.plist` — but verify them manually.

### iOS Scheme (LocalStorage data loss)

Cordova uses `ionic://`, Capacitor uses `capacitor://`. If your app uses LocalStorage or IndexedDB, change the scheme to preserve data:

```ts
// capacitor.config.ts
const config: CapacitorConfig = {
  server: {
    iosScheme: 'ionic', // keeps same origin as Cordova
  },
};
```

### Rewriting a Cordova Plugin as a Capacitor Plugin

If a Cordova plugin has no Capacitor equivalent and doesn't work out of the box:

1. Scaffold a new Capacitor plugin (see above)
2. Port native code from `src/android/` and `src/ios/` of the Cordova plugin
3. Replace Cordova's `plugin.xml` configuration with:
   - `@CapacitorPlugin` annotation (Android permissions)
   - `Info.plist` entries (iOS permissions)
   - `.podspec` or `Package.swift` (iOS dependencies)
   - `build.gradle` (Android dependencies)
4. Replace Cordova's `execute()` with `@PluginMethod` / `@objc func`
5. Replace `callbackContext.success()` with `call.resolve()`
6. Replace `callbackContext.error()` with `call.reject()`

### Removing Cordova Completely

Once all plugins are migrated:

```bash
# Remove Cordova
npm uninstall cordova cordova-ios cordova-android
rm config.xml
rm -rf platforms/ plugins/

# Keep Capacitor native projects in source control
git add ios/ android/
```

> Note: Cordova removal is optional. Capacitor can coexist with Cordova indefinitely if needed.

---

## Common Mistakes

❌ Modifying `platforms/` folder (Cordova habit) — Capacitor uses `ios/` and `android/` at root
❌ Forgetting `npx cap sync` after plugin changes
❌ Not calling `call.reject()` on error paths — always resolve or reject every call
❌ Putting business logic in the bridge class — keep it in the Implementation class
❌ Using `Plugins` import from old Capacitor v2 — use named imports from the plugin package instead
