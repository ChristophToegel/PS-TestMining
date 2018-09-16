# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from textMining.models import Paper, Metadata
import json
from django.shortcuts import redirect
from os import listdir
from os.path import join
import metriken
from textMining.saveFile import savePaper

#currentJsonfiles=[]

def calculateMetriken(request):
    papers = Paper.objects.all()
    for paper in papers:
        words=metriken.calculateWords(paper)
        print(words)
    # save words in DB
    context = {'info': 'metriken werden berechnet'}
    categories = Metadata.objekts.distinct('category')
    return render(request, 'startseite.html', context, categories)

def calculateFreqWords(request):
    corpus1=metriken.calculateWordFrequency(Paper.objects.filter(metaData__category='Food & Nutrition'))
    #print(corpus1)
    corpus2 = metriken.calculateWordFrequency(Paper.objects.filter(metaData__category='Mathematics'))
    #print(corpus2)
    return render(request, 'old/freqWords.html', {"corpus1":corpus1, "corpus2":corpus2})

def showStartPage(request):
    return render(request, 'startseite.html')

def calculateMeanImpactFactor(impact):
    sum = 0
    counter = 0
    for factor in impact:
        sum += factor
        counter += 1
    mean = sum/counter
    return mean



#hier alles was benötigt wird rein, wird bei url:http://127.0.0.1:8000/textMining/vergleich/ aufgerufen
def showVergleichPage(request):
    categories = Paper.objects.distinct('metaData.category')
    countries = Paper.objects.distinct('authors_authorList_university_university_universityCountry')
    authors = Paper.objects.distinct('authors_authorList.authorName')
    journals = Paper.objects.distinct('metaData.journalTitle')
    impactfactor = Paper.objects.distinct('metaData.impactfactor')
    #meanimpact = calculateMeanImpactFactor(impactfactor)
    keywords = Paper.objects.distinct('metaData.keywords')
    context = {'categories': categories, 'countries':countries, 'authors': authors, 'journals': journals,
               'impactfactor': impactfactor, 'keywords':keywords}
    return render(request, 'vergleich.html',context)

#TODO DB files download!

def showResults(request):
    #1. getCorpora filterdata should bei in the request
    corpus1 = Paper.objects.all()[0:4]
    corpus2 = Paper.objects.all()[4:8]
    print(Paper.objects(authors__authorList__university__university_universityCountry__icontains = 'Malaysia'))
    #2.calculate sum for some Metrtiken.

    context={'corpus1':corpus1,'corpus2':corpus2}
    return render(request, 'ergebnis.html',context)

def readJsonFiles(request):
    # loads all Json files....
    readpath = "./output"
    onlyOne = False
    counter=0
    for filename in listdir(readpath):
        if not onlyOne:
            if filename != ".DS_Store": #file.endswith('.json')
                file = open(join(readpath, filename), 'r', encoding='utf-8', errors="ignore")
                paperJson = json.load(file)
                paper=savePaper(paperJson)
                print("Paper saved!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                counter+=1
        onlyOne=False

    paperlist=Paper.objects.all()
    print('categorien')
    print(Paper.objects.distinct('metaData.category'))
    context = {'paperlist': paperlist}
    return render(request, 'old/Helloworld.html', context)


#Aufbereiten der Text Stopwortfiltern und lemmatisieren
def processPaper(request):
    print("Paper werden aufbreitet....")
    paperlist = Paper.objects.all()[4:8]
    for paper in paperlist:
        metriken.removeStopwords(paper) #MET_text_to_STOP_text
        metriken.lemmatize_Paper(paper) #MET_text_to_LEMMA_text
        metriken.char_count_per_section_Paper(paper) #MET_char_Count
        metriken.citation_count_per_section_Paper(paper) #MET_citation_Count
        metriken.punctuation_count_per_section_Paper(paper) #MET_punctuation_Count
        metriken.word_count_per_section_Paper(paper) #MET_word_Count
        metriken.sentencelength_average_per_section_Paper(paper) #MET_average_sentslength

    print("Papersind aufbereitet")

    context = {'paperlist': paperlist}
    return render(request, 'old/Helloworld.html', context)

