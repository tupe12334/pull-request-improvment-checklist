import json, os, shutil, subprocess, sys, tempfile

# Feed each command in trigger-cases.tsv to steplock and check that it
# blocks or allows as expected. Usage: check-trigger.py [steplock-binary]
steplock = sys.argv[1] if len(sys.argv) > 1 else "steplock"
checklist = ".steplock/checklists/pr-improvement"
cases = os.path.join(os.path.dirname(__file__), "trigger-cases.tsv")
fail = 0
for n, line in enumerate(open(cases).read().splitlines()):
    want, cmd = line.split("\t", 1)
    cmd = cmd.replace("\\n", "\n")
    root = tempfile.mkdtemp()
    shutil.copytree(checklist, os.path.join(root, ".steplock/checklists/pr-improvement"))
    event = {"session_id": f"c{n}", "hook_event_name": "PreToolUse", "tool_name": "Bash",
             "tool_input": {"command": cmd}, "cwd": root}
    out = subprocess.run([os.path.abspath(steplock) if os.sep in steplock else steplock], input=json.dumps(event), capture_output=True, text=True,
                         cwd=root, env={**os.environ, "STEPLOCK_GLOBAL_DIR": ""}).stdout
    got = "BLOCK" if '"deny"' in out else "ALLOW"
    ok = got == want
    fail += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {want:5} {cmd.splitlines()[0][:60]!r}")
    shutil.rmtree(root)
sys.exit(1 if fail else 0)
