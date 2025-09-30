import json
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from ..tools.hf import make_chat


class RouteOut(BaseModel):
	intent: str = Field(description="one of: plan, design, dev, tests, security, pr, status, help")
	args: dict = Field(default_factory=dict)


router_prompt = ChatPromptTemplate.from_messages([
	("system", """
You are a strict router for a software-dev multi-agent system.
Choose an intent from {plan, design, dev, tests, security, pr, status, help}.
- plan: refine requirements and produce/patch PRD & tasks
- design: propose/patch RFC/ADR
- dev: implement or modify code/tests in small diffs
- tests: run lints & unit tests
- security: run dependency & secrets scan
- pr: assemble or update a pull request summary
- status: summarize current state
- help: explain available commands
Respond ONLY as JSON: {"intent":"...","args":{...}}
"""),
	("human", "User: {text}\nState summary: {state_summary}")
])


def summarize_state(state: dict) -> str:
	return (
		f"tasks={len(state.get('tasks', []))}, "
		f"branch={state.get('branch') or '-'}, "
		f"lint_ok={state.get('lint_ok')}, tests_ok={state.get('tests_ok')}, sec_ok={state.get('sec_ok')}"
	)

INTENTS = {"plan","design","dev","tests","security","pr","status","help"}


def route(text: str, state: dict) -> RouteOut:
	chat = make_chat()
	msg = router_prompt.format_messages(text=text, state_summary=summarize_state(state))
	raw = chat.invoke(msg).content
	try:
		data = json.loads(raw)
	except Exception:
		start, end = raw.find("{"), raw.rfind("}") + 1
		data = json.loads(raw[start:end])
	out = RouteOut(**data)
	if out.intent not in INTENTS:
		out.intent = "help"
	return out
