# of-asks

How an agent asks its owner a question, and how the owner sees and answers it: a Bench package for
[Organic Framework](https://github.com/organic-framework/organic-framework).

This version is a description over the code organic-framework has today (`of ask`, `of asks`, the judge, the pulse):
installing it changes no behaviour. It names the method's modules and the code that performs each (`main.lua`), the
records it writes and the view built from them (`records/`), and the skills an agent follows (`skills/`). It offers
an organization one setting and one module to extend. OF acts on them once organic-framework takes the change
that reads them (`bin/of_asks_package.py`, kept by `of_asks`); until then they are read and checked at install only:

| | | What it changes |
|---|---|---|
| setting | `escalate_after` (duration, default `2h`) | when a routed card that nobody answered rises to the owner, for a delegation whose `escalate_when` holds a bare `ask_unanswered` |
| hook | before `"file"` | a hook may stop a card before it is filed; `of ask` then names the hook and its reason |

```lua
-- Benchfile
package("of-asks", { git = "https://github.com/organic-framework/of-asks", ref = "main" })

-- config/settings/of-asks.lua
return { escalate_after = "4h" }
```

How to change a setting, write a hook and keep a fork: the skill `change-a-method` in Bench's repository.

## Tests

`sh tests/run.sh`, in this folder: the asks tests of the organic-framework checkout it runs on (`OF_HOME`, default
the one the `of` on PATH runs from), then the package's own checks (`tests/package.py`, which reads the package in
Bench's closed reader, Bench found where OF's configuration names it). Bench evaluates only inside an
operating-system sandbox that cannot start inside an agent session's own, so there the package's checks skip.

License: Apache-2.0.
