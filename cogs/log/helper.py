from __future__ import annotations
from core.bot import Bot
from typing import Any, Optional , Callable , Literal , Union
from datetime import timedelta , datetime
from cogs.cog_config import Plugin
from discord.ext import commands
from humanfriendly import parse_timespan , InvalidTimespan
from discord import app_commands , User , utils as Utils , CategoryChannel , ForumChannel , PartialMessageable , Object , TextChannel , Thread , Permissions , StageChannel , VoiceChannel , Role , Attachment , Forbidden , Color
from pytz import UTC
from aiohttp import ClientSession
import aiohttp
import discord
import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from easy_pil import Editor , Canvas, load_image_async , Font
from config import TOKEN
import requests
from typing import Union 
from datetime import timedelta , datetime
cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["messages"]


async def help(ctx):
    
    async def menu_callback(ctx):
        if selectmenu.values[0] == '1':
            embed = discord.Embed(
                title='APA moderation help',
                description=f'update your discord to see all mention commands\n\n🤖 commands:\n\n🌀 </kick:1134780676923732107>:\nTo kick a user from server [reason optional] \n\n🌀 </ban:1134780677095690280>:\nTo ban a member from server\n\n🌀 </unban:1134780677095690281>:\nTo unban member from server\n\n🌀 </mute:1134780677095690282>:\nTo timeout a member\n\n🌀 </unmute:1134780677095690283>:\nTo remove timeout\n\n🌀 </purge:1134780676923732106>:\nTo purge messages\n\n🌀 </lock:1134780677095690284>:\nTo lock text channel to send message\n\n🌀 </unlock:1134780677095690285>:\nTo remove lock from text channel\n\n🌀 </channel create:1134780677095690286>:\nTo create channel\n\n🌀 </channel delete:1134780677095690286>:\nTo delete channel\n\n🌀 </role rolecreate:1134780677095690287>:\nTo create role\n\n🌀 </role deleterole:1134780677095690287>:\nTo delete a role\n\n🌀 </role add:1134780677095690287>:\nTo add a role to user\n\n🌀 </role remove:1134780677095690287>:\nTo remove a role from user\n\n🌀 </autoroles:1134780677670310000>:\nEnable autorole feature\n\n🌀 </autoroles_role_add:1134780677670310001>:\nAdd role to autorole\n\n🌀 </show_autoroles:1134780677670310002>:\nShow all roles that you added to autorole\n\n🌀 a!roletoall:\nAdd a role to all users from server for using this command you must enter role id after id exp:a!roletoall 123764868516253\n\n🌀 a!remove_from_all:\nRemove a role from all users in the server for using this command you must enter role id after id exp:a!remove_from_all 123764868516253\n\n🌀 </vote:1154735532274880602>:\nTo create vote\n\n🌀 a!embedcopy <color> <yourtext>:Its will copy your text and send as a embed you can select the color too your options for color:white,black,purple,blue,red,pink,yellow,green exp:!embedcopy red hello my friend\n\n🌀 </update:1137484575426215996>:\nTo update bot whenever there is a update use this command every day if you are not in support server to check if there is any update\n\n🌀 </embedpost:1136646909528920082>:\nCreate an embed post with the bot\n\n🌀 </full_log_enable:1134780676923732104>:\nEnable log feature\n\n🌀 </full_log_set:1134780676923732105>:\nSet text channel for log | you can use it every 1 hour\n\n🌀 </auto_log_creator:1136646909528920075>:\nCreate seprate channels automatically for logs | you can use it every 6 hours\n\n🌀 </disable_log_sections:1136646909528920074>\nDisable log sections like full log set and auto log creator\n\n🌀 </selectrole:1134780677670309999>:\nCreate select menu add role\n\n🌀 </giveaway create:1134780676923732103>:\nCreate giveaway\n\n🌀  </giveaway reroll:1134780676923732103>:\nReroll the giveaway\n\n🌀 </avatar:1134780677095690288>:\nTo show user or your avatar\n\n🌀 </anime:1134780677095690289>:\nTo generate random anime picture',
                timestamp=datetime.now(),
                color = 0xF6F6F6
            )
            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
            await ctx.response.send_message(embed=embed , ephemeral=True)
        elif selectmenu.values[0] =='2':
            embed = discord.Embed(
                title='APA moderation help',
                description=f'update your discord to see all mention commands\n\n🤖🛡 Important Note: if you wants to be safe againts Nukes you must activate all security features and set punishment and warn limit for them to work if you just enable anti nuke feature you will only protected againts chat nukes so if you want to have one hundred percent security and be safe againts them make sure to install and config all the settings \n\n🛡 Step 1 : Turn on </security_on_off:1134780677305409556> \n\n🛡 Step 2: turn on </security_install:1134780677305409557>:\nTo install anti raid , anti prune , channels security options , role security options , bot invite security , discord link invite security \n\n🛡 Step 3:Turn on </ultra_security:1134780677305409558> to install anti server change , anti bad word , anti spam , anti ban , anti kick , anti unban , anti timeout , anti emoji delete , anti server change\n\n🛡 Step 4: </invite_security:1134780677468991610> to remove discord invite links (optional)\n\n🔐 Now you must config the security features otherwise its wont work\n\n🛡 </channel_security_config:1134780677305409559>:\no turn on channel options security and set warns and punishment this options are required if you want channel security options work for you\n\n🛡 </ultra_security_config:1134780677305409560>:\nset warn limits and punishments for ultra security options\n\n🛡 </role_security_config:1134780677305409561>:\nto turn on role options security and set warn limits and punishments, this options are required if you want role security options work for you\n\n🔐 Spam Config Section:\n\n🛡 </add_bad_words:1134780677305409562>:\nthe words that you want filter from your chat\n\n🛡 </remove_bad_words:1134780677468991607>:\nremove the words that you added to badwords\n\n🛡 </show_bad_words:1134780677468991608>:\nshow all of your bad words\n\n🛡 </timeout_time_badwords:1134780677305409563>:\nthe timeout that you want for punishment of using badwords (required)\n\n🛡 </anti_spam_time:1134780677305409564>:\nset time of timeout for spamming if you not set this its will use our default time for timeout that is 15m\n\n🔐 Whitelist Section:\n\n🛡 </role_security_whitelist:1134780677305409565>:\nset whitelist for role security section\n\n🛡 </channel_security_whitelist:1134780677468991601>:\nset whitelist for channel security section\n\n🛡 </general_whitelist:1134780677468991602>:\nset all whitelist , set anti prune whitelist , set anti spam whitelist , set bot invite whitelist , set discord invite whitelist\n\n🛡 </ultra_security_whitelist:1134780677468991603>:\nset whitelist for ultra security section\n\n🛡 </remove_whitelist:1134780677468991604>:\nremoving items from whitelists\n\n🛡 </show_whitelist:1134780677468991609>:\nshow all of your whitelists\n\n🔐 Security Log Config\n\n🛡 </security_log_enable:1134780677468991605>:\nto enable security log feature that is different with normal log\n\n🛡 </security_log_set:1134780677468991606>:\nto set a text channel for security log | you can use it every 1 hour',
                timestamp=datetime.now(),
                color = 0xF6F6F6
            )
            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
            await ctx.response.send_message(embed=embed , ephemeral=True)
        elif selectmenu.values[0] == '3':
            embed = discord.Embed(
                title='APA moderation help',
                description=f'update your discord to see all mention commands\n\n🤖 commands:\n\n🌀 </welcome_enable:1134780677670310005>:\nEnable welcome Feature\n\n🌀 </welcome_config:1134780677825503253>:\nSet required configs for welcome feature to work\n\n🌀 </welcome_disable:1134780677670310006>:\ndisable welcome feature and delete all welcome configs\n\n🌀 </welcome_channel_set:1134780677670310007>:\nset a text channel for welcome | you can use it every 1 hour\n\n🌀 </welcome_channel_remove:1134780677670310008>:\nRemove the welcome channel\n\n🌀 </reset_welcome_config:1134780677825503252>:\nDelete all welcome config',
                timestamp=datetime.now(),
                color = 0xF6F6F6
            )
            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
            await ctx.response.send_message(embed=embed , ephemeral=True)            
        elif selectmenu.values[0] == '4':
            embed = discord.Embed(
                title='APA moderation help',
                description=f'update your discord to see all mention commands\n\n🤖 commands:\n\n🌀 </ticket_config:1135170752107266048>:\nIts will enbale ticket and you can config the all parts of ticket system\n\n🌀 </ticket_remove_all:1136646909528920078>:\nRemoving all of your admins\n\n🌀 </ticket_remove_admin_menu:1153304040625680495>:\nRemove specific admin from menu style\n\n🌀 </ticket_remove_menu_item:1153304040625680496>:\nRemove specific item from dropdown menu of ticket\n\n🌀 </ticket_remove_admin_button:1153304040625680497>:\nRemove specific admin from button style\n\n🌀 </ticket_add_admin_button:1153534393894322287>:\nAdd admin to button style\n\n\n🌀 </ticket_add_admin_menu:1153304040625680498>:\nadd admin to menu style\n\n🌀 </ticket_style:1153304040625680499>:\nchoose the style of the ticket\n\n🌀 </ticket_show_admins:1136646909528920077>:\nyou can see support roles that you added\n\n🌀 </ticket_send:1135170752107266049>:\nSend ticket embed message for creation tickets in the specific channel that you want',
                color = 0xF6F6F6,
                timestamp=datetime.now()
            )
            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
            await ctx.response.send_message(embed=embed , ephemeral=True)             

        else:
            await ctx.response.defer()

    options = []
    options.append(discord.SelectOption(label='Moderation' , value='1' ,emoji='🤖'))
    options.append(discord.SelectOption(label='Security' , value='2' , emoji='🛡'))
    options.append(discord.SelectOption(label='Welcome' , value='3' , emoji='🙌'))
    options.append(discord.SelectOption(label='Ticket System' , value='4' , emoji='📩'))


    selectmenu = discord.ui.Select(placeholder='Select a command category to show commands' , options=options)
    selectmenu.callback = menu_callback
    select_view = discord.ui.View()
    select_view.add_item(selectmenu)
    av_button = discord.ui.Button(label ='Support Server' , url ='https://discord.gg/mkTXmUXfwZ' , emoji='🔽')
    link_button = discord.ui.Button(label= 'Vote Bot' , url = 'https://top.gg/bot/1119184391319601233/vote' , emoji = '🤖')
    select_view.add_item(av_button)
    select_view.add_item(link_button)
    embed = discord.Embed(title=f'APA HELP COMMANDS | Prefix:a!' ,description=f'🤖 Important Note: make sure to join our support server cause our updates will only announce in the support server so sometimes if we turn the bot off you must be in our support to know what is happening and if you had selected role with our bot there is no need to config it again after we turn the bot on and its will work fine like our ticket system\n\n🤖 Important Note 2 : if you want to be one hundred percent safe againts nuke attacks you must install and config all security features not just enable anti nuke reminde this!\n\nChoose the help section that you want from select menu' , timestamp=datetime.now() , color=0xF6F6F6 )
    embed.set_footer(text='Developed by APA team with ❤' , icon_url='https://cdn.discordapp.com/attachments/1135103098805817477/1135105421644943400/giphy.gif')        
    return embed , select_view


def get_timer(message):
    if (find:= collection.find_one({"user_id":message.author.id , "guild_id":message.guild.id , "punish":False})):
        timer = find['time']
        return timer

def get_message(message):
    if (find:= collection.find_one({"user_id":message.author.id , "guild_id":message.guild.id , "punish":False})):
        new_msg=find['message']
        return new_msg


def get_duplicate(message):
    if (find:= collection.find_one({"user_id":message.author.id , "guild_id":message.guild.id , "punish":False})):
        duplicate = find['duplicate']
        return duplicate


def get_count(message):
    if (find:= collection.find_one({"user_id":message.author.id , "guild_id":message.guild.id , "punish":False})):
        count = find['count']
        return count

def update_one(message , new_li ,count , duplicate , timer):
    collection.update_one({"user_id":message.author.id,"guild_id":message.guild.id} , {"$set":{"message":new_li, "count":count, "duplicate":duplicate, 'time':timer}})


def delete_one(message):
    collection.delete_one({"user_id":message.author.id , "guild_id":message.guild.id})



async def anti_spam(message):
    now=datetime.now().second
    if (find:= collection.find_one({"user_id":message.author.id , "guild_id":message.guild.id , "punish":False})):
        timer = get_timer(message)
        if (timer - now) >2:
            delete_one(message)
            return False
        else:
            timer = now
        new_msg= get_message(message)
        duplicate = get_duplicate(message)
        indexer = len(new_msg)-1
        flag=False
        if new_msg[indexer] == message.content:
            flag=True
        
        new_li =[]
        if flag ==True:
            duplicate+=1
        if duplicate ==3:
            delete_one(message)
            return True
        count = get_count(message)
        count+=1
        if count == 5:
            delete_one(message)
            return True
        
        new_li.extend(new_msg)
        new_li.append(message.content)
        # new_msg=new_msg.append(message.content)
        update_one(message ,new_li , count , duplicate , timer)
    else:
        messageer = list(message.content.split(','))
        collection.insert_one({"user_id":message.author.id , "guild_id":message.guild.id , "message":messageer , "count":1 , "duplicate":0 , 'punish':False , 'time':now})
    

