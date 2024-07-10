
# 基于Python官方镜像
FROM python:3.9-slim
 
# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
# 创建工作目录
WORKDIR /app
 
# 安装依赖
COPY requirements.txt /app/
#配置安装依赖
RUN python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 复制Django项目到工作目录
COPY . /app/
 
# 创建数据库表结构
RUN python manage.py migrate
 
# 创建超级用户（可选）
# RUN python manage.py createsuperuser
 
# 暴露端口
EXPOSE 8000
 
# 运行Django开发服务器
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# 使用多阶段构建，同时支持 HTTP 和 WebSocket
FROM python:3.9-slim as http_server
COPY --from=0 /app /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.9-slim as websocket_server
COPY --from=0 /app /app
CMD ["daphne", "vue-admin-api.asgi:application"]