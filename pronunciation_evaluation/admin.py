from django.contrib import admin
from .models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date_added", "last_modified")
    search_fields = ("user__username", "user__email")
    list_filter = ("date_added", "last_modified")
    ordering = ("-date_added",)
    readonly_fields = ("id", "date_added", "last_modified")