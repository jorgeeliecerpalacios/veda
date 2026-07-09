import json
import os

import requests
from pydantic import BaseModel, Field


# =====================================================================
# 📋 CONTRATO ESTRICTO DE DATOS (ESQUEMA INMUTABLE PARA LA IA)
# =====================================================================
class MultimediaGuidelinesSchema(BaseModel):
    visuals: str = Field(description="Search keywords or guidelines for images and infographics.")
    videos: str = Field(description="Search keywords or guidelines for videos and interactive animations.")

class VedaWorkspaceSchema(BaseModel):
    topic: str = Field(description="The formal or standardized name of the researched topic.")
    lesson_material: str = Field(description="Full text containing detailed content, definitions, and key subtopics to teach.")
    suggested_activity: str = Field(description="Detailed pedagogical step-by-step classroom activity or dynamic.")
    key_learning_points: list[str] = Field(description="A clean bulleted list of learning objectives or points.")
    multimedia_guidelines: MultimediaGuidelinesSchema


class VedaIntelligenceService:
    """
    Engine responsible for web research and curriculum adaptation using LLM APIs.
    Returns structured data matching the pedagogical criteria of Veda.
    """

    def __init__(self) -> None:
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")

    def research_and_curate_topic(
        self, topic: str, country: str, age: int, methodology: str
    ) -> dict:
        """
        Sends metadata to the AI or triggers a local mock fallback if no API keys are present.
        """
        system_prompt = (
            "You are Veda, an advanced AI specialized in international curriculum mapping and pedagogy.\n"
            f"You MUST adapt the content for a student target age of {age} years old inside the country context of {country}, "
            f"strictly using the '{methodology}' framework.\n"
            "Generate extensive explanation text inside the 'lesson_material' field."
        )
        user_prompt = f"Research, filter, and adapt the following topic: '{topic}'"

        if self.openai_key:
            return self._call_openai(system_prompt, user_prompt)
        elif self.gemini_key:
            return self._call_gemini(system_prompt, user_prompt)
        else:
            return self._generate_mock_response(topic, country, age, methodology)

    def _generate_mock_response(
        self, topic: str, country: str, age: int, methodology: str
    ) -> dict:
        """Devuelve un objeto estructurado simulando la respuesta exacta del LLM"""
        return {
            "topic": topic,
            "key_learning_points": [
                f"Core foundations of {topic} adapted for {age} year olds.",
                f"Contextual applications conforming to {country} educational guidelines.",
                f"Interactive experimentation based on {methodology} principles.",
            ],
            "lesson_material": (
                f"This is a curated educational module for '{topic}'. In {country}, students at this level "
                f"approach this via {methodology}. The focus is on tactile learning and core vocabulary "
                f"suitable for a target audience of {age} years old. (Veda Sandbox Engine active)."
            ),
            "suggested_activity": f"Group dynamic: Build a conceptual model or run a simulation of '{topic}' using local classroom resources.",
            "multimedia_guidelines": {
                "visuals": f"Infographics displaying basic {topic} dynamics.",
                "videos": f"Animated 3-minute clips explaining {topic}.",
            },
        }

    def _call_openai(self, system_prompt: str, user_prompt: str) -> dict:
        # Mantenemos tu integración con OpenAI forzando también el formato JSON
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_key}",
        }
        payload = {
            "model": "gpt-4o",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt + " Output must strictly conform to a JSON containing fields: 'topic', 'lesson_material', 'suggested_activity', 'key_learning_points'[], and 'multimedia_guidelines'{'visuals', 'videos'}"},
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
        import traceback

        from google import genai
        from google.genai import types

        try:
            clean_key = self.gemini_key.strip()
            client = genai.Client(api_key=clean_key)

            # 🚀 AQUÍ OBLIGAMOS A GEMINI A SEGUIR EL SQUEMA PYDANTIC Exacto
            config = types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json",
                response_schema=VedaWorkspaceSchema,  # 🔥 EL CONTRATO INMUTABLE
                system_instruction=system_prompt,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )

            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=user_prompt,
                config=config,
            )

            raw_text = response.text
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()

            print("✅ GEMINI ESTRUCTURADO RECIBIDO CORRECTAMENTE")
            return json.loads(clean_text)

        except Exception as e:
            print("\n" + "=" * 40)
            print("💥 ERROR EN EL NUEVO SDK DETECTADO")
            traceback.print_exc()
            print("=" * 40 + "\n")
            return {"error": True, "message": f"Error del SDK: {str(e)}"}
