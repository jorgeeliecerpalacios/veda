from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
from django.views import View

from schedule_app.models import ClassBlock, Subject

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

        start_dt = parse_datetime(start_str) if start_str else subject.created_at
        if start_dt and is_naive(start_dt):
            start_dt = make_aware(start_dt)

        end_dt = parse_datetime(end_str) if end_str else subject.created_at
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

        # DB Persistence - Instantiating our Schedule Model dynamically
        new_block = ClassBlock.objects.create(
            subject=subject,
            topic_title=ai_response.get("refined_title", raw_topic),
            ai_generated_content=ai_response.get("lesson_content"),
            pedagogical_methodology=methodology,
            start_time=parse_datetime(start_str) if start_str else subject.created_at,
            end_time=parse_datetime(end_str) if end_str else subject.created_at,
        )

        return render(
            request,
            "ai_core/lesson_workspace.html",
            {"block": new_block, "ai_data": ai_response},
        )
