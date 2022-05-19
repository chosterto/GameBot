import discord
import asyncio
from discord.ext import commands
from random import random
import helpers


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = False


    @commands.command()
    async def rps(self, ctx):
        if self.active:
            return
        self.active = True

        user = helpers.RPS()
        bot = helpers.RPS()

        await ctx.channel.send("Rock :rock:, Paper :newspaper:, or Scissors :scissors:?\n\nType rock, paper, or scissors to select one.")
        response = await self.bot.wait_for(
            "message", 
            check=lambda msg: msg.content in ("rock", "paper", "scissors")
            and msg.channel == ctx.channel 
            and msg.author == ctx.author
        )
        
        user.choose_shape(response.content)
        bot.choose_random_shape()

        await ctx.channel.send("You chose " + user.shape() + " and I chose " + bot.shape())

        if user.is_same_as(bot):
            await ctx.channel.send("Tied! :joy::ok_hand:")
        elif user.is_winner(bot):
            await ctx.channel.send("You won! :smiley:")
        else:
            await ctx.channel.send("You lost! Better luck next time... :smiling_imp:")

        self.active = False


    @commands.command()
    async def coinflip(self, ctx):
        if self.active:
            return
        self.active = True

        await ctx.channel.send("Heads or Tails?")
        side = await self.bot.wait_for(
            "message", 
            check=lambda msg: msg.content.lower() in ("heads", "tails")
            and msg.channel == ctx.channel
            and msg.author == ctx.author
        )
        side = side.content.lower()
        
        if random() > 0.5:
            has_won = "Good guess!" if side == "heads" else "You guessed wrong!"
            await ctx.channel.send(":coin: It's Heads! " + has_won)
        else:
            has_won = "Good guess!" if side == "tails" else "You guessed wrong!"
            await ctx.channel.send(":coin: It's Tails! " + has_won)

        self.active = False


    @commands.command()
    async def ttt(self, ctx):
        if self.active:
            return
        self.active = True

        ttt = helpers.TicTacToe()

        await ctx.channel.send("Select a difficulty: easy or hard.")
        difficulty = await self.bot.wait_for(
            "message", 
            check=lambda msg: msg.content in ("easy", "hard")
            and msg.channel == ctx.channel 
            and msg.author == ctx.author
        )
        bot_select_space = ttt.bot_random if difficulty.content == "easy" else ttt.bot_smart

        bot_goes_first = random() > 0.5
        if bot_goes_first:
            ttt.bot_random()
        await ctx.channel.send("I go first." if bot_goes_first else "You go first.")
        board = await ctx.channel.send(ttt.display())

        while not ttt.is_finished():
            space = await self.bot.wait_for(
                "message", 
                check=lambda msg: msg.content in list(map(str, [*range(1, 10)]))
                and msg.channel == ctx.channel
                and msg.author == ctx.author
            )
            await space.delete()
            space = int(space.content)
            if ttt.is_space_unoccupied(space):
                ttt.mark_space(space)
            else:
                await ctx.channel.send("Space {0} is occupied.".format(space))
                continue
            await board.edit(content=ttt.display())
            # Check again if the game is finished
            if ttt.is_finished():
                break
            bot_select_space()
            await asyncio.sleep(1)
            await board.edit(content=ttt.display())
        
        if ttt.winner:
            await ctx.channel.send("Game is done. The winner is... " + ttt.winner)
        else:
            await ctx.channel.send("It's a draw! Nobody wins...")
        # await asyncio.sleep(2)
        # await board.delete()

        self.active = False


    @commands.command()
    async def maze(self, ctx):
        if self.active:
            return
        self.active = True

        maze = helpers.Maze()

        maze.generate_maze()

        maze.initialize_pos()

        board = await ctx.channel.send(maze.display_hidden())

        prompt = await ctx.channel.send(
            embed=discord.Embed(
                title="The Maze Game",
                description=""":arrow_up: — Go up.\n
                :arrow_down: — Go down.\n
                :arrow_left: — Go left.\n
                :arrow_right: — Go right.\n
                :stop_button: — Stop the game."""
            )
        )
        await prompt.add_reaction("⬆️")
        await prompt.add_reaction("⬇️")
        await prompt.add_reaction("⬅️")
        await prompt.add_reaction("➡️")
        await prompt.add_reaction("⏹️")

        while not maze.is_end_reached():
            reaction, _ = await self.bot.wait_for(
                "reaction_add", 
                check=lambda react, user: str(react.emoji) in ("⬆️", "⬇️", "⬅️", "➡️", "⏹️")
                and user == ctx.author 
            )
            emote = str(reaction)
            
            if emote == "⏹️":
                break

            maze.move_player(emote)

            if maze.is_flag_reached():
                maze.remove_barrier()

            await board.edit(content=maze.display_hidden())
        
        await board.edit(content=maze.display_unhidden())
        await ctx.channel.send(embed=discord.Embed(title="Game is finished. Type ?maze to play again!"))
        # await asyncio.sleep(2)
        # await board.delete()
        # await prompt.delete()
        
        self.active = False
    
    
    @commands.command()
    async def cups(self, ctx):
        if self.active:
            return
        self.active = True

        cupball = helpers.Cupball()

        cups = await ctx.channel.send(cupball.display())
        await asyncio.sleep(1.5)
        cupball.hide_balls()
        await cups.edit(content=cupball.display())

        while not cupball.is_swapping_done():
            await asyncio.sleep(1)
            cupball.select_cups()
            await cups.edit(content=cupball.display())
            await asyncio.sleep(0.75)
            cupball.swap_cup1()
            await cups.edit(content=cupball.display())
            await asyncio.sleep(0.75)
            cupball.swap_cup2()
            await cups.edit(content=cupball.display())
            await asyncio.sleep(0.75)
            cupball.place_cups()
            await cups.edit(content=cupball.display())
        
        await ctx.channel.send(
            embed=discord.Embed(
                title="Which cup contains the green ball?",
                description="Type '1' for the left cup, '2' for the middle cup, or '3' for the right cup"
            )
        )
        user_cup = await self.bot.wait_for(
            "message", 
            check=lambda msg: msg.content in ('1', '2', '3')
            and msg.channel == ctx.channel
            and msg.author == ctx.author
        )
        cupball.reveal_balls()
        await cups.edit(content=cupball.display())

        if cupball.has_green_ball(int(user_cup.content)):
            await ctx.channel.send("Correct! :smile:")
        else:
            await ctx.channel.send("Wrong ball! :x:")

        self.active = False


def setup(bot):
    bot.add_cog(Games(bot))
