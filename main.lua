-- of-asks: the method. Each module names the code that does its work today (paths in the organic-framework tree).
-- What an organization changes: the setting escalate_after (config/settings/of-asks.lua), read by the pulse for a
-- delegation's bare `ask_unanswered` rule, and a hook before the module "file" (extensions/of-asks/*.lua), called
-- by `of ask` before a card is filed (bin/of_asks_package.py).
local records = require "records.events"

roles { "asker", "decider" }             -- the decider is the owner, or the head of a delegated unit

subject "question" {
  states  = { "needed", "written", "filed", "delivered", "answered", "applied" },
  exits   = { "decided_by_asker", "withdrawn", "superseded" },
  records = records,
}

setting "escalate_after" { type = "duration", default = "2h" }   -- when an unanswered routed card rises

module "decide"     { by = skill "decide-to-ask" }
module "write-card" { by = skill "write-card", checks = "bin/of_ask_text.py" }
module "file"       { on = command "ask", code = "bin/of: cmd_ask; bin/of_events.py: record, card_ref" }
module "amend"      { on = command "ask --amend", code = "bin/of: cmd_ask" }
module "deliver"    { on = record "of.agent_question",
                      code = "bin/of_asks_tui.py, bin/of_asks_inbox.py, bin/of_herdr_asks.py, bin/of_asks_chat.py" }
module "remind"     { on = schedule "the pulse, every 5 minutes", code = "bin/of_pulse.py: escalations" }
module "answer"     { on = act "answer", by = role "decider", code = "bin/of_asks_answer.py" }
module "take-answer" { on = record "of.agent_question_answered", by = skill "take-answer" }
module "spot-question" { on = turn_end(), by = classifier "question",
                         code = "bin/of_classify.py (candidates), bin/of_judge.py (the judge)" }
module "blocked"    { on = turn_end(), code = "bin/of_blocked.py" }

extendable { "file" }
