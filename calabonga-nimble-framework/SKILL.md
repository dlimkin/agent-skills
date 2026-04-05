---
name: calabonga-nimble-framework
description: >
  Project context and coding guidelines for the Nimble Framework — an ASP.NET Core (.NET 10)
  microservice template system by Calabonga. Use this skill whenever working on code, tests,
  architecture decisions, or documentation for this project. Triggers on any mention of
  Nimble Framework, microservice templates, IdentityModule, Mediator.Net, Calabonga, CQRS
  patterns in this codebase, or when generating/reviewing C# code that belongs to this project.
---

# Nimble Framework — Project Guidelines

**Nimble Framework** is a set of microservice templates for ASP.NET Core (.NET 10) by Sergey Calabonga.  
Repo: https://github.com/Calabonga/Microservice-Template  
Wiki: https://github.com/Calabonga/Microservice-Template/wiki  
Current version: **10.0.0**

---

## Two Templates

| Template | NuGet Package | Purpose |
|----------|--------------|---------|
| **IdentityModule** | `Calabonga.Microservice.IdentityModule.Template` | Microservice with auth (OpenIddict, OAuth2.0, Bearer, PKCE) |
| **Module** | `Calabonga.Microservice.Module.Template` | Microservice without auth |

---

## Project Structure

```
{Name}.Entities/      → Domain entities, DTOs, interfaces
{Name}.Application/   → CQRS: Queries, Commands, Handlers
{Name}.Web/           → ASP.NET Core Web API, controllers, Program.cs
AuthClientSamples/    → Example client apps (Blazor Web App)
```

---

## Tech Stack

| Library | Purpose | Notes |
|---------|---------|-------|
| **Mediator.Net** | CQRS mediator | Replaced MediatR in v9.1.0. Uses SourceGenerator — no Reflection |
| **Mapster** | Object mapping | Replaced AutoMapper in v9.1.0 |
| **OpenIddict 6.x** | Auth (IdentityModule only) | OAuth2.0, PKCE, Authorization Code Flow |
| **EntityFramework Core** | ORM | InMemory for tests |
| **FluentValidation** | Request validation | + DependencyInjectionExtensions |
| **Calabonga.Results** | Operation results (RFC7807) | Replaced OperationResultCore in v8.0.1 |
| **Calabonga.UnitOfWork** | Unit of Work pattern | |
| **Microsoft.AspNetCore.OpenApi** | OpenAPI doc generation | Replaced Swashbuckle generator in v9.0.0 |
| **Swashbuckle.AspNetCore.SwaggerUI** | Swagger UI only | Only for displaying `/openapi/v1.json` |
| **Serilog** | Logging | |

> See `references/tech-stack.md` for detailed migration notes and version history.

---

## Code Conventions

### CQRS — always use `record`, not `class`

```csharp
// ✅ Correct
public record GetItemByIdQuery(int Id) : IQuery<OperationResult<ItemViewModel>>;

public class GetItemByIdQueryHandler : IQueryHandler<GetItemByIdQuery, OperationResult<ItemViewModel>>
{
    public async Task<OperationResult<ItemViewModel>> Handle(
        GetItemByIdQuery query, CancellationToken cancellationToken)
    {
        // implementation
    }
}
```

### Object Mapping — Mapster

```csharp
// Simple mapping (extension method)
var viewModel = entity.Adapt<ItemViewModel>();

// Collection mapping
var list = entities.Adapt<List<ItemViewModel>>();

// Custom configuration (in Program.cs or a dedicated MappingConfig class)
TypeAdapterConfig<Item, ItemViewModel>
    .NewConfig()
    .Map(dest => dest.FullName, src => $"{src.FirstName} {src.LastName}");

// DI-based mapping via IMapper
public class Handler(IMapper mapper)
{
    var result = mapper.From(entity).AdaptToType<ItemViewModel>();
}
```

> ❌ Do NOT use `AutoMapper` — it has been removed from the project.

### Operation Results — Calabonga.Results

```csharp
// Success
return OperationResult.CreateResult(viewModel);

// Error (RFC7807)
return OperationResult.CreateResult<ItemViewModel>(new AppException("Not found"));
```

### Validation — FluentValidation

```csharp
public class CreateItemValidator : AbstractValidator<CreateItemRequest>
{
    public CreateItemValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(200);
    }
}
```

### OpenIddict — use `EndSession`, not `Logout`

```csharp
// ✅ Correct (OpenIddict 6.x+)
OpenIddictConstants.Permissions.Endpoints.EndSession

// ❌ Outdated
OpenIddictConstants.Permissions.Endpoints.Logout
```

---

## What NOT to Use

| ❌ Forbidden | ✅ Use instead |
|------------|--------------|
| `MediatR` | `Mediator.Net` |
| `AutoMapper` | `Mapster` |
| `OperationResultCore` | `Calabonga.Results` |
| `Swashbuckle` (doc generator) | `Microsoft.AspNetCore.OpenApi` |
| `Logout` endpoint in OpenIddict | `EndSession` |
| `class` for Query/Command | `record` |
| `Console.WriteLine` for logs | `ILogger<T>` (Serilog) |

---

## Commit Message Conventions

Format: `<prefix>: <description>`

| Prefix | When to use |
|--------|------------|
| `feat:` | New feature (service, endpoint, functionality) |
| `fix:` | Bug fix that affects system behavior |
| `refactor:` | Code refactor without logic changes |
| `style:` | Formatting, whitespace, indentation |
| `test:` | Creating or modifying tests |
| `docs:` | Documentation changes, README updates |
| `build:` | Build process, nuget/npm dependency changes |
| `chore:` | Other changes not affecting logic or tests |
| `perf:` | Performance improvements |
| `ci:` | CI/CD configuration changes |
| `revert:` | Reverting a previous commit |

**Examples:**
```
feat: add endpoint for retrieving user list
fix: resolve validation error in CreateItemCommand
refactor: convert QueryHandler to use record
build: update EntityFrameworkCore nuget packages to 10.x
docs: update README with v10 examples
```

---

## Useful Links

- [Wiki / Documentation](https://github.com/Calabonga/Microservice-Template/wiki)
- [Blazor Web App Sample](https://github.com/Calabonga/Microservice-Template/wiki/Blazor-Web-App-Sample)
- [Mapster (GitHub)](https://github.com/MapsterMapper/Mapster)
- [Mediator.Net (GitHub)](https://github.com/mayuanyang/Mediator.Net)
- [Calabonga.Results (GitHub)](https://github.com/Calabonga/Calabonga.Results)
- [Calabonga.UnitOfWork.Controllers](https://github.com/Calabonga/Calabonga.UnitOfWork.Controllers)
- [Author's Blog](https://www.calabonga.net)
