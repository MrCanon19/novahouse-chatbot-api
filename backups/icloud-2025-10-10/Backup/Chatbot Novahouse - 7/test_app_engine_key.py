#!/usr/bin/env python3
"""
Test the specific OpenAI API key from app.yaml
"""

import requests

def test_app_engine_key():
    """Test the API key from app.yaml"""
    
    # Key from app.yaml
    api_key = "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"
    
    print(f"✅ Testing App Engine API Key: {api_key[:20]}...")
    
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
            print("✅ App Engine OpenAI API Key works!")
            print(f"Response: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ OpenAI API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    test_app_engine_key()

