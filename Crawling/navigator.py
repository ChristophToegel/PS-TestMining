# -*- coding: utf-8 -*-

'''
First of all, we need to navigate through omicsonline
--> pip install selenium
'''
from selenium import webdriver

driver = webdriver.Safari()
driver.get("https://www.omicsonline.org/archive-vaccines-vaccination-open-access.php") # = URL of Journal

links = []
links.append(driver.find_elements_by_class_name("nav-link col-12 col-sm-4"))

for i in len(links):
    links[i].click()

driver.close()