from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app1.serializers import *


# Create your views here.
# class StudentViewSet(viewsets.ViewSet):
#     def list(self, request):
#         """
#         :param request:
#         :return:
#         """
#         students = Student.objects.filter(is_delete=False)
#         # 因为需要将数据从后端放到前端需要进行序列化操作
#         serializer = StudentSerializer(students, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StudentSerializer(data=request.data)
#         serializer.is_valid()
#         # save方法会调用你使用的模型的create方法如果是自定义的则需要重写create方法
#         serializer.save()
#         return Response(serializer.data)
#     def retrieve(self,request,pk=None):
#         try:
#             student = Student.objects.get(id=pk)
#         except Student.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#         serializer = StudentSerializer(student)
#         return Response(serializer.data)
#     def update(self,request,pk=None):
#         """
#         更新操作
#         :param request:
#         :param pk:
#         :return:
#         """
#         # 先从后端找到数据
#         try:
#             student = Student.objects.get(id=pk)
#         except Student.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#         # instance是需要更新的对象 data是更新的参数
#         serializer = StudentSerializer(instance=student,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def destroy(self,request,pk):
#         """
#         删除学生信息
#         :param request:
#         :param pk:
#         :return:
#         """
#         try:
#             student = Student.objects.get(id=pk)
#         except Student.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#         # 这里因为student是模型中数据对象调用delete方法
#         # 是模型中的方法需要到模型中重写也可以直接删除
#         student.delete()
#         return Response(status=HTTP_204_NO_CONTENT)


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.filter(is_delete=False)
    serializer_class = StudentSerializer


class ClassesViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.filter(is_delete=False)
    serializer_class = ClassesSerializer

    @action(methods=['get'], detail=False)
    def last(self, request):
        classes = Classes.objects.last()
        data = self.get_serializer(classes)
        return Response(data.data)
