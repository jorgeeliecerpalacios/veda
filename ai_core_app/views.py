import json

from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware
from django.views import View
from django.views.generic import ListView
from schedule_app.models import ClassBlock, Subject

# pyrefly: ignore [missing-import]
from .services import VedaIntelligenceService


class ResearchTopicView(View):
    """
    Handles processing of specific research queries submitted by teachers.
    Generates and saves a ClassBlock with AI insights.
    """

    def get(self, request, subject_id):  # noqa: ANN001, ANN201
        # We fetch the specific subject to extract its context (age, country)
        subject = get_object_or_404(Subject, id=subject_id)
        return render(request, "ai_core/research_form.html", {"subject": subject})

    def post(self, request, subject_id):  # noqa: ANN001, ANN201
        subject = get_object_or_404(Subject, id=subject_id)
        raw_topic = request.POST.get("topic")
        methodology = request.POST.get("methodology", "Constructivism")

        # Calendar block inputs from the teacher
        start_str = request.POST.get("start_time")
        end_str = request.POST.get("end_time")

        start_dt = parse_datetime(start_str) if start_str else None
        if start_dt and is_naive(start_dt):
            start_dt = make_aware(start_dt)

        end_dt = parse_datetime(end_str) if end_str else None
        if end_dt and is_naive(end_dt):
            end_dt = make_aware(end_dt)
        print("Received POST data:", request.POST)

        # Trigger our AI Core engine
        ai_engine = VedaIntelligenceService()
        ai_response = ai_engine.research_and_curate_topic(
            topic=raw_topic,
            country=subject.country,
            age=subject.target_age,
            methodology=methodology,
        )

        if "error" in ai_response:
            return render(
                request,
                "ai_core/research_form.html",
                {"subject": subject, "error": ai_response["message"]},
            )

        # Convertimos el diccionario completo de la IA en una cadena de texto JSON para la BD
        ai_json_string = json.dumps(ai_response, ensure_ascii=False)

        # DB Persistence - Instantiating our Schedule Model dynamically
        new_block = ClassBlock.objects.create(
            subject=subject,
            topic_title=ai_response.get("topic", raw_topic),
            ai_generated_content=ai_json_string,
            pedagogical_methodology=methodology,
            start_time=start_dt if start_dt else subject.created_at,
            end_time=end_dt if end_dt else subject.created_at,
        )

        # 🎯 MISMO MAPEO EXACTO PARA EL POST
        adaptation = ai_response.get("pedagogical_adaptation", {})

        ai_data_mapped = {
            "suggested_activity": " / ".join(adaptation.get("scaffolding_strategies", [])) or "No activity specified",
            "key_learning_points": adaptation.get("learning_objectives", []),
            "multimedia_guidelines": {
                "visuals": "Search graphs or numerical lines for irrational numbers.",
                "videos": "Search visual proofs of the Pythagorean theorem."
            }
        }

        lesson_material = f"Definition:\n{adaptation.get('definition', '')}\n\n"
        lesson_material += "Key Concepts:\n" + "\n".join([f"• {c}" for c in adaptation.get("key_concepts", [])])

        return render(
            request,
            "ai_core/lesson_workspace.html",
            {
                "block": new_block,                  # Para buscar variables generales
                "new_block": new_block,              # Para el modal y el formulario de recursos
                "subject": subject,
                "ai_data": ai_data_mapped,           # Diccionario con llaves estandarizadas
                "lesson_material": lesson_material, # Texto limpio para el cuadro central
            },
        )


class AIResearchDashboardView(ListView):
    """
    Panel principal (Hub) de Inteligencia Artificial.
    Permite al docente elegir en qué materia quiere realizar investigación con Gemini.
    """
    model = Subject
    template_name = "ai_core/research_dashboard.html"
    context_object_name = "subjects"

    def get_queryset(self):  # noqa: ANN201
        # Traemos las materias y anotamos cuántas clases (ClassBlocks) se han generado en cada una
        return Subject.objects.annotate(total_classes=Count('class_blocks')).order_by('name')
