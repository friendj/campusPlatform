# encoding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
from system.storage import ImageStorage
from campusPlatform import settings


# Create your models here.


class OrganizationManager(models.Manager):
    def get_queryset(self):
        return super(OrganizationManager, self).get_queryset().filter(isDelete=False)


class Organization(models.Model):
    objects = OrganizationManager()
    oName = models.CharField(max_length=20)
    createTime = models.DateTimeField(auto_now_add=True)
    charge_man = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=20)
    introduction = models.CharField(max_length=200)
    detail = models.TextField()
    isDelete = models.BooleanField(default=False)
    img = models.ImageField(max_length=50, upload_to='static/media/%Y%m', storage=ImageStorage(),
                            default='/static/img/society/society01.jpg')

    class Meta:
        db_table = 'organization'


class Activity(models.Model):
    objects = OrganizationManager()
    aName = models.CharField(max_length=20)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    beginTime = models.DateTimeField()
    charge_man = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=20)
    introduction = models.CharField(max_length=200)
    detail = models.TextField()
    img = models.ImageField(max_length=50, upload_to='static/media/%Y%m', storage=ImageStorage(), default=None)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    place = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    follow_num = models.IntegerField(default=0)
    participate_num = models.IntegerField(default=0)
    u = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(max_length=50, upload_to='static/file/%Y%m', storage=ImageStorage(), default=None)

    class Meta:
        db_table = 'activity'


class Follow(models.Model):
    objects = OrganizationManager()
    u = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'follow'


class Participate(models.Model):
    objects = OrganizationManager()
    u = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'participate'


class UserProfile(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=True)
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default='male',
                              verbose_name='性别')
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'
