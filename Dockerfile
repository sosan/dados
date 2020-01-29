# suponemos que en la 3.8.X no habra muchos cambios
FROM python:3.8-slim-buster
# mas pequeña pero no tiene glib, empaqueta musl
# https://wiki.musl-libc.org/functional-differences-from-glibc.html
#FROM python:3.8.1-alpine3.11


# copiamos lugar volatil requirements
COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# creamos usuario para no ser root
RUN useradd --create-home usuarioapp
WORKDIR /home/usuarioapp

# creamos el arbol de directorios
COPY /src /home/usuarioapp/src
RUN chmod +x /home/usuarioapp/src/testing.sh

USER usuarioapp

# cambiamos directorio a SRC
WORKDIR /home/usuarioapp/src

# bin en PATH
ENV PATH="/home/usuarioapp/.local/bin:${PATH}"

# por si acaso no esta en requirements. memorion 2 veces al dia XD
RUN pip install gunicorn

# abierto puerto -- cambiar por otro puerto --
EXPOSE 5000
ENV PORT=5000

# argumentos y varibles de entorno para flask --  cambiar development/production . devolopment=hot reloads ----
# docker build -t dados:latest -t dados:v1 . --build-arg FLASK_ENV="development"
ARG FLASK_ENV="development"
ENV FLASK_ENV="${FLASK_ENV}" \
    FLASK_APP=main.py:app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# cmd o entrypoint ???
CMD [ "/bin/sh", "-c", "/home/usuarioapp/src/testing.sh" ]

# usumos gunicorn por tener hot reload sin necesitar de tener debug=true
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "main:app", "--reload"]