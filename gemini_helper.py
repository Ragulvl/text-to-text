"""
Gemini API Helper Module
This module handles all interactions with the Google Gemini API.
"""

import google.generativeai as genai
import time
import re
from typing import Optional


class GeminiHelper:
    """
    A helper class to interact with Google Gemini API for text generation tasks.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Gemini API client.
        
        Args:
            api_key (str): Your Google Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        # Store available models for fallback
        self.available_models = []
        self.current_model_name = 'gemini-pro'
        self.model = genai.GenerativeModel(self.current_model_name)
        
        # Pre-fetch available models for fallback
        try:
            models = genai.list_models()
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    # Store model name without 'models/' prefix
                    model_name = model.name.replace('models/', '')
                    self.available_models.append(model_name)
        except Exception:
            # If we can't list models, just use gemini-pro
            pass
    
    def generate_text(self, user_text: str, operation: str) -> Optional[str]:
        """
        Generate text based on the user's input and selected operation.
        
        Args:
            user_text (str): The input text from the user
            operation (str): The operation to perform ('Summarize', 'Rephrase', or 'Expand')
        
        Returns:
            str: The generated text, or None if an error occurred
        """
        # Create a prompt based on the selected operation
        if operation == "Summarize":
            prompt = f"Please provide a concise summary of the following text:\n\n{user_text}"
        elif operation == "Rephrase":
            prompt = f"Please rephrase the following text while maintaining its original meaning:\n\n{user_text}"
        elif operation == "Expand":
            prompt = f"Please expand the following text with more details and explanations:\n\n{user_text}"
        else:
            return "Invalid operation selected."
        
        # Try to generate with current model, fallback to other models if needed
        models_to_try = [self.current_model_name] + [m for m in self.available_models if m != self.current_model_name]
        
        for model_name in models_to_try:
            try:
                # Create model instance
                model = genai.GenerativeModel(model_name)
                # Generate the response
                response = model.generate_content(prompt)
                # Update current model if we switched
                if model_name != self.current_model_name:
                    self.current_model_name = model_name
                    self.model = model
                # Return the generated text
                return response.text
            except Exception as e:
                # If this model failed, try the next one
                error_msg = str(e)
                
                # Handle quota/rate limit errors (429)
                if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                    # Extract retry delay if available
                    retry_match = re.search(r'retry in ([\d.]+)s', error_msg, re.IGNORECASE)
                    if retry_match:
                        retry_seconds = float(retry_match.group(1))
                        retry_minutes = int(retry_seconds // 60)
                        retry_secs = int(retry_seconds % 60)
                        if retry_minutes > 0:
                            wait_time = f"{retry_minutes} minute(s) and {retry_secs} second(s)"
                        else:
                            wait_time = f"{retry_secs} second(s)"
                    else:
                        wait_time = "a few minutes"
                    
                    return (f"⚠️ QUOTA EXCEEDED\n\n"
                           f"You've exceeded your free tier quota for the Gemini API.\n\n"
                           f"Please wait {wait_time} before trying again, or:\n"
                           f"• Check your usage at: https://ai.dev/usage?tab=rate-limit\n"
                           f"• Learn about quotas: https://ai.google.dev/gemini-api/docs/rate-limits\n"
                           f"• Consider upgrading your plan if you need more requests")
                
                # Handle 404/model not found errors
                if "404" in error_msg or "not found" in error_msg.lower():
                    # Model not found, try next one
                    continue
                
                # Handle other API errors
                if "403" in error_msg or "permission" in error_msg.lower():
                    return (f"⚠️ PERMISSION ERROR\n\n"
                           f"Your API key may not have access to this model or the API.\n"
                           f"Please check:\n"
                           f"• Your API key is valid\n"
                           f"• You have access to Gemini API\n"
                           f"• Your API key permissions are correct")
                
                # For other errors, return a cleaner message
                return f"Error: {error_msg}"
        
        # If all models failed
        return "Error: Could not generate text with any available model. Please check your API key and model access."

