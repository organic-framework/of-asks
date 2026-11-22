"""The package's tests of the module "file", run on the module as an organization extends it (organic-framework-build
reports/framework/metamethod/11-first-slice.md, part 5: "the package's tests of 'file' run on the module as
extended"; of_metamethod, message 01a20588-412e).

The organic-framework tests that file a card through `of ask` run twice, each time with every `of ask` they start
calling an organization's hook before "file":
  1. a hook that passes every card: every test still holds;
  2. a hook that stops a card tagged "money": the tests that expected such a card filed no longer hold, and are named.
As part 6 does for a fork, this shows which of the package's promises an organization's version still keeps; it does
not forbid the hook.

The hook is installed as an organization installs it (a Benchfile naming this package, extensions/of-asks/*.lua,
`of bench install`'s framework, of_method.on_install) into a throwaway organization, and evaluated by Bench as at work,
inside its outer layer: run it where that layer starts (outside an agent session). A sitecustomize module, put on the
test processes' PYTHONPATH only, makes of_asks_package.before_file ask that organization's hooks for every card.

    OF_HOME=<organic-framework checkout> python3 tests/as_extended.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OF_HOME = os.environ.get("OF_HOME") or (
    os.path.dirname(os.path.dirname(os.path.realpath(shutil.which("of")))) if shutil.which("of") else "")

# the organic-framework tests of the module "file": every test module that files a card through `of ask` (its command
# or cmd_ask), but test_bench_of_asks, which installs hooks of its own
FILE_TESTS = ["tests.test_ask_text", "tests.test_ask_amend", "tests.test_asks_chat", "tests.test_door",
              "tests.test_diagnose_rules", "tests.test_of", "tests.test_loop", "tests.test_pulse", "tests.test_tempo"]

HOOKS = {
    "passes every card": '''
before "file" {
  written_for = "of-asks 1",
  run = function(card, ctx) return "pass" end,
}
''',
    "stops a card tagged money": '''
before "file" {
  written_for = "of-asks 1",
  run = function(card, ctx)
    for _, t in ipairs(card.tags or {}) do
      if t == "money" then return { decision = "stop", reason = "money cards go to finance first" } end
    end
    return "pass"
  end,
}
''',
}

SITECUSTOMIZE = '''
# Written by of-asks's tests/as_extended.py for one run of the tests of "file": every `of ask` asks the throwaway
# organization's hooks. Never installed anywhere else.
import os, sys
_of_bin = os.path.join(os.environ["AS_EXTENDED_OF_HOME"], "bin")
if _of_bin not in sys.path:
    sys.path.insert(0, _of_bin)
# OF's tests give each test a home folder of its own, where OF's configuration names no Bench: the Bench this run
# installed with, found where the real configuration names it, is handed to of_method here
sys.path.insert(0, os.path.join(os.environ["AS_EXTENDED_BENCH"], "bin"))
import bench, of_asks_package, of_method
of_method.bench, of_method.BenchError, of_method._MISSING = bench, bench.BenchError, None
_org = os.environ["AS_EXTENDED_ORG"]
_log = os.environ["AS_EXTENDED_LOG"]


def _before_file(project, card, org=None, ask=None):
    card = {k: card[k] for k in of_asks_package.CARD_KEYS if k in card}
    d = of_method.before(_org, "of-asks", "file", card)
    with open(_log, "a") as f:
        f.write(d["decision"] + "\\n")
    return d


of_asks_package.before_file = _before_file
'''

UNITTEST = re.compile(r"^(test\w*) \(([\w.]+)\)(?:\n.*?)? \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure|"
                      r"unexpected success)$", re.M)


def install(org, hook):
    sys.path.insert(0, os.path.join(OF_HOME, "bin"))
    import of_method
    bench = of_method.bench
    if bench is None:
        raise SystemExit(f"no Bench where OF's configuration names it: {of_method._MISSING}")
    os.makedirs(os.path.join(org, "extensions", "of-asks"))
    with open(os.path.join(org, "Benchfile"), "w") as f:
        f.write(f'package("of-asks", {{ path = "{HERE}" }})\n')
    with open(os.path.join(org, "extensions", "of-asks", "hook.lua"), "w") as f:
        f.write(hook)
    bench.FRAMEWORK = of_method.on_install
    bench.install(org, log=lambda *a: None)
    return os.path.dirname(os.path.dirname(os.path.abspath(bench.__file__)))


def run(name, hook):
    t = tempfile.mkdtemp(prefix="of-asks-as-extended.")
    try:
        org, site, log = os.path.join(t, "org"), os.path.join(t, "site"), os.path.join(t, "decisions")
        os.makedirs(org)
        os.makedirs(site)
        bench_home = install(org, hook)
        with open(os.path.join(site, "sitecustomize.py"), "w") as f:
            f.write(SITECUSTOMIZE)
        env = dict(os.environ, PYTHONPATH=site + os.pathsep + os.environ.get("PYTHONPATH", ""),
                   AS_EXTENDED_OF_HOME=OF_HOME, AS_EXTENDED_BENCH=bench_home, AS_EXTENDED_ORG=org,
                   AS_EXTENDED_LOG=log)
        r = subprocess.run([sys.executable, "-m", "unittest", "-v", *FILE_TESTS], cwd=OF_HOME, env=env,
                           capture_output=True, text=True, timeout=1800)
        out = r.stdout + r.stderr
        def name(m):
            return m.group(2) if m.group(2).endswith(m.group(1)) else f"{m.group(2)}.{m.group(1)}"
        held = [name(m) for m in UNITTEST.finditer(out) if m.group(3) == "ok"]
        broke = [name(m) for m in UNITTEST.finditer(out) if m.group(3) in ("FAIL", "ERROR")]
        decisions = open(log).read().split() if os.path.exists(log) else []
        print(f"with a hook that {name}: {len(held)} hold, {len(broke)} do not; the hook decided "
              f"{len(decisions)} cards ({decisions.count('pass')} pass, {len(decisions) - decisions.count('pass')} "
              f"not)")
        for b in broke:
            print(f"  no longer holds: {b}")
        return held, broke, decisions
    finally:
        shutil.rmtree(t, ignore_errors=True)


def main():
    if not OF_HOME or not os.path.isfile(os.path.join(OF_HOME, "bin", "of_asks_package.py")):
        raise SystemExit("set OF_HOME to an organic-framework checkout with bin/of_asks_package.py")
    held1, broke1, dec1 = run("passes every card", HOOKS["passes every card"])
    held2, broke2, dec2 = run("stops a card tagged money", HOOKS["stops a card tagged money"])
    ok = bool(dec1) and not broke1 and bool(dec2)
    if not dec1:
        print("the hook decided no card: the tests did not reach it, so this run shows nothing")
    if broke1:
        print("a hook that passes every card broke tests: the module as extended does not keep its promises")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
