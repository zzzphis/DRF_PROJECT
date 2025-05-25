import io
import logging

from django import views
from django.contrib.auth.models import User
from django.http import HttpResponse
from django_redis import get_redis_connection
from fdfs_client.client import get_tracker_conf, Fdfs_client
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from config.dbs.redisconfig import KEY_TEMPLATE, EXPIRE_TIME
from users.serializers import UserSerializer, MyTokenObtainPairSerializer, UserDetailSerializer, \
    UpdatePasswordSerializer
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
logger = logging.getLogger("__name__")
tracker_path = get_tracker_conf('utils/fastdfs/client.conf')
client = Fdfs_client(tracker_path)


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

    # 因为需要对个人信息进行上传，
    # 需要判断是不是info路由更换序列化器
    def get_serializer_class(self):
        if self.action in ['info']:
            return UserDetailSerializer
        elif self.action in ['password']:
            return UpdatePasswordSerializer
        else:
            return self.serializer_class

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

    @action(methods=['put'], detail=False)
    def info(self, request):
        # 得到当前的登录用户信息
        user = request.user

        # 无论user_id传的是多少，都必须是当前登录的用户的id
        request.POST._mutable = True  # 允许修改POST的数据
        request.data['user'] = user.id

        # 得到上次的文件数据
        file = request.FILES.get('file')
        # 判断是否有文件数据和是否图片
        if file:
            if file.content_type not in ('image/jpeg', 'image/jpg', 'image/png', 'image/gif'):
                return Response(status=HTTP_400_BAD_REQUEST)
            try:
                images_ext_name = file.name.split('.')[-1]
            except Exception as e:
                logger.info('图片拓展名异常:%s' % e)
                images_ext_name = 'png'

            # 交给fastdfs服务器，上传到storage服务器
            try:
                upload_res = client.upload_by_buffer(file.read(), file_ext_name=images_ext_name)
            except Exception as e:
                logger.error('图片上传异常:%s' % e)
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # 上面只是请求成功了，还需要判断上传是否成功
                if upload_res.get('Status') != 'Upload successed.':
                    logger.warning('图片上传失败')
                    return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

                # 得到存储的地址路由信息，写入到数据中
                image_name = upload_res.get('Remote file_id').decode()
                request.data['avatar'] = image_name

        # 判断是否有详情数据
        if hasattr(user, 'userdetail'):
            # 如果有就修改
            if user.userdetail.avatar != request.data['avatar']:
                try:
                    # 如果之前上传了头像，然后又要修改图片，就需要删除之前上传的头像图片
                    client.delete_file(user.userdetail.avatar.encode())
                except Exception as e:
                    pass
            user_detail_serializer = self.get_serializer(user.userdetail, data=request.data)
        else:
            # 没有就创建
            user_detail_serializer = self.get_serializer(data=request.data)
        user_detail_serializer.is_valid(raise_exception=True)
        user_detail_serializer.save()
        return Response(user_detail_serializer.data)

    @action(methods=['put'], detail=False)
    def password(self, request):
        user = request.user
        # 通过serializers 进行密码的校验
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        newPassword = request.data['new_password']
        user.set_password(newPassword)
        user.save()

        return Response({'msg': '修改成功'})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
