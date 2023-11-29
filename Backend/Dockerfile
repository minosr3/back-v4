FROM python:3.11-alpine

WORKDIR /app

COPY . /app/

# Actualiza pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# Instala las dependencias
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "src/app.py"]
