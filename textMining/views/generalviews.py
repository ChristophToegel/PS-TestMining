# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render, render_to_response
from textMining.models import Metric,Text, Subsection, Reference, References, Paper, Author, Metadata, Authors, University, Abstract, \
    Picture, Pictures, Table, Tables, ResCitationSegmentCount, ResCharSegmentCount
import json
from django.shortcuts import redirect
from os import listdir
from os.path import join
import metriken
from jsonschema import Draft4Validator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
import ast
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


def showResults(request):
    return render(request, 'ergebnis.html')

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
                '''paperDB=Paper()
                paperDB.title=paperJson['title']
                print(file)
                print(counter)
                # create paper form jsonfile
                # create Authors
                if paperJson.get('authors'):
                    paperDB.authors=Authors(count = paperJson['authors']['count'],authorList = [])
                    for autor in paperJson['authors']['authorList']:
                        paperDB.authors.authorList.append(
                            Author(authorName=autor['authorName'], authorIndex=autor['authorIndex'],
                                                  university=University(
                                                      university_universityName=autor['university']['universityName'],
                                                      university_universityCountry=autor['university'][
                                                          'universityCountry'])))
                    #authors = Authors.objects.create(count=paperJson['authors']['count'], authorList=arrayAutoren)
                else:
                    paperDB.authors = Authors(count=0, authorList=[])

                # metadata
                if paperJson['metaData']:
                    paperDB.metaData=Metadata(yearOfArticle=paperJson['metaData']['yearOfArticle'],category=paperJson['metaData']['category'],
                                              source=paperJson['metaData']['source'],journalTitle = paperJson['metaData']['journaltitle'],
                                              impactfactor=paperJson['metaData']['impactFactor'],URL=paperJson['metaData']['URL'],
                                              paperType=paperJson['metaData']['paperType'])
                    if paperJson['metaData'].get('keywords'):
                        paperDB.metaData.keywords =paperJson['metaData']['keywords']
                    else:
                        paperDB.metaData.keywords =[]
                        #paperDB.metaData.yearOfArticle=paperJson['metaData']['yearOfArticle'],
                        #paperDB.metaData.category=paperJson['metaData']['category'],
                        #paperDB.metaData.source=paperJson['metaData']['source'],
                        #paperDB.metaData.journalTitle = paperJson['metaData']['journaltitle'],
                        #paperDB.metaData.impactfactor = paperJson['metaData']['impactFactor'],
                        #paperDB.metaData.URL=paperJson['metaData']['URL'],
                        #paperDB.metaData.paperType=paperJson['metaData']['paperType']

                # create Abstract
                #Todo paper sollte immer Array sein( auch bei titel=empty and text=empty) <<empty>>
                paperDB.abstract=[]
                if isinstance(paperJson['abstract'], list):
                    for abstractPart in paperJson['abstract']:
                        paperDB.abstract.append(Abstract(title=abstractPart['title'],text=abstractPart['text'] ,metrik = Metric()))
                else:
                    if not paperJson['abstract']=='<<empty>>':
                        paperDB.abstract.append(Abstract(title=paperJson['abstract']['title'], text=paperJson['abstract']['title'],metrik = Metric()))

                if paperJson.get('references'):
                    # create Reference
                    paperDB.references=References(referencesList=[],count=paperJson['references']['count'])
                    arrayReferences = []
                    for reference in paperJson['references']['referencesList']:
                        paperDB.references.referencesList.append(Reference(referenceIndex=reference['referenceIndex'],
                                                                        referenceName=reference['referenceName'],
                                                                        referenceAuthor=reference['referenceAuthor'],
                                                                        referenceYear=str(reference['referenceYear'])))
                else:
                    paperDB.references = References(referencesList=[], count=0)


                # createText todo tabellen und bilder an models anpassen!
                paperDB.text= []
                for textsection in paperJson['text']:
                    # tables
                    subTextArray=[]
                    arrayTables = []
                    if textsection['tables']:
                        for table in textsection['tables']['tablesList']:
                            arrayTables.append(
                                Table(tableIndex=table['index'], tableRowDim=table['tableRowDim'],
                                                     tableCodDim=table['tableColDim'],
                                                     tableDescription=table['tableDescription']))
                        tables = Tables(count=textsection['tables']['count'], tablesList=arrayTables)
                    else:
                        tables=None
                    # pictures
                    arrayPictures = []
                    if textsection['pictures']:
                        for picture in textsection['pictures']['picturesList']:
                            arrayTables.append(
                                Picture(pictureIndex=picture['index'], pictureDescription=picture[
                                    'pictureDescription']))
                        pictures = Pictures(count=textsection['pictures']['count'], picturesList=arrayPictures)
                    else:
                        pictures = None

                    if textsection['subsection']:
                        for subsection in textsection['subsection']:
                            subTextArray.append(Subsection(title=subsection['title'], text=subsection['text'],metrik = Metric()))

                    paperDB.text.append(
                        Text(title=textsection['title'], text=textsection['text'], metrik = Metric(), subsection=subTextArray,
                                            tables=tables, pictures=pictures,
                                            #formula=textsection['formula']
                                            ))

                paperDB.save()'''
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
    paperlist = Paper.objects.all()[:4]
    for paper in paperlist:
        metriken.removeStopwords(paper)
        metriken.lemmatize_Paper(paper)
        metriken.char_count_per_section_Paper(paper)


    context = {'paperlist': paperlist}
    return render(request, 'old/Helloworld.html', context)

'''
def uploadFiles(request):
    if request.method == 'GET':
        return render(request, 'upload.html')

    if request.method == 'POST':
        global currentJsonfiles
        #print(request.FILES.getlist('JsonPaper'))
        validPaper = []
        invalidPaper = []
        json_data = open("Paperschema.json", "r")
        schema = json.load(json_data)
        v = Draft4Validator(schema)
        for uploadfile in request.FILES.getlist('JsonPaper'):
            print(uploadfile.name)
            jsondata=json.loads(uploadfile.read().decode('utf-8'))
            #print(jsondata)
            currentJsonfiles.append(jsondata)
            if v.is_valid(jsondata):
                validPaper.append(uploadfile)
                print("validFile:"+uploadfile.name)
            else:

                print("invalidFile:" + uploadfile.name)
                errors=[]
                for error in sorted(v.iter_errors(jsondata), key=str):
                    errors.append(error)
                    #print(error)
                #print(json.dumps(jsondata))
                invalidPaper.append({'filename':uploadfile,'data': json.dumps(jsondata),'errors':errors})
            #save the paper
            #fs = FileSystemStorage()
            #filename = fs.save(myfile.name, myfile)

        #currentJsonfiles=request.FILES.getlist('JsonPaper')
        testfiles=None
        context={'validPaper':validPaper,'invalidPaper':invalidPaper,'filestest':testfiles}
        return render(request, 'uploadSummary.html', context)

def completeUpload(request):
    if request.method == 'GET':
        global currentJsonfiles
        print("Jsonfiles")
        print(currentJsonfiles)
        for jsonfile in currentJsonfiles:
            print(jsonfile)
        currentJsonfiles=[]
        print("Alle files sollen jetzt gespeichert werden")
        return render(request, 'ergebnis.html')


@csrf_exempt
def uploadImprovedPaper(request):
    if request.method == 'POST':
        global currentJsonfiles
        print(request.POST)
        filename=request.POST.get('filename')
        response = {}
        filedata=request.POST.get('file')
        jsondata = json.loads(filedata)
        json_data = open("Paperschema.json", "r")
        schema = json.load(json_data)
        v = Draft4Validator(schema)

        if v.is_valid(jsondata):
            print("validFile:" + filename)
            response['valid'] = 'true'
            response['filename'] = filename
            currentJsonfiles.append(jsondata)
        else:
            print("invalidFile:" + filename)
            response['valid'] = 'false'
            response['errors'] = []
            for error in sorted(v.iter_errors(jsondata), key=str):
                response['errors'].append(str(error))
                print(error)
            response['filename'] = filename
            response['data'] = jsondata
            #response['errors'] = errors

        return JsonResponse(response)

'''
