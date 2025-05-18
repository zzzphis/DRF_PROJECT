from rest_framework import serializers

from app1.models import *


# class StudentSerializer(serializers.Serializer):
#     # 自动生成
#     id = serializers.IntegerField(label='ID', read_only=True)
#     name = serializers.CharField(label='名字', max_length=30)
#     # required = false表示不必须填写
#     age = serializers.IntegerField(label='年龄', required=False)
#     sex = serializers.IntegerField(label='性别', required=False)
#     create_time = serializers.DateTimeField(label='创建时间', read_only=True, required=False)
#     update_time = serializers.DateTimeField(label='更新时间', read_only=True, required=False)
#
#     # 创建操作
#     def create(self, validated_data):
#         return Student.objects.create(**validated_data)
#
#     # 更新操作 validated_data是个字典
#     def update(self,instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.age = validated_data.get('age', instance.age)
#         instance.sex = validated_data.get('sex', instance.sex)
#         instance.save()
#         return instance
#     def validate(self,attrs):
#         if attrs['age']<18:
#             raise serializers.ValidationError('未成年不能报名')
class StudentSerializer(serializers.ModelSerializer):
    classes_name = serializers.CharField(source='Classes.name', read_only=True, label='班级')

    class Meta:
        model = Students
        exclude = ['is_delete']

    extra_kwargs = {
        'name': {
            'max_length': 30,
            'error_messages': {
                'max_length': '姓名长度不能超过30'
            }
        },
        'age': {
            'required': False,
            'error_messages': {
                'required': '年龄不能为空'
            }
        },
        'classes': {
            'write_only': True,
        }

    }


class StudentSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'name']


class ClassesSerializer(serializers.ModelSerializer):
    # 这个属性名需要与你指定的管理器名称相同
    students = StudentSerializerModel(many=True, read_only=True)

    class Meta:
        model = Classes
        exclude = ['create_time','update_time','is_delete']
