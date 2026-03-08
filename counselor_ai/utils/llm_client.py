"""
LLM client utilities for interacting with AI models
"""
import os
from typing import Optional, List, Dict, Any, Union
from dotenv import load_dotenv

load_dotenv()

# Try importing OpenAI
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def create_llm_client(
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    use_local: Optional[bool] = None
) -> Union['LLMClient', 'LocalLLMClient']:
    """
    Factory function to create appropriate LLM client
    
    Args:
        model: Model name to use
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        use_local: Force local model (True) or OpenAI (False). 
                   If None, auto-detect based on API key availability
    
    Returns:
        LLMClient or LocalLLMClient instance
    """
    # Check environment variable for preference
    if use_local is None:
        use_local_env = os.getenv("USE_LOCAL_MODEL", "false").lower()
        use_local = use_local_env in ["true", "1", "yes"]
    
    # If not explicitly requesting local, check for OpenAI API key
    if not use_local:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key" and OPENAI_AVAILABLE:
            print("Using OpenAI API")
            return LLMClient(model=model, temperature=temperature, max_tokens=max_tokens)
    
    # Default to local model
    print("Using local LLM model")
    from counselor_ai.utils.local_llm_client import LocalLLMClient
    return LocalLLMClient(model=model, temperature=temperature, max_tokens=max_tokens)


class LLMClient:
    """Client for interacting with LLM APIs"""
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize LLM client
        
        Args:
            model: Model to use (default from env or gpt-4-turbo-preview)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI library not installed. "
                "Install with: pip install openai\n"
                "Or use local models by setting USE_LOCAL_MODEL=true in .env"
            )
        
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == "your_openai_api_key":
            raise ValueError(
                "OPENAI_API_KEY not found or invalid in environment variables.\n"
                "Get your API key from: https://platform.openai.com/api-keys\n"
                "Or use a local model by setting USE_LOCAL_MODEL=true in .env"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv("DEFAULT_MODEL", "gpt-4-turbo-preview")
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a completion from the LLM
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated text response
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
        )
        
        return response.choices[0].message.content
    
    def generate_structured_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a structured completion (e.g., JSON)
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            response_format: Expected response format
            
        Returns:
            Generated structured response
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        
        # Add response format if using newer models
        if response_format and "gpt-4" in self.model:
            kwargs["response_format"] = response_format
        
        response = self.client.chat.completions.create(**kwargs)
        
        return response.choices[0].message.content
    
    def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response in a multi-turn conversation
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated response
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
        )
        
        return response.choices[0].message.content
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        
        return response.data[0].embedding


class PromptTemplate:
    """Template for constructing prompts"""
    
    def __init__(self, template: str):
        """
        Initialize with a template string
        
        Args:
            template: Template string with {variable} placeholders
        """
        self.template = template
    
    def format(self, **kwargs) -> str:
        """
        Format the template with provided variables
        
        Args:
            **kwargs: Variables to substitute in template
            
        Returns:
            Formatted prompt string
        """
        return self.template.format(**kwargs)
