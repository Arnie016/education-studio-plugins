# Direct one research effort, visibly and within your limits

This is a campaign/schedule design contract plus a tested read-only preflight
planner. It is not a background worker, billing firewall or live provider adapter.

## Each participant owns their own authority

One owner, campaign and workspace per plan. The owner selects their account,
model, allowance floor, optional cash ceiling and approved data. Never reuse
another user's credentials, allowances or approvals. Store only secret handles,
not secret values, in a local plan; use the host's authenticated connector or
secret store. Changing the owner, objective, target or budget invalidates a lease.
Do not imply pooled credits, purchased tokens, guaranteed savings or scientific returns.

## One cycle

1. **Choose:** one exact question, lecture anchor, hypothesis, observable,
   alternative and failure condition. Retrieve only the needed context.
2. **Preflight:** check fresh allowance, provider access, time/token/cash limits,
   outstanding reservations, running jobs and scoped authority. Unknown or stale
   usage blocks metered work; tokens and dollars are separate budgets.
3. **Reserve:** the real executor must atomically reserve the worst-case spend
   including retries, tool calls, child jobs and storage. The Python planner
   cannot enforce provider charges or prevent multi-process races.
4. **Run:** one cheap algebra/control test before scans. A worker proposes;
   a different calculation or fixed evaluator checks. Agents cannot expand their
   own tools, network, credentials, budget or success criteria.
5. **Checkpoint:** retain source/version, code/input hashes, actual tool actions,
   elapsed time, observed usage/spend (or unavailable), result and evidence class.
6. **Review:** continue, revise, stop or request a human decision. Stop at the
   allowance floor, any cost cap, unexpected access, repeated non-improvement,
   solver failure or exhausted finite run count. Negative results are valid.

Use `DRAFT`, `PREFLIGHT_BLOCKED`, `READY_FOR_HOST_REVIEW`, `SCHEDULED`, `RUNNING`,
`CHECKPOINTED`, `COMPLETED_IN_SCOPE` and `STOPPED`. These are distinct states.
A scheduled task is not a completed run. A successful preflight is not authority
or proof that a run happened. Display one current state and its next action.

## Scheduling workflow

Start with a finite weekly plan of four short runs and one concurrent worker.
Change cadence only when the question benefits. Use an explicit IANA timezone,
next run, expiry, maximum run count, no-overlap lock, missed-run policy and
cancel/pause action. Retries consume the same finite limits; never replay a
financial action without an idempotency key and fresh status check.

When a user actually asks to activate a schedule, discover the host's native
automation tool, inspect matching existing schedules, present the bounded plan
and use that tool under its approval rules. For Codex, use the provided
automation mechanism, not raw cron or a hidden process. For another host, use
its supported scheduler and permissions. If no scheduler/usage meter/executor
exists, leave `DRAFT` and give a missing-capability report; do not pretend an
MD file can wake a laptop or run a remote agent.

The example plan is disabled. The build created no new schedules, agents or
fund transfers. Existing research schedules were context only and unchanged.

## Funding and execution boundaries

The default is local CPU and zero external spend. Paid work needs an exact
provider/model, verified current pricing, worst-case quote, per-run and campaign
caps, an expiring scoped approval, provider-side hard limits where supported,
monitoring and cancellation. A valid API key is not spending permission.
If the service cannot give a defensible upper bound or stop mechanism, do not
promise a hard ceiling; remain local or ask for a smaller bounded action.

For scaling beyond one worker, first implement owner isolation, transactions,
idempotency, secrets scoping and cancellation in the executor. Do not merely
increase the parallelism number. The v0.2 planner deliberately accepts only
one concurrent run and executes nothing.

## Observable receipt

Record campaign and run ID; question; source/code/input hashes; scoped approval
reference and expiry; queue/start/end state; per-tool actions and denials;
budget reserved/actual/unavailable; equation and controls; verifier class;
negative result; claim boundary; blocker and next decision. Keep operational
details local. A public lesson should not include raw chats, private data or
credentials. No automated publication, expert outreach or account changes.

## First example campaign

“Which information is lost in two-flavour oscillation measurements?” Use
lecture chapters 1, 5 and 9, then the common-phase lesson and local controls.
The first useful result is a checked limitation and a next discriminating
measurement, not an asserted dark-matter discovery.
