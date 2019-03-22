FROM python:3.6.8

RUN pip install setuptools pip --upgrade --force-reinstall
ENV TARGET_DIR /opt/mate_counter
RUN mkdir ${TARGET_DIR}

COPY counter ${TARGET_DIR}/counter
COPY manage.py ${TARGET_DIR}/manage.py
COPY mate_counter ${TARGET_DIR}/mate_counter
COPY .python-version ${TARGET_DIR}/.python-version
COPY requirements.txt ${TARGET_DIR}/requirements.txt
COPY wait-for-it.sh ${TARGET_DIR}/wait-for-it.sh

RUN pip install -r ${TARGET_DIR}/requirements.txt
WORKDIR $TARGET_DIR

EXPOSE 8000:8000
CMD /bin/sh -c "./wait-for-it.sh $DJANGO_DATABASE_HOST:$DJANGO_DATABASE_PORT -- ./manage.py makemigrations; ./manage.py migrate ; ./manage.py runserver"
