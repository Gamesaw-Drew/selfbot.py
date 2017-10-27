import discord
from discord.ext import commands
from ext.utility import parse_equation
from ext.colours import ColorNames
from urllib.request import urlopen
from sympy import solve
from PIL import Image
import asyncio
import random
import emoji
import copy
import io
import aiohttp
import json
import os
import traceback


class New:
    def __init__(self, bot):
        self.bot = bot
			
    @commands.command(pass_context=True, aliases=['pick'])
    async def choose(self, ctx, *, choices: str):
        """Choose randomly from the options you give. [p]choose this | that"""
        await ctx.send(
                       self.bot.bot_prefix + 'I choose: ``{}``'.format(random.choice(choices.split("|"))))
		
    @commands.group(pass_context=True, invoke_without_command=True)
    async def ascii(self, ctx, *, msg):
        """Convert text to ascii art. Ex: ascii stuff help ascii for more info."""
        if ctx.invoked_subcommand is None:
            if msg:
                font = get_config_value("optional_config", "ascii_font")
                msg = str(figlet_format(msg.strip(), font=font))
                if len(msg) > 2000:
                    await ctx.send(self.bot.bot_prefix + 'no fuck off')
                else:
                    await ctx.message.delete()
                    await ctx.send(self.bot.bot_prefix + '```\n{}\n```'.format(msg))
            else:
                await ctx.send(self.bot.bot_prefix + "put in text noob")

    @commands.command(pass_context=True)
    async def textflip(self, ctx, *, msg):
        """Flip given text."""
        result = ""
        for char in msg:
            if char in self.text_flip:
                result += self.text_flip[char]
            else:
                result += char
        await ctx.message.edit(content=result[::-1])  # slice reverses the string

    @commands.command(pass_context=True)
    async def regional(self, ctx, *, msg):
        """Replace letters with regional indicator emojis"""
        await ctx.message.delete()
        msg = list(msg)
        regional_list = [self.regionals[x.lower()] if x.isalnum() or x in ["!", "?"] else x for x in msg]
        regional_output = '\u200b'.join(regional_list)
        await ctx.send(regional_output)
        
    @commands.command(pass_context=True)
    async def heil(self):
        try:
            await self.bot.say("卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐")
        except:
            await self.bot.say(str("```" + traceback.format_exc() + "```"))
            
    @commands.command(pass_context=True, no_pm=False)
    async def stab(self, ctx):
        try:
            if len(ctx.message.mentions) > 1:
                await self.bot.say("You can only stab one person at a time " + ctx.message.author.mention + "!")
                pass
            elif len(ctx.message.mentions) == 0:
                await self.bot.say("`usage: !stab <user>`")
                pass
            else:
                if ctx.message.mentions[0] == ctx.message.author:
                    await self.bot.send_message(ctx.message.channel, ':knife: ' + ctx.message.author.mention + ' commited suicide')
                else:
                    await self.bot.send_message(ctx.message.channel, '#getstabbed ' + ctx.message.mentions[0].mention + ' :knife:')
        except:
            await self.bot.say(str("```" + traceback.format_exc() + "```"))
            
    @commands.command(pass_context=True, no_pm=False)
    async def shoot(self, ctx):
        try:
            if len(ctx.message.mentions) > 1:
                await self.bot.say("You can only police brutality one person at a time " + ctx.message.author.mention + "!")
                pass
            elif len(ctx.message.mentions) == 0:
                await self.bot.say("`usage: !shoot <user>`")
                pass
            else:
                if ctx.message.mentions[0] == ctx.message.author:
                    await self.bot.send_message(ctx.message.channel, ':gun: ' + ctx.message.author.mention + '\'s gun jammed! UH OH!!!!')
                else:
                    await self.bot.send_message(ctx.message.channel, 'Preparing to shoot ' + ctx.message.mentions[0].mention + '...')
                    await asyncio.sleep(2)
                    await self.bot.send_message(ctx.message.channel, ctx.message.mentions[0].mention + ' :gun: UH OH! THE GUN JAMMED! UH OH! UH OH!')
        except:
            await self.bot.say(str("```" + traceback.format_exc() + "```"))
            
    @commands.command(pass_context=True, no_pm=False)
    async def bomb(self, ctx):
        try:
            if len(ctx.message.mentions) > 1:
                await self.bot.say("You can only isis one person at a time " + ctx.message.author.mention + "!")
                pass
            elif len(ctx.message.mentions) == 0:
                await self.bot.say("`usage: !bomb <user>`")
                pass
            else:
                if ctx.message.mentions[0] == ctx.message.author:
                    await self.bot.send_message(ctx.message.channel, ':man_with_turban::skin-tone-5: :bomb: ' + ctx.message.author.mention + ' jihaded them\'re selves to death')
                else:
                    await self.bot.send_message(ctx.message.channel, 'Transforming ' + ctx.message.mentions[0].mention + ' into a school and then bombing it...\n:man_with_turban::skin-tone-5: :school: :bomb: *allahu akbar*')
        except:
            await self.bot.say(str("```" + traceback.format_exc() + "```"))
            
    @commands.command(pass_context=True, no_pm=False)
    async def robloxavatar(self, ctx, roblobabeUserName):
        getId = requests.get("https://api.roblox.com/users/get-by-username?username=" + roblobabeUserName)
        idJson = getId.json()
        userId = idJson['Id']
        
        avatarImage = requests.get("http://www.roblox.com/bust-thumbnail/json?userId="+ str(userId) +"&height=180&width=180")
        avImg = avatarImage.json()
        await self.bot.send_message(ctx.message.channel, avImg['Url'])
        
    @commands.command(pass_context=True, no_pm=False)
    async def minecraftavatar(self, ctx, minecraftUsername):
        await self.bot.send_message(ctx.message.channel, "https://mcapi.ca/skin/2d/" + minecraftUsername + "/85/true")
        
    @commands.command(pass_context=True, no_pm=False)
    async def minecraftserver(self, ctx, serverAddress):
        await self.bot.say("Getting server data, it may take a bit, and sometimes it may not work...")
        getStatus = requests.get("https://mcapi.ca/query/" + serverAddress + "/info")
        getPlayerList = requests.get("https://mcapi.ca/query/" + serverAddress + "/list")
        players = getPlayerList.json()
        status = getStatus.json()
        await self.bot.send_message(ctx.message.channel, "```MOTD: " + status['motd'] + "\nPlayers: " + str(status['players']['online']) + "/" + str(status['players']['max']) + "\nPlayers List: " + str(players['Players']['list']) + "```")

def setup(bot):
    bot.add_cog(New(bot))