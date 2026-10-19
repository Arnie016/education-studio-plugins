---
name: physics-derivation-check
description: Audit a physics or mathematical-physics derivation line by line, locate the first invalid implication, and repair it with explicit conventions and checks. Use for homework reasoning, symbolic work, equations in papers, or claimed proofs.
---

# Derivation Check

Read [the studio contract](../../references/studio-contract.md).

1. Restate the target result, domain, variables, units, sign/frame conventions,
   boundary conditions and approximations. Preserve the user's original steps.
2. Inspect each implication: equality versus approximation, differentiation,
   integration constants, division by possibly zero expressions, conjugation,
   normalization, basis changes and dimensional consistency.
3. Show the first decisive invalid or unjustified step. If all inspected steps
   hold, state the bounded scope; do not pretend this proves every premise.
4. Repair the chain with enough intermediate algebra to reproduce it. Check a
   limit, dimensional identity, symmetry, independent derivation or counterexample.
5. Report the physical interpretation and the assumption most likely to fail.

For claimed solved problems, separate the exact quantifiers from a finite
search or a continuous relaxation. See lesson 5 in
[worked lessons](../../references/worked-lessons.md).
Computer algebra is a tool, not a proof certificate unless the proof is actually
provided and checked. Do not invent tool execution or formal-verifier success.
