FROM debian:9.7
RUN apt-get update
RUN apt-get install python3 curl wget python3-pip git bzip2 readline-common sqlite3 -y
RUN apt-get update && apt-get install -y python python-dev python3 python3-dev python3-pip virtualenv libssl-dev libpq-dev git build-essential libfontconfig1 libfontconfig1-dev
RUN pip3 install setuptools pip --upgrade --force-reinstall
RUN curl https://pyenv.run -o install-pyenv.sh
RUN bash install-pyenv.sh
RUN git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
RUN chmod +x /root/.pyenv/bin
RUN eval "$(pyenv virtualenv-init -)"
RUN export PATH="/root/.pyenv/bin:$PATH"
RUN eval "$(pyenv init -)"


RUN /root/.pyenv/bin/pyenv install 3.6.8
RUN /root/.pyenv/bin/pyenv virtualenv 3.6.8 mate_counter
RUN virtualenv /venv/testenv/ -p which python3.6.8

ENV target_dir /opt/mate_counter
RUN mkdir ${target_dir}

COPY counter ${target_dir}/counter
COPY manage.py ${target_dir}/manage.py
COPY mate_counter ${target_dir}/mate_counter
COPY .python-version ${target_dir}/.python-version
COPY requirements.txt ${target_dir}/requirements.txt
COPY start.sh /start.sh

RUN pip3 install -r ${target_dir}/requirements.txt

CMD ["./start.sh"]

EXPOSE 8000:8000
