# pull-request-improvment-checklist

A [steplock](https://github.com/polyhook/steplock) checklist that makes an AI coding agent improve a pull request before it runs `gh pr merge` or `gh pr ready`.

The checklist follows the Kev workflow: a local decision model ([jaredpalmer/kev](https://github.com/jaredpalmer/kev)) is the merge gate, and a low score means the PR needs more work, not a handoff to the user.

## Steps

1. **Fresh state**: re-read the PR and fetch the base branch.
2. **Probe Kev**: send one request to `localhost:8009/v1/systemone` with a 90 second timeout.
   - Kev answers: continue at step 3.
   - Kev does not answer: run the **Kev unavailable** subflow.
3. **Scope**: ask Kev keep / split / grow, then move unrelated changes to their own PR.
4. **Design choices**: put each non-obvious decision to Kev as its own `choice` and take the top option. On a near-tie, add verified facts and re-ask. Do not hand the choice to the user.
5. **Verified**: run the tests, the local CI gates, and a dev-environment deploy where required.
6. **Honest state**: build the Kev state from verified facts only, with neutral criteria.
7. **Threshold**: probe concerns and fix until the merge `noul` reaches 0.8 (own PR) or 0.95 (colleague PR with fix PR applied).
   - Stalled: do not ask the user. Create new true facts: fix the top concern, run more local checks or dry runs, split out unrelated changes, or verify an unverified item. Then re-ask. Only when nothing is left to try, record the open question on the PR with the scores and do other in-scope tasks. A stalled score never unlocks the merge.
8. **Checks green**: get every check green and merge without admin bypass.
9. **Reported**: report every round's scores in the PR body or summary.

### Kev unavailable subflow

1. **Restart Kev** (installed but not answering): `launchctl kickstart -k gui/$(id -u)/io.kev.server`, read `~/Library/Logs/kev.log`, and probe again. If Kev answers, return to step 3.
2. **Kev missing** (no `io.kev.server` launchd agent, no checkout): ask the user whether to install Kev and wait for the answer.
   - **Install Kev** (user approved): clone [jaredpalmer/kev](https://github.com/jaredpalmer/kev), start its server on port 8009, register it as the `io.kev.server` launchd agent, and probe until it answers. Then return to step 3.
   - User declined, or the install failed: go to Use Jev.
3. **Use Jev**: send the same requests to hosted Jev (`https://openrouter.ai/api/alpha/decisions`, model `~typesafe/jev-latest`). If Jev answers, return to step 3 with Jev in place of Kev.
4. **User gate**: when no model answers, verify end to end, ask the user for the go/no-go, and continue to step 8 only on an explicit yes.

The flow lives in [`flow.mmd`](.steplock/checklists/pr-improvement/flow.mmd); the trigger in [`config.toml`](.steplock/checklists/pr-improvement/config.toml).

## Install

For one project, copy `.steplock/checklists/pr-improvement/` into the project's `.steplock/checklists/`.

For every project, copy it into the global directory:

```sh
mkdir -p ~/.config/steplock/checklists
cp -R .steplock/checklists/pr-improvement ~/.config/steplock/checklists/
steplock validate
```

The steplock hook must be registered in the agent's settings; see the [steplock installation guide](https://github.com/polyhook/steplock/blob/main/Installation.md).
