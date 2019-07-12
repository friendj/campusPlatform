"""campusPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from apps.user import views as user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', user.home),
    # url(r'^home.html/', views.home),
    url(r'^login/$', user.login),
    url(r'^logout/$', user.logout),
    url(r'manager-center/$', user.manager_center),
    url(r'activity-wall/$', user.activity_index),
    url(r'activity-detail/$', user.act_detail),
    url(r'society-wall/$', user.society_index),
    url(r'society-detail/$', user.org_detail),
    url(r'student-center/$', user.student_center),
]

