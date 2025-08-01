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

def find_research_gap(paper_summaries):
    combined_text = ""
    for i, paper in enumerate(paper_summaries):
        combined_text += f"\nPaper {i+1} Title: {paper['title']}\nSummary: {paper['summary']}\n"
        
    prompt = f"""
You are a research analyst. Based on the following collection of paper summaries, identify:

1. A common research gap or limitation
2. Why this gap is important
3. Suggest what a student can explore to address this gap

Summaries:
{combined_text}

Respond in 3 short paragraphs.
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


def suggest_methodology_based_on_gap(topic, gap_description):
    prompt = f"""
You are an AI research mentor. A student is exporing the follwing topic:

Research Topic: {topic}

Based on this gap in existing research:
{gap_description}

Suggest the following:
1. Methodology or approach rhey can follow
2. Tools,models, or datasets they can use
3. A clean, small plan to carry out research

Respond in Markdown format, clearly and simply.
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