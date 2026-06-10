---
name: handoff-pro
description: >
  Universal context transfer skill for both agent-to-agent continuation and PM reporting.
  Produces a compact but information-dense handoff artifact that preserves reasoning state,
  execution progress, and decision history for reliable continuation in a fresh context.

trigger:
  - /handoff
  - session continuation
  - context limit approaching
  - "continue later"
  - "resume work"
  - completion report
  - handoff to agent or PM

mode: dual
  - agent_continuation
  - pm_reporting

---

# UNIFIED HANDOFF

## 1. Context (1–3 lines)
Summarize the actual intent of the work and current objective state.

---

## 2. Current State (Most Important)
Describe exactly where execution stopped.

- What is currently happening
- What is actively broken / incomplete
- What the system behaves like right now

---

## 3. Progress

### Completed
- [✔] Key milestone or task (with outcome)

### In Progress
- [~] What is partially done

---

## 4. Reasoning State (Critical for Agents)
Preserve decision logic and understanding.

### Hypotheses Tested
- Hypothesis → result

### What We Know So Far
- Key confirmed facts

### Unresolved Uncertainty
- What is still unknown or ambiguous

---

## 5. Decisions

- Decision → rationale
- Architectural choices that must NOT be reversed without reason

---

## 6. Dead Ends (Important Anti-Repetition Layer)

- Approach tried → why it failed
- Avoid repeating these in next session

---

## 7. Key Artifacts

### Files
- path/to/file → role/importance

### Commands / Queries
- Important commands executed

### External Systems
- CI, APIs, services, integrations used

---

## 8. Open Questions

- [ ] Questions blocking progress
- [ ] Decisions pending PM or agent

---

## 9. Risks / Issues

- Technical risks
- Unknown stability issues
- Performance / correctness concerns

---

## 10. Next Actions (Strict Priority Order)

1. HIGH  - immediate next step
2. HIGH  - next dependency
3. MEDIUM - follow-up work
4. LOW    - optional improvements

---

## 11. Output Modes

### If Agent Continuation Mode
Focus on:
- reasoning state
- open questions
- dead ends
- next actions

Minimize:
- PM-style summaries
- CI/git noise

---

### If PM Reporting Mode
Focus on:
- completed tasks
- verification
- risks
- next delivery steps

Minimize:
- internal reasoning details

---

## 12. Optional System Snapshot (if available)

- Git status: <optional>
- CI status: <optional>
- Test status: <optional>
- Build state: <optional>

---

# Design Principles

- Optimize for **lossless continuation of reasoning**, not just status reporting
- Avoid duplication of information across sections
- Prefer structured bullets over prose
- Never assume full context is available in next session
- Preserve *why*, not only *what*

---