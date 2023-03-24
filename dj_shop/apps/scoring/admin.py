from django.contrib import admin
from .models import Scoring

@admin.register(Scoring)
class ScoringAdmin(admin.ModelAdmin):
    list_display=('product','scoring_user','score')
    list_filter=('score',)