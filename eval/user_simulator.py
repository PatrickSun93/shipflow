import os
import requests
import json

class UserSimulator:
    def __init__(self, persona_description):
        self.persona_description = persona_description

        # Support either OpenAI-compatible API (like DeepSeek) or Ollama
        self.api_base = os.environ.get("SIMULATOR_API_BASE", "https://api.deepseek.com")
        self.api_key = os.environ.get("SIMULATOR_API_KEY", "")
        self.model = os.environ.get("SIMULATOR_MODEL", "deepseek-chat")
        self.is_ollama = os.environ.get("SIMULATOR_IS_OLLAMA", "false").lower() == "true"

        self.conversation_history = [
            {
                "role": "system",
                "content": f"You are a user working with an AI development team to build a project. "
                           f"Your persona and goal are: {self.persona_description}. "
                           f"The AI will ask you questions to clarify requirements during the Discovery phase. "
                           f"Answer concisely and practically, as a real user would. Do not give long essays. "
                           f"If asked about something you haven't decided, make a reasonable, simple choice. "
                           f"Do not prefix your answers with your name or any label. Just reply naturally."
            }
        ]

    def answer_question(self, ai_question):
        """Sends the AI's question to the LLM and returns the simulated user's answer."""
        self.conversation_history.append({"role": "user", "content": ai_question})

        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "stream": False
        }

        headers = {}
        if not self.is_ollama:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["Content-Type"] = "application/json"
            endpoint = f"{self.api_base.rstrip('/')}/v1/chat/completions"
        else:
            endpoint = f"{self.api_base.rstrip('/')}/api/chat"

        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            result = response.json()

            if self.is_ollama:
                answer = result.get("message", {}).get("content", "").strip()
            else:
                answer = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

            # Store the answer in history
            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer

        except Exception as e:
            print(f"[Simulator Error] Failed to generate answer: {e}")
            if response is not None:
                print(f"[Simulator Error] Response: {response.text}")
            # Fallback answer to keep the evaluation moving
            fallback = "Let's keep it simple for now, whatever you think is standard practice."
            self.conversation_history.append({"role": "assistant", "content": fallback})
            return fallback

if __name__ == "__main__":
    # Test
    sim = UserSimulator("I want to build a newsletter platform. Start simple, MVP focused.")
    print("AI: What payment provider do you want to use?")
    ans = sim.answer_question("What payment provider do you want to use?")
    print(f"Simulator: {ans}")
