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


def calculateMetriken(request):
    papers = Paper.objects.all()
    for paper in papers:
        words=metriken.calculateWords(paper)
        print(words)
    # save words in DB
    context = {'info': 'metriken werden berechnet'}
    return render(request, 'Startseite.html', context)


def showStartPage(request):
    return render(request, 'Startseite.html')


def readJsonFiles(request):
    # loads all Json files....
    readpath = "./output"
    onlyOne = False
    for filename in listdir(readpath):
        if not onlyOne:
            file = open(join(readpath, filename), 'r')
            paper = json.load(file)
            print(file)
            #paper = json.loads(file)
            # create paper form jsonfile
            # create Authors
            arrayAutoren = []
            for autor in paper['authors']['authorList']:
                arrayAutoren.append(
                    Author.objects.create(authorName=autor['authorName'], authorIndex=autor['authorIndex'],
                                          university=University.objects.create(
                                              university_universityName=autor['university']['universityName'],
                                              university_universityCountry=autor['university'][
                                                  'universityCountry'])))
            authors = Authors.objects.create(count=paper['authors']['count'], authorList=arrayAutoren)

            # metadata
            metaDatavalue = Metadata.objects.create(keywords=paper['metaData']['keywords'],
                                                    yearOfArticle=paper['metaData']['yearOfArticle'],
                                                    category=paper['metaData']['category'],
                                                    source=paper['metaData']['source'])
            # create Abstract
            abstract = Abstract.objects.create(title=paper['abstract']['title'], text=paper['abstract']['text'])

            # create Reference
            arrayReferences = []
            for reference in paper['references']['referencesList']:
                arrayReferences.append(Reference.objects.create(referenceIndex=reference['referenceIndex'],
                                                                referenceName=reference['referenceName'],
                                                                referenceAuthor=reference['referenceAuthor'],
                                                                referenceYear=str(reference['referenceYear'])))
            references = References.objects.create(count=paper['references']['count'], referencesList=arrayReferences)

            # createText todo tabellen und bilder an models anpassen!
            TextArray = []
            for textsection in paper['text']:
                subTextArray = []
                # tables
                arrayTables = []
                if textsection['tables']:
                    for table in textsection['tables']['tablesList']:
                        arrayTables.append(
                            Table.objects.create(tableIndex=table['tableIndex'], tableRowDim=table['tableIndex'],
                                                 tableCodDim=table['tableIndex'],
                                                 tableDescription=table['tableIndex']))
                tables = Tables.objects.create(count=textsection['tables']['count'], tablesList=arrayTables)
                # pictures
                arrayPictures = []
                if textsection['pictures']['picturesList']:
                    for picture in textsection['pictures']['picturesList']:
                        arrayTables.append(
                            Picture.objects.create(pictureIndex=picture['pictureIndex'], pictureDescription=picture[
                                'pictureDescription']))
                pictures = Pictures.objects.create(count=textsection['pictures']['count'], picturesList=arrayPictures)

                if textsection['subsection']:
                    for subsection in textsection['subsection']:
                        subTextArray.append(
                            Subsection.objects.create(title=subsection['title'], text=subsection['text']))
                TextArray.append(
                    Text.objects.create(title=textsection['title'], text=textsection['text'], subsection=subTextArray,
                                        tables=tables, pictures=pictures,
                                        #formula=textsection['formula']
                                        ))

            newpaper = Paper.objects.create(title=paper['title'], metaData=metaDatavalue, authors=authors,
                                            abstract=abstract,
                                            references=references, text=TextArray)
        onlyOne=True
    print(newpaper)
    context = {'paper': newpaper}
    return render(request, 'Helloworld.html', context)
