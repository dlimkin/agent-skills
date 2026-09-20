# Tech Stack — NET10.0 generation, package inventory and replacement history

**Verified against the repository on 2026-09-20**: <https://github.com/Calabonga/Microservice-Template>,
branch `master`, commit `ad82376a3583e138cc5b59439756f0433b273c63` (2026-08-27).
Package metadata read from `api.nuget.org` `.nuspec` files on the same date.
Nothing here was produced by generating or building a template — see "Not verified" in `SKILL.md`.

---

## 1. Exact package lists per template (NET10.0)

All twelve `.csproj` files target `net10.0` with `ImplicitUsings=enable` and `Nullable=enable`.
`InvariantGlobalization=false` is set in the Module and IdentityModule templates, not in RazorPages.

### Calabonga.Microservice.Module.Template

`content/Calabonga.Microservice.Module.Domain/…csproj` — **no PackageReference at all.**

`content/Calabonga.Microservice.Module.Infrastructure/…csproj`:

```xml
<PackageReference Include="Calabonga.Results" Version="1.1.0" />
<PackageReference Include="Calabonga.UnitOfWork" Version="10.0.1" />
<PackageReference Include="Calabonga.PredicatesBuilder" Version="2.0.2" />
<PackageReference Include="Calabonga.Microservices.Core" Version="6.0.0" />
<PackageReference Include="Microsoft.EntityFrameworkCore" Version="10.0.11" />
<PackageReference Include="Microsoft.EntityFrameworkCore.InMemory" Version="10.0.11" />
<PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" Version="10.0.11" />
```

`content/Calabonga.Microservice.Module.Web/…csproj`:

```xml
<PackageReference Include="Calabonga.AspNetCore.AppDefinitions" Version="10.0.0" />
<PackageReference Include="FluentValidation" Version="12.1.1" />
<PackageReference Include="FluentValidation.DependencyInjectionExtensions" Version="12.1.1" />
<PackageReference Include="Mediator.Abstractions" Version="3.0.2" />
<PackageReference Include="Mediator.SourceGenerator" Version="3.0.2" />   <!-- PrivateAssets=all -->
<PackageReference Include="Microsoft.AspNetCore.Authentication.OpenIdConnect" Version="10.0.11" />
<PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="10.0.11" />
<PackageReference Include="Microsoft.AspNetCore.Components.QuickGrid.EntityFrameworkAdapter" Version="10.0.11" />
<PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="10.0.11" />
<PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="10.0.11" />  <!-- PrivateAssets=all -->
<PackageReference Include="Microsoft.VisualStudio.Web.CodeGeneration.Design" Version="10.0.2" />
<PackageReference Include="OpenIddict.AspNetCore" Version="7.6.1" />
<PackageReference Include="Serilog.AspNetCore" Version="10.0.0" />
<PackageReference Include="Serilog.Formatting.Compact" Version="3.0.0" />
<PackageReference Include="Serilog.Sinks.Console" Version="6.1.1" />
<PackageReference Include="Serilog.Sinks.File" Version="7.0.0" />
<PackageReference Include="Swashbuckle.AspNetCore.SwaggerUI" Version="10.2.3" />
```

### Calabonga.Microservice.IdentityModule.Template

Domain: **no PackageReference.**

Infrastructure: `Calabonga.Results` 1.1.0, `Calabonga.UnitOfWork` 10.0.1,
`Calabonga.PredicatesBuilder` 2.0.2, `Microsoft.EntityFrameworkCore` 10.0.11,
`.InMemory` 10.0.11, `.Tools` 10.0.11, `Microsoft.AspNetCore.Identity.EntityFrameworkCore` 10.0.11,
**`OpenIddict.EntityFrameworkCore` 7.6.1**.

Web: same as the Module Web list except — adds `Calabonga.Microservices.Core` 6.0.0 and
`System.Linq.Async` 7.0.1, uses `Microsoft.EntityFrameworkCore.Design` 10.0.11 instead of
`.Tools`, and has no `Microsoft.AspNetCore.Authentication.OpenIdConnect`,
no `QuickGrid.EntityFrameworkAdapter`, no `Microsoft.VisualStudio.Web.CodeGeneration.Design`.

### Calabonga.AspNetCoreRazorPages.Template

Domain: `Calabonga.Results` 1.1.0 (the only Domain project in the repo with a package reference).

Infrastructure: `Calabonga.UnitOfWork` 10.0.1, `Calabonga.PredicatesBuilder` 2.0.2,
`Calabonga.Microservices.Core` 6.0.0, `Microsoft.EntityFrameworkCore` 10.0.11,
`.Design` 10.0.11, `.Relational` 10.0.11, `.InMemory` 10.0.11,
`OpenIddict.EntityFrameworkCore` 7.6.1.

Web: `Microsoft.AspNetCore.Authentication.OpenIdConnect` 10.0.11 (`NoWarn="NU1605"`),
`Calabonga.AspNetCore.AppDefinitions` 10.0.0, `FluentValidation` (+ DI) 12.1.1,
`Mediator.Abstractions` 3.0.2, `Mediator.SourceGenerator` 3.0.2,
`Microsoft.Extensions.Caching.StackExchangeRedis` 10.0.11,
`Microsoft.VisualStudio.Web.CodeGeneration.Design` 10.0.2, `OpenIddict.AspNetCore` 7.6.1,
`Serilog.AspNetCore` 10.0.0, `Serilog.Sinks.Console` 6.1.1.
**No OpenApi, no SwaggerUI, no `Microsoft.AspNetCore.OpenApi`** — it is a UI, not an API.

---

## 2. Target frameworks of the Calabonga libraries

From each package's `.nuspec` dependency groups:

| Package | Version | Target framework(s) |
|---|---|---|
| `Calabonga.UnitOfWork` | 6.2.0 | `net8.0`, `net9.0` |
| `Calabonga.UnitOfWork` | 10.0.1 / 10.0.2 / 10.0.3 | `net10.0` only |
| `Calabonga.AspNetCore.AppDefinitions` | 2.4.3 | `net6.0`, `net8.0` |
| `Calabonga.AspNetCore.AppDefinitions` | 3.0.0 | `net8.0` ("Migration to NET8") |
| `Calabonga.AspNetCore.AppDefinitions` | 4.0.0 | `net9.0` ("Migration to NET9") |
| `Calabonga.AspNetCore.AppDefinitions` | 10.0.0 / 10.0.1 | `net10.0` ("Migration to NET10") |
| `Calabonga.Results` | 1.1.0 and 2.0.1 | `netstandard2.1` |
| `Calabonga.PagedListCore` | 2.0.0 and 3.0.0 | `netstandard2.1` |
| `Calabonga.Microservices.Core` | 6.0.0 | `netstandard2.1` |
| `Calabonga.PredicatesBuilder` | 2.0.2 | `netstandard2.1` |

So only `UnitOfWork` 10.x and `AppDefinitions` 10.x actually require net10; the result,
paging, predicate and core-helper packages are `netstandard2.1` and impose nothing.

.NET platform support, from `dotnet/core` → `release-notes/releases-index.json` (read 2026-09-20):

| Channel | Type | Phase | End of support |
|---|---|---|---|
| 8.0 | LTS | maintenance | **2026-11-10** |
| 9.0 | STS | maintenance | **2026-11-10** |
| 10.0 | LTS | active | **2028-11-14** |

---

## 3. Transitive dependency that matters: PagedListCore

| `Calabonga.UnitOfWork` | pulls `Calabonga.PagedListCore` |
|---|---|
| 6.2.0 | 1.0.4 |
| 10.0.1 (pinned by the templates) | **2.0.0** |
| 10.0.3 (latest) | **3.0.0** |

`Calabonga.PagedListCore` 3.0.0 release notes: *"PageIndex unified to 1-based;
HasPreviousPage/HasNextPage off-by-one fixed; argument validation added. Breaking change."*

Template code assumes 0-based paging (`int pageIndex = 0` default in
`Endpoints/EventItemEndpoints.cs`, and the `pagedList.PageIndex > pagedList.TotalPages`
re-query in `GetEventItemPaged.cs`). Bumping `Calabonga.UnitOfWork` from 10.0.1 to 10.0.3
changes paging semantics through this transitive edge. Review the paging code before upgrading.

---

## 4. The mediator: martinothamar/Mediator, not Mediator.Net

The repository changelog for version 9.1.0 says MediatR was replaced with
"[Mediator.Net](https://github.com/mayuanyang/Mediator.Net)". That link is wrong for the code
that actually ships. Evidence:

- The packages referenced are `Mediator.Abstractions` and `Mediator.SourceGenerator`.
- Their `.nuspec` metadata: `<authors>Martin Othamar</authors>`,
  `<projectUrl>https://github.com/martinothamar/Mediator</projectUrl>`,
  `<repository url="https://github.com/martinothamar/Mediator" />`,
  description "A high performance .NET Mediator pattern implemenation using source generation."
- The API used in the templates is martinothamar's:
  `IRequest<TResponse>`, `IRequestHandler<TRequest, TResponse>` with
  `ValueTask<TResponse> Handle(TRequest, CancellationToken)`,
  `IPipelineBehavior<TRequest, TResponse>` with
  `ValueTask<TResponse> Handle(TRequest message, MessageHandlerDelegate<TRequest, TResponse> next, CancellationToken)`,
  registration `services.AddMediator(options => options.ServiceLifetime = ServiceLifetime.Scoped)`.
  The `Mediator.Net` package id (mayuanyang) is never referenced, and none of its registration
  entry points appear anywhere in the templates.

Pipeline behavior, verbatim from
`NET10.0/Calabonga.Microservice.Module.Template/content/Calabonga.Microservice.Module.Web/Definitions/Mediator/Base/UnitOfWorkTransactionBehavior.cs`:

```csharp
public class TransactionBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IUnitOfWork _unitOfWork;

    public TransactionBehavior(IUnitOfWork unitOfWork) => _unitOfWork = unitOfWork;

    public async ValueTask<TResponse> Handle(TRequest message, MessageHandlerDelegate<TRequest, TResponse> next, CancellationToken cancellationToken)
    {
        await using var transaction = await _unitOfWork.BeginTransactionAsync();
        try
        {
            var response = await next(message, cancellationToken);
            await transaction.CommitAsync(cancellationToken);
            return response;
        }
        catch (Exception)
        {
            await transaction.RollbackAsync(cancellationToken);
            throw;
        }
    }
}
```

Note the class is named `TransactionBehavior` although the file is `UnitOfWorkTransactionBehavior.cs`,
and that in the Module template only `ValidatorBehavior<,>` is registered in
`MediatorDefinition.cs` — the transaction behavior ships unregistered.

---

## 5. Mapping: no mapper library in any generation since NET9

- `NET8.0/` Web projects reference `Automapper` 13.0.1.
- `NET9.0/` and `NET10.0/` reference **no** mapping package. Verified by fetching all 32
  `.csproj` files in `NET8.0/`, `NET9.0/` and `NET10.0/`: `Mapster` appears in **zero** of them,
  and `AutoMapper` appears as a `PackageReference` only in the two `NET8.0/` Web projects
  (`Automapper` 13.0.1) — elsewhere it survives only inside stale `<Description>` packaging text.
- Replacement is hand-written extension methods, one static class per entity. The template
  file even says so in its XML doc comment (`EventItemMapping.cs`: `/// Replacement for Automapper`).

**Mapster was never part of these templates.** Any guidance mentioning `Adapt<T>()`,
`TypeAdapterConfig`, `ServiceMapper` or `IMapper` for this codebase is wrong.

Stale evidence to ignore: the template packaging metadata in
`NET10.0/Calabonga.Microservice.Module.Template/Calabonga.Microservice.Module.Template.csproj`
still has `<Description>Microservice template on Minimal API with Automapper, FluentValidation
and other helpful thing</Description>`. It describes an older generation.

---

## 6. Results: `Calabonga.Results` package, `Calabonga.OperationResults` namespace

Replaced `OperationResultCore` in version 8.0.1 (2024-02-06). The package id and the root
namespace differ — the package's own release note reads "Root namespace renamed from
Calabonga.Results to Calabonga.OperationResults".

Public shape, from `src/Calabonga.Results/Operation.cs` at the 1.1.0 commit
(`234810170a400ad361843b291470f7716a4ea1ed`):

```csharp
namespace Calabonga.OperationResults
{
    public readonly struct Operation<T>
    {
        public T Result { get; }
        public bool Ok { get; }
        public static implicit operator bool(Operation<T> result) => result.Ok;
        public static implicit operator Operation<T>(T result) => new Operation<T>(result);
        public static implicit operator Operation<T>(SuccessResult<T> result) => new Operation<T>(result.Result);
        public static implicit operator Operation<T>(ErrorResult result) => Error;
    }

    public readonly struct Operation<T, T1>
    {
        public readonly T1 Error;      // public FIELD, not a property
        public T Result { get; }
        public bool Ok { get; }
        public void Deconstruct(out T result, out T1 error) { result = Result; error = Error; }
        public static implicit operator Operation<T, T1>(SuccessResult<T> result) => ...;
        public static implicit operator Operation<T, T1>(ErrorResult<T1> result) => ...;
    }
    // also Operation<T, T1, T2> and Operation<T, T1, T2, T3>, whose Error is `object?`
}
```

Factory helpers, from `src/Calabonga.Results/OperationHelpers.cs`:

```csharp
public static class Operation
{
    public static SuccessResult Result();
    public static SuccessResult<T> Result<T>(T result);
    public static ErrorResult Error();
    public static ErrorResult<T> Error<T>(T error);
}
```

So `Operation.Result(x)` and `Operation.Error(msg)` do not return an `Operation<...>` directly —
they return `SuccessResult<T>` / `ErrorResult<T>`, which convert implicitly at the `return`
statement. Assigning them to a `var` and then returning will not compile the same way; return
them directly, as the templates do.

Usage in the templates (`GetEventItemById.cs`):

```csharp
if (entityWithoutIncludes == null)
{
    return Operation.Error($"Entity with identifier {id} not found");
}

var mapped = entityWithoutIncludes.MapToViewModel();
if (mapped is not null)
{
    return Operation.Result(mapped);
}

return Operation.Error(AppData.Exceptions.MappingException);
```

`Operation.cs` and `OperationHelpers.cs` are byte-identical between the 1.1.0 commit and
`main` (2.0.1), so the upgrade looks source-compatible — but the rest of the 2.0.x diff was
not reviewed, so treat that as an expectation.

The older API `OperationResult.CreateResult(...)` belongs to `OperationResultCore` and does
not exist in this stack.

---

## 7. OpenAPI: Microsoft generator + Swagger UI

Changed in version 9.0.0 (2024-11-26): `Swashbuckle.AspNetCore` (the document generator) was
removed, `Microsoft.AspNetCore.OpenApi` became the generator, and
`Swashbuckle.AspNetCore.SwaggerUI` was kept purely as the UI over `/openapi/v1.json`.

In NET10.0 (`…/Definitions/OpenApi/OpenApiDefinition.cs`) the document transformer registers
an `oauth2` security scheme with the Authorization Code flow pointed at
`{AuthServer:Url}/connect/authorize` and `/connect/token`, applies it as a global security
requirement, and in Development calls `app.MapOpenApi()` plus `app.UseSwaggerUI(...)` with
`OAuthUsePkce()`, `OAuthClientId("client-id-code")`.

The `template.json` blurb claims the UI is Scalar. No Scalar package is referenced anywhere;
the wired-up UI is Swagger UI.

---

## 8. OpenIddict 7.6.1 — three different roles

| Template | Call chain | Notable options |
|---|---|---|
| Module | `AddOpenIddict().AddValidation()` | `UseLocalServer()`, `UseAspNetCore()` |
| IdentityModule | `.AddCore().AddServer().AddValidation()` | EF Core stores with `ReplaceDefaultEntities<Guid>()`; code flow + PKCE, password, client credentials, refresh; ephemeral/development keys; `OpenIddictWorker` seeds clients `client-id-sts` and `client-id-code` |
| RazorPages | `.AddCore().AddClient()` | `AllowAuthorizationCodeFlow()`, `UseSystemNetHttp()`, one `OpenIddictClientRegistration` reading `AuthService:Url` / `ClientId` / `ClientSecret` |

`Logout` → `EndSession` rename (OpenIddict 6.0, adopted in template 9.0.2) is still the correct
API in 7.6.1:

```csharp
// IdentityModule Definitions/OpenIddict/OpenIddictDefinition.cs
.SetEndSessionEndpointUris("connect/logout")
// ...
.EnableEndSessionEndpointPassthrough()

// IdentityModule HostedServices/OpenIddictWorker.cs
OpenIddictConstants.Permissions.Endpoints.EndSession,
```

The endpoint *path* is still `connect/logout` and the Razor pages are still
`Pages/Connect/Login.cshtml` / `Logout.cshtml` — only the .NET API names changed.
Whether the old `Logout` constants were removed or merely obsoleted in OpenIddict 6.x was not
checked against OpenIddict's own sources.

---

## 9. Replacement history, tied to generations

| Template version (date) | Change | First folder that ships it |
|---|---|---|
| 8.0.0 (2023-11-20) | first NET8 templates; Bearer added alongside Cookie in IdentityModule | `NET8.0/` |
| 8.0.1 (2024-02-06) | `OperationResultCore` → `Calabonga.Results` | `NET8.0/` |
| 9.0.0 (2024-11-26) | net9; `Swashbuckle.AspNetCore` generator removed, `Microsoft.AspNetCore.OpenApi` in, SwaggerUI kept as UI | `NET9.0/` |
| 9.0.1 (2024-12-13) | introspection endpoint + PKCE for authorization code flow | `NET9.0/` |
| 9.0.2 (2024-12-25) | OpenIddict 6.0: `Logout` → `EndSession`; `AuthClientSamples/Calabonga.BlazorApp` added | `NET9.0/` |
| 9.1.0 (2025-06-16) | `MediatR` → martinothamar `Mediator` (source-generated); `AutoMapper` removed with no replacement library | `NET9.0/` |
| 9.2.0 (2025-09-11) | `Calabonga.AspNetCoreRazorPages.Template` added (third template) | `NET9.0/` |
| 10.0.0 (2026-02-14) | everything moved to net10; OpenAPI gains a `Bearer` scheme, `OAuth2.0` scheme updated | `NET10.0/` |
| 2026-08-27 (no version heading) | AppDefinitions 4.0.0→10.0.0, MS packages 10.0.3→10.0.11, OpenIddict 7.2.0→7.6.1, Mediator 3.0.1→3.0.2, SwaggerUI 10.1.2→10.2.3, UnitOfWork 10.0.0→10.0.1, `System.Linq.Async` 7.0.0→7.0.1; CI unified into `publish-templates.yml` with Nerdbank.GitVersioning per-template versioning | `NET10.0/` |

Cross-generation package snapshot (Web projects, for orientation):

| | NET8.0 | NET9.0 | NET10.0 |
|---|---|---|---|
| Mediator | `MediatR` 12.4.1 | `Mediator.Abstractions`/`.SourceGenerator` 3.0.1 | 3.0.2 |
| Mapping | `Automapper` 13.0.1 | none | none |
| OpenIddict | 5.8.0 | 7.0.0 | 7.6.1 |
| OpenAPI | `Swashbuckle.AspNetCore` 6.7.3 + `Microsoft.AspNetCore.OpenApi` 8.0.8 | `Swashbuckle.AspNetCore.SwaggerUI` 9.0.4 + OpenApi 9.0.8 | SwaggerUI 10.2.3 + OpenApi 10.0.11 |
| AppDefinitions | 2.4.3 | 4.0.0 | 10.0.0 |
| FluentValidation | 11.10.0 | 12.0.0 | 12.1.1 |
| Templates in folder | 2 | 3 | 3 |

Project layout is `Domain` / `Infrastructure` / `Web` in **all three** generations. No
generation has ever had `{Name}.Entities` or `{Name}.Application` projects.

---

## 10. Repository's own convention files

The template repo carries agent rules of its own under `.claude/rules/` — worth reading before
proposing a structural change:

- `architecture.md` — dependency direction, "Domain has no PackageReference", where interfaces live.
- `conventions.md` — the CQRS naming rules reproduced in `SKILL.md`, including the note that
  the nested `Request`/`Handler` pattern is "`Mediator`, not MediatR".
- `code-styles.md`, `testing.md`, `workflow.md` — not summarised here.
- `.claude/skills/nuget-update/` — the author's own skill that bumps package versions in
  `NET10.0/` (patch + minor automatically, major on confirmation), which is why the pinned
  versions move as a batch.
