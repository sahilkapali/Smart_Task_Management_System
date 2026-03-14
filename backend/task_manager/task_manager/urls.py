from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/login/', TokenObtainPairView.as_view()),

    path('api/', include('tasks.urls')),

    path('api/users/', include('users.urls')),

]
