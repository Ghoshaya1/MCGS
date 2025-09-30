import os
from typing import Optional, Dict, Any
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.language_models.chat_models import BaseChatModel

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, rely on system environment


# Model configurations for different use cases
MODEL_CONFIGS = {
    "default": {
        "provider": "huggingface",
        "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "temperature": 0.2,
        "max_new_tokens": 1024,
    },
    "planning": {
        "provider": "huggingface", 
        "model_id": "meta-llama/Meta-Llama-3.1-70B-Instruct",  # Larger model for complex planning
        "temperature": 0.3,
        "max_new_tokens": 2048,
    },
    "coding": {
        "provider": "huggingface",
        "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",  # Use working model for now
        "temperature": 0.1,  # Lower temperature for more deterministic code
        "max_new_tokens": 4096,
    },
    "architecture": {
        "provider": "huggingface",
        "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "temperature": 0.2,
        "max_new_tokens": 1536,
    },
    # Additional Hugging Face models for variety
    "mistral": {
        "provider": "huggingface",
        "model_id": "mistralai/Mistral-7B-Instruct-v0.1",
        "temperature": 0.2,
        "max_new_tokens": 1024,
    },
    "codellama": {
        "provider": "huggingface", 
        "model_id": "codellama/CodeLlama-13b-Instruct-hf",
        "temperature": 0.1,
        "max_new_tokens": 2048,
    },
    "gemma": {
        "provider": "huggingface",
        "model_id": "google/gemma-7b-it",
        "temperature": 0.3,
        "max_new_tokens": 1024,
    },
    # Language-specific coding models (when available)
    "python_coding": {
        "provider": "huggingface",
        "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "temperature": 0.1,
        "max_new_tokens": 4096,
    },
    "javascript_coding": {
        "provider": "huggingface", 
        "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "temperature": 0.1,
        "max_new_tokens": 4096,
    },
    "csharp_coding": {
        "provider": "huggingface",
        "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct", 
        "temperature": 0.1,
        "max_new_tokens": 4096,
    },
    # OpenAPI models (require langchain-openai)
    "openai_gpt4": {
        "provider": "openai",
        "model_id": "gpt-4",
        "temperature": 0.2,
        "max_tokens": 1024,
    },
    "openai_gpt35": {
        "provider": "openai",
        "model_id": "gpt-3.5-turbo",
        "temperature": 0.2,
        "max_tokens": 1024,
    },
    # Anthropic models (require langchain-anthropic)
    "anthropic_claude": {
        "provider": "anthropic", 
        "model_id": "claude-3-sonnet-20240229",
        "temperature": 0.2,
        "max_tokens": 1024,
    },
    "anthropic_haiku": {
        "provider": "anthropic",
        "model_id": "claude-3-haiku-20240307",
        "temperature": 0.2,
        "max_tokens": 1024,
    },
    # Ollama models (require langchain-ollama)
    "ollama_codellama": {
        "provider": "ollama",
        "model_id": "codellama:13b",
        "temperature": 0.1,
        "max_tokens": 4096,
    },
    "ollama_mistral": {
        "provider": "ollama", 
        "model_id": "mistral:7b",
        "temperature": 0.2,
        "max_tokens": 2048,
    },
}


# Language-specific model preferences
LANGUAGE_MODEL_PREFERENCES = {
    "python": ["python_coding", "coding", "default"],
    "javascript": ["javascript_coding", "coding", "default"],
    "typescript": ["javascript_coding", "coding", "default"],
    "csharp": ["csharp_coding", "coding", "default"],
    "java": ["coding", "default"],
    "go": ["coding", "default"],
    "rust": ["coding", "default"],
    "cpp": ["coding", "default"],
    "c": ["coding", "default"],
}

# Task-specific model fallbacks
TASK_MODEL_FALLBACKS = {
    "coding": ["coding", "python_coding", "javascript_coding", "default"],
    "planning": ["planning", "architecture", "default"],
    "architecture": ["architecture", "planning", "default"],
    "general": ["default"],
}


def select_best_model_for_language(language: str, task: str = "coding") -> str:
    """
    Select the best available model for a given programming language and task.
    
    Args:
        language: Programming language (python, javascript, etc.)
        task: Type of task (coding, planning, architecture, etc.)
        
    Returns:
        Name of the best available model configuration
        
    Examples:
        >>> select_best_model_for_language("python", "coding")
        'python_coding'  # if available, otherwise falls back
        
        >>> select_best_model_for_language("rust", "planning") 
        'planning'  # language-specific not needed for planning
    """
    
    # First try language-specific models
    if language in LANGUAGE_MODEL_PREFERENCES:
        for model_config in LANGUAGE_MODEL_PREFERENCES[language]:
            if model_config in MODEL_CONFIGS:
                # Check if the provider is available
                config = MODEL_CONFIGS[model_config]
                if is_provider_available(config["provider"]):
                    return model_config
    
    # Fall back to task-specific models
    if task in TASK_MODEL_FALLBACKS:
        for model_config in TASK_MODEL_FALLBACKS[task]:
            if model_config in MODEL_CONFIGS:
                config = MODEL_CONFIGS[model_config]
                if is_provider_available(config["provider"]):
                    return model_config
    
    # Final fallback to default
    return "default"


def is_provider_available(provider: str) -> bool:
    """
    Check if a provider is available based on environment variables and dependencies.
    
    Args:
        provider: Provider name (huggingface, openai, anthropic, ollama)
        
    Returns:
        True if provider is available, False otherwise
    """
    
    if provider == "huggingface":
        return bool(os.environ.get("HUGGINGFACEHUB_API_TOKEN"))
    
    elif provider == "openai":
        return bool(os.environ.get("OPENAI_API_KEY"))
    
    elif provider == "anthropic":
        return bool(os.environ.get("ANTHROPIC_API_KEY"))
    
    elif provider == "ollama":
        # Check if Ollama is running locally
        try:
            import requests
            base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
            response = requests.get(f"{base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    return False


def _create_huggingface_chat(config: Dict[str, Any]) -> BaseChatModel:
    """Create a Hugging Face chat model."""
    token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is required. Please set it in your .env file or environment.")
    
    llm = HuggingFaceEndpoint(
        repo_id=config["model_id"],
        temperature=config["temperature"],
        max_new_tokens=config["max_new_tokens"],
        huggingfacehub_api_token=token,
    )
    return ChatHuggingFace(llm=llm)


def _create_openai_chat(config: Dict[str, Any]) -> BaseChatModel:
    """Create an OpenAI chat model."""
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=config["model_id"],
            temperature=config["temperature"],
            max_tokens=config.get("max_tokens", 1024),
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
    except ImportError:
        raise NotImplementedError(
            "OpenAI provider requires langchain-openai. Install with: pip install langchain-openai"
        )


def _create_anthropic_chat(config: Dict[str, Any]) -> BaseChatModel:
    """Create an Anthropic chat model. (Placeholder - requires langchain-anthropic)"""
    # TODO: Uncomment when langchain-anthropic is installed  
    # from langchain_anthropic import ChatAnthropic
    # return ChatAnthropic(
    #     model=config["model_id"],
    #     temperature=config["temperature"],
    #     max_tokens=config.get("max_tokens", 1024),
    #     api_key=os.environ.get("ANTHROPIC_API_KEY"),
    # )
    raise NotImplementedError("Anthropic provider not yet implemented. Add langchain-anthropic to requirements.txt")


# Provider factory mapping
PROVIDER_FACTORIES = {
    "huggingface": _create_huggingface_chat,
    "openai": _create_openai_chat,
    "anthropic": _create_anthropic_chat,
}


def make_chat(
    model_config: Optional[str] = None,
    model_id: Optional[str] = None, 
    provider: Optional[str] = None,
    **kwargs
) -> BaseChatModel:
    """
    Create a chat model instance.
    
    Args:
        model_config: Name of predefined config from MODEL_CONFIGS (e.g., 'coding', 'planning')
        model_id: Override model ID (takes precedence over config)
        provider: Override provider (takes precedence over config)  
        **kwargs: Override any config parameters (temperature, max_new_tokens, etc.)
        
    Examples:
        # Use default model
        chat = make_chat()
        
        # Use predefined config for coding
        chat = make_chat("coding")
        
        # Override specific model
        chat = make_chat(model_id="microsoft/DialoGPT-medium")
        
        # Mix config with overrides
        chat = make_chat("planning", temperature=0.5)
        
        # Use different provider (when implemented)
        chat = make_chat("openai_gpt4")
    """
    
    # Start with default config
    config = MODEL_CONFIGS["default"].copy()
    
    # Apply named config if provided
    if model_config and model_config in MODEL_CONFIGS:
        config.update(MODEL_CONFIGS[model_config])
    elif model_config:
        raise ValueError(f"Unknown model config: {model_config}. Available: {list(MODEL_CONFIGS.keys())}")
    
    # Apply environment variable overrides ONLY if no specific config was requested
    # This allows HF_MODEL_ID to override the default, but preserves specialized configs
    if os.getenv("HF_MODEL_ID") and not model_config:
        config["model_id"] = os.getenv("HF_MODEL_ID")
    
    # Apply parameter overrides
    if model_id:
        config["model_id"] = model_id
    if provider:
        config["provider"] = provider
    config.update(kwargs)
    
    # Get the provider factory
    provider_name = config["provider"]
    if provider_name not in PROVIDER_FACTORIES:
        raise ValueError(f"Unknown provider: {provider_name}. Available: {list(PROVIDER_FACTORIES.keys())}")
    
    # Create and return the chat model
    factory = PROVIDER_FACTORIES[provider_name]
    return factory(config)


def list_available_models() -> Dict[str, Dict[str, Any]]:
    """
    Return all available model configurations.
    
    Returns:
        Dict mapping config names to their configurations
    """
    return MODEL_CONFIGS.copy()


def get_model_info(model_config: str) -> Dict[str, Any]:
    """
    Get information about a specific model configuration.
    
    Args:
        model_config: Name of the model configuration
        
    Returns:
        Dictionary with model configuration details
        
    Raises:
        ValueError: If model_config doesn't exist
    """
    if model_config not in MODEL_CONFIGS:
        raise ValueError(f"Unknown model config: {model_config}. Available: {list(MODEL_CONFIGS.keys())}")
    
    config = MODEL_CONFIGS[model_config].copy()
    
    # Add some metadata
    config["available"] = config["provider"] == "huggingface"  # Only HF is currently implemented
    
    if config["provider"] == "huggingface":
        config["description"] = _get_hf_model_description(config["model_id"])
    else:
        config["description"] = f"{config['provider'].title()} model (not yet implemented)"
    
    return config


def _get_hf_model_description(model_id: str) -> str:
    """Get a description for a Hugging Face model."""
    descriptions = {
        "meta-llama/Meta-Llama-3.1-8B-Instruct": "General-purpose instruction-following model, good balance of capability and speed",
        "meta-llama/Meta-Llama-3.1-70B-Instruct": "Large model with enhanced reasoning capabilities, best for complex planning",
        "bigcode/starcoder2-15b": "Code-specialized model optimized for programming tasks",
        "mistralai/Mistral-7B-Instruct-v0.1": "Efficient general-purpose model with good instruction following",
        "codellama/CodeLlama-13b-Instruct-hf": "Code-focused Llama variant, excellent for programming",
        "google/gemma-7b-it": "Google's instruction-tuned model with strong reasoning abilities",
    }
    return descriptions.get(model_id, f"Hugging Face model: {model_id}")


def print_available_models():
    """Print a formatted list of all available models."""
    print("Available Model Configurations:")
    print("=" * 50)
    
    for name, config in MODEL_CONFIGS.items():
        status = "✅ Available" if config["provider"] == "huggingface" else "🚧 Placeholder"
        provider = config["provider"].title()
        model_id = config["model_id"]
        temp = config["temperature"]
        
        print(f"\n{name}:")
        print(f"  Status: {status}")
        print(f"  Provider: {provider}")
        print(f"  Model: {model_id}")
        print(f"  Temperature: {temp}")
        
        if config["provider"] == "huggingface":
            print(f"  Description: {_get_hf_model_description(model_id)}")
        
    print(f"\nUsage Examples:")
    print(f"  chat = make_chat()                    # Use default model")
    print(f"  chat = make_chat('coding')            # Use code-specialized model")  
    print(f"  chat = make_chat('planning')          # Use large model for planning")
    print(f"  chat = make_chat(model_id='custom')   # Override model directly")


def make_chat_for_language(
    language: str,
    task: str = "coding",
    model_config: Optional[str] = None,
    **kwargs
) -> BaseChatModel:
    """
    Create a chat model optimized for a specific programming language and task.
    
    Args:
        language: Programming language (python, javascript, csharp, etc.)
        task: Type of task (coding, planning, architecture, etc.)
        model_config: Override model config selection
        **kwargs: Additional parameters to pass to make_chat
        
    Returns:
        BaseChatModel instance optimized for the language/task
        
    Examples:
        # Get best model for Python coding
        chat = make_chat_for_language("python", "coding")
        
        # Get best model for JavaScript with custom temperature
        chat = make_chat_for_language("javascript", "coding", temperature=0.05)
        
        # Force specific model config
        chat = make_chat_for_language("python", "coding", model_config="openai_gpt4")
    """
    
    if not model_config:
        model_config = select_best_model_for_language(language, task)
    
    return make_chat(model_config, **kwargs)


# Backward compatibility function (old signature)
def make_chat_legacy(model_id: str = None, *, temperature=0.2, max_new_tokens=1024):
    """Legacy function signature for backward compatibility."""
    return make_chat(model_id=model_id, temperature=temperature, max_new_tokens=max_new_tokens)
