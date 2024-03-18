# 使用官方的 Python 3.8 镜像作为基础镜像
FROM python:3.8-slim-buster

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到工作目录中
COPY hsbot_refac.py /app/hsbot_refac.py

# 安装依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple bs4 cloudscraper requests amiyabot

# 设置启动命令
CMD ["python", "./hsbot_refac.py"]