from .shell import run


def ensure_branch(repo_path: str, name: str) -> str:
    code, out = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path)
    # create if not exists
    run(["git", "checkout", "-B", name], cwd=repo_path)
    return name
