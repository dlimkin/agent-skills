# supabase-csharp

> Claude skill for working with the [Supabase C# SDK](https://github.com/supabase-community/supabase-csharp)

Gives Claude expert knowledge of the official Supabase C# library (NuGet: `supabase`). Covers the entire API surface with working code examples, common pitfalls, and idiomatic patterns for .NET, MAUI, Blazor, Unity, and ASP.NET Core.

---

## Installation

```bash
npx skills add dlimkin/agent-skills --skill supabase-csharp
```

---

## What the skill covers

Claude applies the skill automatically whenever Supabase is mentioned in a C# context — no explicit invocation needed.

### Database
- `From<T>()` queries — SELECT, INSERT, UPDATE, UPSERT, DELETE
- LINQ filters and string filters, JSON column paths (`address->street`)
- JOIN and INNER JOIN with foreign tables
- RPC — calling Postgres functions
- Pagination via `.Range()`, row counting via `.Count()`

### Filters & Modifiers
- All `Operator.*` values — comparison, patterns, arrays, null checks, full-text search
- `OR`, `NOT`, `Match`, `Contains`, `ContainedIn`
- Filtering on JSON columns and foreign tables
- Modifiers — `Order`, `Limit`, `Range`, `Single`

### Auth
- SignUp / SignIn (email, phone, password)
- Magic Link and OTP (email and SMS)
- OAuth (Google, GitHub, Apple, and more)
- Session and user management
- Session persistence via `ISupabaseSessionHandler` (MAUI / mobile)

### Realtime
- Postgres Changes — subscriptions via model and via raw channel
- Row-level filters
- Broadcast — messaging between connected clients
- Presence — tracking online status

### Storage
- Bucket management (create, update, delete, empty)
- File upload with progress callback, from byte array
- Download, move, copy, delete
- Public URL and Signed URL

### Edge Functions
- Invoke with payload and custom headers
- Typed response deserialization

---

## Skill structure

```
supabase-csharp/
├── SKILL.md                              # Overview + quick examples for every section
└── references/
    ├── database.md                       # SELECT, INSERT, UPDATE, UPSERT, DELETE, RPC, pagination
    ├── filters-modifiers.md              # All operators and modifiers with examples
    ├── auth.md                           # Auth: sign-up, sign-in, session, SessionHandler
    └── realtime-storage-functions.md     # Realtime, Storage, Edge Functions
```

---

## Example prompts

```
How do I subscribe to row-level changes for id=5 in the orders table?
```

```
Upsert by the email field instead of the primary key
```

```
Upload a file to a private bucket and generate a temporary signed URL
```

```
Implement Supabase session persistence in a MAUI app
```

---

## Compatibility

| | |
|---|---|
| Platforms | .NET 6+, MAUI, Blazor, Unity, ASP.NET Core |
| NuGet package | [`supabase`](https://www.nuget.org/packages/supabase) |
| Documentation | [supabase.com/docs/reference/csharp](https://supabase.com/docs/reference/csharp/introduction) |
| Library repository | [supabase-community/supabase-csharp](https://github.com/supabase-community/supabase-csharp) |
