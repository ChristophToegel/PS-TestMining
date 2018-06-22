from bs4 import BeautifulSoup
import json
from os import listdir,path
from os.path import isfile, join,basename



def parseHTML():
    htmlfilesdirectory = 'corpusRawHTML'
    outputdirectory = 'output'
    # open file
    for file in listdir(htmlfilesdirectory):
        if isfile(join(htmlfilesdirectory, file)) and file.endswith('.html'):
            file = open(join(htmlfilesdirectory, file))
            print('parse file: ' + file.name)

            htmlfile = BeautifulSoup(file, 'html.parser')
            output = {}
            htmlarticle = htmlfile.article
            output['title'] = getTitel(htmlarticle)

            name = path.splitext(basename(file.name))[0]
            file = open(join(outputdirectory, name + '.json'), 'w')
            json.dump(output, file)
            file.close()

def readJsonFiles():
    outputdirectory = 'output'
    for file in listdir(outputdirectory):
        # read json
        print('read file: ' + file)
        name = path.splitext(basename(file))[0]
        file = open(join(outputdirectory, name + '.json'), 'r')
        jsonfile = json.load(file)
        print(jsonfile["title"])



def getTitel(htmlArticle):
    title=htmlArticle.find("h1").text
    if title:
        return title
    else:
        return 'no title found'

def getallReferences(htmlArticle):
    pass

def getKeywords(htmlArticle):
    pass

def getAuthors(htmlArticle):
    pass



def getSelection(htmlArticle):
    getInnerSection(htmlArticle)
    SelectionImages(htmlArticle)
    SelectionTables(htmlArticle)
    SelectionFormeln(htmlArticle)

    getSelectionTitle(htmlArticle)
    getSelectionText(htmlArticle)
    getNumSelectionReferences(htmlArticle)
    pass

def getSelectionTitle(htmlSelection):
    pass

def getSelectionText(htmlSelection):
    pass


def getNumSelectionReferences(htmlArticle):
    pass

def SelectionImages(htmlArticle):
    pass

def SelectionTables(htmlArticle):
    pass

def SelectionFormeln(htmlArticle):
    pass

def getInnerSection(htmlArticle):
    #search if inner section --> getSelection(htmlArticle)
    pass


parseHTML()
readJsonFiles()