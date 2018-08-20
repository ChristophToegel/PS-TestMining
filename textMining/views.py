# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from .models import Text, Subsection, Reference, References, Paper, Author, Metadata, Authors, University, Abstract, \
    Picture, Pictures, Table, Tables
import json
from django.shortcuts import redirect
from os import listdir
from os.path import join
import metriken
from jsonschema import Draft4Validator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import ast

def calculateMetriken(request):
    papers = Paper.objects.all()
    for paper in papers:
        words=metriken.calculateWords(paper)
        print(words)
    # save words in DB
    context = {'info': 'metriken werden berechnet'}
    return render(request, 'Startseite.html', context)

def calculateFreqWords(request):
    corpus1=metriken.calculateWordFrequency(Paper.objects.filter(metaData__category='Food & Nutrition'))
    #print(corpus1)
    corpus2 = metriken.calculateWordFrequency(Paper.objects.filter(metaData__category='Mathematics'))
    #print(corpus2)
    return render(request, 'freqWords.html', {"corpus1":corpus1,"corpus2":corpus2})


def showStartPage(request):
    return render(request, 'Startseite.html')


def readJsonFiles(request):
    # loads all Json files....
    readpath = "./output"
    onlyOne = False
    counter=0
    for filename in listdir(readpath):
        if not onlyOne:
            if filename != ".DS_Store": #file.endswith('.json')
                file = open(join(readpath, filename), 'r', encoding='utf-8', errors="ignore")
                paper = json.load(file)
                print(file)
                print(counter)
                # create paper form jsonfile
                # create Authors
                if paper.get('authors'):
                    arrayAutoren = []
                    for autor in paper['authors']['authorList']:
                        arrayAutoren.append(
                            Author.objects.create(authorName=autor['authorName'], authorIndex=autor['authorIndex'],
                                                  university=University.objects.create(
                                                      university_universityName=autor['university']['universityName'],
                                                      university_universityCountry=autor['university'][
                                                          'universityCountry'])))
                    authors = Authors.objects.create(count=paper['authors']['count'], authorList=arrayAutoren)
                else:
                    authors=None

                # metadata
                if paper['metaData']:
                    if paper['metaData'].get('keywords'):
                        keywords=paper['metaData']['keywords']
                    else:
                        keywords=None

                    metaDatavalue = Metadata.objects.create(keywords=keywords,
                                                        yearOfArticle=paper['metaData']['yearOfArticle'],
                                                        category=paper['metaData']['category'],
                                                        source=paper['metaData']['source'],
                                                        journalTitle = paper['metaData']['journaltitle'],
                                                        impactfactor = paper['metaData']['impactFactor'],
                                                        URL=paper['metaData']['URL'],
                                                        paperType=paper['metaData']['paperType']
                                                        )
                else:
                    metaDatavalue=None

                # create Abstract
                #print("abstract")
                #Todo paper sollte immer Array sein( auch bei titel=empty and text=empty) <<empty>>
                abstractArray=[]
                if isinstance(paper['abstract'], list):
                    for abstractPart in paper['abstract']:
                        print(abstractPart)
                        abstractArray.append(Abstract.objects.create(title=abstractPart['title'],text=abstractPart['text']))
                else:
                    if not paper['abstract']=='<<empty>>':
                        abstractArray.append(Abstract.objects.create(title=paper['abstract']['title'], text=paper['abstract']['title']))

                if paper.get('references'):
                    # create Reference
                    arrayReferences = []
                    for reference in paper['references']['referencesList']:
                        arrayReferences.append(Reference.objects.create(referenceIndex=reference['referenceIndex'],
                                                                        referenceName=reference['referenceName'],
                                                                        referenceAuthor=reference['referenceAuthor'],
                                                                        referenceYear=str(reference['referenceYear'])))
                    references = References.objects.create(count=paper['references']['count'], referencesList=arrayReferences)
                else:
                    references=None

                # createText todo tabellen und bilder an models anpassen!
                TextArray = []
                for textsection in paper['text']:
                    subTextArray = []
                    # tables
                    arrayTables = []
                    if textsection['tables']:
                        for table in textsection['tables']['tablesList']:
                            arrayTables.append(
                                Table.objects.create(tableIndex=table['index'], tableRowDim=table['tableRowDim'],
                                                     tableCodDim=table['tableColDim'],
                                                     tableDescription=table['tableDescription']))
                        tables = Tables.objects.create(count=textsection['tables']['count'], tablesList=arrayTables)
                    else:
                        tables=None
                    # pictures
                    arrayPictures = []
                    if textsection['pictures']:
                        for picture in textsection['pictures']['picturesList']:
                            arrayTables.append(
                                Picture.objects.create(pictureIndex=picture['index'], pictureDescription=picture[
                                    'pictureDescription']))
                        pictures = Pictures.objects.create(count=textsection['pictures']['count'], picturesList=arrayPictures)
                    else:
                        pictures = None

                    if textsection['subsection']:
                        for subsection in textsection['subsection']:
                            subTextArray.append(
                                Subsection.objects.create(title=subsection['title'], text=subsection['text']))
                    TextArray.append(
                        Text.objects.create(title=textsection['title'], text=textsection['text'], subsection=subTextArray,
                                            tables=tables, pictures=pictures,
                                            #formula=textsection['formula']
                                            ))

                Paper.objects.create(title=paper['title'], metaData=metaDatavalue, authors=authors,
                                                abstract=abstractArray,
                                                references=references, text=TextArray)

                counter+=1
        onlyOne=False


    #print(newpaper)
    paperlist=Paper.objects.all()[:10]
    kategorien=Metadata.objects.distinct('category')
    journalnames=Author.objects.distinct('authorName')
    print(kategorien)
    #3296
    context = {'paperlist': paperlist}
    return render(request, 'Helloworld.html', context)


#Aufbereiten der Text Stopwortfiltern und lemmatisieren
def processPaper(request):
    print("Paper werden aufbreitet....")
    paperlist = Paper.objects.all()[:20]
    for paper in paperlist:
        metriken.removeStopwords(paper)
    context = {'paperlist': paperlist}
    return render(request, 'Helloworld.html', context)


def uploadFiles(request):
    if request.method == 'GET':
        return render(request, 'Upload.html')

    if request.method == 'POST':
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
            if v.is_valid(jsondata):
                validPaper.append(uploadfile)
                print("validFile:"+uploadfile.name)
            else:

                print("invalidFile:" + uploadfile.name)
                errors=[]
                for error in sorted(v.iter_errors(jsondata), key=str):
                    errors.append(error)
                    print(error)
                #print(json.dumps(jsondata))
                invalidPaper.append({'filename':uploadfile,'data': json.dumps(jsondata),'errors':errors})
            #save the paper
            #fs = FileSystemStorage()
            #filename = fs.save(myfile.name, myfile)

        context={'validPaper':validPaper,'invalidPaper':invalidPaper}
        return render(request, 'UploadSummary.html',context)

@csrf_exempt
def uploadImprovedPaper(request):
    if request.method == 'POST':
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
