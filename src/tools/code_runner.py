"""
Multi-language code runner for different programming languages.
"""

import os
import subprocess
from typing import Dict, Any, Tuple, List, Optional


def run_project_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run tests for a project based on its language and structure"""
    language = project_analysis.get("primary_language", "unknown")
    
    test_runners = {
        'python': run_python_tests,
        'javascript': run_javascript_tests,
        'typescript': run_typescript_tests,
        'csharp': run_csharp_tests,
        'java': run_java_tests,
        'go': run_go_tests,
        'rust': run_rust_tests,
        'php': run_php_tests,
        'ruby': run_ruby_tests,
    }
    
    if language in test_runners:
        return test_runners[language](repo_path, project_analysis)
    
    return 0, f"No test runner available for {language}"


def run_project_build(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build a project based on its language and structure"""
    language = project_analysis.get("primary_language", "unknown")
    
    build_runners = {
        'python': build_python_project,
        'javascript': build_javascript_project,
        'typescript': build_typescript_project,
        'csharp': build_csharp_project,
        'java': build_java_project,
        'go': build_go_project,
        'rust': build_rust_project,
        'php': build_php_project,
        'ruby': build_ruby_project,
    }
    
    if language in build_runners:
        return build_runners[language](repo_path, project_analysis)
    
    return 0, f"No build runner available for {language}"


def run_project_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run linting for a project based on its language and structure"""
    language = project_analysis.get("primary_language", "unknown")
    
    linters = {
        'python': run_python_linting,
        'javascript': run_javascript_linting,
        'typescript': run_typescript_linting,
        'csharp': run_csharp_linting,
        'java': run_java_linting,
        'go': run_go_linting,
        'rust': run_rust_linting,
        'php': run_php_linting,
        'ruby': run_ruby_linting,
    }
    
    if language in linters:
        return linters[language](repo_path, project_analysis)
    
    return 0, f"No linter available for {language}"


# Python runners
def run_python_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Python tests"""
    try:
        # Try pytest first
        result = subprocess.run(
            ["python", "-m", "pytest", "-v"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0 or "collected" in result.stdout:
            return result.returncode, result.stdout + result.stderr
        
        # Fallback to unittest
        result = subprocess.run(
            ["python", "-m", "unittest", "discover", "-v"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout + result.stderr
    
    except subprocess.TimeoutExpired:
        return 1, "Test execution timed out"
    except Exception as e:
        return 1, f"Error running Python tests: {e}"


def build_python_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build Python project (mainly check syntax)"""
    try:
        result = subprocess.run(
            ["python", "-m", "py_compile"] + [f for f in project_analysis.get("source_files", []) if f.endswith('.py')],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error building Python project: {e}"


def run_python_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Python linting"""
    try:
        # Try ruff first
        result = subprocess.run(
            ["ruff", "check", "."],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 127:  # Command found
            return result.returncode, result.stdout + result.stderr
        
        # Fallback to flake8
        result = subprocess.run(
            ["flake8", "."],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    
    except Exception as e:
        return 1, f"Error running Python linting: {e}"


# JavaScript/Node.js runners
def run_javascript_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run JavaScript tests"""
    try:
        if os.path.exists(os.path.join(repo_path, "package.json")):
            result = subprocess.run(
                ["npm", "test"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode, result.stdout + result.stderr
        else:
            return 0, "No package.json found"
    except Exception as e:
        return 1, f"Error running JavaScript tests: {e}"


def build_javascript_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build JavaScript project"""
    try:
        if os.path.exists(os.path.join(repo_path, "package.json")):
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            # If build script doesn't exist, that's okay
            if "missing script: build" in result.stderr:
                return 0, "No build script defined (okay for basic projects)"
            return result.returncode, result.stdout + result.stderr
        else:
            return 0, "No package.json found"
    except Exception as e:
        return 1, f"Error building JavaScript project: {e}"


def run_javascript_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run JavaScript linting"""
    try:
        # Try ESLint
        result = subprocess.run(
            ["npx", "eslint", "."],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running JavaScript linting: {e}"


# TypeScript runners
def run_typescript_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run TypeScript tests"""
    return run_javascript_tests(repo_path, project_analysis)  # Usually same as JS


def build_typescript_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build TypeScript project"""
    try:
        if os.path.exists(os.path.join(repo_path, "tsconfig.json")):
            result = subprocess.run(
                ["npx", "tsc"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode, result.stdout + result.stderr
        else:
            return build_javascript_project(repo_path, project_analysis)
    except Exception as e:
        return 1, f"Error building TypeScript project: {e}"


def run_typescript_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run TypeScript linting"""
    try:
        # Try TypeScript compiler for type checking
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running TypeScript linting: {e}"


# C# runners
def run_csharp_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run C# tests"""
    try:
        result = subprocess.run(
            ["dotnet", "test"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running C# tests: {e}"


def build_csharp_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build C# project"""
    try:
        result = subprocess.run(
            ["dotnet", "build"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error building C# project: {e}"


def run_csharp_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run C# linting"""
    try:
        # dotnet build includes compile-time checks
        result = subprocess.run(
            ["dotnet", "build", "--verbosity", "normal"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running C# linting: {e}"


# Java runners
def run_java_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Java tests"""
    try:
        if os.path.exists(os.path.join(repo_path, "pom.xml")):
            result = subprocess.run(
                ["mvn", "test"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=180
            )
        elif os.path.exists(os.path.join(repo_path, "build.gradle")):
            gradle_cmd = "./gradlew" if os.path.exists(os.path.join(repo_path, "gradlew")) else "gradle"
            result = subprocess.run(
                [gradle_cmd, "test"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=180
            )
        else:
            return 0, "No Maven or Gradle build file found"
        
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running Java tests: {e}"


def build_java_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build Java project"""
    try:
        if os.path.exists(os.path.join(repo_path, "pom.xml")):
            result = subprocess.run(
                ["mvn", "compile"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=180
            )
        elif os.path.exists(os.path.join(repo_path, "build.gradle")):
            gradle_cmd = "./gradlew" if os.path.exists(os.path.join(repo_path, "gradlew")) else "gradle"
            result = subprocess.run(
                [gradle_cmd, "compileJava"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=180
            )
        else:
            return 0, "No Maven or Gradle build file found"
        
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error building Java project: {e}"


def run_java_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Java linting"""
    try:
        # Use checkstyle if available, otherwise just compile
        result = subprocess.run(
            ["mvn", "checkstyle:check"] if os.path.exists(os.path.join(repo_path, "pom.xml")) else ["gradle", "check"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return build_java_project(repo_path, project_analysis)  # Fallback to build


# Go runners
def run_go_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Go tests"""
    try:
        result = subprocess.run(
            ["go", "test", "./..."],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running Go tests: {e}"


def build_go_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build Go project"""
    try:
        result = subprocess.run(
            ["go", "build", "./..."],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error building Go project: {e}"


def run_go_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Go linting"""
    try:
        # Try golangci-lint first, then go vet
        result = subprocess.run(
            ["golangci-lint", "run"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 127:  # Command found
            return result.returncode, result.stdout + result.stderr
        
        # Fallback to go vet
        result = subprocess.run(
            ["go", "vet", "./..."],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running Go linting: {e}"


# Rust runners
def run_rust_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Rust tests"""
    try:
        result = subprocess.run(
            ["cargo", "test"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=180
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running Rust tests: {e}"


def build_rust_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build Rust project"""
    try:
        result = subprocess.run(
            ["cargo", "build"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=180
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error building Rust project: {e}"


def run_rust_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Rust linting"""
    try:
        result = subprocess.run(
            ["cargo", "clippy", "--", "-D", "warnings"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running Rust linting: {e}"


# PHP runners
def run_php_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run PHP tests"""
    try:
        if os.path.exists(os.path.join(repo_path, "vendor/bin/phpunit")):
            result = subprocess.run(
                ["vendor/bin/phpunit"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=120
            )
        else:
            result = subprocess.run(
                ["phpunit"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=120
            )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running PHP tests: {e}"


def build_php_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build PHP project (syntax check)"""
    try:
        php_files = [f for f in project_analysis.get("source_files", []) if f.endswith('.php')]
        if not php_files:
            return 0, "No PHP files found"
        
        for php_file in php_files:
            result = subprocess.run(
                ["php", "-l", php_file],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                return result.returncode, result.stdout + result.stderr
        
        return 0, "All PHP files syntax check passed"
    except Exception as e:
        return 1, f"Error building PHP project: {e}"


def run_php_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run PHP linting"""
    try:
        # Try PHP_CodeSniffer
        result = subprocess.run(
            ["phpcs", "."],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return build_php_project(repo_path, project_analysis)  # Fallback to syntax check


# Ruby runners
def run_ruby_tests(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Ruby tests"""
    try:
        if os.path.exists(os.path.join(repo_path, "spec")):
            # RSpec
            result = subprocess.run(
                ["rspec"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=120
            )
        else:
            # Minitest
            result = subprocess.run(
                ["ruby", "-Itest", "-e", "Dir.glob('./test/**/*_test.rb').each {|f| require f}"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=120
            )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running Ruby tests: {e}"


def build_ruby_project(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Build Ruby project (syntax check)"""
    try:
        ruby_files = [f for f in project_analysis.get("source_files", []) if f.endswith('.rb')]
        if not ruby_files:
            return 0, "No Ruby files found"
        
        for ruby_file in ruby_files:
            result = subprocess.run(
                ["ruby", "-c", ruby_file],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                return result.returncode, result.stdout + result.stderr
        
        return 0, "All Ruby files syntax check passed"
    except Exception as e:
        return 1, f"Error building Ruby project: {e}"


def run_ruby_linting(repo_path: str, project_analysis: Dict[str, Any]) -> Tuple[int, str]:
    """Run Ruby linting"""
    try:
        # Try RuboCop
        result = subprocess.run(
            ["rubocop"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return build_ruby_project(repo_path, project_analysis)  # Fallback to syntax check


def get_run_commands(language: str, project_type: str = "basic") -> Dict[str, str]:
    """Get common run commands for a language"""
    commands = {
        'python': {
            'run': 'python main.py',
            'test': 'pytest',
            'lint': 'ruff check .',
            'install': 'pip install -r requirements.txt'
        },
        'javascript': {
            'run': 'node index.js',
            'test': 'npm test',
            'lint': 'eslint .',
            'install': 'npm install',
            'build': 'npm run build'
        },
        'typescript': {
            'run': 'npm start',
            'test': 'npm test',
            'lint': 'tsc --noEmit',
            'install': 'npm install',
            'build': 'tsc'
        },
        'csharp': {
            'run': 'dotnet run',
            'test': 'dotnet test',
            'build': 'dotnet build',
            'restore': 'dotnet restore'
        },
        'java': {
            'maven_run': 'mvn exec:java',
            'maven_test': 'mvn test',
            'maven_build': 'mvn compile',
            'gradle_run': 'gradle run',
            'gradle_test': 'gradle test',
            'gradle_build': 'gradle build'
        },
        'go': {
            'run': 'go run main.go',
            'test': 'go test ./...',
            'build': 'go build',
            'lint': 'go vet ./...'
        },
        'rust': {
            'run': 'cargo run',
            'test': 'cargo test',
            'build': 'cargo build',
            'lint': 'cargo clippy'
        },
        'php': {
            'run': 'php index.php',
            'test': 'phpunit',
            'lint': 'phpcs .',
            'install': 'composer install'
        },
        'ruby': {
            'run': 'ruby main.rb',
            'test': 'rspec',
            'lint': 'rubocop',
            'install': 'bundle install'
        }
    }
    
    return commands.get(language, {})
