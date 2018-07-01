from bs4 import BeautifulSoup
import json
from os import listdir,path
from os.path import isfile, join,basename


def parseHTML():
    htmlfilesdirectory = 'corpusRawHTML'
    outputdirectory = 'output'
    source = 'omics'
    # open file
    readpathbasic=path.join(htmlfilesdirectory,source)
    for categoryFolder in listdir(readpathbasic):
        print(categoryFolder)
        test = 0
        readpath=path.join(readpathbasic,categoryFolder)
        for file in listdir(readpath):
            #print(file)
            #categoryDirectory=path.join(outputdirectory,folder)
            if isfile(join(readpath, file)) and file.endswith('.html') and test<=2:
                file = open(join(readpath, file))
                print('parse file: ' + file.name)

                htmlfile = BeautifulSoup(file, 'html.parser')
                output = {}
                htmlarticle = htmlfile.article
                output['title'] = getTitel(htmlarticle)
                output['metaData']= getMetadata(htmlfile,categoryFolder,source)
                output['abstract'] = getAbstract(htmlarticle)

                name = path.splitext(basename(file.name))[0]
                file = open(join(outputdirectory, name + '.json'), 'w')
                json.dump(output, file)
                file.close()
                test+=1

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

def getKeywords(htmlfile):
    #Todo unicode Zeichen!
    print("keywords")
    for div in htmlfile.findAll('strong'):
            if div.text and div.text == "Keywords:":
                text=div.text
                keywordsArray = div.parent.text.replace(text,"").strip()
                keywords=keywordsArray.split(";")
                keywords= [keyword.strip(' ') for keyword in keywords]
                break
            else:
                keywords="no Keywords"
    print(keywords)
    return keywords

def getYear(htmlfile):
    print('year')
    year=htmlfile.find("meta", {"name": "citation_year"})['content']
    print(year)
    return int(year)

def getAbstract(htmlArticle):
    #todo nummerierung hinzufügen prüfen, textabschnitte auch mit links und umbrüche
    print("Abstract")
    for div in htmlArticle.findAll('div'):
        if div.find('h3'):
            container=div.find('h3')
            if container.text and container.text=="Abstract":
                #print("Abstract found!!")
                break
    abstract = div.find('p').find('p')
    if abstract:
        #Absätze mit überschriften
        if abstract.find('strong'):
            list=[]
            #list.append({'titel': 'no Titel', 'text': abstract.next_sibling})
            for index,section in enumerate(abstract.findAll('strong')):
                #print(section)
                #print(section.next_sibling)
                list.append({'titel': section.text,'text':section.next_sibling,'index':index})
        #Absätze ohne überschriften
        elif abstract.find('br'):
            list = []
            #print(abstract.text.splitlines())
            for index,section in enumerate(abstract.text.splitlines()):
                #print(section)
                list.append({'title':'no Titel','text':section,'index':index})
        #ohne Absatz
        else:
            list = {'title': 'no Titel', 'text': abstract.text}
        print(list)
    else:
        list = {'title': 'no Titel', 'text': 'no Abstract'}
    return list

def getMetadata(htmlfile,category,source):
    output={}
    output['keywords']=getKeywords(htmlfile)
    output['yearOfArticle']=getYear(htmlfile)
    output['category']=category
    output['source']=source
    return output

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
#readJsonFiles()