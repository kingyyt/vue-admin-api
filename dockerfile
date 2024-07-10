# 使用官方的Python基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器的/app目录下
COPY . /app

# 安装依赖
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# 暴露端口
EXPOSE 8000

# 运行Django项目
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]