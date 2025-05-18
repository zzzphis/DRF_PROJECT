from django.db import models


class DataTimeModelMixin(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True  # 指定类为抽象模型类，不在迁移映射中生成对应的表


class IsDeleteModelMixin(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    class Meta:
        abstract = True  # 指定类为抽象模型类，不在迁移映射中生成对应的表


class ModelSetMixin(DataTimeModelMixin, IsDeleteModelMixin):
    class Meta:
        abstract = True  # 指定类为抽象模型类，不在迁移映射中生成对应的表
