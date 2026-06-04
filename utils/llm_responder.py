import os
import markdown
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Try loading .env variables
load_dotenv()

def call_llm_api(system_prompt: str, user_prompt: str, severity: str, confidence: float) -> str:
    """
    Calls the Google Gemini LLM API with the specified system and user prompts.
    Returns an HTML string to be rendered in the chat UI.
    """
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        return "<p><em>Error: GEMINI_API_KEY environment variable is not set. Please add it to your .env file or environment variables to enable AI responses.</em></p>"
    
    try:
        # Initialize Gemini Client using new google.genai SDK
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Generation configuration
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            top_p=0.8,
            max_output_tokens=800,
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=user_prompt,
            config=config
        )
        
        # The LLM returns Markdown. Convert it to HTML for our chat UI.
        md_text = response.text
        html_content = markdown.markdown(md_text, extensions=['extra', 'nl2br'])
        
        # Add a subtle confidence badge if you wish
        pct = int(confidence * 100)
        badge_cls = "conf-high" if pct >= 70 else ("conf-medium" if pct >= 45 else "conf-low")
        badge_html = f'<span class="confidence-badge {badge_cls}">~{pct}% AI Confidence</span>'
        
        # Severity strip
        severity_colors = {
            "emergency": ("🚨", "strip-emergency"),
            "moderate": ("⚠️", "strip-moderate"),
            "mild": ("💬", "strip-mild"),
        }
        icon, strip_cls = severity_colors.get(severity, ("💬", "strip-mild"))
        
        # Return cleanly structured component
        final_html = f'''<div class="chat-response">
  <div class="severity-strip {strip_cls}">{icon} {badge_html}</div>
  <div class="chat-body llm-body">{html_content}</div>
</div>'''
        
        return final_html

    except Exception as e:
        print(f"LLM Error: {e}")
        return f"<p><em>AI System Temporarily Unavailable: {str(e)}</em></p>"
