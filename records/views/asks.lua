-- The view of-asks reads: the open questions, kept by the listener. Its version is the processor's own and is
-- raised there; raising it rebuilds the view by replaying the log.
return {
  name     = "view_asks",
  groups   = "view_ask_groups",
  built_by = "bin/of_listen.py: AsksProcessor",
  fold     = "bin/of_asks.py: project",
}
