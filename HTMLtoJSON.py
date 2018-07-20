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
                output['text'] = getSelectionText(htmlfile)

                print("output")
                print(output)

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
            #print("referenesElement")
            #print(str(reference.contents[1]))

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

    #print("referenes")
    #print (references)
    return references


def getKeywords(htmlfile):
    #print("keywords")
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
    #print(keywords)
    return keywords


def getJournalTitle (htmlfile):
    journalTitle = EMPTYJSONTAG
    titleEl = htmlfile.find("meta" ,{"name":"citation_journal_title"})
    if titleEl != None and titleEl != -1:
       journalTitle = titleEl['content']

    return journalTitle


def getPaperType (htmlArticle):
    paperType = EMPTYJSONTAG

    container = htmlArticle.find("div", {"class": "col-xs-12 col-sm-9"})
    if container != -1 and container != None:
        paperType = str(container.ul.li.contents[0]).strip()


    return paperType



def getYear(htmlfile):
    #print('year')
    year=htmlfile.find("meta", {"name": "citation_year"})['content']
    #print(year)
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
    #print("Abstract")
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
                list.append({'title':EMPTYJSONTAG,'text':section,'index':index})
        #ohne Absatz
        else:
            list = {'title': EMPTYJSONTAG, 'text': abstract.text}
    else:
        list = {'title': EMPTYJSONTAG, 'text': EMPTYJSONTAG}
    #print(list)
    return list

def getMetadata(htmlfile,category,source):
    output={}
    output['keywords']=getKeywords(htmlfile)
    output['yearOfArticle']=getYear(htmlfile)
    output['journaltitle']=getJournalTitle(htmlfile)
    output['category']=category
    output['source']=source
    output['paperType'] = getPaperType(htmlfile)
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

            #print("finding")
            #print(authorEl.next_element.next_element.find('a'))

            if not (authorEl.next_element.next_element.find('a') != None or authorEl.next_element.next_element.find('a') != -1) and authorEl.next_sibling and str(authorEl.next_element.next_element.find('a').contents[0]) != '*':
                universityIndex = authorEl.next_element.next_element.a.string
                university = htmlArticle.dl.find('dd', id="a" + universityIndex)
                universityCountry = str(university.contents[-1]).split(',')[-1].strip()

                print("XXCountry")
                print(universityCountry)

                if university.find('a', title=True):
                    universityName = str(university.find('a', href=True)['title'])
                else:
                    universityName = str(university.contents[-1].split(',')[0] + ", " + str(university.contents[-1].split(',')[1]))
            # All authors are from the same university therefore no numbers
            else:
                university = htmlArticle.dl.find('dd', id="a1")
                universityCountry = str(university.contents[-1]).replace(",","").strip()
                #print("university")
                #print(university.contents)
                if university.find('a', title=True):
                    universityName = str(university.find('a', href=True)['title'])
                else:
                    universityName = str(university.contents[0]).split(',')[0]

            author['university'] = {"universityName": universityName, "universityCountry": universityCountry}
            authorsOutput['authorList'].append(author)
            authorsOutput['count'] = index

    #print(authorsOutput)
    return authorsOutput


def getSelectionText(htmlArticle):
    h4array=[]
    subsection=[]
    title=""
    text=""
    for section in htmlArticle.findAll("h4"):
        #neuerh4 gefunden --> speichern
        if section.text=="References":
            continue
        if title!="" and text!="":
            dataImages=getImages(section.findNext())
            dataFormula= ""#getFormula(section.findNext())
            dataTables = getTables(section.findNext())
            h4array.append({"title": title, "text": text,'subsection':subsection,'tables':dataTables,'pictures':dataImages,'formula':dataFormula})
            print('save h4section')
        print("titel:" + section.text)
        subsection = []
        title = section.text
        text = ""
        innertitle = ""
        innertext = ""
        subsectionfound=False

        #alle untertags bis zum nächsten h4 <div class="text-justify">....</div>
        #<div class="table-responsive"> to get table  <div class="card card-block card-header mb-2"> bilder
        print(section.findNext())
        #print(section.findAll('p'))
        for element in section.findNext():
            print("element")
            print(element)
            if element.name == 'p' and not element.find("strong"):
                print("p ohne strong")
                #print(element)
                if subsectionfound:
                    innertext+=element.get_text()
                else:
                    text=text+element.get_text()
                #h4array.append({"titel": title, "text": element.get_text()})

            elif element.name == 'p' and element.find("strong") and not element.find("strong")==-1:
                # none wenns vorkommt -1 wenn nicht
                if element.contents[0].find("strong")!=-1 :
                    print("unterüberschrift found")
                    subsectionfound = True
                    if innertitle != "" and innertext != "":
                        subsection.append({"title": innertitle, "text": innertext, 'subsubsection': []})
                    innertitle = element.find("strong").text
                    innertext = ""
                else:
                    #if subsectionfound:
                    innertext += element.get_text()
                    #else:
                    #    text = text + element.get_text()
                    print("tabelle oder bild referenziert --> hinzufügen")


    return h4array


def getTables(section):
    print("tablesection")

    sectionTableData = {"count": 0, "tablesList": []}
    for element in section.findNext():
        print("Hällo")
        #class ="card card-block card-header mb-2
        print(element)
        if element.name == "div" and "table-responsive" in element['class']:

            print("tableStart")

            sectionTableData['count'] += 1
            description = EMPTYJSONTAG

            print(element.find("tr").contents)

            rows = len(element.find_all("tr"))

            colsArray = element.find("tr").contents

            while '\n' in colsArray: colsArray.remove('\n')
            cols = len(colsArray)

            print("sauber")
            print(colsArray)

            print("näcshtes")
            print(element.findNext())
            print("näcshtes ENDE")

            tableData = {"index": sectionTableData['count'], "tableRowDim": rows, "tableColDim": cols, "tableDescription": description}
            sectionTableData['tablesList'].append(tableData)

            print(sectionTableData)
            print("table gefunden")
            print("tablesection ENDE")

    return sectionTableData

def getImages(section):
    print("picturesection")

    sectionPictureData = {"count": 0, "picturesList": []}
    for element in section.findNext():
        print(element)
        if element.name == "div" and "card" in element['class']:
            print("pictureStart")

            print(element)

            sectionPictureData['count'] += 1
            description = EMPTYJSONTAG

            print(element.find("tr").contents)

            print("näcshtes")
            print(element.findNext())
            print("näcshtes ENDE")

            pictureData = {"index": sectionPictureData['count'], "pictureDescription": description}
            sectionPictureData['picturesList'].append(pictureData)

            print(sectionPictureData)
            print("picture gefunden")
            print("picturesection ENDE")
    return sectionPictureData

def getFormula(section):
    return""




parseHTML()
#readJsonFiles()