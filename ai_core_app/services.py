import json
import os

import requests


class VedaIntelligenceService:
    """
    Engine responsible for web research and curriculum adaptation using LLM APIs.
    Returns structured data matching the pedagogical criteria of Veda.
    """

    def __init__(self) -> None:
        # Fallback reading order: environment variables -> django settings
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")

    def research_and_curate_topic(
        self, topic: str, country: str, age: int, methodology: str
    ) -> dict:
        """
        Sends metadata to the AI, instructs it to simulate web research,
        and extracts pinpoint accurate topics for the target class.
        """
        # Build a highly precise system persona to ensure JSON schema conformity
        system_prompt = (
            f"You are Veda, an advanced AI specialized in international curriculum mapping and pedagogy.\n"
            f"Your goal is to research the web and curate content for the country: '{country}'.\n"
            f"Target Audience: Children aged {age} years old. You MUST strictly adapt vocabulary, depth, "
            f"and cognitive complexity to this specific age and its corresponding school grade.\n"
            f"Pedagogical Framework to apply: '{methodology}'.\n\n"
            f"CRITICAL: You must reply ONLY with a valid, clean JSON object. Do not wrap it in markdown code blocks like ```json. "
            f"The JSON structure must match this exact schema:\n"
            f"{{\n"
            f'  "refined_title": "A pedagogical name for the topic session",\n'
            f'  "key_learning_points": ["Point 1", "Point 2", "Point 3"],\n'
            f'  "lesson_content": "Detailed structured content ready for the teacher to deliver...",\n'
            f'  "suggested_activity": "Step-by-step activity tailored to the age group and chosen methodology",\n'
            f'  "multimedia_guidelines": {{\n'
            f'     "visuals": "Specific instructions on what type of images/infographics to look for",\n'
            f'     "videos": "Search keywords or content ideas for video resources"\n'
            f"  }}\n"
            f"}}"
        )

        user_prompt = f"Research, filter, and adapt the following topic: '{topic}'"

        # Routing logic based on which API Key is populated in your .env
        if self.openai_key:
            return self._call_openai(system_prompt, user_prompt)
        elif self.gemini_key:
            return self._call_gemini(system_prompt, user_prompt)
        else:
            raise ValueError(
                "No API credentials found for OpenAI or Gemini in your configuration."
            )

    def _call_openai(self, system_prompt: str, user_prompt: str) -> dict:
        url = "[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_key}",
        }
        payload = {
            "model": "gpt-4o",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            raw_text = response.json()["choices"][0]["message"]["content"]
            return json.loads(raw_text)
        except Exception as e:
            return {"error": True, "message": f"OpenAI Integration Error: {str(e)}"}

    def _call_gemini(self, system_prompt: str, user_prompt: str) -> dict:
        # Standard endpoint using Gemini 1.5 Flash (excellent and fast for structured extraction)
        url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=){self.gemini_key}"
        headers = {"Content-Type": "application/json"}

        # We concatenate prompts for Gemini while enforcing JSON schema via systemInstruction
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.3,
            },
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            raw_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(raw_text)
        except Exception as e:
            return {"error": True, "message": f"Gemini Integration Error: {str(e)}"}
