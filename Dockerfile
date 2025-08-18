FROM python:3.13.2

WORKDIR /code

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY app ./app

CMD ["fastapi", "run", "./app/main.py", "--port", "80"]