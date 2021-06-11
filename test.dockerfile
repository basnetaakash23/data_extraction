# syntax=docker/dockerfile:1

FROM python:3.9.5-buster

WORKDIR /Users/aakashbasnet/Documents/eplrestapi/
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apt-get update -y && apt-get install -y \
  curl \
  unzip \
  libglib2.0 \libnss3 \
  libnss3 \
  libxcb1



# RUN curl https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip -o chromedriver_linux64.zip


# RUN unzip chromedriver_linux64.zip
# RUN chmod +x chromedriver
# RUN mkdir linux
# RUN mv chromedriver linux/

# ENV PATH /linux/chromedriver:$PATH

COPY . .

CMD [ "python3", "epl.py"]

