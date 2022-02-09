import json

from nextcord.ext import commands
from nextcord.ext.tasks import loop

from twitch import get_notifications

with open("config.json") as config_file:
    config = json.load(config_file)

bot = commands.Bot(command_prefix="$")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong")


@loop(seconds=90)
async def check_twitch_online_streamers():
    channel = bot.get_channel(config["channel_id"])
    if not channel:
        return

    notifications = get_notifications()
    for notification in notifications:
        await channel.send("Streamer {} is now online: {}".format(notification["user_login"], notification))

@bot.event
async def on_ready():
    print("Bot has connected to Discord.")


if __name__ == "__main__":  
    check_twitch_online_streamers.start()
    bot.run(config["discord_token"])

