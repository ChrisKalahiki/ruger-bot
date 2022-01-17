FROM python:3

WORKDIR /ruger-bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /ruger-bot/src

CMD [ "python", "bot.py" ]