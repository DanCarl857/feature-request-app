FROM python:2.7
WORKDIR /app
ADD . /app

#Environment
RUN apt-get update
RUN apt-get install -y ruby

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make Entrypoint executable
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 5000

CMD [ "/bin/bash", "/app/docker-entrypoint.sh" ]