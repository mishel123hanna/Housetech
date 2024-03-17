from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.ListAllPropertiesAPIView.as_view(), name="all-properties"),

]