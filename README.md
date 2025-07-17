# ORACLE

## What is Oracle?

#### Oracle is a discord bot that allows people to play akinator on discord but with a twist. The bot askes questions about the users in the server!!! 

## Commands and features 

#### /enroll - enroll for the bot. This command askes you questions about yourself so that the bot can guess you 
#### /forgetme - this command allows you to delete all of your data but this will make you not guessable by the bot
#### /guess - this starts the main game where the bot asks you questions and tries to guess the person you are thinking about
#### /ping - checks if the server is up by returning "pong!"

## Tech Stack
#### python
#### postgres

## Runing the bot yourself 
First you need to make a .env file with the following 
``` env
DC_TOKEN # discord bot token
DB_User # username of postgres user who has acsess to the db
DB_User_PASS # password of the postgres user who has acsess to the db
```
you might also need to also need to change the line 23 in utils.py to change the name of the db, host, or port

After that you can do the following to run the discord bot
``` bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
