#!/usr/bin/env python3
"""Small educational checks, Python standard library only; no external I/O.

Quantum model: H = a I + bx sigma_x + bz sigma_z, real coefficients, hbar=1.
Time/Hamiltonian are dimensionless toy values, not detector/neutrino data.
Pendulum inputs use SI and first-order Gaussian covariance propagation.
"""

import argparse
import cmath
import itertools
import json
import math
import unittest


def evolved(a, bx, bz, t):
    """Analytic evolution of initial state (1, 0) under constant H."""
    r = math.hypot(bx, bz)
    phase = cmath.exp(-1j * a * t)
    if r == 0:
        return (phase, 0j)
    s = math.sin(r * t) / r
    return (phase * (math.cos(r * t) - 1j * bz * s),
            phase * (-1j * bx * s))


def rk4(a, bx, bz, t, steps):
    """Independent integration of dpsi/dt = -i H psi, not the formula above."""
    if not isinstance(steps, int) or steps <= 0:
        raise ValueError("steps must be a positive integer")
    h = t / steps
    y = (1 + 0j, 0j)

    def f(v):
        return (-1j * ((a + bz) * v[0] + bx * v[1]),
                -1j * (bx * v[0] + (a - bz) * v[1]))

    def shifted(v, k, scale):
        return tuple(v[i] + scale * k[i] for i in range(2))

    for _ in range(steps):
        k1 = f(y)
        k2 = f(shifted(y, k1, h / 2))
        k3 = f(shifted(y, k2, h / 2))
        k4 = f(shifted(y, k3, h))
        y = tuple(y[i] + h * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6
                  for i in range(2))
    return y


def transition(state):
    return abs(state[1]) ** 2


def pendulum_g(length, period):
    if not all(math.isfinite(x) and x > 0 for x in (length, period)):
        raise ValueError("length and period must be positive finite SI values")
    return 4 * math.pi ** 2 * length / period ** 2


def pendulum_variance(length, period, sigma_l, sigma_t, rho=0):
    if not all(math.isfinite(x) and x >= 0 for x in (sigma_l, sigma_t)):
        raise ValueError("standard uncertainties must be nonnegative and finite")
    if not math.isfinite(rho) or abs(rho) > 1:
        raise ValueError("correlation must be between -1 and 1")
    g = pendulum_g(length, period)
    jl, jt = g / length, -2 * g / period
    return jl*jl*sigma_l**2 + jt*jt*sigma_t**2 + 2*jl*jt*rho*sigma_l*sigma_t


def matrix_rank(rows, relative_tolerance=1e-12):
    """Small floating-point teaching routine, not a conditioning certificate."""
    a = [list(map(float, row)) for row in rows]
    if not a:
        return 0
    if any(len(row) != len(a[0]) for row in a):
        raise ValueError("ragged matrix")
    scale = max((abs(x) for row in a for x in row), default=0)
    tol = scale * relative_tolerance
    rank = 0
    for col in range(len(a[0])):
        if rank == len(a):
            break
        pivot = max(range(rank, len(a)), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) <= tol:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][col]
        a[rank] = [v / p for v in a[rank]]
        for row in range(rank + 1, len(a)):
            factor = a[row][col]
            a[row] = [x - factor*y for x, y in zip(a[row], a[rank])]
        rank += 1
    return rank


def ratio_design(n):
    rows = []
    for i, j in itertools.combinations(range(n), 2):
        row = [0] * n
        row[i], row[j] = 1, -1
        rows.append(row)
    return rows


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def summary():
    a, bx, bz, t = 0.7, 0.8, -0.3, 2.3
    exact = evolved(a, bx, bz, t)
    numerical = rk4(a, bx, bz, t, 400)
    base = transition(evolved(0, bx, bz, t))
    shifted = transition(exact)
    changed = transition(evolved(0, bx + 0.2, bz, t))
    return {
        "status": "TOY_NUMERICS_NOT_OBSERVATIONS",
        "quantum_inputs": {"a": a, "bx": bx, "bz": bz, "t": t,
                           "units": "dimensionless; hbar=1; initial=(1,0)"},
        "analytic_rk4_max_amplitude_error": max(abs(x-y) for x, y in zip(exact, numerical)),
        "identity_shift_probability_difference": abs(base-shifted),
        "positive_control_change_in_probability": abs(base-changed),
        "pendulum": {"inputs": {"L_m": 1.0, "T_s": 2.006,
                                 "sigma_L_m": 0.002, "sigma_T_s": 0.004,
                                 "correlation": 0},
                     "g_m_s2": pendulum_g(1.0, 2.006),
                     "standard_uncertainty_m_s2": math.sqrt(pendulum_variance(1, 2.006, .002, .004))},
        "four_flux_pair_count": len(ratio_design(4)),
        "four_flux_log_ratio_design_rank": matrix_rank(ratio_design(4)),
        "two_parameter_proportional_rank": matrix_rank([[1, 2], [2, 4]]),
        "two_parameter_contrasting_rank": matrix_rank([[1, 2], [2, 1]]),
        "prime_polynomial_counterexample": {"n": 40, "value": 1681, "factorization": "41*41"},
        "limits": "No detector fit, discovery, formal theorem, or experimental replication."
    }


class PhysicsChecks(unittest.TestCase):
    def test_zero_time(self):
        self.assertEqual(evolved(.7, .8, -.3, 0), (1+0j, 0j))

    def test_zero_hamiltonian(self):
        self.assertEqual(evolved(0, 0, 0, 3), (1+0j, 0j))

    def test_no_off_diagonal_no_transition(self):
        self.assertEqual(transition(evolved(.7, 0, -.3, 4)), 0)

    def test_closed_form_norm(self):
        for t in (0, .1, 2.3, 8):
            self.assertAlmostEqual(sum(abs(v)**2 for v in evolved(.7, .8, -.3, t)), 1, places=13)

    def test_identity_shift_invariance(self):
        for t in (.2, 1.3, 3.5):
            self.assertAlmostEqual(transition(evolved(0, .8, -.3, t)),
                                   transition(evolved(2, .8, -.3, t)), places=13)

    def test_positive_control_changes_probability(self):
        self.assertGreater(abs(transition(evolved(0, .8, -.3, 2.3)) -
                               transition(evolved(0, 1.0, -.3, 2.3))), .01)

    def test_rk4_agrees_with_closed_form(self):
        error = max(abs(x-y) for x, y in zip(evolved(.7, .8, -.3, 2.3),
                                              rk4(.7, .8, -.3, 2.3, 400)))
        self.assertLess(error, 1e-9)

    def test_rk4_norm(self):
        self.assertAlmostEqual(sum(abs(v)**2 for v in rk4(.7, .8, -.3, 2.3, 400)), 1, places=9)

    def test_rk4_convergence(self):
        exact = evolved(.7, .8, -.3, 2.3)
        errors = [max(abs(x-y) for x, y in zip(exact, rk4(.7, .8, -.3, 2.3, n)))
                  for n in (20, 40)]
        self.assertGreater(errors[0] / errors[1], 12)
        self.assertLess(errors[0] / errors[1], 20)

    def test_invalid_steps(self):
        for steps in (0, -1, 2.5):
            with self.assertRaises(ValueError):
                rk4(0, 1, 0, 1, steps)

    def test_pendulum_si_scale(self):
        self.assertTrue(9.80 < pendulum_g(1, 2.006) < 9.82)
        self.assertAlmostEqual(pendulum_g(2, 2.006), 2*pendulum_g(1, 2.006))

    def test_pendulum_invalid_inputs(self):
        for length, period in ((0, 2), (1, 0), (-1, 2), (1, math.nan)):
            with self.assertRaises(ValueError):
                pendulum_g(length, period)
        with self.assertRaises(ValueError):
            pendulum_variance(1, 2, .1, .1, 2)
        with self.assertRaises(ValueError):
            pendulum_variance(1, 2, -.1, .1)

    def test_uncertainty_finite_difference(self):
        length, period, step = 1.0, 2.006, 1e-5
        dl = (pendulum_g(length+step, period)-pendulum_g(length-step, period))/(2*step)
        dt = (pendulum_g(length, period+step)-pendulum_g(length, period-step))/(2*step)
        independent = dl**2*.002**2 + dt**2*.004**2
        self.assertAlmostEqual(independent, pendulum_variance(length, period, .002, .004), places=10)

    def test_covariance_changes_uncertainty(self):
        self.assertLess(pendulum_variance(1, 2, .002, .004, .5),
                        pendulum_variance(1, 2, .002, .004, 0))

    def test_log_ratio_rank(self):
        self.assertEqual(len(ratio_design(4)), 6)
        self.assertEqual(matrix_rank(ratio_design(4)), 3)

    def test_common_flux_scale_cancels(self):
        flux = [2, 3, 5, 7]
        for i, j in itertools.combinations(range(4), 2):
            self.assertAlmostEqual(math.log(flux[i]/flux[j]),
                                   math.log((13*flux[i])/(13*flux[j])))

    def test_proportional_and_contrasting_design(self):
        self.assertEqual(matrix_rank([[1, 2], [2, 4]]), 1)
        self.assertEqual(matrix_rank([[1, 2], [2, 1]]), 2)
        self.assertEqual(matrix_rank([[0, 0], [0, 0]]), 0)

    def test_vector_density_cancellation(self):
        mass, particles, antiparticles = 5., 3., 3.
        self.assertGreater(mass*(particles+antiparticles), 0)
        self.assertEqual(particles-antiparticles, 0)

    def test_finite_search_not_universal_proof(self):
        self.assertTrue(all(is_prime(n*n+n+41) for n in range(40)))
        self.assertFalse(is_prime(40*40+40+41))
        self.assertEqual(40*40+40+41, 41**2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(PhysicsChecks))
        print(json.dumps({"tests_run": result.testsRun, "failures": len(result.failures),
                          "errors": len(result.errors), "passed": result.wasSuccessful()}, indent=2))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    print(json.dumps(summary(), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
