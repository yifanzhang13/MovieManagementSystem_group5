FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update  
RUN apt-get install python3-dev default-libmysqlclient-dev -y 

RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install pip -U -i https://mirrors.aliyun.com/pypi/simple/
ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN rm -rf /code
ADD . /code/
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
