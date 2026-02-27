from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from debug_toolbar.toolbar import debug_toolbar_urls
schema_view = get_schema_view(
    openapi.Info(
        title="Roomsy Hotel Booking API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/',include('apps.accounts.urls')),
    path('api/hotels/',include('apps.hotels.urls')),
    path('api/bookings/',include('apps.bookings.urls')),
    path('api/reviews/',include('apps.reviews.urls')),
    path('api/dashboard/',include('apps.dashboard.urls')),
    path('swagger/',schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0), name='redoc'),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
