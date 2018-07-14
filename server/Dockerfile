FROM python:3.6-alpine
ADD . /www
WORKDIR /www
RUN apk update
RUN apk add gcc python3-dev musl-dev build-base linux-headers pcre-dev
RUN apk add postgresql-dev
RUN apk add uwsgi
RUN pip install -r requirements.txt
RUN pip install https://github.com/unbit/uwsgi/archive/uwsgi-2.0.zip#egg=uwsgi
CMD ["uwsgi", "--ini", "./uwsgi.ini"]
