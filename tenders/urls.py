from django.urls import path
from . import views


urlpatterns = [
    path('', views.keywords_list, name='keywords_list'),
    path('search', views.search, name='search'),
    path('tenders_list', views.tenders_list, name='tenders_list'),
    path('tenders_choose', views.tenders_choose, name='tenders_choose'),
]
