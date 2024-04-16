#core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('noruntable.html', views.noruntable, name='noruntable'),
    path('index2.html', views.mlb_games_view, name='mlb_games_view')
]
