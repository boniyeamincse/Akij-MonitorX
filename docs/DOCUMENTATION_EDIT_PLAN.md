Documentation Edit Plan — Akij MonitorX
======================================

Goal
----
Create a clear, accurate, and maintainable documentation set for Akij MonitorX that helps developers, operators, and testers run, extend, and deploy the system.

Scope
-----
- All markdown files under `docs/`
- `README.md` (links and quickstarts)
- `docs/test.md`, `docs/UNDERSTANDING.md`, `docs/agentinstallationguide.md`, `docs/docker-troubleshooting-cheatsheet.md`, `docs/architecture.md`, `docs/userguide.md`

Phased Plan
-----------
1. Audit (1 day)
   - Read all existing docs and the README.
   - Create a gap list of missing topics, outdated commands (systemctl vs Windows), and inconsistencies.
   - Deliverable: `docs/AUDIT_REPORT.md` with prioritized items.

2. Edit (2-4 days)
   - Apply edits in small PRs (one doc per PR) covering:
     - Quick start accuracy (Linux/Windows)
     - Smoke test commands and scripts (scripts/test.sh, smoke-test.sh, smoke-test.ps1)
     - Agent installation guide (document agent-install.sh, agent-install.ps1, setup.sh)
     - Docker Compose deployment notes and compose file correctness
     - Reference environment variables and `.env.example` (create if missing)
   - Deliverable: updated markdown files in `docs/` and `README.md`.

3. Review (1-2 days)
   - Peer review or self-review of PRs.
   - Verify commands in a test environment (Docker Compose on Ubuntu), update steps with timing notes.
   - Deliverable: review comments resolved and PRs merged.

4. QA & Verify (1 day)
   - Run smoke tests (`npm run full-test`) on an Ubuntu instance.
   - Confirm agent installers operate as expected on Ubuntu and Windows (or document known limitations).
   - Deliverable: `docs/QA_REPORT.md` with test run outputs and fixes made.

5. Publish & Maintenance
   - Merge all docs to `main` and tag a release or update README with links.
   - Optionally publish docs to GitHub Pages.
   - Add a `CONTRIBUTING.md` and `MAINTAINERS.md` for documentation ownership.

Work breakdown (example PRs)
---------------------------
- PR 1: `docs/test.md` — standardize and add bash steps, include `scripts/test.sh` usage.
- PR 2: `docs/agentinstallationguide.md` — add installer scripts details and systemd user account guidance.
- PR 3: `docs/docker-troubleshooting-cheatsheet.md` — add Windows and WSL notes and common docker-compose commands.
- PR 4: `README.md` — ensure top-level links and quickstarts are accurate.
- PR 5: Add `.env.example` and `docs/ENV_VARS.md` listing expected env vars for Node and AI Engine.
- PR 6: `docs/UNDERSTANDING.md` — refine architecture and developer notes.

Acceptance criteria
-------------------
- All playbook steps are executable on a clean Ubuntu 22.04 LTS VM with Docker and Node installed.
- Commands in docs produce expected outputs or document deviations.
- README links to primary docs and smoke-test scripts are accurate.
- CI (optional) runs the `scripts/test.sh` during PR validation.

Risks and mitigations
---------------------
- Heavy Python dependencies: recommend using Docker for AI Engine to avoid local install issues.
- Windows variability: provide PowerShell steps but test only on Windows Server/Win10/11 where possible.

Next actions (I will execute if you confirm)
-------------------------------------------
1. Run the Audit step and produce `docs/AUDIT_REPORT.md`.
2. Implement the highest-priority doc edits (PRs grouped by file).
3. Run QA using `scripts/test.sh` on a Ubuntu VM and collect results.

Please confirm and I will start the Audit and produce the audit report as the first deliverable.
