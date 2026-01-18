import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini if key is present
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

async def analyze_reviews(text_content: str):
    """
    Analyzes the text content using an LLM to extract Pain Points and Hooks.
    """
    if not GEMINI_API_KEY:
        # Fallback for dev/testing if no key
        print("Warning: No GEMINI_API_KEY found. Returning mock data.")
        return {
            "complaints": [{"insight": "Missing API Key", "frequency": "high", "suggested_copy": "Please set GEMINI_API_KEY"}],
            "hooks": [{"insight": "Great Error Handling", "frequency": "high", "suggested_copy": "System expects keys"}]
        }

    try:
        # Truncate text if too long (Gemini 1.5 Flash has 1M context, but let's be safe/economical)
        # 100k chars is plenty for a MVP
        truncated_text = text_content[:100000]

        prompt = f"""
        You are a direct-response marketing expert. Analyze the following customer feedback/reviews for a product.
        
        Identify the top 3 'Recurring Complaints' (Pain Points) and the top 3 'Emotional Triggers' (Hooks).
        
        Return the response STRICTLY as a JSON object. Do not add any markdown formatting like ```json ... ```.
        The JSON schema is:
        {{
            "complaints": [{{"insight": "string", "frequency": "high/medium/low", "suggested_copy": "string"}}],
            "hooks": [{{"insight": "string", "frequency": "high/medium/low", "suggested_copy": "string"}}]
        }}

        Reviews/Content:
        {truncated_text}
        """
        
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        
        # Parse logic
        response_text = response.text.strip()
        # Remove markdown code blocks if present (Gemini sometimes adds them despite instruction)
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        return json.loads(response_text)

    except Exception as e:
        print(f"LLM Analysis Error: {e}")
        return {
            "complaints": [],
            "hooks": [],
            "error": str(e)
        }
