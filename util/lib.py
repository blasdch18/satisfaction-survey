from datetime import datetime, timedelta, date
from django.conf import settings
from django.db import models
from django.http import HttpResponse

import time
try:
    import simplejson as json
except ImportError:
    import json


def _unix_timestamp(d):
    return int(time.mktime(d.timetuple()))


def _model2dict(item, fields=[]):
    d = {}
    for field in fields:
        f = item.__dict__[field]
        if type(f) in [datetime, date]:
            d[field] = _unix_timestamp(f)
        else:
            d[field] = f
    
    return d


def _qs2list(qs, fields=[]):
    return [_model2dict(item, fields) for item in qs]


def response_json(data, fields=[]):
    if (issubclass(data.__class__, models.Model)):
        data = _model2dict(data, fields)
    elif (issubclass(data.__class__, models.query.QuerySet)):
        d = []
        for item in data:
            d.append(_model2dict(item, fields))
        data = d
    
    return HttpResponse(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False), mimetype='application/json')



















