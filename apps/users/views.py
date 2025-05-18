import io

from django import views
from django.contrib.auth.models import User
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from config.dbs.redisconfig import KEY_TEMPLATE, EXPIRE_TIME
from users.serializers import UserSerializer, MyTokenObtainPairSerializer
from utils.verifyutil import ImageVerify


# Create your views here.
class ImageVerifyView(views.View):

    def get(self, request, uuid, func):
        imageVerify = ImageVerify()
        img, code = imageVerify.verify_code()

        # 生成一个临时文件
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # 保存到数据库
        cache = get_redis_connection(alias='verify_codes')  # 使用redis
        cache.set(KEY_TEMPLATE % (func, uuid), code, EXPIRE_TIME)  # uuid作为key，code作为value，过期时间为60秒
        print(cache.get(KEY_TEMPLATE % (func, uuid)))  # 打印缓存中的验证码
        # 返回字节数据

        return HttpResponse(img_bytes, content_type='image/png')


# GenericViewSet 没有任何默认的方法
# 视图集是用于交互
class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['now']:
            print(self.action)
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data.get('username')
        password = request.data.get('password')
        print(request.data.get('uuid'))
        user = User(username=username)
        user.set_password(password)
        user.save()

        return Response(self.get_serializer(user).data)

    @action(methods=['get'], detail=False)
    def now(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
