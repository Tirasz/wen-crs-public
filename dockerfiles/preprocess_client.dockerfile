FROM python:3.10.13-bookworm

WORKDIR /src
COPY ../src/preprocess /src
COPY ../src/config.json /src/configs

RUN python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN python -m pip install -r /src/requirements.txt

# Download sentence transformer stuff
RUN python init.py

# Apply cron job
RUN apt-get update
RUN apt-get install -y cron
RUN cp /src/cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob

CMD [ "bash", "-c", "python main.py", "cron -f" ]