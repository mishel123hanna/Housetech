from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.ListAllPropertiesAPIView.as_view(), name="all-properties"),
    # path("add/", views.add_property, name="add-properties"),
    path("add/", views.PropertyCreateAPIView.as_view(), name="add-properties"),
    path("<slug:slug>/", views.PropertyRetrieveUpdateDestroyAPIView.as_view(), name="property-details"),
    path('image/<int:pkid>/', views.PropertyImageDelete.as_view(), name="remove_image"),
    path('upload-images', views.PropertyImagesCreateAPIView.as_view(), name="upload_images"),
    path("user", views.UserProperties.as_view(), name="user_properties"),
    # path("user-prop", views.get_user_properties, name="user_properties"),
]