# -*- coding: utf-8 -*-
# Download.
from django.shortcuts import render
import json
from jsonschema import Draft4Validator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from textMining.saveFile import savePaper

def downloadResults(request):
    if request.method == 'GET':
        response = HttpResponse("test",mimetype='application/json')
        response['Content-Disposition'] = 'attachment; filename="ergebnisse.json"'