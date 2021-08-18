from django.contrib import admin

# Register your models here.

from . models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestuionAdmin(admin.ModelAdmin):
    list_display = (
        'question_text',
        'publication_date',
        'was_published_recently'
    )
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['publication_date']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestuionAdmin)

