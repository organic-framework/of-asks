-- The records of-asks writes to the event store today (docs/events.md), and who writes each. Read by main.lua as
-- plain data; tests/test_bench_of_asks.py checks the list against the code.
return {
  { name = "of.agent_question",          writer = "of ask; the hook (a permission prompt, a heuristic candidate); the judge (a pane card)" },
  { name = "of.ask_amended",             writer = "of ask --amend" },
  { name = "of.ask_ref",                 writer = "the pulse (a card id given later)" },
  { name = "of.agent_question_judged",   writer = "the judge" },
  { name = "of.agent_question_answered", writer = "the popup and the panel; of asks answer; of status --answered; the relay" },
  { name = "of.ask_withdrawn",           writer = "of status; the popup; reconcile" },
  { name = "of.ask_escalated",           writer = "the pulse; of ask" },
  { name = "of.permission_request",      writer = "the hook" },
}
