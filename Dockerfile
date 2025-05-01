FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

# CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--reload"]