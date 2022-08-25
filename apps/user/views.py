from django.shortcuts import render,redirect,HttpResponse
import re
from django.conf import settings
from apps.user.models import User
from django.urls import reverse
from django.views import View
from itsdangerous.serializer import Serializer
from itsdangerous.exc import BadSignature
# Create your views here.

'''
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        rpassword = request.POST.get('cpwd')
        email = request.POST.get('email')

        # 数据校验,检验是否不完整
        if not all([username,password,email]):
            return render(request,'register.html',{"errmsg":"数据不完整"})
        # 校验密码是否一致
        if rpassword !=password:
            return render(request,'register.html', {'errmsg':'两次密码不一致'})
        # 邮箱校验
        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$",email):
            return render(request,'register.html',{"errmsg":"邮箱格式不正确"})

        # 校验用户是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user=None
        if user:
            return render(request, 'register.html', {'errmsg': '用户已存在'})
        user = User.objects.create_user(username,password,email)
        user.is_active = 0
        user.save()

        return redirect(reverse('goods:index'))
'''
class RegisterView(View):
    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        rpassword = request.POST.get('cpwd')
        email = request.POST.get('email')

        # 数据校验,检验是否不完整
        if not all([username, password, email]):
            return render(request, 'register.html', {"errmsg": "数据不完整"})
        # 校验密码是否一致
        if rpassword != password:
            return render(request, 'register.html', {'errmsg': '两次密码不一致'})
        # 邮箱校验
        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, 'register.html', {"errmsg": "邮箱格式不正确"})

        # 校验用户是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户已存在'})
        user = User.objects.create_user(username, password, email)
        user.is_active = 0
        user.save()
        # 发送激活邮箱,需带本网站地址和用户加密信息
        # 加密信息生成token
        serializerinfo = Serializer(settings.SECRET_KEY,300)
        info = {'confirm':user.id}
        token = serializerinfo.dumps(info)
        # 发送邮箱

        return redirect(reverse('goods:index'))


class ActiveView(View):
    def get(self, request,token):

        serializerinfo = Serializer(settings.SECRET_KEY, 300)
        try:
            info = serializerinfo.loads(token)
            user_id = info['confirm']
            user = User.objects.get(user_id)
            user.is_active = 1
            user.save()
            # 跳转到登录界面
            return redirect(reverse('user:login'))

        except BadSignature as e:
            return HttpResponse('激活链接超时!')


class LoginView(View):
    def get(self,request):
        return render(request,'login.html')





