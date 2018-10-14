import hashlib
from django.db import models
# Create your models here.
# postid	唯一标识
# title	标题 -image	图片
# duration时长
# app_fu_title简要信息

class HomeWheel(models.Model):
    bannerid=models.IntegerField(default=1)
    image = models.CharField(max_length=2001)
    class Meta:
        db_table = 'dy_wheel'


class movies(models.Model):
    postpeid = models.IntegerField(default=1)
    title = models.CharField(max_length=32)
    image = models.CharField(max_length=200)
    duration=models.IntegerField(default=1)
    app_fu_title=models.CharField(max_length=200)

    class Meta:
        db_table = 'dy_movies'

class UserModel(models.Model):
    u_name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=32, unique=True)
    u_icon = models.ImageField(upload_to='icons')
    is_delete = models.BooleanField(default=False)

    def generate_hash(self, u_password):
        sha = hashlib.sha512()
        sha.update(u_password.encode('utf-8'))
        return sha.hexdigest()

    def set_password(self, u_password):
        self.password = self.generate_hash(u_password)

    def check_password(self, u_password):
        return self.password == self.generate_hash(u_password)

# class Collected(models.Model):
#     c_user = models.ForeignKey(UserModel)
#     c_movies = models.ForeignKey(movies)

