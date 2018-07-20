from django.db import models

# Create your models here.
from mongoengine import *

#http://docs.mongoengine.org
connect('test5')

class Subsection(Document):
    title = StringField()
    text = StringField()
    subsubsection = ListField()

class Text(Document):
    title = StringField()
    text = StringField()
    subsection = EmbeddedDocumentListField('Subsection')
    # TODO nicht string?
    tables = StringField()
    pictures = StringField()
    formula = StringField()

class Reference(Document):
    referenceIndex = IntField()
    referenceName = StringField()
    referenceAuthor = StringField()
    referenceYear = IntField()


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
    text = ListField(EmbeddedDocumentField('Text'))