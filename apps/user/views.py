# encoding:utf-8
from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from .models import Follow
from .models import Participate
from .models import Organization
from .models import Activity
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.http import StreamingHttpResponse
from campusPlatform.settings import BASE_DIR
from django.utils.encoding import escape_uri_path

import json
import copy
import os


# Create your views here.
def home(request):
    #  主页面
    activity = Activity.objects.order_by('?')[:6]
    return render(request, 'home.html', {'activity': activity})


def login(request):
    #  登录
    error = None
    if request.method == 'POST':
        #  获取用户名密码
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username is None or username == '':
            error = '用户名不能为空'
            # return render(request, 'home.html', {'error': error})
        elif password is None or password == '':
            error = '密码不能为空'
            # return render(request, 'home.html', {'error': error})
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                # 一周后登录过期
                request.session.set_expiry(24 * 60 * 60 * 7)
                # return render(request, 'home.html', {'error': error})
            else:
                error = '用户名错误'
                # return render(request, 'home.html', {'error': error})
        else:
            error = '用户名或密码错误'
    return render(request, 'home.html', {'error': error})

    # return render(request, 'home.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@csrf_exempt
def manager_center(request):
    #  管理员中心页面处理
    all_org = None
    activity = None
    user = None
    msg = {}
    page = request.GET.get('page')
    if page == '1' or page is None:
        all_org = Organization.objects.all()
        activity = Activity.objects.filter(u=request.user)
        if request.method == 'POST':
            act_id = request.POST.get('act_id')
            delete_user_id = request.POST.get('delete_user_id')
            activity_id = request.POST.get('activity_id')
            del_activity = request.POST.get('activity')
            revise_id = request.POST.get('revise')
            file_button = request.POST.get('file_button')
            act_file_id = request.POST.get('act_file_id')
            if act_id:
                all_user = {}
                user = {}
                participate = Participate.objects.filter(activity_id=act_id)
                all_user['count'] = participate.count()
                for i in range(participate.count()):
                    user['name'] = participate[i].u.username
                    user['id'] = participate[i].u.id
                    user['gender'] = participate[i].u.gender
                    user['email'] = participate[i].u.email
                    all_user[i] = copy.deepcopy(user)
                all = json.dumps(all_user)
                return HttpResponse(all, content_type='application/json')

            if delete_user_id and activity_id:
                participate = Participate.objects.filter(u_id=delete_user_id, activity_id=activity_id)
                activity = Activity.objects.get(id=activity_id)
                try:
                    if participate:
                        for i in participate:
                            i.isDelete = True
                            i.save()
                        msg['msg'] = '删除成功'
                    else:
                        msg['msg'] = '已删除成功'
                    num = activity.participate_num
                    activity.participate_num = num - 1
                    activity.save()
                except:
                    msg['msg'] = '删除失败'
                # print(msg)
                return HttpResponse(json.dumps(msg), content_type='application/json')

            if del_activity:
                activity = Activity.objects.filter(id=del_activity)
                try:
                    if activity:
                        for i in activity:
                            i.isDelete = True
                            i.save()
                        msg['msg'] = '删除成功'
                    else:
                        msg['msg'] = '已删除成功'
                except:
                    msg['msg'] = '删除失败'
                return HttpResponse(json.dumps(msg), content_type='application/json')

            if revise_id:
                #  修改活动内容
                try:
                    act = Activity.objects.get(id=revise_id)
                    topic = request.POST.get('topic', '')
                    if topic:
                        act.aName = topic
                    time = request.POST.get('time', '')
                    if time:
                        act.beginTime = time
                    place = request.POST.get('place', '')
                    if place:
                        act.place = place
                    type = request.POST.get('gridRadios', '')
                    if type:
                        act.type = type
                    org = request.POST.get('org', '')
                    if org:
                        organization = Organization.objects.get(id=org)
                        act.organization = organization
                    charge = request.POST.get('charge', '')
                    if charge:
                        act.charge_man = charge
                    phone_num = request.POST.get('phoneNum', '')
                    if phone_num:
                        act.phone_num = phone_num
                    introduction = request.POST.get('introduction', '')
                    if introduction:
                        act.introduction = introduction
                    detail = request.POST.get('detail', '')
                    if detail:
                        act.detail = detail
                    act.u = request.user
                    img = request.FILES.get('img', '')
                    if img:
                        act.img = img
                    act.save()
                    msg = '修改成功'
                except:
                    msg = '修改失败'

            if file_button:
                #  提交证明资料
                act = Activity.objects.get(id=file_button)
                try:
                    file = request.FILES.get('file')
                    # print('file', file)
                    if file:
                        act.file = file
                        act.save()
                        msg = '提交成功'
                    else:
                        msg = '未提交成功'
                except:
                    msg = '提交失败'

            if act_file_id:
                #  下载证明资料
                act = Activity.objects.get(id=act_file_id)
                file = BASE_DIR + '/' + str(act.file)
                file = open(file, 'rb')
                response = StreamingHttpResponse(file)
                response['Content-Type'] = 'application/octet-stream'
                file_name = act.aName + '.' + str(act.file).split('/')[-1].split('.')[-1]
                response['Content-Disposition'] = 'attachment;filename={0}'.format(escape_uri_path(file_name))
                return response

    if page == '2':
        user = Participate.objects.filter(organization=request.user.organization)

    if page == '3':
        pass

    if page == '4':
        #  发布活动页面
        all_org = Organization.objects.all()
        if request.method == 'POST':
            try:
                activity = Activity()
                #  获取参数
                activity.aName = request.POST.get('topic', '')
                activity.beginTime = request.POST.get('time', '')
                activity.place = request.POST.get('place', '')
                activity.type = request.POST.get('gridRadios', '')
                organization = Organization.objects.get(id=request.POST.get('org', ''))
                activity.organization = organization
                activity.charge_man = request.POST.get('charge', '')
                activity.phone_num = request.POST.get('phoneNum', '')
                activity.introduction = request.POST.get('introduction', '')
                activity.detail = request.POST.get('detail', '')
                activity.u = request.user
                activity.img = request.FILES.get('img', '')
                activity.save()
                msg = '发布成功'
            except:
                msg = '发布失败'
    return render(request, 'manager-center.html',
                  {'page': page, 'org': all_org, 'msg': msg, 'activity': activity, 'user': user})


@csrf_exempt
def student_center(request):
    msg = {}
    activity = None
    organization = None
    user = None
    page = request.GET.get('page')
    if page == '1' or page is None:
        if request.method == 'GET':
            activity = Follow.objects.filter(u=request.user)
        if request.method == 'POST':
            cancel_id = request.POST.get('cancel_id')
            participate_id = request.POST.get('participate_id')
            if cancel_id:
                try:
                    follow = Follow.objects.filter(u=request.user, activity_id=cancel_id)
                    act = Activity.objects.get(id=cancel_id)
                    for i in follow:
                        i.isDelete = True
                        i.save()
                    num = act.follow_num
                    act.follow_num = num - 1
                    act.save()
                    msg['msg'] = '取消成功'
                except:
                    msg['msg'] = '取消失败'
            if participate_id:
                try:
                    participate_filter = Participate.objects.filter(u=request.user, activity_id=participate_id)
                    if participate_filter:
                        msg['msg'] = '已报名成功'
                    else:
                        participate = Participate()
                        participate.u = request.user
                        participate.activity_id = participate_id
                        participate.save()
                        msg['msg'] = '报名成功'
                except:
                    msg['msg'] = '报名失败'
            return HttpResponse(json.dumps(msg), content_type="application/json")

    if page == '2':
        if request.method == 'GET':
            activity = Participate.objects.filter(u=request.user, activity_id__isnull=False)
        if request.method == 'POST':
            cancel_follow_id = request.POST.get('cancel_follow_id')
            cancel_act_id = request.POST.get('cancel_act_id')
            if cancel_follow_id:
                try:
                    follow = Follow.objects.filter(u=request.user, activity_id=cancel_follow_id)
                    act = Activity.objects.get(id=cancel_follow_id)
                    if follow:
                        for i in follow:
                            i.isDelete = True
                            i.save()
                        num = act.follow_num
                        act.follow_num = num - 1
                        act.save()
                        msg['msg'] = '取消成功'
                    else:
                        msg['msg'] = '已取消成功'
                except:
                    msg['msg'] = '取消失败'
            if cancel_act_id:
                try:
                    participate = Participate.objects.filter(u=request.user, activity_id=cancel_act_id)
                    act = Activity.objects.get(id=cancel_act_id)
                    if participate:
                        for i in participate:
                            i.isDelete = True
                            i.save()
                        num = act.participate_num
                        act.participate_num = num - 1
                        act.save()
                        msg['msg'] = '退出成功'
                    else:
                        msg['msg'] = '已退出成功'
                except:
                    msg['msg'] = '退出失败'
            return HttpResponse(json.dumps(msg), content_type="application/json")

    if page == '3':
        if request.method == 'GET':
            organization = Participate.objects.filter(u=request.user, organization_id__isnull=False)
        if request.method == 'POST':
            try:
                cancel_follow_org = request.POST.get('cancel_follow_org')
                if cancel_follow_org:
                    participate = Participate.objects.filter(u=request.user, organization_id=cancel_follow_org)
                    if participate:
                        for i in participate:
                            i.isDelete = True
                            i.save()
                        msg['msg'] = '取消成功'
                    else:
                        msg['msg'] = '已取消成功'
            except:
                msg['msg'] = '取消失败'
            return HttpResponse(json.dumps(msg), content_type='application/json')

    if page == '4':
        if request.method == 'GET':
            activity = Participate.objects.filter(u=request.user, activity_id__isnull=False)
            # for i in activity:
            #     print(i.activity.aName)
        if request.method == 'POST':
            act_file_id = request.POST.get('act_file_id')
            if act_file_id:
                act = Activity.objects.get(id=act_file_id)
                file = BASE_DIR + '/' + str(act.file)
                file = open(file, 'rb')
                response = StreamingHttpResponse(file)
                response['Content-Type'] = 'application/octet-stream'
                file_name = act.aName + '.' + str(act.file).split('/')[-1].split('.')[-1]
                response['Content-Disposition'] = 'attachment;filename={0}'.format(escape_uri_path(file_name))
                return response

    if page == '5':
        if request.method == 'GET':
            user = UserProfile.objects.get(id=request.user.id)

    return render(request, 'student-center.html',
                  {'activity': activity, 'organization': organization, 'page': page, 'user': user})


def manager_centers(request, page):
    all_org = None
    msg = ''
    if page == '4':
        all_org = Organization.objects.all()
        if request.method == 'POST':
            try:
                activity = Activity()
                activity.aName = request.POST.get('topic', '')
                activity.beginTime = request.POST.get('time', '')
                activity.place = request.POST.get('place', '')
                activity.type = request.POST.get('gridRadios', '')
                organization = Organization.objects.get(id=request.POST.get('org', ''))
                activity.organization = organization
                activity.charge_man = request.POST.get('charge', '')
                activity.phone_num = request.POST.get('phoneNum', '')
                activity.introduction = request.POST.get('introduction', '')
                activity.detail = request.POST.get('detail', '')
                # print(activity.detail)
                activity.img = request.FILES.get('img', '')
                # print(activity.img)
                activity.save()
                msg = '发布成功'
            except:
                msg = '发布失败'
    return render(request, 'manager-center.html', {'page': page, 'org': all_org, 'msg': msg})


@csrf_exempt
def activity_index(request):
    search_dict = dict()
    place_num = None
    typ_num = None
    time = None
    organization = None
    page = None
    msg = {}
    if request.method == 'GET':
        place_num = request.GET.get('place')
        typ_num = request.GET.get('type')
        time = request.GET.get('time')
        organization = request.GET.get('org')
        page = request.GET.get('page', '')
        if page == '' or page is None:
            page = 1
        page = int(page)
        place = None
        typ = None
        if place_num != 'undefined' and place_num and place_num != 'None':
            if place_num == '1':
                place = '行政楼'
            elif place_num == '2':
                place = '教学楼'
            elif place_num == '3':
                place = '体育馆'
            else:
                place = '足球场'
            search_dict['place'] = place
        if typ_num != 'undefined' and typ_num and typ_num != 'None':
            if typ_num == '1':
                typ = '学术'
            elif typ_num == '2':
                typ = '演讲'
            else:
                typ = '文体'
            search_dict['type'] = typ
        if time != 'undefined' and time and time != 'None':
            search_dict['beginTime__gte'] = time
        if organization != 'undefined' and organization and organization != 'None':
            search_dict['organization_id'] = organization
            organization = int(organization)

    if request.method == 'POST':
        follow_id = request.POST.get('follow_id')
        participate_id = request.POST.get('participate_id')
        if follow_id:
            try:
                follow_filter = Follow.objects.filter(u_id=request.user.id, activity_id=follow_id)
                if follow_filter:
                    msg['msg'] = '已关注成功'
                else:
                    follow = Follow()
                    follow.u = request.user
                    follow.activity_id = follow_id
                    follow.save()
                    activity2 = Activity.objects.filter(id=follow_id)
                    for i in activity2:
                        follow_num = i.follow_num
                        i.follow_num = int(follow_num) + 1
                        i.save()
                    msg['msg'] = '关注成功'
            except:
                msg['msg'] = '关注失败'
            return HttpResponse(json.dumps(msg), content_type="application/json")
        if participate_id:
            try:
                participate_filter = Participate.objects.filter(u_id=request.user.id, activity_id=participate_id)
                if participate_filter:
                    msg['msg'] = '已报名成功'
                else:
                    participate = Participate()
                    participate.u = request.user
                    participate.activity_id = participate_id
                    participate.save()
                    activity2 = Activity.objects.filter(id=participate_id)
                    for i in activity2:
                        participate_num = i.participate_num
                        i.participate_num = int(participate_num) + 1
                        i.save()
                    msg['msg'] = '报名成功'
            except:
                msg['msg'] = '报名失败'
            return HttpResponse(json.dumps(msg), content_type="application/json")

    activity = Activity.objects.filter(**search_dict)
    count = activity.count()
    page_count = int(count / 6 + 1)
    act = activity[(page - 1) * 6:page * 6]
    org = Organization.objects.all()
    return render(request, 'activity-wall.html',
                  {'activity': act, 'page': page, 'page_count': page_count, 'place': place_num, 'type': typ_num,
                   'time': time, 'org': org, 'org_id': organization})


def act_detail(request):
    activity = None
    msg = {}
    if request.method == 'GET':
        activity_id = request.GET.get('aid')
        activity = Activity.objects.filter(id=activity_id)

    if request.method == 'POST':
        follow_id = request.POST.get('follow_id')
        participate_id = request.POST.get('participate_id')
        if follow_id:
            try:
                follow_filter = Follow.objects.filter(u_id=request.user.id, activity_id=follow_id)
                # if follow_filter:
                #     print(follow_filter)
                if follow_filter:
                    msg['msg'] = '已关注成功'
                else:
                    follow = Follow()
                    follow.u = request.user
                    follow.activity_id = follow_id
                    follow.save()
                    msg['msg'] = '关注成功'
            except:
                msg['msg'] = '关注失败'
            return HttpResponse(json.dumps(msg), content_type="application/json")
        if participate_id:
            try:
                participate_filter = Participate.objects.filter(u_id=request.user.id, activity_id=participate_id)
                if participate_filter:
                    msg['msg'] = '已报名成功'
                else:
                    participate = Participate()
                    participate.u = request.user
                    participate.activity_id = participate_id
                    participate.save()
                    msg['msg'] = '报名成功'
            except:
                msg['msg'] = '报名失败'
            return HttpResponse(json.dumps(msg), content_type="application/json")
    return render(request, 'activity-detail.html', {'activity': activity})


@csrf_exempt
def society_index(request):
    search_dict = {}
    msg = {}
    page = None
    if request.method == 'GET':
        page = request.GET.get('page', '')
        if page == '' or page is None:
            page = 1
        page = int(page)

    if request.method == 'POST':
        try:
            participate_id = request.POST.get('participate_id')
            if participate_id:
                participate_filter = Participate.objects.filter(u=request.user, organization_id=participate_id)
                if participate_filter:
                    msg['msg'] = '已报名成功'
                else:
                    participate = Participate()
                    participate.u = request.user
                    participate.organization_id = participate_id
                    participate.save()
                    msg['msg'] = '报名成功'
        except:
            msg['msg'] = '报名失败'
        return HttpResponse(json.dumps(msg), content_type="application/json")

    organization = Organization.objects.filter(**search_dict)
    # print(organization)
    count = organization.count()
    page_count = int(count / 6 + 1)
    org = organization[(page - 1) * 6:page * 6]
    return render(request, 'society-wall.html', {'organization': org, 'page': page, 'page_count': page_count})


def org_detail(request):
    msg = {}
    activity = None
    page = None
    page_count = None
    if request.method == 'GET':
        oid = request.GET.get('oid')
        page = request.GET.get('page', '')
        if page == '' or page is None:
            page = 1
        page = int(page)
        activity = Activity.objects.filter(organization_id=oid)
        count = activity.count()
        page_count = int(count / 6) + 1
        act = activity[(page - 1) * 6:page * 6]
        # print(count)
    if request.method == 'POST':
        follow_id = request.POST.get('follow_id')
        participate_id = request.POST.get('participate_id')
        if follow_id:
            try:
                follow_filter = Follow.objects.filter(u_id=request.user.id, activity_id=follow_id)
                if follow_filter:
                    msg['msg'] = '已关注成功'
                else:
                    follow = Follow()
                    follow.u = request.user
                    follow.activity_id = follow_id
                    follow.save()
                    activity2 = Activity.objects.filter(id=follow_id)
                    for i in activity2:
                        follow_num = i.follow_num
                        i.follow_num = int(follow_num) + 1
                        i.save()
                    msg['msg'] = '关注成功'
            except:
                msg['msg'] = '关注失败'
            return HttpResponse(json.dumps(msg), content_type="application/json")
        if participate_id:
            try:
                participate_filter = Participate.objects.filter(u_id=request.user.id, activity_id=participate_id)
                if participate_filter:
                    msg['msg'] = '已报名成功'
                else:
                    participate = Participate()
                    participate.u = request.user
                    participate.activity_id = participate_id
                    participate.save()
                    activity2 = Activity.objects.filter(id=participate_id)
                    for i in activity2:
                        participate_num = i.participate_num
                        i.participate_num = int(participate_num) + 1
                        i.save()
                    msg['msg'] = '报名成功'
            except:
                msg['msg'] = '报名失败'
            return HttpResponse(json.dumps(msg), content_type="application/json")

    return render(request, 'society-detail.html', {'activity': act, 'page': page, 'page_count': page_count, 'oid': oid})
