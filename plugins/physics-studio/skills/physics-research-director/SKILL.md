---
name: physics-research-director
description: Design a bounded personal physics research campaign, schedule proposal and allowance/cash budget with visible run receipts. Use when someone wants agents to investigate a specific science question on a cadence, using only their own authorized resources.
---

# Research Director

Read [the studio contract](../../references/studio-contract.md) and
[the research-harness contract](../../references/research-harness.md).

Select one [lecture anchor](../../references/lecture-atlas.md), exact question,
observable, competing explanation and cheapest useful test. Build a small
campaign rather than a vague “discover physics” objective. Keep current research
facts primary-source-bound; imported agent reports start unverified.

Use `examples/research-plan.json` as a disabled, local-first template, not a live
schedule. Let each owner select their own allowance floor and limits. Validate
with `scripts/research_harness.py --plan PATH`, resolving scripts from the plugin
root. Without fresh usage, the planner should block. It cannot enforce spending,
run agents, reserve funds, isolate tenants or install a background scheduler.

If scheduling is explicitly requested, discover the host's native automation
tool and inspect duplicates. Bind owner, objective, targets, credentials,
cadence/timezone, expiry, finite runs, no-overlap and cancellation. Use scoped
approvals; an MD file or available account never grants spending authority.
Do not activate a paid schedule without the required execution/funding gates.

Expose state, latest verified result, actual usage/spend or its absence, blocker
and next checkpoint. Preserve failures, stop at limits, and keep scheduling,
execution, scientific verification and publication as separate evidence gates.
