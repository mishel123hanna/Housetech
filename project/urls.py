from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/auth/", include("apps.social_accounts.urls")),
    path("api/v1/properties/", include("apps.properties.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
    path("", include("apps.utils.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

admin.site.site_header = "Housetech Admin"
admin.site.site_title = "Housetech Admin Portal"
admin.site.index_title = "Welcome to Housetech adminstration"