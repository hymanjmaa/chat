import random
import subprocess
import time

from flask import render_template, send_from_directory, request, redirect, url_for, jsonify
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from selenium import webdriver
from selenium.webdriver.common.by import By

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


class ChatView(BaseView):
    route_base = '/chatview'
    default_view = 'chat1'
    allow_browser_login = True

    @expose('/chat1')
    def chat1(self):
        if not current_user.is_authenticated:
            return redirect(url_for('AuthDBView.login', next=request.url))
        return self.render_template('bot1.html')

    @expose('/chat2')
    def chat2(self):
        if not current_user.is_authenticated:
            return redirect(url_for('AuthDBView.login', next=request.url))
        return self.render_template('bot2.html')

    @expose('/chat3')
    def chat3(self):
        if not current_user.is_authenticated:
            return redirect(url_for('AuthDBView.login', next=request.url))
        return self.render_template('bot3.html')

    @expose('/execute_script')
    def trigger_script(self):
        # if not current_user.is_authenticated:
        #     return redirect(url_for('AuthDBView.login', next=request.url))
        order_num = request.args.get('order_num', random.choice(['20250317118', '20250317119',
                                                                 '20250317120', '20250317121']))
        result = subprocess.run(['python', 'rpa.py'], capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
        order_info = {
            'order_num': order_num,
            'order_status': random.choice(['Init', 'Packing', 'Delivering', 'Completed']),
            'user': random.choice(['Alice', 'Bob', 'Charlie', 'David', 'Eve'])
        }
        return jsonify({'msg': output or error, 'status': 0, 'order_info': order_info})

    @protect()
    @expose('/action_browser')
    def action_browser(self):
        # if not current_user.is_authenticated:
        #     return redirect(url_for('AuthDBView.login', next=request.url))
        driver = webdriver.Chrome()
        driver.get('https://www.baidu.com')
        search = driver.find_element(By.ID, "kw")
        search.send_keys('LLM')
        send_button = driver.find_element(By.ID, "su")
        send_button.click()
        time.sleep(3)
        driver.quit()
        return jsonify({'msg': 'action browser success', 'status': 0})


# 修改后的配置
appbuilder.add_view(
    ChatView,
    "Chat Bot 1",
    href="/chatview/chat1",  # 修改 href 路径
    icon="fa-comments",
    category="聊天机器人",
    category_icon="fa-robot"
)

appbuilder.add_view(
    ChatView,
    "Chat Bot 2",
    href="/chatview/chat2",  # 修改 href 路径
    icon="fa-comments",
    category="聊天机器人",
    category_icon="fa-robot"
)

appbuilder.add_view(
    ChatView,
    "Chat Bot 3",
    href="/chatview/chat3",  # 修改 href 路径
    icon="fa-comments",
    category="聊天机器人",
    category_icon="fa-robot"
)

appbuilder.add_view(
    ChatView,
    "执行脚本",
    href="/chatview/execute_script",  # 修改 href 路径
    icon="fa-play",
    category="聊天机器人",
    category_icon="fa-robot"
)

appbuilder.add_view(
    ChatView,
    "浏览器操作",
    href="/chatview/action_browser",  # 修改 href 路径
    icon="fa-chrome",
    category="聊天机器人",
    category_icon="fa-robot"
)

db.create_all()
