# chat

## Python version: 3.9

## install
```commandline
pip install -r requirements.txt
cd chat_app
python run.py
```

## 接口文档
### 1. Chat Bot 1
- 路径 : /chatview/chat1
- 方法 : GET
- 说明 : 聊天机器人界面1
- 认证 : 需要登录
- 返回 : HTML页面
### 2. Chat Bot 2
- 路径 : /chatview/chat2
- 方法 : GET
- 说明 : 聊天机器人界面2
- 认证 : 需要登录
- 返回 : HTML页面
### 3. Chat Bot 3
- 路径 : /chatview/chat3
- 方法 : GET
- 说明 : 聊天机器人界面3
- 认证 : 需要登录
- 返回 : HTML页面
### 4. 执行脚本
- 路径 : /chatview/execute_script
- 方法 : GET
- 说明 : 执行RPA脚本
- 认证 : 需要登录
- 返回 : JSON
  ```json
  {
    "msg": "执行结果",
    "status": 0
  }
   ```
### 5. 浏览器操作
- 路径 : /chatview/action_browser
- 方法 : GET
- 说明 : 自动化操作浏览器
- 认证 : 需要登录
- 返回 : JSON
  ```json
  {
    "msg": "action browser success",
    "status": 0
  }
   ```
## 认证说明
- 所有接口都需要登录认证
- 未登录访问时会自动跳转到登录页面
- 登录成功后会自动跳回原访问页面