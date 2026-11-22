"""of-asks's own checks: its files read in Bench's closed reader, and what they name exists in the organic-framework
checkout it runs on (OF_HOME, else the one the `of` on PATH runs from). Bench is found as OF finds it: at the folder
OF's configuration names (`of owner set bench`, else ~/.local/share/bench), never from the environment. Bench
evaluates only inside its outer layer, an operating-system sandbox that cannot start inside an agent session's own:
there these checks skip, and `bench test` outside a session, or CI, runs them."""

import os
import re
import shutil
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OF_HOME = os.environ.get("OF_HOME") or (
    os.path.dirname(os.path.dirname(os.path.realpath(shutil.which("of")))) if shutil.which("of") else "")
if OF_HOME:
    sys.path.insert(0, os.path.join(OF_HOME, "bin"))

try:
    import of_method  # noqa: E402  OF's reading of main.lua; it imports Bench from where OF's configuration says
    bench = of_method.bench
    MISSING = None if bench else of_method._MISSING
except ImportError as e:
    of_method, bench, MISSING = None, None, f"no organic-framework checkout with bin/of_method.py ({e})"

RECORD_WORDS = {"decl": ["record", "view"], "value": []}


def read(rel, words):
    return bench.evaluate(bench.lua_sources(HERE), rel, words, name=f"of-asks/{rel}")


class PackageTest(unittest.TestCase):
    def setUp(self):
        if bench is None:
            if os.environ.get("CI"):
                self.fail(MISSING)
            self.skipTest(MISSING)
        try:
            bench.evaluate({"x.lua": "return 1"}, "x.lua", bench.NO_WORDS)
        except bench.BenchError as e:
            if "outer layer" not in str(e):
                raise
            if os.environ.get("CI"):
                self.fail(f"Bench's outer layer does not start in CI: {e}")
            self.skipTest("Bench's outer layer cannot start here (an agent session's sandbox)")

    def test_the_spec_reads(self):
        spec = bench.read_spec(HERE)
        self.assertEqual(spec["name"], "of-asks")
        self.assertRegex(spec["version"], r"^1\.\d+\.\d+$")   # a later version of the same major keeps its promises
        self.assertEqual(spec["depends"], ["organic-framework ~> 1"])

    def test_the_method_offers_escalate_after_and_file(self):
        m = of_method.read_method(HERE, bench.read_spec(HERE))
        self.assertEqual(m["settings"]["escalate_after"], {"type": "duration", "default": "2h"})
        self.assertEqual(m["extendable"], ["file"])
        self.assertIn("file", m["modules"])

    def test_every_record_named_exists_in_OF(self):
        if not OF_HOME:
            self.skipTest("OF_HOME is not set")
        with open(os.path.join(OF_HOME, "docs", "events.md"), encoding="utf-8") as f:
            known = set(re.findall(r"`(of\.[a-z_]+)`", f.read()))
        records = read("records/events.lua", bench.NO_WORDS)["returned"]
        self.assertTrue(records)
        for r in records:
            self.assertIn(r["name"], known, f"{r['name']} is not in OF's docs/events.md")
        view = read("records/views/asks.lua", bench.NO_WORDS)["returned"]
        with open(os.path.join(OF_HOME, "bin", "of_listen.py"), encoding="utf-8") as f:
            listen = f.read()
        for table in (view["name"], view["groups"]):
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table} ", listen)

    def test_every_code_path_named_exists_in_OF(self):
        if not OF_HOME:
            self.skipTest("OF_HOME is not set")
        m = of_method.read_method(HERE, bench.read_spec(HERE))
        self.assertTrue(any((b.get("code") or "").startswith("bin/") for b in m["modules"].values()))
        for name, body in m["modules"].items():
            for path in re.findall(r"\bbin/[\w./-]+\w", (body.get("code") or "") + " " + (body.get("checks") or "")):
                self.assertTrue(os.path.isfile(os.path.join(OF_HOME, path)), f"module {name}: no {path} in OF")

if __name__ == "__main__":
    unittest.main()
