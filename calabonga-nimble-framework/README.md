# calabonga-nimble-framework skill

An AI agent skill that provides coding guidelines, architecture context, and project conventions
for the [Nimble Framework](https://github.com/Calabonga/Microservice-Template) — the ASP.NET Core
microservice template set by Sergey Calabonga.

Scope: the **NET10.0** generation of the template repository.
Verified against `master` @ `ad82376` (commit dated 2026-08-27) on **2026-09-20**; template
packages on nuget.org were at 10.0.5. Every code example in the skill is copied from a real
file in that commit, with the path stated next to it.

## What it does

When added to your AI agent (Claude, Cursor, GitHub Copilot), this skill activates when you work
with Nimble Framework code. It helps the agent:

- Use the real project layout — `{Name}.Domain` / `{Name}.Infrastructure` / `{Name}.Web`,
  `.slnx` solutions, `Definitions/*` composition via AppDefinitions
- Write CQRS the way the templates do: a `public static class` per operation with nested
  `Request` (a `record`) and `Handler`, `using Mediator;`, `ValueTask` returns
- Use `Calabonga.Results` correctly — package `Calabonga.Results`, namespace
  `Calabonga.OperationResults`, `Operation<T, string>`, `Operation.Result(...)` / `Operation.Error(...)`
- Map objects with hand-written `{Entity}Mapping` extension methods, because **no mapper
  library is present** in NET9/NET10
- Avoid libraries that were dropped (MediatR, AutoMapper, OperationResultCore, the Swashbuckle
  document generator) and API names that were renamed (`Logout` → `EndSession`)
- Pin package versions to what the templates actually ship, and know which upgrades are risky
- Write commit messages in the project's conventional format

## Skill contents

```
calabonga-nimble-framework/
├── SKILL.md                      # Guidelines, conventions, verified code examples
└── references/
    └── tech-stack.md             # Per-template package inventory, TFMs, generation history
```

## Tech stack covered (NET10.0, as pinned by the templates)

| Library | Version in templates | Role |
|---|---|---|
| [Mediator](https://github.com/martinothamar/Mediator) (`Mediator.Abstractions` + `Mediator.SourceGenerator`) | 3.0.2 | CQRS mediator, source-generated (replaced MediatR in 9.1.0) |
| `Calabonga.AspNetCore.AppDefinitions` | 10.0.0 | Composition: one `AppDefinition` per concern |
| `Calabonga.UnitOfWork` | 10.0.1 | Unit of Work / repositories over EF Core |
| `Calabonga.Results` | 1.1.0 | `Operation<T, TError>` results (replaced OperationResultCore in 8.0.1) |
| `Calabonga.PagedListCore` | 2.0.0 (transitive) | `IPagedList<T>`, `PagedList.From(...)` |
| `Calabonga.PredicatesBuilder` / `Calabonga.Microservices.Core` | 2.0.2 / 6.0.0 | Predicate composition, shared constants |
| `OpenIddict.AspNetCore` / `.EntityFrameworkCore` | 7.6.1 | OAuth2/OIDC — validation, server or client depending on template |
| EF Core, ASP.NET Core packages | 10.0.11 | ORM, auth handlers, OpenAPI |
| `FluentValidation` (+ DI extensions) | 12.1.1 | Request validation via a Mediator pipeline behavior |
| `Microsoft.AspNetCore.OpenApi` + `Swashbuckle.AspNetCore.SwaggerUI` | 10.0.11 / 10.2.3 | OpenAPI document + UI only |
| `Serilog.AspNetCore` | 10.0.0 | Logging |

**Object mapping: none.** AutoMapper was removed in 9.1.0 and nothing replaced it — the
templates use hand-written static extension methods. Mapster has never been part of them.

## The three templates

| NuGet package | What it is |
|---|---|
| `Calabonga.Microservice.Module.Template` | Minimal-API microservice, OpenIddict **validation** (resource server) |
| `Calabonga.Microservice.IdentityModule.Template` | The same plus a full OpenIddict **authorization server** |
| `Calabonga.AspNetCoreRazorPages.Template` | Razor Pages UI, OpenIddict **client** (added in 9.2.0) |

```bash
dotnet new install Calabonga.Microservice.Module.Template
dotnet new install Calabonga.Microservice.IdentityModule.Template
dotnet new install Calabonga.AspNetCoreRazorPages.Template
```

## Installation

```bash
npx skills add dlimkin/agent-skills --skill calabonga-nimble-framework
```

## Requirements

- An ASP.NET Core project generated from the **NET10.0** generation of the
  [Nimble Framework](https://github.com/Calabonga/Microservice-Template) templates
  (template package 10.x). The NET8.0 and NET9.0 generations differ — the skill documents
  what changed and when, but its conventions target NET10.0.
- Claude, Cursor, or GitHub Copilot with skills support.

## Links

- [Nimble Framework repository](https://github.com/Calabonga/Microservice-Template) · [changelog](https://github.com/Calabonga/Microservice-Template/blob/master/README-en.md)
- [Wiki / installation](https://github.com/Calabonga/Microservice-Template/wiki)
- [Mediator (martinothamar)](https://github.com/martinothamar/Mediator) — the mediator actually used
- [Calabonga.Results](https://github.com/Calabonga/Calabonga.Results)
- [Calabonga.UnitOfWork](https://github.com/Calabonga/UnitOfWork)
- [Calabonga.PagedListCore](https://github.com/Calabonga/Calabonga.PagedListCore)
