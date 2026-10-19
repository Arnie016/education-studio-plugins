# Physics Studio

By Arnav Salkade · 0.2.0 · private working edition

Bring a question, a page of working, a graph or a paper. Start with what you
already understand; the studio helps you make the next step visible.

| Your task | Skill |
| --- | --- |
| Understand an idea or build a short study session | `physics-tutor` |
| Find the first mistake in a derivation | `physics-derivation-check` |
| Calculate with units and realistic uncertainty | `physics-measurement-check` |
| Explore an equation with a small reproducible simulation | `physics-simulation-lab` |
| Understand particles, neutrinos or a dark-sector proposal | `physics-particle-lab` |
| Analyse a paper or check what a claimed proof establishes | `physics-paper-lab` |
| Plan a personal research effort, budget, cadence and run evidence | `physics-research-director` |

Skills are independently usable. Select one main skill, and add another only
when its distinct check matters. A lesson should not become six reports.

Try: “Explain why neutrino oscillations cannot determine the common mass-squared
offset. Give me the intuition, a derivation, and a tiny calculation I can rerun.”

## Included, and not implied

- Seven teaching/review/research workflows, shared evidence rules, five worked lessons,
  an experiment template, a review checklist, and a standard-library Python lab.
- The lab runs with `python3 scripts/physics_checks.py`; append `--self-test`
  for checks. Resolve this path from the plugin's actual installed directory.
- No network calls, API keys, telemetry, shell subprocesses or automatic uploads
  in the bundled lab. No dependency installation is needed.
- The host must provide code execution to run Python. Otherwise explain the
  reproducible steps and label the calculation `NOT_RUN`.
- This package does not include a custom graphical interface, a full lecture
  transcript, private chats, other researchers' datasets, or a paper archive.
- No educational or scientific endorsement by the linked creators or agencies.
  New numerical checks demonstrate the named toy models, not nature or novelty.

Sources and what was actually inspected: [source cards](references/source-cards.md).
Video-led learning: [twelve-part lecture atlas](references/lecture-atlas.md).
Worked teaching material: [lessons](references/worked-lessons.md).
Boundaries and review: [studio contract](references/studio-contract.md).

## Direct your own research allowance

Use `physics-research-director` to turn one question into a bounded campaign.
Choose a cadence, per-run time/token limits, a remaining-allowance floor and a
separate cash ceiling. The included planner checks a campaign and usage snapshot:

`python3 scripts/research_harness.py --plan examples/research-plan.json`

Without a fresh usage snapshot it correctly blocks a run. `--self-test` runs
synthetic control cases. The planner only prints decisions; it starts no agent,
schedule or payment. A real host must enforce approvals, isolation, locks,
reservations, cancellation and provider billing limits. It must read your actual
allowance rather than guess a percentage from token estimates.

Each user brings their own accounts and funds. This is not a shared credit pool,
fundraising platform or automatic scientific-discovery service. Live scheduling,
meter integration, paid execution and multi-user isolation remain unimplemented
in this portable package. The director provides the contracts and native-host
setup workflow; no recurring job has been created by this build.

## Related education resources

When asked for learning resources or the wider education platform, consult [the reference directory](references/education-platform-links.md). Separate official IB requirements, independent teaching perspectives and proposed infrastructure. Do not turn ordinary tutoring into promotion or payment solicitation.

