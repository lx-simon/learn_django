from django.db import models
# 重要，对数据库操作
# Create your models here.

class UserInfo(models.Model):
    '''
    create table  app01_userinfo(
        id bigint auto_increment primary key,
        name varchar(32),
        password varchar(64),
        age int
    )
    '''
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField(default=18)
    # size = models.IntegerField()
    # data = models.IntegerField(null=True, blank=True)

class Department(models.Model):
    title = models.CharField(max_length=16)


class Role(models.Model):
    caption = models.CharField(max_length=16)

################# 新建数据 ################

# 本质 insert into app01_department (title) values ('销售部')
# Department.objects.create(title="销售部")
# Department.objects.create(title="技术部")    
# UserInfo.objects.create(name="xll", password="123", age=18)
