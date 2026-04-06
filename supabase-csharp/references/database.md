# Database — Полный справочник CRUD

> Читать когда: нужны подробные примеры по SELECT / INSERT / UPDATE / UPSERT / DELETE / RPC, включая все вариации.

## Модель-пример (используется во всех примерах ниже)

```csharp
[Table("cities")]
public class City : BaseModel
{
    // false = не автогенерируемый PK (нужно передавать вручную при вставке)
    [PrimaryKey("id", false)]
    public int Id { get; set; }

    [Column("name")]
    public string Name { get; set; }

    [Column("country_id")]
    public int CountryId { get; set; }

    public override bool Equals(object obj) =>
        obj is City c && Id == c.Id;

    public override int GetHashCode() => HashCode.Combine(Id);
}
```

---

## SELECT (Fetch data)

### Все строки
```csharp
var result = await supabase.From<City>().Get();
List<City> cities = result.Models;
```

### Только нужные столбцы (LINQ)
```csharp
var result = await supabase
    .From<City>()
    .Select(x => new object[] { x.Name, x.CountryId })
    .Get();
```

### Запрос связанных таблиц (JOIN — только строковая форма)
```csharp
// LINQ здесь НЕ работает — обязательно использовать строку
var data = await supabase
    .From<Transaction>()
    .Select("id, supplier:supplier_id(name), purchaser:purchaser_id(name)")
    .Get();
```

### INNER JOIN с фильтром по вложенной таблице
```csharp
var result = await supabase
    .From<Movie>()
    .Select("*, users!inner(*)")
    .Filter("users.username", Operator.Equals, "Jane")
    .Get();
```

### Фильтрация по JSON-колонке
```csharp
var result = await supabase
    .From<User>()
    .Select("id, name, address->street")
    .Filter("address->postcode", Operator.Equals, 90210)
    .Get();
```

### Только количество строк (без данных)
```csharp
var count = await supabase
    .From<City>()
    .Count(CountType.Exact);
// Варианты: CountType.Exact | CountType.Planned | CountType.Estimated
```

### Одна строка
```csharp
var city = await supabase
    .From<City>()
    .Where(x => x.Name == "Paris")
    .Single();
// Бросает исключение если 0 или >1 строк
```

---

## INSERT

### Вставка одной записи
```csharp
var model = new City { Name = "The Shire", CountryId = 554 };
await supabase.From<City>().Insert(model);
```

### Вставка с получением созданной записи обратно
```csharp
var result = await supabase
    .From<City>()
    .Insert(model, new QueryOptions { Returning = ReturnType.Representation });
City created = result.Model;
```

### Массовая вставка (bulk insert)
```csharp
var models = new List<City>
{
    new City { Name = "The Shire", CountryId = 554 },
    new City { Name = "Rohan",     CountryId = 553 },
};
await supabase.From<City>().Insert(models);
```

> **Примечание:** если PK автогенерируемый (SERIAL / UUID), укажите `[PrimaryKey("id", false)]` — второй аргумент `false` означает «не включать PK в INSERT payload».

---

## UPDATE

### Через запрос (Set + Where)
```csharp
await supabase
    .From<City>()
    .Where(x => x.Name == "Auckland")
    .Set(x => x.Name, "Middle Earth")
    .Update();
```

### Через гидрированную модель
```csharp
var city = await supabase
    .From<City>()
    .Where(x => x.Name == "Auckland")
    .Single();

city.Name = "Middle Earth";
await city.Update<City>();
```

> PrimaryKey обязан быть заполнен — иначе UPDATE не знает, какую строку обновить.

---

## UPSERT

### Стандартный upsert
```csharp
var model = new City { Id = 554, Name = "Middle Earth" };
await supabase.From<City>().Upsert(model);
```

### Upsert по конкретному полю конфликта
```csharp
await supabase
    .From<City>()
    .OnConflict(x => x.Name)   // конфликт по полю Name
    .Upsert(model);
```

### Upsert с подсчётом строк
```csharp
await supabase
    .From<City>()
    .Upsert(model, new QueryOptions { Count = QueryOptions.CountType.Exact });
```

> **Важно:** PK должен быть натуральным (не суррогатным) для корректного UPSERT.

---

## DELETE

### По условию через LINQ
```csharp
await supabase
    .From<City>()
    .Where(x => x.Id == 342)
    .Delete();
```

### Через Filter
```csharp
await supabase
    .From<City>()
    .Filter("name", Operator.Equals, "Mordor")
    .Delete();
```

### Через гидрированную модель
```csharp
await city.Delete<City>();
```

> **Всегда** добавляйте фильтр к Delete — иначе будут удалены все строки таблицы.

---

## RPC (Вызов Postgres-функции)

### Без параметров
```csharp
await supabase.Rpc("hello_world", null);
```

### С параметрами
```csharp
await supabase.Rpc("hello_world", new Dictionary<string, object>
{
    { "foo", "bar" },
    { "count", 42 }
});
```

### Типизированный результат
```csharp
var result = await supabase.Rpc<MyResponseType>("my_function", parameters);
```

---

## Пагинация

```csharp
// Страница 1: строки 0–24
var page1 = await supabase.From<City>().Range(0, 24).Get();

// Страница 2: строки 25–49
var page2 = await supabase.From<City>().Range(25, 49).Get();

// С сортировкой
var sorted = await supabase
    .From<City>()
    .Order("name", Ordering.Ascending)
    .Range(0, 9)
    .Get();
```

> По умолчанию Supabase возвращает максимум **1 000 строк**. Используйте `.Range()` для пагинации.
