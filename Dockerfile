FROM python:3.9.12-slim
EXPOSE 8000
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./app /app/app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
