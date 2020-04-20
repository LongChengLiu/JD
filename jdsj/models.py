from django.db.models import DateTimeField, EmailField, Model, DateField, TextField, FloatField, \
    IntegerField, AutoField, CharField


class Phone_jdsj(Model):
    pid = CharField(max_length=18, primary_key=True)
    skid = TextField()
    config = TextField()
    price = FloatField()
    color = TextField()
    configs = TextField()
    defaultGoodCount = IntegerField()
    defaultGoodCountStr = TextField()
    commentCount = IntegerField()
    commentCountStr = TextField()
    goodRateShow = FloatField()
    title = TextField(default='1')


class Image(Model):
    image_id = AutoField(primary_key=True)
    skid = TextField()
    color = TextField()
    img_url = TextField()


class Slide(Model):
    image_id = IntegerField(primary_key=True)
    skid = TextField()
    img_url = TextField()


class User(Model):
    email = EmailField(primary_key=True)
    birth = DateField()
    sex = IntegerField()
    tell = CharField(max_length=11)
    order = TextField()
    cart = TextField()
    header_photo = TextField()
    nick_name = CharField(max_length=18)
    pwd = CharField(max_length=32)
    balance = FloatField()



class Send_email(Model):
    email_address = EmailField(primary_key=True)
    data_time = DateTimeField()
    verif = CharField(max_length=37)
    static = IntegerField()


