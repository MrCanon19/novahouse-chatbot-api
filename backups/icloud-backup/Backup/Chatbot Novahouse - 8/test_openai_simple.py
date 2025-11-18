#!/usr/bin/env python3
"""
Simple test OpenAI connection
"""

import os
import requests

def test_openai_direct():
    """Test OpenAI API directly"""
    
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test direct API call
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hello, test message"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ OpenAI API works!")
            print(f"Response: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ OpenAI API error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_openai_direct()

