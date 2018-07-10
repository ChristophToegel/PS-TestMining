from bs4 import BeautifulSoup
import json
import re
from bs4 import Tag
from os import listdir,path
from os.path import isfile, join,basename

EMPTYJSONTAG = "<<empty>>"


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
                output['authors'] = getAuthors(htmlarticle)
                output['references'] = getallReferences(htmlarticle)

                name = path.splitext(basename(file.name))[0]
                file = open(join(outputdirectory, name + '.json'), 'w', encoding='utf-8')
                json.dump(output, file,ensure_ascii=False)
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
    references = {"count": 0, "referencesList": []}
    referencesElement = htmlArticle.find_all("li", id="Reference_Titile_Link")  # .next_element
    if (referencesElement):
        for reference in referencesElement:
            print("referenesElement")
            print(str(reference.contents[1]))

            #get year
            matchYear = re.search(r'[(][0-9]{4}[)]', str(reference.contents[1]))
            refYear = EMPTYJSONTAG
            if matchYear:
                refYear = int(str(matchYear.group())[1:-1])

            #get author
            refAuthorName = EMPTYJSONTAG
            if "<" not in str(reference.contents[1]):
                refAuthorName = str(reference.contents[1])

            references["count"] += 1
            referenceData ={"referenceIndex": int(reference.a['id']), "referenceName": str(reference.contents[-1].string), "referenceAuthor": refAuthorName, "referenceYear": refYear}
            references["referencesList"].append(referenceData)

    print("referenes")
    print (references)
    return references


def getKeywords(htmlfile):
    print("keywords")
    keywords=[]
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

def getAbstractText(abstract):
    result = []
    text = ""
    titel = ""
    #print(data.text.splitlines())
    for tag in abstract.findAll():
        #print(tag.name)
        if tag.name=="strong":
            if titel == "" and tag.text!=":":
                titel=tag.text
                text=tag.next_sibling
                #print(tag.next_sibling)
            elif tag.text!=":":
                #print(tag.text)
                titel=titel.strip().replace(":","")
                text=text.strip()
                result.append({"title":titel,"text":text,"depth":1})
                #print('section: '+ "title:"+ titel+"text: "+text)
                titel=tag.text
                text=tag.next_sibling
            else:
                text = tag.next_sibling
        elif not (tag.name == "br" or tag.name =="p"):
            #print("sgtrzjtukziluikhjg")
            #print(tag.name)
            if tag.text and tag.next_sibling:
                text=text+tag.text
            if tag.next_sibling:
                text = text + tag.next_sibling
    result.append({"title": titel, "text": text, "depth": 1})
    return result

def getAbstract(htmlArticle):
    #find abstract
    print("Abstract")
    for div in htmlArticle.findAll('div'):
        if div.find('h3'):
            container=div.find('h3')
            if container.text and container.text=="Abstract":
                break
    abstract = div.find('p').find('p')

    if abstract:
        #Absätze mit überschriften
        if abstract.find('strong'):
            list=[]
            list = getAbstractText(abstract)
        #Absätze ohne überschriften
        elif abstract.find('br'):
            list = []
            #print(abstract.text.splitlines())
            for index,section in enumerate(abstract.text.splitlines()):
                #print(section)
                list.append({'title':'<no Title>','text':section,'index':index})
        #ohne Absatz
        else:
            list = {'title': '<no Title>', 'text': abstract.text}
    else:
        list = {'title': '<no Title>', 'text': '<no Abstract>'}
    print(list)
    return list

def getMetadata(htmlfile,category,source):
    output={}
    output['keywords']=getKeywords(htmlfile)
    output['yearOfArticle']=getYear(htmlfile)
    output['category']=category
    output['source']=source
    return output

def getAuthors(htmlArticle):
    authorsOutput = {'count': None, 'authorList': []}
    authorListHTML = htmlArticle.dl.dt.find_all('a')

    index = 0
    for authorEl in authorListHTML:
        author = {}
        if authorEl.has_attr('title'):
            author['authorName'] = authorEl['title'].strip()
            author['authorIndex'] = index = index + 1

            print("finding")
            print(authorEl.next_element.next_element.find('a'))

            if not (authorEl.next_element.next_element.find('a') != None or authorEl.next_element.next_element.find('a') != -1) and authorEl.next_sibling and str(authorEl.next_element.next_element.find('a').contents[0]) != '*':
                universityIndex = authorEl.next_element.next_element.a.string
                university = htmlArticle.dl.find('dd', id="a" + universityIndex)
                universityCountry = str(university.contents[-1]).split(',')[-1].strip()
                if university.find('a', title=True):
                    universityName = str(university.find('a', href=True)['title'])
                else:
                    universityName = str(university.contents[-1].split(',')[0] + ", " + str(university.contents[-1].split(',')[1]))
            # All authors are from the same university therefore no numbers
            else:
                university = htmlArticle.dl.find('dd', id="a1")
                universityCountry = str(university.contents[-1]).replace(",","").strip()
                print("university")
                print(university.contents)
                if university.find('a', title=True):
                    universityName = str(university.find('a', href=True)['title'])
                else:
                    universityName = str(university.contents[0]).split(',')[0]

            author['university'] = {"universityName": universityName, "universityCountry": universityCountry}
            authorsOutput['authorList'].append(author)
            authorsOutput['count'] = index

    print(authorsOutput)
    return authorsOutput


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
    # search if inner section --> getSelection(htmlArticle)
    pass

parseHTML()
#readJsonFiles()