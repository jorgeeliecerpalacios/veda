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
        Sends metadata to the AI or triggers a local mock fallback if no API keys are present.
        """
        system_prompt = (
            "You are Veda, an advanced AI specialized in international curriculum mapping and pedagogy...\n"
            # (El resto de tu system prompt se mantiene igual...)
        )
        user_prompt = f"Research, filter, and adapt the following topic: '{topic}'"

        # ROUTING OR MOCK FALLBACK
        if self.openai_key:
            return self._call_openai(system_prompt, user_prompt)
        elif self.gemini_key:
            return self._call_gemini(system_prompt, user_prompt)
        else:
            # INTERCERCETAMOS AQUÍ: Mock inteligente para desarrollo local gratuito
            return self._generate_mock_response(topic, country, age, methodology)

    def _generate_mock_response(
        self, topic: str, country: str, age: int, methodology: str
    ) -> dict:
        """Devuelve un objeto estructurado simulando la respuesta exacta del LLM"""
        return {
            "refined_title": f"Exploring {topic} via {methodology}",
            "key_learning_points": [
                f"Core foundations of {topic} adapted for {age} year olds.",
                f"Contextual applications conforming to {country} educational guidelines.",
                f"Interactive experimentation based on {methodology} principles.",
            ],
            "lesson_content": (
                f"This is a curated educational module for '{topic}'. In {country}, students at this level "
                f"approach this via {methodology}. The focus is on tactile learning and core vocabulary "
                f"suitable for a target audience of {age} years old. (Veda Sandbox Engine active)."
            ),
            "suggested_activity": f"Group dynamic: Build a conceptual model or run a simulation of '{topic}' using local classroom resources.",
            "multimedia_guidelines": {
                "visuals": f"Infographics displaying basic {topic} dynamics with high-contrast elements.",
                "videos": f"Animated 3-minute clips explaining {topic} without dense academic jargon.",
            },
        }

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
        import json
        import traceback

        from google import genai
        from google.genai import types

        try:
            clean_key = self.gemini_key.strip()

            # 1. Usamos el cliente exacto del snippet de Google
            client = genai.Client(api_key=clean_key)

            # 2. Mantenemos nuestra configuración que fuerza el JSON
            # Configuración optimizada para velocidad (sin bloqueos de espera)
            config = types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json",
                system_instruction=system_prompt,
                # Forzamos a que no gaste tiempo en el proceso de "thinking" extenso
                thinking_config=types.ThinkingConfig(
                    thinking_budget=0
                )
            )

            # 3. ¡AQUÍ ESTÁ LA MAGIA! Usamos el modelo que te asignó Google
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=user_prompt,
                config=config,
            )

            # 4. Limpiamos cualquier Markdown remanente
            raw_text = response.text
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()

            print("✅ GEMINI 3 CONECTADO EXITOSAMENTE:\n", clean_text[:200], "...")

            return json.loads(clean_text)

        except Exception as e:
            print("\n" + "=" * 40)
            print("💥 ERROR EN EL NUEVO SDK DETECTADO")
            traceback.print_exc()
            print("=" * 40 + "\n")
            return {"error": True, "message": f"Error del SDK: {str(e)}"}
