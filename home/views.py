import re, os, json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import models, forms

from .helper.process import convert
from .helper.trends import nyt_trends

# TODO : Add urls for generic and elements.html and resolve their assets into static as well

# Create your views here.
def index(req):

    # if request method is POST
    if req.method == 'POST':
        # submitted info
        form = forms.TrendForm(req.POST)

        # check for django form validity
        if form.is_valid():
            # print(form.cleaned_data)

            # loop through a python dict and add all vales to a list whose key matces a substring?
            terms = []
            for k,v in {key: value for key, value in form.cleaned_data.items() if key.startswith('rel')}.items():
                terms.append(str(v))

            name = form.cleaned_data["model_type"]
            base_term = form.cleaned_data["base_term"]
            rel_terms = terms

            labels, dataready = nyt_trends(base_term, rel_terms)
    else:
        name = "nyt"
        base_term = "race"
        rel_terms = ["state", "government", "new", "sports"]

        labels, dataready = nyt_trends(base_term, rel_terms)
    

    context = {
        "context": {
            "graph": {
                "rangeX": 7,
                "rangeY": 1.2,
                "name" : name,
                "base_term": base_term,
                "rel_terms": rel_terms,
                "period_labels": labels,
                "dataready": dataready,
            },
            "form": forms.TrendForm()
        }
    }

    

    return render(req, 'index.html', context)