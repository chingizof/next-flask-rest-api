FROM python:3.6-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

#copy everything from docker image
COPY . . 

#expose port 4000
EXPOSE 4000

#0.0.0.0 is a current host machine
CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
