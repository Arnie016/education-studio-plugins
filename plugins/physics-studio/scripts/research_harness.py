#!/usr/bin/env python3
"""Read-only campaign preflight. Never executes an agent, payment or schedule."""
import argparse
import copy
from datetime import datetime, timezone
from decimal import Decimal
import json
import math
from pathlib import Path
import unittest
from zoneinfo import ZoneInfo


def money(value):
    amount = Decimal(str(value))
    if not amount.is_finite() or amount < 0:
        raise ValueError("cash values must be finite, nonnegative USD")
    return amount


def integer(value):
    if type(value) is not int or value < 1:
        raise ValueError("run and resource caps must be positive integers")
    return value


def assess(plan, usage=None, now=None):
    now = now or datetime.now(timezone.utc)
    reasons = []
    try:
        if plan["schema_version"] != 1 or not plan["owner_alias"] or not plan["objective"]:
            raise ValueError("missing owner, objective or unsupported schema")
        if plan["execution"]["mode"] != "PLAN_ONLY":
            raise ValueError("this package implements PLAN_ONLY, not a live executor")
        schedule, limits = plan["schedule"], plan["limits"]
        if type(schedule["enabled"]) is not bool:
            raise ValueError("schedule enabled must be boolean")
        if schedule["cadence"] not in ("daily", "weekly", "manual"):
            raise ValueError("unsupported cadence")
        ZoneInfo(schedule["timezone"])
        max_runs = integer(schedule["max_runs"])
        integer(limits["max_wall_seconds_per_run"])
        integer(limits["max_tokens_per_run"])
        attempts = integer(limits["max_attempts_per_run"])
        if integer(limits["max_parallel_runs"]) != 1:
            raise ValueError("parallel execution needs a transactional isolated executor")
        floor = float(limits["remaining_allowance_floor_pct"])
        if not math.isfinite(floor) or not 0 <= floor <= 100:
            raise ValueError("invalid remaining allowance floor")
        run_cap = money(limits["max_external_usd_per_run"])
        total_cap = money(limits["max_external_usd_total"])
        if run_cap > total_cap:
            raise ValueError("per-run cap exceeds total cap")
        if type(plan["funding"]["paid_execution_approved"]) is not bool:
            raise ValueError("approval must be a boolean; still not an execution lease")
    except (KeyError, ValueError, TypeError, ArithmeticError) as exc:
        return {"plan_valid": False, "decision": "INVALID_PLAN", "reason": str(exc),
                "executed": False, "external_spend_usd": "0.00"}

    if not usage:
        reasons.append("FRESH_USAGE_SNAPSHOT_MISSING")
    else:
        try:
            if usage["owner_alias"] != plan["owner_alias"] or usage["campaign_id"] != plan["campaign_id"]:
                raise ValueError("usage snapshot owner/campaign mismatch")
            observed = datetime.fromisoformat(usage["observed_at"].replace("Z", "+00:00"))
            if observed.tzinfo is None:
                raise ValueError("usage timestamp needs timezone")
            age = (now - observed).total_seconds()
            if not -30 <= age <= 300:
                reasons.append("USAGE_STALE_OR_FUTURE")
            remaining = float(usage["allowance_remaining_pct"])
            if not math.isfinite(remaining) or not 0 <= remaining <= 100:
                raise ValueError("allowance unavailable or invalid")
            if remaining <= floor:
                reasons.append("ALLOWANCE_FLOOR_REACHED")
            for field in ("completed_runs", "active_runs"):
                if type(usage[field]) is not int or usage[field] < 0:
                    raise ValueError("run counts unavailable or invalid")
            if usage["completed_runs"] >= max_runs:
                reasons.append("FINITE_RUN_LIMIT_REACHED")
            if usage["active_runs"]:
                reasons.append("ANOTHER_RUN_ACTIVE")
            quote = money(usage["worst_case_usd_per_attempt"])
            worst_run = quote * attempts
            committed = money(usage["spent_usd"]) + money(usage["reserved_usd"])
            if worst_run > run_cap or committed + worst_run > total_cap:
                reasons.append("CASH_CAP_WOULD_BE_EXCEEDED")
            if quote and not plan["funding"]["paid_execution_approved"]:
                reasons.append("PAID_EXECUTION_NOT_APPROVED")
        except (KeyError, ValueError, TypeError, ArithmeticError) as exc:
            reasons.append("INVALID_USAGE_SNAPSHOT: " + str(exc))
    return {"plan_valid": True,
            "decision": "PREFLIGHT_BLOCKED" if reasons else "READY_FOR_HOST_REVIEW",
            "reasons": reasons, "campaign_id": plan["campaign_id"],
            "schedule_state": "DRAFT_NOT_ACTIVATED", "executed": False,
            "external_spend_usd": "0.00",
            "boundary": "Advisory checks only. No lease, reservation, agent, schedule or billing enforcement."}


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((Path(__file__).resolve().parents[1] / "examples/research-plan.json").read_text())
        self.now = datetime(2026, 10, 19, 12, 0, tzinfo=timezone.utc)
        self.usage = {"owner_alias": self.plan["owner_alias"], "campaign_id": self.plan["campaign_id"],
                      "observed_at": self.now.isoformat(), "allowance_remaining_pct": 24,
                      "completed_runs": 0, "active_runs": 0, "spent_usd": "0",
                      "reserved_usd": "0", "worst_case_usd_per_attempt": "0"}

    def result(self):
        return assess(self.plan, self.usage, self.now)

    def test_local_preview_never_executes(self):
        result = self.result()
        self.assertEqual(result["decision"], "READY_FOR_HOST_REVIEW")
        self.assertFalse(result["executed"])
        self.assertEqual(result["schedule_state"], "DRAFT_NOT_ACTIVATED")

    def test_missing_usage_blocks(self):
        self.assertEqual(assess(self.plan)["decision"], "PREFLIGHT_BLOCKED")

    def test_floor_blocks_at_equality(self):
        self.usage["allowance_remaining_pct"] = 21
        self.assertIn("ALLOWANCE_FLOOR_REACHED", self.result()["reasons"])

    def test_stale_snapshot(self):
        self.usage["observed_at"] = "2026-10-19T11:00:00+00:00"
        self.assertIn("USAGE_STALE_OR_FUTURE", self.result()["reasons"])

    def test_wrong_owner(self):
        self.usage["owner_alias"] = "someone-else"
        self.assertEqual(self.result()["decision"], "PREFLIGHT_BLOCKED")

    def test_unknown_usage(self):
        self.usage["allowance_remaining_pct"] = None
        self.assertEqual(self.result()["decision"], "PREFLIGHT_BLOCKED")

    def test_retry_cash_and_pending_reservations(self):
        self.plan["limits"].update(max_external_usd_per_run="1.00", max_external_usd_total="2.00", max_attempts_per_run=2)
        self.plan["funding"]["paid_execution_approved"] = True
        self.usage.update(worst_case_usd_per_attempt="0.40", spent_usd="1.00", reserved_usd="0.30")
        self.assertIn("CASH_CAP_WOULD_BE_EXCEEDED", self.result()["reasons"])

    def test_paid_approval_not_implicit(self):
        self.plan["limits"].update(max_external_usd_per_run="1.00", max_external_usd_total="2.00")
        self.usage["worst_case_usd_per_attempt"] = "0.50"
        self.assertIn("PAID_EXECUTION_NOT_APPROVED", self.result()["reasons"])

    def test_finite_runs_and_no_overlap(self):
        self.usage.update(completed_runs=4, active_runs=1)
        self.assertIn("FINITE_RUN_LIMIT_REACHED", self.result()["reasons"])
        self.assertIn("ANOTHER_RUN_ACTIVE", self.result()["reasons"])

    def test_no_parallel_or_live_executor_claim(self):
        for target, key, value in (("limits", "max_parallel_runs", 2), ("execution", "mode", "LIVE")):
            plan = copy.deepcopy(self.plan)
            plan[target][key] = value
            self.assertEqual(assess(plan, self.usage, self.now)["decision"], "INVALID_PLAN")

    def test_nonfinite_cash_denied(self):
        self.plan["limits"]["max_external_usd_total"] = "NaN"
        self.assertEqual(self.result()["decision"], "INVALID_PLAN")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--usage", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(HarnessTests))
        print(json.dumps({"tests_run": result.testsRun, "passed": result.wasSuccessful()}))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if not args.plan:
        parser.error("--plan is required unless --self-test is used")
    plan = json.loads(args.plan.read_text())
    usage = json.loads(args.usage.read_text()) if args.usage else None
    print(json.dumps(assess(plan, usage), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
