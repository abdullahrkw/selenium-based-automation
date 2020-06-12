FROM ubuntu:18.04
WORKDIR /workspace
RUN apt-get update &&\
    rm -rf /var/lib/apt/list/* 

RUN apt-get install -y software-properties-common &&\
    apt-get update &&\
    add-apt-repository ppa:ubuntu-mozilla-security/ppa

RUN apt-get install -y  wget net-tools python3-pip firefox sudo libcanberra-gtk-module

#installing geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz &&\
    tar -xvzf geckodriver* &&\
    chmod a+x ./geckodriver &&\
    mv ./geckodriver /usr/local/bin &&\
    rm geckodriver*
    
RUN pip3 install -U urllib3 selenium flask

CMD ["python3", "convo_automation.py"]

COPY . .
