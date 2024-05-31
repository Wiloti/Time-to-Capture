<h1 align="center">Time-to-Capture</h1>

## About

Time-to-Capture is a little Discord bot for CTF organization and information based on the CTFtime API.

## Features

- List the top 25 teams in the leaderboard from 2011 to today.
- List of CTF to come in the next 7 days.
- Set a Discord event as a reminder for a specific CTF.

## Prerequisites Setup
- python version >= 3.12.3

First you will need to register a bot on [Discord Dev page](https://discord.com/developers) developers platform.

Once created, on the **OAuth2** panel select *Bot* and add those permissions:

- Read Messages/View Channels
- Manage Events
- Create Events
- Send Messages
- Manage Messages
- Embed Links
- Use Slash Commands
- Use Embedded Activities

Copy the link provided and select the server you want.

The necessary **TOKEN** is located on The *bot* panel.

## Local installation

```
git clone https://github.com/Wiloti/Time-to-Capture
cd Time-to-Capture
pip install -r requirements.txt
mv .env.example .env
sed -i 's/TOKEN_BOT_HERE/<YOUR_TOKEN>/' .env
python bot.py
```

## Docker container

```
git clone https://github.com/Wiloti/Time-to-Capture
cd Time-to-Capture
mv .env.example .env
sed -i 's/TOKEN_BOT_HERE/<YOUR_TOKEN>/' .env
docker build --tag <NAME> .
docker run -d <NAME>:latest
```
