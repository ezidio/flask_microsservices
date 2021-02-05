FROM python:3.8

# Adiciona usuario de trabalho
RUN adduser --disabled-password --gecos '' python

# Copia configuração e instala dependencias
COPY ./requirements/requirements.txt /app/requirements.txt
RUN su python -c 'python -m venv ~/.env'
RUN su python -c 'source ~/.env/bin/activate  && pip install -r /app/requirements.txt'

# Copia conteudo da aplicação para o /app
WORKDIR /app
COPY ./src /app

USER python

# Configuração do multiprocess do prometheus
ENV prometheus_multiproc_dir /tmp/prometheus
RUN mkdir /tmp/prometheus

EXPOSE 5000
CMD . ~/.env/bin/activate && uwsgi --ini /app/wsgi.ini