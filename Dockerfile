FROM python:3.8
WORKDIR /code


COPY ./requirements.txt /code
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

