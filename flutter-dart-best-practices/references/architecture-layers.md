# Architecture Layers — Clean Architecture in Flutter

## Core Principle

Architecture is not about which package to use. It is a **team agreement**:
what depends on what, what is passed where, and what must never be violated.

---

## Data Layer

**Responsibility:** fetching and persisting data from any source.

```
DataSources
├── RemoteDataSource   <- HTTP API, WebSocket
└── LocalDataSource    <- local DB, SharedPreferences, files

Models / DTOs          <- JSON serialization, fromJson/toJson
Repositories (impl)    <- implement interfaces defined in Domain
```

**Rules:**
- DataSource returns raw data (Map, JSON, DTOs)
- Repository converts DTO -> Domain Entity
- Errors are rethrown with the original stack trace preserved
- Remote and Local DataSources can be combined inside a repository for caching

```dart
class NotesRepositoryImpl implements NotesRepository {
  final RemoteDataSource _remote;
  final LocalDataSource _local;

  @override
  Future<List<Note>> getNotes() async {
    try {
      final dtos = await _remote.fetchNotes();
      final notes = dtos.map((dto) => dto.toDomain()).toList();
      await _local.cacheNotes(dtos);
      return notes;
    } catch (e, st) {
      // network failed — try cache
      try {
        final cached = await _local.getCachedNotes();
        return cached.map((dto) => dto.toDomain()).toList();
      } catch (_, __) {
        Error.throwWithStackTrace(e, st); // throw original error
      }
    }
  }
}
```

---

## Domain Layer

**Responsibility:** business rules and use cases.
Does not know about UI or concrete data sources.

```
Entities       <- pure business objects (no annotations, no JSON)
Repositories   <- abstract interfaces
UseCases       <- one concrete scenario = one UseCase class
```

```dart
// Entity — pure object
class Note {
  final String id;
  final String title;
  final String content;
  final DateTime createdAt; // always UTC!

  const Note({
    required this.id,
    required this.title,
    required this.content,
    required this.createdAt,
  });
}

// Repository — interface only
abstract interface class NotesRepository {
  Future<List<Note>> getNotes();
  Future<Note> getNote(String id);
  Future<void> saveNote(Note note);
  Future<void> deleteNote(String id);
}

// UseCase — one scenario
class GetNotesUseCase {
  final NotesRepository _repository;
  GetNotesUseCase(this._repository);

  Future<List<Note>> call() => _repository.getNotes();
}
```

---

## Presentation Layer

**Responsibility:** displaying data and reacting to user actions.

```
Pages / Screens   <- full-screen pages
Widgets           <- reusable UI components
BLoC / Cubit      <- state management
```

**BLoC receives UseCases via constructor — never creates repositories itself:**

```dart
class NotesBloc extends Bloc<NotesEvent, NotesState> {
  final GetNotesUseCase _getNotesUseCase;
  final SaveNoteUseCase _saveNoteUseCase;

  NotesBloc({
    required GetNotesUseCase getNotesUseCase,
    required SaveNoteUseCase saveNoteUseCase,
  })  : _getNotesUseCase = getNotesUseCase,
        _saveNoteUseCase = saveNoteUseCase,
        super(NotesInitial()) {
    on<LoadNotes>(_onLoadNotes);
    on<SaveNote>(_onSaveNote);
  }

  Future<void> _onLoadNotes(LoadNotes event, Emitter<NotesState> emit) async {
    emit(NotesLoading());
    try {
      final notes = await _getNotesUseCase();
      emit(NotesLoaded(notes));
    } catch (e, st) {
      emit(NotesError(e.toString()));
      Error.throwWithStackTrace(e, st); // log, do not silence
    }
  }
}
```

---

## Dependency Injection

Dependencies are created once at the top level and passed down:

```dart
// main.dart or Init screen
MultiRepositoryProvider(
  providers: [
    RepositoryProvider<NotesRepository>(
      create: (_) => NotesRepositoryImpl(
        remote: RemoteDataSource(dio),
        local: LocalDataSource(db),
      ),
    ),
  ],
  child: MultiBlocProvider(
    providers: [
      BlocProvider<NotesBloc>(
        create: (ctx) => NotesBloc(
          getNotesUseCase: GetNotesUseCase(ctx.read<NotesRepository>()),
          saveNoteUseCase: SaveNoteUseCase(ctx.read<NotesRepository>()),
        ),
      ),
    ],
    child: const App(),
  ),
)
```
