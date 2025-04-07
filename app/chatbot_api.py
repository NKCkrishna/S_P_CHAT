import os
import google.generativeai as genai
from dotenv import load_dotenv
import sys
from pathlib import Path
import time

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

# List available models
try:
    models = genai.list_models()
    print("Available models:")
    for m in models:
        print(f"- {m.name}")
        print(f"  Supported methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {str(e)}")

def get_chatbot_response(prompt, context=None):
    """Get a response from the Gemini model."""
    try:
        # Create the model with the latest version
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Prepare system prompt
        system_prompt = """You are SustainifyAI, an expert assistant specializing in sustainability, agriculture, and environmental topics. 
        Provide helpful, accurate, and practical advice about:
        - Sustainable practices
        - Agricultural techniques
        - Energy efficiency
        - Environmental conservation
        - Weather and climate impacts
        
        Keep responses clear, informative, and focused on sustainability."""
        
        # Combine prompts
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        
        # Generate response with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=1024,
                    )
                )
                
                if response and response.text:
                    return response.text.strip()
                else:
                    print(f"Attempt {attempt + 1}: Empty response")
                    if attempt == max_retries - 1:
                        return "I apologize, but I couldn't generate a response. Please try asking your question in a different way."
                    time.sleep(1)
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(1)
            
    except Exception as e:
        print(f"Error in Gemini API: {str(e)}")
        return "I apologize, but I'm having trouble connecting to the AI service right now. Please try again later." 