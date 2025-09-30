import argparse
from dotenv import load_dotenv
from .session import Session
from .graph import build_graph
from .agents.router import route
from .agents import planner, architect, dev as dev_agent, tests_agent, security as sec_agent, pr_agent


load_dotenv()


ACTIONS = {
"plan": planner.planner_node,
"design": architect.architect_node,
"dev": dev_agent.dev_node,
"tests": tests_agent.tests_node,
"security": sec_agent.security_node,
"pr": pr_agent.pr_node,
}


HELP_TEXT = (
"Commands: plan, design, dev, tests, security, pr, status, help.\n"
"Type natural language and the router will choose. Prefix with / to force, e.g., /tests"
)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--repo-path", required=True)
	parser.add_argument("--request", default="")
	args = parser.parse_args()


sess = Session()
state = sess.init_if_empty(repo_path=args.repo_path, request=args.request)


print("🤖 Multi-Agent REPL. Type 'exit' to quit.")
print("🤖 Multi-Agent REPL. Type 'exit' to quit.\n" + HELP_TEXT)
while True:
	try:
		user = input("you> ").strip()
	except (EOFError, KeyboardInterrupt):
		print()
		break
	if user.lower() in {"exit", "quit"}:
		break
	if not user:
		continue

	# Slash command override
	if user.startswith("/"):
		forced = user[1:].split()[0]
		intent = forced if forced in ACTIONS or forced in {"status", "help"} else "help"
		args = {}
	else:
		r = route(user, state)
		intent, args = r.intent, r.args

	if intent == "status":
		print(f"status> branch={state.get('branch') or '-'} lint_ok={state.get('lint_ok')} tests_ok={state.get('tests_ok')} sec_ok={state.get('sec_ok')} pr_url={state.get('pr_url') or '-'}")
		continue
	if intent == "help":
		print(HELP_TEXT)
		continue

	fn = ACTIONS.get(intent)
	if not fn:
		print("(no action)")
		continue

	try:
		state = fn(state)
		sess.update(state)
		print(f"ok> {intent} done. Logs tail: {state['logs'][-1][:160] if state['logs'] else ''}")
	except Exception as e:
		print("error>", e)

if __name__ == "__main__":
	main()
