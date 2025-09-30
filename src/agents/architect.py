from langchain_core.prompts import ChatPromptTemplate
from ..tools.hf import make_chat
from ..tools.repo_context import summarize_repo


architect_prompt = ChatPromptTemplate.from_messages([
("system", """
You are the Architect.
Produce an RFC in Markdown:
- Proposed module boundaries and folder layout
- Public interfaces and data flow
- Risks & alternatives
Return RAW Markdown, no backticks.
"""),
("human", "PRD:\n{prd}\n\nRepo summary:\n{repo}")
])


def _write_artifact(repo_path: str, rel: str, content: str):
    import os
    path = os.path.join(repo_path, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)    

def architect_node(state):
    chat = make_chat("architecture")  # Use architecture-optimized config
    repo = summarize_repo(state["repo_path"])[:4000]
    out = chat.invoke(architect_prompt.format_messages(prd=state["prd"], repo=repo)).content
    state["rfc"] = out
    state["logs"].append("Architect: RFC produced")
    # Persist artifacts
    _write_artifact(state["repo_path"], ".agent/PRD.md", state["prd"])
    _write_artifact(state["repo_path"], ".agent/RFC.md", state["rfc"])
    return state
