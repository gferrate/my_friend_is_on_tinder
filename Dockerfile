FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENV STATIC_INDEX 0
ENV STATIC_PATH /app/app/static

COPY . /app

#RUN /app/compile_translations.sh
