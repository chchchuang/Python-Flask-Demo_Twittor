# 設置 venv: 1.$pip3 install virtualenv  2.$python3 -m virtualenv venv
# 啟動 venv: 1.cd到 venv folder  2.$source bin/activate
# 跳脫 venv: $deactivate
# docker執行 MySQL init
'''
$ docker run -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7
$ docker exec -it some-mysql sh # 進到 docker內
sh-4.2# mysql -u root -p
Enter password: 輸入密碼 root
mysql> CREATE DATABASE twittor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; #創 database
mysql> DROP DATABASE twittor; # 刪 database
mysql> SHOW DATABASES;
'''
# flask-migrate: manager方法失效,改用 cli方式進行 migrate
'''
(venv) chchchuang@StevendeMacBook-Pro TWITTOR % 
>>> flask db init # 初始化目錄 migrations folder
>>> flask db migrate -m "create user, tweet" #表
>>> flask db migrate -m "add phone" #項目
>>> flask db migrate -m "add new columns for user" #一次多項
>>> flask db current #目前版本號
>>> flask db upgrade #進版 執行後才會在SQLite看到表等更新項目
>>> flask db downgrade #退版 MySQL可以drop, SQLite不能drop
'''

# 使用python3 cli進行數據庫操作
''' 
>>> from twittor import create_app, db
>>> app=create_app()
>>> db
<SQLAlchemy>
>>> app.app_context().push() # 需進入 app的上下文內才能知道 db的配置
>>> db
<SQLAlchemy sqlite:////Users/chchchuang/Desktop/SideProject/lesson/udemy_Flask/TWITTOR/twittor/twittor.db>
>>> from twittor.models.user import User, Tweet

## 增
>>> u = User(username='admin', email='admin@admin.com')
>>> u.set_password('admin')
>>> db.session.add(u)
>>> db.session.commit()
>>> u1 = User(username='test1', email='test1@admin.com')
>>> u2 = User(username='test2', email='test2@admin.com')
>>> u = [u1, u2]
>>> db.session.add_all(u)
>>> db.session.commit()

## 查
>>> User.query.all()
[id=1, username=admin, email=admin@admin.com, password_hash=None, id=2, username=test1, email=test1@admin.com, password_hash=None]
>>> User.query.get(1) # get id==1的 user
id=1, username=admin, email=admin@admin.com, password_hash=None
# 補充篩選
>>> User.query.filter_by(username=admin).first()
# 補充排序
>>> User.query.filter_by(username=admin).order_by("value desc")

## 刪
>>> u = User.query.get(2)
>>> u
id=2, username=test1, email=test1@admin.com, password_hash=None
>>> db.session.delete(u)
>>> db.session.commit()
>>> User.query.all()
[id=1, username=admin, email=admin@admin.com, password_hash=None]

## 改
>>> u = User.query.get(1)
>>> u
id=1, username=admin, email=admin@admin.com, password_hash=None
>>> u.email = "admin_new@admin.com"
>>> db.session.commit()
>>> User.query.get(1)
id=1, username=admin, email=admin_new@admin.com, password_hash=None

## follow
>>> u1 = User.query.get(1) #get id==1
>>> u3 = User.query.get(3)
>>> u1.followed.append(u3)
>>> db.session.commit()

## check
>>> u1.followed.all()
[id=3, username=test2, email=test2@admin.com, password_hash=pbkdf2:sha256:260000$qQ4ZMEPM0YdbJlij$3058d53d8da527197b4d2e5ebf27488a64a8a7a7c77887bfefdf5c7091a84ce0]
>>> u3.followers.all()
[id=1, username=admin, email=admin@admin.com, password_hash=pbkdf2:sha256:260000$ctot9RdPKJ2e7PPg$b409df54a8ba417b5592f91c8e81aa451b5172e458c90d15823f54ee65c58da2]
>>> for u in u1.followed:
...     print(u)
id=3, username=test2, email=test2@admin.com, password_hash=pbkdf2:sha256:260000$qQ4ZMEPM0YdbJlij$3058d53d8da527197b4d2e5ebf27488a64a8a7a7c77887bfefdf5c7091a84ce0

## unfollow
>>> u1.followed.remove(u3)
>>> db.session.commit()
'''
