#!/usr/bin/env python3
"""
Nano Banana BCG Image Generator Script (PNG/JPEG)
Uses Google Generative AI (Gemini 3.1 Flash Image) to generate consulting-style presentation slides.
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Try to import google.generativeai, install if missing
try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
except ImportError:
    print("Error: `google-generativeai` package not found.", file=sys.stderr)
    print("Please install it: pip install google-generativeai python-dotenv", file=sys.stderr)
    sys.exit(1)

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
ENV_FILE = SKILL_DIR / ".env"
SYSTEM_TEMPLATE_PATH = SKILL_DIR / "assets" / "SYSTEM_TEMPLATE"

def load_environment():
    """Load API key from .env or environment variables."""
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment or .env file.", file=sys.stderr)
        sys.exit(1)
    return api_key

def load_system_prompt():
    """Read the system prompt template."""
    if not SYSTEM_TEMPLATE_PATH.exists():
        print(f"Warning: System template not found at {SYSTEM_TEMPLATE_PATH}. Using default.", file=sys.stderr)
        return "You are an expert visual designer. Generate professional consulting slides."
    return SYSTEM_TEMPLATE_PATH.read_text(encoding="utf-8")

def generate_image(prompt: str, api_key: str, resolution: str = "4K"):
    """Call Gemini API to generate an image."""
    genai.configure(api_key=api_key)
    
    # Use Gemini 3.1 Flash Image for high-quality generation
    model = genai.GenerativeModel('gemini-3.1-flash-image-preview')
    
    system_prompt = load_system_prompt()
    full_prompt = f"{system_prompt}\n\nUSER REQUEST: {prompt}\n\nRESOLUTION: {resolution}\nFORMAT: 16:9 Presentation Slide"
    
    # Configuration for image generation if supported, otherwise part of prompt
    # Note: Gemini 3 might accept generation_config for aspect_ratio
    generation_config = {
        "temperature": 0.4, # Lower temperature for more adherence to consulting style
    }

    try:
        print("Sending request to Gemini 3.1 Flash Image...")
        response = model.generate_content(
            full_prompt, 
            generation_config=generation_config
        )
        
        # Extract image data
        if not response.parts:
            print("Error: Empty response from API.", file=sys.stderr)
            if response.prompt_feedback:
                 print(f"Prompt feedback: {response.prompt_feedback}", file=sys.stderr)
            sys.exit(1)

        for part in response.parts:
            if part.inline_data and part.inline_data.data:
                # Found image data
                return part.inline_data.data
        
        # If we get here, no image was found
        print("Error: No image data found in response.", file=sys.stderr)
        print(f"Response text (if any): {response.text}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Error generating content: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate BCG-style slides using Gemini 3.1 Flash.")
    parser.add_argument("--prompt", required=True, help="Description of the slide/diagram to generate.")
    parser.add_argument("--filename", default="output.png", help="Output filename (e.g., slide.png).")
    parser.add_argument("--resolution", default="4K", help="Target resolution hint.")
    
    args = parser.parse_args()
    
    api_key = load_environment()
    
    print(f"Generating consulting slide for: '{args.prompt}'...")
    image_data = generate_image(args.prompt, api_key, args.resolution)
    
    # Handle filename extension
    output_path = Path(args.filename)
    if output_path.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
        print(f"Note: Changing extension to .png for image output.")
        output_path = output_path.with_suffix(".png")
        
    try:
        # write_bytes for binary data
        output_path.write_bytes(image_data)
        print(f"Success! Saved to {output_path.absolute()}")
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
