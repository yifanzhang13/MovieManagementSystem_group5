FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update  
RUN apt-get install python3-dev default-libmysqlclient-dev -y 

RUN mkdir /code/
WORKDIR /code/
RUN pip install pip -U -i https://mirrors.aliyun.com/pypi/simple/
ADD requirements.txt /code/
RUN python -m pip install -r requirements.txt 
ADD . /code/
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
