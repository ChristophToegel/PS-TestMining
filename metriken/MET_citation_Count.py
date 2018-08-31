from textMining.models import ResCitationSegmentCount
import re

method="citationcount"

def citation_count_per_section_Paper(paper):
    # Abstract
    for index,section in enumerate(paper.abstract):
        print("punctCount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            citCount= ResCitationSegmentCount.objects.create(citationCount=MET_citation_count(section))
            paper.abstract[index].metrik.citationCountResults = citCount

    #Text
    for indexSection,section in enumerate(paper.text):
        print("punctCount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            citCount = ResCitationSegmentCount.objects.create(citationCount=MET_citation_count(section))
            paper.text[indexSection].metrik.citationCountResults = citCount

        #Subtext
        for indexSubsection,subsection in enumerate(section.subsection):
            print("punctCount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                citCount = ResCitationSegmentCount.objects.create(citationCount=MET_citation_count(subsection))
                paper.text[indexSection].subsection[indexSubsection].metrik.citationCountResults = citCount
    paper.save()


#Count punctuation without citations
def MET_citation_count(text):
    finding = re.findall(r'\[[^]]*\]', text)
    quoteCount = 0
    for quote in finding:
        if "-" in quote:
            quotes = quote.replace("[","").replace("]","").split("-")
            while "-" in quotes: quotes.remove("-")
            quoteCount += (int(quotes[1]) -int(quotes[0])) + 1
        elif "," in quote:
            quotes = (quote.split(","))
            while "," in quotes: quotes.remove(",")
            quoteCount += len(quotes)
        else:
            quoteCount += 1

    return str(quoteCount)

#checks if section has Wordcount with this method
def paperIsRehashed(section):
    return False


