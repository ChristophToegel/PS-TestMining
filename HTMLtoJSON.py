from bs4 import BeautifulSoup
import json
from os import listdir
from os.path import isfile, join
import os
from os.path import basename

htmlfilesdirectory='corpusRawHTML'
outputdirectory='output'
#open file
for file in listdir(htmlfilesdirectory):
    if isfile(join(htmlfilesdirectory, file)) and file.endswith('.html'):
        file = open(join(htmlfilesdirectory, file))
        print('parse file: '+ file.name)

        htmlfile = BeautifulSoup(file, 'html.parser')
        output = {}
        htmlarticle=htmlfile.article
        #print(htmlarticle)

        title = htmlarticle.find("h1")
        print(title.text)

        output['title'] = title.text

        #output['test'] = "Hello world"
        name=os.path.splitext(basename(file.name))[0]
        file = open(join(outputdirectory, name+'.json'), 'w')
        json.dump(output, file)
        file.close()
