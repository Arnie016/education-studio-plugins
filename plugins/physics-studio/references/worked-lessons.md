# Five lessons: a question, a derivation, a check

All examples are original simplified teaching material. Follow the studio
contract and read the source cards before making attribution claims.

## 1. Can a longer calculation recover an invisible mass offset?

In a closed, coherent, ultrarelativistic vacuum propagation model with fixed
energy E, use natural units and a unitary mixing matrix U:

H = U diag(m1², m2²) U† / (2E).

Shift both mass squares by C. Since UU† = I, H' = H + C I/(2E).
The identity commutes with H, so exp(-iH't) = exp(-iCt/(2E))exp(-iHt).
Every flavour-transition amplitude gets the same phase; taking its squared
magnitude removes that phase. Oscillations in this model cannot determine C.

This is not “neutrinos have no mass” or “absolute mass is unknowable”. It says
this observable is insensitive to one parameter. Other measurements can carry
different information. Approximation, production and detection assumptions matter.

Check: the script compares a two-state Hamiltonian H = aI + bxσx + bzσz
with and without a; it also changes bx to ensure probabilities can change.
Its time and Hamiltonian are dimensionless toy quantities with ħ = 1.
Learner: identify which parameter is removed, and name a different measurement
you would need rather than demanding a larger language model.

## 2. Why do astronauts float if gravity still acts?

For a test body in an ideal circular orbit around a spherical mass M,
the inward gravitational force supplies centripetal acceleration:
GMm/r² = mv²/r → v² = GM/r → T = 2π√(r³/(GM)).

The spacecraft and passenger fall together, reducing the supporting contact
force the passenger feels. The gravity term did not disappear. Distinguish
altitude from radius r, and do not replace orbital speed with an escape speed.
This model neglects drag, nonspherical gravity, third bodies and thrust.

Learner: if radius doubles, what happens to orbital period? Answer: multiply
by 2^(3/2), not 2. For actual Earth calculations fetch a dated gravitational
parameter; no precise current Earth constant is bundled here.

## 3. A pendulum is a measurement, not just a formula

For a small-angle, ideal simple pendulum, T = 2π√(L/g), hence g = 4π²L/T².
Units: L in metres and T in seconds give g in m/s². Synthetic data:
L = 1.000 m, T = 2.006 s, σL = 0.002 m, σT = 0.004 s.

First-order propagation uses J = (g/L, -2g/T):
Var(g) ≈ J Σ Jᵀ = (g/L)²σL² + (2g/T)²σT²
                         - 4g² Cov(L,T)/(LT).

For independent inputs Cov = 0. A covariance-free formula is not valid merely
because measurements have separate names. Timing 20 swings requires converting
the total time to a period and propagating its uncertainty consistently.
Finite amplitude, pivot friction, length definition and clock calibration are
model/systematic effects, not automatically included in this random-error budget.

The script independently finite-differences the gradient and compares variance.
Learner: convert 200.6 centiseconds to seconds before substituting.

## 4. Six ratios do not create six independent measurements

Let four positive fluxes have logs z1,...,z4. Pairwise log ratios are zi-zj.
Six pairwise differences exist, but their design matrix has rank three:
(z1-z2)+(z2-z3)=z1-z3, and any common shift of all zi cancels.
Original flux errors become correlated in ratio space. Do not multiply six
independent likelihoods without modelling the shared measurements.

A related linear toy response is yi = εbi + ηdi. Two response rows separate
ε and η only if b1d2-b2d1 is nonzero. For actual probabilities P(x), their
derivatives also matter: a full-rank design need not yield sensitivity at an
oscillation node. Local rank does not establish global uniqueness or precision.

For one nonrelativistic vector-current dark-sector model,
ρ = m(n + nbar), whereas a mean-field vector potential may scale with n-nbar.
An equal particle/antiparticle population can gravitate while this particular
potential vanishes. Do not generalize that cancellation to every dark-matter
interaction. No detection or viable new particle is established by this toy.

Learner: propose a second response with a different b/d ratio, and explain
which nuisance parameters could still mimic your effect.

## 5. “It passed every example” is not an unrestricted proof

The polynomial f(n)=n²+n+41 is prime for n=0,...,39, but f(40)=1681=41².
The script checks both the finite successes and the first stated counterexample.
Increasing the finite search gives evidence about that finite set, not the
universal quantifier. A continuous relaxation similarly needs an explicit
transfer theorem before it establishes a result for discrete objects.

For a claimed solved problem, write: exact statement; quantifiers; domain;
assumptions; proof artifact; independent checks; missing implication. Separate
“restricted-family theorem”, “finite certificate”, “conjecture” and “full proof”.
Learner: explain why a solver returning no counterexample is not a proof unless
its completeness and the exact bounded domain have also been established.
