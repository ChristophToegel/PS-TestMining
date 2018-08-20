from nltk.corpus import stopwords
from textMining.models import StemmedText
from nltk.tokenize import RegexpTokenizer

method="nltk stopwordlist: english"

def removeStopwords(paper):
    # paper.update(set__abstract__stemmedText=stemmedText)
    # Abstract
    for index,section in enumerate(paper.abstract):
        print("stemmed:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            print('notStemmend')
            stemmedText= StemmedText.objects.create(text=getStopwordsForTextsection(section.text),method=method)
            paper.abstract[index].stemmedText.append(stemmedText)

    #Text
    for indexSection,section in enumerate(paper.text):
        print("stemmed:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            stemmedText = StemmedText.objects.create(text=getStopwordsForTextsection(section.text), method=method)
            paper.text[indexSection].stemmedText.append(stemmedText)

        #Subtext
        for indexSubsection,subsection in enumerate(section.subsection):
            print("stemmed:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                stemmedText = StemmedText.objects.create(text=getStopwordsForTextsection(subsection.text), method=method)
                paper.text[indexSection].subsection[indexSubsection].stemmedText.append(stemmedText)
    paper.save()


#Stopwortliste nltk(english) word to lowercase
def getStopwordsForTextsection(text):
    text = RegexpTokenizer(r'\w+').tokenize(text) #Satzzeichen weg?
    #print("text:"+text)
    textnostop = ""
    for word in str(text).split():
        word = word.lower()
        if word not in stopwords.words('english'):
            textnostop+=" "+word
    return textnostop

#checks if section has StemmedText with this method
def paperIsRehashed(section):
    if section.stemmedText:
        for stemmedText in section.stemmedText:
            if stemmedText.method==method:
                return True
    else:
        return False