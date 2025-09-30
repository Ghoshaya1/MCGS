import json
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from ..tools.hf import make_chat


class Task(BaseModel):
    id: str
    title: str
    
    @classmethod
    def model_validate(cls, data):
        # Handle different field names that the LLM might use
        if isinstance(data, dict):
            # Map task_id to id
            if 'task_id' in data and 'id' not in data:
                data['id'] = str(data['task_id'])
            # Map task_desc to title
            if 'task_desc' in data and 'title' not in data:
                data['title'] = data['task_desc']
        return super().model_validate(data)


class PlannerOut(BaseModel):
    prd_md: str = Field(..., description="Markdown PRD with goals and acceptance criteria")
    tasks: List[Task]


planner_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are the Planner.
    - Convert the user request into a concise PRD (markdown) and 3–6 atomic tasks.
    - Prefer small, independent tasks.
    - Output ONLY valid JSON with this exact format:
    {{
      "prd_md": "# PRD\\n\\n## Goal\\n...markdown content...",
      "tasks": [
        {{"id": "task1", "title": "Task description"}},
        {{"id": "task2", "title": "Another task description"}}
      ]
    }}
    """),
    ("human", "{request}")
])


def planner_node(state):
    chat = make_chat("planning")  # Use larger model for complex planning
    msg = planner_prompt.format_messages(request=state["request"])
    raw = chat.invoke(msg).content
    
    # Log the raw response for debugging
    state["logs"].append(f"Planner raw response: {raw[:200]}...")
    
    try:
        data = json.loads(raw)
    except Exception as e:
        state["logs"].append(f"JSON parse error: {e}")
        # light repair attempt: extract JSON block
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            # No JSON found, create a fallback response
            state["logs"].append("No JSON found, creating fallback response")
            data = {
                "prd_md": f"# PRD\n\nRequest: {state['request']}\n\n## Goal\nImplement the requested feature.\n\n## Acceptance Criteria\n- Feature implemented\n- Tests pass\n- Code follows standards",
                "tasks": [
                    {"id": "task1", "title": "Implement feature"},
                    {"id": "task2", "title": "Add tests"},
                    {"id": "task3", "title": "Update documentation"}
                ]
            }
        else:
            try:
                extracted = raw[start:end]
                state["logs"].append(f"Extracted JSON: {extracted[:200]}...")
                data = json.loads(extracted)
            except Exception as e2:
                state["logs"].append(f"Extracted JSON parse error: {e2}")
                # Final fallback
                data = {
                    "prd_md": f"# PRD\n\nRequest: {state['request']}\n\n## Goal\nImplement the requested feature.\n\n## Acceptance Criteria\n- Feature implemented\n- Tests pass\n- Code follows standards",
                    "tasks": [
                        {"id": "task1", "title": "Implement feature"},
                        {"id": "task2", "title": "Add tests"},
                        {"id": "task3", "title": "Update documentation"}
                    ]
                }
    
    # Convert tasks to the expected format
    if 'tasks' in data:
        converted_tasks = []
        for task in data['tasks']:
            if isinstance(task, dict):
                task_data = {
                    'id': str(task.get('task_id', task.get('id', f"task{len(converted_tasks)+1}"))),
                    'title': task.get('task_desc', task.get('title', 'Untitled task'))
                }
                converted_tasks.append(task_data)
        data['tasks'] = converted_tasks
    
    out = PlannerOut(**data)
    state["prd"] = out.prd_md
    state["tasks"] = [t.dict() for t in out.tasks]
    state["logs"].append("Planner: PRD+tasks created")
    return state
