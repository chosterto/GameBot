import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


client = commands.Bot(command_prefix="?")

client.remove_command("help")
client.load_extension("InfoCommands")
client.load_extension("GameCommands")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("A Lot of Games."))
    print("Logged on as {0.name}!".format(client.user))


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    client.run(TOKEN)
    