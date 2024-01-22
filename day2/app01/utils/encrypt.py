import hashlib

# 导入project里setting.py的配置
from django.conf import settings

def md5(data_string):
    # salt = "xxxxxxxxx" # 不加盐加密是固定，加盐变得随机
    # obj = hashlib.md5(salt.encode("utf-8"))
    # django setting里有随机值，不用自己生成盐
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
