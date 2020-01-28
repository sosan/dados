FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src

RUN pip install --upgrade pip

COPY requirements.txt /src/

RUN pip install -r requirements.txt

COPY . /src/

EXPOSE 8000
ENV FLASK_APP=main.py:app
CMD ["python", "src/main.py"]