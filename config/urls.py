from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),  # For browsable API login/logout
    # Nutzerendpunkte direkt unter /api/ (ohne 'user/' Präfix)
    path('api/', include('users.urls')),
    path('api/', include('mental.urls')),
]
