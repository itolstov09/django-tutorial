from django.contrib import admin

# Register your models here.

from . models import Question


class QuestuionAdmin(admin.ModelAdmin):
    fields = ['publication_date', 'question_text']


admin.site.register(Question, QuestuionAdmin)

