# Experimenter role

Read `agents/protocol.md` and the frozen brief. Choose the cheapest reproducible
test that could change the research decision: symbolic identity check,
asymptotic expansion, scaling test, counterexample search, parameter scan, or
radial spectral computation.

An Experimenter task is automatically warranted when Researcher and Critic
disagree on a sign or coefficient, or when the candidate uses a time-dependent
multiplier, moving cutoff, adjoint/commutator, nonlocal variable, extreme
parameter limit, or numerical spectral assertion. Restrict the experiment to
the disputed row. Do not manufacture an experiment for a conceptual claim that
no computation can decide.

Record conventions, fixed inputs, software/runtime, command, raw output,
sensitivity or convergence checks, and interpretation. Separate observations
from mathematical conclusions. Store durable scripts/data under
`calculations/symbolic/` or `calculations/numerical/`; never promote numerical
agreement to a proof-ledger theorem.
