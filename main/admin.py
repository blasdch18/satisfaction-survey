# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order_factor', 'content')
    list_display_links = ('order_factor', 'content')


class TermAdmin(admin.ModelAdmin):
    list_display = ('order_factor', 'content')
    list_display_links = ('order_factor', 'content')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('value', 'content')
    list_display_links = ('value', 'content')


class SectionAdmin(admin.ModelAdmin):
    list_display = ('order_factor', 'name')
    list_display_links = ('order_factor', 'name')


class FormTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class SurveyFormAdmin(admin.ModelAdmin):
    pass


class FormAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'question', 'term', 'answer', 'comment')
    list_display_links = ('id',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(FormType, FormTypeAdmin)
admin.site.register(SurveyForm, SurveyFormAdmin)
admin.site.register(FormAnswer, FormAnswerAdmin)
