import json, os
from typing import Dict, Any


DEFAULT_PATH = ".agent/state.json"


class Session:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.state: Dict[str, Any] = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.state = json.load(f)

    def init_if_empty(self, **kwargs):
        if not self.state:
            self.state = {
                "request": kwargs.get("request", ""),
                "repo_path": kwargs["repo_path"],
                "prd": "", "rfc": "", "tasks": [],
                "branch": "", "lint_ok": False, "tests_ok": False,
                "sec_ok": False, "pr_url": "", "logs": [],
            }
            self.save()
        return self.state

    def update(self, new_state: Dict[str, Any]):
        self.state.update(new_state)
        self.save()

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)
