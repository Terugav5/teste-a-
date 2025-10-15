import requests
import os
import json

def call_gemini_api(prompt: str) -> str:
    """
    Calls the Google Gemini API with a given prompt.

    Args:
        prompt: The text prompt to send to the AI.

    Returns:
        The text response from the AI, or an error message.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set."

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key,
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
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Extract the text from the response
        response_json = response.json()
        text_response = response_json['candidates'][0]['content']['parts'][0]['text']
        return text_response

    except requests.exceptions.RequestException as e:
        return f"Error calling API: {e}"
    except (KeyError, IndexError) as e:
        return f"Error parsing response: {e}\nResponse body: {response.text}"


if __name__ == "__main__":
    # Example usage:
    # 1. Set your API key in your terminal:
    #    export GEMINI_API_KEY="YOUR_API_KEY_HERE"
    #
    # 2. Run the script:
    #    python gemini_agent.py

    user_prompt = "Explain how AI works in a few words"
    print(f"Sending prompt: '{user_prompt}'")

    ai_response = call_gemini_api(user_prompt)

    print("\nAI Response:")
    print(ai_response)