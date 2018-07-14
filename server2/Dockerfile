FROM python:3.6-alpine
ADD . /server
WORKDIR /server
RUN apk update
RUN apk add gcc python3-dev musl-dev build-base linux-headers pcre-dev
RUN apk add postgresql-dev
RUN pip install -r requirements.txt
CMD ["python", "index.py"]
