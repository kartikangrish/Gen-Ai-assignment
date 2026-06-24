import requests
import json

class LLMAPIClient:
    def __init__(self, api_endpoint: str, api_key: str = None):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def send_query(self, user_input: str, temperature: float = 0.7, system_prompt: str = None):
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "messages": [{"role": "user", "content": user_input}],
            "temperature": temperature,
            "max_tokens": 1024
        }

        if system_prompt:
            payload["messages"].insert(0, {"role": "system", "content": system_prompt})

        try:
            print(f"\nSending request to {self.api_endpoint}")
            print(f"Temperature: {temperature}")
            print(f"Query: {user_input}")
            print("-" * 70)

            response = requests.post(
                self.api_endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {str(e)}")
            return {"error": str(e)}

    def extract_assistant_reply(self, response):
        if "error" in response:
            return f"Error: {response['error']}"

        try:
            if "content" in response.get("choices", [{}])[0]:
                return response["choices"][0]["content"][0]["text"]
            return "No response content found"
        except (KeyError, IndexError, TypeError) as e:
            return f"Failed to parse response: {str(e)}"


def main():
    print("=" * 70)
    print("Exercise 2: Calling LLM via API")
    print("=" * 70)
    print()

    API_ENDPOINT = "https://api.anthropic.com/v1/messages"
    API_KEY = "your-api-key-here"

    client = LLMAPIClient(API_ENDPOINT, API_KEY)

    query1 = "What is the importance of embeddings in machine learning?"
    print("Query 1:")
    print(f"'{query1}'")
    response1 = client.send_query(query1, temperature=0.7)

    print("\n✓ Full Response 1:")
    print(json.dumps(response1, indent=2))

    assistant_reply1 = client.extract_assistant_reply(response1)
    print("\n✓ Assistant Reply 1:")
    print(assistant_reply1)

    query2 = "Explain similarity scoring in NLP with a simple example"
    print("\n" + "=" * 70)
    print("Query 2 (Lower temperature = more deterministic):")
    print(f"'{query2}'")
    response2 = client.send_query(query2, temperature=0.3)

    print("\n✓ Full Response 2:")
    print(json.dumps(response2, indent=2))

    assistant_reply2 = client.extract_assistant_reply(response2)
    print("\n✓ Assistant Reply 2:")
    print(assistant_reply2)

    print("\n" + "=" * 70)
    print("Comparison:")
    print("=" * 70)
    print("Temperature 0.7 (Query 1): More creative, varied responses")
    print("Temperature 0.3 (Query 2): More focused, consistent responses")
    print()


if __name__ == "__main__":
    main()
