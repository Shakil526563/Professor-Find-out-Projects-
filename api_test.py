#!/usr/bin/env python
"""
Quick API key test
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_keys():
    print("=== API Key Test ===")
    
    tavily_key = os.getenv('TAVILY_API_KEY')
    groq_key = os.getenv('GROQ_API_KEY')
    
    print(f"Tavily API Key: {'✓ Present' if tavily_key else '✗ Missing'}")
    print(f"Groq API Key: {'✓ Present' if groq_key else '✗ Missing'}")
    
    if tavily_key:
        print(f"Tavily key: {tavily_key[:15]}...")
    if groq_key:
        print(f"Groq key: {groq_key[:15]}...")
    
    # Test Tavily API
    if tavily_key:
        print("\n=== Testing Tavily API ===")
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": tavily_key,
                "query": "test professors MIT",
                "search_depth": "basic",
                "include_answer": False,
                "include_images": False,
                "max_results": 3
            }
            
            response = requests.post(url, json=payload, timeout=10)
            print(f"Tavily Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"✓ Tavily API working! Got {len(results)} results")
            else:
                print(f"✗ Tavily API error: {response.text}")
                
        except Exception as e:
            print(f"✗ Tavily API exception: {e}")
    
    # Test Groq API
    if groq_key:
        print("\n=== Testing Groq API ===")
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": "Say 'Hello, API test successful!'"}
                ],
                "temperature": 0.1,
                "max_tokens": 50
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            print(f"Groq Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                message = data['choices'][0]['message']['content']
                print(f"✓ Groq API working! Response: {message}")
            else:
                print(f"✗ Groq API error: {response.text}")
                
        except Exception as e:
            print(f"✗ Groq API exception: {e}")

if __name__ == "__main__":
    test_api_keys()
