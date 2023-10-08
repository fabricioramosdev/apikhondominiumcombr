# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim-buster

EXPOSE 8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

ENV POSTGRES_DB=d1fb8sqe119kh
ENV POSTGRES_USER=mcwwasjotdaxsd
ENV POSTGRES_PASSWORD=34d9d31e839892d4e6a56288a037785d731b0695958de690a67078b200c6eef0
ENV POSTGRES_HOST=ec2-44-194-4-127.compute-1.amazonaws.com
ENV POSTGRES_PORT=5432
ENV PORT=80


# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
RUN chmod -R 777 /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder: 'api'. Please enter the Python path to wsgi file.
CMD ["python3", "main.py"]
