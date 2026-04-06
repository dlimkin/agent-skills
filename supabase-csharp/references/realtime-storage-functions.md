# Realtime, Storage, Edge Functions — Полный справочник

> Читать когда: нужны подробные примеры Realtime-подписок (Broadcast, Presence, Postgres Changes), операций с файлами, или вызовов Edge Functions.

---

## REALTIME

### Предварительные требования
1. Включить репликацию: Dashboard → Database → Replication → включить нужные таблицы
2. Чтобы получать старые значения при UPDATE/DELETE: `ALTER TABLE your_table REPLICA IDENTITY FULL;`

---

### Postgres Changes — через модель (простой способ)

```csharp
// Все изменения (Insert + Update + Delete)
await supabase.From<City>().On(ListenType.All, (sender, change) =>
{
    Console.WriteLine(change.Payload.Data);
});

// Только вставки
await supabase.From<City>().On(ListenType.Inserts, (sender, change) =>
{
    var newCity = change.Model<City>();
    Console.WriteLine($"Новый город: {newCity.Name}");
});

// Только обновления
await supabase.From<City>().On(ListenType.Updates, (sender, change) =>
{
    Console.WriteLine(change.Payload.Data);
});

// Только удаления
await supabase.From<City>().On(ListenType.Deletes, (sender, change) =>
{
    Console.WriteLine(change.Payload.Data);
});
```

---

### Postgres Changes — через канал (полный контроль)

```csharp
// Все изменения во всех таблицах публичной схемы
var channel = supabase.Realtime.Channel("realtime", "public", "*");

channel.AddPostgresChangeHandler(ListenType.All, (sender, change) =>
{
    Console.WriteLine($"Событие: {change.Event}");
    Console.WriteLine($"Таблица: {change.Payload.Table}");
    Console.WriteLine($"Данные: {change.Payload.Data}");
});

await channel.Subscribe();
```

### Фильтр по конкретной строке (Row-Level)

```csharp
// Слушать изменения только строки с id = 200 в таблице countries
var channel = supabase.Realtime.Channel(
    "realtime",   // тип
    "public",     // схема
    "countries",  // таблица
    "id",         // колонка
    "id=eq.200"   // фильтр
);

channel.AddPostgresChangeHandler(ListenType.All, (sender, change) =>
{
    Console.WriteLine(change.Payload);
});

await channel.Subscribe();
```

---

### Broadcast (отправка сообщений между клиентами)

```csharp
// Определить тип сообщения
class CursorBroadcast : BaseBroadcast
{
    [JsonProperty("cursorX")] public int CursorX { get; set; }
    [JsonProperty("cursorY")] public int CursorY { get; set; }
}

// Создать канал и подписаться
var channel   = supabase.Realtime.Channel("cursor-room");
var broadcast = channel.Register<CursorBroadcast>();

broadcast.AddBroadcastEventHandler((sender, msg) =>
{
    var cursor = broadcast.Current();
    Console.WriteLine($"X: {cursor?.CursorX}, Y: {cursor?.CursorY}");
});

await channel.Subscribe();

// Отправить сообщение всем в канале
await broadcast.Send("cursor", new CursorBroadcast { CursorX = 123, CursorY = 456 });
```

---

### Presence (отслеживание онлайн-состояния)

```csharp
// Определить тип состояния
class UserPresence : BasePresence
{
    [JsonProperty("isTyping")] public bool IsTyping   { get; set; }
    [JsonProperty("onlineAt")] public DateTime OnlineAt { get; set; }
}

var channel     = supabase.Realtime.Channel("typing-room");
var presenceKey = Guid.NewGuid().ToString();   // уникальный ключ клиента
var presence    = channel.Register<UserPresence>(presenceKey);

// Обработчики событий Presence
presence.AddPresenceEventHandler(EventType.Sync, (sender, type) =>
{
    // Вызывается при синхронизации состояния (начальная загрузка)
    var state = presence.CurrentState;
    foreach (var (key, value) in state)
        Console.WriteLine($"{key}: IsTyping={value.First().IsTyping}");
});

presence.AddPresenceEventHandler(EventType.Join, (sender, type) =>
{
    Console.WriteLine("Кто-то подключился");
});

presence.AddPresenceEventHandler(EventType.Leave, (sender, type) =>
{
    Console.WriteLine("Кто-то отключился");
});

await channel.Subscribe();

// Обновить своё состояние
await presence.Track(new UserPresence
{
    IsTyping = true,
    OnlineAt = DateTime.UtcNow
});

// Перестать отслеживаться
await presence.Untrack();
```

---

### Управление каналами

```csharp
// Отписаться от канала
await supabase.Realtime.RemoveChannel(channel);

// Получить список всех активных каналов
var channels = supabase.Realtime.GetChannels();

// Отписаться от всех каналов
await supabase.Realtime.RemoveAllChannels();
```

---

## STORAGE

### Управление бакетами

```csharp
// Список всех бакетов
var buckets = await supabase.Storage.ListBuckets();

// Получить бакет по имени
var bucket = await supabase.Storage.GetBucket("avatars");

// Создать бакет
await supabase.Storage.CreateBucket("avatars",
    new BucketUpsertOptions { Public = true });   // Public = false — приватный

// Обновить настройки бакета
await supabase.Storage.UpdateBucket("avatars",
    new BucketUpsertOptions { Public = false });

// Очистить бакет (удалить все файлы, оставить сам бакет)
await supabase.Storage.EmptyBucket("avatars");

// Удалить бакет (бакет должен быть пустым)
await supabase.Storage.DeleteBucket("avatars");
```

---

### Загрузка файлов

```csharp
var storage = supabase.Storage.From("avatars");

// Простая загрузка
await storage.Upload(
    "Assets/photo.png",         // локальный путь
    "users/alice/photo.png",    // путь в бакете
    new FileOptions
    {
        CacheControl = "3600",  // Cache-Control заголовок в секундах
        Upsert = false          // true = перезаписать если существует
    });

// С прогрессом
await storage.Upload(
    "Assets/photo.png",
    "users/alice/photo.png",
    onProgress: (sender, pct) => Console.WriteLine($"Загружено: {pct}%"));

// Из байтового массива
var bytes = File.ReadAllBytes("Assets/photo.png");
await storage.Upload(
    bytes,
    "users/alice/photo.png",
    new FileOptions { ContentType = "image/png" });
```

---

### Обновление, перемещение, удаление

```csharp
var storage = supabase.Storage.From("avatars");

// Заменить существующий файл
await storage.Update("Assets/photo-new.png", "users/alice/photo.png",
    new FileOptions { CacheControl = "3600" });

// Переместить файл внутри бакета
await storage.Move("users/alice/photo.png", "users/alice/avatar.png");

// Скопировать файл
await storage.Copy("users/alice/photo.png", "backup/alice/photo.png");

// Удалить файлы (список путей)
await storage.Remove(new List<string>
{
    "users/alice/photo.png",
    "users/alice/avatar.png"
});
```

---

### Скачивание

```csharp
var storage = supabase.Storage.From("avatars");

// Скачать в память
var bytes = await storage.Download("users/alice/photo.png", null);

// С прогрессом
var bytes = await storage.Download("users/alice/photo.png",
    (sender, pct) => Console.WriteLine($"Скачано: {pct}%"));

// Сохранить на диск
await File.WriteAllBytesAsync("Downloads/photo.png", bytes);
```

---

### URL файлов

```csharp
var storage = supabase.Storage.From("avatars");

// Публичный URL (только для Public бакетов)
var publicUrl = storage.GetPublicUrl("users/alice/photo.png");

// Signed URL (временная ссылка, работает для приватных бакетов)
var signedUrl = await storage.CreateSignedUrl(
    "users/alice/photo.png",
    expiresIn: 3600);   // секунды

// Несколько Signed URL за раз
var signedUrls = await storage.CreateSignedUrls(
    new List<string> { "file1.png", "file2.png" },
    expiresIn: 3600);
```

---

### Список файлов в бакете

```csharp
var storage = supabase.Storage.From("avatars");

// Все файлы в корне
var files = await storage.List();

// Файлы в папке
var files = await storage.List("users/alice/");

// С параметрами
var files = await storage.List("users/alice/", new SearchOptions
{
    Limit  = 50,
    Offset = 0,
    SortBy = new SortBy { Column = "name", Order = "asc" }
});
```

---

## EDGE FUNCTIONS

```csharp
// Простой вызов без параметров
await supabase.Functions.Invoke("hello-world");

// С body и заголовками
var options = new InvokeFunctionOptions
{
    Headers = new Dictionary<string, string>
    {
        { "Authorization", $"Bearer {session.AccessToken}" }
    },
    Body = new Dictionary<string, object>
    {
        { "name", "Alice" },
        { "count", 42 }
    }
};
await supabase.Functions.Invoke("my-function", options: options);

// С типизированным ответом
class HelloResponse
{
    [JsonProperty("message")] public string Message { get; set; }
}

var result = await supabase.Functions.Invoke<HelloResponse>("hello", options: options);
Console.WriteLine(result.Message);
```

> **Примечание:** Authorization заголовок обязателен для Edge Functions. Если клиент уже авторизован через `supabase.Auth`, токен подставляется автоматически.
