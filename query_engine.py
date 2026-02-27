import os
import streamlit as st
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

claude_client = Anthropic(api_key=get_secret("ANTHROPIC_API_KEY"))
openai_client = OpenAI(api_key=get_secret("OPENAI_API_KEY"))

def ask_claude(query):
    message = claude_client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": query}]
    )
    return message.content[0].text

def ask_chatgpt(query):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content

def check_if_mentioned(response_text, restaurant_name):
    return restaurant_name.lower() in response_text.lower()

def run_visibility_check(restaurant_name, city, cuisine_type):
    queries = [
        f"What are the best {cuisine_type} restaurants in {city}?",
        f"Where should I eat {cuisine_type} food in {city}?",
        f"Top rated {cuisine_type} restaurants in {city}",
    ]
    
    results = []
    
    for query in queries:
        claude_response = ask_claude(query)
        claude_mentioned = check_if_mentioned(claude_response, restaurant_name)

        chatgpt_response = ask_chatgpt(query)
        chatgpt_mentioned = check_if_mentioned(chatgpt_response, restaurant_name)

        results.append({
            "query": query,
            "claude_response": claude_response,
            "claude_mentioned": claude_mentioned,
            "chatgpt_response": chatgpt_response,
            "chatgpt_mentioned": chatgpt_mentioned,
        })
    
    return results