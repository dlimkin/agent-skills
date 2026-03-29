# Extended Error Handling in Dart / Flutter

## Dart Error Hierarchy

```
Object
├── Error       <- programming errors (bugs, should not be caught in prod)
│   ├── AssertionError
│   ├── TypeError
│   └── StateError
└── Exception   <- expected abnormal situations (should be caught and handled)
    ├── IOException
    ├── FormatException
    └── TimeoutException
```

**Rule:** extend your custom exceptions from `Exception`, not from `Error`.
`Error` = a bug in code. `Exception` = a normal abnormal situation.

---

## Pattern: Result type

For layers where you want to explicitly distinguish success from failure
without letting exceptions propagate:

```dart
sealed class Result<T> {
  const Result();
}

final class Success<T> extends Result<T> {
  final T data;
  const Success(this.data);
}

final class Failure<T> extends Result<T> {
  final Object error;
  final StackTrace stackTrace;
  const Failure(this.error, this.stackTrace);
}

// Repository returning Result
Future<Result<List<Note>>> getNotes() async {
  try {
    final notes = await _dataSource.fetchNotes();
    return Success(notes.map((e) => e.toDomain()).toList());
  } catch (e, st) {
    return Failure(e, st);
  }
}

// Handling in BLoC
final result = await _getNotesUseCase();
switch (result) {
  case Success(:final data):
    emit(NotesLoaded(data));
  case Failure(:final error, :final stackTrace):
    emit(NotesError(error.toString()));
    FirebaseCrashlytics.instance.recordError(error, stackTrace);
}
```

---

## Global Error Handler

```dart
void main() {
  // Flutter framework errors
  FlutterError.onError = (details) {
    FirebaseCrashlytics.instance.recordFlutterFatalError(details);
  };

  // Errors outside Flutter framework (isolates, async gaps)
  PlatformDispatcher.instance.onError = (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };

  runApp(const App());
}
```

---

## Mapping Network Errors (Dio)

```dart
class ApiExceptionMapper {
  static Exception map(DioException e) {
    return switch (e.type) {
      DioExceptionType.connectionTimeout =>
          const NetworkException('Connection timed out'),
      DioExceptionType.connectionError =>
          const NetworkException('No internet connection'),
      DioExceptionType.badResponse =>
          _mapStatusCode(e.response?.statusCode),
      _ => ApiException('Unknown error: ${e.message}'),
    };
  }

  static Exception _mapStatusCode(int? code) => switch (code) {
    401 => const UnauthorizedException(),
    403 => const ForbiddenException(),
    404 => const NotFoundException(),
    422 => const ValidationException(),
    500 => const ServerException(),
    _ => ApiException('HTTP error: $code'),
  };
}

// In repository
try {
  final response = await _dio.get('/notes');
  return NotesDto.fromJson(response.data);
} on DioException catch (e, st) {
  Error.throwWithStackTrace(ApiExceptionMapper.map(e), st);
}
```

---

## DateTime Utilities

```dart
class DateTimeUtils {
  /// Use for any backend/DB exchange
  static String toUtcIso(DateTime dt) => dt.toUtc().toIso8601String();

  /// Parse and convert to local for display
  static DateTime fromIso(String iso) => DateTime.parse(iso).toLocal();

  /// Unix timestamp — timezone-safe
  static int toUnixMs(DateTime dt) => dt.millisecondsSinceEpoch;
  static DateTime fromUnixMs(int ms) =>
      DateTime.fromMillisecondsSinceEpoch(ms, isUtc: true).toLocal();
}

// DTO example — using Unix timestamp (safest option)
class NoteDto {
  final String id;
  final String title;
  final int createdAtMs; // Unix timestamp

  Note toDomain() => Note(
    id: id,
    title: title,
    createdAt: DateTimeUtils.fromUnixMs(createdAtMs),
  );
}
```
