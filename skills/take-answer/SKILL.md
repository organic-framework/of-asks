---
name: take-answer
description: Take the owner's answer to your card - apply it, cite it by its card id, close the card, and for a task check the result first. Use when an answer, a reply or the owner's words reach you about a card you filed.
---

# Take the owner's answer

From organic-framework AGENTS.md, "Nobody waits unseen" and "Asking the founder (or any human owner)".

1. **An answer from the popup or the panel closes the card** and is typed into your pane, naming the version of an
   amended card it answered. Act on that version.
2. **His words in your session close none of your asks.** When they, a relay or a unit owner answered one, run
   `of status working --answered <id>`.
3. **A task closes only on its result.** When he says it is done, check it (the new key works), then
   `of status working --done-task <id>`; if it is not there, `of status working --reopen-task <id> --note "what you
   still see"`. Close the part he did the same turn.
4. **Cite the decision by its card id** wherever it drives work: "the founder approved X (card `AS-412`)".
5. **A pause or a decision covers only what his words name.** Anything next to it keeps or gets its own ask.
6. End the turn with `of status`.
