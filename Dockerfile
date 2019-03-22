FROM python:3.6.8

RUN pip install setuptools pip --upgrade --force-reinstall
ENV TARGET_DIR /opt/mate_counter
RUN mkdir ${TARGET_DIR}

COPY . ${TARGET_DIR}/

RUN pip install -r ${TARGET_DIR}/requirements.txt
WORKDIR $TARGET_DIR

EXPOSE 8000:8000
CMD /bin/sh -c "./wait-for-it.sh $DJANGO_DATABASE_HOST:$DJANGO_DATABASE_PORT -- ./manage.py makemigrations &&./manage.py migrate && ./manage.py runserver 0.0.0.0:8000"
