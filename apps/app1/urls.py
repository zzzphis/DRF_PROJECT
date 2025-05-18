from django.urls import path
from rest_framework.routers import DefaultRouter

from app1 import views
from app1.views import StudentsViewSet, ClassesViewSet

urlpatterns = [
    # path('students/',StudentViewSet.as_view({'get':'list','post':'create'})),
    # path('students/<int:pk>/',StudentViewSet.as_view({'put':'update','get':'retrieve','delete':'destroy'}))
]
router = DefaultRouter()

router.register('students', StudentsViewSet,basename='student')
router.register('classes',ClassesViewSet,basename='classes')
urlpatterns += router.urls
