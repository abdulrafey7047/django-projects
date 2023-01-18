from django.contrib import admin

from .models import Author, Question, Choice

admin.site.register(Author)
admin.site.register(Question)
admin.site.register(Choice)
