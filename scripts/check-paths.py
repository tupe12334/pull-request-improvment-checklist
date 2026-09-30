import json, os, shutil, subprocess, sys, tempfile

# Walk ack.sh paths through the pr-improvement flow and check that each one
# ends where expected. Usage: check-paths.py [steplock-binary]
steplock = sys.argv[1] if len(sys.argv) > 1 else "steplock"
steplock = os.path.abspath(steplock) if os.sep in steplock else steplock
checklist = ".steplock/checklists/pr-improvement"
head = ["repo_kind", "probe_kev", "scope", "design_choices", "verified", "honest_state", "threshold"]
cases = [
    ("config repo skips a stalled gate", head + ["stalled", "config_skip", "checks_green", "reported"], True),
    ("gate passed", head + ["checks_green", "reported"], True),
    ("no skip straight from threshold", head + ["config_skip"], False),
    ("no skip before the gate", ["repo_kind", "probe_kev", "config_skip"], False),
]
fail = 0
for n, (name, path, want_allow) in enumerate(cases):
    root = tempfile.mkdtemp()
    shutil.copytree(checklist, os.path.join(root, checklist))
    event = json.dumps({"session_id": f"p{n}", "hook_event_name": "PreToolUse", "tool_name": "Bash",
                        "tool_input": {"command": "gh pr merge 1"}, "cwd": root})
    env = {**os.environ, "STEPLOCK_GLOBAL_DIR": ""}
    hook = lambda: subprocess.run([steplock], input=event, capture_output=True, text=True, cwd=root, env=env).stdout
    hook()
    ack = os.path.join(root, ".steplock/sessions", f"p{n}", "pr-improvement/ack.sh")
    ok_path = all(subprocess.run(["sh", ack, s], cwd=root, capture_output=True).returncode == 0 for s in path)
    if ok_path:
        subprocess.run(["sh", ack], cwd=root, capture_output=True)
    allowed = ok_path and '"deny"' not in hook()
    ok = allowed == want_allow
    fail += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}")
    shutil.rmtree(root)
sys.exit(1 if fail else 0)
