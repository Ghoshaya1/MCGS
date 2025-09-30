import argparse, json
from dotenv import load_dotenv
from .graph import build_graph


load_dotenv()


parser = argparse.ArgumentParser()
parser.add_argument("--request", required=True)
parser.add_argument("--repo-path", required=True)
args = parser.parse_args()


initial = {
"request": args.request,
"repo_path": args.repo_path,
"prd": "",
"rfc": "",
"tasks": [],
"branch": "",
"lint_ok": False,
"tests_ok": False,
"sec_ok": False,
"pr_url": "",
"dev_attempts": 0,
"logs": [],
}


app = build_graph()
final = app.invoke(initial)


print("=== DONE ===")
print("PRD written to .agent/PRD.md, RFC to .agent/RFC.md")
print("PR URL:", final.get("pr_url"))
print("\n-- Logs --\n" + "\n".join(final.get("logs", [])))
