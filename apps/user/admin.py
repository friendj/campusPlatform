# encoding:utf-8
from django.contrib import admin

from .models import UserProfile, Activity, Organization, Follow, Participate


# Register your models here.

# class userAdmin(admin.ModelAdmin):
    # 列表页属性
    # list_display = []  # 列表显示属性
    # list_filter = []  # 列表过滤器
    # search_fields = []  # 搜索
    # list_per_page = 5  # 每页几条数据

    # 添加、修改页属性 不能同时使用
    # fields = #可规定属性的先后顺序
    # fieldsets = #给属性分组


admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Activity)
admin.site.register(Follow)
admin.site.register(Participate)
