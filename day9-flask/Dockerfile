FROM python:3.12-slim

# Create a dedicated non-root user and group
RUN groupadd --gid 10001 appgroup && \
    useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Give the non-root user ownership of the app file
COPY --chown=10001:10001 day9-flask/app.py .

# Switch to the non-root user
USER 10001:10001

EXPOSE 5000

CMD ["python", "app.py"]