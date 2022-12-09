FROM python:3.11-slim

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
