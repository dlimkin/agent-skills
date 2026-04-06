# Фильтры и Модификаторы — Полный справочник

> Читать когда: нужна конкретная комбинация операторов или модификаторов, примеры с Foreign Table фильтрацией, JSON-путями, LINQ vs string.

---

## Два стиля записи фильтров

```csharp
// LINQ (работает только с простыми колонками модели)
.Where(x => x.Status == "active")

// String / Operator (работает везде: JSON, Foreign Tables, встроенные ресурсы)
.Filter("status", Operator.Equals, "active")
```

> **Правило:** используйте LINQ для простых полей модели. Для JSON-путей (`address->city`) и вложенных таблиц — только строковый вариант.

---

## Все операторы Operator.*

### Сравнение
```csharp
.Filter("price", Operator.Equals,             100)    // eq
.Filter("price", Operator.NotEquals,          100)    // neq
.Filter("price", Operator.GreaterThan,        100)    // gt
.Filter("price", Operator.GreaterThanOrEqual, 100)    // gte
.Filter("price", Operator.LessThan,           100)    // lt
.Filter("price", Operator.LessThanOrEqual,    100)    // lte
```

### Строковые паттерны
```csharp
.Filter("name", Operator.Like,  "%Alice%")   // LIKE — чувствителен к регистру
.Filter("name", Operator.ILike, "%alice%")   // ILIKE — нечувствителен к регистру
```

### Null / булевы проверки
```csharp
.Filter("deleted_at", Operator.Is,    null)
.Filter("deleted_at", Operator.IsNot, null)
.Filter("is_active",  Operator.Is,    true)
```

### Массивы и диапазоны
```csharp
// Значение входит в список
.Filter("status", Operator.In,
    new List<string> { "active", "pending", "paused" })

// Массив-колонка содержит ВСЕ указанные элементы
.Filter("tags", Operator.Contains,
    new List<string> { "csharp", "dotnet" })

// Массив-колонка содержится ВНУТРИ указанного списка
.Filter("tags", Operator.ContainedIn,
    new List<string> { "csharp", "dotnet", "fsharp" })
```

### Полнотекстовый поиск
```csharp
.Filter("fts", Operator.TextSearch, "'supab' & 'base'")
// Колонка fts должна быть типа tsvector
```

### Match (точное совпадение нескольких полей)
```csharp
.Match(new Dictionary<string, string>
{
    { "status", "active" },
    { "country_id", "42" }
})
```

### NOT и OR
```csharp
// NOT: инвертирует любой оператор
.Not("status", Operator.Equals, "deleted")

// OR: строковый синтаксис PostgREST
.Or("status.eq.active,status.eq.pending")

// OR по внешней таблице
.Or("name.eq.Paris,name.eq.London", foreignTable: "cities")
```

---

## Фильтрация по JSON-колонкам

```csharp
// Drill-down через -> (возвращает JSON) или ->> (возвращает текст)
.Filter("address->postcode", Operator.Equals, 90210)
.Filter("metadata->>'key'", Operator.Equals, "value")

// В SELECT тоже можно
var result = await supabase
    .From<User>()
    .Select("id, name, address->street")
    .Filter("address->postcode", Operator.Equals, 90210)
    .Get();
```

---

## Фильтрация по Foreign Tables

```csharp
// Вернуть страны с городом Bali (INNER JOIN)
var results = await supabase
    .From<Country>()
    .Select("name, cities!inner(name)")
    .Filter("cities.name", Operator.Equals, "Bali")
    .Get();

// Фильтр по вложенной таблице без INNER
var result = await supabase
    .From<Movie>()
    .Select("*, users!inner(*)")
    .Filter("users.username", Operator.Equals, "Jane")
    .Get();
```

---

## Модификаторы

### Order (сортировка)
```csharp
.Order("created_at", Ordering.Descending)
.Order("name",       Ordering.Ascending)

// Сортировка по вложенной таблице
.Order("cities.name", Ordering.Ascending, foreignTable: "cities")

// Nulls first / last
.Order("deleted_at", Ordering.Descending, nullsFirst: true)
```

### Limit (ограничение)
```csharp
.Limit(10)
// Limit по вложенной таблице:
.Limit(5, foreignTable: "cities")
```

### Range (пагинация, включительно)
```csharp
.Range(0, 24)   // строки 0–24 (25 строк)
.Range(25, 49)  // строки 25–49
```

### Single
```csharp
.Single()
// Возвращает единственную запись.
// Бросает PostgrestException если строк 0 или больше 1.
```

---

## Комбинированный пример

```csharp
var result = await supabase
    .From<Product>()
    .Select("id, name, price, category:category_id(name)")
    .Filter("price",      Operator.GreaterThanOrEqual, 10)
    .Filter("price",      Operator.LessThan,           500)
    .Not("status",        Operator.Equals, "archived")
    .Filter("tags",       Operator.Contains, new List<string> { "sale" })
    .Order("price",       Ordering.Ascending)
    .Range(0, 19)
    .Get();
```
