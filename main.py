# Got bored
import discord
from discord.ext import commands

intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
bot = commands.Bot(command_prefix="!", intents=intents, activity=activity ,help_command=None,)

@bot.listen("on_ready")
async def readyed():
    print(f"""
    Reaper Bot for Sons of Anarchy
    Created By: Senya29_
    Version: 1.0
    Bot Name: {bot.user}
    Python Version: 3
    DISCORD.PY V2.0
    """)
    print("Loading Timetracker System")
    try:
        await bot.load_extension("timetracker")
    except Exception as e:
        print(f"A error has occured while loading Timetracker System.\n\n{e}")
    
    

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        color = discord.Color.green(),
        title = "Reaper Help Menu",
        description = "This is the help menu for the non-redbot version of the Reaper including the Timetracker system!!"
    )
    embed.add_field(name="**Timetracker System:**", value=f"""
    `!start` Start Clock
    `!end` End Clocking
    `!view` View yours or others time cards
    `!reset` Reset a members hours
    """)
    await ctx.author.send(embed=embed)
    await ctx.reply("You got Mail!")


bot.run("Enter What Ever Bot Token Right Fuckin Here")