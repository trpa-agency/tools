# Department pods

The pod model brings AI tooling to one TRPA department at a time: forward deployed engineer, implementation and project manager, and QA engineer (one or two people plus Claude).

- `pods/README.md` is the playbook and the source of truth; the `trpa-pod` skill in `trpa-agency/trpa-claude-skills` mirrors it and must be updated when the playbook changes.
- One folder per department under `pods/`: communications, eip, finance, legal, long-range-transportation, permitting-compliance, reporting-accountability, science-data. Science and Data staffs the pod.
- An engagement starts by copying `pods/_intake-template.md` into the department folder as `intake-YYYY-MM-DD.md`. Data access gets answered at intake (SDE unreachable from the browser, office-network CORS, internalapi for LT Info).
- Beta apps stamp from `qa/_template/` (index.html plus README) into `qa/<category>/` and register in `apps.json` with beta true. Not every engagement produces an app: skills, pipelines, and document workflows are equal containers, and Legal and Finance work stays out of this public repo.
- Four-week beta, then graduate (named department owner, beta flag dropped) or archive (removed from apps.json, reason in the intake doc). No zombie betas.
- Public repo: engagement notes are role-level, never staff names or sensitive records.
