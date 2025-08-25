FROM python:3.12-slim
WORKDIR /app


COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt


# Copy the model to a consistent location
COPY model_artifacts ./model_artifacts

RUN pip install --no-cache-dir -r ./model_artifacts/requirements.txt


# Copy the app code
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]