from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/auth/', include('rest_framework.urls')),  # For browsable API login/logout
    path('api/user/', include('users.urls')),
]
