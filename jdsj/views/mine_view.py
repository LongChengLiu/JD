from django.shortcuts import render, HttpResponse
from jdsj.models import Phone_jdsj, Image, User
import json
from django import views
from .sjfroms import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid1
import base64
import myconfig
import os
from qiniu import Auth, put_file, etag


class Mine(views.View):
    def get(self, request):
        email = request.session.get('email')
        if not email:
            message = '您还没有登录！'
            after_url = "jdsj:login"
            after_page = '登录页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        u1 = User.objects.filter(email=email).first()
        return render(request, 'mine/mine.html', {'username': 1, 'u1': u1})


class Info(views.View):
    def get(self, request):
        register_form = RegisterForm()
        email = request.session.get('email')
        u1 = User.objects.filter(email=email).first()
        if u1.sex == 1:
            u1.sex = '男'
        else:
            u1.sex = '女'
        return render(request, 'mine/change-info.html', {'u1': u1, 'register_form': register_form, 'username': 1})

    def post(self, request):
        register_form = RegisterForm()
        email = request.session.get('email')
        u1 = User.objects.filter(email=email).first()
        nick_name = request.POST.get('nick_name')
        sex = request.POST.get('sex')
        birth = request.POST.get('birth')
        tell = request.POST.get('tell')
        u1.nick_name = nick_name
        u1.sex = sex
        u1.birth = birth
        u1.tell = tell
        try:
            u1.save()
            message = '信息修改成功！'
            after_url = "jdsj:mine"
            after_page = '我的'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        except Exception as e:
            message = '信息修改失败，请重试！'
            return render(request, 'mine/change-info.html',
                          {'u1': u1, 'register_form': register_form, 'username': 1, 'message': message})


class Order_info(views.View):
    def get(self, request):
        email = request.session.get('email')
        u1 = User.objects.filter(email=email).first()
        nick_name = u1.nick_name
        cart = u1.cart
        if not cart:
            cart = '{}'
        cart = json.loads(cart)
        cart_list = []

        for key, value in cart.items():
            sum_price = 0
            cart_dict = {}
            p1 = Phone_jdsj.objects.filter(pid=key).first()
            color = p1.color
            img1 = Image.objects.filter(skid=p1.skid, color=color).first()
            cart_dict['pid'] = p1.pid
            cart_dict['title'] = p1.title
            cart_dict['config'] = p1.config
            cart_dict['color'] = p1.color
            cart_dict['price'] = float(p1.price)
            cart_dict['flag'] = 1
            sum_price = float(p1.price) * value
            cart_dict['count'] = value
            cart_dict['img_url'] = json.loads(img1.img_url)[0].replace('n5/jfs', 'n1/s320x320_jfs').replace(
                'n5/s54x54_jfs', 'n1/s320x320_jfs')
            cart_dict['sum_price'] = sum_price
            cart_list.append(cart_dict)
        return render(request, 'mine/order-info.html',
                      {'cart_list': cart_list, 'username': nick_name})


# http://q8gl2rnhc.bkt.clouddn.com/f88e2a3c98278525d0e8cb5d3b0f23d.jpg
class Balance(views.View):
    def get(self, request):
        email = request.session.get('email')
        u1 = User.objects.filter(email=email).first()
        balance = u1.balance
        return render(request, 'mine/balance-info.html', {'balance': balance})


class Change_hp(views.View):
    def get(self, request):
        email = request.session.get('email')
        return render(request, 'mine/change-hp.html', {'email': email})

    def post(self, request):
        file = request.read()
        print(file)
        path = r'C:\Users\Administrator\Desktop\image'
        test = file.decode()
        print(type(test))

        bs = base64.b64decode(test[22:])
        print(bs)
        with open(f'{path}' + '\\' + '1.png', 'wb') as f:
            f.write(bs)
        return HttpResponse({'data': '保存成功'})


@csrf_exempt
def change_pp(request):
    if request.method == "POST":
        pic_name = str(uuid1())
        file_path = r'E:/py-probject/Jd/static/media/' + pic_name + '.png'
        try:
            file = request.POST
            data = file.getlist('data')[0]
            print(data)
            email = file.getlist('email')[0]

            path = r'static/media/'

            print(type(data))
            bs = base64.b64decode(data[22:])
            with open(path + pic_name + '.png', 'wb') as f:
                f.write(bs)
            # 需要填写你的 Access Key 和 Secret Key
            access_key = myconfig.access_key
            secret_key = myconfig.secret_key
            # 构建鉴权对象
            q = Auth(access_key, secret_key)
            # 要上传的空间
            bucket_name = 'llcimage'
            # 上传后保存的文件名
            key = pic_name
            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(bucket_name, key)
            # 要上传文件的本地路径
            ret, info = put_file(token, key, file_path)
            print(info)
            assert ret['key'] == key
            assert ret['hash'] == etag(file_path)

            u1 = User.objects.filter(email=email).first()
            u1.header_photo = 'http://q8gl2rnhc.bkt.clouddn.com/' + pic_name
            u1.balance += 1.0
            u1.save()
        except Exception as e:
            print(e)
            if os.path.exists(file_path):
                os.remove(file_path)
            return HttpResponse(json.dumps({'status': 1, 'info': '上传失败，请重新上传！'}))
        return HttpResponse(json.dumps({'status': 0, 'info': '上传成功！'}))
