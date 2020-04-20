"""Jd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import main_view, cart_view, mine_view

app_name = 'jdsj'

urlpatterns = [
    path('main', main_view.Main.as_view(), name='main'),
    path('main/search', main_view.Search.as_view(), name='search'),
    path('main/login', main_view.Login.as_view(), name='login'),
    path('main/logout', main_view.Logout.as_view(), name='logout'),
    path('main/register', main_view.Register.as_view(), name='register'),
    path('main/forget', main_view.Forget.as_view(), name='forget'),
    path('main/registing/<str:verif>', main_view.Registing.as_view(), name='registing'),
    path('main/change_pwd/<str:verif>', main_view.Change_pwd.as_view(), name='change'),
    path('main/detail/<str:pid>/<str:message>', main_view.Detail.as_view(), name='detail'),
    path('main/detail/<str:skid>/<str:col>/<str:message>', main_view.Choice_color.as_view(), name='detail-col'),
    path('main/detail/<str:skid>/<str:col>/<str:con>/<str:message>', main_view.Choice_config.as_view(), name='detail-con'),
    path('cart/<int:flag_all>/<str:message>', cart_view.Cart.as_view(), name='cart'),
    path('cart/change_count/<str:pid>', cart_view.Change_count.as_view(), name='change-count'),
    path('cart/addcart/<str:pid>', cart_view.Add_cart.as_view(), name='addcart'),
    path('cart/add/<str:pid>', cart_view.Add.as_view(), name='add'),
    path('cart/sub/<str:pid>', cart_view.Sub.as_view(), name='sub'),
    path('cart/comm_choose/<str:pid>', cart_view.Comm_choose.as_view(), name='comm_choose'),
    path('cart/comm_chooseall/<int:flag_all>', cart_view.Comm_chooseall.as_view(), name='comm_chooseall'),
    path('cart/account_sum', cart_view.Account_sum.as_view(), name='account-sum'),
    path('mine', mine_view.Mine.as_view(), name='mine'),
    path('mine/info', mine_view.Info.as_view(), name='info'),
    path('mine/order_info', mine_view.Order_info.as_view(), name='order-info'),
    path('mine/balance_inf', mine_view.Balance.as_view(), name='balance-info'),
    path('mine/change_hp', mine_view.Change_hp.as_view(), name='change-hp'),
    path('mine/change_pp', mine_view.change_pp, name='change-pp'),
]
