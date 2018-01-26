FROM python:3

WORKDIR /tmp

# Install Masscan

RUN apt-get update && apt-get install -y git gcc make libpcap-dev clang

RUN git clone https://github.com/robertdavidgraham/masscan

RUN cd masscan && make

# Install Nmap

RUN wget https://nmap.org/dist/nmap-7.60.tar.bz2

RUN tar -jxvf nmap-7.60.tar.bz2

RUN cd nmap-7.60 && ./configure && make && make install

# Install Scanner python requirements

RUN mkdir /tmp/Scanner

WORKDIR /tmp/Scanner

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
