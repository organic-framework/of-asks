---
name: write-card
description: Write an `of ask` card the owner can answer between other work, without your context - the decision in one line, why now, short context, options with consequences and a recommendation, then evidence. Use for every question or task you file for the owner.
---

# Write a card for the owner

From organic-framework AGENTS.md, "Asking the founder (or any human owner)". He reads a card between other work,
without your context.

1. **The decision in one line**, a question he can answer, in his language and plain words.
2. **Why now**: the deadline and what happens if nobody answers.
3. **Context in 2 to 4 sentences**: which system, what happened, what you already checked. Spell out every internal
   name or id the first time.
4. **The options**, each with its consequence, risk and money cost; mark your recommendation and say why:
   `--options "yes, run it (recommended: …)|no, move it to Thursday"`.
5. **The evidence after the text**, never instead of it: links, log lines, file paths.

Rules:

- **No time estimates**: never how long something takes. A real deadline with its source stays.
- **Every claim that drives work carries its basis**: an ask id, a source with its quote, evidence, or "inference,
  unconfirmed".
- **The owner's decisions travel as card ids**, never retold: "the founder approved X (card `AS-412`)".
- Use `--tags` (`prod_change:<systems>`, `money`, `security_incident`, `irreversible`, `window_go:<systems>`);
  `--blocking` only when you really stop; `--due` only for a real deadline.
- **A task that makes a secret** says where it is run (a plain terminal, never an agent's pane or a chat) and where
  the value goes (a mode-600 file, read silently).
- **No at sign directly before a file path** in the card's text.

`of ask` refuses a time estimate (`bin/of_ask_text.py`); the rest is yours to keep.
