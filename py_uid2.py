# #
#
#
# from qiniu import Auth, put_file, etag
# import qiniu.config
# #需要填写你的 Access Key 和 Secret Key
# access_key = 'HU8AWrostwOmbdeWuzpDuH9J3SsXbKbE6ueTvky1'
# secret_key = 'HUfUhZQPJdloPCeUdECnHr8SmEbv-iyY0dyMZZ6e'
# #构建鉴权对象
# q = Auth(access_key, secret_key)
# #要上传的空间
# bucket_name = 'llcimage'
# #上传后保存的文件名
# key = '捕获111111111111.PNG'
# #生成上传 Token，可以指定过期时间等
# token = q.upload_token(bucket_name, key, 3600)
# #要上传文件的本地路径
# localfile = r'C:\Users\Administrator\Desktop\捕获.PNG'
# ret, info = put_file(token, key, localfile)
# print(info)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)


# # http://q8gl2rnhc.bkt.clouddn.com/


1231