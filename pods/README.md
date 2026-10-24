# Department pods

A pod is how we bring AI tooling to one TRPA department at a time: sit with the department, find the problem worth solving, build a beta, and either graduate it or kill it. This folder holds the playbook and one working folder per department.

This repo is public. Engagement notes name roles and workflows, never individual staff, and never sensitive records.

## The pod

Three roles, usually one or two people plus Claude:

- **Forward deployed engineer.** Sits with the department, watches the workflow, writes the intake, builds the prototype. Discovery is the job; the build is the easy part.
- **Implementation and project manager.** Owns the scope document, the beta schedule, and check-ins with the department lead. Keeps the engagement to one problem.
- **QA engineer.** Runs the `trpa-dashboard-qa` checklist, verifies numbers against source data, and signs off before anyone outside the pod sees the tool.

## Lifecycle

1. **Intake.** Copy `_intake-template.md` into the department folder as `intake-YYYY-MM-DD.md` and fill it during the sit-down. The data access section is mandatory: a problem whose data cannot be reached from a static page needs a different container, and finding that out after the prototype is too late.
2. **Scope.** Pick one problem and one container. An app in `qa/` is one option, not the default. Other containers: a Claude skill in `trpa-agency/trpa-claude-skills`, a data pipeline in its own repo, or a document workflow (Legal and Finance problems usually land here, not in a public repo).
3. **Build.** For an app, stamp `qa/_template/` into the matching `qa/<category>/` folder and register it in `apps.json` with `"beta": true`. For a skill, build it in the skills repo with `skill-creator`.
4. **QA.** Full `trpa-dashboard-qa` pass for apps. Numbers spot-checked against source for everything.
5. **Beta.** Four weeks with the department, start date written in the intake doc. The department uses it on real work; the pod fixes what they hit.
6. **Graduate or archive.** At the four-week mark the department either commits a named owner and the tool is promoted (beta flag dropped, moved out of `qa/` when it is promoted on the site), or it is archived: removed from `apps.json` and noted in the intake doc with the reason. No zombie betas.

## Rules

- One engagement per department at a time.
- The intake doc is the source of truth for an engagement. Decisions, dates, and the final graduate-or-archive call are recorded there.
- Public repo: no secrets, no credentials, no staff names, no case or enforcement records.
- Data access gets answered at intake, not at build. Known traps: office-network CORS on maps.trpa.org (see `.claude/memory/internal-cors-issue.md`), SDE is not reachable from GitHub Pages, LT Info tabular data comes from `internalapi.laketahoeinfo.org`.
- Betas carry the QA banner and live under `qa/` until promoted.

## Folders

```
pods/
├── README.md                      this playbook
├── _intake-template.md            copy per engagement
├── communications/
├── eip/
├── finance/
├── legal/
├── long-range-transportation/
├── permitting-compliance/
├── reporting-accountability/
└── science-data/
```

## Skills that run the pod

- `trpa-pod` (trpa-claude-skills): this playbook as a skill, so any machine can run an engagement the same way
- `trpa-dashboard-stack` plus a brand skill: the build
- `trpa-dashboard-qa`: the QA role
- `trpa-data-services`: where the data lives and how to reach it
