from django.shortcuts import render
from . import models
import datetime

from tenders.parsers.zakupki_gov_ru_parser import Parser

# Create your views here.

parser = Parser()


def keywords_list(request):
    keywords = models.Keyword.objects.all()
    return render(request, 'tenders/keywords_list.html', {'keywords': keywords})


def search(request):
    tenders = models.Tender.objects.all()
    length = len(tenders)
    if request.method == 'POST':
        words = [str(item.split(b'=')[0])[2:-1] for item in request.body.split(b'&')[1:]]
        parser.init_keywords(words)
        parser.start()
        return render(request, 'tenders/search_page.html', {'result': length, 'finish': False})
    elif request.method == 'GET':
        if parser.is_alive():
            return render(request, 'tenders/search_page.html', {'result': length, 'finish': False})
        else:
            return render(request, 'tenders/search_page.html', {'result': length, 'finish': True})


def tenders_list(request):
    tenders = models.Tender.objects.all()
    return render(request, 'tenders/tenders_list.html', {'tenders': tenders})


def tenders_choose(request):
    ids = [int(str(item.split(b'=')[0])[2:-1]) for item in request.body.split(b'&')[1:]]
    tenders = []
    for id in ids:
        tenders.append(models.Tender.objects.get(id=id))
    return render(request, 'tenders/tenders_list.html', {'tenders': tenders})
