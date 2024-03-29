# imports
import json, pandas as pd, math
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from . import forms

# importing helper functions
from home.helper.transform import update_csv, graph_dict, reverse_doc

## TRENDS
# NYT
from home.helper.trends.nyt.generate import gen_nyt_trends
from home.helper.trends.nyt.reverse import reverse_nyt
# Healthcare
from home.helper.trends.healthcare.generate import gen_healthcare_trends
from home.helper.trends.healthcare.reverse import reverse_healthcare

# TODO : add proper descripion to all functions and methods and files

# Function to get initial data
def init():
    name = "nyt"
    base = "race"
    terms = ["state", "government", "news", "sports"]
    
    # docs = [
    #     "In College Football, No Player Escapes the Eye of the Strength Coach Head coaches and players emphasize the importance of the strength coach, and salaries for the position at top college football programs are growing.",
    #     "Where CPR on a Boy Is Time Wasted: U.S. Doctors Recall Aleppos Horrors Three American doctors provided a personal perspective on the deepening emergency in a Syrian city where local doctors have grown weary of the bloodshed.",
    #     "Israels Benjamin Netanyahu, Still a Step Ahead of Scandals, Faces a New Inquiry The new attorney general says he will take a hard line, but Mr. Netanyahu has shown he can slip away from accusations with Teflon-coated ease.",
    #     "Russias Acres, if Not Its Locals, Beckon Chinese Farmers With farmland in China scarce, migrants are crossing the border to lease large, unused tracts in the Far East, where many residents grumble about their presence and hard work.",
    #     "Exaggerator Storms Down the Stretch to Win the Haskell Invitational On a sloppy track, Nyquist, the Kentucky Derby winner, faded to fourth in a field of six."
    # ]

    docs = reverse_nyt(base, terms[0], terms[1])

    return name, base, terms, docs

# Create your views here.
def index(req):
    # initialize model
    name, base_term, rel_terms, rev_data = init()

    # get values of terms and y-axis labels
    labels, values = gen_nyt_trends(base_term, rel_terms)

    # update values in the graph data csv 
    update_csv(rel_terms, values)
    
    # Context dict to send to page
    context = {
        "context": {
            "graph": graph_dict(values, name, base_term, rel_terms, labels),
            "trendForm": forms.TrendForm(),
            "revData": reverse_doc(rev_data, base_term, rel_terms[0], rel_terms[1]),
            "revForm": forms.ReverseForm(),
        }
    }

    return render(req, 'index.html', context)

def method(req):
    return render(req, 'method.html')

def about(req):
    return render(req, 'about-us.html')

def graph_update(req):
    # if request method is POST
    if req.method == 'POST':
        # submitted info
        form = forms.TrendForm(req.POST)

        # check for django form validity
        if form.is_valid():
            # loop through a python dict and add all vales to a list whose key matces a substring?
            terms = []
            for k,v in {key: value for key, value in form.cleaned_data.items() if key.startswith('rel')}.items():
                terms.append(str(v))

            # received data
            name = form.cleaned_data["model_type"]
            base_term = form.cleaned_data["base_term"]
            rel_terms = terms

            if name == 'nyt':
                labels, values = gen_nyt_trends(base_term, rel_terms)
            elif name == 'healthcare':
                labels, values = gen_healthcare_trends(base_term, rel_terms)

            # updating the data stored in the graph csv
            update_csv(rel_terms, values)

            return JsonResponse({
                "status":"success",
                "code": 200,
                "graph": graph_dict(values, name, base_term, rel_terms, labels),
            })

def reverse(req):
    # if request method is POST
    if req.method == 'POST':
        # submitted info
        form = forms.ReverseForm(req.POST)

        # check for django form validity
        if form.is_valid():
            # loop through a python dict and add all vales to a list whose key matces a substring?
            terms = []
            for k,v in {key: value for key, value in form.cleaned_data.items() if key.startswith('rel')}.items():
                terms.append(str(v))

            # received data
            name = form.cleaned_data["model_type"]
            base_term = form.cleaned_data["base_term"]
            rel_terms = terms

            if name == 'nyt':
                rev_data = reverse_nyt(base_term, rel_terms[0], rel_terms[1])
            elif name == 'healthcare':
                # example:
                #   base: diseases
                #   rel1:  infections
                #   rel1:  cleaning
                rev_data = reverse_healthcare(base_term, rel_terms[0], rel_terms[1])

            # print(base_term, rel_terms[0], rel_terms[1])
            # print(rev_data)
            # print(reverse_doc(rev_data))

            return JsonResponse({
                "status":"success",
                "code": 200,
                "revData": reverse_doc(rev_data, base_term, rel_terms[0], rel_terms[1]),
            })

def term_autocomplete(req, model_type):
    if req.GET.get('q'):
        if model_type == 'nyt':
            BASE_DIR = "./home/helper/trends/nyt/"
        elif model_type == 'healthcare':
            BASE_DIR = "./home/helper/trends/healthcare/"
        else:
            return JsonResponse([], safe=False)
            
        f = open(BASE_DIR + "words.json")
        data = json.load(f)["common"]

        letter = str(req.GET['q']).lower()
        subset = [i for i in data if i.lower().startswith(letter)]

        return JsonResponse(subset, safe=False)
