# Dockerfile

# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./ /code/

RUN apt-get update && apt-get -y install netcat && apt-get clean
# ENTRYPOINT ["/bin/nc"]