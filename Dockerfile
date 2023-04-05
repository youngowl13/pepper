FROM nickgryg/alpine-pandas

WORKDIR /usr/src/pepper

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache g++ python3-dev postgresql-dev musl-dev snappy-dev krb5-dev

RUN pip install --upgrade pip 
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
