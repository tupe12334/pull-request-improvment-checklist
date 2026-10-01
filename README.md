# pull-request-improvment-checklist

A [steplock](https://github.com/polyhook/steplock) checklist that makes an AI coding agent improve a pull request before it runs `gh pr merge`. `gh pr ready` is not gated, because it merges nothing. The trigger ignores the merge command when it appears inside quoted text, such as a PR body passed with `--body`. If the quotes in a command do not balance, it gates any mention of the merge command, so it never lets a real merge through.

The checklist follows the Kev workflow: a local decision model ([jaredpalmer/kev](https://github.com/jaredpalmer/kev)) is the merge gate, and a low score means the PR needs more work, not a handoff to the user.

The one exception is a PR that changes only a configuration repository, such as a skill library or an agent config repo. If its score stalls after every true fact was tried, the checklist lets it skip the gate and merge, with the Kev scores recorded. The same kind of PR may also merge over a check that fails the same way on the base branch or never started, once the agent has run that check locally and recorded the result. A code change never skips the gate and always needs every check green.

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
