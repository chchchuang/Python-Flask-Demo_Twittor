from twittor import create_app  # 不需指定__init__
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

''' flask-migrate方法失效,改用 cli
>>> flask db init
>>> flask db migrate -m "create user" #表
>>> flask db migrate -m "add phone" #項目
>>> flask db current #目前版本號
>>> flask db upgrade #進版 執行後才會在SQLite看到表等更新項目
>>> flask db downgrade #退版 MySQL可以drop, SQLite不能drop
'''

''' 使用python3 cli進行數據庫操作
>>> from twittor import create_app, db
>>> app=create_app()
>>> db
<SQLAlchemy>
>>> app.app_context().push()
>>> db
<SQLAlchemy sqlite:////Users/chchchuang/Desktop/SideProject/lesson/udemy_Flask/TWITTOR/twittor/twittor.db>
增
>>> from twittor.models import User, Tweet
>>> u = User(username='admin', email='admin@admin.com')
>>> db.session.add(u)
>>> db.session.commit()
>>> u = User(username='test1', email='test1@admin.com')
>>> db.session.add(u)
>>> db.session.commit()
查
>>> User.query.all()
[id=1, username=admin, email=admin@admin.com, password_hash=None, id=2, username=test1, email=test1@admin.com, password_hash=None]
>>> User.query.get(1)
id=1, username=admin, email=admin@admin.com, password_hash=None
刪
>>> u = User.query.get(2)
>>> u
id=2, username=test1, email=test1@admin.com, password_hash=None
>>> db.session.delete(u)
>>> db.session.commit()
>>> User.query.all()
[id=1, username=admin, email=admin@admin.com, password_hash=None]
改
>>> u = User.query.get(1)
>>> u
id=1, username=admin, email=admin@admin.com, password_hash=None
>>> u.email = "admin_new@admin.com"
>>> db.session.commit()
>>> User.query.get(1)
id=1, username=admin, email=admin_new@admin.com, password_hash=None
'''