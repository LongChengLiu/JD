from django import forms


class RegisterForm(forms.Form):
    num = forms.RegexField('[0-9]*?',min_length=1, max_length=4, label='数量：',widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(min_length=6, max_length=25, label='邮箱',
                             widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱地址', 'class': "form-control"}))
    sex = forms.ChoiceField(choices=((1, '男'), (2, '女')), initial=1, widget=forms.RadioSelect)
    tell = forms.CharField(min_length=11, max_length=11, label='手机号码',
                           widget=forms.TextInput(attrs={'placeholder': '请输入电话号码', 'class': "form-control"}))
    nick_name = forms.CharField(label='昵称', min_length=1, max_length=5,
                                widget=forms.TextInput(attrs={'placeholder': '请输入1-5位昵称', 'class': "form-control"}))
    pwd1 = forms.CharField(min_length=6, max_length=12, label='密码',
                           widget=forms.PasswordInput(attrs={'placeholder': '请输入6-12位密码', 'class': "form-control"}))
    pwd2 = forms.CharField(min_length=6, max_length=12, label='再次输入密码', show_hidden_initial=True,
                           widget=forms.PasswordInput(attrs={'placeholder': '请输入6-12位密码', 'class': "form-control"}))
    birth = forms.DateField(label='出生日期', widget=forms.DateInput(attrs={'type': 'date'}))
