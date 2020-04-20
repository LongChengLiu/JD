from qiniu import Auth, put_file, etag, put_stream
from qiniu.utils import etag_stream
import qiniu.config
import time
import uuid

# 需要填写你的 Access Key 和 Secret Key
access_key = 'HU8AWrostwOmbdeWuzpDuH9J3SsXbKbE6ueTvky1'
secret_key = 'HUfUhZQPJdloPCeUdECnHr8SmEbv-iyY0dyMZZ6e'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'llcimage'
# 上传后保存的文件名
key = 'my-python-logo.png'
# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key)
# 要上传文件的本地路径

localfile = r'C:\Users\Administrator\Desktop\捕获.PNG'
file_name = uuid.uuid1()
with open(localfile,'rb') as f:
    input_stream = f.read()
size = len(input_stream)
modify_time = int(time.time())
ret, info =put_stream(token, key, input_stream, file_name, size, params=None,mime_type='application/octet-stream', progress_handler=None,upload_progress_recorder=None,modify_time=modify_time, keep_last_modified=False)

print(info)
print(info)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag_stream(input_stream)


# qiuniu yun2222
132312