import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("AIzaSyCTo6dBRtJCapTUzlgqpv2XZ9om4roiCFw"))

model = genai.GenerativeModel("gemini-pro")

def ai_scam_analysis(text, rule_result):
    prompt = f"""
You are a cybersecurity assistant.

Analyze the following job offer and explain:
- Why it may or may not be a scam
- Mention specific suspicious patterns
- Give user-friendly advice

Job Offer:
{text}

Rule-based findings:
{rule_result}

Write a clear paragraph (5–7 lines).
"""

    response = model.generate_content(prompt)
    return response.text.strip()