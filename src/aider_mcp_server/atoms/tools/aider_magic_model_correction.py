"""
Magic model correction tool for Aider MCP server.

This tool provides functionality to correct model names using an AI model.
It can take a potentially incorrect or ambiguous model name and suggest the
correct model name based on available models for a provider.
"""

import logging
import importlib
import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from ..logging import get_logger

logger = get_logger(__name__)

# Known model mappings for common providers
KNOWN_MODELS = {
    "openai": [
        "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", 
        "gpt-4-vision-preview", "gpt-4-32k", "gpt-3.5-turbo-16k"
    ],
    "anthropic": [
        "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307",
        "claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022", "claude-2.1", "claude-2.0",
        "claude-instant-1.2"
    ],
    "gemini": [
        "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-1.0-pro-vision",
        "gemini-2.5-pro-exp-03-25", "gemini-2.0-flash", "gemini-2.0-pro"
    ],
    "cohere": [
        "command", "command-r", "command-r-plus", "command-light", "command-nightly"
    ],
    "mistral": [
        "mistral-small", "mistral-medium", "mistral-large", "mistral-embed"
    ]
}

def get_available_models(provider: str) -> List[str]:
    """
    Get available models for a provider.
    
    Args:
        provider: Provider name
        
    Returns:
        List of available model names
    """
    # First check if we have a cached list of known models
    if provider.lower() in KNOWN_MODELS:
        return KNOWN_MODELS[provider.lower()]
    
    # Otherwise, try to get models from the provider's API
    # This is a placeholder - in a real implementation, you would
    # call the provider's API to get the list of models
    return []

def _call_ai_for_correction(provider: str, model: str, available_models: List[str], correction_model: str) -> str:
    """
    Use an AI model to correct a model name.
    
    Args:
        provider: Provider name
        model: Original model name
        available_models: List of available models for the provider
        correction_model: Model to use for the correction
        
    Returns:
        Corrected model name
    """
    try:
        # For demonstration, we'll use a simple string matching algorithm
        # In a real implementation, you would call an AI model API
        
        # Log the correction attempt
        logger.info(f"Attempting to correct model '{model}' for provider '{provider}'")
        logger.info(f"Available models: {available_models}")
        
        # Simple matching algorithm - find the closest match
        best_match = None
        best_score = 0
        
        for available_model in available_models:
            # Calculate a simple similarity score
            # (number of matching characters in sequence)
            score = 0
            for i in range(min(len(model), len(available_model))):
                if model[i].lower() == available_model[i].lower():
                    score += 1
                else:
                    break
            
            # Check if this is a better match
            if score > best_score:
                best_score = score
                best_match = available_model
        
        # If we found a match with a reasonable score, return it
        if best_match and best_score >= 3:  # At least 3 characters match
            logger.info(f"Corrected '{model}' to '{best_match}' (score: {best_score})")
            return best_match
        
        # If no good match, return the original model
        logger.info(f"No good match found for '{model}', keeping original")
        return model
        
    except Exception as e:
        logger.error(f"Error in AI correction: {e}")
        return model

def magic_model_correction(provider: str, model: str, correction_model: str) -> str:
    """
    Correct a model name using a correction AI model if needed.

    Args:
        provider: Provider name
        model: Original model name
        correction_model: Model to use for the correction, e.g. "gemini/gemini-2.5-pro-exp-03-25"

    Returns:
        Corrected model name
    """
    try:
        # Log the request
        logger.info(f"Magic model correction request:")
        logger.info(f"  Provider: {provider}")
        logger.info(f"  Model: {model}")
        logger.info(f"  Correction model: {correction_model}")
        
        # Get available models for the provider
        available_models = get_available_models(provider)
        
        # If the model is already in the list of available models, return it
        if model in available_models:
            logger.info(f"Model '{model}' is already valid for provider '{provider}'")
            return model
        
        # If we have available models, try to correct the model name
        if available_models:
            corrected_model = _call_ai_for_correction(
                provider, model, available_models, correction_model
            )
            
            # If the correction is different from the original, log it
            if corrected_model != model:
                logger.info(f"Corrected model name from '{model}' to '{corrected_model}'")
            
            return corrected_model
        
        # If we don't have available models, just return the original
        logger.warning(f"No available models found for provider '{provider}', keeping original model name")
        return model
        
    except Exception as e:
        logger.error(f"Error in model correction: {e}")
        return model
