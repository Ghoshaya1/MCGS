from .shell import run
import os


def run_tests(repo_path: str, project_analysis: dict):
    """Run tests based on project language"""
    language = project_analysis.get("primary_language", "unknown")
    
    if language == "python":
        return run_python_tests(repo_path)
    elif language in ["javascript", "typescript"]:
        return run_node_tests(repo_path)
    elif language == "csharp":
        return run_dotnet_tests(repo_path)
    elif language == "java":
        return run_java_tests(repo_path)
    elif language == "go":
        return run_go_tests(repo_path)
    elif language == "rust":
        return run_rust_tests(repo_path)
    else:
        return 1, f"No test runner configured for {language}"


def run_linter(repo_path: str, project_analysis: dict):
    """Run linter based on project language"""
    language = project_analysis.get("primary_language", "unknown")
    
    if language == "python":
        return run_python_linter(repo_path)
    elif language in ["javascript", "typescript"]:
        return run_node_linter(repo_path)
    elif language == "csharp":
        return run_dotnet_linter(repo_path)
    elif language == "java":
        return run_java_linter(repo_path)
    elif language == "go":
        return run_go_linter(repo_path)
    elif language == "rust":
        return run_rust_linter(repo_path)
    else:
        return 0, f"No linter configured for {language}"


def run_security_audit(repo_path: str, project_analysis: dict):
    """Run security audit based on project language"""
    language = project_analysis.get("primary_language", "unknown")
    
    if language == "python":
        return run_python_audit(repo_path)
    elif language in ["javascript", "typescript"]:
        return run_node_audit(repo_path)
    elif language == "csharp":
        return run_dotnet_audit(repo_path)
    elif language == "java":
        return run_java_audit(repo_path)
    elif language == "go":
        return run_go_audit(repo_path)
    elif language == "rust":
        return run_rust_audit(repo_path)
    else:
        return 0, f"No security audit configured for {language}"


# Python runners
def run_python_tests(repo_path: str):
    try:
        # Try to use project's virtual environment first
        venv_path = os.path.join(repo_path, "venv")
        if os.path.exists(venv_path):
            if os.name == 'nt':  # Windows
                pytest_path = os.path.join(venv_path, "Scripts", "pytest")
            else:  # Unix/Linux/macOS
                pytest_path = os.path.join(venv_path, "bin", "pytest")
            
            if os.path.exists(pytest_path):
                return run([pytest_path, "-q"], cwd=repo_path)
        
        # Fallback to system pytest
        return run(["pytest", "-q"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "pytest not found - skipping tests"


def run_python_linter(repo_path: str):
    try:
        return run(["ruff", "check", "."], cwd=repo_path)
    except FileNotFoundError:
        return 1, "ruff not found - skipping lint check"


def run_python_audit(repo_path: str):
    try:
        # Check if requirements.txt exists
        req_file = os.path.join(repo_path, "requirements.txt")
        if os.path.exists(req_file):
            return run(["pip-audit", "-r", "requirements.txt"], cwd=repo_path)
        else:
            # Run on current environment if no requirements.txt
            return run(["pip-audit"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "pip-audit not found - skipping security check"


# Node.js runners
def run_node_tests(repo_path: str):
    try:
        # Check if npm test script exists
        package_json = os.path.join(repo_path, "package.json")
        if os.path.exists(package_json):
            return run(["npm", "test"], cwd=repo_path)
        else:
            return run(["jest"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "npm/jest not found - skipping tests"


def run_node_linter(repo_path: str):
    try:
        # Try ESLint first
        return run(["npx", "eslint", "."], cwd=repo_path)
    except FileNotFoundError:
        return 1, "eslint not found - skipping lint check"


def run_node_audit(repo_path: str):
    try:
        return run(["npm", "audit"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "npm not found - skipping security audit"


# .NET runners
def run_dotnet_tests(repo_path: str):
    try:
        return run(["dotnet", "test"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "dotnet not found - skipping tests"


def run_dotnet_linter(repo_path: str):
    try:
        return run(["dotnet", "format", "--verify-no-changes"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "dotnet not found - skipping lint check"


def run_dotnet_audit(repo_path: str):
    try:
        return run(["dotnet", "list", "package", "--vulnerable"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "dotnet not found - skipping security audit"


# Java runners
def run_java_tests(repo_path: str):
    try:
        # Check for Maven first
        if os.path.exists(os.path.join(repo_path, "pom.xml")):
            return run(["mvn", "test"], cwd=repo_path)
        # Check for Gradle
        elif os.path.exists(os.path.join(repo_path, "build.gradle")) or os.path.exists(os.path.join(repo_path, "build.gradle.kts")):
            return run(["./gradlew", "test"], cwd=repo_path)
        else:
            return 1, "No build tool found (Maven/Gradle)"
    except FileNotFoundError:
        return 1, "Java build tools not found - skipping tests"


def run_java_linter(repo_path: str):
    try:
        # Try Checkstyle
        return run(["mvn", "checkstyle:check"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "checkstyle not found - skipping lint check"


def run_java_audit(repo_path: str):
    try:
        if os.path.exists(os.path.join(repo_path, "pom.xml")):
            return run(["mvn", "dependency:tree"], cwd=repo_path)
        else:
            return run(["./gradlew", "dependencies"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "Java build tools not found - skipping security audit"


# Go runners
def run_go_tests(repo_path: str):
    try:
        return run(["go", "test", "./..."], cwd=repo_path)
    except FileNotFoundError:
        return 1, "go not found - skipping tests"


def run_go_linter(repo_path: str):
    try:
        return run(["golint", "./..."], cwd=repo_path)
    except FileNotFoundError:
        try:
            return run(["go", "vet", "./..."], cwd=repo_path)
        except FileNotFoundError:
            return 1, "go linter not found - skipping lint check"


def run_go_audit(repo_path: str):
    try:
        return run(["go", "list", "-m", "all"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "go not found - skipping security audit"


# Rust runners
def run_rust_tests(repo_path: str):
    try:
        return run(["cargo", "test"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "cargo not found - skipping tests"


def run_rust_linter(repo_path: str):
    try:
        return run(["cargo", "clippy"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "cargo not found - skipping lint check"


def run_rust_audit(repo_path: str):
    try:
        return run(["cargo", "audit"], cwd=repo_path)
    except FileNotFoundError:
        return 1, "cargo-audit not found - skipping security audit"


# Legacy functions for backward compatibility
def run_pytests(repo_path: str):
    """Legacy function - use run_python_tests instead"""
    return run_python_tests(repo_path)


def run_ruff(repo_path: str):
    """Legacy function - use run_python_linter instead"""
    return run_python_linter(repo_path)


def run_pip_audit(repo_path: str):
    """Legacy function - use run_python_audit instead"""
    return run_python_audit(repo_path)
