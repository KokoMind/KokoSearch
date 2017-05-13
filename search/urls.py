from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^process_query', views.process_query, name='process_query'),
    url(r'^process_image', views.process_image, name='process_image'),
    url(r'^results', views.results, name='results'),
]
