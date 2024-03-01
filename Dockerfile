# 使用官方的miniconda3基础镜像
FROM continuumio/miniconda3

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到工作目录中
COPY . /app

# 使用conda安装Python 3.7
RUN conda install python=3.8

# 使用environment.yml文件创建conda环境
RUN conda env create -f environment.yml

# 激活conda环境
RUN echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH


# 安装bs4库
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple bs4 cloudscraper requests
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple amiyabot

# 设置启动命令
CMD ["python", "./hsbot-refac.py"]