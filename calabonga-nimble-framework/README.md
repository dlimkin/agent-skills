# calabonga-nimble-framework skill

An AI agent skill that provides coding guidelines, architecture context, and project conventions for the [Nimble Framework](https://github.com/Calabonga/Microservice-Template) — a microservice template system for ASP.NET Core (.NET 10) by Sergey Calabonga.

## What it does

When added to your AI agent (GitHub Copilot, Cursor, or Claude), this skill automatically activates when you work with Nimble Framework code. It helps the agent:

- Follow the correct tech stack (Mediator.Net, Mapster, Calabonga.Results, OpenIddict 6.x)
- Generate CQRS code using the right patterns (`record`-based queries/commands)
- Avoid deprecated libraries (MediatR, AutoMapper, OperationResultCore, Swashbuckle generator)
- Write commit messages in the project's conventional format
- Apply correct OpenIddict 6.x API (`EndSession`, not `Logout`)

## Skill contents

```
nimble-framework/
├── SKILL.md                      # Core guidelines & code conventions
└── references/
    └── tech-stack.md             # Detailed migration notes (MediatR→Mediator.Net, AutoMapper→Mapster, etc.)
```

## Tech stack covered

| Library | Role |
|---------|------|
| Mediator.Net | CQRS mediator (replaces MediatR) |
| Mapster | Object mapping (replaces AutoMapper) |
| Calabonga.Results | Operation results, RFC7807 (replaces OperationResultCore) |
| OpenIddict 6.x | Authorization (IdentityModule template) |
| EntityFramework Core | ORM |
| FluentValidation | Request validation |
| Microsoft.AspNetCore.OpenApi | OpenAPI doc generation |
| Serilog | Logging |

## Installation

```bash
npx skills add dlimkin/agent-skills --skill calabonga-nimble-framework
```

## Requirements

- ASP.NET Core project based on [Nimble Framework](https://github.com/Calabonga/Microservice-Template) v9.x or v10.x
- GitHub Copilot, Cursor, or Claude with skills support

## Links

- [Nimble Framework repository](https://github.com/Calabonga/Microservice-Template)
- [Wiki / Documentation](https://github.com/Calabonga/Microservice-Template/wiki)
- [Mapster](https://github.com/MapsterMapper/Mapster)
- [Mediator.Net](https://github.com/mayuanyang/Mediator.Net)
- [Calabonga.Results](https://github.com/Calabonga/Calabonga.Results)
