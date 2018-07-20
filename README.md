# PS-TextMining
Frei zugängliche wissenschaftliche Textsorten verschiedener Fachbereiche solle akquirieret werden und mit Methoden des Text Mining verglichen werden

#### Allgemeine Installationsvorraussetzungen:

Die Anwendung erfordert Python3 und eine lokale mongoDB Installation.

######verwendete Bibliotheken:

* [requests](http://docs.python-requests.org/en/master/) (sudo pip(3) install requests)
* [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) (sudo pip(3) install bs4)
* [django](https://www.djangoproject.com) (sudo pip(3) install django) 
* [mongoengine](http://docs.mongoengine.org) (sudo pip(3) install mongoengine)

######MongoDB installation:
[Zur Installationsanleitung von MongDB](https://docs.mongodb.com/manual/administration/install-community/)


#### Start der Anwendung: 
Schritt1: MongoDB mit dem Befehl "mongod" im Terminal starten \
Schritt2: Django starten im Projektordner mit dem Befehl "python(3) manage.py runserver 8000" \
Schritt3: im Browser http://127.0.0.1:8000/textMining