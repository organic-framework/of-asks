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
# organization's hooks. Never installed anywhere else. It imports nothing of OF's at a process's start, so OF's test
# isolation (its own home and state folders) is in place before any OF module reads them: it only waits for OF to
# import of_asks_package, and patches that module then.
import importlib.abc, importlib.machinery, os, sys


def _before_file(project, card, org=None, ask=None):
    # the package's own before_file runs, for the throwaway organization: its lock check, its call to of_method.before
    # and its "any error stops the card" (of_asks on of-asks PR 1). OF's tests give each test a home folder of its own,
    # where the owner's configuration names no Bench: of_benchpath is pointed at the Bench this run installed with.
    try:
        import of_benchpath, of_method
        of_benchpath.home = lambda: os.environ["AS_EXTENDED_BENCH"]
        of_benchpath.ensure()
        bench = sys.modules["bench"]
        of_method.bench, of_method.BenchError, of_method._MISSING = bench, bench.BenchError, None
        d = _REAL[0](os.environ["AS_EXTENDED_ORG"], card, org=org, ask=ask)
    except Exception as err:  # noqa: BLE001 - as the package does: a gate that cannot be reached stays closed
        d = {"decision": "stop", "by": "as_extended", "reason": f"{type(err).__name__}: {err}"}
    with open(os.environ["AS_EXTENDED_LOG"], "a") as f:
        f.write(d["decision"] + "\\n")
    return d


_REAL = []


class _Patch(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, name, path=None, target=None):
        if name != "of_asks_package":
            return None
        spec = importlib.machinery.PathFinder.find_spec(name, path)
        if spec is None:
            return None
        self._real = spec.loader
        spec.loader = self
        return spec

    def create_module(self, spec):
        return self._real.create_module(spec)

    def exec_module(self, module):
        self._real.exec_module(module)
        _REAL[:] = [module.before_file]
        module.before_file = _before_file


sys.meta_path.insert(0, _Patch())
'''

# The tests run under a runner that writes each test's result to a file of its own, one line each as it ends: a
# result read back from unittest's stderr is lost whenever another output (a warning, a test's own process saying
# "not filed") lands between a test's name and its result (of_asks on of-asks PR 1). A test with no line there never
# ended: its module did not import, or the run was cut off.
RUNNER = '''
import sys, unittest


class Result(unittest.TextTestResult):
    def _put(self, test, status):
        with open(sys.argv[1], "a") as f:
            f.write(status + " " + test.id() + "\\n")

    def addSuccess(self, test):
        super().addSuccess(test)
        self._put(test, "ok")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._put(test, "FAIL")

    def addError(self, test, err):
        super().addError(test, err)
        self._put(test, "ERROR")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._put(test, "skipped")

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self._put(test, "expected-failure")

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self._put(test, "unexpected-success")


suite = unittest.defaultTestLoader.loadTestsFromNames(sys.argv[2:])
sys.exit(0 if unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite).wasSuccessful() else 1)
'''


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
    """The tests of "file" with HOOK installed (None: the package not installed, the baseline): (held, broke, the
    hook's decisions, the run's exit status)."""
    t = tempfile.mkdtemp(prefix="of-asks-as-extended.")
    try:
        env = dict(os.environ)
        # evaluated in the test's own process, as in a plain terminal: never through the listener's hooks door
        env.pop("CLAUDE_CODE_SESSION_ID", None)
        log = os.path.join(t, "decisions")
        if hook is not None:
            org, site = os.path.join(t, "org"), os.path.join(t, "site")
            os.makedirs(org)
            os.makedirs(site)
            bench_home = install(org, hook)
            with open(os.path.join(site, "sitecustomize.py"), "w") as f:
                f.write(SITECUSTOMIZE)
            env.update(PYTHONPATH=site + os.pathsep + os.environ.get("PYTHONPATH", ""), AS_EXTENDED_BENCH=bench_home,
                       AS_EXTENDED_ORG=org, AS_EXTENDED_LOG=log)
        results = os.path.join(t, "results")
        try:
            r = subprocess.run([sys.executable, "-c", RUNNER, results, *FILE_TESTS], cwd=OF_HOME, env=env,
                               capture_output=True, text=True, timeout=1800)
            code, out = r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired as e:  # what ended before the cut is kept; the rest has no line
            code, out = "cut off at 1800 s", f"{e.stdout or ''}{e.stderr or ''}"
            print(f"{name}: the run was cut off at 1800 s")
        lines = [ln.split(" ", 1) for ln in open(results).read().splitlines()] if os.path.exists(results) else []
        held = {i for s_, i in lines if s_ == "ok"}
        broke = {i for s_, i in lines if s_ in ("FAIL", "ERROR")}
        decisions = open(log).read().split() if os.path.exists(log) else []
        if code != 0 and not lines:
            print(f"{name}: unittest exited {code} with no result line:\n{out[-2000:]}")
        return held, broke, decisions, code
    finally:
        shutil.rmtree(t, ignore_errors=True)


def main():
    if not OF_HOME or not os.path.isfile(os.path.join(OF_HOME, "bin", "of_asks_package.py")):
        raise SystemExit("set OF_HOME to an organic-framework checkout with bin/of_asks_package.py")
    # the baseline first: a test that does not hold here fails for a reason of its own, not the hook's, and is not
    # counted
    held0, broke0, _, code0 = run("the baseline", None)
    print(f"without the package: {len(held0)} hold, {len(broke0)} do not")
    for b in sorted(broke0):
        print(f"  does not hold without it either (not counted): {b}")
    ok = bool(held0 or broke0)
    if not ok:
        print("  the baseline gave no result line: this run shows nothing")
    for name, hook in HOOKS.items():
        held, broke, decisions, code = run(name, hook)
        # a test held without the hook and not with it no longer holds, whatever its line says: a FAIL, an ERROR, a
        # skip, a line another process's output broke, or no line at all (a module that did not import, a timeout)
        lost = sorted(held0 - held)
        unseen = sorted((held0 | broke0) - (held | broke))
        stops = len(decisions) - decisions.count("pass")
        print(f"with a hook that {name}: {len(held)} hold, {len(lost)} no longer hold; the hook decided "
              f"{len(decisions)} cards ({decisions.count('pass')} pass, {stops} not)")
        for b in lost:
            print(f"  no longer holds: {b}")
        if unseen:
            print(f"  {len(unseen)} of the baseline's tests gave no result line under this hook (counted above)")
        if not (held or broke):
            print("  no result line at all under this hook: this run shows nothing")
            ok = False
        if not decisions:
            print("  the hook decided no card: the tests did not reach it, so this run shows nothing")
            ok = False
        if name == "passes every card" and lost:
            print("  a hook that passes every card broke tests: the module as extended does not keep its promises")
            ok = False
        if name == "stops a card tagged money" and not stops:
            print("  the hook stopped no card: the tests did not reach the gate, so this run shows nothing of it")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
