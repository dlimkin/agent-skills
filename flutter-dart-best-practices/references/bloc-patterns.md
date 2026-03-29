# BLoC Patterns — Correct Usage

## Basics

BLoC (Business Logic Component) — stream-based state management.

```
UI Widget
  | (dispatches Event)
  v
BLoC
  | (calls UseCase)
  v
UseCase -> Repository -> DataSource
  |
  v (emits State)
UI Widget rebuilds
```

---

## Common Beginner Mistakes

### Instantiating a BLoC inside another BLoC's state

```dart
// BAD
class ParentBloc extends Bloc<ParentEvent, ParentState> {
  void _onSomeEvent(event, emit) {
    final childBloc = ChildBloc(); // WRONG
    emit(ParentState(childBloc: childBloc));
  }
}
```

### Correct: subscribe to another BLoC via stream

```dart
// GOOD
class ParentBloc extends Bloc<ParentEvent, ParentState> {
  final ChildBloc _childBloc;
  late final StreamSubscription _childSub;

  ParentBloc({required ChildBloc childBloc})
      : _childBloc = childBloc,
        super(ParentInitial()) {
    _childSub = _childBloc.stream.listen((childState) {
      add(ChildStateChanged(childState));
    });
  }

  @override
  Future<void> close() {
    _childSub.cancel();
    return super.close();
  }
}
```

### Business logic in widgets

```dart
// BAD
ElevatedButton(
  onPressed: () async {
    final notes = await repository.getNotes(); // logic in UI!
    setState(() => _notes = notes);
  },
)

// GOOD — UI only dispatches events
ElevatedButton(
  onPressed: () => context.read<NotesBloc>().add(LoadNotes()),
)
```

---

## Auth Guard Pattern

```dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepository _authRepository;

  AuthBloc({required AuthRepository authRepository})
      : _authRepository = authRepository,
        super(AuthInitial()) {
    on<CheckAuthStatus>(_onCheckAuth);
    on<LoggedIn>(_onLoggedIn);
    on<LoggedOut>(_onLoggedOut);
  }

  Future<void> _onCheckAuth(
    CheckAuthStatus event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());
    try {
      final user = await _authRepository.getCurrentUser();
      emit(user != null ? AuthAuthenticated(user) : AuthUnauthenticated());
    } catch (e, st) {
      emit(AuthUnauthenticated());
      Error.throwWithStackTrace(e, st);
    }
  }
}

// Init page reacts to auth state
class InitPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocListener<AuthBloc, AuthState>(
      listener: (context, state) {
        if (state is AuthAuthenticated) {
          Navigator.pushReplacementNamed(context, '/home');
        } else if (state is AuthUnauthenticated) {
          Navigator.pushReplacementNamed(context, '/auth');
        }
      },
      child: const SplashScreen(),
    );
  }
}
```

---

## BlocBuilder vs BlocListener vs BlocConsumer

| Widget | When to use |
|---|---|
| `BlocBuilder` | Only UI rebuilds on state change |
| `BlocListener` | Only side-effects (navigation, snackbar) |
| `BlocConsumer` | Both UI rebuild and side-effects |

```dart
BlocConsumer<NotesBloc, NotesState>(
  listener: (context, state) {
    if (state is NotesError) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.message)),
      );
    }
  },
  builder: (context, state) {
    return switch (state) {
      NotesLoading() => const CircularProgressIndicator(),
      NotesLoaded(:final notes) => NotesList(notes: notes),
      NotesError() => const ErrorWidget(),
      _ => const SizedBox.shrink(),
    };
  },
)
```

---

## Navigation: imperative vs declarative

```dart
// Imperative (Navigator 1.0)
Navigator.push(context, MaterialPageRoute(builder: (_) => NotePage()));

// Declarative (go_router — recommended)
context.go('/notes/${note.id}');
```

For most apps `go_router` is the reasonable choice.
Declarative navigation scales better and is easier to test.
