# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim-buster

EXPOSE 8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

ENV POSTGRES_DB=d1f77p8c2b8ppv
ENV POSTGRES_USER=tvyjxoryioyven
ENV POSTGRES_PASSWORD=ecc0a6540844dd12a252d9342429675f35618aeeadac57c5818e751f2acfe163
ENV POSTGRES_HOST=ec2-3-210-173-88.compute-1.amazonaws.com
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
