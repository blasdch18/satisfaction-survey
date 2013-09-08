# -*- coding: utf-8 -*-
from django.db import models


class Answer(models.Model):
    content = models.CharField(max_length=64)
    value = models.IntegerField(unique=True)
    
    def __unicode__(self):
        return u"(%s) %s" % (self.value, self.content)
    
    class Meta:
        ordering = ['value']


class Term(models.Model):
    content = models.CharField(max_length=64)
    order_factor = models.PositiveIntegerField(default=1)
    answers = models.ManyToManyField(Answer, related_name='terms')
    
    def __unicode__(self):
        return self.content
    
    class Meta:
        ordering = ['order_factor']


class Question(models.Model):
    content = models.CharField(max_length=512)
    order_factor = models.PositiveIntegerField(default=1)
    answers = models.ManyToManyField(Answer, related_name='questions', null=True, blank=True)
    terms = models.ManyToManyField(Term, related_name='questions', null=True, blank=True)
    
    def __unicode__(self):
        limit = 64
        return u"%s%s" % (self.content[:limit], len(self.content) > limit and u"..." or u"")
    
    class Meta:
        ordering = ['order_factor']


class Section(models.Model):
    name = models.CharField(max_length=256)
    order_factor = models.PositiveIntegerField(default=1)
    questions = models.ManyToManyField(Question, related_name='sections')
    
    def __unicode__(self):
        limit = 64
        return u"%s%s" % (self.name[:limit], len(self.name) > limit and u"..." or u"")
    
    class Meta:
        ordering = ['order_factor']


class FormType(models.Model):
    name = models.CharField(max_length=512)
    sections = models.ManyToManyField(Section, related_name='form_types')
    
    def __unicode__(self):
        limit = 64
        return u"%s%s" % (self.name[:limit], len(self.name) > limit and u"..." or u"")


class SurveyForm(models.Model):
    customer_id = models.IntegerField()
    date = models.DateField()
    submitted = models.BooleanField(default=False, blank=True)
    form_type = models.ForeignKey(FormType, related_name='forms')
    
    def __unicode__(self):
        return u"customer %s, form %s on (%s)" % (self.customer_id, self.form_type, self.date)
    
    class Meta:
        unique_together = ('customer_id', 'date', 'form_type')


class FormAnswer(models.Model):
    form = models.ForeignKey(SurveyForm)
    question = models.ForeignKey(Question, null=True, blank=True)
    term = models.ForeignKey(Term, null=True, blank=True)
    answer = models.ForeignKey(Answer, related_name='answers')
    comment = models.TextField(blank=True)
    
    def __unicode__(self):
        return u"answer to %s from %s" % (self.question, self.form)





























