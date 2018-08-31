from textMining.models import ResWordSegmentCount
import re

method="wordcount"

def punctation_count_per_section_Paper(paper):
    # Abstract
    for index,section in enumerate(paper.abstract):
        print("wordcount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            wordCount= ResWordSegmentCount.objects.create(wordCount=MET_word_count(section))
            paper.abstract[index].metrik.wordCountResults = wordCount

    #Text
    for indexSection,section in enumerate(paper.text):
        print("wordcount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            wordCount = ResWordSegmentCount.objects.create(wordCount=MET_word_count(section))
            paper.text[indexSection].metrik.wordCountResults = wordCount

        #Subtext
        for indexSubsection,subsection in enumerate(section.subsection):
            print("wordcount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                wordCount = ResWordSegmentCount.objects.create(wordCount=MET_word_count(subsection))
                paper.text[indexSection].subsection[indexSubsection].metrik.wordCountResults = wordCount
    paper.save()



def MET_word_count(text):
    #Remove quotes
    word_count = len(re.sub(r"(\s\[[^]]*\])", "", text).split(" "))
    return str(word_count)



def paperIsRehashed(section):
    return False


