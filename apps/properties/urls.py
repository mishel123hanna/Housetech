from django.urls import path

from .views import (
    ListAllPropertiesAPIView,
    PropertyCreateAPIView,
    PropertyImageDelete,
    PropertyImagesCreateAPIView,
    PropertyRetrieveUpdateDestroyAPIView,
    UserProperties,
    UserPropertyFavoriteDeleteView,
    UserPropertyFavoriteListCreateView,
)

urlpatterns = [
    path("all/", ListAllPropertiesAPIView.as_view(), name="all-properties"),
    path("add/", PropertyCreateAPIView.as_view(), name="add-properties"),
    path(
        "<slug:slug>/",
        PropertyRetrieveUpdateDestroyAPIView.as_view(),
        name="property-details",
    ),
    path("image/<int:pkid>/", PropertyImageDelete.as_view(), name="remove_image"),
    path(
        "upload-images",
        PropertyImagesCreateAPIView.as_view(),
        name="upload_images",
    ),
    path("user", UserProperties.as_view(), name="user_properties"),
    path(
        "user/favorites/",
        UserPropertyFavoriteListCreateView.as_view(),
        name="favorite-list-create",
    ),
    path(
        "user/favorites/delete/",
        UserPropertyFavoriteDeleteView.as_view(),
        name="favorite-delete",
    ),
    # path("user-prop", get_user_properties, name="user_properties"),
]
