#!/bin/sh
# of-asks's tests: the asks tests of the organic-framework checkout the package runs on (no behaviour of its own in
# this version, so the code's own tests are the package's), then the package's own checks. Bench runs this in the
# package's folder (`bench test of-asks`, a rebase) and reads unittest's verbose lines.
#   OF_HOME   the organic-framework checkout (default: the one the `of` on PATH runs from)
set -u
here=$(pwd)
if [ -z "${OF_HOME:-}" ]; then
  of=$(command -v of) || { echo "not ok 1 - an organic-framework checkout: set OF_HOME, or put of on PATH"; exit 1; }
  OF_HOME=$(cd "$(dirname "$(readlink -f "$of")")/.." && pwd)
fi
[ -f "$OF_HOME/bin/of_asks.py" ] || { echo "not ok 1 - $OF_HOME holds no bin/of_asks.py"; exit 1; }
cd "$OF_HOME" || exit 1
python3 -m unittest -v tests.test_ask_amend tests.test_ask_text tests.test_asks_answer tests.test_asks_chat \
  tests.test_asks_inbox tests.test_asks_live tests.test_asks_permission tests.test_blocked tests.test_card_ids \
  tests.test_card_refs tests.test_owner_panel tests.test_guard_asks_outbox tests.test_pulse tests.test_fold 2>&1
rc=$?
cd "$here" || exit 1
python3 "$here/tests/package.py" -v 2>&1 || rc=1
exit $rc
