# Deriving the latest base image
FROM --platform=linux/arm64/v8 python:3.12.0-slim-bullseye

# Working directory
WORKDIR /usr/src/app

# Update
RUN apt update

# Environment variables
ENV APP_DEBUG=True

# COPY the remote file at working directory in container
COPY . .

# Install any needed packages specified in requirements.txt
RUN python -m pip cache purge
RUN pip install -r requirements.txt --timeout 2000 --no-cache-dir

# CMD instruction should be used to run the software
EXPOSE 8080
CMD [ "python", "./server.py"]