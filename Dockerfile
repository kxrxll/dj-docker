FROM python:3.11

COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src
EXPOSE 6060
WORKDIR src

CMD ["python3", "manage.py", "runserver"]