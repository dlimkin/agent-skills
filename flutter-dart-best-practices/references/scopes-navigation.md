# Scopes & Declarative Navigation in Flutter

## The Scopes Pattern

### What is a Scope?

A **Scope** is a `StatefulWidget` (usually backed by `InheritedModel`) placed above
the Navigator in the widget tree. It:
- Provides state/dependencies to everything nested below it
- Can act as a guard (show alternative UI instead of child)
- Can display overlays above all screens (using Overlay.of)
- Exposes static helper methods for clean call-site API

### Widget Tree Structure

```
runApp()
  └── DependencyInjection (repos, services)
        └── MaterialApp
              └── MaterialApp.builder:
                    ├── ApplicationScope    (version check, force-update dialog)
                    │     └── AuthScope     (auth guard, user context)
                    │           └── SettingsScope
                    │                 └── ChatListScope
                    │                       └── Navigator  ← screen stack
```

### Minimal Scope Implementation

```dart
class CartScope extends StatefulWidget {
  const CartScope({super.key, required this.child});
  final Widget child;

  // Static helpers — clean API, no extra imports at call site
  static CartController of(BuildContext context) =>
      InheritedModel.inheritFrom<_CartInherited>(context)!.controller;

  static void addItem(BuildContext context, CartItem item) =>
      of(context).addItem(item);

  @override
  State<CartScope> createState() => _CartScopeState();
}

class _CartScopeState extends State<CartScope> {
  late final CartController _controller;

  @override
  void initState() {
    super.initState();
    _controller = CartController(
      repository: context.read<CartRepository>(),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => _CartInherited(
        controller: _controller,
        child: widget.child,
      );
}

class _CartInherited extends InheritedModel<String> {
  const _CartInherited({required this.controller, required super.child});
  final CartController controller;

  @override
  bool updateShouldNotify(_CartInherited old) => controller != old.controller;

  // Granular subscriptions — only rebuild for the aspect that changed
  @override
  bool updateShouldNotifyDependent(_CartInherited old, Set<String> deps) {
    if (deps.contains('count') && controller.count != old.controller.count) {
      return true;
    }
    if (deps.contains('items') && controller.items != old.controller.items) {
      return true;
    }
    return false;
  }
}
```

---

## Auth Guard via Scope

```dart
class AuthScope extends StatefulWidget {
  const AuthScope({super.key, required this.child});
  final Widget child; // the authenticated app content

  static UserEntity userOf(BuildContext context) =>
      InheritedModel.inheritFrom<_AuthInherited>(context)!.user;

  static void logout(BuildContext context, {VoidCallback? onSuccess}) =>
      _AuthScopeState._of(context)._controller.logout(onSuccess: onSuccess);

  static void authenticatedOr(
    BuildContext context, {
    required void Function(UserEntity user) onAuthenticated,
    VoidCallback? onUnauthenticated,
  }) {
    final user = userOf(context);
    if (user is AuthenticatedUser) {
      onAuthenticated(user);
    } else {
      onUnauthenticated?.call();
    }
  }
}

class _AuthScopeState extends State<AuthScope> {
  late final AuthController _controller;

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: _controller,
      builder: (context, _) {
        final user = _controller.currentUser;

        return _AuthInherited(
          user: user,
          child: user is AuthenticatedUser
              ? widget.child  // show the whole app
              : _AuthNavigator(), // show only login/register screens
        );
      },
    );
  }
}

class _AuthNavigator extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Navigator(
      pages: const [SignInPage()],
      onDidRemovePage: (_) {},
    );
  }
}
```

---

## Declarative Navigator

### Core Concept

```dart
class AppNavigator extends StatefulWidget {
  // Navigator state = list of Pages
  // To navigate = transform that list
}

class _AppNavigatorState extends State<AppNavigator> {
  List<Page<dynamic>> _pages = const [ChatPage()];

  // THE core method — receives current, returns desired
  void change(List<Page> Function(List<Page> current) transform) {
    setState(() => _pages = transform(List.of(_pages)));
  }

  @override
  Widget build(BuildContext context) {
    return Navigator(
      pages: _pages,
      onDidRemovePage: (_) => change((p) => p..removeLast()),
    );
  }
}
```

### All Navigation Operations via change()

```dart
// Push
navigator.change((pages) => [...pages, ProductPage(id: '42')]);

// Pop
navigator.change((pages) => pages.length > 1 ? (pages..removeLast()) : pages);

// Reset to root
navigator.change((_) => [const HomePage()]);

// Ensure unique (go to settings, no duplicates)
navigator.change((pages) => [
  ...pages.where((p) => p is! SettingsPage),
  const SettingsPage(),
]);

// Handle deep link (open product on top of home)
navigator.change((_) => [const HomePage(), ProductPage(id: deepLinkId)]);
```

### Pages vs Screens — Naming Convention

| Name suffix | What it is | Example |
|---|---|---|
| `Screen` / `View` | The actual widget | `ChatScreen extends StatelessWidget` |
| `Page` | Navigator descriptor, NOT a widget | `ChatPage extends Page<void>` |

```dart
// Page holds the key and creates the Route/Screen
sealed class AppPage extends Page<void> {
  const AppPage({super.key});
}

final class ChatPage extends AppPage {
  const ChatPage() : super(key: const ValueKey('chat'));

  @override
  Route<void> createRoute(BuildContext context) => MaterialPageRoute(
        settings: this,
        builder: (_) => const ChatScreen(),
      );
}

final class ProductPage extends AppPage {
  const ProductPage({required this.productId})
      : super(key: ValueKey('product-$productId'));

  final String productId;

  @override
  Route<void> createRoute(BuildContext context) => MaterialPageRoute(
        settings: this,
        builder: (_) => ProductScreen(productId: productId),
      );
}
```

### Navigator vs Router

| | Navigator | Router |
|---|---|---|
| **Purpose** | Screen stack with transitions | Sync state with platform (URL, back button) |
| **Required for** | All apps | Web URL support, OS deep links parsing |
| **Depends on each other?** | No | No — fully independent |

**Rule:** Start with Navigator only. Add Router only when you need URL sync.

### Deep Links Without Router

```dart
// main.dart — read the launch URL before showing any UI
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // The URL/route that launched the app
  final initialRoute = PlatformDispatcher.instance.defaultRouteName;
  // e.g. "/" or "/product/42" or "myapp://settings"

  runApp(App(initialRoute: initialRoute));
}

// In AppNavigator initState — build initial page stack from the route
List<Page> _buildInitialPages(String route) {
  if (route.startsWith('/product/')) {
    final id = route.split('/').last;
    return [const HomePage(), ProductPage(id: id)];
  }
  if (route == '/settings') {
    return [const HomePage(), const SettingsPage()];
  }
  return [const HomePage()];
}
```

---

## Local Packages — Extraction Rules

### Extract to Local Package

| What | Why |
|---|---|
| `packages/ui` — UI Kit | Compile separately, preview on desktop, share with designers |
| `packages/l10n` — Localization | Auto-generated, changes independently |
| Local forks of buggy packages | Fix quickly without waiting for pub.dev |
| Database layer (optional) | Changes independently, easy to mock in tests |

### Do NOT Extract

- Individual features / screens — adds complexity, zero benefit
- Single classes or utilities — just put them in the main lib
- Everything — monolith packages are fine, don't over-engineer

### UI Kit Package Setup

```
packages/ui/
├── pubspec.yaml          (name: ui, publish_to: none)
├── lib/
│   ├── ui.dart           (barrel export)
│   ├── src/
│   │   ├── components/   (buttons, cards, inputs)
│   │   ├── icons.dart    (icon font class)
│   │   ├── typography.dart
│   │   └── theme.dart
│   └── fonts/
│       └── app_icons.ttf (generated by IconMoon)
└── example/              (flutter create --template=app example)
    └── lib/
        └── main.dart     (catalog of all components)
```

```yaml
# root pubspec.yaml
workspace:
  - packages/ui
  - packages/l10n
```

### Icon Strategy

```
Raster PNG (fixed size, fixed color)  →  Sprite Atlas
Custom icons (multiple colors/sizes)  →  Icon Font (IconMoon → TTF)
Logos / scalable graphics             →  Canvas (CustomPainter / LeafRenderObjectWidget)
SVG at runtime                        →  Avoid — parsed by Dart every build, slow
```

```dart
// Icon font usage
abstract final class AppIcons {
  static const IconData instagram = IconData(
    0xe900, // glyph code from IconMoon
    fontFamily: 'AppIcons',
    fontPackage: 'ui', // required when icon font is in a local package
  );
}
```
