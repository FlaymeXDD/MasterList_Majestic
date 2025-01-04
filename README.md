# Majestic Masterlist Discord Bot

This bot retrieves and displays a list of game servers from the Majestic Masterlist API. It aggregates server information and sends periodic updates to a specified Discord channel.
Features

    Displays the number of players on each server.
    Periodically updates the server status in the configured Discord channel.

Prerequisites

Before running this bot, ensure you have the following dependencies installed:

    Python 3.6 or higher
    requests
    discord.py
    python-dotenv

You can install the required Python packages using the following:

    pip install requests discord.py python-dotenv

Configuration
**Create a .env File**

You need to create a .env file in your project directory to store sensitive information like the bot token and the channel ID.

Here's an example of how your .env file should look:

TOKEN=your_discord_bot_token
CHANNEL_ID=your_discord_channel_id

    Replace your_discord_bot_token with the token for your bot, which you can get from the Discord Developer Portal.
    Replace your_discord_channel_id with the ID of the Discord channel where you want the bot to send updates.

