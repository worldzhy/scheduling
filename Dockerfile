# Deriving the latest base image
FROM python:latest

# Working directory
WORKDIR /usr/src/app

# COPY the remote file at working directory in container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# CMD instruction should be used to run the software
CMD [ "python", "./server.py"]