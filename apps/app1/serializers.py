from random import choice

from rest_framework import serializers

from app1.models import Student


class StudentSerializer(serializers.Serializer):
    # 自动生成
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(label='名字', max_length=30)
    # required = false表示不必须填写
    age = serializers.IntegerField(label='年龄', required=False)
    sex = serializers.IntegerField(label='性别', required=False)
    create_time = serializers.DateTimeField(label='创建时间',read_only=True,required=False)
    update_time = serializers.DateTimeField(label='更新时间',read_only=True,required=False)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
