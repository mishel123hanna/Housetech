from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/auth/", include("apps.social_accounts.urls")),
    path("api/v1/properties/", include("apps.listings.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header = "Housetech Admin"
admin.site.site_title = "Housetech Admin Portal"
admin.site.index_title = "Welcome to Housetech adminstration"