from django.db import models

class UserInfo(models.Model):
    username = models.CharField(verbose_name="姓名",max_length=32,db_index=True)
    password = models.CharField(verbose_name="密码",max_length=64)
    token = models.CharField(verbose_name="TOKEN",max_length=64,null=True,blank=True,db_index=True)

class JsonInfo(models.Model):
    id = models.AutoField(verbose_name="ID",primary_key=True)
    name = models.CharField(verbose_name="页面名称",max_length=32)
    json = models.TextField(verbose_name="页面JSON")
    user_id = models.ForeignKey(verbose_name="关联用户",to="UserInfo",on_delete=models.CASCADE,null=True, blank=True)

class BuildUniappFile(models.Model):
    id = models.AutoField(verbose_name="ID",primary_key=True)
    filename = models.CharField(verbose_name="文件名",max_length=32)