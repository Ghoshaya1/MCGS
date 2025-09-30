from langchain_core.prompts import ChatPromptTemplate
from ..tools.git_tools import ensure_branch
from ..tools.hf import make_chat_for_language
from ..tools.file_operations import analyze_project_structure, read_file_content, write_file_content
from ..tools.dependency_manager import setup_project_dependencies
from ..tools.language_detector import detect_language_from_request


dev_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a Senior Developer. Generate code based on the RFC and project analysis.
    
    Project Analysis: {project_analysis}
    RFC: {rfc}
    Tasks: {tasks}
    
    Based on the analysis, generate the necessary code files for the detected language and framework.
    
    CRITICAL: You must return ONLY valid JSON. Do not include any markdown, explanations, or formatting.
    Start your response with {{ and end with }}.
    
    IMPORTANT: When writing file content, escape special characters properly:
    - Use \\n for newlines
    - Use \\" for quotes inside strings
    - Use \\\\ for backslashes
    - Do NOT use @ strings, raw strings, or multiline strings
    
    CRITICAL for Go projects:
    - Use ONLY standard library imports (fmt, net/http, encoding/json, etc.)
    - DO NOT use fake import paths like "github.com/your/project/..."
    - Keep all Go code in the main package unless creating actual separate packages
    - Module name in go.mod should be simple (e.g., "myapp", "go-server")
    
    Use this exact format:
    {{
        "files": [
            {{
                "path": "relative/path/to/file.ext",
                "content": "// Full file content here\\ncode..."
            }}
        ],
        "summary": "Brief summary of changes made"
    }}
    
    Guidelines by language:
    - Python: Use proper imports, type hints, docstrings, and follow PEP 8
    - JavaScript/TypeScript: Use modern ES6+ syntax, proper error handling, and JSDoc comments
    - C#: Use proper namespaces, async/await patterns, and XML documentation
    - Java: Use proper packages, annotations, and Javadoc comments  
    - Go: Use proper package structure, error handling, and Go conventions. Use standard library only unless external dependencies are essential. Module paths should match the actual project structure.
    - Rust: Use proper modules, error handling with Result types, and Rust idioms
    
    Always include appropriate tests and documentation files.
    """),
    ("human", "Generate the code files needed for: {request}. Language context: {language}. Remember: Return ONLY valid JSON, no markdown or explanations.")
])


def dev_node(state):
    repo = state["repo_path"]
    if not state.get("branch"):
        state["branch"] = ensure_branch(repo, "feat/auto-agent")
    
    # Track development attempts to prevent infinite loops
    dev_attempts = state.get("dev_attempts", 0) + 1
    state["dev_attempts"] = dev_attempts
    
    state["logs"].append(f"Dev: Starting development (attempt {dev_attempts})")
    
    try:
        # Analyze the project structure
        project_analysis = analyze_project_structure(repo)
        state["logs"].append(f"Dev: Analyzed project - Type: {project_analysis['project_type']}, Language: {project_analysis['primary_language']}")
        
        # Detect language from request if not detected from project
        detected_language = project_analysis.get("primary_language", "unknown")
        if detected_language == "unknown":
            detected_language = detect_language_from_request(state["request"]) or "python"
            project_analysis["primary_language"] = detected_language
            state["logs"].append(f"Dev: Detected language from request: {detected_language}")
        
        # Use LLM to generate code - select best model for the language
        chat = make_chat_for_language(detected_language, "coding")
        state["logs"].append(f"Dev: Using model for {detected_language} coding")
        
        msg = dev_prompt.format_messages(
            project_analysis=str(project_analysis),
            rfc=state.get("rfc", ""),
            tasks=str(state.get("tasks", [])),
            request=state["request"],
            language=detected_language
        )
        
        raw_response = chat.invoke(msg).content
        state["logs"].append(f"Dev: LLM response received ({len(raw_response)} chars)")
        
        # Parse the JSON response
        import json
        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as e:
            state["logs"].append(f"Dev: JSON decode error: {e}")
            # Try to extract JSON from response
            start = raw_response.find("{")
            end = raw_response.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    data = json.loads(raw_response[start:end])
                    state["logs"].append("Dev: Successfully extracted JSON from response")
                except json.JSONDecodeError as e2:
                    state["logs"].append(f"Dev: Failed to parse extracted JSON: {e2}")
                    state["logs"].append(f"Dev: Raw response (first 500 chars): {raw_response[:500]}")
                    data = _generate_fallback_code(state, project_analysis)
            else:
                state["logs"].append("Dev: No JSON found in response, using fallback")
                state["logs"].append(f"Dev: Raw response (first 500 chars): {raw_response[:500]}")
                data = _generate_fallback_code(state, project_analysis)
        
        # Write the generated files
        files_written = 0
        for file_info in data.get("files", []):
            file_path = file_info["path"]
            content = file_info["content"]
            
            # Handle case where LLM returns content as dict instead of string
            if isinstance(content, dict):
                if file_path.endswith(".json"):
                    # For JSON files, convert dict to JSON string
                    import json
                    content = json.dumps(content, indent=2)
                else:
                    # For other files, this is likely malformed - try to extract string
                    state["logs"].append(f"Dev: Warning - content for {file_path} is dict, attempting to fix")
                    if isinstance(content, dict) and len(content) == 1:
                        content = list(content.values())[0]
                    else:
                        content = str(content)
            
            if write_file_content(repo, file_path, content):
                files_written += 1
                state["logs"].append(f"Dev: Created/updated {file_path}")
            else:
                state["logs"].append(f"Dev: Failed to write {file_path}")
        
        summary = data.get("summary", "Code generation completed")
        state["logs"].append(f"Dev: {summary} ({files_written} files)")
        
        # Set up project dependencies
        if files_written > 0:
            dep_code, dep_out = setup_project_dependencies(repo, project_analysis)
            if dep_code == 0:
                state["logs"].append("Dev: Dependencies installed successfully")
            else:
                state["logs"].append(f"Dev: Dependency setup failed: {dep_out[:200]}...")
        
    except Exception as e:
        import traceback
        state["logs"].append(f"Dev: Error during development: {e}")
        state["logs"].append(f"Dev: Traceback: {traceback.format_exc()}")
        # Generate fallback code
        project_analysis = analyze_project_structure(repo)
        fallback_data = _generate_fallback_code(state, project_analysis)
        for file_info in fallback_data.get("files", []):
            if write_file_content(repo, file_info["path"], file_info["content"]):
                state["logs"].append(f"Dev: Created fallback {file_info['path']}")
    
    return state


def _generate_fallback_code(state, project_analysis):
    """Generate basic fallback code when LLM fails - supports multiple languages"""
    request = state["request"].lower()
    language = project_analysis.get("primary_language", "python")
    
    # Import template generator
    from ..tools.project_templates import get_template_files
    
    # Determine project type from request
    if any(keyword in request for keyword in ["react", "dashboard", "frontend", "ui", "web app", "webapp"]):
        if language in ["javascript", "typescript"]:
            project_type = "react"
        else:
            project_type = "basic"
    elif any(keyword in request for keyword in ["api", "rest", "endpoint", "health", "server"]):
        if language == "python" and ("fastapi" in request or "fast" in request):
            project_type = "fastapi"
        elif language in ["javascript", "typescript"] and ("express" in request or "node" in request):
            project_type = "express"
        elif language == "csharp" and ("dotnet" in request or ".net" in request):
            project_type = "dotnet"
        elif language == "java" and ("spring" in request):
            project_type = "spring"
        else:
            project_type = "api"
    elif any(keyword in request for keyword in ["game", "tic-tac-toe", "tictactoe"]):
        project_type = "game"
    elif any(keyword in request for keyword in ["web", "website", "frontend"]):
        project_type = "web"
    else:
        project_type = "basic"
    
    try:
        # Get template files from existing system
        template_files = get_template_files(language, project_type)
        
        # Convert to the expected format
        files = []
        for path, content in template_files.items():
            files.append({
                "path": path,
                "content": content
            })
        
        return {
            "files": files,
            "summary": f"Generated {language} {project_type} project with {len(files)} files"
        }
        
    except Exception as e:
        # Ultimate fallback - create a basic file structure
        if language == "python":
            return _get_python_basic_fallback(request)
        elif language in ["javascript", "typescript"]:
            return _get_javascript_basic_fallback(language, request)
        elif language == "csharp":
            return _get_csharp_basic_fallback(request)
        elif language == "java":
            return _get_java_basic_fallback(request)
        elif language == "go":
            return _get_go_basic_fallback(request)
        elif language == "rust":
            return _get_rust_basic_fallback(request)
        else:
            return _get_python_basic_fallback(request)


def _get_python_basic_fallback(request):
    """Basic Python fallback"""
    return {
        "files": [
            {
                "path": "main.py",
                "content": f'''#!/usr/bin/env python3
"""
Generated Python application.
"""

def main():
    """Main function"""
    print("Hello from Python!")
    print("Request: {request}")

if __name__ == "__main__":
    main()
'''
            },
            {
                "path": "requirements.txt",
                "content": "# No dependencies required\n"
            }
        ],
        "summary": "Generated basic Python application"
    }


def _get_javascript_basic_fallback(language, request):
    """Basic JavaScript/TypeScript fallback"""
    ext = "ts" if language == "typescript" else "js"
    return {
        "files": [
            {
                "path": f"index.{ext}",
                "content": f'''/**
 * Generated JavaScript application
 */

function main() {{
    console.log("Hello from JavaScript!");
    console.log("Request: {request}");
}}

if (require.main === module) {{
    main();
}}

module.exports = {{ main }};
'''
            },
            {
                "path": "package.json",
                "content": '''{
  "name": "generated-app",
  "version": "1.0.0",
  "description": "Generated application",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "echo \\"No tests specified\\""
  }
}
'''
            }
        ],
        "summary": f"Generated basic {language} application"
    }


def _get_csharp_basic_fallback(request):
    """Basic C# fallback"""
    return {
        "files": [
            {
                "path": "Program.cs",
                "content": f'''using System;

namespace GeneratedApp
{{
    class Program
    {{
        static void Main(string[] args)
        {{
            Console.WriteLine("Hello from C#!");
            Console.WriteLine("Request: {request}");
        }}
    }}
}}
'''
            },
            {
                "path": "ConsoleApp.csproj",
                "content": '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
</Project>
'''
            }
        ],
        "summary": "Generated basic C# application"
    }


def _get_java_basic_fallback(request):
    """Basic Java fallback"""
    return {
        "files": [
            {
                "path": "src/main/java/com/example/App.java",
                "content": f'''package com.example;

public class App {{
    public static void main(String[] args) {{
        System.out.println("Hello from Java!");
        System.out.println("Request: {request}");
    }}
}}
'''
            },
            {
                "path": "pom.xml",
                "content": '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>generated-app</artifactId>
    <version>1.0.0</version>
    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>
</project>
'''
            }
        ],
        "summary": "Generated basic Java application"
    }


def _get_go_basic_fallback(request):
    """Basic Go fallback"""
    if any(keyword in request for keyword in ["server", "routing", "web", "api", "http"]):
        return {
            "files": [
                {
                    "path": "main.go",
                    "content": '''package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
    Status  string `json:"status"`
}

func main() {
    // Set up routes  
    http.HandleFunc("/", homeHandler)
    http.HandleFunc("/health", healthHandler)
    
    fmt.Println("Go server starting on :8080")
    fmt.Println("Routes available:")
    fmt.Println("  GET  /       - Home page")
    fmt.Println("  GET  /health - Health check")
    
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    response := Response{
        Message: "Welcome to Go Web Server",
        Status:  "running",
    }
    json.NewEncoder(w).Encode(response)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    response := Response{
        Status: "healthy",
    }
    json.NewEncoder(w).Encode(response)
}
'''
                },
                {
                    "path": "go.mod",
                    "content": '''module go-server

go 1.21
'''
                },
                {
                    "path": "main_test.go",
                    "content": '''package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHealthHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/health", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(healthHandler)
    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }
}

func TestHomeHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(homeHandler)
    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }
}
'''
                }
            ],
            "summary": "Generated Go web server with routing"
        }
    else:
        return {
            "files": [
                {
                    "path": "main.go",
                    "content": '''package main

import "fmt"

func main() {
    fmt.Println("Hello, Go World!")
    
    person := Person{Name: "Alice", Age: 30}
    fmt.Println(person.Greet())
}

type Person struct {
    Name string
    Age  int
}

func (p Person) Greet() string {
    return fmt.Sprintf("Hello, my name is %s and I am %d years old.", p.Name, p.Age)
}
'''
                },
                {
                    "path": "go.mod",
                    "content": '''module go-app

go 1.21
'''
                },
                {
                    "path": "main_test.go",
                    "content": '''package main

import "testing"

func TestPersonGreet(t *testing.T) {
    person := Person{Name: "Bob", Age: 25}
    expected := "Hello, my name is Bob and I am 25 years old."
    
    if got := person.Greet(); got != expected {
        t.Errorf("Person.Greet() = %v, want %v", got, expected)
    }
}
'''
                }
            ],
            "summary": "Generated basic Go application"
        }


def _get_rust_basic_fallback(request):
    """Basic Rust fallback"""
    return {
        "files": [
            {
                "path": "src/main.rs",
                "content": f'''use std::io::prelude::*;
use std::net::{{TcpListener, TcpStream}};

fn main() {{
    println!("Starting Rust server...");
    let listener = TcpListener::bind("127.0.0.1:8080").unwrap();
    
    for stream in listener.incoming() {{
        let stream = stream.unwrap();
        handle_connection(stream);
    }}
}}

fn handle_connection(mut stream: TcpStream) {{
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();
    
    let response = "HTTP/1.1 200 OK\\r\\n\\r\\n{{\\\"status\\\": \\\"healthy\\\"}}";
    stream.write(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}}
'''
            },
            {
                "path": "Cargo.toml",
                "content": '''[package]
name = "generated-app"
version = "0.1.0"
edition = "2021"

[dependencies]
'''
            }
        ],
        "summary": "Generated basic Rust application"
    }
