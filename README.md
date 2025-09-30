# Multiagent Code Generation System

A sophisticated multiagent system that automatically plans, designs, and generates code for software development tasks **in any programming language**. The system uses multiple specialized AI agents working together to create production-ready code with proper testing, linting, security auditing, and pull request generation.

## Multi-Language Support

This system supports code generation in multiple programming languages with intelligent language detection and framework-specific optimizations:

### Supported Languages & Frameworks:
- **Python**: FastAPI, Flask, Django, pytest
- **JavaScript**: Node.js, Express.js, React, Jest  
- **TypeScript**: Express.js, React, Jest
- **C#/.NET**: ASP.NET Core, Entity Framework, xUnit
- **Java**: Spring Boot, Maven, JUnit
- **Go**: Gin, Chi, Go modules, Go test
- **Rust**: Actix, Warp, Cargo, Rust test
  

### Intelligent Features:
- **Smart Language Detection**: Automatically detects target language from your request
- **Language-Specific Model Selection**: Uses optimized models for each programming language
- **Framework-Aware Code Generation**: Generates appropriate boilerplate for popular frameworks
- **Multi-Language Testing**: Runs language-appropriate tests (pytest, Jest, Go test, etc.)  
- **Language-Specific Linting**: Uses proper linters (ruff, ESLint, golangci-lint, etc.)
- **Dependency Management**: Handles requirements.txt, package.json, go.mod, Cargo.toml, etc.

## Features

- **Planning Agent**: Analyzes user requests and creates detailed Product Requirements Documents (PRDs)
- **Architecture Agent**: Designs technical implementation plans and Request for Comments (RFCs)
- **Development Agent**: Generates actual code files, sets up dependencies, and creates project structure
- **Testing Agent**: Runs automated tests and code quality checks using ruff linting
- **Security Agent**: Performs security audits using pip-audit
- **PR Agent**: Creates pull request summaries and documentation

## Supported Project Types (Any Language)

- **Web APIs**: RESTful APIs, GraphQL endpoints, microservices
  - Python: FastAPI, Flask, Django REST
  - JavaScript/TypeScript: Express.js, Koa.js, NestJS
  - C#: ASP.NET Core Web API
  - Java: Spring Boot, JAX-RS
  - Go: Gin, Chi, Echo
  - Rust: Actix-web, Warp

- **Web Applications**: Full-stack applications with frontend and backend
  - Python: Django, Flask with templates
  - JavaScript: Node.js + React/Vue
  - TypeScript: Express + React/Angular
  - C#: ASP.NET MVC/Blazor
  - Java: Spring MVC, JSP

- **Command Line Tools**: CLI applications and utilities
  - Python: Click, argparse
  - JavaScript: Commander.js
  - Go: Cobra, flag
  - Rust: Clap, structopt
  - C#: System.CommandLine

- **Games & Interactive Applications**: Simple games and interactive programs
  - Python: Pygame, console games
  - JavaScript: Browser games, Node.js games
  - C#: Console games, Unity scripts
  - Go: Terminal games
  - Rust: Console games

All projects include:
- **Smart Dependency Management**: requirements.txt, package.json, go.mod, Cargo.toml, .csproj
- **Language-Appropriate Testing**: pytest, Jest, Go test, Rust test, xUnit
- **Code Quality Checks**: Language-specific linting and formatting
- **Security Audits**: Where applicable (pip-audit for Python, etc.)
- **Proper Project Structure**: Following language conventions and best practices

## Prerequisites

- Python 3.8 or higher (for running the multiagent system)
- Git (for repository operations)
- Hugging Face API token
- **Target language tools** (installed automatically when possible):
  - **Node.js & npm** (for JavaScript/TypeScript projects)
  - **.NET SDK** (for C# projects)  
  - **Java & Maven** (for Java projects)
  - **Go** (for Go projects)
  - **Rust & Cargo** (for Rust projects)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd multiagent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Hugging Face API token:
```bash
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```

Get your token from: https://huggingface.co/settings/tokens

## Usage

### Basic Usage

Run the multiagent system with a development request:

```bash
python -m src.main --request "Create a complete e-commerce API with product catalog and shopping cart" --repo-path /path/to/target/repo
```

### Command Line Arguments

- `--request`: Description of what you want to build (required)
- `--repo-path`: Path to the target repository where code will be generated (required)

### Example Requests (Multi-Language)

#### Python Examples:
```bash
# FastAPI e-commerce API
python -m src.main --request "Create a Python FastAPI e-commerce API with product catalog and shopping cart" --repo-path ../python-ecommerce

# Django blog platform  
python -m src.main --request "Build a Django blog platform with user authentication and comments" --repo-path ../django-blog
```

#### JavaScript/TypeScript Examples:
```bash
# Express.js REST API
python -m src.main --request "Create a JavaScript Express.js REST API with health endpoints" --repo-path ../js-api

# TypeScript React app
python -m src.main --request "Build a TypeScript React application with user dashboard" --repo-path ../ts-react-app
```

#### C# Examples:
```bash
# ASP.NET Core Web API
python -m src.main --request "Create a C# ASP.NET Core web API with health endpoints" --repo-path ../csharp-api

# .NET console application
python -m src.main --request "Build a C# .NET console application for data processing" --repo-path ../csharp-console
```

#### Go Examples:
```bash
# Go REST API
python -m src.main --request "Create a Go REST API with health endpoints" --repo-path ../go-api

# Go web server
python -m src.main --request "Build a simple Go web server with routing" --repo-path ../go-server
```

#### Java Examples:
```bash
# Spring Boot API
python -m src.main --request "Create a Java Spring Boot REST API with CRUD operations" --repo-path ../java-spring

# Java console application
python -m src.main --request "Build a Java console application for file processing" --repo-path ../java-console
```

#### Rust Examples:
```bash
# Rust web server
python -m src.main --request "Create a Rust web server with health endpoints" --repo-path ../rust-server

# Rust CLI tool
python -m src.main --request "Build a Rust command-line tool for text processing" --repo-path ../rust-cli
```

#### Game Examples:
```bash
# Python tic-tac-toe
python -m src.main --request "Create a Python tic-tac-toe game" --repo-path ../python-tictactoe

# JavaScript browser game  
python -m src.main --request "Build a JavaScript browser-based puzzle game" --repo-path ../js-game
```

## How It Works

The system follows a structured, language-aware workflow:

1. **Planning Phase**: Analyzes the request and creates a detailed PRD
2. **Architecture Phase**: Designs the technical implementation and creates an RFC  
3. **Development Phase**: 
   - **Language Detection**: Automatically detects target language from request
   - **Smart Model Selection**: Chooses optimal AI model for the detected language
   - **Project Analysis**: Analyzes existing project structure and conventions
   - **Code Generation**: Generates language-appropriate code files and structure
   - **Dependency Setup**: Installs dependencies using language package managers
4. **Testing Phase**: 
   - **Language-Specific Linting**: Uses appropriate linters (ruff, ESLint, golangci-lint, etc.)
   - **Multi-Language Testing**: Runs tests using language test frameworks (pytest, Jest, Go test, etc.)
5. **Security Phase**: Performs security audits where available (pip-audit for Python, etc.)
6. **PR Phase**: Creates pull request documentation

### Intelligent Language Detection

The system automatically detects your target language from natural language requests:

- `"Create a Python FastAPI server"` → **Python** + FastAPI framework
- `"Build a JavaScript React app"` → **JavaScript** + React framework  
- `"Make a C# .NET web API"` → **C#** + .NET framework
- `"Create a Go REST API"` → **Go** + REST API pattern
- `"Build a Rust web server"` → **Rust** + web server pattern

### Smart Model & Tool Selection

For each language, the system:
- **Selects optimal AI models** trained for that language
- **Uses appropriate package managers**: pip, npm, dotnet, mvn, go mod, cargo
- **Applies language-specific linting**: ruff, ESLint, golangci-lint, clippy
- **Runs proper test frameworks**: pytest, Jest, Go test, Rust test, xUnit

## Generated Project Structures

The system automatically generates appropriate project structures based on your request and detected language:

### Python FastAPI Structure:
```
python-api/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies  
├── test_main.py        # pytest tests
└── README.md           # Documentation
```

### JavaScript Express Structure:
```
js-api/
├── app.js              # Express server
├── package.json        # npm dependencies
├── app.test.js         # Jest tests  
└── README.md           # Documentation
```

### C# ASP.NET Structure:
```
csharp-api/
├── Program.cs          # Main application
├── WebApi.csproj       # Project file
├── Controllers/        # API controllers
└── README.md           # Documentation
```

### Go Web Server Structure:
```
go-api/
├── main.go             # Main application
├── go.mod              # Go modules
├── main_test.go        # Go tests
└── README.md           # Documentation
```

### Java Spring Boot Structure:
```
java-api/
├── src/main/java/      # Java source files
├── pom.xml             # Maven dependencies
├── src/test/java/      # JUnit tests
└── README.md           # Documentation
```

### Rust Web Server Structure:
```
rust-api/
├── src/main.rs         # Main application  
├── Cargo.toml          # Rust dependencies
├── tests/              # Rust tests
└── README.md           # Documentation
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app setup
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   ├── routes/            # API endpoints
│   │   ├── __init__.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   └── orders.py
│   └── services/          # Business logic
│       ├── __init__.py
│       └── payment.py
├── tests/
│   ├── __init__.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
└── requirements.txt       # Auto-managed dependencies
```

### Blog Platform Structure:
```
blog-platform/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── posts.py
│   │   └── admin.py
│   └── templates/         # HTML templates (if web UI requested)
│       ├── index.html
│       └── post.html
├── static/               # CSS/JS files
│   ├── style.css
│   └── app.js
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_posts.py
└── requirements.txt
```

### Data Analytics Dashboard Structure:
```
analytics-dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── data/             # Data processing
│   │   ├── __init__.py
│   │   ├── processor.py
│   │   └── visualizer.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   └── dashboard.py
│   └── utils/
│       ├── __init__.py
│       └── charts.py
├── uploads/              # File upload directory
├── tests/
│   ├── __init__.py
│   └── test_data_processing.py
└── requirements.txt
```

## Advanced Features

### Language-Aware Templating
The system includes comprehensive project templates for each supported language:

- **Basic Projects**: Simple console applications and starter projects
- **API Projects**: RESTful APIs with health endpoints, routing, and middleware
- **Web Projects**: Full web applications with frontend and backend components  
- **Game Projects**: Interactive games and entertainment applications

### Intelligent Fallback System
When AI models encounter issues, the system gracefully falls back to:
1. **Template-based generation**: Uses pre-built templates for the detected language
2. **Language-specific basic projects**: Creates minimal but functional applications
3. **Cross-language compatibility**: Ensures projects work in the target environment

### Multi-Provider AI Support
Choose from multiple AI providers for optimal results:

| Provider | Languages | Specialization |
|----------|-----------|----------------|
| **Hugging Face** | All supported | Open-source models, code generation |
| **OpenAI** | All supported | Advanced reasoning, complex projects |
| **Anthropic** | All supported | Safety-focused, reliable outputs |
| **Ollama** | All supported | Local models, privacy-focused |

### Error Handling & Recovery
- **Automatic retry logic**: Attempts multiple approaches when generation fails
- **JSON parsing recovery**: Extracts valid content from malformed responses
- **Dependency conflict resolution**: Handles package manager conflicts automatically
- **Language environment validation**: Verifies required tools are available

### Testing & Quality Assurance

| Language | Linter | Test Framework | Package Manager |
|----------|--------|----------------|-----------------|
| Python | ruff | pytest | pip |
| JavaScript | ESLint | Jest | npm/yarn |
| TypeScript | ESLint + TSC | Jest | npm/yarn |
| C# | dotnet format | xUnit | NuGet |
| Java | CheckStyle | JUnit | Maven/Gradle |
| Go | golangci-lint | go test | go modules |
| Rust | clippy | cargo test | cargo |

## Configuration

### Environment Variables

- `HUGGINGFACEHUB_API_TOKEN`: Your Hugging Face API token (required)
- `HF_MODEL_ID`: Override the default model (optional, defaults to Meta-Llama-3.1-8B-Instruct)

### Supported Models

The system supports multiple LLM providers and models, with specialized configurations for different tasks:

#### Currently Available (Hugging Face):
- **default**: `meta-llama/Meta-Llama-3.1-8B-Instruct` - General-purpose model
- **planning**: `meta-llama/Meta-Llama-3.1-70B-Instruct` - Larger model for complex planning
- **coding**: `meta-llama/Meta-Llama-3.1-8B-Instruct` - Code generation (all languages)
- **python_coding**: `meta-llama/Meta-Llama-3.1-8B-Instruct` - Python-optimized
- **javascript_coding**: `meta-llama/Meta-Llama-3.1-8B-Instruct` - JavaScript-optimized
- **csharp_coding**: `meta-llama/Meta-Llama-3.1-8B-Instruct` - C#-optimized
- **mistral**: `mistralai/Mistral-7B-Instruct-v0.1` - Efficient general-purpose
- **gemma**: `google/gemma-7b-it` - Google's instruction-tuned model

#### Additional Providers (Ready to Use):
- **OpenAI**: GPT-4, GPT-3.5-turbo (requires `OPENAI_API_KEY` + `pip install langchain-openai`)
- **Anthropic**: Claude-3 models (requires `ANTHROPIC_API_KEY` + `pip install langchain-anthropic`)  
- **Ollama**: Local models (requires Ollama running locally + `pip install langchain-ollama`)

#### Model Configuration Options:
```bash
# Environment variable only affects default config (preserves specialization)
HF_MODEL_ID=your-preferred-model  # Only used when no specific config requested

# Agent specialization (ignores HF_MODEL_ID)
chat = make_chat("coding")        # Always uses bigcode/starcoder2-15b
chat = make_chat("planning")      # Always uses meta-llama/Meta-Llama-3.1-70B-Instruct
chat = make_chat("architecture")  # Always uses meta-llama/Meta-Llama-3.1-8B-Instruct

# Direct overrides (highest priority)
chat = make_chat(model_id="custom-model")  # Direct model override
chat = make_chat("coding", model_id="different-code-model")  # Override specialized config
```

**Priority Order** (highest to lowest):
1. Direct `model_id` parameter
2. Named configuration (e.g., "coding", "planning")  
3. `HF_MODEL_ID` environment variable (default only)
4. Built-in default model

## Project Structure

```
multiagent/
├── src/
│   ├── main.py              # Entry point
│   ├── graph.py             # Agent workflow orchestration
│   ├── state.py             # Shared state management
│   ├── session.py           # Session management
│   ├── agents/              # AI agents
│   │   ├── planner.py       # Planning agent
│   │   ├── architect.py     # Architecture agent
│   │   ├── dev.py           # Development agent
│   │   ├── test_agent.py    # Testing agent
│   │   ├── security.py      # Security agent
│   │   └── pr_agent.py      # PR agent
│   └── tools/               # Utility tools
│       ├── hf.py            # Hugging Face integration
│       ├── git_tools.py     # Git operations
│       ├── shell.py         # Shell command execution
│       ├── runners.py       # Test and lint runners
│       ├── repo_context.py  # Repository analysis
│       ├── file_operations.py  # File I/O operations
│       └── dependency_manager.py  # Dependency management
├── tests/
│   └── test_smoke.py        # System tests
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Testing Model Configurations

Test different LLM models and configurations:

```bash
python test_models.py
```

This will:
- List all available model configurations  
- Test model instantiation
- Show which agents use which models
- Demonstrate usage examples

### Code Quality

The system uses ruff for linting and formatting:

```bash
ruff check src/
ruff format src/
```

### Adding New Agents

1. Create a new agent file in `src/agents/`
2. Implement the agent function following the existing patterns
3. Add the agent to the workflow in `src/graph.py`
4. Update the state management in `src/state.py` if needed

### Adding New Tools

1. Create a new tool file in `src/tools/`
2. Implement utility functions following existing patterns
3. Import and use in relevant agents

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the project root and using `python -m src.main`

2. **Missing Dependencies**: The system automatically installs dependencies in target repos, but ensure your multiagent environment has all requirements installed

3. **Hugging Face API Issues**: 
   - Verify your API token is correct
   - Check your token has appropriate permissions
   - Ensure you have access to the model being used

4. **Permission Errors**: Ensure the target repository path is writable

5. **Git Issues**: The system creates branches automatically, ensure git is configured properly

### Debug Mode

For verbose output, you can modify the logging in individual agent files or add debug prints.

## Usage Tips & Troubleshooting

### Best Practices

#### Writing Effective Requests:
- **Be specific about the language**: "Create a **Python** FastAPI server" vs "Create a server"
- **Mention frameworks**: "Build a **React** app" vs "Build a web app"  
- **Include key features**: "Create a REST API **with health endpoints**"
- **Specify project type**: "Build a **console application**" vs "Build an application"

#### Examples of Good Requests:
```bash
"Create a Python FastAPI e-commerce API with product catalog and shopping cart"
"Build a JavaScript Express.js REST API with authentication middleware"
"Make a C# ASP.NET Core web API with health endpoints and Swagger docs"
"Create a Go web server with routing and JSON responses"
```

#### Examples of Unclear Requests:
```bash
"Create an app" (no language, no specifics)
"Build something with a database" (too vague)
"Make a website" (unclear if frontend, backend, or both)
```

### Common Issues & Solutions

#### Language Detection Issues:
```bash
# Problem: Wrong language detected
Request: "Create a server with health endpoints"
Detected: python (default fallback)

# Solution: Be explicit about language
Request: "Create a Go server with health endpoints" 
Detected: go
```

#### Model/Provider Errors:
```bash  
# Problem: StopIteration or provider errors
Error: "provider_helper = get_provider_helper(...) StopIteration"

# Solution: Model not available, system falls back to templates automatically
# Check logs: "Dev: Using fallback code generation"
```

#### Dependency Installation Issues:
```bash
# Problem: Dependencies fail to install
Error: "Dependency setup failed: MSBUILD : error MSB1011"

# Solution: Ensure target language tools are installed:
- .NET SDK for C# projects
- Node.js for JavaScript projects  
- Go for Go projects
- Java + Maven for Java projects
```

#### Missing Linters/Tools:
```bash
# Problem: Linter not found
Error: "Error running Go linting: [Errno 2] No such file or directory: 'golangci-lint'"

# Solution: Install language-specific tools (optional):
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
npm install -g eslint
pip install ruff
```

### System Status Indicators

Watch for these log messages to understand what's happening:

#### Success Indicators:
```
Dev: Detected language from request: go
Dev: Using model for go coding  
Dev: LLM response received (2501 chars)
Tests (go): exit=0
Dependencies installed successfully
```

#### Fallback Indicators:
```  
Dev: JSON decode error: Invalid control character
Dev: Using fallback code generation
Dev: Generated go api project with 4 files (4 files)
```

#### Error Indicators (Still Works):
```
Linter (go): exit=1 (tool not installed, but tests pass)
Tests (python): exit=5 (wrong language, but project generated)
```

### Performance Tips

- **Smaller projects generate faster**: Start with basic projects, then iterate
- **Language-specific models are optimized**: Python/JS requests use specialized models
- **Fallback system is reliable**: Even if AI fails, you get working code templates
- **Dependencies auto-install**: Most package managers work automatically

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Architecture Notes

The system uses LangGraph for orchestrating the multiagent workflow. Each agent is implemented as a node in the graph, with shared state passed between agents. The system is designed to be extensible and can be adapted for different programming languages and frameworks.

Key design principles:
- Modular agent architecture
- Robust error handling and fallbacks
- Automatic dependency management
- Real file system operations
- Production-ready code generation
