from django.db import models

class UserInfo(models.Model):
    username = models.CharField(verbose_name="姓名",max_length=32,db_index=True)
    password = models.CharField(verbose_name="密码",max_length=64)
    token = models.CharField(verbose_name="TOKEN",max_length=64,null=True,blank=True,db_index=True)
