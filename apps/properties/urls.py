from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.ListAllPropertiesAPIView.as_view(), name="all-properties"),
    # path("add/", views.add_property, name="add-properties"),
    path("add/", views.PropertyCreateAPIView.as_view(), name="add-properties"),
    path("<slug:slug>/", views.PropertyRetrieveUpdateDestroyAPIView.as_view(), name="property-details"),
    path('image/<int:pkid>', views.PropertyImageDelete.as_view(), name="remove_image"),


]