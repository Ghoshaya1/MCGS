import os


def summarize_repo(repo_path: str, max_files: int = 200) -> str:
    """Naive repo summary: list top-level dirs/files and a few README lines."""
    parts = []
    for root, dirs, files in os.walk(repo_path):
        rel = os.path.relpath(root, repo_path)
        depth = rel.count(os.sep)
        if depth > 1:
            continue
        parts.append(f"[{rel}] files: {', '.join(files[:8])}")
        if len(parts) > max_files:
            break
    readme = os.path.join(repo_path, "README.md")
    if os.path.exists(readme):
        with open(readme, "r", encoding="utf-8", errors="ignore") as f:
            parts.append("README.md (head):\n" + f.read(400))
    return "\n".join(parts)
