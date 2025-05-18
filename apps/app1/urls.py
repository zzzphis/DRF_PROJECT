from django.urls import path
from rest_framework.routers import DefaultRouter

from app1 import views
from app1.views import StudentViewSet

urlpatterns = [
    path('students/',StudentViewSet.as_view({'get':'list','post':'create'}))
]
# router = DefaultRouter()
#
# router.register('students', StudentViewSet,basename='student')
#
# urlpatterns += router.urls
