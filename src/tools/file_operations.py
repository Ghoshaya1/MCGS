import os
import json
from typing import List, Dict, Any


def read_file_content(repo_path: str, file_path: str) -> str:
    """Read content of a file relative to repo_path"""
    full_path = os.path.join(repo_path, file_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return f"Error reading file: {e}"


def write_file_content(repo_path: str, file_path: str, content: str) -> bool:
    """Write content to a file relative to repo_path"""
    full_path = os.path.join(repo_path, file_path)
    try:
        # Validate content is string
        if not isinstance(content, str):
            print(f"Error writing file {file_path}: content must be str, got {type(content).__name__}")
            print(f"Content preview: {str(content)[:200]}...")
            return False
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        print(f"Content type: {type(content).__name__}")
        return False


def list_files(repo_path: str, pattern: str = "*.py") -> List[str]:
    """List files in repo matching pattern"""
    import glob
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        # Skip hidden directories and common build/cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', 'env']]
        for filename in filenames:
            if not filename.startswith('.'):
                rel_path = os.path.relpath(os.path.join(root, filename), repo_path)
                files.append(rel_path)
    return files


def analyze_project_structure(repo_path: str) -> Dict[str, Any]:
    """Analyze the project structure to understand what kind of project it is"""
    # Use the new language detector
    from .language_detector import analyze_project_structure as detect_structure
    return detect_structure(repo_path)


def get_project_template(language: str, project_type: str = "basic") -> Dict[str, str]:
    """Get project template files for a specific language and type"""
    from .project_templates import get_template_files
    return get_template_files(language, project_type)
