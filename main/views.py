# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from forms import *
from models import *
from pprint import pprint
from util.lib import response_json
from util.xtea import crypt


def survey(request, survey_id):
    survey_id, survey_string, formtype, survey_date, customer_id, formtype_id = _process_input(survey_id)
    survey_form, created = SurveyForm.objects.get_or_create(date=datetime.strptime(survey_date, settings.ENCRYPTION_DATE_FMT).date(), customer_id=customer_id, form_type=formtype)
    
    if survey_form.submitted:
        return redirect('thank_you')
    elif date.today() > survey_form.date + timedelta(days=settings.SURVEYFORM_LIFEDAYS):
        return redirect('expired')
    
    if request.method == 'POST':
        _process_submit(request.POST, survey_form)
        return redirect('thank_you')
    
    return render_to_response('main/survey.html', {
        'survey_data': _build_survey(survey_form),
        'survey_id': survey_id,
        'comment_from': settings.COMMENT_FROM,
        'max_rate': Answer.objects.aggregate(Max('value'))['value__max']
    }, context_instance=RequestContext(request))


def generate_link(request, customer_id, formtype_id, creation_date=None):
    if creation_date is not None:
        try:
            survey_date = datetime.strptime(creation_date, settings.ENCRYPTION_DATE_FMT).date()
        except ValueError:
            raise Http404
    else:
        survey_date = date.today()
    
    survey_string = settings.ENCRYPTION_SEPARATOR.join([survey_date.strftime(settings.ENCRYPTION_DATE_FMT), customer_id, formtype_id])
    return response_json(reverse('survey', kwargs={'survey_id': crypt(settings.ENCRYPTION_KEY, survey_string).encode('hex')}))


def survey_structure(request):
    form_type = FormType.objects.get(pk=1)
    data = {'formtypes': [{'formtype_id': form_type.pk, 'formtype_name': form_type.name, 'sections': []}], 'answers': []}
    for section in form_type.sections.all():
        section_node = {'section_id': section.pk, 'section_name': section.name, 'questions': []}
        for question in section.questions.all():
            question_node = {'question_id': question.pk, 'question_text': question.content, 'terms': []}
            for term in question.terms.all():
                term_node = {'term_id': term.pk, 'term_text': term.content}
                question_node['terms'].append(term_node)
            section_node['questions'].append(question_node)
        data['formtypes'][0]['sections'].append(section_node)
    for answer in Answer.objects.all():
        data['answers'].append({'answer_id': answer.pk, 'answer_text': answer.content, 'answer_value': answer.value})
    return response_json(data)


def survey_submit(request, form_id):
    survey_form = get_object_or_404(SurveyForm, pk=form_id)
    data = {'customer_id': survey_form.customer_id, 'formtype_id': survey_form.form_type_id, 'creation_date': survey_form.date.strftime(settings.ENCRYPTION_DATE_FMT), 'answers': []}
    for answer in FormAnswer.objects.filter(form=survey_form):
        data['answers'].append({'question_id': answer.question_id, 'term_id': answer.term_id, 'answer_id': answer.answer_id, 'comment': answer.comment})
    return response_json(data)


def survey_range(request, from_date, to_date, submitted):
    from_date = datetime.strptime(from_date, settings.ENCRYPTION_DATE_FMT).date()
    to_date = datetime.strptime(to_date, settings.ENCRYPTION_DATE_FMT).date()
    data = []
    surveys = bool(int(submitted)) and SurveyForm.objects.filter(date__gte=from_date, date__lte=to_date, submitted=True) or SurveyForm.objects.filter(date__gte=from_date, date__lte=to_date)
    for survey in surveys:
        s = {'form_id': survey.pk, 'customer_id': survey.customer_id, 'formtype_id': survey.form_type_id, 'creation_date': survey.date.strftime(settings.ENCRYPTION_DATE_FMT), 'answers': []}
        for answer in FormAnswer.objects.filter(form=survey):
            s['answers'].append({'question_id': answer.question_id, 'term_id': answer.term_id, 'answer_id': answer.answer_id, 'comment': answer.comment})
        data.append(s)
    return response_json(data)


def _build_survey(survey_form):
    data = {'survey': survey_form, 'sections': []}
    for section in survey_form.form_type.sections.all():
        section_node = {'section': section, 'questions': []}
        for question in section.questions.all():
            question_node = {'question': question, 'terms': [], 'answers': []}
            for answer in question.answers.all():
                question_node['answers'].append(answer)
            for term in question.terms.all():
                term_node = {'term': term, 'answers': []}
                for term_answer in term.answers.all():
                    term_node['answers'].append(term_answer)
                question_node['terms'].append(term_node)
            section_node['questions'].append(question_node)
        data['sections'].append(section_node)
    return data


def _process_input(survey_id):
    if settings.ENCRYPTION_SEPARATOR in survey_id:
        survey_string = survey_id
        survey_id = crypt(settings.ENCRYPTION_KEY, survey_string).encode('hex')
    else:
        try:
            survey_string = crypt(settings.ENCRYPTION_KEY, survey_id.decode('hex'))
        except TypeError:
            raise Http404
    
    try:
        survey_date, customer_id, formtype_id = survey_string.split(settings.ENCRYPTION_SEPARATOR)
        formtype = FormType.objects.get(pk=formtype_id)
    except (ValueError, FormType.DoesNotExist):
        raise Http404
    
    return survey_id, survey_string, formtype, survey_date, customer_id, formtype_id


def _process_submit(data, form):
    answer_prefix = 'answer_'
    comment_prefix = 'comment_'
    for key in data.keys():
        if answer_prefix not in key:
            continue
        answer = {'sect': None, 'quest': None, 'term': None}
        params = key.replace(answer_prefix, '').split('_')
        for param in params:
            ans_key, ans_value = param.split('-')
            answer[ans_key] = ans_value
        form_answer = FormAnswer(form=form, question_id=int(answer['quest']))
        form_answer.answer = Answer.objects.get(value=int(data[key]))
        form_answer.comment = int(data[key]) <= settings.COMMENT_FROM and data[key.replace(answer_prefix, comment_prefix)] or u""
        if answer['term']:
            form_answer.term_id = int(answer['term'])
        form_answer.save()
    form.submitted = True
    form.save()





























