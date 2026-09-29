# pull-request-improvment-checklist

A [steplock](https://github.com/polyhook/steplock) checklist that makes an AI coding agent improve a pull request before it runs `gh pr merge` or `gh pr ready`.

The checklist follows the Kev workflow: a local decision model ([jaredpalmer/kev](https://github.com/jaredpalmer/kev)) is the merge gate, and a low score means the PR needs more work, not a handoff to the user.

## Steps

1. **Fresh state**: re-read the PR and fetch the base branch.
2. **Scope**: ask Kev keep / split / grow; move unrelated changes to their own PR.
3. **Design choices**: put each non-obvious decision to Kev as its own `choice`.
4. **Verified**: run the tests, the local CI gates, and a dev-environment deploy where required.
5. **Honest state**: build the Kev state from verified facts only, with neutral criteria.
6. **Threshold**: probe concerns and fix until the merge `noul` reaches 0.8 (own PR) or 0.95 (colleague PR with fix PR applied).
   - Reached: **checks green**. Get every check green; merge without admin bypass.
   - Stalled: stop the merge, record the open question with scores, do other tasks Kev approves.
7. **Reported**: report every round's scores in the PR body or summary.

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
