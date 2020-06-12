FROM ubuntu:18.04
RUN apt-get update &&\
    rm -rf /var/lib/apt/list/* 

RUN apt-get install -y software-properties-common &&\
    apt-get update &&\
    add-apt-repository ppa:ubuntu-mozilla-security/ppa

RUN apt-get install -y  wget net-tools python3-pip firefox sudo libcanberra-gtk-module
# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

#installing geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz &&\
    tar -xvzf geckodriver* &&\
    chmod a+x ./geckodriver &&\
    mv ./geckodriver /usr/local/bin &&\
    rm geckodriver*
    
RUN pip3 install -U urllib3 selenium flask

USER developer
ENV HOME /home/developer
