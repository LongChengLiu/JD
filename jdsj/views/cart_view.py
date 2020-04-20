from django.shortcuts import render, redirect
from jdsj.models import Phone_jdsj, Image, User
import json
from django import views
import copy
from jdsj.views.sjfroms import RegisterForm


formss = RegisterForm()

class Cart(views.View):
    def get(self, request, flag_all, message):

        email = request.session.get('email', '')
        if not email:
            message = '您还没有登录！'
            after_url = "jdsj:login"
            after_page = '登录页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        u1 = User.objects.filter(email=email).first()
        nick_name = u1.nick_name
        order = u1.order
        if not order:
            order = '{}'
        order = json.loads(order)
        order_list = []
        sum_price = 0
        for key, value in order.items():
            order_dict = {}
            p1 = Phone_jdsj.objects.filter(pid=key).first()
            color = p1.color
            img1 = Image.objects.filter(skid=p1.skid, color=color).first()
            order_dict['pid'] = p1.pid
            order_dict['title'] = p1.title
            order_dict['config'] = p1.config
            order_dict['color'] = p1.color
            order_dict['price'] = float(p1.price) * abs(value)
            order_dict['flag'] = 1
            sum_price += order_dict['price']
            if value < 0:
                order_dict['flag'] = 0
                sum_price -= order_dict['price']
            order_dict['count'] = abs(value)
            order_dict['img_url'] = json.loads(img1.img_url)[0].replace('n5/jfs', 'n1/s320x320_jfs').replace(
                'n5/s54x54_jfs', 'n1/s320x320_jfs')
            order_list.append(order_dict)
        return render(request, 'cart/cart.html',
                      {'order_list': order_list, 'username': nick_name, 'flag_all': flag_all, 'sum_price': sum_price,
                       'message': message, 'formss': formss})


class Add_cart(views.View):
    def get(self, request, pid):
        email = request.session.get('email', '')
        nick_name = None
        if email:
            u1 = User.objects.filter(email=email).first()
        else:
            message = '您还没有登录！'
            after_url = "jdsj:login"
            after_page = '登录页'
            return render(request, 'main/after.html',
                          {'after_url': after_url, 'message': message, 'after_page': after_page})
        order = u1.order
        if order:
            order = json.loads(order)
            if pid in order:
                order[pid] += 1
            else:
                order[pid] = 1
        else:
            order = {}
            order[pid] = 1
        u1.order = json.dumps(order)
        u1.save()
        message = '此商品已添加到购物！'
        return redirect('jdsj:detail', pid, message)


class Add(views.View):
    def get(self, request, pid):
        email = request.session.get('email', '')
        u1 = User.objects.filter(email=email).first()
        order = u1.order
        if order:
            order = json.loads(order)
            if pid in order:
                print(pid in order)
                if order[pid] < 0:
                    order[pid] = -(abs(order[pid]) + 1)
                else:
                    order[pid] += 1
            else:
                order[pid] = 1
        else:
            order = {}
            order[pid] = 1
        u1.order = json.dumps(order)
        u1.save()
        return redirect('jdsj:cart', 1, 1)


class Sub(views.View):
    def get(self, request, pid):
        email = request.session.get('email', '')
        u1 = User.objects.filter(email=email).first()
        order = u1.order
        if order:
            order = json.loads(order)
            if pid in order:
                if abs(order[pid]) == 1:
                    order.pop(pid)
                else:
                    order[pid] = abs(order[pid]) - 1
            else:
                order[pid] = 1
        else:
            order = {}
            order[pid] = 1
        u1.order = json.dumps(order)
        u1.save()
        return redirect('jdsj:cart', 1, 1)


class Comm_choose(views.View):
    def get(self, request, pid):
        email = request.session.get('email', '')
        u1 = User.objects.filter(email=email).first()
        order = u1.order
        if order:
            order = json.loads(order)
            order[pid] = -order[pid]
        u1.order = json.dumps(order)
        u1.save()
        return redirect('jdsj:cart', 1, 1)


class Comm_chooseall(views.View):
    def get(self, request, flag_all):
        email = request.session.get('email', '')
        u1 = User.objects.filter(email=email).first()
        order = u1.order
        order = json.loads(order)

        for key, value in order.items():
            if flag_all:
                order[key] = abs(value)
            else:
                order[key] = -abs(value)

        u1.order = json.dumps(order)
        u1.save()
        return redirect('jdsj:cart', flag_all, 1)


class Account_sum(views.View):
    def get(self, request):
        email = request.session.get('email', '')
        u1 = User.objects.filter(email=email).first()
        order = u1.order
        order = json.loads(order)
        order1 = copy.deepcopy(order)
        if not u1.cart:
            u1.cart = '{}'
        cart = json.loads(u1.cart)
        print(cart)
        sum_price = 0
        for key, value in order1.items():
            p1 = Phone_jdsj.objects.filter(pid=key).first()
            if value < 0:
                order[key] = abs(value)
            else:
                sum_price += float(p1.price) * abs(value)
                order.pop(key)
                cart[key] = value
        balance = u1.balance - sum_price
        if balance >= 0:
            u1.balance = balance
            u1.cart = json.dumps(cart)
            u1.order = json.dumps(order)
            u1.save()
            message = f'已成功结算，本次共消费:{sum_price}元，账户余额:{balance}'
            return redirect('jdsj:cart', 1, message)
        else:
            message = '余额不足！'
            return redirect('jdsj:cart', 1, message)


class Change_count(views.View):
    def post(self, request, pid):
        count = request.POST.get('num')
        if count.isdigit():
            if int(count) >= 0:
                email = request.session.get('email', '')
                u1 = User.objects.filter(email=email).first()
                order = u1.order
                if order:
                    order = json.loads(order)
                    if pid in order:
                        print(pid in order)
                        if order[pid] < 0:
                            order[pid] = -(int(count))
                        else:
                            order[pid] = int(count)
                    else:
                        order[pid] = 1
                else:
                    order = {}
                    order[pid] = 1
                u1.order = json.dumps(order)
                u1.save()
                return redirect('jdsj:cart', 1, 1)
        message = '输入数值有误，请重新输入！'
        return redirect('jdsj:cart', 1, message)