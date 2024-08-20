from django.contrib import admin
from django.urls import path,include

from rest_framework.routers import DefaultRouter

from api_app import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('userapi', views.UserAPI, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', views.registration, name='registration'), 
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
