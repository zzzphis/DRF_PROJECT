from django.db import models

# Create your models here.
class Student(models.Model):
    sex_choice = {
        (1,'男'),
        (2,'女')
    }
    name = models.CharField(max_length=30,verbose_name='姓名',unique=True)
    age = models.IntegerField(verbose_name='年龄',null=True,blank=True)
    sex = models.IntegerField(verbose_name='性别',null=True,blank=True,choices=sex_choice)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间',)
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间', null=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    # classes这个属性与表Classes的外键关联
    # classes = models.ForeignKey('Classes',on_delete=models.CASCADE,verbose_name='班级')

class Classes(models.Model):
    name = models.CharField(max_length=30,verbose_name='班级名称',unique=True)
    slogan = models.TextField(verbose_name='班级口号',null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', )
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间', null=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    def __str__(self):
        return self.name