# Learn a Skill

Author a new `SKILL.md` from whatever the user points you at: a local directory or file, an online documentation page, a workflow you just walked through together in this conversation, or notes/a procedure the user describes or pastes in. You do the sourcing yourself, with whatever tools you already have — there is no separate ingestion engine.

This skill does not itself perform the task described by the source. It produces a **new, separate skill file** that captures how to do the task, for reuse in future sessions.

## Installation
```bash
npx skills add dlimkin/agent-skills --skill learn
```

## When to Use

- The user runs `/learn <description>` or says "turn this into a skill", "learn how to do X", "remember this workflow", "make this repeatable"
- The user points you at a directory, SDK, or API and asks you to learn it
- The user asks you to capture something you (the agent) just did successfully, so it can be repeated later
- The user pastes a described procedure and asks for it to become a skill


## Когда использовать
- Пользователь запускает `/learn <описание>` или говорит "сделай из этого навык", "научи, как делать X", "запомни этот процесс", "сделай это повторяемым"
- Пользователь указывает вам каталог, SDK или API и просит вас изучить его
- Пользователь просит вас зафиксировать что-то, что вы (агент) только что успешно сделали, чтобы это можно было повторить позже
- Пользователь вставляет описанную процедуру и просит превратить её в навык