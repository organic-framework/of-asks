---
name: decide-to-ask
description: Decide whether a question goes to the owner at all, and in what form - a question, a task for the owner's hands, the unit owner, or your own decision. Use before every `of ask`, and whenever you are about to leave a question for the owner in your pane.
---

# Decide whether to ask the owner

From organic-framework AGENTS.md, "Nobody waits unseen" and "Asking the founder (or any human owner)".

1. **Don't ask what you may decide yourself** within your mandate and grants. In a delegated unit, ask the unit
   owner first; the owner gets only escalations.
2. **Check what he already decided** before asking him to grant or confirm something: `of asks --all`, the grants.
3. **Never leave a question in your pane.** A question that stays there is invisible: ask only with `of ask`. OF
   finds one left in a closing message and files it for you, or types a correction in.
4. **Work for his own hands is a task**, not a question: a key, a login, a token, a payment, a click in a UI.
   `of ask "<title>" --task "<steps>" [--command …] [--where phone|browser|machine]`. One task is one sitting of
   his hands; a step that waits for a signal or a yes is its own task, filed when it can be done.
5. **One decision per ask.** Several decisions are several asks, or numbered.
6. **Correct an open ask by amending it** (`of ask --amend <id> "<new text>"`), never by a replacement card. A
   different decision is a new ask, with the old one withdrawn.
7. **A question another position carries is theirs.** Name its card id (`OF-230`) in your message; do not file it
   again.

Then write the card: the skill write-card.
