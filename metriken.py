
def calculateWords(Paper):
    #calculate for Abschnitte
    #print(Paper.text)
    response={}
    total=0
    for index,text in enumerate(Paper.text):
        #print(text.title)
        #print(len(text.title))
        #print(text.text)
        total+=len(text.title)
        total+=len(text.text)
        response['abschnitt'+str(index)]=len(text.text)+len(text.title)
    response['total']=total
    return response