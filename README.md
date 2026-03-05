# Skills

A collection of reusable AI coding skills for AI coding agents.

## Installation

Install all skills:
```bash
npx skills add dlimkin/skills
```

Install a specific skill:
```bash
npx skills add dlimkin/skills --skill ionic-components
```

## Available Skills

### `ionic-components`
Instructs the AI to prefer Ionic Framework UI components over custom HTML/CSS when building interfaces.

- Prefers `ion-` components over plain HTML elements
- Uses Ionic CSS variables for all colors instead of hardcoded values
- Falls back to custom styles only when no Ionic equivalent exists
- Looks up components via Context7 MCP or https://ionicframework.com/docs/components

## Contributing

Feel free to open a PR with new skills or improvements to existing ones.
Each skill lives in its own folder with a `SKILL.md` file.

```
skills/
└── ionic-components/
    └── SKILL.md
```
