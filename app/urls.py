from django.urls import path
from .views import *

urlpatterns = [
    path("myinbox/", appEmailDataModelListView.as_view(), name="appEmailDataModelListViewURL"),
    path("email-in-format/", appEmailinFormatView.as_view(), name="appEmailinFormatViewURL"),
    path("search-email/", appFromEmailSearchView.as_view(), name="appFromEmailSearchViewURL"),
    path("smtp-inbox/", appEmailMyinbox.as_view(), name="appEmailMyinboxURL"),
    path("task/", DemoClassView.as_view(), name="DemoClassViewURL")
]


