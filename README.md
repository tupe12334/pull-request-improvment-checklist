# pull-request-improvment-checklist

A [steplock](https://github.com/polyhook/steplock) checklist that makes an AI coding agent improve a pull request before it runs `gh pr merge` or `gh pr ready`.

The checklist follows the Kev workflow: a local decision model ([jaredpalmer/kev](https://github.com/jaredpalmer/kev)) is the merge gate, and a low score means the PR needs more work, not a handoff to the user.

The steps are defined in [`flow.mmd`](.steplock/checklists/pr-improvement/flow.mmd), and the trigger in [`config.toml`](.steplock/checklists/pr-improvement/config.toml).

## Install

For one project, copy `.steplock/checklists/pr-improvement/` into the project's `.steplock/checklists/`.

For every project, copy it into the global directory:

```sh
mkdir -p ~/.config/steplock/checklists
cp -R .steplock/checklists/pr-improvement ~/.config/steplock/checklists/
steplock validate
```

The steplock hook must be registered in the agent's settings; see the [steplock installation guide](https://github.com/polyhook/steplock/blob/main/Installation.md).
