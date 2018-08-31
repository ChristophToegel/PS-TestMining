# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from .models import Text, Subsection, Reference, References, Paper, Author, Metadata, Authors, University, Abstract, \
    Picture, Pictures, Table, Tables, Metric, ResCitationSegmentCount
import json
from django.shortcuts import redirect
from os import listdir
from os.path import join
import metriken


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

def showVergleichPage(request):
    return render(request, 'vergleich.html')

def showUploadArea(request):
    return render(request, 'upload.html')

def showResults(request):
    return render(request, 'ergebnis.html')

def readJsonFiles(request):
    # loads all Json files....
    readpath = "./output20"
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
                        abstractArray.append(Abstract.objects.create(title=abstractPart['title'],text=abstractPart['text'] ,metrik = Metric.objects.create())) #citationCountResults = ResCitationSegmentCount.objects.create(citationCount = 11) ))
                else:
                    if not paper['abstract']=='<<empty>>':
                        abstractArray.append(Abstract.objects.create(title=paper['abstract']['title'], text=paper['abstract']['title'],metrik = Metric.objects.create()))

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
                                Subsection.objects.create(title=subsection['title'], text=subsection['text'],metrik = Metric.objects.create()))
                    TextArray.append(
                        Text.objects.create(title=textsection['title'], text=textsection['text'],metrik = Metric.objects.create(), subsection=subTextArray,
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
    return render(request, 'old/Helloworld.html', context)


#Aufbereiten der Text Stopwortfiltern und lemmatisieren
def processPaper(request):
    print("Paper werden aufbreitet....")
    paperlist = Paper.objects.all()[:4]
    for paper in paperlist:
        print (paper)
        metriken.removeStopwords(paper)
        metriken.lemmatize_Paper(paper)
        metriken.char_count_per_section_Paper(paper)


    context = {'paperlist': paperlist}
    return render(request, 'old/Helloworld.html', context)


