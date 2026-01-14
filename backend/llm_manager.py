import requests
import json

class LLMManager:
    def __init__(self, base_url="http://localhost:11434", model="llama3.2"):
        self.base_url = base_url
        self.model = model

    def generate_response(self, prompt: str, system_prompt: str = None, history: list = None) -> str:
        """
        Generates a response from the Ollama model, including history and system prompt.
        """
        url = f"{self.base_url}/api/chat" # Use /api/chat for better context handling
        
        # Build messages list
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if history:
            messages.extend(history)
            
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return f"Error: {str(e)}"

# Example usage (for testing purposes)
if __name__ == "__main__":
    llm = LLMManager()
    print(llm.generate_response("Hello, who are you?"))
