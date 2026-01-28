import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_translate():
    print("Testing /translate...")
    payload = {
        "text": "How are you doing?",
        "direction": "en_to_pidgin",
        "variant": "ghana"
    }
    try:
        response = requests.post(f"{BASE_URL}/translate", json=payload)
        response.raise_for_status()
        print("Success:", json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Failed: {e}")
        return None

def test_tts(text):
    print("\nTesting /tts...")
    payload = {
        "text": text,
        "variant": "ghana"
    }
    try:
        response = requests.post(f"{BASE_URL}/tts", json=payload)
        response.raise_for_status()
        print("Success:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Failed: {e}")

def test_stats():
    print("\nTesting /analytics/stats...")
    try:
        response = requests.get(f"{BASE_URL}/analytics/stats")
        response.raise_for_status()
        print("Success:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    result = test_translate()
    start_text = result.get('translated', 'No translation') if result else "Test"
    test_tts(start_text)
    test_stats()
