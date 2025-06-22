from django.contrib import admin
from django.utils.html import format_html
from .models import Evaluation, FlowResult, EvaluationResult, PronunciationResult


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date_added", "last_modified", "result_link")
    list_display_links = ("id",)
    search_fields = ("user__username", "user__email")
    list_filter = ("date_added", "last_modified")
    ordering = ("-date_added",)
    readonly_fields = ("id", "date_added", "last_modified", "user")

    @admin.display(description="Result")
    def result_link(self, obj):
        if hasattr(obj, "result") and obj.result:
            url = f"/admin/pronunciation_evaluation/evaluationresult/{obj.result.id}/change/"
            return format_html(format_string=f'<a href="{url}">View Result</a>')
        return "-"

    def save_model(self, request, obj, form, change):
        # Use getattr to avoid RelatedObjectDoesNotExist
        user = getattr(obj, "user", None)
        if not user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(FlowResult)
class FlowResultAdmin(admin.ModelAdmin):
    list_display = ("id", "speaking_ratio", "speaking_speed", "flow_score")
    search_fields = ("id", "speaking_ratio", "speaking_speed", "flow_score")
    list_filter = ("speaking_ratio", "speaking_speed", "flow_score")
    ordering = ("-flow_score",)
    readonly_fields = ("id", "speaking_ratio", "speaking_speed", "flow_score")


@admin.register(PronunciationResult)
class PronunciationResultAdmin(admin.ModelAdmin):
    list_display = ("id", "score", "percentage", "user_phonemes", "reference_phonemes")
    search_fields = ("score", "percentage")
    list_filter = ("score", "percentage")
    readonly_fields = (
        "id",
        "score",
        "percentage",
        "user_phonemes",
        "reference_phonemes",
    )


@admin.register(EvaluationResult)
class EvaluationResultAdmin(admin.ModelAdmin):
    list_display = ("id", "evaluation", "clarity_score", "date_added")
    search_fields = (
        "evaluation__user__username",
        "evaluation__user__email",
        "evaluation__reference_text",
    )
    list_filter = ("clarity_score", "date_added")
    readonly_fields = (
        "id",
        "clarity_score",
        "date_added",
        "evaluation",
        "reference_flow_result",
        "user_flow_result",
        "pronunciation_result",
    )
