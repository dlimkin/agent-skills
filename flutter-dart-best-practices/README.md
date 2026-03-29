# Flutter & Dart Best Practices Skill

A skill for AI coding agents that teaches how to avoid common Flutter and Dart mistakes — including proper error handling, Clean Architecture, BLoC patterns, local database selection, DateTime pitfalls, and navigation.

## Installation

```bash
npx skills add dlimkin/agent-skills --skill flutter-dart-best-practices
```

## What this skill does

- Enforces correct error handling: no silent catch blocks, always preserve stack traces
- Applies Clean Architecture with proper layer separation (Data / Domain / Presentation)
- Implements BLoC pattern correctly: no BLoC-in-BLoC, no business logic in widgets
- Selects local databases based on test coverage and isolation support, not star count
- Handles DateTime safely: UTC or Unix timestamp for all backend/DB exchanges
- Implements Auth Guard pattern for navigation flow
- Reviews code against a practical checklist of the most common production mistakes

## Covered Topics

| Topic | Description |
|-------|-------------|
| Error handling | `try/catch` anti-patterns, `Error.throwWithStackTrace`, preserving stack traces |
| Result type | `sealed class Result<T>` pattern for explicit success/failure handling |
| Network errors | Mapping `DioException` to domain exceptions with status code handling |
| Global error handler | `FlutterError.onError` + `PlatformDispatcher.instance.onError` setup |
| Local databases | Criteria for package selection: test coverage, transactions, concurrency |
| DateTime | Why `DateTime.now().toString()` is dangerous; UTC ISO and Unix timestamp patterns |
| Clean Architecture | 3-layer structure, dependency rule, entity/repository/use-case definitions |
| Dependency injection | `Provider` / `get_it` setup, passing dependencies top-down |
| BLoC pattern | Events, states, correct inter-BLoC communication via streams |
| BlocBuilder/Listener | When to use `BlocBuilder` vs `BlocListener` vs `BlocConsumer` |
| Auth Guard | `AuthBloc` as a gatekeeper, `SplashScreen` while checking auth status |
| Navigation | Imperative vs declarative (go_router), API schema under version control |
| Code readability | Why "clever" code hurts teams; conciseness vs terseness |
| Performance myths | Why correct algorithms beat "fast" packages every time |

## Links

- [Flutter Documentation](https://docs.flutter.dev)
- [Dart Language Tour](https://dart.dev/language)
- [flutter_bloc package](https://pub.dev/packages/flutter_bloc)
- [go_router package](https://pub.dev/packages/go_router)
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Effective Dart](https://dart.dev/effective-dart)
- [pub.dev](https://pub.dev)
