from textMining.models import ResWordSegmentCount
import re

method="sentsCount"


def punctation_count_per_section_Paper(paper):
    # Abstract
    for index,section in enumerate(paper.abstract):
        print("sentsCount" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            sentsCount= ResWordSegmentCount.objects.create(sentsCount=MET_sents_count(section))
            paper.abstract[index].metrik.wordCountResults = sentsCount

    #Text
    for indexSection,section in enumerate(paper.text):
        print("sentsCount" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            sentsCount = ResWordSegmentCount.objects.create(sentsCount=MET_sents_count(section))
            paper.abstract[index].metrik.wordCountResults = sentsCount

        #Subtext
        for indexSubsection,subsection in enumerate(section.subsection):
            print("sentsCount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                sentsCount = ResWordSegmentCount.objects.create(sentsCount=MET_sents_count(section))
                paper.abstract[index].metrik.wordCountResults = sentsCount
    paper.save()



def MET_sents_count(text):
    #Remove quotes
    sents = text.split('.')
    avg_len = sum(len(x.split()) for x in sents) / len(sents)



def paperIsRehashed(section):
    return False


