from __future__ import annotations
from sre_parse import State
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
import asyncio


cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["security"]

class security(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        

    @commands.hybrid_command(name='security_on_off' , description='Enable Security Feature')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.choices(security=[
        app_commands.Choice(name='Enable' , value=1),
        app_commands.Choice(name='Disable' , value=2)
    ])
    async def security_def(self,ctx,security:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)   
        try:
            if security.value ==1:
                if(find:= collection.find_one({"_id":ctx.guild.id})):
                    return await ctx.send('# Security already enabled')
                else:
                    await ctx.defer()
                    collection.insert_one({'_id':ctx.guild.id ,
                     'state':security.value ,
                     'anti_raid':None,
                     'all_white_list_user':None ,
                     'all_white_list_role':None,
                     'anti_bad_word':None,
                     'bad_words':None,
                     'bad_word_time_timeout':None,
                     'anti_bad_words_warn':None,
                     'anti_bad_words_punishment':None,
                     'anti_bad_words_white_role':None,
                     'anti_bad_words_white_user':None,
                     'anti_spam':None,
                     'anti_spam_white_user':None ,
                     'anti_spam_white_role':None,
                     'anti_spam_time':None,
                     'anti_ban':None,
                     'anti_ban_warn':None,
                     'anti_ban_punishment':None,
                     'anti_ban_white_role':None,
                     'anti_ban_white_user':None,
                     'anti_kick':None,
                     'anti_kick_warn':None,
                     'anti_kick_punishment':None,
                     'anti_kick_white_user':None,
                     'anti_kick_white_role':None,
                     'anti_unban':None,
                     'anti_unban_warn':None,
                     'anti_unban_punishment':None,
                     'anti_unban_white_role':None,
                     'anti_unban_white_user':None,
                     'anti_timeout':None,
                     'anti_timeout_warn':None,
                     'anti_timeout_punishment':None,
                     'anti_timeout_white_role':None,
                     'anti_timeout_white_user':None,
                     'anti_emoji_delete':None,
                     'anti_emoji_delete_warn':None,
                     'anti_emoji_delete_punishment':None,
                     'anti_emoji_white_role':None,
                     'anti_emoji_white_user':None,
                     'anti_server_change':None,
                     'anti_server_change_warn':None,
                     'anti_server_change_punishment':None,
                     'anti_server_change_white_role':None,
                     'anti_server_change_white_user':None,
                     'anti_prune' :None ,
                     'anti_prune_warn':None,
                     'anti_prune_punishment':None,
                     'anti_prune_white_role':None,
                     'anti_prune_white_user':None,
                     'anti_prune_role_id':None,
                     'bot_invite_ban_security':None,
                     'server_invite_detect_security':None,
                     'server_invite_warn':1,
                     'server_invite_punishment':'Delete',
                     'bot_invite_white_user':None ,
                     'bot_invite_white_role':None,
                     'bot_invite_warn':None,
                     'bot_invite_punishment':None, 
                     'discord_invite_white_user':None ,
                     'discord_invite_white_role':None, 
                     'channel_delete_enable':None,
                     'channel_update_enable':None,
                     'channel_create_enable':None,
                     'role_create_enable':None,
                     'role_update_enable':None,
                     'role_delete_enable':None,
                     'channel_delete_white_role':None ,
                     'channel_delete_white_user':None , 
                     'channel_create_white_role':None ,
                     'channel_create_white_user':None , 
                     'channel_update_white_role':None , 
                     'channel_update_white_user':None ,
                     'role_create_white_role':None , 
                     'role_create_white_user':None , 
                     'role_update_white_role':None , 
                     'role_update_white_user':None ,
                     'role_delete_white_role':None , 
                     'role_delete_white_user':None ,
                     'channel_delete_warn_limit':None , 
                     'channel_delete_punishment':None , 
                     'channel_create_warn_limit':None,
                     'channel_create_punishment':None , 
                     'channel_update_warn_limit':None,
                     'channel_update_punishment':None,
                     'role_delete_warn_limit':None,
                     'role_delete_punishment':None,
                     'role_update_warn_limit':None,
                     'role_update_punishment':None,
                     'role_create_warn_limit':None,
                     'role_create_punishment':None,
                     'security_log_channel':None,
                     'security_log_webhook':None

                     })
                    await ctx.send("# Security Feature Enabled successfully ")
            elif security.value ==2:
                collection.update_one({'_id':ctx.guild.id} , {'$set':{'state':security.value}})
                await ctx.send("# Security Feature Disabled successfully ")
        except:
            return await ctx.send('# something went wrong but it can be done too test security install maybe its installed')

        return
    @commands.hybrid_command(name='security_install' , description='Security install')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)   
    async def security_def1(self,ctx ,anti_raid:bool,anti_prune:bool,channel_delete_security:bool,channel_update_security:bool,channel_create_security:bool,role_create_security:bool,role_delete_security:bool,role_update_security:bool,discord_invite_security:bool,bot_invite_security:bool ):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if find['state']==1:
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_raid':anti_raid,'anti_prune':anti_prune , 'channel_delete_enable':channel_delete_security , 'channel_update_enable':channel_update_security , 'channel_create_enable':channel_create_security ,'role_create_enable':role_create_security , 'role_update_enable':role_update_security , 'role_delete_enable':role_delete_security , 'server_invite_detect_security':discord_invite_security , 'bot_invite_ban_security':bot_invite_security}} )
                    # if anti_prune == True:
                    #     if find['anti_prune_role_id'] is None:
                    #         anti_prune_role=await ctx.guild.create_role(name='anti prune')
                    #         collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_role_id':anti_prune_role.id}})
                    #         for member in ctx.guild.members:
                    #             await member.add_roles(anti_prune_role)
                    #     else:
                    #         flag = False
                    #         for role in ctx.guild.roles:
                    #             if role.id == find['anti_prune_role_id']:
                    #                 flag = True
                    #                 for member in ctx.guild.members:
                    #                     await asyncio.sleep(0.5)
                    #                     await member.add_roles(role)
                                        
                    #         if flag == False:
                    #             anti_prune_role=await ctx.guild.create_role(name='anti prune')
                    #             collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_role_id':anti_prune_role.id}})
                    #             for member in ctx.guild.members:
                    #                 await asyncio.sleep(0.5)
                    #                 await member.add_roles(anti_prune_role)

    

                    # elif anti_prune == False:
                    #     if find['anti_prune_role_id'] is not None:
                    #         for role in ctx.guild.roles:
                    #             if role.id == find['anti_prune_role_id']:
                    #                 await role.delete()
                    #                 collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_role_id':None}})

                    await ctx.send('# Settings Saved')
                elif find['state'] == 2:
                    await ctx.send('# pls Enable security Feature First')
            else:
                await ctx.send('# pls Enable security Feature First')

                    # role = discord.utils.get(ctx.guild.roles , id = find['anti_prune_role_id'])
                    # for member in ctx.guild.members:
                    #     await member.remove_roles(role)
        except:
            await ctx.send('# something went wrong pls try again')


        return
    @commands.hybrid_command(name='ultra_security' , description='for anti spam , anti kick and ...')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.cooldown(1, 10, commands.BucketType.guild)   
    async def security_def2(self,ctx ,anti_server_change:bool,anti_bad_word:bool ,anti_spam:bool,anti_ban:bool,anti_kick:bool,anti_unban:bool,anti_timeout:bool,anti_emoji_delete:bool):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if find['state']==1:
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_bad_word':anti_bad_word , 'anti_spam':anti_spam , 'anti_ban':anti_ban , 'anti_kick':anti_kick , 'anti_unban':anti_unban,'anti_timeout':anti_timeout , 'anti_emoji_delete':anti_emoji_delete , 'anti_server_change':anti_server_change }} )
                    await ctx.send('Settings Saved')
                elif find['state'] == 2:
                    await ctx.send('# pls Enable security Feature First')
            else:
                await ctx.send('# pls turn on security feature first')
        except:
            await ctx.send('# something went wrong pls try again')

        return
        
    @commands.hybrid_command(name='channel_security_config' , description='set warn limit and punishment')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.choices(channel_delete_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)
    ])
    @app_commands.choices(channel_create_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])

    @app_commands.choices(channel_update_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])
    async def channel_security(self,ctx ,channel_delete_security:bool,channel_create_security:bool,channel_update_security:bool, channel_delete_warn_limit:int,channel_update_warn_limit:int , channel_create_warn_limit:int ,  channel_delete_punishment:app_commands.Choice[int] , channel_create_punishment:app_commands.Choice[int] , channel_update_punishment:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if find['state']==1:
                    channel_delete_warn_limit = abs(channel_delete_warn_limit)
                    channel_update_warn_limit=abs(channel_update_warn_limit)
                    channel_create_warn_limit=abs(channel_create_warn_limit)
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_delete_enable':channel_delete_security,'channel_create_enable':channel_create_security , 'channel_update_enable':channel_update_security,'channel_delete_warn_limit':channel_delete_warn_limit , 'channel_create_warn_limit':channel_create_warn_limit , 'channel_update_warn_limit':channel_update_warn_limit , 'channel_delete_punishment':channel_delete_punishment.name , 'channel_create_punishment':channel_create_punishment.name , 'channel_update_punishment':channel_update_punishment.name}})
                    await ctx.send('Settings Saved')
                elif find['state'] == 2:
                    await ctx.send('# pls Enable security Feature First')

            else:
                await ctx.send("# Enable Security at the first then use this command")
        except:
            await ctx.send('# something went wrong')

        return

    @commands.hybrid_command(name='ultra_security_config' , description='set warn limit and punishment')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @app_commands.choices(anti_bad_words_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2),
        app_commands.Choice(name='Timeout' , value=3)
    ])

    @app_commands.choices(anti_kick_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])

    @app_commands.choices(anti_unban_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])

    @app_commands.choices(anti_timeout_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])

    @app_commands.choices(anti_emoji_delete_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])

    @app_commands.choices(anti_server_change_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])

    @app_commands.choices(anti_ban_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])

    @app_commands.choices(anti_prune_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])
    async def ultra_security_config(self,ctx ,anti_prune_warn:int ,anti_server_change_warn:int,anti_bad_words_warn:int,anti_ban_warn:int,anti_kick_warn:int,anti_unban_warn:int,anti_timeout_warn:int , anti_emoji_delete_warn:int ,  anti_bad_words_punishment:app_commands.Choice[int], anti_kick_punishment:app_commands.Choice[int], anti_unban_punishment:app_commands.Choice[int], anti_timeout_punishment:app_commands.Choice[int], anti_emoji_delete_punishment:app_commands.Choice[int], anti_server_change_punishment:app_commands.Choice[int]  , anti_ban_punishment:app_commands.Choice[int] , anti_prune_punishment:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if find['state']==1:
                    anti_bad_words_warn = abs(anti_bad_words_warn)
                    anti_ban_warn=abs(anti_ban_warn)
                    anti_kick_warn=abs(anti_kick_warn)
                    anti_unban_warn=abs(anti_unban_warn)
                    anti_timeout_warn=abs(anti_timeout_warn)
                    anti_emoji_delete_warn=abs(anti_emoji_delete_warn)
                    anti_server_change_warn=abs(anti_server_change_warn)
                    anti_prune_warn=abs(anti_prune_warn)
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_bad_words_warn':anti_bad_words_warn, 'anti_ban_warn':anti_ban_warn,'anti_kick_warn':anti_kick_warn , 'anti_unban_warn':anti_unban_warn , 'anti_timeout_warn':anti_timeout_warn , 'anti_emoji_delete_warn':anti_emoji_delete_warn ,'anti_server_change_warn':anti_server_change_warn , 'anti_prune_warn':anti_prune_warn,'anti_prune_punishment':anti_prune_punishment.name, 'anti_bad_words_punishment':anti_bad_words_punishment.name , 'anti_kick_punishment':anti_kick_punishment.name , 'anti_unban_punishment':anti_unban_punishment.name , 'anti_timeout_punishment':anti_timeout_punishment.name , 'anti_emoji_delete_punishment':anti_emoji_delete_punishment.name , 'anti_server_change_punishment':anti_server_change_punishment.name  , 'anti_ban_punishment':anti_ban_punishment.name}})
                    await ctx.send('# settings saved')
                elif find['state'] == 2:
                    await ctx.send('# pls Enable security Feature First')

            else:
                await ctx.send("# Enable Security at the first then use this command")
        except:
            await ctx.send('# something went wrong pls try again')

        return




    @commands.hybrid_command(name='role_security_config' , description='set warn limit and punishment')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @app_commands.choices(role_create_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])  
    @app_commands.choices(role_update_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])

    @app_commands.choices(role_delete_punishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)])
    
    async def role_security(self,ctx ,role_create_security:bool,role_delete_security:bool,role_update_security:bool ,role_delete_warn_limit:int,role_update_warn_limit:int , role_create_warn_limit:int ,  role_create_punishment:app_commands.Choice[int] , role_update_punishment:app_commands.Choice[int] , role_delete_punishment:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if find['state']==1:
                    role_delete_warn_limit = abs(role_delete_warn_limit)
                    role_update_warn_limit=abs(role_update_warn_limit)
                    role_create_warn_limit=abs(role_create_warn_limit)
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_create_enable':role_create_security,'role_delete_security':role_delete_security,'role_update_security':role_update_security,'role_delete_warn_limit':role_delete_warn_limit , 'role_update_warn_limit':role_update_warn_limit , 'role_create_warn_limit':role_create_warn_limit , 'role_create_punishment':role_create_punishment.name , 'role_update_punishment':role_update_punishment.name , 'role_delete_punishment':role_delete_punishment.name}})
                    await ctx.send('# settings saved')
                elif find['state'] == 2:
                    await ctx.send('# pls Enable security Feature First')

            else:
                await ctx.send("# Enable Security at the first then use this command")
        except:
            await ctx.send('# something went wrong pls try again')
        
        return 

    @commands.hybrid_command(name='add_bad_words' , description='Enter the bad words that you wanna block')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def bad_word_add(self,ctx,*,bad_words:str):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            list_create_role=[]
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if find['state']==1:
                    if bad_words is not None:
                        if find['anti_bad_word'] == True:
                            text = bad_words.split(',')
                            try:    
                                tmp=find['bad_words']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.extend(text)
                                else:
                                    list_create_role = []
                                    list_create_role.append(tmp)
                                    list_create_role.extend(text)

                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bad_words':list_create_role}})
                                await ctx.send('done')
                            except:
                                return
                        else:
                            await ctx.send('# you should first complete other parts of bad words feature then use this option')
                    else:
                        await ctx.send('# bad words are empty')
                else:
                    await ctx.send('# pls Enable Security First')
            else:
                await ctx.send('# pls turn on security feature first')
        except:
            await ctx.send('# something went wrong pls try again')
        
        return

    @commands.hybrid_command(name='timeout_time_badwords' , description='Enter the time of timeout for bad words')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def bad_word_time(self,ctx,time):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            await ctx.defer()
            try:
                if(find:= collection.find_one({"_id":ctx.guild.id ,'anti_timeout':True })):
                    time = parse_timespan(time)
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bad_word_time_timeout':time}})
                    await ctx.send('# done')
                else:
                    await ctx.send('# make sure that you Enabled anti bad words and security then use this command')
            except InvalidTimespan:
                await ctx.send('# you didnt enter a valid time')
        except:
            await ctx.send('# something went wrong pls try again')
        
        return

    @commands.hybrid_command(name='anti_spam_time' , description='Enter the time of timeout for spam')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def anti_spam_time(self,ctx,time):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            try:
                if(find:= collection.find_one({"_id":ctx.guild.id , 'anti_spam':True})):
                    time = parse_timespan(time)
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_time':time}})
                    await ctx.send('# done')
                else:
                    await ctx.send('# make sure that you Enabled anti spam and security then use this command')
            except InvalidTimespan:
                await ctx.send('# you didnt enter a valid time')       
        except:
            await ctx.send('# something went wrong pls try again')
        
        return 

    @commands.hybrid_command(name='role_security_whitelist' , description='set role security whitelist')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def role_security_white(self,ctx,role_create_whitelist:Optional[Union[User , Role]] , role_delete_whitelist:Optional[Union[User , Role]] , role_update_whitelist:Optional[Union[User , Role]]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        await ctx.defer()
        list_create_role=[]
        list_create_user=[]
        list_delete_role=[]
        list_delete_user=[]
        list_update_user=[]
        list_update_role=[]
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            if find['state']==1:
                if role_create_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=role_create_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=role_create_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in role create is above me no need to add in whitelist')
                            else:
                                tmp=find['role_create_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(role_create_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_create_white_role':list_create_role}})
                                    await ctx.send('role create whitelist done')
                                else:
                                    if role_create_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(role_create_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_create_white_role':list_create_role}})
                                        await ctx.send('role create whitelist done')
                                    else:
                                        await ctx.send('its already in role create whitelist')
                            
                        elif check2 is not None:
                            tmp=find['role_create_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(role_create_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_create_white_user':list_create_user}})
                                await ctx.send('role create whitelist done')
                            else:
                                if role_create_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(role_create_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_create_white_user':list_create_user}})
                                    await ctx.send('role create whitelist done')
                                else:
                                    await ctx.send('its already in role create whitelist')
                            

                    except:
                        await ctx.send('something went wrong in role create whitelist pls try again')

                if role_delete_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=role_delete_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=role_delete_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in role delete is above me no need to add in whitelist')
                            else:

                                tmp=find['role_delete_white_role']
                                if tmp is None:
                                    list_delete_role = []
                                    list_delete_role.append(role_delete_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_delete_white_role':list_delete_role}})
                                    await ctx.send('role delete whitelist done')
                                else:
                                    if role_delete_whitelist.id not in tmp:
                                        list_delete_role = []
                                        list_delete_role.extend(tmp)
                                        list_delete_role.append(role_delete_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_delete_white_role':list_delete_role}})
                                        await ctx.send('role delete whitelist done')
                                    else:
                                        await ctx.send('its already in role delete whitelist')

                            
                            
                        elif check2 is not None:
                            tmp=find['role_delete_white_user']
                            if tmp is None:
                                list_delete_user = []
                                list_delete_user.append(role_delete_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_delete_white_user':list_delete_user}})
                                await ctx.send('role delete whitelist done')
                            else:
                                if role_delete_whitelist.id not in tmp:
                                    list_delete_user = []
                                    list_delete_user.extend(tmp)
                                    list_delete_user.append(role_delete_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_delete_white_user':list_delete_user}})
                                    await ctx.send('role delete whitelist done')
                                else:
                                    await ctx.send('its already in role delete whitelist')

                            
                    except:
                        await ctx.send('something went wrong in role delete whitelist pls try again')

                if role_update_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=role_update_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=role_update_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in role update is above me no need to add in whitelist')
                            else:

                                tmp=find['role_update_white_role']
                                if tmp is None:
                                    list_update_role = []
                                    list_update_role.append(role_update_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_update_white_role':list_update_role}})
                                    await ctx.send('role update whitelist done')
                                else:
                                    if role_update_whitelist.id not in tmp:
                                        list_update_role = []
                                        list_update_role.extend(tmp)
                                        list_update_role.append(role_update_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_update_white_role':list_update_role}})
                                        await ctx.send('role update whitelist done')
                                    else:
                                        await ctx.send('its already in role update whitelist')

                            
                            await ctx.send('done')
                        elif check2 is not None:
                            tmp=find['role_update_white_user']
                            if tmp is None:
                                list_update_user = []
                                list_update_user.append(role_update_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_update_white_user':list_update_user}})
                                await ctx.send('role update white user')
                            else:
                                if role_update_whitelist.id not in tmp:
                                    list_update_user = []
                                    list_update_user.extend(tmp)
                                    list_update_user.append(role_update_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_update_white_user':list_update_user}})
                                    await ctx.send('role update white user')
                                else:
                                    await ctx.send('its already in role update whitelist')
                            
                    except:
                        await ctx.send('something went wrong in role update whitelist pls try again')
                await ctx.send('done')
               
            elif find['state']==2:
                await ctx.send('pls Enable Security First')
        else:
            await ctx.send('pls turn on security feature')

        return
    @commands.hybrid_command(name='channel_security_whitelist' , description='set channel security whitelist')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def channel_security_white(self,ctx,channel_create_whitelist:Optional[Union[User , Role]] , channel_delete_whitelist:Optional[Union[User , Role]] , channel_update_whitelist:Optional[Union[User , Role]]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)

        await ctx.defer()
        list_create_role=[]
        list_create_user=[]
        list_delete_role=[]
        list_delete_user=[]
        list_update_user=[]
        list_update_role=[]
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            if find['state']==1:
                if channel_delete_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=channel_delete_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=channel_delete_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in channel delete is above me no need to add in whitelist')
                            else:
                                tmp=find['channel_delete_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(channel_delete_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_delete_white_role':list_create_role}})
                                    await ctx.send('channel delete whitelist done')
                                else:
                                    if channel_delete_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(channel_delete_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_delete_white_role':list_create_role}})
                                        await ctx.send('channel delete whitelist done')
                                    else:
                                        await ctx.send('its already in channel delete whitelist')

                            
                        elif check2 is not None:
                            tmp=find['channel_delete_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(channel_delete_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_delete_white_user':list_create_user}})
                                await ctx.send('channel delete whitelist done')
                            else:
                                if channel_delete_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(channel_delete_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_delete_white_user':list_create_user}})
                                    await ctx.send('channel delete whitelist done')
                                else:
                                    await ctx.send('its already in channel delete whitelist')
                            

                    except:
                        await ctx.send('something went wrong in channel delete pls try again')

                if channel_create_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=channel_create_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=channel_create_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in channel create is above me no need to add in whitelist')
                            else:

                                tmp=find['channel_create_white_role']
                                if tmp is None:
                                    list_delete_role = []
                                    list_delete_role.append(channel_create_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_create_white_role':list_delete_role}})
                                    await ctx.send('channel create whitelist done')
                                else:
                                    if channel_create_whitelist.id not in tmp:
                                        list_delete_role = []
                                        list_delete_role.extend(tmp)
                                        list_delete_role.append(channel_create_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_create_white_role':list_delete_role}})
                                        await ctx.send('channel create whitelist done')
                                    else:
                                        await ctx.send('its already in channel create whitelist')

                        elif check2 is not None:
                            tmp=find['channel_create_white_user']
                            if tmp is None:
                                list_delete_user = []
                                list_delete_user.append(channel_create_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_create_white_user':list_delete_user}})
                                await ctx.send('channel create whitelist done')
                            else:
                                if channel_create_whitelist.id not in tmp:
                                    list_delete_user = []
                                    list_delete_user.extend(tmp)
                                    list_delete_user.append(channel_create_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_create_white_user':list_delete_user}})
                                    await ctx.send('channel create whitelist done')
                                else:
                                    await ctx.send('its already in channel create whitelist')

                            
                    except:
                        await ctx.send('something went wrong in channel create pls try again')

            
                if channel_update_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=channel_update_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=channel_update_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in channel update is above me no need to add in whitelist')
                            else:
                                tmp=find['channel_update_white_role']
                                if tmp is None:
                                    list_update_role = []
                                    list_update_role.append(channel_update_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_update_white_role':list_update_role}})
                                    await ctx.send('channel update whitelist done')
                                else:
                                    if channel_update_whitelist.id not in tmp:
                                        list_update_role = []
                                        list_update_role.extend(tmp)
                                        list_update_role.append(channel_update_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_update_white_role':list_update_role}})
                                        await ctx.send('channel update whitelist done')
                                    else:
                                        await ctx.send('its already in channel update whitelist')

                            
                        elif check2 is not None:
                            tmp=find['channel_update_white_user']
                            if tmp is None:
                                list_update_user = []
                                list_update_user.append(channel_update_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_update_white_user':list_update_user}})
                                await ctx.send('channel update whitelist done')
                            else:
                                if channel_update_whitelist.id not in tmp:
                                    list_update_user = []
                                    list_update_user.extend(tmp)
                                    list_update_user.append(channel_update_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_update_white_user':list_update_user}})
                                    await ctx.send('channel update whitelist done')
                                else:
                                    await ctx.send('its already in channel update whitelist')

                            
                    except:
                        await ctx.send('something went wrong in channel update pls try again')


                await ctx.send('done')
            elif find['state']==2:
                await ctx.send('pls Enable Security First')
        else:
            await ctx.send('pls turn on security feature')

        return
    @commands.hybrid_command(name='general_whitelist' , description='set general security whitelist')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def local_security_white(self,ctx,anti_prune_whitelist:Optional[Union[User , Role]],all_white_list:Optional[Union[User , Role]],anti_spam_whitelist:Optional[Union[User , Role]] , bot_invite_whitelist:Optional[Union[User , Role]] , discord_invite_whitelist:Optional[Union[User , Role]]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        await ctx.defer()
        list_create_role=[]
        list_create_user=[]
        list_delete_role=[]
        list_delete_user=[]
        list_update_user=[]
        list_update_role=[]
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            if find['state']==1:
                if all_white_list is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=all_white_list.id)
                    check2 = discord.utils.get(ctx.guild.members , id=all_white_list.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in all whitelist is above me no need to add in whitelist')
                            else:
                                tmp=find['all_white_list_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(all_white_list.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'all_white_list_role':list_create_role}})
                                    await ctx.send('all whitelist done')
                                else:
                                    if all_white_list.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(all_white_list.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'all_white_list_role':list_create_role}})
                                        await ctx.send('all whitelist done')
                                    else:
                                        await ctx.send('its already in all whitelist')

                            
                        elif check2 is not None:
                            tmp=find['all_white_list_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(all_white_list.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'all_white_list_user':list_create_user}})
                                await ctx.send('all whitelist done')
                            else:
                                if all_white_list.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(all_white_list.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'all_white_list_user':list_create_user}})
                                    await ctx.send('all whitelist done')
                                else:
                                    await ctx.send('its already in all whitelist')

                            
                    except:
                        await ctx.send('something went wrong in all whitelist pls try again')

                if anti_spam_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_spam_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_spam_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti spam is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_spam_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_spam_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_role':list_create_role}})
                                    await ctx.send('anti spam whitelist done')
                                else:
                                    if anti_spam_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_spam_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_role':list_create_role}})
                                        await ctx.send('anti spam whitelist done')
                                    else:
                                        await ctx.send('its already in spam whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_spam_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_spam_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_user':list_create_user}})
                                await ctx.send('anti spam whitelist done')
                            else:
                                if anti_spam_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_spam_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_user':list_create_user}})
                                    await ctx.send('anti spam whitelist done')
                                else:
                                    await ctx.send('its already in spam whitelist')

                            

                    except:
                        await ctx.send('something went wrong in anti spam whitelist pls try again')

                if anti_prune_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_prune_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_prune_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti prune is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_prune_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_prune_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_white_role':list_create_role}})
                                    await ctx.send('anti prune whitelist done')
                                else:
                                    if anti_prune_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_prune_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_white_role':list_create_role}})
                                        await ctx.send('anti prune whitelist done')
                                    else:
                                        await ctx.send('its already in anti prune whitelist')
                            
                        elif check2 is not None:
                            tmp=find['anti_prune_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_prune_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_white_user':list_create_user}})
                                await ctx.send('anti prune whitelist done')
                            else:
                                if anti_prune_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_prune_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_white_user':list_create_user}})
                                    await ctx.send('anti prune whitelist done')
                                else:
                                    await ctx.send('its already in anti prune whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti prune whitelist pls try again')

                if bot_invite_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=bot_invite_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=bot_invite_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in bot invite is above me no need to add in whitelist')
                            else:
                                tmp=find['bot_invite_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(bot_invite_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bot_invite_white_role':list_create_role}})
                                    await ctx.send('anti bot invite whitelist done')
                                else:
                                    if bot_invite_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(bot_invite_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bot_invite_white_role':list_create_role}})
                                        await ctx.send('anti bot invite whitelist done')
                                    else:
                                        await ctx.send('its already in anti bot invite whitelist')

                            
                        elif check2 is not None:
                            tmp=find['bot_invite_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(bot_invite_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bot_invite_white_user':list_create_user}})
                                await ctx.send('anti bot invite whitelist done')
                            else:
                                if bot_invite_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(bot_invite_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bot_invite_white_user':list_create_user}})
                                    await ctx.send('anti bot invite whitelist done')
                                else:
                                    await ctx.send('its already in anti bot invite whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti bot invite whitelist pls try again')

                if discord_invite_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=discord_invite_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=discord_invite_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in discord invite is above me no need to add in whitelist')
                            else:
                                tmp=find['discord_invite_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(discord_invite_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'discord_invite_white_role':list_create_role}})
                                    await ctx.send('anti discord invite whitelist done')
                                else:
                                    if discord_invite_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(discord_invite_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'discord_invite_white_role':list_create_role}})
                                        await ctx.send('anti discord invite whitelist done')
                                    else:
                                        await ctx.send('its already in anti discord invite whitelist')
                                    

                            
                        elif check2 is not None:
                            tmp=find['discord_invite_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(discord_invite_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'discord_invite_white_user':list_create_user}})
                                await ctx.send('anti discord invite whitelist done')
                            else:
                                if discord_invite_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(discord_invite_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'discord_invite_white_user':list_create_user}})
                                    await ctx.send('anti discord invite whitelist done')
                                else:
                                    await ctx.send('its already in anti discord invite whitelist')
                            
                  
                    except:
                        await ctx.send('something went wrong in anti discord invite whitelist pls try again')
            
                await ctx.send('done')            
            elif find['state']==2:
                await ctx.send('pls Enable Security First')

        else:
            await ctx.send('pls turn on security feature first')
        
        return
    @commands.hybrid_command(name='ultra_security_whitelist' , description='set ultra security section whitelist')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def ultra_security_white(self,ctx,anti_bad_words_whitelist:Optional[Union[User , Role]],anti_spam_whitelist:Optional[Union[User , Role]] , anti_ban_whitelist:Optional[Union[User , Role]] , anti_kick_whitelist:Optional[Union[User , Role]] , anti_unban_whitelist:Optional[Union[User , Role]] , anti_timeout_whitelist:Optional[Union[User , Role]],anti_emoji_whitelist:Optional[Union[User , Role]],anti_server_change_whitelist:Optional[Union[User , Role]]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        await ctx.defer()
        list_create_role=[]
        list_create_user=[]
        list_delete_role=[]
        list_delete_user=[]
        list_update_user=[]
        list_update_role=[]
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            if find['state']==1:
                if anti_bad_words_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_bad_words_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_bad_words_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti bad words is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_bad_words_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_bad_words_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_bad_words_white_role':list_create_role}})
                                    await ctx.send('anti bad words done')
                                else:
                                    if anti_bad_words_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_bad_words_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_bad_words_white_role':list_create_role}})
                                        await ctx.send('anti bad words done')
                                    else:
                                        await ctx.send('its already in anti bad words whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_bad_words_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_bad_words_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_bad_words_white_user':list_create_user}})
                                await ctx.send('anti bad words done')
                            else:
                                if anti_bad_words_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_bad_words_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_bad_words_white_user':list_create_user}})
                                    await ctx.send('anti bad words done')
                                else:
                                    await ctx.send('its already in anti bad words whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti bad words whitelist pls try again')

                if anti_spam_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_spam_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_spam_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti spam is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_spam_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_spam_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_role':list_create_role}})
                                    await ctx.send('anti spam done')
                                else:
                                    if anti_spam_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_spam_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_role':list_create_role}})
                                        await ctx.send('anti spam done')
                                    else:
                                        await ctx.send('its already in anti spam whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_spam_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_spam_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_user':list_create_user}})
                                await ctx.send('anti spam done')
                            else:
                                if anti_spam_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_spam_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_user':list_create_user}})
                                    await ctx.send('anti spam done')
                                else:
                                    await ctx.send('its already in anti spam whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti spam whitelist pls try again')

                if anti_ban_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_ban_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_ban_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti ban is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_ban_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_ban_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_ban_white_role':list_create_role}})
                                    await ctx.send('anti ban done')
                                else:
                                    if anti_ban_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_ban_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_ban_white_role':list_create_role}})
                                        await ctx.send('anti ban done')
                                    else:
                                        await ctx.send('its already in anti ban whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_ban_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_ban_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_ban_white_user':list_create_user}})
                                await ctx.send('anti ban done')
                            else:
                                if anti_ban_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_ban_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_ban_white_user':list_create_user}})
                                    await ctx.send('anti ban done')
                                else:
                                    await ctx.send('its already in anti ban whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti ban whitelist pls try again')

                if anti_kick_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_kick_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_kick_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti kick is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_kick_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_kick_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_kick_white_role':list_create_role}})
                                    await ctx.send('anti kick done')
                                else:
                                    if anti_kick_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_kick_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_kick_white_role':list_create_role}})
                                        await ctx.send('anti kick done')
                                    else:
                                        await ctx.send('its already in anti kick whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_kick_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_kick_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_kick_white_user':list_create_user}})
                                await ctx.send('anti kick done')
                            else:
                                if anti_kick_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_kick_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_kick_white_user':list_create_user}})
                                    await ctx.send('anti kick done')
                                else:
                                    await ctx.send('its already in anti kick whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti kick whitelist pls try again')

                if anti_unban_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_unban_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_unban_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti unban is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_unban_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_unban_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_unban_white_role':list_create_role}})
                                    await ctx.send('anti unban done')
                                else:
                                    if anti_unban_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_unban_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_unban_white_role':list_create_role}})
                                        await ctx.send('anti unban done')
                                    else:
                                        await ctx.send('its already in anti unban whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_unban_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_unban_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_unban_white_user':list_create_user}})
                                await ctx.send('anti unban done')
                            else:
                                if anti_unban_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_unban_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_unban_white_user':list_create_user}})
                                    await ctx.send('anti unban done')
                                else:
                                    await ctx.send('its already in anti unban whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti unban whitelist pls try again')

                if anti_timeout_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_timeout_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_timeout_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti timeout is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_timeout_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_timeout_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_timeout_white_role':list_create_role}})
                                    await ctx.send('anti timeout done')
                                else:
                                    if anti_timeout_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_timeout_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_timeout_white_role':list_create_role}})
                                        await ctx.send('anti timeout done')
                                    else:
                                        await ctx.send('its already in anti timeout whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_timeout_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_timeout_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_timeout_white_user':list_create_user}})
                                await ctx.send('anti timeout done')
                            else:
                                if anti_timeout_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_timeout_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_timeout_white_user':list_create_user}})
                                    await ctx.send('anti timeout done')
                                else:
                                    await ctx.send('its already in anti timeout whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti timeout whitelist pls try again')


                if anti_emoji_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_emoji_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_emoji_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti emoji is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_emoji_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_emoji_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_emoji_white_role':list_create_role}})
                                    await ctx.send('anti emoji done')
                                else:
                                    if anti_emoji_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_emoji_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_emoji_white_role':list_create_role}})
                                        await ctx.send('anti emoji done')
                                    else:
                                        await ctx.send('its already in anti emoji whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_emoji_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_emoji_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_emoji_white_user':list_create_user}})
                                await ctx.send('anti emoji done')
                            else:
                                if anti_emoji_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_emoji_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_emoji_white_user':list_create_user}})
                                    await ctx.send('anti emoji done')
                                else:
                                    await ctx.send('its already in anti emoji whitelist')

                            
                    except:
                        await ctx.send('something went wrong in anti emoji whitelist pls try again')

                if anti_server_change_whitelist is not None:
                    check1=discord.utils.get(ctx.guild.roles , id=anti_server_change_whitelist.id)
                    check2 = discord.utils.get(ctx.guild.members , id=anti_server_change_whitelist.id)
                    try:    
                        if check1 is not None:
                            if ctx.guild.me.top_role.position <= check1.position:
                                await ctx.send('the choosen role in anti server change is above me no need to add in whitelist')
                            else:
                                tmp=find['anti_server_change_white_role']
                                if tmp is None:
                                    list_create_role = []
                                    list_create_role.append(anti_server_change_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_server_change_white_role':list_create_role}})
                                    await ctx.send('anti server change done')
                                else:
                                    if anti_server_change_whitelist.id not in tmp:
                                        list_create_role = []
                                        list_create_role.extend(tmp)
                                        list_create_role.append(anti_server_change_whitelist.id)
                                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_server_change_white_role':list_create_role}})
                                        await ctx.send('anti server change done')
                                    else:
                                        await ctx.send('its already in anti server change whitelist')

                            
                        elif check2 is not None:
                            tmp=find['anti_server_change_white_user']
                            if tmp is None:
                                list_create_user = []
                                list_create_user.append(anti_server_change_whitelist.id)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_server_change_white_user':list_create_user}})
                                await ctx.send('anti server change done')
                            else:
                                if anti_server_change_whitelist.id not in tmp:
                                    list_create_user = []
                                    list_create_user.extend(tmp)
                                    list_create_user.append(anti_server_change_whitelist.id)
                                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_server_change_white_user':list_create_user}})
                                    await ctx.send('anti server change done')
                                else:
                                    await ctx.send('its already in anti server change whitelist')

                    except:
                        await ctx.send('something went wrong in anti server change whitelist pls try again')
                await ctx.send('done')

            elif find['state']==2:
                await ctx.send('enable security first')
        else:
            await ctx.send("pls turn on security feature firs")                    

        return

    @commands.hybrid_command(name='remove_whitelist' , description='remove optional whitelist')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @app_commands.choices(choose_whitelist=[        
        app_commands.Choice(name='all_white_list' , value=1),
        app_commands.Choice(name='anti_bad_words_whitelist' , value=2),
        app_commands.Choice(name='anti_spam_whitelist' , value=3),
        app_commands.Choice(name='anti_ban_whitelist' , value=4),
        app_commands.Choice(name='anti_kick_whitelist' , value=5),
        app_commands.Choice(name='anti_unban_whitelist' , value=6),
        app_commands.Choice(name='anti_timeout_whitelist' , value=7),
        app_commands.Choice(name='anti_emoji_whitelist' , value=8),
        app_commands.Choice(name='anti_server_change_whitelist' , value=9),
        app_commands.Choice(name='anti_prune_whitelist' , value=10),
        app_commands.Choice(name='bot_invite_whitelist' , value=11),
        app_commands.Choice(name='discord_invite_whitelist' , value=12),
        app_commands.Choice(name='channel_delete_whitelist' , value=13),
        app_commands.Choice(name='channel_create_whitelist' , value=14),
        app_commands.Choice(name='channel_update_whitelist' , value=15),
        app_commands.Choice(name='role_create_whitelist' , value=16),
        app_commands.Choice(name='role_update_whitelist' , value=17),
        app_commands.Choice(name='role_delete_whitelist' , value=18),])

    async def remove_whitelist(self,ctx , choose_whitelist:app_commands.Choice[int] ,remove_item:Union[User , Role] ):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if choose_whitelist.value ==1:
                    list_roles = []
                    list_users=[]
                    if find['all_white_list_role'] is not None:
                        for i in find['all_white_list_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['all_white_list_user'] is not None:
                        for j in find['all_white_list_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'all_white_list_role':list_roles}})
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'all_white_list_user':list_users}})

                if choose_whitelist.value ==2:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_bad_words_white_role'] is not None:
                        for i in find['anti_bad_words_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_bad_words_white_user'] is not None:
                        for j in find['anti_bad_words_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_bad_words_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_bad_words_white_user':list_users}})
                                flag=True
                    
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')

                if choose_whitelist.value ==3:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_spam_white_role'] is not None:
                        for i in find['anti_spam_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_spam_white_user'] is not None:
                        for j in find['anti_spam_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_spam_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==4:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_ban_white_role'] is not None:
                        for i in find['anti_ban_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_ban_white_user'] is not None :
                        for j in find['anti_ban_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_ban_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_ban_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')

                if choose_whitelist.value ==5:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_kick_white_role'] is not None:
                        for i in find['anti_kick_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_kick_white_user'] is not None:
                        for j in find['anti_kick_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_kick_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_kick_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')

                if choose_whitelist.value ==6:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_unban_white_role'] is not None:
                        for i in find['anti_unban_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_unban_white_user'] is not None:
                        for j in find['anti_unban_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_unban_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_unban_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==7:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_timeout_white_role'] is not None:
                        for i in find['anti_timeout_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_timeout_white_user'] is not None:
                        for j in find['anti_timeout_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_timeout_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_timeout_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')

                if choose_whitelist.value ==8:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_emoji_white_role'] is not None:
                        for i in find['anti_emoji_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_emoji_white_user'] is not None:
                        for j in find['anti_emoji_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_emoji_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_emoji_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==9:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_server_change_white_role'] is not None:
                        for i in find['anti_server_change_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_server_change_white_user'] is not None:
                        for j in find['anti_server_change_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_server_change_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_server_change_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==10:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['anti_prune_white_role'] is not None:
                        for i in find['anti_prune_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_prune_white_user'] is not None:
                        for j in find['anti_prune_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'anti_prune_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==11:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['bot_invite_white_role'] is not None:
                        for i in find['bot_invite_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['bot_invite_white_user'] is not None:
                        for j in find['bot_invite_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bot_invite_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bot_invite_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')



                if choose_whitelist.value ==12:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['discord_invite_white_role'] is not None:
                        for i in find['discord_invite_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['discord_invite_white_user'] is not None:
                        for j in find['discord_invite_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'discord_invite_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'discord_invite_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==13:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['channel_delete_white_role'] is not None:
                        for i in find['channel_delete_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['channel_delete_white_user'] is not None:
                        for j in find['channel_delete_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_delete_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_delete_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==14:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['channel_create_white_role'] is not None:
                        for i in find['channel_create_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['channel_create_white_user'] is not None:
                        for j in find['channel_create_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_create_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_create_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')



                if choose_whitelist.value ==15:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['channel_update_white_role'] is not None:
                        for i in find['channel_update_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['channel_update_white_user'] is not None:
                        for j in find['channel_update_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_update_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel_update_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==16:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['role_create_white_role'] is not None:
                        for i in find['role_create_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['role_create_white_user'] is not None:
                        for j in find['role_create_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_create_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_create_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==17:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['role_update_white_role'] is not None:
                        for i in find['role_update_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['role_update_white_user'] is not None:
                        for j in find['role_update_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_update_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_update_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                if choose_whitelist.value ==18:
                    list_roles = []
                    list_users=[]
                    flag=False
                    if find['role_delete_white_role'] is not None:
                        for i in find['role_delete_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['role_delete_white_user'] is not None:
                        for j in find['role_delete_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                    if len(list_roles) !=0:
                        for i in list_roles:
                            if i == remove_item.id:
                                list_roles.remove(i)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_delete_white_role':list_roles}})
                                flag=True
                    
                    if len(list_users) !=0:
                        for j in list_users:
                            if j == remove_item.id:
                                list_users.remove(j)
                                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'role_delete_white_user':list_users}})
                                flag=True
                    if flag == True:
                        await ctx.send('removed successfully')
                    else:
                        await ctx.send('the item that you choosed was`nt in this section white roles')


                await ctx.send('done')
            else:
                await ctx.send('Enable security first')
        except:
            await ctx.send('something went wrong pls try again')

        return
    @commands.hybrid_command(name='security_log_enable' , description='Enable Security Log Feature')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def security_log_enable(self,ctx , state:bool):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if state == True:
                    if (find2:= collection.find_one({"state_sec":True,"guild_id":ctx.guild.id , "sec_log":True})) is None:
                        collection.insert_one({'state_sec':state , 'guild_id':ctx.guild.id, "sec_log":True})
                        await ctx.send('security log channel enable successfully')
                    else:
                        await ctx.send('already enable')
                elif state == False:
                    collection.delete_one({'state_sec':True , 'guild_id':ctx.guild.id, "sec_log":True})
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'security_log_channel':None}})
                    await ctx.send('security log channel disable successfully')
            else:
                await ctx.send('Enable security first')
        except:
            await ctx.send('something went wrong pls try again')
    
        return

    @commands.hybrid_command(name='security_log_set' , description='set security log Feature text channel')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3600, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 3600.0, key=lambda i: (i.guild.id))
    async def security_log(self,ctx , log_channel:TextChannel):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        await ctx.defer()
        member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
        webhook_avatar =member1.display_avatar
        profile_webhook= await webhook_avatar.read()
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            if(find2:= collection.find_one({"state_sec":True,"guild_id":ctx.guild.id , "sec_log":True})):
                webhook_channel_set=discord.Object(log_channel.id , type='abc.Snowflake')
                webhook_check = find['security_log_webhook']
                if webhook_check is not None:
                    exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                    if exist_check is not None:
                        await exist_check.edit(channel=webhook_channel_set)
                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'security_log_channel':log_channel.id}})
                    else:
                        webhooker=await log_channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                        await webhooker.edit(channel=webhook_channel_set)
                        collection.update_one({'_id':ctx.guild.id} ,{'$set':{'security_log_channel':log_channel.id , 'security_log_webhook':webhooker.id}})
                else:
                    webhooker=await log_channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                    await webhooker.edit(channel=webhook_channel_set)
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'security_log_channel':log_channel.id , 'security_log_webhook':webhooker.id}})

                
                return await ctx.send('changes done successfully')
            else:
                await ctx.send('enable security log first')
        else:
            await ctx.send('enable security first then Enable security log after that use this')

        # @commands.hybrid_command(name='automod_setup' , description='show all of the bad words that you entered')
        # @app_commands.guild_only()
        # @app_commands.checks.has_permissions(administrator=True)
        # @commands.has_permissions(administrator=True)
        # async def setup_automod(self,ctx):
        #     num=await ctx.guild.fetch_automod_rules()
        #     await ctx.guild.create_automod_rule(name='block harmful links' , event_type=discord.AutoModRuleEventType.message_send ,trigger=discord.AutoModTrigger(type=discord.AutoModRuleTriggerType.harmful_link) , actions=[discord.AutoModRuleAction(custom_message='a harmful linked you entered')] , enabled=True, reason ='haminjori')
        #     await ctx.send('done')

        return
    @commands.hybrid_command(name='remove_bad_words' , description='show all of the bad words that you entered')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def remove_bad_words(self,ctx,word:str):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id,"anti_bad_word":True})):
                bad_words = find['bad_words']
                word=word.lower()
                flag = False
                for i in bad_words:
                    if i.lower() == word:
                        bad_words.remove(i)
                        flag=True
                if flag == True:
                    collection.update_one({'_id':ctx.guild.id,"anti_bad_word":True} ,{'$set':{'bad_words':bad_words}})
                    await ctx.send('removed successfully')
                else:
                    await ctx.send('your word is not in your bad words')
                

            else:
                await ctx.send('make sure that you Enabled Security and Anti bad words then use this command')
        except:
            await ctx.send('something went wrong pls try again')

        return
    @commands.hybrid_command(name='show_bad_words' , description='show all of the bad words that you entered')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id,i.guild.id))
    async def show_bad_word(self,ctx):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id,"anti_bad_word":True})):
                bad_words = find['bad_words']
                text = ",".join(bad_words)
                embed=discord.Embed(
                title=f"all white list",
                description= f"bad words >.<: \n {text}",
                timestamp=datetime.now(),
                color= 0xFF7BFB
                )
                await ctx.send(embed=embed)
                
            else:
                await ctx.send('make sure that you Enabled Security and Anti bad words then use this command')
        except:
            await ctx.send('something went wrong pls try again')
            
        return
    @commands.hybrid_command(name='show_whitelist' , description='show optional whitelist')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id,i.guild.id))
    @app_commands.choices(choose_whitelist=[
        app_commands.Choice(name='all_white_list' , value=1),
        app_commands.Choice(name='anti_bad_words_whitelist' , value=2),
        app_commands.Choice(name='anti_spam_whitelist' , value=3),
        app_commands.Choice(name='anti_ban_whitelist' , value=4),
        app_commands.Choice(name='anti_kick_whitelist' , value=5),
        app_commands.Choice(name='anti_unban_whitelist' , value=6),
        app_commands.Choice(name='anti_timeout_whitelist' , value=7),
        app_commands.Choice(name='anti_emoji_whitelist' , value=8),
        app_commands.Choice(name='anti_server_change_whitelist' , value=9),
        app_commands.Choice(name='anti_prune_whitelist' , value=10),
        app_commands.Choice(name='bot_invite_whitelist' , value=11),
        app_commands.Choice(name='discord_invite_whitelist' , value=12),
        app_commands.Choice(name='channel_delete_whitelist' , value=13),
        app_commands.Choice(name='channel_create_whitelist' , value=14),
        app_commands.Choice(name='channel_update_whitelist' , value=15),
        app_commands.Choice(name='role_create_whitelist' , value=16),
        app_commands.Choice(name='role_update_whitelist' , value=17),
        app_commands.Choice(name='role_delete_whitelist' , value=18),
        
          ]) 
    async def show_whitelist(self,ctx , choose_whitelist:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if choose_whitelist.value ==1:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['all_white_list_role'] is not None:
                        for i in find['all_white_list_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['all_white_list_user'] is not None:
                        for j in find['all_white_list_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass

                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"all white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)

                if choose_whitelist.value ==2:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_bad_words_white_role'] is not None:
                        for i in find['anti_bad_words_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_bad_words_white_user'] is not None:
                        for j in find['anti_bad_words_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti bad words white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)

                if choose_whitelist.value ==3:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_spam_white_role'] is not None:
                        for i in find['anti_spam_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_spam_white_user'] is not None :
                        for j in find['anti_spam_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti spam white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)

                if choose_whitelist.value ==4:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_ban_white_role'] is not None:
                        for i in find['anti_ban_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_ban_white_user'] is not None:
                        for j in find['anti_ban_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti ban white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==5:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_kick_white_role'] is not None:
                        for i in find['anti_kick_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_kick_white_user'] is not None:
                        for j in find['anti_kick_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti kick white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)

                if choose_whitelist.value ==6:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_unban_white_role'] is not None:
                        for i in find['anti_unban_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_unban_white_user'] is not None:
                        for j in find['anti_unban_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti unban white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==7:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_timeout_white_role'] is not None:
                        for i in find['anti_timeout_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_timeout_white_user'] is not None:
                        for j in find['anti_timeout_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti timeout white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)

                if choose_whitelist.value ==8:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_emoji_white_role'] is not None:
                        for i in find['anti_emoji_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_emoji_white_user'] is not None:
                        for j in find['anti_emoji_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti timeout white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==9:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_server_change_white_role'] is not None:
                        for i in find['anti_server_change_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_server_change_white_user'] is not None:
                        for j in find['anti_server_change_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users)!=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti server change white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)

                if choose_whitelist.value ==10:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['anti_prune_white_role'] is not None:
                        for i in find['anti_prune_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['anti_prune_white_user'] is not None:
                        for j in find['anti_prune_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti prune white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)

                if choose_whitelist.value ==11:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['bot_invite_white_role'] is not None:
                        for i in find['bot_invite_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['bot_invite_white_user'] is not None:
                        for j in find['bot_invite_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti bot invite white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==12:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['discord_invite_white_role'] is not None:
                        for i in find['discord_invite_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['discord_invite_white_user'] is not None:
                        for j in find['discord_invite_white_user']:
                            try:    
                                
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"anti discord invite white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==13:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['channel_delete_white_role'] is not None:
                        for i in find['channel_delete_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['channel_delete_white_user'] is not None:
                        for j in find['channel_delete_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"channel delete white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==14:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['channel_create_white_role'] is not None:
                        for i in find['channel_create_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['channel_create_white_user'] is not None:
                        for j in find['channel_create_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"channel create white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==15:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['channel_update_white_role'] is not None:
                        for i in find['channel_update_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['channel_update_white_user'] is not None:
                        for j in find['channel_update_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users)!=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"channel update white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==16:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['role_create_white_role'] is not None:
                        for i in find['role_create_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['role_create_white_user'] is not None:
                        for j in find['role_create_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"role create white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)

                if choose_whitelist.value ==17:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['role_update_white_role'] is not None:
                        for i in find['role_update_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['role_update_white_user'] is not None:
                        for j in find['role_update_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles) !=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users) !=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"role update white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)


                if choose_whitelist.value ==18:
                    list_roles = []
                    list_users=[]
                    show_users=[]
                    show_roles=[]
                    if find['role_delete_white_role'] is not None:
                        for i in find['role_delete_white_role']:
                            try:
                                check_role=discord.utils.get(ctx.guild.roles , id=i)
                                if check_role is not None:
                                    list_roles.append(i)
                            except:
                                pass
                    if find['role_delete_white_user'] is not None:
                        for j in find['role_delete_white_user']:
                            try:    
                                check_member = discord.utils.get(ctx.guild.members , id=j)
                                if check_member is not None:
                                    list_users.append(j)
                            except:
                                pass
                        
                    if len(list_roles)!=0:
                        show_roles=[]
                        for i in list_roles:
                            user = '<@&' + str(i) + '>'
                            show_roles.append(user)

                    if len(list_users)!=0:
                        show_users=[]
                        for i in list_users:
                            user = '<@' + str(i) + '>'
                            show_users.append(user)
                    if show_users is not None or show_roles is not None:
                        embed=discord.Embed(
                                title=f"role delete white list",
                                description= f"roles : {show_roles}\nusers : {show_users}",
                                timestamp=datetime.now(),
                                color= 0xFF7BFB
                        )
                        await ctx.send(embed=embed)
            else:
                await ctx.send ('Enable Security First')
        except:
            await ctx.send('something went wrong pls try again')
                    # user = member.mention
                    # user = user.replace("<","")
                    # user = user.replace(">","")
                    # user = user.replace("@","")
        return
    @commands.hybrid_command(name='invite_security' , description='set invite related security Feature punishment')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @app_commands.choices(bot_invite_pnishment=[
        app_commands.Choice(name='Kick' , value=1),
        app_commands.Choice(name='Ban' , value=2)]) 
    async def invite_security(self,ctx , bot_invite_pnishment:app_commands.Choice[int] ,bot_invite_warn:int):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id,"bot_invite_ban_security":True})):
                bot_invite_warn = abs(bot_invite_warn)
                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'bot_invite_punishment':bot_invite_pnishment.name ,  'bot_invite_warn':bot_invite_warn}})
                await ctx.send('settings saved')
            else:
                await ctx.send('make sure that you Enabled Security and anti bot invite then use this command')
        except:
            await ctx.send('something went wrong pls try again')


        return
                    

        

async def setup(bot : Bot):
    await bot.add_cog(security(bot))
    