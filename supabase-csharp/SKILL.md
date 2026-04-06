---
name: supabase-csharp
description: >
  Expert knowledge of the Supabase C# client library (NuGet: supabase). Use this skill whenever
  the user works with Supabase in C#, .NET, MAUI, Unity, Blazor, or any C#-based project —
  including tasks like setting up the client, querying a database, authenticating users, subscribing
  to realtime events, managing storage buckets, or invoking Edge Functions. Trigger on any mention
  of "Supabase", "supabase-csharp", "postgrest-csharp", "BaseModel", "supabase.From()", or
  questions about connecting C# / .NET apps to Supabase backends. Always use this skill before
  writing any Supabase-related C# code — it contains idiomatic patterns, gotchas, and complete
  working examples.
---

# Supabase C# SDK — Complete Reference Skill

> Official NuGet package: `supabase` · Community-maintained · [GitHub](https://github.com/supabase-community/supabase-csharp)

## Table of Contents
1. [Installation & Initialization](#1-installation--initialization)
2. [Data Modeling (BaseModel)](#2-data-modeling-basemodel)
3. [Database — CRUD](#3-database--crud)
4. [Filters & Modifiers](#4-filters--modifiers)
5. [Auth](#5-auth)
6. [Realtime](#6-realtime)
7. [Storage](#7-storage)
8. [Edge Functions](#8-edge-functions)
9. [Common Gotchas & Best Practices](#9-common-gotchas--best-practices)

## Reference files (читать по необходимости)

| Файл | Содержимое |
|---|---|
| `references/database.md` | Все варианты SELECT (JOIN, JSON, COUNT, Single), INSERT (bulk, returning), UPDATE (Set/model), UPSERT (OnConflict), DELETE, RPC, пагинация |
| `references/filters-modifiers.md` | Полная таблица операторов Operator.*, LINQ vs string, JSON-пути, Foreign Table фильтры, OR/NOT, все модификаторы с параметрами |
| `references/auth.md` | SignUp с метаданными, SignIn (email/phone/OTP/OAuth), VerifyOtp, GetSession/GetUser, UpdateUser, StateChanged listener, реализация ISupabaseSessionHandler |
| `references/realtime-storage-functions.md` | Postgres Changes (модель и канал), Row-Level фильтр, Broadcast, Presence (Track/Untrack/EventType), управление каналами; Storage (бакеты, upload/update/move/copy/delete/download/list, URL); Edge Functions с типизированным ответом |

---

## 1. Installation & Initialization

```bash
dotnet add package supabase
```

### Standard initialization
```csharp
var url = Environment.GetEnvironmentVariable("SUPABASE_URL");
var key = Environment.GetEnvironmentVariable("SUPABASE_KEY");

var options = new Supabase.SupabaseOptions
{
    AutoConnectRealtime = true
};

var supabase = new Supabase.Client(url, key, options);
await supabase.InitializeAsync();
```

### Dependency Injection (MAUI / ASP.NET Core)
```csharp
builder.Services.AddSingleton(provider => new Supabase.Client(
    url, key,
    new SupabaseOptions
    {
        AutoRefreshToken = true,
        AutoConnectRealtime = true,
        // SessionHandler = new SupabaseSessionHandler() // implement for token persistence
    }
));
```

**Key options:**

| Option | Default | Purpose |
|---|---|---|
| `AutoConnectRealtime` | false | Connect to WebSocket on init |
| `AutoRefreshToken` | true | Auto-refresh JWT before expiry |
| `SessionHandler` | null | Custom session persistence (must implement `ISupabaseSessionHandler`) |

---

## 2. Data Modeling (BaseModel)

Every table interaction requires a model class derived from `BaseModel`.

```csharp
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

[Table("messages")]
public class Message : BaseModel
{
    [PrimaryKey("id")]
    public int Id { get; set; }

    [Column("username")]
    public string UserName { get; set; }

    [Column("channel_id")]
    public int ChannelId { get; set; }

    [Column("created_at")]
    public DateTime CreatedAt { get; set; }

    // Required for equality checks in collections
    public override bool Equals(object obj) =>
        obj is Message m && Id == m.Id;

    public override int GetHashCode() => HashCode.Combine(Id);
}
```

**Rules:**
- `[Table("db_table_name")]` — maps class to table
- `[PrimaryKey("col")]` — marks the PK; required for `Update()` / `Delete()`
- `[Column("col")]` — maps property to column; name must match the **database** column name when used in string filters
- Properties without `[Column]` are ignored by the serializer
- LINQ `.Select(x => ...)` does **not** support embedded/foreign columns — use string overload for joins

---

## 3. Database — CRUD

### Fetch (SELECT)
```csharp
// All rows
var result = await supabase.From<Message>().Get();
List<Message> messages = result.Models;

// Specific columns via LINQ
var result = await supabase.From<Movie>()
    .Select(x => new object[] { x.Name, x.CreatedAt })
    .Get();

// Foreign table join (string form required)
var data = await supabase
    .From<Transaction>()
    .Select("id, supplier:supplier_id(name), purchaser:purchaser_id(name)")
    .Get();

// JSON column drill-down
var result = await supabase
    .From<User>()
    .Select("id, name, address->street")
    .Filter("address->postcode", Operator.Equals, 90210)
    .Get();

// Count only
var count = await supabase
    .From<Movie>()
    .Count(CountType.Exact);
```

### Insert
```csharp
var newMessage = new Message { UserName = "alice", ChannelId = 1 };
var result = await supabase.From<Message>().Insert(newMessage);
Message inserted = result.Model;
```

### Update
```csharp
// Via model instance (PrimaryKey must be set)
model.UserName = "bob";
await model.Update<Message>();

// Via query
await supabase.From<Message>()
    .Where(x => x.Id == 42)
    .Set(x => x.UserName, "bob")
    .Update();
```

### Upsert
```csharp
await supabase.From<Message>().Upsert(new Message { Id = 1, UserName = "alice" });
```

### Delete
```csharp
// Via model instance
await model.Delete<Message>();

// Via query
await supabase.From<Message>()
    .Where(x => x.Id == 42)
    .Delete();
```

### Call Postgres Function (RPC)
```csharp
var result = await supabase.Rpc("function_name", new Dictionary<string, object>
{
    { "param1", "value" }
});
```

---

## 4. Filters & Modifiers

Filters chain after `.From<T>()`:

```csharp
// Equality
.Filter("column", Operator.Equals, value)
.Where(x => x.Status == "active")   // LINQ shorthand

// Comparison
.Filter("price", Operator.GreaterThan, 100)
.Filter("price", Operator.LessThanOrEqual, 500)

// Pattern matching
.Filter("name", Operator.Like, "%Alice%")
.Filter("name", Operator.ILike, "%alice%")  // case-insensitive

// Null check
.Filter("deleted_at", Operator.Is, null)

// In list
.Filter("status", Operator.In, new List<string> { "active", "pending" })

// Contains (array/JSONB)
.Filter("tags", Operator.Contains, new List<string> { "csharp" })

// Text search
.Filter("fts", Operator.TextSearch, "'supab' & 'base'")

// NOT / OR
.Not("status", Operator.Equals, "deleted")
.Or("status.eq.active,status.eq.pending")
```

**Modifiers** (chain after filters):

```csharp
.Order("created_at", Ordering.Descending)
.Limit(10)
.Range(0, 24)        // pagination: rows 0–24 inclusive
.Single()            // returns one row, throws if 0 or >1
```

> **Default row limit:** Supabase returns max **1,000 rows** by default. Use `.Range()` for pagination.

---

## 5. Auth

```csharp
// Sign up
var session = await supabase.Auth.SignUp(email, password);

// Sign in with password
var session = await supabase.Auth.SignInWithPassword(email, password);

// Sign in with OTP (magic link)
await supabase.Auth.SignInWithOtp(new SignInWithPasswordlessEmailOptions(email));

// OAuth (returns URL to redirect user to)
var signInUrl = await supabase.Auth.SignInWithOAuth(Provider.Google);

// Sign out
await supabase.Auth.SignOut();

// Verify OTP
var session = await supabase.Auth.VerifyOTP(email, token, EmailOtpType.Email);

// Session & user
var session = await supabase.Auth.GetSession();
var user    = await supabase.Auth.GetUser(session.AccessToken);

// Update user (e.g. change email or password)
await supabase.Auth.UpdateUser(new UserAttributes { Email = "new@email.com" });

// Listen to auth state changes
supabase.Auth.AddStateChangedListener((sender, state) =>
{
    Debug.WriteLine($"Auth state changed: {state}");
});
```

**Behaviour notes:**
- `SignUp` returns `user` + `session`. If **Confirm email** is enabled in dashboard, `session` is `null` until confirmed.
- If you call `SignUp` for an existing confirmed user with both confirmations enabled, a fake/obfuscated user object is returned (not an error).

---

## 6. Realtime

> Enable replication in Supabase Dashboard → Database → Replication before using.

```csharp
// --- Postgres changes on a model ---
await supabase.From<City>().On(ListenType.All, (sender, change) =>
{
    Debug.WriteLine(change.Payload.Data);
});

// Only inserts / updates / deletes:
await supabase.From<City>().On(ListenType.Inserts, handler);
await supabase.From<City>().On(ListenType.Updates, handler);
await supabase.From<City>().On(ListenType.Deletes, handler);

// --- Raw channel (full control) ---
var channel = supabase.Realtime.Channel("realtime", "public", "*");
channel.AddPostgresChangeHandler(ListenType.All, (sender, change) =>
{
    Debug.WriteLine(change.Event);
    Debug.WriteLine(change.Payload);
});
await channel.Subscribe();

// Row-level filter
var channel = supabase.Realtime.Channel("realtime", "public", "countries", "id", "id=eq.200");

// --- Broadcast ---
class CursorBroadcast : BaseBroadcast
{
    [JsonProperty("cursorX")] public int CursorX { get; set; }
    [JsonProperty("cursorY")] public int CursorY { get; set; }
}

var channel   = supabase.Realtime.Channel("cursor-room");
var broadcast = channel.Register<CursorBroadcast>();
broadcast.AddBroadcastEventHandler((sender, msg) => { var cur = broadcast.Current(); });
await channel.Subscribe();
await broadcast.Send("cursor", new CursorBroadcast { CursorX = 10, CursorY = 20 });

// --- Presence ---
class UserPresence : BasePresence
{
    [JsonProperty("isTyping")] public bool IsTyping { get; set; }
    [JsonProperty("onlineAt")] public DateTime OnlineAt { get; set; }
}

var channel  = supabase.Realtime.Channel("typing-room");
var key      = Guid.NewGuid().ToString();
var presence = channel.Register<UserPresence>(key);
presence.AddPresenceEventHandler(EventType.Sync, (sender, type) =>
{
    var state = presence.CurrentState;
});
await channel.Subscribe();
await presence.Track(new UserPresence { IsTyping = true, OnlineAt = DateTime.Now });

// Unsubscribe
await supabase.Realtime.RemoveChannel(channel);

// List all channels
var channels = supabase.Realtime.GetChannels();
```

> To receive `old` values on UPDATE/DELETE, run: `ALTER TABLE your_table REPLICA IDENTITY FULL;`

---

## 7. Storage

### Buckets
```csharp
// List / get / create / update / delete / empty
var buckets = await supabase.Storage.ListBuckets();
var bucket  = await supabase.Storage.GetBucket("avatars");

await supabase.Storage.CreateBucket("avatars", new BucketUpsertOptions { Public = true });
await supabase.Storage.UpdateBucket("avatars", new BucketUpsertOptions { Public = false });
await supabase.Storage.EmptyBucket("avatars");
await supabase.Storage.DeleteBucket("avatars");
```

### File operations
```csharp
var storage = supabase.Storage.From("avatars");

// Upload
await storage.Upload("Assets/photo.png", "photo.png",
    new FileOptions { CacheControl = "3600", Upsert = false });

// Upload with progress callback
await storage.Upload("Assets/photo.png", "photo.png",
    onProgress: (sender, pct) => Debug.WriteLine($"{pct}%"));

// Replace (update)
await storage.Update("Assets/photo-new.png", "photo.png",
    new FileOptions { CacheControl = "3600" });

// Move
await storage.Move("old/path.png", "new/path.png");

// Download
var bytes = await storage.Download("photo.png", (sender, pct) => Debug.WriteLine($"{pct}%"));

// Delete
await storage.Remove(new List<string> { "photo.png", "avatar.jpg" });

// List files
var files = await storage.List("folder/");

// URLs
var publicUrl = storage.GetPublicUrl("photo.png");
var signedUrl = await storage.CreateSignedUrl("photo.png", expiresIn: 3600);
```

---

## 8. Edge Functions

```csharp
// Basic invocation
var response = await supabase.Functions.Invoke("function-name",
    new Dictionary<string, object> { { "key", "value" } });

// With typed response
var result = await supabase.Functions.Invoke<MyResponseType>("function-name", payload);
```

---

## 9. Common Gotchas & Best Practices

| # | Issue | Solution |
|---|---|---|
| 1 | LINQ `.Select()` breaks on foreign/embedded columns | Use string overload: `.Select("*, users(name)")` |
| 2 | String column names in `.Filter()` must match **database** names, not C# property names | Use `[Column]` attribute value, not property name |
| 3 | Default 1,000 row cap | Use `.Range(from, to)` for pagination |
| 4 | `apikey` is reserved by API gateway | Never name a column `apikey` |
| 5 | Realtime not receiving old values on UPDATE | Run `ALTER TABLE t REPLICA IDENTITY FULL;` |
| 6 | Realtime disabled by default | Enable via Dashboard → Replication |
| 7 | `SignUp` returns null session when email confirmation is ON | Check `session != null` before using tokens |
| 8 | `InitializeAsync()` must be awaited | Not awaiting skips Realtime connection setup |
| 9 | Singleton DI pattern required | Never register `Supabase.Client` as transient |
| 10 | Session persistence in MAUI/mobile | Implement `ISupabaseSessionHandler` and pass via options |

---

## Quick-Reference: Method Chaining Pattern

```
supabase
  .From<TModel>()           // target table
  [.Select(...)]            // columns
  [.Filter() / .Where()]    // WHERE clause
  [.Order() / .Limit() / .Range() / .Single()]   // modifiers
  .Get() / .Insert() / .Update() / .Delete() / .Upsert() / .Count()
```

Auth lives at: `supabase.Auth.*`
Storage lives at: `supabase.Storage.From("bucket").*`
Realtime lives at: `supabase.Realtime.*` or `supabase.From<T>().On(...)`
Edge Functions live at: `supabase.Functions.Invoke(...)`
