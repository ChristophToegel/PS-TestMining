from nltk.corpus import stopwords
from textMining.models import TextVariant
from nltk.tokenize import RegexpTokenizer

method="nltk stopwordlist: english"

def removeStopwords(paper):
    # Abstract
    for index,section in enumerate(paper.abstract):
        print("stopFiltered:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            print('NotstopFiltered')
            print(getStopwordsForTextsection(section.text))
            stopWordFilteredText_String = TextVariant.objects.create(text=getStopwordsForTextsection(section.text),method=method)
            paper.abstract[index].stopFilteredText = (stopWordFilteredText_String)

    #Text
    for indexSection,section in enumerate(paper.text):
        print("stopFiltered:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            stopWordFilteredText_String = TextVariant.objects.create(text=getStopwordsForTextsection(section.text), method=method)
            paper.text[indexSection].stopFilteredText = (stopWordFilteredText_String)

        #Subtext
        for indexSubsection,subsection in enumerate(section.subsection):
            print("stopFiltered:"+str(paperIsRehashed(subsection)))
            if not paperIsRehashed(subsection):
                stopWordFilteredText_String = TextVariant.objects.create(text=getStopwordsForTextsection(subsection.text), method=method)
                print ("String hier")
                print (stopWordFilteredText_String)
                paper.text[indexSection].subsection[indexSubsection].stopFilteredText = (stopWordFilteredText_String)
    paper.save()

#Stopwortliste nltk(english) word to lowercase
def getStopwordsForTextsection(text):
    text_As_Array = RegexpTokenizer(r'\w+').tokenize(text) #Satzzeichen weg?
    #print("text:"+text)
    textnostop = ""
    for word in text_As_Array:
        word = str(word).lower()
        if word not in stopwords.words('english'):
            textnostop += " " + word

    print(textnostop)
    return textnostop

#checks if section has StemmedText with this method
def paperIsRehashed(section):
    return False
    """
    if section.stopFilteredText:
        for stopFilteredText in section.stopFilteredText:
            print("Hier")
            print (stopFilteredText)

            if stopFilteredText.method == method and stopFilteredText.text != "":
                print ("stopFilteredText Text Hier")
                print (stopFilteredText.text)
                return True
            else:
                return False
    else:
        return False"""