"""
Local LLM client using HuggingFace transformers
"""
import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Optional imports for local models
try:
    import torch
    from transformers import pipeline, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


class LocalLLMClient:
    """Client for local LLM models using HuggingFace transformers"""
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize Local LLM client
        
        Args:
            model: Model to use (default: TinyLlama/TinyLlama-1.1B-Chat-v1.0)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        """
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "transformers and torch are required for local models. "
                "Install with: pip install torch transformers accelerate"
            )
        
        self.model_name = model or os.getenv(
            "LOCAL_MODEL", 
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        )
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        print(f"Loading local model: {self.model_name}...")
        print("This may take a few minutes on first run...")
        
        # Initialize the pipeline
        try:
            # Use bfloat16 if available, otherwise float16
            torch_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float16
            
            self.pipe = pipeline(
                "text-generation",
                model=self.model_name,
                torch_dtype=torch_dtype,
                device_map="auto",
                trust_remote_code=True
            )
            
            self.tokenizer = self.pipe.tokenizer
            print(f"✓ Model {self.model_name} loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to CPU...")
            self.pipe = pipeline(
                "text-generation",
                model=self.model_name,
                device_map="cpu",
                trust_remote_code=True
            )
            self.tokenizer = self.pipe.tokenizer
    
    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a completion from the local LLM
        
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
        
        # Format using chat template if available
        try:
            formatted_prompt = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
        except Exception:
            # Fallback if chat template not available
            if system_prompt:
                formatted_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            else:
                formatted_prompt = f"User: {prompt}\n\nAssistant:"
        
        # Generate response
        outputs = self.pipe(
            formatted_prompt,
            max_new_tokens=max_tokens or self.max_tokens,
            do_sample=True,
            temperature=temperature or self.temperature,
            top_k=50,
            top_p=0.95,
            return_full_text=False
        )
        
        return outputs[0]["generated_text"].strip()
    
    def generate_structured_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a structured completion (e.g., JSON)
        Note: Local models may not follow JSON format as strictly as GPT
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            response_format: Expected response format (informational only for local models)
            
        Returns:
            Generated structured response
        """
        # Add JSON formatting instruction to prompt
        enhanced_prompt = f"{prompt}\n\nPlease respond in valid JSON format."
        return self.generate_completion(enhanced_prompt, system_prompt)
    
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
        try:
            formatted_prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
        except Exception:
            # Fallback formatting
            formatted_prompt = ""
            for msg in messages:
                role = msg["role"].capitalize()
                content = msg["content"]
                formatted_prompt += f"{role}: {content}\n\n"
            formatted_prompt += "Assistant:"
        
        outputs = self.pipe(
            formatted_prompt,
            max_new_tokens=max_tokens or self.max_tokens,
            do_sample=True,
            temperature=temperature or self.temperature,
            top_k=50,
            top_p=0.95,
            return_full_text=False
        )
        
        return outputs[0]["generated_text"].strip()
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for text (not implemented for local models by default)
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector (placeholder)
        """
        raise NotImplementedError(
            "Text embedding not implemented for local models. "
            "Use a dedicated embedding model or OpenAI API."
        )
