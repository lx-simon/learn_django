# day3 Django开发

- 部门管理
- 用户管理
  - 用户列表
  - 新建用户
    - ModelForm，针对数据库中的某个表。
    - Form。

# 续写day2代码

- 分页的逻辑和处理逻辑规则
  - 从头到尾开发
  - 写项目用【pagination.py】公共组件
- 小Bug, 搜索+分页情况下。

```
分页的时候保留原来的搜索条件
http://127.0.0.1:8000/pretty/list/?q=888
http://127.0.0.1:8000/pretty/list/?page=1

http://127.0.0.1:8000/pretty/list/?q=888&page=1
```

分页
