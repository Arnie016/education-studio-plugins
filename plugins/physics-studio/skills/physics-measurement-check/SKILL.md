---
name: physics-measurement-check
description: Check units, scales, significant figures, covariance and uncertainty in physics calculations. Use for measured quantities, numerical substitutions, experimental estimates, dimensional analysis, or suspiciously precise answers.
---

# Measurement Check

Read [the studio contract](../../references/studio-contract.md).

1. Make a compact input table: value, unit, uncertainty type, origin and date.
   Separate measured constants, exact SI definitions and invented example inputs.
2. Normalize units explicitly. Preserve conversions and ask when inputs conflict.
   Estimate order of magnitude before calculating.
3. State the physical equation and validity range. Carry units through it.
4. Propagate uncertainty using JΣJᵀ when linearization is appropriate. Keep
   covariance; explain any independence assumption. Use bounded sampling only
   when nonlinear effects justify it and state seeds and sample count.
5. Separate statistical, calibration/model and discretization uncertainty. Round
   the result to meaningful precision; check a limit or independent calculation.

Use [the pendulum lesson](../../references/worked-lessons.md) for a worked
gradient/covariance example and the bundled lab for a numerical gradient check.
Retrieve dated constants from [primary sources](../../references/source-cards.md)
when needed. Do not confuse radians with degrees, standard uncertainty with a
95% interval, or a synthetic result with a real measurement.
