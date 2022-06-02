FROM ubuntu:20.04

RUN apt-get update && apt-get install -y firefox wget

RUN apt update \
	&& apt install -y python3 pip \
	&& cd /usr/bin \
	&& ln -s python3 python
# ADD ./BET_BOT /mnt/data 
COPY requirements.txt /mnt/data/requirements.txt
WORKDIR /mnt/data 
ADD start.sh /
RUN chmod +x /start.sh


RUN pip install -r requirements.txt
COPY . /mnt/data/




CMD ["/start.sh"]

# CMD ["python", "-m", "http.server", "-d", "/mnt/", "80"]
