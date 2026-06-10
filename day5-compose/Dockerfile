FROM python:3.14-slim
WORKDIR /app
RUN pip install psycopg2-binary
COPY day5-db.py .
CMD ["python", "day5-db.py"]

