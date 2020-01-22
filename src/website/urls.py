from django.urls import path
from . import views

'''
Responsável por realizar o mapeamento de rotas com as respectivas views
definidas no arquivo views.py
'''

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('picture', views.picture, name='picture'),
    path('list', views.list, name='list'),
    path('play', views.play, name='play'),
    path('examples', views.examples, name='examples'),
    path('settings', views.settings, name='settings'),
]