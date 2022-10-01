from asyncio import tasks
import asyncio
from re import A

from turtle import title
from unittest.mock import NonCallableMagicMock
import discord
from discord.ext import commands, tasks
import json
from datetime import datetime
import os
import time
import pytz
from pytz import timezone

"""
Timetracker.py Created by Senya29_#7672
Created for Sons of Anarchy SPECIFICLY will not work for anything else
tbh only god and i know how this works lol

"""
class timetrackercopy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="start")
    async def _clockstart(self, ctx):
        # Clocking In Command
            try:
                with open(f"timecards/{ctx.author.id}timecard.json", "r") as f:
                    config = json.load(f)
                    f.close()
            except Exception as e:
                return await ctx.send("Your timecard does not exist do `!create`")
            
            with open(f"timecards/{ctx.author.id}timecard.json", "r") as g:
                config = json.load(g)
            
            ## Reformed Time Card Version
            start2 =  config["start"]
            start_time = time.time()
            if start2 == "empty":
                current_hours = config["current_hours"]
                data = {
                    "userid" : f"{ctx.author.id}",
                    "username" : f"{ctx.author.name}",
                    "current_hours" : f"{current_hours}",
                    "start" : f"{start_time}",
                    "end" : "empty"
                }
                g.close()
                try:
                    with open(f"timecards/{ctx.author.id}timecard.json", "w") as g:
                    
                        json.dump(data, g)
                        g.close()
                except Exception as e:
                    await ctx.send(f"A error has occured\n{e}")
            
                embed = discord.Embed(
                    color = discord.Color.green(),
                    title = "Reaper Hour Tracking",
                    description = f"You have started clocking.\nTime Punched in at: {start_time}"
                )
                embed.set_footer(text="Punched in time is in a diffrent format used by the system.\n")
                await ctx.reply(embed=embed)
                embed2 = discord.Embed(
                    color = discord.Color.green(),
                    title = f"{ctx.author.name} Has started clocking",
                    description = f"Information: \n> `*clock timecard view {ctx.author.id}` to view there timecard"
                )
                now_time = datetime.now(timezone('America/Chicago'))
                embed2.add_field(name="Time clocked in at:", value=f"**{now_time.strftime('%I:%M:%S %p')} CST**")
                channel2 = self.bot.get_channel(1014317432720064593)
                await channel2.send(embed=embed2)
            else:
                await ctx.send("you are already clocking do `*clock end` to stop")
        
    @commands.command(name="end")
    async def _clockend(self, ctx):
            # Clocking out Command
            try:
                with open(f"timecards/{ctx.author.id}timecard.json", "r") as f:
                    config = json.load(f)
                    f.close()
            except Exception as e:
                return await ctx.send("Your timecard does not exist do `!create`")
            
            with open(f"timecards/{ctx.author.id}timecard.json", "r") as g:
                config = json.load(g)
            
            start_time = config["start"]
            end_time = time.time()
            if start_time == "empty":
                await ctx.send("You have not started clocking do `!start` to start clocking")
            else:
                time_elapsed = end_time - float(start_time)
                timedone = time_convert(time_elapsed)
                embed = discord.Embed(
                    color = discord.Color.green(),
                    title = "Reaper Hour Tracking",
                    description = "Your hour tracking has ended to view your hours do `!view`"
                )
                embed.add_field(name="Time Clocked:", value=f"{timedone}")
                await ctx.reply(embed=embed)
                embed2 = discord.Embed(
                    color = discord.Color.green(),
                    title = f"{ctx.author.name} Has ended clocking",
                    description = f"Information: \n> `!view {ctx.author.id}` to view there timecard"
                )
                now_timecst = datetime.now(timezone('America/Chicago'))
                embed2.add_field(name="Time clocked out at:", value=f"**{now_timecst.strftime('%I:%M:%S %p')} CST**")
                embed2.add_field(name="Total Hours Clocked", value=f"{timedone}")
                current_hour = config["current_hours"]
                timeconverted = time_convert(int(float(current_hour)))
                embed2.add_field(name="Total Hours Before:", value=f"{timeconverted}")
                embed2.add_field(name="Total Hours Before Root:", value=f"{time_elapsed}")
                current_hours = float(current_hour) + time_elapsed
                timeconverted2 = time_convert(int(float(current_hours)))
                embed2.add_field(name="Total Hours After Root:", value=f"{current_hours}")
                embed2.add_field(name="Total Hours After:", value=f"{timeconverted2}")
                channel2 = self.bot.get_channel(1014317432720064593)
                await channel2.send(embed=embed2)
                

                g.close()
                # End discord side
                
                data = {
                "userid" : f"{ctx.author.id}",
                "username" : f"{ctx.author.name}",
                "current_hours" : f"{current_hours}",
                "start" : "empty",
                "end" : "empty"
                }
                try:
                    with open(f"timecards/{ctx.author.id}timecard.json", "w") as f:
                        json.dump(data, f)
                        f.close()
                except Exception as e:
                    print("Error: " + e)
    
    @commands.command(
        name="create"
    )
    async def _create(self, ctx):
        if discord.utils.get(ctx.author.roles, name="S.A.M.C.R.O") is not None:
                    try:
                        with open(f"timecards/{ctx.author.id}timecard.json", "r") as f:
                            config = json.load(f)
                            f.close()
                            return await ctx.send("Your time card already exists")

                    except Exception as e:
                        await ctx.send("Creating Timecard")
                    data = {
                        "userid" : f"{ctx.author.id}",
                        "username" : f"{ctx.author.name}",
                        "current_hours" : "0",
                        "start" : "empty",
                        "end" : "empty"

                    }
                    
                    try:
                        with open(f"timecards/{ctx.author.id}timecard.json", 'w') as f:
                            json.dump(data, f)
                    except Exception as e:
                        await ctx.send(e)
                    await ctx.send("Timecard created do `!view` to view Timecard stats")
        else:
                    await ctx.send("You are not a member of this club.")
            

                
   

    @commands.command(
        name="reset"
    )
    async def _reset(self, ctx):
        if discord.utils.get(ctx.author.roles, name="Senior Table Members") is not None:
                    await ctx.send("Please respond with a user id, these are used to identify the timecards\n\nRepsond with **no** to cancel")
                    
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    msg = await self.bot.wait_for("message", check=check)
                    if msg.content == "no":
                        return await ctx.send("canceling")
                    else:
                        try:
                            
                            with open(f"timecards/{msg.content}timecard.json", "r") as f:
                                config = json.load(f)
                                f.close()
                        except Exception as e:
                            return await ctx.send("This persons timecard does not exist.")
                        try:
                            with open(f"timecards/{msg.content}timecard.json", "r") as f:
                                config = json.load(f)
                                
                            
                        except Exception as e:
                            return await ctx.send(f"Failed to reset Timecard. \nERROR: {e}")
                        
                        userid = config["userid"]
                        username = config["username"]
                        hours = 0
                        data = {
                            "userid" : f"{userid}",
                            "username" : f"{username}",
                            "current_hours" : f"0",
                            "start" : "empty",
                            "end" : "empty",
                        }
                        f.close()
                        try:
                            with open(f"timecards/{msg.content}timecard.json", "w") as f:
                                json.dump(data, f)
                                
                            
                        except Exception as e:
                            return await ctx.send(f"Failed to reset Timecard. \nERROR: {e}")
                        embed = discord.Embed(
                            color = discord.Color.green(), 
                            title = "Timecard Reset Complete",
                            description = f"{username}'s Timecard hours has been reset. to view there timecard do this command `*clock timecard view {userid}` "
                        )
                        embed.set_footer(text="Reaper Timetracker System")
                        await ctx.send(embed=embed)
        else:
                    await ctx.send("You are not a Senior Table Member")

    @commands.Cog.listener(name="on_member_leave")
    async def _leave(self, member):
        # attempts to open timecard
        try: 
            with open(f"timecards/{member.id}timecard.json", "r") as f:
                f.close()
        except Exception as e:
            errorchannel = self.bot.get_channel(1013327285685858364)
            return await errorchannel.send(f"could not find {member.id} in the timecard folder")
        os.remove(f"timecards/{member.id}timecard.json")
        await errorchannel.send(f"{member.name} timecard has been removed due to leaving the discord")


                
     
        
    @commands.command(
        name="view"
    )
    async def _view(self, ctx, sub3=None):
        if sub3 is None:
                    await ctx.send("Getting timecard Data")
                    try:
                        with open(f"timecards/{ctx.author.id}timecard.json", "r") as f:
                            config = json.load(f)
                            f.close()
                    except Exception as e:
                        return await ctx.send("Your timecard does not exist do `!create`")
                    with open(f"timecards/{ctx.author.id}timecard.json", "r") as f:
                            config = json.load(f)
                    userid =config["userid"]
                    username = config["username"]
                    current_hour = config["current_hours"]
                    current_hours = time_convert(float(current_hour))
                    embed = discord.Embed(
                        color = discord.Color.green(),
                        title = f"{username}'s Time Card",
                        description="Timecard for Sons of Anarchy Motorcycle Club"

                    )
                    embed.add_field(name="***Members User Id:***", value=f"{userid}")
                    embed.add_field(name="***Members User Name:***", value=f"{username}")
                    embed.add_field(name="***Members Current Hours:***", value=f"{current_hours}", inline=False)
                    embed.set_footer(text="Please note that the hour system is not finalized, and could give a false reading.")
                    f.close()
                    return await ctx.reply(embed=embed)
        else:
                  
                    await ctx.send("Getting timecard Data")
                    try:
                        with open(f"timecards/{sub3}timecard.json", "r") as f:
                            config = json.load(f)
                            f.close()
                    except Exception as e:
                        return await ctx.send("This persons timecard does not exist tell them to do `!create` or you entered the wrong ID please use there USER ID")
                    with open(f"timecards/{sub3}timecard.json", "r") as f:
                            config = json.load(f)
                    userid =config["userid"]
                    username = config["username"]
                    current_hour = config["current_hours"]
                    current_hours = time_convert(float(current_hour))
                    embed = discord.Embed(
                        color = discord.Color.green(),
                        title = f"{username}'s Time Card",
                        description="Timecard for Sons of Anarchy Motorcycle Club"

                    )
                    
                    embed.add_field(name="***Members User Id:***", value=f"{userid}")
                    embed.add_field(name="***Members User Name:***", value=f"{username}")
                    embed.add_field(name="***Members Current Hours:***", value=f"{current_hours}", inline=False)
                    embed.set_footer(text="Please note that the hour system is not finalized, and could give a false reading.")
                    f.close()
                    return await ctx.reply(embed=embed)
    @commands.command(
        name="edit"
    )
    async def _edit(self, ctx, userid: discord.Member=None, hourstoedit=None):
      if discord.utils.get(ctx.author.roles, name="Senior Table Members") is not None:
        message = """This Edits the Hours COMPLETLY\nExample:\n> `!edit <@500422519904272404> 52` This sets there hours at 52 Hours and 0 Seconds\nFor more info do `!editexplain`"""
        embed = discord.Embed(title="Hour Edit System", description=message)
        if userid is None:
            await ctx.send(embed=embed)
            return await ctx.send("Please @ or provide a valid userid")
        try:
                        with open(f"timecards/{userid.id}timecard.json", "r") as f:
                            config = json.load(f)
                            f.close()
        except Exception as e:
                        return await ctx.send(f"<@{userid.id}>'s timecard does not exist do `!create`")
        onehour = 3600
        if hourstoedit is None:
            await ctx.send(embed=embed)
            return await ctx.send("Please provide the amount of hours to set it to like 2 or 3 hours")

        timetoset = onehour * int(hourstoedit)
        config
        useridtwo = config["userid"]
        username = config["username"]
        start = config["start"]
        end = config["end"]
        hours = 0
        data = {
            "userid" : f"{useridtwo}",
            "username" : f"{username}",
            "current_hours" : f"{timetoset}",
            "start" : f"{start}",
            "end" : f"{end}",
        }
        try:
                        with open(f"timecards/{userid.id}timecard.json", "w") as f:
                            json.dump(data, f)
                            f.close()
        except Exception as e:
                        return await ctx.send(f"Error Could not dump data")
        await ctx.send(f"Hours Set to {time_convert(timetoset)}")
      else:
       if userid is None:
        message = """This Edits the Hours COMPLETLY\nExample:\n> `!edit <@500422519904272404> 52` This sets there hours at 52 Hours and 0 Seconds\nFor more info do `!editexplain`"""
        embed = discord.Embed(title="Hour Edit System", description=message)
        await ctx.send(embed=embed)
        return await ctx.send("Please @ or provide a valid userid")
       else:
        if str(ctx.author.id) == "500422519904272404":
            message = """This Edits the Hours COMPLETLY\nExample:\n> `!edit <@500422519904272404> 52` This sets there hours at 52 Hours and 0 Seconds\nFor more info do `!editexplain`"""
            embed = discord.Embed(title="Hour Edit System", description=message)
            if userid is None:
                await ctx.send(embed=embed)
                return await ctx.send("Please @ or provide a valid userid")
            try:
                        with open(f"timecards/{userid.id}timecard.json", "r") as f:
                            config = json.load(f)
                            f.close()
            except Exception as e:
                        return await ctx.send(f"<@{userid.id}>'s timecard does not exist do `!create`")
            onehour = 3600
            if hourstoedit is None:
                await ctx.send(embed=embed)
                return await ctx.send("Please provide the amount of hours to set it to like 2 or 3 hours")

            timetoset = onehour * int(hourstoedit)
            config
            useridtwo = config["userid"]
            username = config["username"]
            start = config["start"]
            end = config["end"]
            hours = 0
            data = {
                "userid" : f"{useridtwo}",
                "username" : f"{username}",
                "current_hours" : f"{timetoset}",
                "start" : f"{start}",
                "end" : f"{end}",
            }
            try:
                        with open(f"timecards/{userid.id}timecard.json", "w") as f:
                            json.dump(data, f)
                            f.close()
            except Exception as e:
                        return await ctx.send(f"Error Could not dump data")
            await ctx.send(f"Hours Set to {time_convert(timetoset)}") 
        else:
                return await ctx.send("You can not use this command")


        

                

      
                


                

def time_convert(sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        ts = "**{0}** HOURS: ***{1}*** MINUTES: *{2}* SECONDS".format(int(hours),int(mins), int(sec))
        return ts

async def edit2(self, ctx, userid: discord.Member=None, hourstoedit=None):
        message = """This Edits the Hours COMPLETLY\nExample:\n> `!edit <@500422519904272404> 52` This sets there hours at 52 Hours and 0 Seconds\nFor more info do `!editexplain`"""
        embed = discord.Embed(title="Hour Edit System", description=message)
        if userid is None:
            await ctx.send(embed=embed)
            return await ctx.send("Please @ or provide a valid userid")
        try:
                        with open(f"timecards/{userid.id}timecard.json", "r") as f:
                            config = json.load(f)
                            f.close()
        except Exception as e:
                        return await ctx.send(f"<@{userid.id}>'s timecard does not exist do `!create`")
        onehour = 3600
        if hourstoedit is None:
            await ctx.send(embed=embed)
            return await ctx.send("Please provide the amount of hours to set it to like 2 or 3 hours")

        timetoset = onehour * int(hourstoedit)
        config
        useridtwo = config["userid"]
        username = config["username"]
        start = config["start"]
        end = config["end"]
        hours = 0
        data = {
            "userid" : f"{useridtwo}",
            "username" : f"{username}",
            "current_hours" : f"{timetoset}",
            "start" : f"{start}",
            "end" : f"{end}",
        }
        try:
                        with open(f"timecards/{userid.id}timecard.json", "w") as f:
                            json.dump(data, f)
                            f.close()
        except Exception as e:
                        return await ctx.send(f"Error Could not dump data")
        await ctx.send(f"Hours Set to {time_convert(timetoset)}")

async def setup(bot): 
    await bot.add_cog(timetrackercopy(bot)) 