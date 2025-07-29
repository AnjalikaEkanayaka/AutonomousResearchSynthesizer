import os
import requests
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def summarize_paper_with_gemini(title, summary):
    prompt = f"""
You are an expert research assistant. A student is reading this paper titled:

Title: {title}

Abstract:
{summary}

Extract the following clearly and concisely:
1. Method (how the student was done)
2.Results (what the student found)
3. Conclusion (final takeaway)
Respond in Markdown format.
"""
    
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": gemini_api_key
    }   
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f" Gemini API failed ({response.status_code})"
    except Exception as e:
        return f" Error: {str(e)}"