from django.urls import path

from . import views

app_name = 'conex'
urlpatterns = [
    path('', views.index, name='index'),
    path('map', views.map, name='map'),
    # path('add', views.add, name='add'),
    path('countries', views.CountriesView.as_view(), name='countries'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]