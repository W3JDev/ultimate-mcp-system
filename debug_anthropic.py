
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

try:
    print("Attempting to init Anthropic...")
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("✅ Client initialized!")
    
    # Test latest Sonnet models
    models_to_test = [
        "claude-3-5-sonnet-20241022",  # Latest Sonnet v2
        "claude-3-5-sonnet-20240620",  # Original Sonnet 3.5
        "claude-3-sonnet-20240229",    # Sonnet 3
        "claude-3-5-haiku-20241022",   # Latest Haiku
        "claude-3-haiku-20240307"      # Original Haiku
    ]
    
    for model in models_to_test:
        try:
            print(f"\nTesting {model}...")
            response = client.messages.create(
                model=model,
                max_tokens=50,
                messages=[{"role": "user", "content": "Hello"}]
            )
            print(f"✅ {model} works! Response: {response.content[0].text[:50]}...")
            break
        except Exception as e:
            print(f"❌ {model} failed: {str(e)[:100]}...")
    print(f"✅ Success! Response: {message.content[0].text}")
except Exception as e:
    print(f"❌ Failed: {e}")
