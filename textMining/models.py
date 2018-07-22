from django.db import models

# Create your models here.
from mongoengine import *

#http://docs.mongoengine.org
connect('textmining')

class Tables(Document):
    count = IntField()
    tablesList=EmbeddedDocumentListField('Table')

class Table(Document):
    tableIndex = IntField()
    tableRowDim = IntField()
    tableCodDim = IntField()
    tableDescription = StringField()

class Pictures(Document):
    count = IntField()
    picturesList=EmbeddedDocumentListField('Picture')

class Picture(Document):
    pictureIndex = IntField()
    pictureDescription = StringField()

class Subsection(Document):
    title = StringField()
    text = StringField()
    subsubsection = ListField()

class Text(Document):
    title = StringField()
    text = StringField()
    subsection = EmbeddedDocumentListField('Subsection')
    tables = EmbeddedDocumentField('Tables')
    pictures = EmbeddedDocumentField('Pictures')
    formulas = StringField() #String weil leer und nicht 0

class Reference(Document):
    referenceIndex = IntField()
    referenceName = StringField()
    referenceAuthor = StringField()
    referenceYear = StringField()

class References(Document):
    count = IntField()
    referencesList = EmbeddedDocumentListField('Reference')

class University(Document):
    university_universityName = StringField()
    university_universityCountry = StringField()

class Author(Document):
    authorName = StringField()
    authorIndex = IntField()
    university = EmbeddedDocumentField('University')

class Authors(Document):
    count = IntField()
    authorList = EmbeddedDocumentListField('Author')

class Abstract(Document):
    title = StringField()
    text = StringField()

class Metadata(Document):
    keywords = ListField()
    yearOfArticle = IntField()
    category = StringField()
    source = StringField()

class Paper(Document):
    title = StringField()
    metaData = EmbeddedDocumentField('Metadata')
    abstract = EmbeddedDocumentField('Abstract')
    authors = EmbeddedDocumentField('Authors')
    references = EmbeddedDocumentField('References')
    text = EmbeddedDocumentListField('Text')