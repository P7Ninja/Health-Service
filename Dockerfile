FROM python:3.10-alpine

WORKDIR /application

COPY requirements.txt /application/

RUN pip install --no-cache-dir -r requirements.txt

COPY /src/healthservice /application/healthservice
COPY /app/server.py /application/server.py


CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7003", "--root-path", "/recipeservice"]