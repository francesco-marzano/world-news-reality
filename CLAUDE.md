# CLAUDE.md

@AGENTS.md

## Working autonomously

When a step doesn't need Francesco, keep going. Stop and ask only when you can't continue
without him, or before anything destructive or hard to undo. A level 2 change always stops
at the plan.

## TASKS.md

`TASKS.md` is the memory between sessions. Read it at the start, keep it current while you
work, and leave it accurate when you stop, whatever the reason. Its second line is
`Status:` followed by one of `in-progress`, `awaiting-approval`, `blocked`, `done`.
Set `done` only when the step is finished: the Stop hook then runs `just check` and hands
you back any failure before you can finish.

## End of a run

Close with a summary in three parts, in this order: what is waiting on Francesco, what
changed (with the command that proved it), what you found along the way.

## Skills and subagents

- `/autopilot <issue>` takes one milestone step from issue to pull request. Only Francesco starts it.
- Before opening a pull request, ask the `reviewer` subagent for a review. It starts from a
  clean context and sees only the issue, the diff and `REVIEW.md`. Fix what it verified,
  for at most three rounds.
- `source-scout` is the only agent that browses the web. Use it to check an outlet's feeds,
  robots.txt and terms before proposing a source.
