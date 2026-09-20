---
name: calabonga-nimble-framework
description: >
  Project context and coding guidelines for the Nimble Framework — the ASP.NET Core
  microservice template set by Calabonga (Sergey Calabonga). Covers the NET10.0 generation
  of https://github.com/Calabonga/Microservice-Template. Use this skill whenever working on
  code, tests, architecture decisions, or documentation for a project generated from these
  templates. Triggers on any mention of Nimble Framework, Calabonga templates, Microservice
  Module / IdentityModule / AspNetCoreRazorPages templates, AppDefinitions, Calabonga.UnitOfWork,
  Calabonga.Results / Operation results, or when generating or reviewing C# code that belongs
  to such a project.
---

# Nimble Framework — Project Guidelines (NET10.0 generation)

**Verified against the repository on 2026-09-20.**

- Source of truth: <https://github.com/Calabonga/Microservice-Template>, branch `master`,
  commit `ad82376a3583e138cc5b59439756f0433b273c63` (dated 2026-08-27), folder `NET10.0/`.
- Method: GitHub Git Trees API + `raw.githubusercontent.com` for every file quoted below;
  package facts from `api.nuget.org` `.nuspec` files; .NET support dates from
  `dotnet/core` → `release-notes/releases-index.json`.
- Template packages on nuget.org at that date: `Calabonga.Microservice.Module.Template`,
  `Calabonga.Microservice.IdentityModule.Template` and `Calabonga.AspNetCoreRazorPages.Template`
  are all at **10.0.5** (produced by Nerdbank.GitVersioning from `version.json` = `10.0` plus git height).
- Every code block below is copied from a real file in that commit; the path is stated next to it.

> This document describes the **NET10.0** generation only. The repository also keeps `NET8.0/`
> and `NET9.0/` folders whose stacks differ substantially — see "Replacement history by generation".

---

## Three templates (not two)

`NET10.0/` contains three template projects:

| Folder / NuGet package | Root namespace in `content/` | Purpose |
|---|---|---|
| `Calabonga.Microservice.Module.Template` | `Calabonga.Microservice.Module` | Minimal-API microservice, **resource server**: validates tokens issued elsewhere (`AddOpenIddict().AddValidation()`) |
| `Calabonga.Microservice.IdentityModule.Template` | `Calabonga.Microservice.IdentityModule` | Same, plus a full **OpenIddict authorization server** (`AddCore` + `AddServer` + `AddValidation`), Razor login/logout pages, EF Core stores |
| `Calabonga.AspNetCoreRazorPages.Template` | `Calabonga.AspNetCoreRazorPages` | Razor Pages **UI client**: OpenIddict *client* (`AddClient`), no Web API endpoints, no CQRS messages |

Install (wiki → Home):

```bash
dotnet new install Calabonga.Microservice.Module.Template
dotnet new install Calabonga.Microservice.IdentityModule.Template
dotnet new install Calabonga.AspNetCoreRazorPages.Template
```

The Module template's `shortName` is `microservice`
(`NET10.0/Calabonga.Microservice.Module.Template/content/.template.config/template.json`).

---

## Project structure

Three projects per solution, named after the generated root namespace — there is **no
`{Name}.Entities` and no `{Name}.Application` project**:

```
content/
├── {Name}.Domain/           → entities, base types, contracts. NO PackageReference at all
│                              (exception: RazorPages Domain references Calabonga.Results)
├── {Name}.Infrastructure/   → ApplicationDbContext, DatabaseInitializer, Identity types
└── {Name}.Web/              → Minimal API host
    ├── Program.cs           → ~20 lines: Serilog + AddDefinitions/UseDefinitions
    ├── Definitions/         → one AppDefinition class per concern
    │   ├── Authorizations/  Common/  Cors/  DataSeeding/  DbContext/
    │   ├── ETagGenerator/   ErrorHandling/  FluentValidating/
    │   ├── Mediator/        OpenApi/  OpenIddict/  UoW/
    ├── Application/
    │   ├── Messaging/{Entity}Messages/
    │   │   ├── Queries/            → one static class per CQRS operation
    │   │   ├── ViewModels/
    │   │   ├── {Entity}Mapping.cs  → hand-written extension methods
    │   │   └── {Entity}Validator.cs
    │   └── Services/        → application services (IdentityModule: IAccountService)
    └── Endpoints/           → {Entity}Endpoints : AppDefinition
```

Solutions are in the **`.slnx`** format (e.g. `content/Calabonga.Microservice.Module.slnx`),
not `.sln`.

Dependency direction is `Web → Infrastructure → Domain`; `Domain` never references upward
(repository's own rule file `.claude/rules/architecture.md`).

The RazorPages template has no `Application/Messaging` folder: it registers Mediator
(`Definitions/Mediator/MediatorDefinition.cs`) but ships no requests or handlers.

---

## Target frameworks

- Every `.csproj` in all three NET10.0 templates: `<TargetFramework>net10.0</TargetFramework>`,
  `ImplicitUsings=enable`, `Nullable=enable`. The two microservice templates also set
  `<InvariantGlobalization>false</InvariantGlobalization>`; the RazorPages template does not.
- The Calabonga helper libraries are **not** net10-bound — they target `netstandard2.1`:
  `Calabonga.Results` (1.1.0 and 2.0.1), `Calabonga.PagedListCore` (2.0.0 and 3.0.0),
  `Calabonga.Microservices.Core` 6.0.0, `Calabonga.PredicatesBuilder` 2.0.2.
  They can be consumed from older TFMs; nothing forces net10 on their account.
  `Calabonga.UnitOfWork` 10.x and `Calabonga.AspNetCore.AppDefinitions` 10.x **are** net10-only.
- .NET support (from `dotnet/core` `releases-index.json`, read 2026-09-20):
  **.NET 8 (LTS) and .NET 9 (STS) both reach end of support on 2026-11-10**;
  **.NET 10 is LTS, supported until 2028-11-14**. Starting new work on the NET8.0/NET9.0
  template generations is therefore a short-lived choice.

---

## Tech stack as pinned in NET10.0

Read from the twelve `.csproj` files under `NET10.0/`. "Latest" = newest stable on nuget.org
on 2026-09-20; the templates deliberately lag.

| Package | Pinned in templates | Latest stable | Used by |
|---|---|---|---|
| `Calabonga.AspNetCore.AppDefinitions` | 10.0.0 | 10.0.1 | all three (Web) |
| `Mediator.Abstractions` | 3.0.2 | 3.0.2 | all three (Web) |
| `Mediator.SourceGenerator` | 3.0.2 | 3.0.2 | all three (Web) |
| `FluentValidation` (+ `.DependencyInjectionExtensions`) | 12.1.1 | — | all three (Web) |
| `OpenIddict.AspNetCore` | 7.6.1 | — | all three (Web) |
| `OpenIddict.EntityFrameworkCore` | 7.6.1 | — | IdentityModule, RazorPages (Infrastructure) |
| `Microsoft.AspNetCore.OpenApi` | 10.0.11 | — | Module, IdentityModule (Web) |
| `Swashbuckle.AspNetCore.SwaggerUI` | 10.2.3 | — | Module, IdentityModule (Web) — **UI only** |
| `Serilog.AspNetCore` | 10.0.0 | — | all three (Web) |
| `Microsoft.EntityFrameworkCore*`, `Microsoft.AspNetCore.*` | 10.0.11 | — | Infrastructure / Web |
| `Calabonga.UnitOfWork` | 10.0.1 | 10.0.3 | Module, IdentityModule, RazorPages (Infrastructure) |
| `Calabonga.Results` | 1.1.0 | 2.0.1 | Module, IdentityModule (Infrastructure); RazorPages (Domain) |
| `Calabonga.PredicatesBuilder` | 2.0.2 | 2.0.2 | Infrastructure |
| `Calabonga.Microservices.Core` | 6.0.0 | 6.0.0 | Module (Infrastructure), IdentityModule (Web), RazorPages (Infrastructure) |
| `Calabonga.PagedListCore` | **transitive** 2.0.0 (via UnitOfWork 10.0.1) | 3.0.0 | everywhere `IPagedList<T>` is used |

Template-specific extras: `System.Linq.Async` 7.0.1 (IdentityModule Web),
`Microsoft.Extensions.Caching.StackExchangeRedis` 10.0.11 (RazorPages Web),
`Microsoft.AspNetCore.Components.QuickGrid.EntityFrameworkAdapter` 10.0.11 (Module Web).

> **Upgrade trap.** `Calabonga.UnitOfWork` 10.0.1 pulls `Calabonga.PagedListCore` **2.0.0**;
> 10.0.3 pulls **3.0.0**, whose release notes read "PageIndex unified to 1-based;
> HasPreviousPage/HasNextPage off-by-one fixed; argument validation added. Breaking change."
> The template code is written for 0-based paging (`int pageIndex = 0` in the endpoint
> defaults). Bumping UnitOfWork silently changes paging semantics.

See `references/tech-stack.md` for the full per-template package lists and history.

---

## Code conventions

Naming rules below are the repository author's own, from `.claude/rules/conventions.md`
in the template repo.

### CQRS — one `static class` per operation, with nested `Request` and `Handler`

There are no `IQuery<>` / `IQueryHandler<>` / `ICommand<>` types anywhere in the templates.
The mediator is **martinothamar/Mediator** (`using Mediator;`): the contracts are
`IRequest<TResponse>` and `IRequestHandler<TRequest, TResponse>`, and `Handle` returns
**`ValueTask<T>`, not `Task<T>`**.

From `NET10.0/Calabonga.Microservice.Module.Template/content/Calabonga.Microservice.Module.Web/Application/Messaging/EventItemMessages/Queries/GetEventItemPaged.cs`:

```csharp
using Calabonga.Microservice.Module.Domain;
using Calabonga.Microservice.Module.Web.Application.Messaging.EventItemMessages.ViewModels;
using Calabonga.OperationResults;
using Calabonga.PagedListCore;
using Calabonga.PredicatesBuilder;
using Calabonga.UnitOfWork;
using Mediator;
using System.Linq.Expressions;
using PredicateBuilder = Calabonga.PredicatesBuilder.PredicateBuilder;

namespace Calabonga.Microservice.Module.Web.Application.Messaging.EventItemMessages.Queries;

/// <summary>
/// Request for paged list of EventItems
/// </summary>
public static class GetEventItemPaged
{
    public record Request(int PageIndex, int PageSize, string? Search) : IRequest<Operation<IPagedList<EventItemViewModel>, string>>;

    public class Handler(IUnitOfWork unitOfWork)
        : IRequestHandler<Request, Operation<IPagedList<EventItemViewModel>, string>>
    {
        public async ValueTask<Operation<IPagedList<EventItemViewModel>, string>> Handle(
            Request request,
            CancellationToken cancellationToken)
        {
            var predicate = GetPredicate(request.Search);
            var pagedList = await unitOfWork.GetRepository<EventItem>()
                .GetPagedListAsync(
                    predicate: predicate,
                    pageIndex: request.PageIndex,
                    pageSize: request.PageSize,
                    trackingType: TrackingType.NoTracking,
                    cancellationToken: cancellationToken);

            if (pagedList.PageIndex > pagedList.TotalPages)
            {
                pagedList = await unitOfWork.GetRepository<EventItem>()
                    .GetPagedListAsync(
                        pageIndex: 0,
                        pageSize: request.PageSize,
                        trackingType: TrackingType.NoTracking,
                        cancellationToken: cancellationToken);
            }

            var mapped = PagedList.From(pagedList, items => items.Select(item => item.MapToViewModel()!));
            return Operation.Result(mapped);
        }

        private Expression<Func<EventItem, bool>> GetPredicate(string? search)
        {
            var predicate = PredicateBuilder.True<EventItem>();
            if (search is null)
            {
                return predicate;
            }

            predicate = predicate.And(x => x.Message.Contains(search));
            predicate = predicate.Or(x => x.Logger.Contains(search));
            predicate = predicate.Or(x => x.Level.Contains(search));
            return predicate;
        }
    }
}
```

Naming:

- Operation class = HTTP verb + entity: `Get{Entity}ById`, `Get{Entity}Paged`, `Post{Entity}`,
  `Put{Entity}`, `Delete{Entity}`. File is named after the class — one historical exception
  in the template: the file `UpdateEventItem.cs` contains `public static class PutEventItem`.
- Nested types are named exactly `Request` and `Handler`; `Handler` uses a primary constructor.
- `Request` is a `record` in the EventItem messages. It is **not an absolute rule**:
  `…/Application/Messaging/ProfileMessages/Queries/RegisterAccount.cs` (IdentityModule) declares
  `public class Request(RegisterViewModel model) : IRequest<Operation<UserProfileViewModel, string>>`.
  Prefer `record`; do not "fix" the existing `class` one on sight.
- View models: `{Entity}ViewModel`, `{Entity}CreateViewModel`, `{Entity}UpdateViewModel`.

### Operation results — `Calabonga.Results`, namespace `Calabonga.OperationResults`

Package id and namespace differ. The package is `Calabonga.Results`; the `using` is
`Calabonga.OperationResults` (renamed in 1.x, release note: "Root namespace renamed from
Calabonga.Results to Calabonga.OperationResults").

The types are readonly structs `Operation<T>`, `Operation<T, TError>`, `Operation<T, T1, T2>`,
`Operation<T, T1, T2, T3>` with `Result` and `Ok` properties; on the multi-error overloads
`Error` is a **public readonly field**, not a property. Values are produced by the static
helper class `Operation` and converted implicitly:

```csharp
// success — Operation.Result<T>(T) returns SuccessResult<T>, implicitly converted on return
return Operation.Result(mapped);

// error — Operation.Error<T>(T) returns ErrorResult<T>, implicitly converted on return
return Operation.Error($"Entity with identifier {id} not found");
```

(both from `…/Application/Messaging/EventItemMessages/Queries/GetEventItemById.cs`)

The response type used throughout the templates is `Operation<TViewModel, string>` — the error
channel is a plain `string`. Checking a result:

```csharp
var lastResult = unitOfWork.Result;
if (lastResult.Ok)
{
    // ...
}
```

> `OperationResult.CreateResult(...)` does **not** exist here — that was the API of the older
> `OperationResultCore` package, dropped in 8.0.1.

### Object mapping — hand-written extension methods, no mapper library

There is no AutoMapper, no Mapster and no other mapping package in any NET10.0 `.csproj`.
Mapping is a static class of extension methods per entity. From
`…/Application/Messaging/EventItemMessages/EventItemMapping.cs` (the author's own file comment):

```csharp
/// <summary>
/// Replacement for Automapper
/// </summary>
public static class EventItemMapping
{
    public static EventItemViewModel? MapToViewModel(this EventItem? source)
    {
        if (source is null)
        {
            return null;
        }

        return new EventItemViewModel
        {
            CreatedAt = source.CreatedAt,
            ExceptionMessage = source.ExceptionMessage,
            Id = source.Id,
            Level = source.Level,
            Logger = source.Logger,
            Message = source.Message,
            ThreadId = source.ThreadId,
        };
    }

    public static EventItem? MapToEventItem(this EventItemCreateViewModel? source) { /* ... */ }

    public static void MapUpdatesFrom(this EventItem? source, EventItemUpdateViewModel? updateViewModel) { /* ... */ }
}
```

Convention: class `{Entity}Mapping`, methods `MapToViewModel()`, `MapTo{Entity}()`,
`MapUpdatesFrom()`. All of them are nullable-in / nullable-out, which is why call sites use
`!` or an explicit null check.

> The NuGet packaging metadata of the template projects still says
> "Microservice template on Minimal API with Automapper, FluentValidation and other helpful thing"
> (`NET10.0/Calabonga.Microservice.Module.Template/Calabonga.Microservice.Module.Template.csproj`).
> That description is stale — do not treat it as evidence that AutoMapper is present.

### Composition — AppDefinitions, not a long Program.cs

`Program.cs` stays minimal; every concern is an `AppDefinition` subclass discovered by
`Calabonga.AspNetCore.AppDefinitions`. From
`…/Calabonga.Microservice.Module.Web/Program.cs`:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Host.UseSerilog((context, configuration) =>
    configuration.ReadFrom.Configuration(context.Configuration));

builder.AddDefinitions(typeof(Program));

var app = builder.Build();
app.UseDefinitions();
app.UseSerilogRequestLogging();
app.Run();
```

A definition overrides `ConfigureServices(WebApplicationBuilder)` and/or
`ConfigureApplication(WebApplication)`. From `…/Definitions/UoW/UnitOfWorkDefinition.cs`:

```csharp
public class UnitOfWorkDefinition : AppDefinition
{
    public override void ConfigureServices(WebApplicationBuilder builder)
        => builder.Services.AddUnitOfWork<ApplicationDbContext>();
}
```

Mediator registration, from `…/Definitions/Mediator/MediatorDefinition.cs` (Module template):

```csharp
public override void ConfigureServices(WebApplicationBuilder builder)
{
    builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidatorBehavior<,>));
    builder.Services.AddMediator(options => options.ServiceLifetime = ServiceLifetime.Scoped);
}
```

### Endpoints — Minimal API groups inside an AppDefinition

From `…/Calabonga.Microservice.Module.Web/Endpoints/EventItemEndpoints.cs`:

```csharp
public sealed class EventItemEndpoints : AppDefinition
{
    public override void ConfigureApplication(WebApplication app) => app.MapEventItemEndpoints();
}

internal static class EventItemEndpointsExtensions
{
    public static void MapEventItemEndpoints(this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/event-items/").WithTags(nameof(EventItem));

        group.MapGet("paged/{pageIndex:int}", async ([FromServices] IMediator mediator, string? search, HttpContext context, int pageIndex = 0, int pageSize = 10)
                => await mediator.Send(new GetEventItemPaged.Request(pageIndex, pageSize, search), context.RequestAborted))
            .RequireAuthorization(x => x.AddAuthenticationSchemes(OpenIddictServerAspNetCoreDefaults.AuthenticationScheme).RequireAuthenticatedUser())
            .Produces(200)
            .ProducesProblem(401)
            .ProducesProblem(404);
        // ...
    }
}
```

Convention: `{Entity}Endpoints : AppDefinition` plus
`internal static class {Entity}EndpointsExtensions` with `Map{Entity}Endpoints`.

### Validation — FluentValidation with a Mediator pipeline behavior

Validators target the **request type**, not the view model, and the template uses a rule set.
From `…/Application/Messaging/EventItemMessages/EventItemValidator.cs`:

```csharp
public class EventItemCreateRequestValidator : AbstractValidator<PostEventItem.Request>
{
    public EventItemCreateRequestValidator() => RuleSet("default", () =>
    {
        RuleFor(x => x.Model.CreatedAt).NotNull();
        RuleFor(x => x.Model.Message).NotEmpty().MaximumLength(4000);
        RuleFor(x => x.Model.Level).NotEmpty().MaximumLength(50);
        RuleFor(x => x.Model.Logger).NotEmpty().MaximumLength(255);
        RuleFor(x => x.Model.ThreadId).MaximumLength(50);
        RuleFor(x => x.Model.ExceptionMessage).MaximumLength(4000);
    });
}
```

`ValidatorBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>` throws
`ValidationException` on failures; registration is
`builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly)`
(`…/Definitions/FluentValidating/`).

### OpenIddict 7.x — `EndSession`, never `Logout`

The rename landed in OpenIddict 6.0 (repo changelog, version 9.0.2, 2024-12-25) and still holds
in the 7.6.1 that NET10.0 pins. From
`NET10.0/Calabonga.Microservice.IdentityModule.Template/content/Calabonga.Microservice.IdentityModule.Web/Definitions/OpenIddict/OpenIddictDefinition.cs`:

```csharp
options.SetAuthorizationEndpointUris("connect/authorize").RequireProofKeyForCodeExchange()
    .SetIntrospectionEndpointUris("connect/introspect")
    .SetEndSessionEndpointUris("connect/logout")
    .SetTokenEndpointUris("connect/token")
    .SetUserInfoEndpointUris("connect/userinfo");
// ...
options.UseAspNetCore()
    .EnableEndSessionEndpointPassthrough()
    .EnableTokenEndpointPassthrough()
    .EnableAuthorizationEndpointPassthrough()
    .DisableTransportSecurityRequirement();
```

and from `…/HostedServices/OpenIddictWorker.cs`:

```csharp
Permissions =
{
    OpenIddictConstants.Permissions.Endpoints.Authorization,
    OpenIddictConstants.Permissions.Endpoints.EndSession,
    OpenIddictConstants.Permissions.Endpoints.Introspection,
    OpenIddictConstants.Permissions.Endpoints.Token,
    // ...
}
```

Note the *URI* is still `connect/logout`, and the Razor page is still `Pages/Connect/Logout.cshtml`
— only the API surface was renamed. The three templates use three different OpenIddict roles:

| Template | OpenIddict setup | File |
|---|---|---|
| Module | `AddOpenIddict().AddValidation()` with `UseLocalServer().UseAspNetCore()` | `…Module.Web/Definitions/OpenIddict/OpenIddictDefinition.cs` |
| IdentityModule | `AddCore()` (EF Core stores, `ReplaceDefaultEntities<Guid>()`) + `AddServer()` (code + PKCE, password, client credentials, refresh) + `AddValidation()` + `OpenIddictWorker` seeding two clients | `…IdentityModule.Web/Definitions/OpenIddict/OpenIddictDefinition.cs` |
| RazorPages | `AddCore()` + `AddClient()` with `AllowAuthorizationCodeFlow()`, `UseSystemNetHttp()`, one `OpenIddictClientRegistration` | `…RazorPages.Web/Definitions/OpenIddict/OpenIddictDefinition.cs` |

The Module template's default authentication scheme is
`OpenIddictServerAspNetCoreDefaults.AuthenticationScheme`, wired to `AddJwtBearer(..., "OAuth2.0", ...)`
against `AuthServer:Url` (`…Module.Web/Definitions/Authorizations/AuthorizationDefinition.cs`).

### OpenAPI — Microsoft generator, Swashbuckle for the UI only

`…/Definitions/OpenApi/OpenApiDefinition.cs` calls `builder.Services.AddOpenApi(...)` with a
document transformer that adds an `oauth2` Authorization-Code scheme, then in development
`app.MapOpenApi()` and `app.UseSwaggerUI(settings => settings.SwaggerEndpoint("/openapi/v1.json", ...))`.
`AppVersion` is a `const string "10.0.0"` in that same file.

> The Module template's `template.json` advertises "a UI (Scalar)". No Scalar package is
> referenced in any NET10.0 `.csproj`; the UI actually wired up is Swagger UI. Treat the
> template description as out of date.

---

## Replacement history by generation

Each row states the generation folder the claim is true for. Versions come from the `.csproj`
files in each folder; dates and wording from `README-en.md` in the repo root.

| Change | Announced in | First generation that ships it | Evidence |
|---|---|---|---|
| `OperationResultCore` → `Calabonga.Results` | 8.0.1 (2024-02-06) | `NET8.0/` | README-en.md; `Calabonga.Results` in NET8.0 Infrastructure csproj |
| `Swashbuckle.AspNetCore` (doc generator) → `Microsoft.AspNetCore.OpenApi`; SwaggerUI kept | 9.0.0 (2024-11-26) | `NET9.0/` | NET8.0 Web csproj still has `Swashbuckle.AspNetCore` 6.7.3; NET9.0 has only `Swashbuckle.AspNetCore.SwaggerUI` |
| OpenIddict `Logout` → `EndSession` | 9.0.2 (2024-12-25), OpenIddict 6.0 | `NET9.0/` (OpenIddict 7.0.0), still current in `NET10.0/` (7.6.1) | README-en.md diff block; `OpenIddictWorker.cs` |
| `MediatR` → **martinothamar/Mediator** | 9.1.0 (2025-06-16) | `NET9.0/` | NET8.0 Web csproj: `MediatR` 12.4.1. NET9.0/NET10.0: `Mediator.Abstractions` + `Mediator.SourceGenerator` |
| `AutoMapper` **removed**, replaced by hand-written mapping extensions | 9.1.0 (2025-06-16) | `NET9.0/` | NET8.0 Web csproj: `Automapper` 13.0.1. NET9.0/NET10.0: no mapping package at all; `EventItemMapping.cs` |
| RazorPages template added | 9.2.0 (2025-09-11) | `NET9.0/` | `NET8.0/` has two template folders, `NET9.0/` and `NET10.0/` have three |
| Migration to net10.0, OpenAPI `Bearer` scheme added | 10.0.0 (2026-02-14) | `NET10.0/` | all twelve csproj files target `net10.0` |
| Package refresh (AppDefinitions 10.0.0, OpenIddict 7.6.1, EF/ASP.NET 10.0.11, Mediator 3.0.2, UnitOfWork 10.0.1, SwaggerUI 10.2.3); CI unified into `publish-templates.yml` with Nerdbank.GitVersioning | 2026-08-27 | `NET10.0/` | README-en.md; current csproj versions |

Two corrections worth carrying explicitly, because the repo's own changelog is misleading:

1. **The mediator is not "Mediator.Net".** The 9.1.0 changelog entry links
   <https://github.com/mayuanyang/Mediator.Net>, but the packages actually referenced are
   `Mediator.Abstractions` and `Mediator.SourceGenerator`, whose nuspec authors field reads
   "Martin Othamar" and whose `projectUrl`/`repository` is
   <https://github.com/martinothamar/Mediator>. The API in the templates
   (`IRequest<T>`, `IRequestHandler<,>`, `IPipelineBehavior<,>` with
   `MessageHandlerDelegate<,>`, `ValueTask` returns, `AddMediator(options => ...)`) is
   martinothamar's, not mayuanyang's.
2. **Mapster was never adopted.** AutoMapper was removed in 9.1.0 and nothing replaced it.
   All 32 `.csproj` files across `NET8.0/`, `NET9.0/` and `NET10.0/` were fetched and searched:
   `Mapster` occurs in none of them, and `AutoMapper` only as a `PackageReference` in the two
   `NET8.0/` Web projects.

---

## What NOT to use in a NET10.0 project

| Do not use | Use instead | Why |
|---|---|---|
| `MediatR` | `Mediator.Abstractions` + `Mediator.SourceGenerator` (martinothamar) | removed in 9.1.0; source-generated, no reflection |
| `Mediator.Net` (mayuanyang) | same as above | never actually referenced by the templates |
| `AutoMapper`, `Mapster`, any mapper package | hand-written `{Entity}Mapping` extension methods | AutoMapper removed in 9.1.0; no mapper package is referenced |
| `OperationResultCore`, `OperationResult.CreateResult(...)` | `Calabonga.Results` → `using Calabonga.OperationResults;`, `Operation.Result(x)` / `Operation.Error(x)` | replaced in 8.0.1 |
| `using Calabonga.Results;` | `using Calabonga.OperationResults;` | package id ≠ namespace |
| `Task<T>` on a `Handle` method | `ValueTask<T>` | required by martinothamar's `IRequestHandler<,>` |
| `IQuery<>` / `IQueryHandler<>` / `ICommand<>` | nested `Request` / `Handler` in a `public static class` | those interfaces do not exist in this stack |
| `Swashbuckle.AspNetCore` (doc generator) | `Microsoft.AspNetCore.OpenApi` + `Swashbuckle.AspNetCore.SwaggerUI` for the UI | changed in 9.0.0 |
| `OpenIddictConstants.Permissions.Endpoints.Logout`, `EnableLogoutEndpointPassthrough`, `SetLogoutEndpointUris` | `...Endpoints.EndSession`, `EnableEndSessionEndpointPassthrough`, `SetEndSessionEndpointUris` | renamed in OpenIddict 6.0 |
| `{Name}.Entities` / `{Name}.Application` projects | `{Name}.Domain` / `{Name}.Infrastructure` / `{Name}.Web` | those project names do not exist in any generation |
| `PackageReference` in `{Name}.Domain` | keep Domain dependency-free | repo rule `.claude/rules/architecture.md` (the RazorPages Domain's `Calabonga.Results` is the one exception) |
| `Console.WriteLine` for logs | `ILogger<T>` (Serilog) | |

Gotcha: two similarly named constant holders coexist. `AppData.Exceptions.MappingException`
comes from the generated `{Name}.Domain/Base/AppData.Exceptions.cs`, while
`AppContracts.Exceptions.MappingException` comes from the `Calabonga.Microservices.Core`
package. Both appear in `PostEventItem.cs` and `UpdateEventItem.cs`. Match what the
surrounding file already uses.

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
fix: resolve validation error in PostEventItem handler
refactor: extract mapping into EventItemMapping extensions
build: update EntityFrameworkCore nuget packages to 10.0.11
docs: update README with NET10 examples
```

---

## Not verified

Stated here rather than presented as fact:

- **No template was generated, restored or built** during this verification. Every claim comes
  from reading files, `.nuspec` metadata and the repository changelog.
- Whether `OpenIddictConstants.Permissions.Endpoints.Logout` was *removed* or merely *obsoleted*
  in OpenIddict 6.x was not checked against OpenIddict's own sources; what is verified is that
  all three NET10.0 templates use the `EndSession` names exclusively.
- Only `Operation.cs` and `OperationHelpers.cs` were compared between the `Calabonga.Results`
  1.1.0 tag commit and `main` (2.0.1); they are identical, but the rest of the 2.0.x diff was
  not reviewed, so "upgrading 1.1.0 → 2.0.1 is source-compatible" is an expectation, not a
  verified fact.
- The `AuthClientSamples/` folder (Blazor Web App client) and the `NET8.0/` internals beyond the
  Web `.csproj` files were not read in detail.
- nuget.org "latest stable" values are a snapshot of 2026-09-20 and will drift.

---

## Useful Links

- [Repository](https://github.com/Calabonga/Microservice-Template) · [Changelog (English)](https://github.com/Calabonga/Microservice-Template/blob/master/README-en.md)
- [Wiki / installation](https://github.com/Calabonga/Microservice-Template/wiki)
- [Blazor Web App Sample](https://github.com/Calabonga/Microservice-Template/wiki/Blazor-Web-App-Sample)
- [Mediator (martinothamar)](https://github.com/martinothamar/Mediator) — the actual mediator in use
- [Calabonga.Results](https://github.com/Calabonga/Calabonga.Results)
- [Calabonga.UnitOfWork](https://github.com/Calabonga/UnitOfWork)
- [Calabonga.PagedListCore](https://github.com/Calabonga/Calabonga.PagedListCore)
- [Calabonga.AspNetCore.AppDefinitions](https://www.nuget.org/packages/Calabonga.AspNetCore.AppDefinitions)
- [OpenIddict](https://github.com/openiddict/openiddict-core)
- [Author's blog](https://www.calabonga.net)
