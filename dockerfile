
# 基于Python官方镜像
FROM python:3.9-slim
 
# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
# 创建工作目录
WORKDIR /app
 
# 安装依赖
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
 
# 复制Django项目到工作目录
COPY . /app/
 
# 创建数据库表结构
RUN python manage.py migrate
 
# 创建超级用户（可选）
# RUN python manage.py createsuperuser
 
# 暴露端口
EXPOSE 8000
 
# 运行Django开发服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]