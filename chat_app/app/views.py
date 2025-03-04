from flask import render_template, send_from_directory, request, redirect, url_for
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db, app
from flask_appbuilder import BaseView
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.security.decorators import protect
from flask_login import current_user
from flask_appbuilder.security.views import AuthDBView


"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


class MyAuthDBView(AuthDBView):
    def login(self):
        next_url = request.args.get('next')  # 获取用户之前访问的页面
        response = super().login()  # 调用原 FAB 登录逻辑

        if current_user.is_authenticated and next_url:
            return redirect(next_url)  # 登录成功后跳转回原页面
        return response  # 继续默认逻辑


# 替换默认的 AuthDBView
appbuilder.security_manager_class.auth_view = MyAuthDBView


class ChatApi(BaseApi):
    route_base = '/'

    @expose('chat1')
    def chat1(self):
        if not current_user.is_authenticated:
            # 记录用户请求的URL，并重定向到登录页面
            return redirect(url_for('AuthDBView.login', next=request.url))
        return render_template('bot1.html')

    @expose('chat2')
    def chat2(self):
        if not current_user.is_authenticated:
            # 记录用户请求的URL，并重定向到登录页面
            return redirect(url_for('AuthDBView.login', next=request.url))
        return render_template('bot2.html')

    @expose('chat3')
    def chat3(self):
        if not current_user.is_authenticated:
            # 记录用户请求的URL，并重定向到登录页面
            return redirect(url_for('AuthDBView.login', next=request.url))
        return render_template('bot3.html')


appbuilder.add_api(ChatApi)
db.create_all()
