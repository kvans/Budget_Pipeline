FROM python:3.10

RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime

WORKDIR /app

RUN touch /var/log/script.log


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/main.py scripts/transactions.py config.json /app/

# Need this docker container to stay up so that I can schedule it to run once a day with Ofelia. 
# Thats why I used the tail command.
CMD tail -f /var/log/script.log