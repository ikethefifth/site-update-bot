# site-update-bot
Discord bot to check for updates to static HTML pages

## What you'll need
### The code
Clone the repository, or just download main.py
### Libraries
You'll need to install the requests, dotenv, and discord libraries. You might want to make a [virtual environment](https://pypi.org/project/pipenv/) first. Then do "pip install requests", "pip install python-dotenv", and "pip install discord".
### Discord account
If you don't already have one, you can get an account [here](https://discord.com)
### Discord developer tools
Go [here](https://discordapp.com/developers/applications/) and make a new application. Write down the client ID and secret.Then make a bot within the application, write down the token
### Env File
Make a file called ".env" in the same folder as main.py, and paste in "DISCORD_TOKEN=[your token here]"
## Running the Bot
Run main.py - you might be able to double click, if that doesn't work open a terminal and type "python3 main.py"
## Using the Bot
### !ping
Make sure the bot is online
### !addsite [url here]
This will add the url to your list of tracked websites
### !rmvsite [url here]
Stop tracking the website
### !siteupdate
Check your list of sites for updates
