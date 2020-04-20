from django.shortcuts import render, redirect, HttpResponse
from jdsj.models import Phone_jdsj, Image, Slide, Send_email, User
import json
from django import views
from .sjfroms import RegisterForm
from django.core.mail import send_mail
from uuid import uuid1
from django.utils import timezone
import hashlib
import re


# Create your views here.


def pwd_encrypt(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result


def num1(str1):
    print(str1)
    return int(re.sub("\D", "", str1))


class Main(views.View):

    def get(self, request):
        email = request.session.get('email', '')
        nick_name = None
        if email:
            nick_name = User.objects.filter(email=email).first().nick_name
        slides = Slide.objects.all()
        first_slide = slides[0]
        phone_jdsjs = Phone_jdsj.objects.all().order_by('-commentCount')
        a = 0
        phone_list = []
        defe_list = []
        for item in phone_jdsjs:
            if item.skid in defe_list:
                pass
            else:
                defe_list.append(item.skid)
                a += 1
                image = Image.objects.filter(skid=item.skid).first()
                if image:
                    item_dict = {}
                    item_dict['image_url'] = json.loads(image.img_url)[0].replace('n5/jfs', 'n1/s540x540_jfs').replace(
                        'n5/s54x54_jfs', 'n1/s540x540_jfs')
                    item_dict['pid'] = item.pid
                    item_dict['price'] = item.price
                    item_dict['skid'] = item.skid
                    item_dict['defaultGoodCountStr'] = item.defaultGoodCountStr
                    item_dict['commentCountStr'] = item.commentCountStr
                    item_dict['goodRateShow'] = item.goodRateShow
                    item_dict['title'] = item.title
                    phone_list.append(item_dict)
                else:
                    p1s = Phone_jdsj.objects.filter(skid=item.skid).all()
                    for p1 in p1s:
                        p1.delete()
        return render(request, 'main/main.html',
                      {'slides': slides, 'first_slide': first_slide, 'phone_list': phone_list, 'username': nick_name})


class Login(views.View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'main/login.html', {'username': 1, 'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm()
        email = request.POST.get("email").strip()
        pwd = request.POST.get("pwd1").strip()
        pwd = pwd_encrypt(pwd)
        u1 = User.objects.filter(email=email).first()
        print(email, pwd)
        if u1:
            pwd1 = u1.pwd
            if pwd == pwd1:
                print('登录成功')
                request.session['email'] = email
                # after_url
                # message
                # after_page
                message = '成功登录！'
                after_url = "jdsj:main"
                after_page = '主页'
                return render(request, 'main/after.html',
                              {'after_url': after_url, 'message': message, 'after_page': after_page})
            else:
                print('密码错误')
                message = '密码错误！'
                after_url = "jdsj:login"
                after_page = '登录页'
                return render(request, 'main/after.html',
                              {'after_url': after_url, 'message': message, 'after_page': after_page})

        else:
            print('账号错误')
            message = '账号错误！'
            after_url = "jdsj:login"
            after_page = '登录页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})


class Logout(views.View):
    def get(self, request):
        request.session.flush()

        message = '账号成功登出！'
        after_url = "jdsj:main"
        after_page = '主页'
        return render(request, 'main/after.html',
                      {'after_url': after_url, 'message': message, 'after_page': after_page})


class Forget(views.View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'main/forget.html', {'username': 1, 'register_form': register_form})

    def post(self, request):
        email = request.POST.get("email").strip()
        verif = uuid1()
        verif_md5 = pwd_encrypt(str(verif))
        u1 = User.objects.filter(email=email)
        if not u1:
            message = '无此账号，请先重新输入！'
            after_url = "jdsj:forget"
            after_page = '忘记密码页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        else:
            s1 = Send_email.objects.filter(email_address=email).first()
            if s1:
                diff = timezone.now() - s1.data_time
                diff = diff.seconds / 60
                if diff < 5:
                    message = '邮件已发送，到您的邮箱查看，请不要重复发送。如果没有找到邮件，请检查填写邮箱是否错误，或等待5分钟后再次发送！'
                    after_url = "jdsj:login"
                    after_page = '登录页'
                    return render(request, 'main/after.html',
                                  {'after_url': after_url, 'message': message, 'after_page': after_page})
                else:
                    try:
                        send_mail('django 项目密码修改',
                                  f"此邮件不要泄露给他人，请点击注册网址：'http://si-yu.zicp.vip/jdsj/main/change_pwd/{verif}'",
                                  '979746262@qq.com', [email, ])
                        u1.pwd = 'freeze'
                        u1.save()
                        s1.email_address = email
                        s1.data_time = timezone.now()
                        s1.verif = verif_md5
                        s1.static = 2
                        s1.save()
                    except:
                        message = '邮箱账号错误,请重新填写！'
                        after_url = "jdsj:forget"
                        after_page = '忘记密码页'
                        return render(request, 'main/after.html',
                                      {'after_url': after_url, 'message': message, 'after_page': after_page})
                    message = '邮件已重新发送，请登陆邮箱查看邮件，完成密码修改！'
                    after_url = "jdsj:login"
                    after_page = '登录页'
                    return render(request, 'main/after.html',
                                  {'after_url': after_url, 'message': message, 'after_page': after_page})

            else:
                try:
                    send_mail('django 项目账号修改密码',
                              f"此邮件不要泄露给他人，请点击注册网址：'http://si-yu.zicp.vip/jdsj/main/change_pwd/{verif}'",
                              '979746262@qq.com', [email, ])

                    se1 = Send_email(email, timezone.now(), verif_md5, 2)
                    se1.save()
                    u1.pwd = 'freeze'
                    u1.save()
                    message = '邮件已成功发送，请登陆邮箱查看邮件，完成注册！'
                    after_url = "jdsj:login"
                    after_page = '登录页'
                    return render(request, 'main/after.html',
                                  {'after_url': after_url, 'message': message, 'after_page': after_page})
                except:
                    message = '邮箱账号错误,请重新填写！'
                    after_url = "jdsj:forget"
                    after_page = '忘记密码页'
                    return render(request, 'main/after.html',
                                  {'after_url': after_url, 'message': message, 'after_page': after_page})


class Register(views.View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'main/register.html', {'username': 1, 'register_form': register_form})

    def post(self, request):
        email = request.POST.get("email").strip()
        verif = uuid1()
        verif_md5 = pwd_encrypt(str(verif))
        u1 = User.objects.filter(email=email)
        if u1:

            message = '此账号已注册！'
            after_url = "jdsj:login"
            after_page = '登录页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        else:
            s1 = Send_email.objects.filter(email_address=email).first()
            if s1:
                diff = timezone.now() - s1.data_time
                diff = diff.seconds / 60
                if diff < 5:
                    message = '邮件已发送，到您的邮箱查看，请不要重复发送。如果没有找到邮件，请检查填写邮箱是否错误，或等待5分钟后再次发送'
                    after_url = "jdsj:login"
                    after_page = '登录页'
                    return render(request, 'main/after.html',
                                  {'after_url': after_url, 'message': message, 'after_page': after_page})
                else:

                    try:
                        send_mail('django 项目账号注册',
                                  f"此邮件不要泄露给他人，收到邮件后请在5分钟内请点击注册网址：'http://si-yu.zicp.vip/jdsj/main/registing/{verif}'",
                                  '979746262@qq.com', [email, ])

                        s1.email_address = email
                        s1.data_time = timezone.now()
                        s1.verif = verif_md5
                        s1.static = 1
                        s1.save()
                        message = '邮件已重新发送，请登陆邮箱查看邮件，完成注册！'
                        after_url = "jdsj:login"
                        after_page = '登录页'
                        return render(request, 'main/after.html',
                                      {'after_url': after_url, 'message': message, 'after_page': after_page})

                    except Exception as e:
                        print(e)
                        message = '邮箱账号错误,请重新填写！'
                        after_url = "jdsj:register"
                        after_page = '注册页'
                        return render(request, 'main/after.html',
                                      {'after_url': after_url, 'message': message, 'after_page': after_page})
            else:
                try:
                    send_mail('django 项目账号注册',
                              f"此邮件不要泄露给他人，收到邮件后请在5分钟内请点击注册网址：'http://si-yu.zicp.vip/jdsj/main/registing/{verif}'",
                              '979746262@qq.com', [email, ])

                    se1 = Send_email(email, timezone.now(), verif_md5, 1)
                    se1.save()
                    message = '邮件已成功发送，请登陆邮箱查看邮件，完成注册！'
                    after_url = "jdsj:login"
                    after_page = '登录页'
                    return render(request, 'main/after.html',
                                  {'after_url': after_url, 'message': message, 'after_page': after_page})
                except Exception as e:
                    print(e)
                    message = '邮箱账号错误,请重新填写！'
                    after_url = "jdsj:register"
                    after_page = '注册页'
                    return render(request, 'main/after.html',
                                  {'after_url': after_url, 'message': message, 'after_page': after_page})


class Registing(views.View):
    def get(self, request, verif):
        register_form = RegisterForm()
        s1 = Send_email.objects.filter(verif=pwd_encrypt(verif)).first()
        if not s1:
            message = '邮箱验证网址有误！请重新发送验证网址'
            after_url = "jdsj:register"
            after_page = '注册'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})

        diff = timezone.now() - s1.data_time
        diff = diff.seconds / 60
        if diff > 5:
            message = '链接已失效，请重新发送！'
            after_url = "jdsj:register"
            after_page = '注册页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        if s1.static != 1 and not s1:
            message = '邮箱验证网址有误！请重新发送验证网址'
            after_url = "jdsj:register"
            after_page = '注册页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        return render(request, 'main/registing.html', {'register_form': register_form, 'verif': verif})

    def post(self, request, verif):
        register_form = RegisterForm()
        s1 = Send_email.objects.filter(verif=pwd_encrypt(verif)).first()
        email_address = s1.email_address
        birth = request.POST.get('birth').strip()
        sex = request.POST.get('sex').strip()
        tell = request.POST.get('tell').strip()
        nick_name = request.POST.get('nick_name').strip()
        pwd = request.POST.get('pwd1').strip()
        pwd2 = request.POST.get('pwd2').strip()
        if pwd == pwd2 and not (pwd.isalpha() or pwd.isdigit()):
            pwd_md5 = pwd_encrypt(pwd)
            try:
                u1 = User(email=email_address, birth=birth, sex=sex,header_photo='http://img.mp.itc.cn/upload/20170724/cf678e09eb384401aa616ba134126357_th.jpg', tell=tell, nick_name=nick_name, pwd=pwd_md5,
                          balance=100000)
                u1.save()
                s1.delete()
            except Exception as e:
                print(e)
                return render(request, 'main/registing.html', {'register_form': register_form, 'verif': verif})
            message = '恭喜您，注册成功！'
            after_url = "jdsj:login"
            after_page = '登录页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        else:
            message = '请两次输入一致，并且密码必须字母和数字组合的密码'
            return render(request, 'main/registing.html',
                          {'message': message, 'register_form': register_form, 'verif': verif})


class Change_pwd(views.View):
    def get(self, request, verif):
        s1 = Send_email.objects.filter(verif=pwd_encrypt(str(verif))).first()
        if not s1:
            message = '邮箱验证网址有误，请重新发送验证邮件！'
            after_url = "jdsj:forget"
            after_page = '忘记密码页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        diff = timezone.now() - s1.data_time
        diff = diff.seconds / 60
        if diff > 5:
            message = '链接已失效，请重新发送！'
            after_url = "jdsj:forget"
            after_page = '忘记密码页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        if s1.static != 2 or not s1:
            message = '邮箱验证网址有误！请重新发送验证网址'
            after_url = "jdsj:forget"
            after_page = '忘记密码页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        register_form = RegisterForm()
        return render(request, 'main/change-pwd.html', {'register_form': register_form, 'verif': verif})

    def post(self, request, verif):
        register_form = RegisterForm()
        s1 = Send_email.objects.filter(verif=pwd_encrypt(str(verif))).first()
        email_address = s1.email_address
        pwd = request.POST.get('pwd1').strip()
        pwd2 = request.POST.get('pwd2').strip()
        if pwd == pwd2 and not (pwd.isalpha() or pwd.isdigit()):
            pwd_md5 = pwd_encrypt(pwd)
            try:
                u1 = User.objects.filter(email=email_address).first()
                u1.pwd = pwd_md5
                u1.save()
            except Exception as e:
                message = '由于服务器原因修改失败！请稍后重新打开邮件链接'
                after_url = "jdsj:forget"
                after_page = '忘记密码页'
                return render(request, 'main/after.html',
                              {'after_url': after_url, 'message': message, 'after_page': after_page, 'verif': verif})
            # if forms.is_valid():
            #     all_data = register_form.clean()
            #     return render(request, 'main/change-pwd.html', {'register_form': register_form, 'verif': verif})
            s1.delete()
            message = '恭喜您，修改密码成功！'
            after_url = "jdsj:login"
            after_page = '登录页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        else:
            message = '请两次输入一致，并且密码必须字母和数字组合的密码'
            return render(request, 'main/change-pwd.html',
                          {'message': message, 'register_form': register_form, 'verif': verif})


class Detail(views.View):
    def get(self, request, pid, message):
        email = request.session.get('email', '')
        nick_name = None
        if email:
            nick_name = User.objects.filter(email=email).first().nick_name
        phone = Phone_jdsj.objects.filter(pid=pid).first()
        skid = phone.skid
        color = phone.color
        config = phone.config
        image = Image.objects.filter(skid=phone.skid, color=phone.color).first()
        images = json.loads(image.img_url)
        colors = Phone_jdsj.objects.filter(skid=phone.skid).values("color").distinct()
        configs = Phone_jdsj.objects.filter(skid=phone.skid, color=color).values("config").distinct()
        colors = [i['color'] for i in colors]
        configs = [i['config'] for i in configs]
        return render(request, 'main/order-details.html',
                      {'images': images, 'phone': phone, 'colors': colors, 'configs': configs, 'color2': color,
                       'config2': config, 'skid': skid, 'username': nick_name, 'message': message})


class Choice_color(views.View):
    def get(self, request, skid, col, message):
        email = request.session.get('email', '')
        nick_name = None
        if email:
            nick_name = User.objects.filter(email=email).first().nick_name
        phone = Phone_jdsj.objects.filter(skid=skid, color=col).first()
        pid = phone.pid
        phone = Phone_jdsj.objects.filter(pid=pid).first()
        skid = phone.skid
        color = phone.color
        config = phone.config
        image = Image.objects.filter(skid=phone.skid, color=phone.color).first()
        images = json.loads(image.img_url)
        colors = Phone_jdsj.objects.filter(skid=phone.skid).values("color").distinct()
        configs = Phone_jdsj.objects.filter(skid=phone.skid, color=color).order_by('config').values("config").distinct()

        colors = [i['color'] for i in colors]
        configs = [i['config'] for i in configs]
        configs.sort(key=num1)
        print(configs)
        return render(request, 'main/order-details.html',
                      {'images': images, 'phone': phone, 'colors': colors, 'configs': configs, 'color2': color,
                       'config2': config, 'skid': skid, 'username': nick_name, 'message': message})
        # phone = Phone_jdsj.objects.filter(pid=pid).first()
        # skid = phone.skid
        # color = phone.color
        # config = phone.config
        # image = Image.objects.filter(skid=phone.skid, color=phone.color).first()
        # images = json.loads(image.img_url)
        # colors = Phone_jdsj.objects.filter(skid=phone.skid).values("color").distinct()
        # configs = Phone_jdsj.objects.filter(skid=phone.skid).values("config").distinct()
        # colors = [i['color'] for i in colors]
        # configs = [i['config'] for i in configs]
        # return render(request, 'main/order-details.html',
        #               {'images': images, 'phone': phone, 'colors': colors, 'configs': configs, 'color2': color,
        #                'config2': config, 'skid': skid})


class Choice_config(views.View):
    def get(self, request, skid, col, con, message):
        email = request.session.get('email', '')
        nick_name = None
        if email:
            nick_name = User.objects.filter(email=email).first().nick_name
        phone = Phone_jdsj.objects.filter(skid=skid, color=col, config=con).first()
        skid = phone.skid
        image = Image.objects.filter(skid=phone.skid, color=phone.color).first()
        images = json.loads(image.img_url)
        colors = Phone_jdsj.objects.filter(skid=phone.skid).values("color").distinct()
        configs = Phone_jdsj.objects.filter(skid=phone.skid, color=col).order_by('config').values(
            "config").distinct().order_by('config')
        colors = [i['color'] for i in colors]
        configs = [i['config'] for i in configs]
        configs.sort(key=num1)
        return render(request, 'main/order-details.html',
                      {'images': images, 'phone': phone, 'colors': colors, 'configs': configs, 'color2': col,
                       'config2': con, 'skid': skid, 'username': nick_name, 'message': message})


class Search(views.View):
    def post(self, request):
        keyword = request.POST.get('search-name').strip()
        email = request.session.get('email', '')
        nick_name = None
        if email:
            nick_name = User.objects.filter(email=email).first().nick_name
        slides = Slide.objects.all()
        first_slide = slides[0]
        phone_jdsjs = Phone_jdsj.objects.filter(title__icontains=keyword).all().order_by('-commentCount')
        wrong = None
        script = None
        if not phone_jdsjs:
            wrong = '很抱歉，没有找到相关商品！'
            script = 'alert'
            phone_jdsjs = Phone_jdsj.objects.all().order_by('-commentCount')
        a = 0
        phone_list = []
        defe_list = []
        for item in phone_jdsjs:
            if item.skid in defe_list:
                pass
            else:
                defe_list.append(item.skid)
                a += 1
                image = Image.objects.filter(skid=item.skid).first()
                if image:
                    item_dict = {}
                    item_dict['image_url'] = json.loads(image.img_url)[0].replace('n5/jfs', 'n1/s540x540_jfs').replace(
                        'n5/s54x54_jfs', 'n1/s540x540_jfs')
                    item_dict['pid'] = item.pid
                    item_dict['price'] = item.price
                    item_dict['skid'] = item.skid
                    item_dict['defaultGoodCountStr'] = item.defaultGoodCountStr
                    item_dict['commentCountStr'] = item.commentCountStr
                    item_dict['goodRateShow'] = item.goodRateShow
                    item_dict['title'] = item.title
                    phone_list.append(item_dict)
                else:
                    p1s = Phone_jdsj.objects.filter(skid=item.skid).all()
                    for p1 in p1s:
                        p1.delete()
        return render(request, 'main/main.html',
                      {'slides': slides, 'first_slide': first_slide, 'phone_list': phone_list, 'username': nick_name, 'wrong':wrong, 'script':script})
