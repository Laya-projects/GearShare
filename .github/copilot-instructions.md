Project: GearShare Mini. Full spec is in SPEC.md. Read it before any task.
Rules:
- Output and error messages must match the SPEC.md samples exactly. TODAY=2026-11-03.
- No `if tier ==` anywhere; use polymorphism.
- Pass `today` into methods; never call date.today() inside them.
- Parameterised SQL only. No SQL in the GearShare class.
- Work one numbered task at a time. Commit after each task, naming the rule (R1..R10).
- Add tests for every rule; run pytest before saying a task is done.
- Append decisions to DECISIONS.md and each prompt to AI_LOG.md.