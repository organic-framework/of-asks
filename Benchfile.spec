-- of-asks: how an agent asks its owner a question, and how the owner sees and answers it.
-- A package over the code organic-framework has today (bin/of, bin/of_asks*.py, bin/of_judge.py, bin/of_pulse.py):
-- installing it changes no behaviour; it names what that code does, offers one setting and one module to extend.
package {
  name    = "of-asks",
  version = "1.0.0",
  summary = "How an agent asks the owner a question, and how the owner sees and answers it",
  license = "Apache-2.0",
  source  = "https://github.com/organic-framework/of-asks",
  main    = "main.lua",
  tests   = { "sh", "tests/run.sh" },
}

depends { "organic-framework ~> 1" }

needs {                       -- what the package's code needs at work; shown at install, not enforced in this version
  store = { records = { read = "of.agent_question*, of.ask_*, of.permission_*", write = "of.agent_question*, of.ask_*" } },
  model = { "small" },        -- the judge (bin/of_judge.py) and the detectors' second stage
}
