# set base image (host OS)
FROM python:3.8-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH "/home/app/.local/bin:${PATH}"

# set the working directory in the container
WORKDIR /home/app

# copy local files to app directory, includes requirements.txt
COPY . .

# install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "python", "run.py"]
