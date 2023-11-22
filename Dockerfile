FROM python:3.12.0-alpine3.18

ENV PYTHONBUFFERED=1

WORKDIR /taskmaster

# Instala las dependencias con Pipenv
RUN pip install pipenv

# Copia los archivos de Pipfile y Pipfile.lock para instalar dependencias
COPY Pipfile Pipfile.lock /taskmaster/

# Instala dependencias sin activar el entorno virtual
RUN pipenv install --deploy --system

# Copia todos los archivos a la imagen
COPY . .

EXPOSE 8000

# Ejecuta la aplicación
CMD python manage.py runserver 0.0.0.0:8000
