"""
LLM client utilities for interacting with AI models
"""
import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()


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
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
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
