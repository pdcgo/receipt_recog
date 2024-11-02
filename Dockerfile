
FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt

RUN apt-get update
RUN apt-get install zbar-tools -y
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install pyzbar[scripts]


COPY ./main.py /code/app/main.py
COPY ./tool.py /code/app/tool.py

EXPOSE 8080


CMD ["fastapi", "run", "app/main.py", "--port", "8080"]