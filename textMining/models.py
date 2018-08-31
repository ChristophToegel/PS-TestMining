from django.db import models

# Create your models here.
from mongoengine import *

# http://docs.mongoengine.org
connect('textmining')

# TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!!
class TextVariant(Document):
    text = StringField()
    method = StringField()

# METRIK RESULTS !!! METRIK RESULTS !!! METRIK RESULTS !!! METRIK RESULTS !!! METRIK RESULTS !!! METRIK RESULTS !!!


class ResCharSegmentCount(Document):
    charCountWhiteSpace = StringField(default= "0")
    charCountNoWhiteSpace = StringField(default = "0")

class ResWordSegmentCount(Document):
    wordCount = StringField(default= "0")

class ResPunctSegmentCount(Document):
    punctCount = StringField(default= "0")

class ResCitationSegmentCount(Document):
    citationCount = StringField(default= "0")



class Metric(Document):
    charCountResults = EmbeddedDocumentField('ResCharSegmentCount')
    wordCountResults = EmbeddedDocumentField('ResWordSegmentCount')
    punctCountResults = EmbeddedDocumentField('ResPunctSegmentCount')
    citationCountResults = EmbeddedDocumentField('ResCitationSegmentCount')


class Tables(Document):
    count = IntField()
    tablesList = EmbeddedDocumentListField('Table')


class Table(Document):
    tableIndex = IntField()
    tableRowDim = IntField()
    tableCodDim = IntField()
    tableDescription = StringField()


class Pictures(Document):
    count = IntField()
    picturesList = EmbeddedDocumentListField('Picture')


class Picture(Document):
    pictureIndex = IntField()
    pictureDescription = StringField()


class Subsection(Document):
    title = StringField()
    text = StringField()
    stopFilteredText = EmbeddedDocumentField('TextVariant')
    lemmatizedText = EmbeddedDocumentField('TextVariant')
    metrik = EmbeddedDocumentField('Metric', null = True)
    subsubsection = ListField()


class Text(Document):
    title = StringField()
    text = StringField()
    stopFilteredText = EmbeddedDocumentField('TextVariant')
    lemmatizedText = EmbeddedDocumentField('TextVariant')
    metrik = EmbeddedDocumentField('Metric', null = True)
    subsection = EmbeddedDocumentListField('Subsection')
    tables = EmbeddedDocumentField('Tables')
    pictures = EmbeddedDocumentField('Pictures')
    formulas = StringField()  # String weil leer und nicht 0



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
    stopFilteredText = EmbeddedDocumentField('TextVariant')
    lemmatizedText = EmbeddedDocumentField('TextVariant')
    metrik = EmbeddedDocumentField('Metric', null = True)


class Metadata(Document):
    keywords = ListField()
    yearOfArticle = IntField()
    category = StringField()
    source = StringField()
    journalTitle = StringField()
    impactfactor = StringField()
    URL=StringField()
    paperType=StringField()
    # Erweiterungen
    documenttype = StringField()
    publisher = StringField()
    publishingCompany = StringField()
    pages = IntField()
    excerptPages = StringField()
    publicationLocation = StringField()


class Paper(Document):
    title = StringField()
    metaData = EmbeddedDocumentField('Metadata')
    abstract = EmbeddedDocumentListField('Abstract')
    authors = EmbeddedDocumentField('Authors')
    references = EmbeddedDocumentField('References')
    text = EmbeddedDocumentListField('Text')

