"""
Language detection and project analysis tool.
Supports Python, JavaScript/Node.js, C#/.NET, Java, Go, Rust, and more.
"""

import os
import json
from typing import Dict, Any, List, Optional


def detect_language_from_request(request: str) -> Optional[str]:
    """Detect intended programming language from user request"""
    request_lower = request.lower()
    
    # Language keywords in request
    language_keywords = {
        'python': ['python', 'django', 'flask', 'fastapi', 'pytest', 'pip'],
        'javascript': ['javascript', 'js', 'node', 'nodejs', 'npm', 'yarn', 'react', 'vue', 'angular', 'express'],
        'typescript': ['typescript', 'ts', 'angular', 'nest', 'nestjs'],
        'csharp': ['c#', 'csharp', '.net', 'dotnet', 'asp.net', 'blazor', 'mvc'],
        'java': ['java', 'spring', 'maven', 'gradle', 'springboot'],
        'go': ['go', 'golang', 'gin', 'gorilla', 'echo'],
        'rust': ['rust', 'cargo', 'actix', 'warp', 'tokio'],
        'php': ['php', 'laravel', 'symfony', 'composer'],
        'ruby': ['ruby', 'rails', 'sinatra', 'gem'],
        'swift': ['swift', 'ios', 'xcode', 'cocoapods'],
        'kotlin': ['kotlin', 'android', 'spring'],
        'dart': ['dart', 'flutter']
    }
    
    # Count matches for each language with weighted scoring
    language_scores = {}
    
    # Primary language names get higher weight
    primary_language_names = {
        'python': ['python'],
        'javascript': ['javascript', 'js', 'node.js', 'nodejs'],
        'typescript': ['typescript', 'ts'],
        'csharp': ['c#', 'csharp', 'c-sharp', '.net', 'dotnet'],
        'java': ['java'],
        'go': ['go', 'golang'],
        'rust': ['rust'],
        'ruby': ['ruby'],
        'swift': ['swift'],
        'kotlin': ['kotlin'],
        'dart': ['dart']
    }
    
    for lang, keywords in language_keywords.items():
        score = 0
        # Give higher weight to primary language names  
        primary_names = primary_language_names.get(lang, [])
        for keyword in keywords:
            # Use word boundaries to avoid partial matches, but handle special cases
            import re
            if keyword in ['c#', '.net']:
                # Special handling for keywords with special characters
                if keyword in request_lower:
                    weight = 3 if keyword in primary_names else 1
                    score += weight
            else:
                # Use word boundaries for normal keywords
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, request_lower):
                    weight = 3 if keyword in primary_names else 1
                    score += weight
        
        if score > 0:
            language_scores[lang] = score
    
    # Return language with highest score
    if language_scores:
        return max(language_scores, key=language_scores.get)
    
    return None


def analyze_project_structure(repo_path: str) -> Dict[str, Any]:
    """Analyze project structure and detect language/framework"""
    structure = {
        "primary_language": "unknown",
        "secondary_languages": [],
        "project_type": "unknown",
        "frameworks": [],
        "build_tools": [],
        "package_managers": [],
        "config_files": [],
        "source_files": [],
        "test_files": [],
        "documentation_files": [],
        "has_tests": False,
        "entry_points": []
    }
    
    files = list_all_files(repo_path)
    
    # Language detection by file extensions
    language_counts = {}
    for file_path in files:
        ext = get_file_extension(file_path)
        lang = extension_to_language(ext)
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1
            structure["source_files"].append(file_path)
    
    # Determine primary language
    if language_counts:
        structure["primary_language"] = max(language_counts, key=language_counts.get)
        structure["secondary_languages"] = [lang for lang in language_counts.keys() 
                                          if lang != structure["primary_language"]]
    
    # Analyze config files and frameworks
    analyze_config_files(repo_path, files, structure)
    
    # Detect project type and frameworks
    detect_frameworks_and_type(repo_path, files, structure)
    
    # Find entry points and test files
    find_entry_points(files, structure)
    find_test_files(files, structure)
    
    return structure


def list_all_files(repo_path: str) -> List[str]:
    """List all files in the repository, excluding common ignore patterns"""
    ignore_dirs = {
        '.git', '.svn', '.hg',
        'node_modules', '__pycache__', '.pytest_cache',
        'venv', 'env', '.venv', '.env',
        'target', 'build', 'dist', 'out',
        'bin', 'obj', '.vs', '.vscode',
        '.idea', '.gradle', '.maven'
    }
    
    ignore_files = {
        '.DS_Store', 'Thumbs.db', '.gitignore',
        '.env', '.env.local', '.env.production'
    }
    
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for filename in filenames:
            if filename not in ignore_files:
                rel_path = os.path.relpath(os.path.join(root, filename), repo_path)
                files.append(rel_path)
    
    return files


def get_file_extension(file_path: str) -> str:
    """Get file extension in lowercase"""
    return os.path.splitext(file_path)[1].lower()


def extension_to_language(ext: str) -> Optional[str]:
    """Map file extension to programming language"""
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.mjs': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.jsx': 'javascript',
        '.cs': 'csharp',
        '.vb': 'vb.net',
        '.fs': 'fsharp',
        '.java': 'java',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.go': 'go',
        '.rs': 'rust',
        '.php': 'php',
        '.rb': 'ruby',
        '.swift': 'swift',
        '.m': 'objective-c',
        '.mm': 'objective-c++',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
        '.dart': 'dart',
        '.r': 'r',
        '.jl': 'julia',
        '.ex': 'elixir',
        '.exs': 'elixir',
        '.clj': 'clojure',
        '.hs': 'haskell',
        '.ml': 'ocaml',
        '.fs': 'fsharp',
        '.pl': 'perl',
        '.sh': 'bash',
        '.ps1': 'powershell'
    }
    return extension_map.get(ext)


def analyze_config_files(repo_path: str, files: List[str], structure: Dict[str, Any]):
    """Analyze configuration files to detect build tools and package managers"""
    config_patterns = {
        # Python
        'requirements.txt': ('python', 'pip'),
        'pyproject.toml': ('python', 'poetry/setuptools'),
        'setup.py': ('python', 'setuptools'),
        'Pipfile': ('python', 'pipenv'),
        'poetry.lock': ('python', 'poetry'),
        
        # Node.js/JavaScript
        'package.json': ('javascript', 'npm/yarn'),
        'yarn.lock': ('javascript', 'yarn'),
        'package-lock.json': ('javascript', 'npm'),
        'tsconfig.json': ('typescript', 'tsc'),
        'webpack.config.js': ('javascript', 'webpack'),
        'vite.config.js': ('javascript', 'vite'),
        'next.config.js': ('javascript', 'next.js'),
        
        # .NET
        '*.csproj': ('csharp', 'dotnet'),
        '*.vbproj': ('vb.net', 'dotnet'),
        '*.fsproj': ('fsharp', 'dotnet'),
        '*.sln': ('csharp', 'dotnet'),
        'global.json': ('csharp', 'dotnet'),
        
        # Java
        'pom.xml': ('java', 'maven'),
        'build.gradle': ('java', 'gradle'),
        'build.gradle.kts': ('kotlin', 'gradle'),
        
        # Go
        'go.mod': ('go', 'go modules'),
        'go.sum': ('go', 'go modules'),
        
        # Rust
        'Cargo.toml': ('rust', 'cargo'),
        'Cargo.lock': ('rust', 'cargo'),
        
        # PHP
        'composer.json': ('php', 'composer'),
        'composer.lock': ('php', 'composer'),
        
        # Ruby
        'Gemfile': ('ruby', 'bundler'),
        'Gemfile.lock': ('ruby', 'bundler'),
        
        # Other
        'Dockerfile': ('docker', 'docker'),
        'docker-compose.yml': ('docker', 'docker-compose'),
        'Makefile': ('make', 'make'),
        'CMakeLists.txt': ('cpp', 'cmake')
    }
    
    for file_path in files:
        filename = os.path.basename(file_path)
        
        # Exact match
        if filename in config_patterns:
            lang, tool = config_patterns[filename]
            structure["config_files"].append(file_path)
            if tool not in structure["build_tools"]:
                structure["build_tools"].append(tool)
        
        # Pattern match for .csproj, .vbproj, etc.
        for pattern, (lang, tool) in config_patterns.items():
            if '*' in pattern:
                if filename.endswith(pattern.replace('*', '')):
                    structure["config_files"].append(file_path)
                    if tool not in structure["build_tools"]:
                        structure["build_tools"].append(tool)


def detect_frameworks_and_type(repo_path: str, files: List[str], structure: Dict[str, Any]):
    """Detect frameworks and project type by analyzing file contents"""
    from .file_operations import read_file_content
    
    framework_patterns = {
        'python': {
            'fastapi': ['from fastapi', 'import fastapi', 'FastAPI()'],
            'flask': ['from flask', 'import flask', 'Flask(__name__)'],
            'django': ['django.', 'DJANGO_SETTINGS_MODULE', 'manage.py'],
            'pytest': ['import pytest', 'def test_', '@pytest.'],
        },
        'javascript': {
            'react': ['import React', 'from "react"', 'React.Component'],
            'vue': ['import Vue', 'from "vue"', '<template>'],
            'angular': ['@angular/', '@Component', '@Injectable'],
            'express': ['require("express")', 'import express', 'express()'],
            'next': ['next/', 'from "next"', 'getServerSideProps'],
        },
        'csharp': {
            'asp.net': ['using Microsoft.AspNetCore', '[ApiController]', 'WebApplication.'],
            'blazor': ['@page', '@code', 'ComponentBase'],
            'mvc': ['Controller', 'ActionResult', 'ViewResult'],
        },
        'java': {
            'spring': ['@SpringBootApplication', '@RestController', '@Service'],
            'springboot': ['@SpringBootApplication', 'SpringApplication.run'],
        }
    }
    
    language = structure["primary_language"]
    if language in framework_patterns:
        for file_path in files:
            if file_path.endswith(get_source_extensions(language)):
                content = read_file_content(repo_path, file_path)
                
                for framework, patterns in framework_patterns[language].items():
                    if any(pattern in content for pattern in patterns):
                        if framework not in structure["frameworks"]:
                            structure["frameworks"].append(framework)


def get_source_extensions(language: str) -> tuple:
    """Get source file extensions for a language"""
    extension_map = {
        'python': ('.py',),
        'javascript': ('.js', '.mjs', '.jsx'),
        'typescript': ('.ts', '.tsx'),
        'csharp': ('.cs',),
        'java': ('.java',),
        'go': ('.go',),
        'rust': ('.rs',),
        'php': ('.php',),
        'ruby': ('.rb',),
    }
    return extension_map.get(language, ())


def find_entry_points(files: List[str], structure: Dict[str, Any]):
    """Find likely entry point files"""
    entry_patterns = {
        'main.py', 'app.py', 'server.py', 'run.py', '__main__.py',
        'index.js', 'server.js', 'app.js', 'main.js',
        'index.ts', 'server.ts', 'app.ts', 'main.ts',
        'Program.cs', 'Startup.cs', 'Main.cs',
        'Main.java', 'Application.java',
        'main.go', 'server.go', 'app.go',
        'main.rs', 'lib.rs', 'server.rs',
        'index.php', 'app.php', 'server.php'
    }
    
    for file_path in files:
        filename = os.path.basename(file_path)
        if filename in entry_patterns:
            structure["entry_points"].append(file_path)


def find_test_files(files: List[str], structure: Dict[str, Any]):
    """Find test files"""
    test_patterns = [
        'test_', '_test.', '.test.', '.spec.',
        '/test/', '/tests/', '__tests__/',
        'Test.cs', 'Tests.cs', 'Test.java'
    ]
    
    for file_path in files:
        if any(pattern in file_path for pattern in test_patterns):
            structure["test_files"].append(file_path)
    
    structure["has_tests"] = len(structure["test_files"]) > 0


def get_language_info(language: str) -> Dict[str, Any]:
    """Get detailed information about a programming language"""
    language_info = {
        'python': {
            'name': 'Python',
            'extensions': ['.py'],
            'package_managers': ['pip', 'poetry', 'pipenv'],
            'build_tools': ['setuptools', 'poetry', 'pip'],
            'test_frameworks': ['pytest', 'unittest', 'nose2'],
            'frameworks': ['Django', 'Flask', 'FastAPI', 'Tornado'],
            'entry_files': ['main.py', 'app.py', 'server.py', '__main__.py'],
            'config_files': ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile']
        },
        'javascript': {
            'name': 'JavaScript',
            'extensions': ['.js', '.mjs', '.jsx'],
            'package_managers': ['npm', 'yarn', 'pnpm'],
            'build_tools': ['webpack', 'vite', 'rollup', 'parcel'],
            'test_frameworks': ['jest', 'mocha', 'vitest', 'cypress'],
            'frameworks': ['React', 'Vue', 'Angular', 'Express', 'Next.js'],
            'entry_files': ['index.js', 'app.js', 'server.js', 'main.js'],
            'config_files': ['package.json', 'package-lock.json', 'yarn.lock']
        },
        'typescript': {
            'name': 'TypeScript',
            'extensions': ['.ts', '.tsx'],
            'package_managers': ['npm', 'yarn', 'pnpm'],
            'build_tools': ['tsc', 'webpack', 'vite', 'rollup'],
            'test_frameworks': ['jest', 'vitest', 'mocha'],
            'frameworks': ['Angular', 'NestJS', 'Next.js', 'Express'],
            'entry_files': ['index.ts', 'app.ts', 'server.ts', 'main.ts'],
            'config_files': ['tsconfig.json', 'package.json']
        },
        'csharp': {
            'name': 'C#',
            'extensions': ['.cs'],
            'package_managers': ['NuGet'],
            'build_tools': ['dotnet', 'MSBuild'],
            'test_frameworks': ['xUnit', 'NUnit', 'MSTest'],
            'frameworks': ['ASP.NET Core', 'Blazor', 'WPF', 'WinForms'],
            'entry_files': ['Program.cs', 'Startup.cs', 'Main.cs'],
            'config_files': ['*.csproj', '*.sln', 'global.json']
        },
        'java': {
            'name': 'Java',
            'extensions': ['.java'],
            'package_managers': ['Maven', 'Gradle'],
            'build_tools': ['Maven', 'Gradle', 'Ant'],
            'test_frameworks': ['JUnit', 'TestNG', 'Mockito'],
            'frameworks': ['Spring Boot', 'Spring', 'Quarkus', 'Micronaut'],
            'entry_files': ['Main.java', 'Application.java'],
            'config_files': ['pom.xml', 'build.gradle', 'build.gradle.kts']
        },
        'go': {
            'name': 'Go',
            'extensions': ['.go'],
            'package_managers': ['go modules'],
            'build_tools': ['go build', 'go mod'],
            'test_frameworks': ['testing', 'testify', 'ginkgo'],
            'frameworks': ['Gin', 'Echo', 'Gorilla', 'Fiber'],
            'entry_files': ['main.go', 'server.go', 'app.go'],
            'config_files': ['go.mod', 'go.sum']
        },
        'rust': {
            'name': 'Rust',
            'extensions': ['.rs'],
            'package_managers': ['cargo'],
            'build_tools': ['cargo'],
            'test_frameworks': ['built-in tests', 'rstest'],
            'frameworks': ['Actix', 'Warp', 'Rocket', 'Axum'],
            'entry_files': ['main.rs', 'lib.rs', 'server.rs'],
            'config_files': ['Cargo.toml', 'Cargo.lock']
        }
    }
    
    return language_info.get(language, {
        'name': language.title(),
        'extensions': [],
        'package_managers': [],
        'build_tools': [],
        'test_frameworks': [],
        'frameworks': [],
        'entry_files': [],
        'config_files': []
    })
