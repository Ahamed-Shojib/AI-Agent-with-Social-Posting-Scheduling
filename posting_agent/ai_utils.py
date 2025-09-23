from google import genai
from google.genai import types


GEMINI_API_KEY = "oidfh9efoj3rpjfd9dvdd"

def generate_hashtags(text_content: str) -> list[str]:
    
    if not text_content:
        return []

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        system_instruction = (
            "You are a social media expert. Analyze the user's post text and "
            "generate exactly 4 highly relevant and engaging hashtags. "
            "Output ONLY the hashtags, separated by commas, with no other text, "
            "explanation, or line breaks. Each hashtag must start with '#'."
        )
        
        prompt = f"Generate 4 relevant hashtags for this post: '{text_content}'"

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        # Process the raw text response
        raw_hashtags = response.text.strip()
        hashtags = [
            tag.strip() for tag in raw_hashtags.split(',') 
            if tag.strip().startswith('#')
        ]
        
        return hashtags if hashtags else []

    except Exception as e:
        print(f"Gemini API Error: {e}") 
        return ['#AI_Error', '#CheckAPIKey', '#Gemini']