from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from app1.models import *
from app1.serializers import *


# Create your views here.
class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        :param request:
        :return:
        """
        students = Student.objects.all()
        # 因为需要将数据从后端放到前端需要进行序列化操作
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
