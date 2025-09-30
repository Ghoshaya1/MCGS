# Multi-language dependency management tool


def create_dependency_file(repo_path: str, project_analysis: dict) -> bool:
    """Create appropriate dependency file based on project language"""
    from .file_operations import write_file_content
    
    language = project_analysis.get("primary_language", "unknown")
    frameworks = project_analysis.get("frameworks", [])
    
    if language == "python":
        return create_python_requirements(repo_path, frameworks)
    elif language in ["javascript", "typescript"]:
        return create_package_json(repo_path, frameworks, language)
    elif language == "csharp":
        return create_csproj(repo_path, frameworks)
    elif language == "java":
        return create_pom_xml(repo_path, frameworks)
    elif language == "go":
        return create_go_mod(repo_path, frameworks)
    elif language == "rust":
        return create_cargo_toml(repo_path, frameworks)
    
    return False


def create_python_requirements(repo_path: str, frameworks: list) -> bool:
    """Create requirements.txt for Python projects"""
    from .file_operations import write_file_content
    
    requirements = []
    
    if "fastapi" in frameworks:
        requirements.extend([
            "fastapi>=0.100.0",
            "uvicorn[standard]>=0.23.0",
            "pydantic>=2.0.0"
        ])
    
    if "flask" in frameworks:
        requirements.extend([
            "flask>=2.3.0",
            "werkzeug>=2.3.0"
        ])
    
    if "django" in frameworks:
        requirements.extend([
            "django>=4.2.0",
            "djangorestframework>=3.14.0"
        ])
    
    # Always add testing dependencies
    requirements.extend([
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0"
    ])
    
    # Add httpx for FastAPI testing
    if "fastapi" in frameworks:
        requirements.append("httpx>=0.24.0")
    
    content = "\n".join(requirements) + "\n"
    return write_file_content(repo_path, "requirements.txt", content)


def create_package_json(repo_path: str, frameworks: list, language: str) -> bool:
    """Create package.json for Node.js projects"""
    from .file_operations import write_file_content, read_file_content
    import json
    import os
    
    # Check if package.json already exists and has React dependencies
    package_json_path = os.path.join(repo_path, "package.json")
    if os.path.exists(package_json_path):
        try:
            existing_content = read_file_content(repo_path, "package.json")
            if existing_content and ("react" in existing_content or "react-scripts" in existing_content):
                # Package.json already exists with React setup, don't override
                return True
        except:
            pass  # If we can't read it, continue with creation
    
    package_data = {
        "name": "generated-project",
        "version": "1.0.0",
        "description": "Generated project",
        "main": "index.js" if language == "javascript" else "dist/index.js",
        "scripts": {
            "start": "node index.js" if language == "javascript" else "node dist/index.js",
            "test": "jest",
            "build": "tsc" if language == "typescript" else "echo 'No build step needed'"
        },
        "dependencies": {},
        "devDependencies": {}
    }
    
    # Add framework dependencies
    if "express" in frameworks:
        package_data["dependencies"]["express"] = "^4.18.0"
        package_data["devDependencies"]["@types/express"] = "^4.17.0"
    
    if "react" in frameworks:
        package_data["dependencies"].update({
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        })
        package_data["devDependencies"].update({
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0"
        })
    
    if "next" in frameworks:
        package_data["dependencies"]["next"] = "^14.0.0"
        package_data["scripts"]["dev"] = "next dev"
        package_data["scripts"]["build"] = "next build"
        package_data["scripts"]["start"] = "next start"
    
    # TypeScript specific
    if language == "typescript":
        package_data["devDependencies"]["typescript"] = "^5.0.0"
        package_data["devDependencies"]["@types/node"] = "^20.0.0"
    
    # Testing
    package_data["devDependencies"]["jest"] = "^29.0.0"
    
    content = json.dumps(package_data, indent=2)
    return write_file_content(repo_path, "package.json", content)


def create_csproj(repo_path: str, frameworks: list) -> bool:
    """Create .csproj file for C# projects"""
    from .file_operations import write_file_content
    
    project_type = "web" if any(f in ["asp.net", "blazor", "mvc"] for f in frameworks) else "console"
    target_framework = "net8.0"
    
    csproj_content = f'''<Project Sdk="Microsoft.NET.Sdk{'.Web' if project_type == 'web' else ''}">

  <PropertyGroup>
    <TargetFramework>{target_framework}</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
'''
    
    # Add package references based on frameworks
    if "asp.net" in frameworks:
        csproj_content += '    <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="8.0.0" />\n'
        csproj_content += '    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.4.0" />\n'
    
    # Testing packages
    csproj_content += '    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.6.0" />\n'
    csproj_content += '    <PackageReference Include="xunit" Version="2.4.2" />\n'
    csproj_content += '    <PackageReference Include="xunit.runner.visualstudio" Version="2.4.5" />\n'
    
    csproj_content += '''  </ItemGroup>

</Project>'''
    
    return write_file_content(repo_path, "Project.csproj", csproj_content)


def create_pom_xml(repo_path: str, frameworks: list) -> bool:
    """Create pom.xml for Java projects"""
    from .file_operations import write_file_content
    
    pom_content = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>generated-project</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
'''
    
    if "spring" in frameworks or "springboot" in frameworks:
        pom_content += '''        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.1.0</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <version>3.1.0</version>
            <scope>test</scope>
        </dependency>
'''
    
    # Testing dependencies
    pom_content += '''        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
            </plugin>
        </plugins>
    </build>
</project>'''
    
    return write_file_content(repo_path, "pom.xml", pom_content)


def create_go_mod(repo_path: str, frameworks: list) -> bool:
    """Create go.mod for Go projects"""
    from .file_operations import write_file_content
    
    go_mod_content = '''module generated-project

go 1.21
'''
    
    if frameworks:
        go_mod_content += '\nrequire (\n'
        
        if "gin" in frameworks:
            go_mod_content += '    github.com/gin-gonic/gin v1.9.1\n'
        if "echo" in frameworks:
            go_mod_content += '    github.com/labstack/echo/v4 v4.11.1\n'
        
        go_mod_content += ')\n'
    
    return write_file_content(repo_path, "go.mod", go_mod_content)


def create_cargo_toml(repo_path: str, frameworks: list) -> bool:
    """Create Cargo.toml for Rust projects"""
    from .file_operations import write_file_content
    
    cargo_content = '''[package]
name = "generated-project"
version = "0.1.0"
edition = "2021"

[dependencies]
'''
    
    if "actix" in frameworks:
        cargo_content += 'actix-web = "4.4"\n'
        cargo_content += 'tokio = { version = "1.0", features = ["full"] }\n'
    elif "warp" in frameworks:
        cargo_content += 'warp = "0.3"\n'
        cargo_content += 'tokio = { version = "1.0", features = ["full"] }\n'
    
    return write_file_content(repo_path, "Cargo.toml", cargo_content)


def setup_project_dependencies(repo_path: str, project_analysis: dict) -> tuple[int, str]:
    """Set up project dependencies for multi-language projects"""
    from .shell import run
    import os
    
    language = project_analysis.get("primary_language", "unknown")
    
    try:
        # Create dependency file first
        if not create_dependency_file(repo_path, project_analysis):
            return 1, "Failed to create dependency file"
        
        # Language-specific dependency installation
        if language == "python":
            return setup_python_deps(repo_path)
        elif language in ["javascript", "typescript"]:
            return setup_node_deps(repo_path)
        elif language == "csharp":
            return setup_dotnet_deps(repo_path)
        elif language == "java":
            return setup_java_deps(repo_path)
        elif language == "go":
            return setup_go_deps(repo_path)
        elif language == "rust":
            return setup_rust_deps(repo_path)
        else:
            return 0, f"No dependency setup available for {language}"
            
    except Exception as e:
        return 1, f"Error setting up dependencies: {e}"


def setup_python_deps(repo_path: str) -> tuple[int, str]:
    """Setup Python dependencies"""
    from .shell import run
    import os
    
    # Check if we should install dependencies (only if venv exists or we can create one)
    venv_path = os.path.join(repo_path, "venv")
    if not os.path.exists(venv_path):
        # Create virtual environment
        code, out = run(["python", "-m", "venv", "venv"], cwd=repo_path)
        if code != 0:
            return code, f"Failed to create venv: {out}"
    
    # Install dependencies
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:  # Unix/Linux/macOS
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    code, out = run([pip_path, "install", "-r", "requirements.txt"], cwd=repo_path)
    return code, out


def setup_node_deps(repo_path: str) -> tuple[int, str]:
    """Setup Node.js dependencies"""
    from .shell import run
    import os
    
    if not os.path.exists(os.path.join(repo_path, "package.json")):
        return 0, "No package.json found"
    
    # Check for yarn.lock or use npm
    if os.path.exists(os.path.join(repo_path, "yarn.lock")):
        code, out = run(["yarn", "install"], cwd=repo_path)
    else:
        code, out = run(["npm", "install"], cwd=repo_path)
    
    return code, out


def setup_dotnet_deps(repo_path: str) -> tuple[int, str]:
    """Setup .NET dependencies"""
    from .shell import run
    
    code, out = run(["dotnet", "restore"], cwd=repo_path)
    return code, out


def setup_java_deps(repo_path: str) -> tuple[int, str]:
    """Setup Java dependencies"""
    from .shell import run
    import os
    
    if os.path.exists(os.path.join(repo_path, "pom.xml")):
        code, out = run(["mvn", "compile"], cwd=repo_path)
    elif os.path.exists(os.path.join(repo_path, "build.gradle")):
        code, out = run(["gradle", "build"], cwd=repo_path)
    else:
        return 0, "No Maven or Gradle build file found"
    
    return code, out


def setup_go_deps(repo_path: str) -> tuple[int, str]:
    """Setup Go dependencies"""
    from .shell import run
    import os
    
    if os.path.exists(os.path.join(repo_path, "go.mod")):
        code, out = run(["go", "mod", "tidy"], cwd=repo_path)
        return code, out
    else:
        return 0, "No go.mod found"


def setup_rust_deps(repo_path: str) -> tuple[int, str]:
    """Setup Rust dependencies"""
    from .shell import run
    import os
    
    if os.path.exists(os.path.join(repo_path, "Cargo.toml")):
        code, out = run(["cargo", "build"], cwd=repo_path)
        return code, out
    else:
        return 0, "No Cargo.toml found"
