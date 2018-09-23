"""DjangoTextMining URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from textMining.views import uploadviews, generalviews, downloadviews

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('textMining/<int:pk>/', views.changeCategory),

    path('textMining/readPaper/', generalviews.readJsonFiles),
    path('textMining/processPaper/', generalviews.processPaper),

    path('textMining/calculateMetriken/', generalviews.calculateMetriken),

    path('textMining/calculateFreqWords/', generalviews.calculateFreqWords),

    path('textMining', generalviews.showStartPage, name='home'),
    path('textMining/vergleich/', generalviews.showVergleichPage, name='vergleich'),
    path('textMining/results/', generalviews.showResults, name='results'),


    path('textMining/upload/', uploadviews.uploadFiles, name='upload'),
    path('textMining/results/download/', downloadviews.downloadResults, name='download'),
    path('textMining/uploadImprovedPaperAjax/', uploadviews.uploadImprovedPaper, name="improvedPaper"),
    path('textMining/completeUpload/', uploadviews.completeUpload, name='completeUpload'),


    path('textMining/ajax/categorie', generalviews.ajaxCategorie, name='ajaxCateogrie'),
    path('textMining/ajax/categorie', generalviews.ajaxAuthor, name='ajaxAuthor'),
]
