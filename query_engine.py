import os
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

claude_client = Anthropic()
openai_client = OpenAI()


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
        print(f"\nAsking: {query}")

        claude_response = ask_claude(query)
        claude_mentioned = check_if_mentioned(claude_response, restaurant_name)
        print(f"Claude mentioned {restaurant_name}: {claude_mentioned}")

        chatgpt_response = ask_chatgpt(query)
        chatgpt_mentioned = check_if_mentioned(
            chatgpt_response, restaurant_name)
        print(f"ChatGPT mentioned {restaurant_name}: {chatgpt_mentioned}")

        results.append({
            "query": query,
            "claude_response": claude_response,
            "claude_mentioned": claude_mentioned,
            "chatgpt_response": chatgpt_response,
            "chatgpt_mentioned": chatgpt_mentioned,
        })

    return results


if __name__ == "__main__":
    restaurant_name = "14 Prime"
    city = "Jacksonville"
    cuisine_type = "Steak"

    print(f"Running visibility check for: {restaurant_name} in {city}")
    results = run_visibility_check(restaurant_name, city, cuisine_type)

    print("\n--- SUMMARY ---")
    for r in results:
        print(f"\nQuery: {r['query']}")
        print(f"  Claude mentioned it: {r['claude_mentioned']}")
        print(f"  ChatGPT mentioned it: {r['chatgpt_mentioned']}")
