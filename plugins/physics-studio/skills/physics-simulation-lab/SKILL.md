---
name: physics-simulation-lab
description: Build or review a small reproducible local physics simulation with invariants, independent comparisons and convergence tests. Use for exploring equations, testing a toy model, checking numerical stability or teaching through computation.
---

# Simulation Lab

Read [the studio contract](../../references/studio-contract.md) and fill only
the relevant fields of [one experiment card](../../references/experiment-card.md).

Freeze one question, equation, observable, units, initial/boundary conditions,
parameter range and local resource limit before running. Prefer a tiny CPU test
and standard libraries; no paid compute or dependency installs by default.

Choose a comparator that can fail independently: analytic solution versus
integration, different discretization, or a known limiting case. Reusing the
producer's result is not an independent verifier. Include a positive control
that changes the observable, an invariant and a step-size/convergence check.

For bundled examples, locate `scripts/physics_checks.py` relative to the plugin
root (two directories above this skill). Run with `--self-test` for checks or
without arguments for the toy result summary. Read it first; it makes no network
calls. If execution is unavailable, label `NOT_RUN` and provide the exact setup.

Report actual inputs, method, error diagnostic, output and claim boundary.
Never call a two-state toy a detector simulation, or numerical stability a proof
that a proposed physical model describes nature.
