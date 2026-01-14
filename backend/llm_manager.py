import requests
import json

class LLMManager:
    def __init__(self, base_url="http://localhost:11434", model="llama3.2"):
        self.base_url = base_url
        self.model = model

    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generates a response from the Ollama model.
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return f"Error: {str(e)}"

# Example usage (for testing purposes)
if __name__ == "__main__":
    llm = LLMManager()
    print(llm.generate_response("Hello, who are you?"))
