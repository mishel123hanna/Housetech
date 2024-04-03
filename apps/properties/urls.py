from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.ListAllPropertiesAPIView.as_view(), name="all-properties"),
    # path("add/", views.add_property, name="add-properties"),
    path("add/", views.PropertyCreateAPIView.as_view(), name="add-properties"),


]