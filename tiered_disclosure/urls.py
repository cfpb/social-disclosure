from django.conf.urls import url
from otree.urls import urlpatterns

from . import views

# DATA
urlpatterns.append(url(r'^tiered_disclosure/data/download$', views.DataDownload, name="experiment_data_download"))
# urlpatterns.append(url(r'^tiered_disclosure/data/$', views.ViewData, name="experiment_data_view"))