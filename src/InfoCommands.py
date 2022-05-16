import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def help(self, ctx, command=""):
        command_info = {
            "ping": "Pings the user who invoked the command.",
            "rps": "Rock, paper, scissors game.",
            "coinflip": "A game of heads or tails.",
            "ttt": "A game of Tic-Tac-Toe. To understand how to play the game, refer to the number chart below:\n:black_large_square::red_square::black_large_square::red_square::black_large_square:   —>   1 ... 2 ... 3\n:red_square::red_square::red_square::red_square::red_square:\n:black_large_square::red_square::black_large_square::red_square::black_large_square:   —>   4 ... 5 ... 6\n:red_square::red_square::red_square::red_square::red_square:\n:black_large_square::red_square::black_large_square::red_square::black_large_square:   —>   7 ... 8 ... 9\nEach number corresponds to a space on the board.\nType one of the given numbers to mark an unoccupied space.",
            "maze": "A 2D maze game with friendly UI. You must first obtain the flag (🚩) before escaping!"
            }
        if command:
            try:
                custom_help = discord.Embed(title=command, description=command_info[command])
                await ctx.channel.send(embed=custom_help)
            except KeyError:
                await ctx.channel.send(embed=discord.Embed(description=":x: Command does not exist."))
            finally:
                return
        help_msg = discord.Embed(title="help", description="Displays this message. Use ?help <command> for more info.")
        help_msg.add_field(name="List of Game Commands:", value="ping\ncoinflip\nrps\nttt\nmaze")
        await ctx.channel.send(embed=help_msg)


    @commands.command()
    async def ping(self, ctx):
        time = round(self.bot.latency, 2)
        invoker = ctx.author.mention
        await ctx.channel.send("Pong! Your message took {0} seconds to reach {1}".format(time, invoker))


def setup(bot):
    bot.add_cog(Info(bot))
