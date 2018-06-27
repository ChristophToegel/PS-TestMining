# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    #src: https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


#download html-code and save htmlpage
# src:  https://programminghistorian.org/lessons/working-with-web-pages
def downloadArticles(basefilename, urls_to_get):
    harvested_files = []
    for i in range(0,len(urls_to_get),1):
        response = urllib2.urlopen(urls_to_get[i])
        webContent = response.read()
        current_file_id = i + 1
        filename = basefilename + str(current_file_id) + '.html'
        harvested_files.append(filename)

        f = open(filename, 'w')
        f.write(webContent)
        f.close
    return harvested_files

def prettifyHTML(html_files):

    for i in range(0, len(html_files)):
        file = open(html_files[i], 'w+')
        soup = BeautifulSoup(file, 'html.parser')
        file.write(soup.prettify())
        file.close()


if __name__=='__main__':
    urls_to_get=["http://www.digitalhumanities.org/dhq/vol/11/4/000339/000339.html",
                 "http://www.digitalhumanities.org/dhq/vol/11/4/000340/000340.html"]
    basefilename = 'DHQ_2017_11_4_a'

    html_files = downloadArticles(basefilename, urls_to_get)

