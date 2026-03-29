---
name: flutter-dart-best-practices
description: >
  Expert knowledge on Flutter and Dart: common developer mistakes, proper error handling,
  app architecture, BLoC, local databases, DateTime pitfalls, navigation, Scopes pattern,
  declarative navigation, UI Kit local packages, localization, and CI/CD for Flutter.
  Use this skill ALWAYS when the user asks about Flutter or Dart architecture,
  code errors, exception handling, try/catch, BLoC, local databases, DateTime,
  navigation, Clean Architecture in Flutter, Flutter project structure, scopes,
  InheritedWidget, auth guard, declarative navigator, UI kit, localization, CI pipelines,
  or requests a Flutter/Dart code review.
---

# Flutter & Dart Best Practices

This skill contains practical knowledge from real-world Flutter/Dart development.
Content is split into two blocks: **error handling & common anti-patterns** and **app architecture**.

---

## BLOCK 1 — COMMON DART/FLUTTER DEVELOPER MISTAKES

### 1. Error Handling (most frequent and painful topic)

#### Anti-pattern: Silencing errors via try/catch

```dart
// BAD — swallowing the error, returning null
try {
  final data = await repository.fetchData();
  return data;
} catch (e) {
  return null; // or return [];
}
```

**Why it's bad:**
- The error is lost — you'll never know what happened
- Impossible to debug: no stack trace, no exception type
- User sees a blank screen instead of a meaningful message
- You cannot predict ALL possible errors (SocketException, FormatException, DiskFullException, etc.)

#### Anti-pattern: Rethrowing your own Exception without preserving the stack trace

```dart
// BAD — original stack trace is lost
try {
  await dataProvider.fetch();
} catch (e) {
  throw RepositoryException('something went wrong');
}
```

#### Correct: preserve the stack trace when rethrowing

```dart
// GOOD
try {
  await dataProvider.fetch();
} catch (e, stackTrace) {
  Error.throwWithStackTrace(e, stackTrace);
}
```

#### Correct: handle specific errors specifically

```dart
// GOOD — only handle what you know
try {
  final response = await dio.get('/endpoint');
  return response.data;
} on DioException catch (e, st) {
  if (e.response?.statusCode == 404) {
    return []; // only for this specific known case
  }
  Error.throwWithStackTrace(e, st); // rethrow everything else
}
```

**Key rules:**
- Throwing inside a `catch` block is fine. The more errors you throw, the better
- An error is not something terrible — it is an alternative execution path
- `Error` — implies something truly unexpected and unrecoverable
- `Exception` — a normal abnormal situation (no internet, 404, etc.)
- Always preserve `stackTrace` — without it you cannot find the source of the problem

---

### 2. Local Databases

**Common mistake:** choosing a package from pub.dev by star count or a "nice wrapper".

**Right questions when choosing a DB package:**
- Test coverage (the DB replicates your state — bugs here are critical)
- Isolation / transaction support
- Behavior under concurrent access
- Performance on real data, not synthetic benchmarks

**Note:** the difference between 200ms vs 20ms in a local DB is invisible to the user.
Show shimmer effects — users will be happy regardless of DB speed.

---

### 3. DateTime — a critical pitfall

#### Anti-pattern: sending local time without timezone offset

```dart
// BAD — no timezone offset
final dt = DateTime.now();
final str = dt.toString(); // "2024-01-15 14:30:00.000" — no +03:00!
sendToBackend(str); // backend doesn't know the timezone
```

`DateTime.now().toString()` does NOT include the timezone offset.
This leads to systematic, hard-to-find bugs across the entire app.

#### Correct: always use UTC or Unix timestamp

```dart
// GOOD — option 1: UTC ISO string
final utcTime = DateTime.now().toUtc().toIso8601String();
// "2024-01-15T11:30:00.000Z"

// GOOD — option 2: Unix timestamp (always safe)
final unixTime = DateTime.now().millisecondsSinceEpoch;
```

**Rule:** when exchanging dates with the backend or DB — **UTC or Unix Time only**.

---

### 4. Readable code vs "clever" code

- Clever, overly terse code makes maintenance harder for the whole team
- "Concise" != "fewer characters". Concise = clear structure and intent
- Experiment with new approaches in **pet projects**, not in production

---

### 5. "Fast" packages — a myth

Performance comes from **correct data structures and algorithms**, not from picking the "fastest" package.
The difference between two DB packages on real data is usually invisible to the user.

---

## BLOCK 2 — FLUTTER APP ARCHITECTURE

### What is architecture

**Architecture is a set of agreements and constraints.**

Analogies:
- Like a **constitution**: rules that must not be broken
- Like a **building blueprint**: says what goes where, not which fridge model
- Like an **interface**: fixes input/output, implementation is up to you

**Key properties:**
- Architecture is **declarative** (answers "what", not "how")
- Its job is to **impose constraints**, not to help implement features
- Violating architecture = breaking team agreements

**What architecture covers:** state management, number of layers, client-server interaction,
transport, dependency management, DB DDL, services — everything except the concrete implementation.

---

### Clean Architecture in Flutter (3 layers)

```
┌─────────────────────────────┐
│      Presentation Layer     │  <- UI, BLoC/Cubit, widgets
├─────────────────────────────┤
│        Domain Layer         │  <- Use Cases, business logic, repository interfaces
├─────────────────────────────┤
│         Data Layer          │  <- Repository impls, DataSources, DTOs
└─────────────────────────────┘
```

**Dependency rule:** Presentation -> Domain <- Data.
Domain knows nothing about Presentation or Data. Data depends on Domain abstractions.

See `references/architecture-layers.md` for full details and code examples.

---

### BLoC Pattern — correct usage

```
UI -> Event -> BLoC -> State -> UI
               |
           Repository
```

**Common beginner mistakes:**
- Creating a BLoC inside another BLoC's state (wrong!)
- Correct: subscribe to another BLoC's changes via `stream.listen` or `BlocListener`
- Putting business logic directly in widgets

See `references/bloc-patterns.md` for details.

---

### Typical navigation structure (Notes App example)

```
MaterialApp
├── Init         <- decides where to route the user
├── Auth         <- login/register screens
├── List         <- notes list
├── Note         <- create/edit note
└── Settings
```

**Auth Guard pattern:**
```
Init -> Provider<RepoStore> -> AuthBloc
         ├── SplashScr       (while checking auth)
         ├── Auth            (if unauthenticated)
         └── Navigator       (if authenticated)
              ├── Settings
              └── Profile
```

---

### Client-server schema — must be version controlled

Without a schema: backend changes an endpoint -> frontend crashes -> nobody knows why.

**Solution:** define an API schema (OpenAPI / GraphQL / Protobuf), keep it in VCS,
require team agreement for any change.

---

---

## BLOCK 3 — REAL-WORLD PROJECT PATTERNS (from production codebase)

### Scopes Pattern — State above the Navigator

**Scopes** are StatefulWidgets placed above MaterialApp's Navigator in the widget tree.
They provide state/dependencies to everything nested below them, including across screens.
Think of them as "guards" and "context providers" combined.

```dart
// Scopes are nested above the Navigator:
// MaterialApp.builder:
//   ApplicationScope      <- checks app version, shows update overlay
//     AuthScope           <- auth guard + provides user context
//       SettingsScope     <- user settings
//         ChatListScope   <- current user's chat list
//           Navigator     <- actual screen stack
```

**Why scopes over BLoC/Provider at screen level:**
- State lives above navigation — survives screen transitions
- Can display overlays on top of ALL screens (e.g. force-update dialog)
- Can gate access to the app (auth guard without route guards)
- Static helper methods on scope class = clean API, fewer imports

```dart
// Static shortcut helpers on the scope class
class AuthScope extends StatefulWidget {
  static UserEntity? userOf(BuildContext context) { ... }
  static void logout(BuildContext context, {VoidCallback? onSuccess}) { ... }
  static void authenticatedOr(
    BuildContext context, {
    required void Function(UserEntity user) onAuthenticated,
    VoidCallback? onUnauthenticated,
  }) { ... }
}

// Usage — no need to import controller, events, or provider
AuthScope.logout(context);
AuthScope.authenticatedOr(context, onAuthenticated: (user) { ... });
```

**Use InheritedModel** (not plain InheritedWidget) for granular subscriptions:
```dart
// Widgets subscribe only to the aspect they care about
// e.g. only rebuild when user.id changes, not on every auth state change
```

---

### Auth Guard with Scopes (not route guards)

The most reliable auth guard in Flutter — no `go_router` redirect logic needed:

```dart
class AuthScope extends StatefulWidget {
  final Widget child; // the authenticated part of the app

  @override
  Widget build(BuildContext context) {
    final isAuthenticated = /* listen to AuthController */;

    if (isAuthenticated) {
      return child; // shows Navigator with all app screens
    } else {
      return Navigator( // separate mini-navigator for auth flow only
        pages: [SignInPage()],
        onDidRemovePage: (_) {},
      );
    }
  }
}
```

**Why this is better than route-based guards:**
- Impossible to accidentally show authenticated screens to unauthenticated users
- Auth screens are completely isolated — separate Navigator
- No "redirect loops" or race conditions
- When user logs out, the entire app context is replaced, not just redirected

---

### Keep User Identity Separate from User Info

Never merge auth identity and profile data into one model:

```dart
// GOOD — two separate sealed classes
sealed class UserEntity { ... }
class UnauthenticatedUser extends UserEntity { const UnauthenticatedUser(); }
class AuthenticatedUser extends UserEntity {
  final String id;
  final String token;
}

// User profile info is a SEPARATE scope/model
// loaded only after authentication, invalidated on logout
class UserInfoScope extends StatefulWidget { ... }
```

**Why:** auth identity (id, token) is nearly immutable. Profile info changes often.
Merging them causes unnecessary rebuilds and complicated invalidation logic.

---

### Declarative Navigation without go_router

Custom declarative Navigator — zero dependencies, full control:

```dart
class AppNavigator extends StatefulWidget {
  @override
  Widget build(BuildContext context) {
    return Navigator(
      pages: _pages,
      onDidRemovePage: (_) => change((pages) => pages..removeLast()),
      restorationScopeId: null, // disable if not needed
    );
  }

  // The single most important method — change()
  // Takes current page list, returns desired page list
  void change(List<Page> Function(List<Page> current) transform) {
    setState(() => _pages = transform(List.of(_pages)));
  }
}

// All navigation operations via change():
// Push
navigator.change((pages) => [...pages, ProductPage(id: id)]);

// Pop
navigator.change((pages) => pages.length > 1 ? pages..removeLast() : pages);

// Reset to home
navigator.change((_) => [HomePage()]);

// Go to settings (no duplicates)
navigator.change((pages) => [
  ...pages.where((p) => p is! SettingsPage),
  SettingsPage(),
]);
```

**Pages vs Screens — naming convention:**
- `Page` = navigation descriptor (not a widget). E.g. `ChatPage`, `SettingsPage`.
  Use `sealed class` for type-safe parameters.
- `Screen` / `View` = the actual widget. E.g. `ChatScreen`, `SettingsScreen`.
- Never name a widget `SomethingPage` — reserve `Page` for Navigator.

**Router vs Navigator — when you need which:**
- `Navigator` — screen stack with animations. Most apps need only this.
- `Router` — syncs navigation state with the platform (URL bar, back button OS).
  Only needed for web URL support or deep link URL parsing.
  They are **independent** — you can use Navigator without Router and vice versa.

**Deep links without Router:**
```dart
// In main(), after WidgetsFlutterBinding.ensureInitialized():
final initialRoute = PlatformDispatcher.instance.defaultRouteName;
// Pass initialRoute to navigator, parse and build initial page stack
```

---

### Local Packages — What to Extract (and What Not To)

**Extract to a local package only when the content changes independently:**

```
packages/
├── ui/          ← UI kit: components, typography, icons, shaders, theme
└── l10n/        ← Localization (auto-generated from Google Sheets)
```

**Do NOT extract:**
- Individual features (one package per feature = complexity for no gain)
- Initialization code
- Individual screens

**UI Kit as a local package — key benefits:**
1. Compile only the UI kit on desktop (macOS/Windows) — instant hot reload
2. Separate `example/` app targeting web/desktop for previewing components
3. Publish the example to Firebase Hosting → designers can review in browser
4. New team members see all components without reading code

```bash
# Create UI kit package
flutter create --template=package packages/ui
# Add to root pubspec.yaml
# workspaces:
#   - packages/ui
```

**Icon strategy:**
- Raster PNG → use sprite atlas (one image, multiple offsets). Smaller, faster.
- Custom multi-color icons → convert to icon font with IconMoon, export as TTF.
- Logos that scale/recolor → Canvas (`CustomPainter` or `LeafRenderObjectWidget`).
- Avoid `flutter_svg` in production — it parses SVG at runtime on every build.

---

### Localization — Multiple ARB Files per Feature

```dart
// BAD — one giant ARB file
// app_en.arb: { "homeTitle": "...", "settingsTitle": "...", "chatSend": "..." }

// GOOD — one ARB file per feature/screen
// l10n/chat_en.arb, l10n/settings_en.arb, l10n/auth_en.arb

// Usage: each screen uses only its own localizations
context.chatL10n.sendButton
context.settingsL10n.title
```

**Best workflow:** Google Sheets → ARB files → Dart code.
Use `sheet_localization` package (or similar): translators work in Sheets,
CI generates ARB files and runs `flutter gen-l10n`.

---

### CI/CD Best Practices

**Composite local GitHub Action** for shared steps across multiple workflows:

```yaml
# .github/actions/setup-flutter/action.yml
# Used in: check.yml, build-staging.yml, build-prod.yml
# Contains: flutter setup, pub get, code generation, version extraction
```

**Sparse checkout for monorepos** — only pull what CI needs:
```yaml
- uses: actions/checkout@v4
  with:
    sparse-checkout: |
      .github
      frontend
```

**Build number = Unix timestamp** — always monotonically increasing:
```yaml
# pubspec.yaml: version: 1.2.3  (no build number)
# CI sets: version: 1.2.3+$(date +%s)
```

**Internal distribution:**
- Android: Internal App Sharing (no review, instant link)
- iOS: Xcode Cloud triggered from GitHub Action
- Web: Firebase Hosting (preview channels per branch)

---

## QUICK CODE REVIEW CHECKLIST

- [ ] No `catch (e) { return null; }` — errors are not silenced
- [ ] `Error.throwWithStackTrace(e, st)` used when rethrowing
- [ ] All dates exchanged as UTC ISO string or Unix timestamp
- [ ] DB package chosen based on test coverage, not star count
- [ ] Architecture layers respect the dependency rule
- [ ] BLoC does not instantiate other BLoCs inside its state
- [ ] API schema is under version control
- [ ] Production code is readable — no clever one-liners
- [ ] Scopes used for state that must survive navigation
- [ ] Auth guard implemented via scope (not route guard)
- [ ] UserEntity (auth) separated from UserInfo (profile)
- [ ] Navigator used for screen stack; Router only if URL sync needed
- [ ] Widget named `Screen`/`View`, not `Page` (Page = Navigator descriptor)
- [ ] UI Kit extracted to a local package with its own example app
- [ ] Localization split into per-feature ARB files
- [ ] Build number uses Unix timestamp, not manual increment

---

## Reference files

- `references/architecture-layers.md` — Clean Architecture layers with code examples
- `references/bloc-patterns.md` — BLoC patterns, Auth Guard, correct approaches
- `references/error-handling.md` — extended error handling, Result type, DateTime utils
- `references/scopes-navigation.md` — Scopes pattern, declarative Navigator, Pages in depth
