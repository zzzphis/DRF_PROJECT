from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import ImageVerifyView, UserViewSet, MyTokenObtainPairView

urlpatterns = [
    path('verification/<str:func>/<uuid:uuid>/',ImageVerifyView.as_view()),
    path('login/',MyTokenObtainPairView.as_view())
]
router = DefaultRouter()
router.register('users',UserViewSet)
urlpatterns+=router.urls