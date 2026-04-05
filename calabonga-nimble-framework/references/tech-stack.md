# Tech Stack — Migration Notes & Version History

## Key Library Replacements

### MediatR → Mediator.Net (v9.1.0)

**Why:** MediatR went commercial. Mediator.Net uses SourceGenerator instead of Reflection, which significantly improves performance.

**Before (MediatR):**
```csharp
public class GetItemQuery : IRequest<ItemViewModel> { }
public class GetItemQueryHandler : IRequestHandler<GetItemQuery, ItemViewModel> { }
```

**After (Mediator.Net):**
```csharp
public record GetItemQuery(int Id) : IQuery<OperationResult<ItemViewModel>>;
public class GetItemQueryHandler : IQueryHandler<GetItemQuery, OperationResult<ItemViewModel>> { }
```

---

### AutoMapper → Mapster (v9.1.0)

**Why:** AutoMapper changed its licensing model. Mapster is faster and has a clean API.

**NuGet packages:**
- `Mapster` — core library
- `Mapster.DependencyInjection` — DI integration

**Registration in Program.cs:**
```csharp
builder.Services.AddMapster();
// or with custom config:
var config = TypeAdapterConfig.GlobalSettings;
config.Scan(Assembly.GetExecutingAssembly());
builder.Services.AddSingleton(config);
builder.Services.AddScoped<IMapper, ServiceMapper>();
```

**Usage patterns:**
```csharp
// 1. Static extension (simplest)
var dto = entity.Adapt<ItemDto>();

// 2. With IMapper (DI)
public class Handler(IMapper mapper)
{
    var dto = mapper.From(entity).AdaptToType<ItemDto>();
}

// 3. Custom config (in a MappingConfig class)
TypeAdapterConfig<Source, Destination>
    .NewConfig()
    .Map(dest => dest.FullName, src => $"{src.First} {src.Last}")
    .Ignore(dest => dest.InternalField);

// 4. Two-way mapping
TypeAdapterConfig<Item, ItemDto>.NewConfig().TwoWays();
```

---

### OperationResultCore → Calabonga.Results (v8.0.1)

**Why:** Simpler RFC7807 implementation, significantly better serialization performance.

**Usage:**
```csharp
// Success
OperationResult.CreateResult(data);

// Error
OperationResult.CreateResult<T>(new AppException("message"));

// Check in caller
if (result.Ok)
    return result.Result;
else
    return BadRequest(result.Exception);
```

---

### Swashbuckle → Microsoft.AspNetCore.OpenApi (v9.0.0)

**Why:** Microsoft's native OpenAPI support became production-ready in .NET 9.

- `Swashbuckle.AspNetCore` (doc generator) — **removed**
- `Swashbuckle.AspNetCore.SwaggerUI` — **kept** (UI only, reads `/openapi/v1.json`)
- `Microsoft.AspNetCore.OpenApi` — **new** primary doc generator

---

### OpenIddict: Logout → EndSession (v9.0.2, OpenIddict 6.x)

The `Logout` permission endpoint was renamed to `EndSession` in OpenIddict 6.x:

```csharp
// ✅ v6.x+
OpenIddictConstants.Permissions.Endpoints.EndSession

// ❌ < v6.x (removed)
OpenIddictConstants.Permissions.Endpoints.Logout
```

---

## Version History (summary)

| Version | .NET | Key Changes |
|---------|------|------------|
| 10.0.0 | NET10 | NET10 migration, Bearer + OAuth2.0 schemes for OpenAPI |
| 9.2.0 | NET9 | Added ASP.NET Core RazorPages template |
| 9.1.0 | NET9 | MediatR → Mediator.Net, AutoMapper → Mapster |
| 9.0.0 | NET9 | Swashbuckle → Microsoft.AspNetCore.OpenApi |
| 8.0.1 | NET8 | OperationResultCore → Calabonga.Results |
| 8.0.0 | NET8 | NET8 migration |
