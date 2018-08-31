from textMining.models import ResPunctSegmentCount
import re

method="citationcount"

def citation_count_per_section_Paper(paper):
    # Abstract
    for index,section in enumerate(paper.abstract):
        print("punctCount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            punctCount= ResPunctSegmentCount.objects.create(punctCount=MET_punctuation_count(section))
            paper.abstract[index].metrik.punctCountResults = punctCount

    #Text
    for indexSection,section in enumerate(paper.text):
        print("punctCount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            punctCount = ResPunctSegmentCount.objects.create(punctCount=MET_punctuation_count(section))
            paper.text[indexSection].metrik.punctCountResults = punctCount

        #Subtext
        for indexSubsection,subsection in enumerate(section.subsection):
            print("punctCount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                punctCount = ResPunctSegmentCount.objects.create(punctCount=MET_punctuation_count(subsection))
                paper.text[indexSection].subsection[indexSubsection].metrik.punctCountResults = punctCount
    paper.save()


#Count punctuation without citations
def MET_punctuation_count(text):
    #Remove quotes
    finding = re.findall(r'(?<!\[[0-9])[.,\/#!?\^&\*;:{}=\-_`~“”\"()]', text)
    return str(len(finding))


#checks if section has Wordcount with this method
def paperIsRehashed(section):
    return False


