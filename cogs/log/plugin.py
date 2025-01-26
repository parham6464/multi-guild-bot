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
from antispam import AntiSpamHandler, Options
from antispam.enums import Library
from antispam.plugins import AntiSpamTracker
import asyncio
from .helper import help , anti_spam


cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["log"]
security = db["security"]
new_GUILD = db["guilds"]
welcome = db["welcome"]
fun= db["fun"]



class log(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.handler = AntiSpamHandler(self.bot , library=Library.DPY , options=Options(no_punish=True,message_duplicate_count=5))
        self.bot.tracker = AntiSpamTracker(self.bot.handler, 1)
        self.bot.handler.register_plugin(self.bot.tracker)


    @commands.hybrid_command(name='full_log_enable' , description='Enable log Feature')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def full_log_enable(self,ctx,state:bool):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            await ctx.defer()
            if state == True:
                if (find2:= collection.find_one({"state":True,"guild_id":ctx.guild.id})) is None:
                    collection.insert_one({'state':state , 'guild_id':ctx.guild.id})
                    collection.insert_one({"user_id":ctx.guild.id ,
                    "auto_log_creator":True ,
                    'category_id':None,
                    "guild_update_state":None,
                    'guild_update_webhook':None,
                    "member_decrease_state":None ,
                    "member_decrease_webhook":None,
                    'voice_update_state':None,
                    'voice_update_webhook':None,
                    "member_ban_state":None ,
                    'member_ban_webhook':None,
                    'member_kick_state':None,
                    'member_kick_webhook':None,
                    'member_join_state':None,
                    'member_join_webhook':None,
                    'message_delete_state':None,
                    'message_delete_webhook':None,
                    'message_edit_state':None,
                    'message_edit_webhook':None,
                    'member_update_state':None,
                    'member_update_webhook':None,
                    'nickname_state':None,
                    'nickname_webhook':None,
                    "member_unban_state":None ,
                    'member_unban_webhook':None,
                    "emoji_update_state":None ,
                    'emoji_update_webhook':None,
                    "role_create_state":None ,
                    'role_create_webhook':None, 
                    "role_delete_state":None , 
                    'role_delete_webhook':None,
                    "event_create_state":None ,
                    'event_create_webhook':None, 
                    "event_delete_state":None,
                    'event_delete_webhook':None,
                    "thread_create_state":None,
                    'thread_create_webhook':None,
                    "thread_delete_state":None , 
                    'thread_delete_webhook':None,
                    "thread_update_state":None ,
                    'thread_update_webhook':None,
                    "role_update_state":None,
                    'role_update_webhook':None,
                    "invite_create_state":None ,
                    'invite_create_webhook':None,
                    "channel_delete_state":None ,
                    'channel_delete_webhook':None,
                    "channel_create_state":None ,
                    'channel_create_webhook':None,
                    "channel_update_state":None,
                    'channel_update_webhook':None})
                    
                    await ctx.send('log channel enable successfully')
                else:
                    
                    await ctx.send('already enable')
            elif state == False:
                collection.delete_one({'state':True , 'guild_id':ctx.guild.id})
                collection.delete_one({'user_id':ctx.guild.id, "auto_log_creator":True})
                collection.delete_one({'user_id':ctx.guild.id, "full_log_state":True})
                
                await ctx.send('log channel disable successfully')
        except:
            await ctx.send('something went wrong pls try again')

        return     


    @commands.hybrid_command(name='disable_log_sections' , description='disable log sections like full log and auto log')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.has_permissions(administrator=True)
    @app_commands.choices(log_to_disable=[
        app_commands.Choice(name='auto log section' , value=1),
        app_commands.Choice(name='full log in one channel' , value=2)
    ])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def disable_log_sections(self,ctx , log_to_disable:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        await ctx.defer()
        embed=discord.Embed(title='AUTO LOG DISABLE' , description = 'the process will takes time pls be patient')
        msg = await ctx.send(embed=embed)
        try:    
            if log_to_disable.value ==1:
                if (find:= collection.find_one({"user_id":ctx.guild.id, "auto_log_creator":True})):
                    my_channels = []
                    certain_channels=[]
                    count = 0
                    for key in find.keys():
                        if count >=3:
                            tmpor=find[key]
                            if tmpor is not None:
                                my_channels.append(tmpor)
                        count+=1
                    if len(my_channels)!=0:
                        for i in ctx.guild.channels:
                            if i.id in my_channels:
                                checker = discord.utils.get(ctx.guild.channels , id = i.id)
                                if checker is not None:
                                    certain_channels.append(i.id)
                    else:
                        embed1=discord.Embed(title='WARNING' , description = 'there is no channel to disable log!')
                        await msg.edit(embed=embed1)
                        return
                    if len(certain_channels)!=0:
                        for i in certain_channels:
                            checker = discord.utils.get(ctx.guild.channels , id = i)
                            await asyncio.sleep(3)
                            await checker.delete()
                    else:
                        embed1=discord.Embed(title='WARNING' , description = 'there is no channel to disable log,maybe its deleted before!')
                        await msg.edit(embed=embed1)
                        return 

                    embed1=discord.Embed(title='DISABLE COMPLETE' , description = 'The process done sucessfully')
                    await msg.edit(embed=embed1)
                if log_to_disable.value ==2:
                    collection.update_one({"user_id":ctx.guild.id, "full_log_state":True} , {'$set':{'channel':None}})
                    embed1=discord.Embed(title='DISABLE COMPLETE' , description = 'The process done sucessfully')
                    await msg.edit(embed=embed1)

                    
            else:
                embed1=discord.Embed(title='WARNING' , description = 'its already disable')
                
        except:
            embed1=discord.Embed(title='ERROR' , description = 'something went wrong pls try again')
            await msg.edit(embed=embed1)

        return

    @commands.hybrid_command(name='auto_log_creator' , description='its will create automatically seprate channels for log')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 21600.0, key=lambda i: (i.guild.id))
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 21600, commands.BucketType.guild)
    async def auto_log_creator(self,ctx , roles_ids:Optional[Union[str,str]]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        await ctx.defer()
        embed=discord.Embed(title='AUTO LOG CREATION' , description = 'the process will takes time pls be patient')
        
        msg = await ctx.send(embed=embed)
        try:
            if (find2:= collection.find_one({"state":True,"guild_id":ctx.guild.id})):
                if (find:= collection.find_one({"user_id":ctx.guild.id, "auto_log_creator":True})):
                        guild = ctx.guild
                        member = ctx.author
                        overwrites = {
                            guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            member: discord.PermissionOverwrite(read_messages=True , send_messages=True),
                        }
                        category=''
                        tmp_category=find['category_id']
                        if tmp_category is not None:
                            checker = discord.utils.get(ctx.guild.channels , id= tmp_category)
                            if checker is not None:
                                category=checker
                            else:
                                category=await ctx.guild.create_category('﴿━━⟅ 𝙻 𝙾 𝙶 ⟆━━﴾' , overwrites=overwrites)
                                collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"category_id":category.id}})
                        else:
                            category=await ctx.guild.create_category('﴿━━⟅ 𝙻 𝙾 𝙶 ⟆━━﴾' , overwrites=overwrites)
                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"category_id":category.id}})

                        if roles_ids is not None:
                            roles_ids = list(roles_ids.split(','))
                            for i in roles_ids:
                                i = int(i)
                                checker = discord.utils.get(ctx.guild.roles, id=i)
                                if checker is not None:
                                    await category.set_permissions(checker , read_messages=True , send_messages=True)


                        
                        channel_names = ['『📥』ᴍᴇᴍʙᴇʀ-ᴊᴏɪɴ','『📤』ᴍᴇᴍʙᴇʀ-ʟᴇꜰᴛ' , '『🖐』ᴊʟ-ᴠᴏɪᴄᴇ' , '『📩』ɪɴᴠɪᴛᴇ','『⛔』ᴋɪᴄᴋ' , '『⛔』ʙᴀɴ' , '『⛔』ᴜɴʙᴀɴ' ,'『📨』ᴍᴇssᴀɢᴇ-ᴅᴇʟᴇᴛᴇ','『🖋』ᴍᴇssᴀɢᴇ-ᴇᴅɪᴛ','『📍』ᴍᴇᴍʙᴇʀ-ᴜᴘᴅᴀᴛᴇ','『🎫』ɴɪᴄᴋɴᴀᴍᴇ-ʟᴏɢ' , '『✅』ᴄʜᴀɴɴᴇʟ-ᴄʀᴇᴀᴛᴇ' , '『📊』ᴄʜᴀɴɴᴇʟ-ᴜᴘᴅᴀᴛᴇ' , '『❎』ᴄʜᴀɴɴᴇʟ-ᴅᴇʟᴇᴛᴇ' , '『➕』ʀᴏʟᴇ-ᴄʀᴇᴀᴛᴇ' , '『🔃』ʀᴏʟᴇ-ᴜᴘᴅᴀᴛᴇ' , '『❎』ʀᴏʟᴇ-ᴅᴇʟᴇᴛᴇ' ,'『🔐』sᴇʀᴠᴇʀ-ᴄʜᴀɴɢᴇ' , '『✅』ᴇᴠᴇɴᴛ-ᴄʀᴇᴀᴛᴇ' ,'『❎』ᴇᴠᴇɴᴛ-ᴅᴇʟᴇᴛᴇ' , '『🔃』ᴇᴍᴏᴊɪ-ᴜᴘᴅᴀᴛᴇ' , '『✅』ᴛʜʀᴇᴀᴅ-ᴄʀᴇᴀᴛᴇ' , '『❎』ᴛʜʀᴇᴀᴅ-ᴅᴇʟᴇᴛᴇ' , '『🔃』ᴛʜʀᴇᴀᴅ-ᴜᴘᴅᴀᴛᴇ']
                        member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
                        webhook_avatar =member1.display_avatar
                        profile_webhook= await webhook_avatar.read()
                        for i in channel_names:
                            await asyncio.sleep(3)
                            if i == '『📥』ᴍᴇᴍʙᴇʀ-ᴊᴏɪɴ':
                                flag=False
                                tmp_channel = find['member_join_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['member_join_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'member_join_webhook':webhooker.id}})
                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True

                                if flag==True:
                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['member_join_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_join_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_join_state":channel.id , 'member_join_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_join_state":channel.id , 'member_join_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『📤』ᴍᴇᴍʙᴇʀ-ʟᴇꜰᴛ':
                                flag=False
                                tmp_channel = find['member_decrease_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['member_decrease_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'member_decrease_webhook':webhooker.id}})
                                        flag=False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:
                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['member_decrease_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_decrease_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_decrease_state":channel.id , 'member_decrease_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_decrease_state":channel.id , 'member_decrease_webhook':webhooker.id}})

                                    #############################################################
                                
                            elif i == '『🖐』ᴊʟ-ᴠᴏɪᴄᴇ':
                                flag =False
                                tmp_channel = find['voice_update_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['voice_update_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'voice_update_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:
                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['voice_update_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"voice_update_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"voice_update_state":channel.id , 'voice_update_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"voice_update_state":channel.id , 'voice_update_webhook':webhooker.id}})

                                    #############################################################


                            elif i == '『📩』ɪɴᴠɪᴛᴇ':
                                flag= False
                                tmp_channel = find['invite_create_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['invite_create_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'invite_create_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['invite_create_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"invite_create_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"invite_create_state":channel.id , 'invite_create_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"invite_create_state":channel.id , 'invite_create_webhook':webhooker.id}})

                                    #############################################################
                            elif i == '『⛔』ᴋɪᴄᴋ':
                                flag= False
                                tmp_channel = find['member_kick_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['member_kick_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'member_kick_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['member_kick_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_kick_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_kick_state":channel.id , 'member_kick_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_kick_state":channel.id , 'member_kick_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『⛔』ʙᴀɴ':
                                flag=False
                                tmp_channel = find['member_ban_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['member_ban_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'member_ban_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['member_ban_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_ban_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_ban_state":channel.id , 'member_ban_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_ban_state":channel.id , 'member_ban_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『⛔』ᴜɴʙᴀɴ':
                                flag= False
                                tmp_channel = find['member_unban_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['member_unban_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'member_unban_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:
                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['member_unban_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_unban_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_unban_state":channel.id , 'member_unban_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_unban_state":channel.id , 'member_unban_webhook':webhooker.id}})

                                    #############################################################
                            elif i == '『📨』ᴍᴇssᴀɢᴇ-ᴅᴇʟᴇᴛᴇ':
                                flag= False
                                tmp_channel = find['message_delete_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['message_delete_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'message_delete_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['message_delete_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"message_delete_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"message_delete_state":channel.id , 'message_delete_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"message_delete_state":channel.id , 'message_delete_webhook':webhooker.id}})

                                    #############################################################
                            elif i == '『🖋』ᴍᴇssᴀɢᴇ-ᴇᴅɪᴛ':
                                flag=False
                                tmp_channel = find['message_edit_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['message_edit_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'message_edit_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['message_edit_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"message_edit_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"message_edit_state":channel.id , 'message_edit_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"message_edit_state":channel.id , 'message_edit_webhook':webhooker.id}})

                                    #############################################################
                            elif i == '『📍』ᴍᴇᴍʙᴇʀ-ᴜᴘᴅᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['member_update_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['member_update_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'member_update_webhook':webhooker.id}})


                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['member_update_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_update_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_update_state":channel.id , 'member_update_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"member_update_state":channel.id , 'member_update_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『🎫』ɴɪᴄᴋɴᴀᴍᴇ-ʟᴏɢ':
                                flag=False
                                tmp_channel = find['nickname_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['nickname_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'nickname_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['nickname_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"nickname_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"nickname_state":channel.id , 'nickname_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"nickname_state":channel.id , 'nickname_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『✅』ᴄʜᴀɴɴᴇʟ-ᴄʀᴇᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['channel_create_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['channel_create_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'channel_create_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['channel_create_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_create_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_create_state":channel.id , 'channel_create_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_create_state":channel.id , 'channel_create_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『📊』ᴄʜᴀɴɴᴇʟ-ᴜᴘᴅᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['channel_update_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['channel_update_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'channel_update_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['channel_update_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_update_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_update_state":channel.id , 'channel_update_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_update_state":channel.id , 'channel_update_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『❎』ᴄʜᴀɴɴᴇʟ-ᴅᴇʟᴇᴛᴇ':
                                flag=False
                                tmp_channel = find['channel_delete_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['channel_delete_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'channel_delete_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['channel_delete_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_delete_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_delete_state":channel.id , 'channel_delete_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"channel_delete_state":channel.id , 'channel_delete_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『➕』ʀᴏʟᴇ-ᴄʀᴇᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['role_create_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['role_create_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'role_create_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['role_create_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_create_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_create_state":channel.id , 'role_create_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_create_state":channel.id , 'role_create_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『🔃』ʀᴏʟᴇ-ᴜᴘᴅᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['role_update_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['role_update_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'role_update_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:
                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['role_update_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_update_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_update_state":channel.id , 'role_update_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_update_state":channel.id , 'role_update_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『❎』ʀᴏʟᴇ-ᴅᴇʟᴇᴛᴇ':
                                flag=False
                                tmp_channel = find['role_delete_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['role_delete_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'role_delete_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['role_delete_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_delete_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_delete_state":channel.id , 'role_delete_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"role_delete_state":channel.id , 'role_delete_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『🔐』sᴇʀᴠᴇʀ-ᴄʜᴀɴɢᴇ':
                                flag=False
                                tmp_channel = find['guild_update_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['guild_update_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'guild_update_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:
                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['guild_update_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"guild_update_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"guild_update_state":channel.id , 'guild_update_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"guild_update_state":channel.id , 'guild_update_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『✅』ᴇᴠᴇɴᴛ-ᴄʀᴇᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['event_create_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['event_create_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'event_create_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['event_create_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"event_create_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"event_create_state":channel.id , 'event_create_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"event_create_state":channel.id , 'event_create_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『❎』ᴇᴠᴇɴᴛ-ᴅᴇʟᴇᴛᴇ':
                                flag=False
                                tmp_channel = find['event_delete_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['event_delete_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'event_delete_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['event_delete_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"event_delete_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"event_delete_state":channel.id , 'event_delete_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"event_delete_state":channel.id , 'event_delete_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『🔃』ᴇᴍᴏᴊɪ-ᴜᴘᴅᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['emoji_update_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['emoji_update_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'emoji_update_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:
                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['emoji_update_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"emoji_update_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"emoji_update_state":channel.id , 'emoji_update_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"emoji_update_state":channel.id , 'emoji_update_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『✅』ᴛʜʀᴇᴀᴅ-ᴄʀᴇᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['thread_create_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['thread_create_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'thread_create_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['thread_create_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_create_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_create_state":channel.id , 'thread_create_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_create_state":channel.id , 'thread_create_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『❎』ᴛʜʀᴇᴀᴅ-ᴅᴇʟᴇᴛᴇ':
                                flag=False
                                tmp_channel = find['thread_delete_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['thread_delete_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'thread_delete_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['thread_delete_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_delete_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_delete_state":channel.id , 'thread_delete_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_delete_state":channel.id , 'thread_delete_webhook':webhooker.id}})

                                    #############################################################

                            elif i == '『🔃』ᴛʜʀᴇᴀᴅ-ᴜᴘᴅᴀᴛᴇ':
                                flag=False
                                tmp_channel = find['thread_update_state']
                                if tmp_channel is not None:
                                    checker = discord.utils.get(ctx.guild.channels , id= tmp_channel)
                                    if checker is not None:
                                        webhook_channel_set=discord.Object(tmp_channel , type='abc.Snowflake')
                                        webhook_check = find['thread_update_webhook']
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                        else:
                                            webhooker=await checker.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{'thread_update_webhook':webhooker.id}})

                                        flag= False
                                    else:
                                        flag=True
                                else:
                                    flag=True
                                if flag==True:

                                    channel=await ctx.guild.create_text_channel(i, overwrites=overwrites , category=category)
                                    await channel.edit(sync_permissions=True)
                                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                                    #################webhook setting##########################
                                    webhook_check = find['thread_update_webhook']
                                    if webhook_check is not None:
                                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                                        if exist_check is not None:
                                            await exist_check.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_update_state":channel.id}})
                                        else:
                                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                            await webhooker.edit(channel=webhook_channel_set)
                                            collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_update_state":channel.id , 'thread_update_webhook':webhooker.id}})
                                    else:
                                        webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                                        await webhooker.edit(channel=webhook_channel_set)
                                        collection.update_one({'user_id':ctx.guild.id , "auto_log_creator":True } , {"$set":{"thread_update_state":channel.id , 'thread_update_webhook':webhooker.id}})

                                    #############################################################
                                embed1=discord.Embed(title='AUTO LOG COMPLETE' , description = 'The process done sucessfully')
                                await msg.edit(embed=embed1)

                    
                else:
                    embed1=discord.Embed(title='WARNING' , description = 'enable full_log_enable command then use this command')
                    await msg.edit(embed=embed1)  
            else:
                embed1=discord.Embed(title='WARNING' , description = 'enable full_log_enable command then use this command')
                await msg.edit(embed=embed1)
        except:
            embed1=discord.Embed(title='ERROR' , description = 'something went wrong pls try again')
            await msg.edit(embed=embed1)
                
        return

        


    @commands.hybrid_command(name='full_log_set' , description='will set a single channel for all logs')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3600.0, key=lambda i: (i.guild.id))
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3600, commands.BucketType.guild)
    async def full_log_set(self,ctx,channel:discord.TextChannel):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
        webhook_avatar =member1.display_avatar
        profile_webhook= await webhook_avatar.read()
        await ctx.defer()
        try:
            if (find2:= collection.find_one({"state":True,"guild_id":ctx.guild.id})):
                if (find:= collection.find_one({"user_id":ctx.guild.id, "full_log_state":True})):
                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                    webhook_check = find['full_log_webhook']
                    if webhook_check is not None:
                        exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                        if exist_check is not None:
                            await exist_check.edit(channel=webhook_channel_set)
                            collection.update_one({"user_id":ctx.guild.id, "full_log_state":True},{"$set":{"channel":channel.id,'full_log_webhook':channel.id}} )
                        else:
                            webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                            await webhooker.edit(channel=webhook_channel_set)
                            collection.update_one({"user_id":ctx.guild.id, "full_log_state":True},{"$set":{"channel":channel.id,'full_log_webhook':channel.id}} )

                    
                    return await ctx.send('changes done successfully')
            else:
                return await ctx.send('enable full log enable first then use this command')
            if (find2:= collection.find_one({"state":True,"guild_id":ctx.guild.id })):
                    webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
                    webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                    await webhooker.edit(channel=webhook_channel_set)
                    collection.insert_one({'user_id':ctx.guild.id , "channel":channel.id , "full_log_state":True , 'full_log_webhook':channel.id})
                    await ctx.send("Log Feature Enabled successfully ")

                        
        except:
            return await ctx.send('something went wrong')

        return
    @commands.Cog.listener()  #channel delete log
    async def on_guild_channel_delete(self,channel):
        try:
            if (find1:= security.find_one({"_id":channel.guild.id})):
                if find1['state']==1 and find1['channel_delete_warn_limit'] is not None and find1['channel_delete_enable'] == True:
                    async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete , limit=1):
                        async for entry2 in channel.guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:

                                member = discord.utils.get(channel.guild.members , id = entry.user.id)
                                if member.id == channel.guild.me.id:
                                    pass
                                elif member.id == channel.guild.owner_id:
                                    pass
                                if channel.guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:

                                    roles = find1['channel_delete_white_role']
                                    user_ids = find1['channel_delete_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True


                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['channel_delete_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti channel delete Log",
                                                        description= f"user Action : delete channel\nwarn limit : {find1['channel_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_delete_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        
                                                        await exist_check.send(embed=embed)
                                                if find1['channel_delete_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await channel.guild.kick(ss,reason='delete a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                                elif find1['channel_delete_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await channel.guild.ban(ss,reason='delete a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['channel_delete_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:                                                
                                                            embed=discord.Embed(
                                                            title=f"Anti channel delete Log",
                                                            description= f"user Action : delete channel\nwarn limit : {find1['channel_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_delete_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['channel_delete_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await channel.guild.kick(ss,reason='delete a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                                    elif find1['channel_delete_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await channel.guild.ban(ss,reason='delete a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"channel_delete":True, "guild":channel.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel delete Log",
                                                            description= f"user Action : delete channel\nwarn limit : {find1['channel_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":channel.guild.id, "channel_delete":True , "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                            warn=find2['warn']
                                            if warn == find1['channel_delete_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti channel delete Log",
                                                        description= f"user Action : delete channel\nwarn limit : {find1['channel_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_delete_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        
                                                        await exist_check.send(embed=embed)

                                                if find1['channel_delete_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await channel.guild.kick(ss,reason='delete a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                                elif find1['channel_delete_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await channel.guild.ban(ss,reason='delete a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['channel_delete_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel delete Log",
                                                            description= f"user Action : delete channel\nwarn limit : {find1['channel_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_delete_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            
                                                            await exist_check.send(embed=embed)

                                                    if find1['channel_delete_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await channel.guild.kick(ss,reason='delete a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                                    elif find1['channel_delete_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await channel.guild.ban(ss,reason='delete a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_delete":True, "guild":channel.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"channel_delete":True, "guild":channel.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel delete Log",
                                                            description= f"user Action : delete channel\nwarn limit : {find1['channel_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await channel_sender.send(embed=embed)

        except:
            pass
        try:
            if (find:= collection.find_one({"user_id":channel.guild.id , 'auto_log_creator':True})):
                async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete , limit=1):
                    member = discord.utils.get(channel.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['channel_delete_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Channel Deletion Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Channel Delete')
                        embed.add_field(name=f'CHANNEL TYPE:', value=f'{channel.type}')
                        embed.add_field(name=f'CHANNEL NAME:', value=f'{channel.name}')
                        embed.add_field(name=f'DELETE BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" , inline=False )
                        embed.add_field(name=f'ID:' , value=f"```CHANNEL: {channel.id}\nUSER: {member.id}```" )
                        
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":channel.guild.id , 'full_log_state':True})):
                async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete , limit=1):
                    member = discord.utils.get(channel.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Channel Deletion Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Channel Delete')
                        embed.add_field(name=f'CHANNEL TYPE:', value=f'{channel.type}')
                        embed.add_field(name=f'CHANNEL NAME:', value=f'{channel.name}')
                        embed.add_field(name=f'DELETE BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" , inline=False )
                        embed.add_field(name=f'ID:' , value=f"```CHANNEL: {channel.id}\nUSER: {member.id}```" )
                        
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        if channel_check is not None:
                            await webhooker.send(embed=embed)

        except:

            return
        
        return

    @commands.Cog.listener()  #channel create
    async def on_guild_channel_create(self,channel):
        try:
            if (find1:= security.find_one({"_id":channel.guild.id})):
                if find1['state']==1 and find1['channel_create_warn_limit'] is not None and find1['channel_create_enable'] == True:
                    async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create , limit=1):
                        async for entry2 in channel.guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                member = discord.utils.get(channel.guild.members , id = entry.user.id)
                                if member.id == channel.guild.me.id:
                                    pass
                                elif member.id == channel.guild.owner_id:
                                    pass
                                if channel.guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:

                                    roles = find1['channel_create_white_role']
                                    user_ids = find1['channel_create_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True


                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['channel_create_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti channel create Log",
                                                        description= f"user Action : create channel\nwarn limit : {find1['channel_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_create_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['channel_create_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await channel.guild.kick(ss,reason='delete a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                                elif find1['channel_create_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await channel.guild.ban(ss,reason='delete a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['channel_create_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel create Log",
                                                            description= f"user Action : create channel\nwarn limit : {find1['channel_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_create_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['channel_create_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await channel.guild.kick(ss,reason='delete a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                                    elif find1['channel_create_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await channel.guild.ban(ss,reason='delete a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"channel_create":True, "guild":channel.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel create Log",
                                                            description= f"user Action : create channel\nwarn limit : {find1['channel_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":channel.guild.id, "channel_create":True , "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                            warn=find2['warn']
                                            if warn == find1['channel_create_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti channel create Log",
                                                        description= f"user Action : create channel\nwarn limit : {find1['channel_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_create_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['channel_create_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await channel.guild.kick(ss,reason='delete a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                                elif find1['channel_create_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await channel.guild.ban(ss,reason='delete a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['channel_create_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel create Log",
                                                            description= f"user Action : create channel\nwarn limit : {find1['channel_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_create_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['channel_create_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await channel.guild.kick(ss,reason='delete a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                                    elif find1['channel_create_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await channel.guild.ban(ss,reason='delete a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_create":True, "guild":channel.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"channel_create":True, "guild":channel.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel create Log",
                                                            description= f"user Action : create channel\nwarn limit : {find1['channel_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

        except:
            pass
        try:
            if (find:= collection.find_one({"user_id":channel.guild.id , 'auto_log_creator':True})):
                async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create , limit=1):
                    member = discord.utils.get(channel.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['channel_create_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['channel_create_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Channel Creation Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Channel Create')
                        embed.add_field(name=f'CHANNEL TYPE:', value=f'{channel.type}')
                        embed.add_field(name=f'CHANNEL NAME:', value=f'{channel.mention}')
                        embed.add_field(name=f'Created BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" , inline=False )
                        embed.add_field(name=f'ID:' , value=f"```CHANNEL: {channel.id}\nUSER: {member.id}```" )
                        
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":channel.guild.id , 'full_log_state':True})):
                async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create , limit=1):
                    member = discord.utils.get(channel.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Channel Creation Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Channel Create')
                        embed.add_field(name=f'CHANNEL TYPE:', value=f'{channel.type}')
                        embed.add_field(name=f'CHANNEL NAME:', value=f'{channel.mention}')
                        embed.add_field(name=f'Created BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" , inline=False )
                        embed.add_field(name=f'ID:' , value=f"```CHANNEL: {channel.id}\nUSER: {member.id}```" )
                        
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        if tmp_id_channel is not None:
                            await webhooker.send(embed=embed)

        except:

            return

        return
    @commands.Cog.listener()
    async def on_guild_update(self,before, after):
        try:
            if (find1:= security.find_one({"_id":after.id})):

                if find1['state']==1 and find1['anti_server_change_warn'] is not None and find1['anti_server_change'] == True:
                    async for entry in after.audit_logs(action=discord.AuditLogAction.guild_update , limit=1):
                        async for entry2 in after.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                member = discord.utils.get(after.members , id = entry.user.id)
                                roles = find1['anti_server_change_white_role']
                                user_ids = find1['anti_server_change_white_user']
                                if member.id == after.me.id:
                                    pass
                                elif member.id == after.owner_id:
                                    pass
                                elif after.me.top_role.position <= member.top_role.position:
                                    pass
                                else:
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True    

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True

                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['anti_server_change_warn']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await after.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                            title=f"Anti server change Log",
                                                            description= f"user Action : Change server settings\nwarn limit : {find1['anti_server_change_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_server_change_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)
                                                if find1['anti_server_change_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await after.kick(ss , reason='changing server settings')
                                                    security.delete_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})
                                                elif find1['anti_server_change_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await after.ban(ss , reason='changing server settings')
                                                    security.delete_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})
                                            else:
                                                warn +=1
                                                if warn == find1['anti_server_change_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await after.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti server change Log",
                                                            description= f"user Action : Change server settings\nwarn limit : {find1['anti_server_change_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_server_change_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
                                                    if find1['anti_server_change_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await after.kick(ss, reason='changing server settings')
                                                        security.delete_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})
                                                    elif find1['anti_server_change_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await after.ban(ss, reason='changing server settings')
                                                        security.delete_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"anti_sv_change":True , "guild":after.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await after.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti server change Log",
                                                            description= f"user Action : Change server settings\nwarn limit : {find1['anti_server_change_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({"user_id":entry.user.id, "guild":after.id , "anti_sv_change":True, "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id, "anti_sv_change":True, "guild":after.id})
                                            warn=find2['warn']
                                            if warn == find1['anti_server_change_warn']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await after.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                            title=f"Anti server change Log",
                                                            description= f"user Action : Change server settings\nwarn limit : {find1['anti_server_change_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_server_change_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)
                                                if find1['anti_server_change_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await after.kick(ss, reason='changing server settings')
                                                    security.delete_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})
                                                elif find1['anti_server_change_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await after.ban(ss, reason='changing server settings')
                                                    security.delete_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})
                                            else:
                                                warn +=1
                                                if warn == find1['anti_server_change_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await after.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti server change Log",
                                                                description= f"user Action : Change server settings\nwarn limit : {find1['anti_server_change_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_server_change_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
                                                    if find1['anti_server_change_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await after.kick(ss, reason='changing server settings')
                                                        security.delete_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})
                                                    elif find1['anti_server_change_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await after.ban(ss, reason='changing server settings')
                                                        security.delete_one({"user_id":entry.user.id,"anti_sv_change":True,"guild":after.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"anti_sv_change":True , "guild":after.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await after.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti server change Log",
                                                            description= f"user Action : Change server settings\nwarn limit : {find1['anti_server_change_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
        except:
            pass
        try:
            if (find:= collection.find_one({"user_id":after.id, 'auto_log_creator':True})):
                async for entry in after.audit_logs(action=discord.AuditLogAction.guild_update , limit=1):
                    member = discord.utils.get(after.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['guild_update_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['guild_update_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Server Update Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Server Update')
                        embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                        if before.afk_channel != after.afk_channel:
                            embed.add_field(name=f'AFK CHANNEL' , value=f"Changed From {before.afk_channel.name} --> {after.afk_channel.name}" , inline=False)
                        if before.afk_timeout != after.afk_timeout:
                            embed.add_field(name=f'AFK TIMEOUT' , value=f"Changed From {before.afk_timeout} --> {after.afk_timeout}" , inline=False)
                        if before.banner != after.banner:
                            embed.add_field(name=f'SERVER BANNER' , value=f"Server banner changed" , inline=False)
                        if before.bitrate_limit != after.bitrate_limit:
                            embed.add_field(name=f'SERVER BITRATE' , value=f"Changed to {after.bitrate_limit}" , inline=False)
                        if before.name != after.name:
                            embed.add_field(name=f'SERVER NAME' , value=f"Changed From {before.name} --> {after.name}" , inline=False)

                        embed.add_field(name=f'ID:' , value=f"```SERVER: {after.id}\nUSER: {member.id}```", inline=False )
                        embed.set_thumbnail(url=member.display_avatar.url)
                        
                        
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":after.id, 'full_log_state':True})):
                async for entry in after.audit_logs(action=discord.AuditLogAction.guild_update , limit=1):
                    member = discord.utils.get(after.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Server Update Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Server Update')
                        embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                        if before.afk_channel != after.afk_channel:
                            embed.add_field(name=f'AFK CHANNEL' , value=f"Changed From {before.afk_channel.name} --> {after.afk_channel.name}" , inline=False)
                        if before.afk_timeout != after.afk_timeout:
                            embed.add_field(name=f'AFK TIMEOUT' , value=f"Changed From {before.afk_timeout} --> {after.afk_timeout}" , inline=False)
                        if before.banner != after.banner:
                            embed.add_field(name=f'SERVER BANNER' , value=f"Server banner changed" , inline=False)
                        if before.bitrate_limit != after.bitrate_limit:
                            embed.add_field(name=f'SERVER BITRATE' , value=f"Changed to {after.bitrate_limit}" , inline=False)
                        if before.name != after.name:
                            embed.add_field(name=f'SERVER NAME' , value=f"Changed From {before.name} --> {after.name}" , inline=False)

                        embed.add_field(name=f'ID:' , value=f"```SERVER: {after.id}\nUSER: {member.id}```", inline=False )
                        embed.set_thumbnail(url=member.display_avatar.url)
                        
                        
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        if tmp_id_channel is not None:
                            await webhooker.send(embed=embed)
        except:
            pass

        return
    @commands.Cog.listener()
    async def on_audit_log_entry_create(self,enry):
        
        try:
            if (find1:= security.find_one({"_id":enry.guild.id})):
                if find1['state']==1 and find1['anti_prune_warn'] is not None and find1['anti_prune'] == True:
                    async for entry in enry.guild.audit_logs(action=discord.AuditLogAction.member_prune , limit=1):
                        async for entry2 in enry.guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id==entry2.user.id:
                                member = discord.utils.get(enry.guild.members , id = entry.user.id)
                                if member.id == enry.guild.me.id:
                                    pass
                                elif member.id == enry.guild.owner_id:
                                    pass
                                elif enry.guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:
                                    roles = find1['anti_prune_white_role']
                                    user_ids = find1['anti_prune_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True
                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True

                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['anti_prune_warn']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await enry.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                            title=f"Anti Prune Log",
                                                            description= f"user Action : Activate server prune\nwarn limit : {find1['anti_prune_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_prune_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['anti_prune_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await enry.guild.kick(ss , reason='prune server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})
                                                elif find1['anti_prune_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await enry.guild.ban(ss, reason='prune server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['anti_prune_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await enry.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Prune Log",
                                                                description= f"user Action : Activate server prune\nwarn limit : {find1['anti_prune_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_prune_punishment']}",
                                                                timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_prune_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await enry.guild.kick(ss, reason='prune server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})
                                                    elif find1['anti_prune_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await enry.guild.ban(ss, reason='prune server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"anti_prune_user":True,"guild":enry.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await enry.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti Prune Log",
                                                            description= f"user Action : Activate server prune\nwarn limit : {find1['anti_prune_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":enry.guild.id , "anti_prune_user":True, "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id, "anti_prune_user":True, "guild":enry.guild.id})
                                            warn=find2['warn']
                                            if warn == find1['anti_prune_warn']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await enry.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                            title=f"Anti Prune Log",
                                                            description= f"user Action : Activate server prune\nwarn limit : {find1['anti_prune_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_prune_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)
                                                if find1['anti_prune_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await enry.guild.kick(ss, reason='prune server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})
                                                elif find1['anti_prune_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await enry.guild.ban(ss, reason='prune server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['anti_prune_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await enry.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Prune Log",
                                                                description= f"user Action : Activate server prune\nwarn limit : {find1['anti_prune_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_prune_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
                                                    if find1['anti_prune_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await enry.guild.kick(ss, reason='prune server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})
                                                    elif find1['anti_prune_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await enry.guild.ban(ss, reason='prune server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_prune_user":True,"guild":enry.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"anti_prune_user":True , "guild":enry.guild.id} , {'$set':{'warn':warn}})  
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await enry.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti Prune Log",
                                                            description= f"user Action : Activate server prune\nwarn limit : {find1['anti_prune_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
                    
        except:
            pass

        return

    @commands.Cog.listener()  #anti timeout
    async def on_member_update(self,before, after):
        try:
            if (find1:= security.find_one({"_id":after.guild.id})):
                checker=after.is_timed_out()
                checker_first = before.is_timed_out()
                if checker_first == False and checker == True:  
                    if find1['state']==1 and find1['anti_timeout_warn'] is not None and find1['anti_timeout'] == True:
                        async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_update , limit=1):
                            async for entry2 in after.guild.audit_logs(limit=1):
                                if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                    member = discord.utils.get(after.guild.members , id = entry.user.id)
                                    if member.id == after.guild.me.id:
                                        pass
                                    elif member.id == after.guild.owner_id:
                                        pass
                                    elif after.guild.me.top_role.position <= member.top_role.position:
                                        pass
                                    else:
                                        roles = find1['anti_timeout_white_role']
                                        user_ids = find1['anti_timeout_white_user']
                                        check_white_role=False
                                        check_white_user=False
                                        if roles is not None:
                                            for i in roles:
                                                for j in range(len(member.roles)):
                                                    if i == member.roles[j].id:
                                                        check_white_role = True
                                        if user_ids is not None:
                                            for i in user_ids:
                                                if i == member.id:
                                                    check_white_user = True
                                        all_white_roles = find1['all_white_list_role']
                                        all_white_users = find1['all_white_list_user']

                                        if all_white_roles is not None:
                                            for i in all_white_roles:
                                                for j in range(len(member.roles)):
                                                    if i == member.roles[j].id:
                                                        check_white_role = True

                                        if all_white_users is not None:
                                            for i in all_white_users:
                                                if i == member.id:
                                                    check_white_user = True

                                        if check_white_role == True or check_white_user == True:
                                            check_white_user = False
                                            check_white_role = False
                                        else:

                                            if (find2:= security.find_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})) is not None:
                                                warn=find2['warn']
                                                if warn == find1['anti_timeout_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await after.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Timeout Log",
                                                                description= f"user Action : Timeout a user\nwarn limit : {find1['anti_timeout_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_timeout_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_timeout_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await after.guild.kick(ss , reason='timeout a user')
                                                        security.delete_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})
                                                    elif find1['anti_timeout_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await after.guild.ban(ss, reason='timeout a user')
                                                        security.delete_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})
                                                else:
                                                    warn +=1
                                                    if warn == find1['anti_timeout_warn']:
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await after.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                    title=f"Anti Timeout Log",
                                                                    description= f"user Action : Timeout a user\nwarn limit : {find1['anti_timeout_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_timeout_punishment']}",
                                                                    timestamp=datetime.now(),
                                                                        color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)

                                                        if find1['anti_timeout_punishment']=='Kick':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await after.guild.kick(ss, reason='timeout a user')
                                                            security.delete_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})
                                                        elif find1['anti_timeout_punishment']=='Ban':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await after.guild.ban(ss, reason='timeout a user')
                                                            security.delete_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})
                                                        
                                                    else:
                                                        security.update_one({'user_id':entry.user.id,"anti_timeout_user":True,"guild":after.guild.id} , {'$set':{'warn':warn}})
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await after.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                title=f"Anti Timeout Log",
                                                                description= f"user Action : Timeout a user\nwarn limit : {find1['anti_timeout_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)

                                            else:
                                                security.insert_one({'user_id':entry.user.id , "guild":after.guild.id , "anti_timeout_user":True, "warn":0})
                                                find2= security.find_one({"user_id":entry.user.id, "anti_timeout_user":True, "guild":after.guild.id})
                                                warn=find2['warn']
                                                if warn == find1['anti_timeout_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await after.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Timeout Log",
                                                                description= f"user Action : Timeout a user\nwarn limit : {find1['anti_timeout_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_timeout_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
                                                    if find1['anti_timeout_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await after.guild.kick(ss, reason='timeout a user')
                                                        security.delete_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})
                                                    elif find1['anti_timeout_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await after.guild.ban(ss, reason='timeout a user')
                                                        security.delete_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})
                                                else:
                                                    warn +=1
                                                    if warn == find1['anti_timeout_warn']:
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await after.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                    title=f"Anti Timeout Log",
                                                                    description= f"user Action : Timeout a user\nwarn limit : {find1['anti_timeout_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_timeout_punishment']}",
                                                                    timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)
                                                        if find1['anti_timeout_punishment']=='Kick':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await after.guild.kick(ss, reason='timeout a user')
                                                            security.delete_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})
                                                        elif find1['anti_timeout_punishment']=='Ban':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await after.guild.ban(ss, reason='timeout a user')
                                                            security.delete_one({"user_id":entry.user.id,"anti_timeout_user":True,"guild":after.guild.id})
                                                        
                                                    else:
                                                        security.update_one({'user_id':entry.user.id,"anti_timeout_user":True , "guild":after.guild.id} , {'$set':{'warn':warn}})  
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await after.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                title=f"Anti Timeout Log",
                                                                description= f"user Action : Timeout a user\nwarn limit : {find1['anti_timeout_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)
        except:
            pass  
        try:
            if (find:= collection.find_one({"user_id":after.guild.id , 'auto_log_creator':True})):
                async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_update , limit=1):
                    async for entry2 in after.guild.audit_logs(limit=1):
                        if entry.action == entry2.action:
                            tmp_guild = find['user_id']
                            main_guild=self.bot.get_guild(tmp_guild)
                            member = discord.utils.get(main_guild.members , id = entry.user.id)
                            webhooker_id = find['member_update_webhook']
                            webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                            if webhooker is not None:
                                embed=discord.Embed(
                                        title=f"Member Update Log",
                                        timestamp=datetime.now(),
                                        color= 0xF6F6F6
                                )
                                if before.is_timed_out() == False and after.is_timed_out() == True:
                                    embed.add_field(name=f'ACTION:',value=f'Timeout')
                                    embed.add_field(name=f'USER:',value=f'{after.mention}')
                                    embed.add_field(name=f'BY WHO:',value=f'{member.mention}')
                                    embed.add_field(name=f'Timed out until:' , value=f'```{after.timed_out_until}```')
                                    embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}\n{member.name}: {member.id}```')
                                    embed.set_footer(text=f'USERNAME: {after.name}',icon_url=after.display_avatar.url)
                                    await webhooker.send(embed=embed)
                                if before.is_timed_out() == True and after.is_timed_out() == False:
                                    embed.add_field(name=f'ACTION:',value=f'Remove Timeout')
                                    embed.add_field(name=f'USER:',value=f'{after.mention}')
                                    embed.add_field(name=f'BY WHO:',value=f'{member.mention}')
                                    embed.set_footer(text=f'USERNAME: {after.name}',icon_url=after.display_avatar.url)
                                    embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}\n{member.name}: {member.id}```')
                                    await webhooker.send(embed=embed)

                async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_update , limit=1):
                    async for entry2 in after.guild.audit_logs(limit=1):
                        if entry.action == entry2.action:
                            if before.nick != after.nick:
                                tmp_guild = find['user_id']
                                main_guild=self.bot.get_guild(tmp_guild)
                                member = discord.utils.get(main_guild.members , id = entry.user.id)
                                webhooker_id = find['nickname_webhook']
                                webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                                if webhooker is not None:
                                    embed=discord.Embed(
                                            title=f"Member Nickname Log",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                    )
                                    finaller = ''
                                    if member.id == entry.target.id:
                                        finaller = 'by himself'
                                    else:
                                        finaller=member.mention
                                    embed.add_field(name=f'ACTION:',value=f'Nickname Change')
                                    embed.add_field(name=f'USER:',value=f'{after.mention}')
                                    embed.add_field(name=f'BY WHO:',value=f'{finaller}')
                                    embed.add_field(name=f'OLD NAME:' , value=f'```{before.nick}```', inline=False)
                                    embed.add_field(name=f'NEW NAME:' , value=f'```{after.nick}```', inline=False)
                                    embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}```' , inline=False)
                                    embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                    await webhooker.send(embed=embed)



                            
                async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update , limit=1):
                    async for entry2 in after.guild.audit_logs(limit=1):
                        if entry.action == entry2.action:
                            tmp_guild = find['user_id']
                            main_guild=self.bot.get_guild(tmp_guild)
                            member = discord.utils.get(main_guild.members , id = entry.user.id)
                            webhooker_id = find['member_update_webhook']
                            webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                            if webhooker is not None:
                                embed=discord.Embed(
                                        title=f"Member Update Log",
                                        timestamp=datetime.now(),
                                        color= 0xF6F6F6
                                )
                                role_before = []
                                role_after = []
                                for i in after.roles:
                                    role_after.append(i.id)
                                for j in before.roles:
                                    role_before.append(j.id)
                                
                                if len(role_before)>len(role_after):
                                    for i in range(len(role_before)):
                                        if role_before[i] not in role_after:
                                            removed_role = discord.utils.get(main_guild.roles , id = role_before[i])
                                            embed.add_field(name=f'ACTION:',value=f'Remove Role')
                                            embed.add_field(name=f'USER:',value=f'{after.mention}')
                                            embed.add_field(name=f'BY WHO:',value=f'{member.mention}')
                                            embed.add_field(name=f'Removed Role:',value=f'{removed_role.mention}' , inline=False)
                                            embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}\n{member.name}: {member.id}```')
                                            embed.set_footer(text=f'USERNAME: {after.name}',icon_url=after.display_avatar.url)
                                            await webhooker.send(embed=embed)
                                
                                if len(role_after)>len(role_before):
                                    for i in range(len(role_after)):
                                        if role_after[i] not in role_before:
                                            added_role = discord.utils.get(main_guild.roles , id = role_after[i])
                                            embed.add_field(name=f'ACTION:',value=f'Add Role')
                                            embed.add_field(name=f'USER:',value=f'{after.mention}')
                                            embed.add_field(name=f'BY WHO:',value=f'{member.mention}')
                                            embed.add_field(name=f'Added Role:',value=f'{added_role.mention}' , inline=False)
                                            embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}\n{member.name}: {member.id}```')
                                            embed.set_footer(text=f'USERNAME: {after.name}',icon_url=after.display_avatar.url)
                                            await webhooker.send(embed=embed)
                            
            if (find:= collection.find_one({"user_id":member.guild.id , 'full_log_state':True})):
                async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_update , limit=1):
                    async for entry2 in after.guild.audit_logs(limit=1):
                        if entry.action == entry2.action:
                            tmp_guild = find['user_id']
                            channel_check= find['channel']
                            main_guild=self.bot.get_guild(tmp_guild)
                            member = discord.utils.get(main_guild.members , id = entry.user.id)
                            webhooker_id = find['full_log_webhook']
                            webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                            if webhooker is not None:
                                embed=discord.Embed(
                                        title=f"Member Update Log",
                                        timestamp=datetime.now(),
                                        color= 0xF6F6F6
                                )
                                if before.is_timed_out() == False and after.is_timed_out() == True:
                                    embed.add_field(name=f'ACTION:',value=f'Timeout')
                                    embed.add_field(name=f'USER:',value=f'{after.mention}')
                                    embed.add_field(name=f'BY WHO:',value=f'{member.mention}')
                                    embed.add_field(name=f'Timed out until:' , value=f'```{after.timed_out_until}```')
                                    embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}\n{member.name}: {member.id}```')
                                    embed.set_footer(text=f'USERNAME: {after.name}',icon_url=after.display_avatar.url)
                                    await webhooker.send(embed=embed)
                                if before.is_timed_out() == True and after.is_timed_out() == False:
                                    embed.add_field(name=f'ACTION:',value=f'Remove Timeout')
                                    embed.add_field(name=f'USER:',value=f'{after.mention}')
                                    embed.add_field(name=f'BY WHO:',value=f'{member.mention}')
                                    embed.set_footer(text=f'USERNAME: {after.name}',icon_url=after.display_avatar.url)
                                    embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}\n{member.name}: {member.id}```')
                                    if channel_check is not None:
                                        await webhooker.send(embed=embed)


                async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_update , limit=1):
                    async for entry2 in after.guild.audit_logs(limit=1):
                        if entry.action == entry2.action:
                            if before.nick != after.nick:
                                tmp_guild = find['user_id']
                                main_guild=self.bot.get_guild(tmp_guild)
                                channel_check= find['channel']
                                member = discord.utils.get(main_guild.members , id = entry.user.id)
                                webhooker_id = find['full_log_webhook']
                                webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                                if webhooker is not None:
                                    embed=discord.Embed(
                                            title=f"Member Nickname Log",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                    )
                                    finaller = ''
                                    if member.id == entry.target.id:
                                        finaller = 'by himself'
                                    else:
                                        finaller=member.mention
                                    embed.add_field(name=f'ACTION:',value=f'Nickname Change')
                                    embed.add_field(name=f'USER:',value=f'{after.mention}')
                                    embed.add_field(name=f'BY WHO:',value=f'{finaller}')
                                    embed.add_field(name=f'OLD NAME:' , value=f'```{before.nick}```', inline=False)
                                    embed.add_field(name=f'NEW NAME:' , value=f'```{after.nick}```', inline=False)
                                    embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}```' , inline=False)
                                    embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                    if channel_check is not None:
                                        await webhooker.send(embed=embed)

                            
                async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update , limit=1):
                    async for entry2 in after.guild.audit_logs(limit=1):
                        if entry.action == entry2.action:
                            tmp_guild = find['user_id']
                            main_guild=self.bot.get_guild(tmp_guild)
                            channel_check= find['channel']
                            member = discord.utils.get(main_guild.members , id = entry.user.id)
                            webhooker_id = find['full_log_webhook']
                            webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                            if webhooker is not None:
                                embed=discord.Embed(
                                        title=f"Member Update Log",
                                        timestamp=datetime.now(),
                                        color= 0xF6F6F6
                                )
                                role_before = []
                                role_after = []
                                for i in after.roles:
                                    role_after.append(i.id)
                                for j in before.roles:
                                    role_before.append(j.id)
                                
                                if len(role_before)>len(role_after):
                                    for i in range(len(role_before)):
                                        if role_before[i] not in role_after:
                                            removed_role = discord.utils.get(main_guild.roles , id = role_before[i])
                                            embed.add_field(name=f'ACTION:',value=f'Remove Role')
                                            embed.add_field(name=f'USER:',value=f'{after.mention}')
                                            embed.add_field(name=f'BY WHO:',value=f'{member.mention}')
                                            embed.add_field(name=f'Removed Role:',value=f'{removed_role.mention}' , inline=False)
                                            embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}\n{member.name}: {member.id}```')
                                            embed.set_footer(text=f'USERNAME: {after.name}',icon_url=after.display_avatar.url)
                                            if channel_check is not None:
                                                await webhooker.send(embed=embed)
                                
                                if len(role_after)>len(role_before):
                                    for i in range(len(role_after)):
                                        if role_after[i] not in role_before:
                                            added_role = discord.utils.get(main_guild.roles , id = role_after[i])
                                            embed.add_field(name=f'ACTION:',value=f'Add Role')
                                            embed.add_field(name=f'USER:',value=f'{after.mention}')
                                            embed.add_field(name=f'BY WHO:',value=f'{member.mention}')
                                            embed.add_field(name=f'Added Role:',value=f'{added_role.mention}' , inline=False)
                                            embed.add_field(name=f'ID:' , value=f'```{after.name}: {after.id}\n{member.name}: {member.id}```')
                                            embed.set_footer(text=f'USERNAME: {after.name}',icon_url=after.display_avatar.url)
                                            if channel_check is not None:
                                                await webhooker.send(embed=embed)
        except:
            pass
                        

            
        return
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        
        try:
            if (find1:= security.find_one({"_id":member.guild.id})):
                if find1['state']==1 and find1['anti_kick_warn'] is not None and find1['anti_kick'] == True:
                    async for entry2 in member.guild.audit_logs(limit=1):
                        async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick , limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                if entry.target.id == member.id:
                                    member = discord.utils.get(member.guild.members , id = entry.user.id)
                                    if member.id == member.guild.me.id:
                                        pass
                                    elif member.id == member.guild.owner_id:
                                        pass
                                    elif member.guild.me.top_role.position <= member.top_role.position:
                                        pass
                                    else:
                                        roles = find1['anti_kick_white_role']
                                        user_ids = find1['anti_kick_white_user']
                                        check_white_role=False
                                        check_white_user=False
                                        if roles is not None:
                                            for i in roles:
                                                for j in range(len(member.roles)):
                                                    if i == member.roles[j].id:
                                                        check_white_role = True
                                        if user_ids is not None:
                                            for i in user_ids:
                                                if i == member.id:
                                                    check_white_user = True

                                        all_white_roles = find1['all_white_list_role']
                                        all_white_users = find1['all_white_list_user']

                                        if all_white_roles is not None:
                                            for i in all_white_roles:
                                                for j in range(len(member.roles)):
                                                    if i == member.roles[j].id:
                                                        check_white_role = True

                                        if all_white_users is not None:
                                            for i in all_white_users:
                                                if i == member.id:
                                                    check_white_user = True


                                        if check_white_role == True or check_white_user == True:
                                            check_white_user = False
                                            check_white_role = False
                                        else:

                                            if (find2:= security.find_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})) is not None:
                                                warn=find2['warn']
                                                if warn == find1['anti_kick_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Kick Log",
                                                                description= f"user Action : kicked {entry.target.name}\nwarn limit : {find1['anti_kick_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_kick_punishment']}",
                                                                timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
                                                    if find1['anti_kick_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await member.guild.kick(ss, reason='kick a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})
                                                    elif find1['anti_kick_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await member.guild.ban(ss, reason='kick a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})
                                                else:
                                                    warn +=1
                                                    if warn == find1['anti_kick_warn']:
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                    title=f"Anti Kick Log",
                                                                    description= f"user Action : kicked {entry.target.name}\nwarn limit : {find1['anti_kick_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_kick_punishment']}",
                                                                    timestamp=datetime.now(),
                                                                        color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)
                                                        if find1['anti_kick_punishment']=='Kick':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await member.guild.kick(ss, reason='kick a user from server')
                                                            security.delete_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})
                                                        elif find1['anti_kick_punishment']=='Ban':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await member.guild.ban(ss, reason='kick a user from server')
                                                            security.delete_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})
                                                        
                                                    else:
                                                        security.update_one({'user_id':entry.user.id,"anti_kick":True, "guild":member.guild.id} , {'$set':{'warn':warn}})
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                    title=f"Anti Kick Log",
                                                                    description= f"user Action : kicked {entry.target.name}\nwarn limit : {find1['anti_kick_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                                    timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)

                                            else:
                                                security.insert_one({'user_id':entry.user.id , "guild":member.guild.id , "anti_kick":True, "warn":0})
                                                find2= security.find_one({"user_id":entry.user.id, "anti_kick":True  , "guild":member.guild.id})
                                                warn=find2['warn']
                                                if warn == find1['anti_kick_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Kick Log",
                                                                description= f"user Action : kicked {entry.target.name}\nwarn limit : {find1['anti_kick_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_kick_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_kick_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await member.guild.kick(ss, reason='kick a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})
                                                    elif find1['anti_kick_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await member.guild.ban(ss, reason='kick a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})
                                                else:
                                                    warn +=1
                                                    if warn == find1['anti_kick_warn']:
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                    title=f"Anti Kick Log",
                                                                    description= f"user Action : kicked {entry.target.name}\nwarn limit : {find1['anti_kick_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_kick_punishment']}",
                                                                    timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)

                                                        if find1['anti_kick_punishment']=='Kick':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await member.guild.kick(ss, reason='kick a user from server')
                                                            security.delete_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})
                                                        elif find1['anti_kick_punishment']=='Ban':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await member.guild.ban(ss, reason='kick a user from server')
                                                            security.delete_one({"user_id":entry.user.id,"anti_kick":True, "guild":member.guild.id})
                                                        
                                                    else:
                                                        security.update_one({'user_id':entry.user.id,"anti_kick":True, "guild":member.guild.id} , {'$set':{'warn':warn}})
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                    title=f"Anti Kick Log",
                                                                    description= f"user Action : kicked {entry.target.name}\nwarn limit : {find1['anti_kick_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                                    timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)

        except:
            pass

        
                #member kick or left log
        try:
            if (find:= collection.find_one({"user_id":member.guild.id , 'auto_log_creator':True})):
                async for entry2 in member.guild.audit_logs(limit=1):
                    async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick , limit=1):
                        if entry.action == entry2.action and entry.user.id == entry2.user.id:
                            if entry.target.id == member.id:
                                tmp_guild = find['user_id']
                                main_guild=self.bot.get_guild(tmp_guild)
                                kicker = discord.utils.get(main_guild.members , id = entry.user.id)
                                webhooker_id1 = find['member_kick_webhook']
                                webhooker1 = discord.utils.get(await main_guild.webhooks() , id = webhooker_id1)
                                if webhooker1 is not None:
                                    embed=discord.Embed(
                                            title=f"Kick Log",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                    )
                                    embed.add_field(name=f'ACTION:',value=f'Kick')
                                    embed.add_field(name=f'USER:', value=f'{member.mention}')
                                    embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                                    embed.add_field(name=f'REASON:', value=f'{entry.reason}')
                                    embed.add_field(name=f'KICKED BY:', value=f'{kicker.mention}' , inline=False)
                                    embed.add_field(name=f'KICKER ID:', value=f'```{kicker.id}```' , inline=False)
                                    embed.add_field(name=f'ID:' , value=f'```{member.name}: {member.id}```', inline=False)
                                    embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                    await webhooker1.send(embed=embed)
                            
                
                        else:

                            tmp_guild = find['user_id']
                            tmp_id_channel= find['member_decrease_state']
                            main_guild=self.bot.get_guild(tmp_guild)
                            webhooker_id = find['member_decrease_webhook']
                            webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                            if webhooker is not None:
                                embed=discord.Embed(
                                        title=f"MEMBER LEFT LOG",
                                        timestamp=datetime.now(),
                                        color= 0xF6F6F6
                                )
                                embed.add_field(name=f'ACTION:',value='Left Guild')
                                embed.add_field(name=f'USERNAME:', value=f'{member.name}')
                                embed.add_field(name=f'USER MENTION:', value=f'{member.mention}')
                                embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" , inline=False)
                                embed.add_field(name=f'REASON:', value=f'{entry.reason}')
                                embed.add_field(name=f'joined at:',value=f"{discord.utils.format_dt(member.joined_at , 'R')}" , inline=False)
                                embed.add_field(name=f'ID:' , value=f'```{member.name}: {member.id}```', inline=False)
                                embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)

                                await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":member.guild.id , 'full_log_state':True})):
                async for entry2 in member.guild.audit_logs(limit=1):
                    async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick , limit=1):
                        if entry.action == entry2.action and entry.user.id == entry2.user.id:
                            if entry.target.id == member.id:
                                tmp_guild = find['user_id']
                                channel_check= find['channel']
                                main_guild=self.bot.get_guild(tmp_guild)
                                kicker = discord.utils.get(main_guild.members , id = entry.user.id)
                                webhooker_id1 = find['full_log_webhook']
                                webhooker1 = discord.utils.get(await main_guild.webhooks() , id = webhooker_id1)
                                if webhooker1 is not None:
                                    embed=discord.Embed(
                                            title=f"Kick Log",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                    )
                                    embed.add_field(name=f'ACTION:',value=f'Kick')
                                    embed.add_field(name=f'USER:', value=f'{member.mention}')
                                    embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                                    embed.add_field(name=f'REASON:', value=f'{entry.reason}')
                                    embed.add_field(name=f'KICKED BY:', value=f'{kicker.mention}' , inline=False)
                                    embed.add_field(name=f'KICKER ID:', value=f'```{kicker.id}```' , inline=False)
                                    embed.add_field(name=f'ID:' , value=f'```{member.name}: {member.id}```', inline=False)
                                    embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                    if channel_check is not None:
                                        await webhooker1.send(embed=embed)
                            
                
                        else:
                        
                            tmp_guild = find['user_id']
                            tmp_id_channel= find['member_decrease_state']
                            channel_check= find['channel']
                            main_guild=self.bot.get_guild(tmp_guild)
                            webhooker_id = find['full_log_webhook']
                            webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                            if webhooker is not None:
                                embed=discord.Embed(
                                        title=f"MEMBER LEFT LOG",
                                        timestamp=datetime.now(),
                                        color= 0xF6F6F6
                                )
                                embed.add_field(name=f'ACTION:',value='Left Guild')
                                embed.add_field(name=f'USERNAME:', value=f'{member.name}')
                                embed.add_field(name=f'USER MENTION:', value=f'{member.mention}')
                                embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" , inline=False)
                                embed.add_field(name=f'REASON:', value=f'{entry.reason}')
                                embed.add_field(name=f'joined at:',value=f"{discord.utils.format_dt(member.joined_at , 'R')}" , inline=False)
                                embed.add_field(name=f'ID:' , value=f'```{member.name}: {member.id}```', inline=False)
                                embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)

                                if channel_check is not None:
                                    await webhooker.send(embed=embed)

        except:
            pass


        return
          
    @commands.Cog.listener()
    async def on_member_ban(self,guild, user:Union(discord.User , discord.Member)):
        
        try:
            if (find1:= security.find_one({"_id":guild.id})):
                if find1['state']==1 and find1['anti_ban_warn'] is not None and find1['anti_ban'] == True:
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.ban , limit=1):
                        async for entry2 in guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:

                                member = discord.utils.get(guild.members , id = entry.user.id)
                                if member.id == guild.me.id:
                                    pass
                                elif member.id == guild.owner_id:
                                    pass
                                elif guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:
                                    roles = find1['anti_ban_white_role']
                                    user_ids = find1['anti_ban_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True


                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['anti_ban_warn']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                            title=f"Anti Ban Log",
                                                            description= f"user Action : banned {entry.target.name}\nwarn limit : {find1['anti_ban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_ban_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['anti_ban_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await guild.kick(ss,reason='ban a user from server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})
                                                elif find1['anti_ban_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await guild.ban(ss,reason='ban a user from server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['anti_ban_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Ban Log",
                                                                description= f"user Action : banned {entry.target.name}\nwarn limit : {find1['anti_ban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_ban_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_ban_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.kick(ss,reason='ban a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})
                                                    elif find1['anti_ban_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.ban(ss,reason='ban a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"anti_ban":True, "guild":guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti Ban Log",
                                                            description= f"user Action : banned {entry.target.name}\nwarn limit : {find1['anti_ban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":guild.id , "anti_ban":True, "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id, "anti_ban":True, "guild":guild.id})
                                            warn=find2['warn']
                                            if warn == find1['anti_ban_warn']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                            title=f"Anti Ban Log",
                                                            description= f"user Action : banned {entry.target.name}\nwarn limit : {find1['anti_ban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_ban_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['anti_ban_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await guild.kick(ss,reason='ban a user from server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})
                                                elif find1['anti_ban_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await guild.ban(ss,reason='ban a user from server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['anti_ban_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Ban Log",
                                                                description= f"user Action : banned {entry.target.name}\nwarn limit : {find1['anti_ban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_ban_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_ban_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.kick(ss,reason='ban a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})
                                                    elif find1['anti_ban_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.ban(ss,reason='ban a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_ban":True, "guild":guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"anti_ban":True, "guild":guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti Ban Log",
                                                            description= f"user Action : banned {entry.target.name}\nwarn limit : {find1['anti_ban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

        except:
            pass

        try: #mwmber ban log
            if (find:= collection.find_one({"user_id":guild.id , 'auto_log_creator':True})):
                async for entry in guild.audit_logs(action=discord.AuditLogAction.ban , limit=1):
                    member = discord.utils.get(guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['member_ban_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['member_ban_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Ban Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Ban')
                        embed.add_field(name=f'USER:', value=f'{user.mention}')
                        embed.add_field(name=f'BAN BY:', value=f'{member.mention}' , inline=False)
                        embed.add_field(name=f'REASON:', value=f'{entry.reason}')
                        embed.add_field(name=f'joined at:',value=f"{discord.utils.format_dt(user.joined_at , 'R')}" , inline=False)
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(user.created_at , 'R')}" , inline=False )
                        embed.add_field(name=f'ID:' , value=f"```{user.name}: {user.id}\n{member.name}: {member.id}```", inline=False )
                        
                        embed.set_footer(text=f'USERNAME: {user.name}',icon_url=user.display_avatar.url)
                        await webhooker.send(embed=embed)
            if (find:= collection.find_one({"user_id":guild.id , 'full_log_state':True})):
                async for entry in guild.audit_logs(action=discord.AuditLogAction.ban , limit=1):
                    member = discord.utils.get(guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Ban Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Ban')
                        embed.add_field(name=f'USER:', value=f'{user.mention}')
                        embed.add_field(name=f'BAN BY:', value=f'{member.mention}' , inline=False)
                        embed.add_field(name=f'REASON:', value=f'{entry.reason}')
                        embed.add_field(name=f'joined at:',value=f"{discord.utils.format_dt(user.joined_at , 'R')}" , inline=False)
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(user.created_at , 'R')}" , inline=False )
                        embed.add_field(name=f'ID:' , value=f"```{user.name}: {user.id}\n{member.name}: {member.id}```", inline=False )
                        
                        embed.set_footer(text=f'USERNAME: {user.name}',icon_url=user.display_avatar.url)
                        if channel_check is not None:
                            await webhooker.send(embed=embed)
        except:

            return
        
        return
    @commands.Cog.listener()
    async def on_member_unban(self,guild, user):
        
        try:
            if (find1:= security.find_one({"_id":guild.id})):
                if find1['state']==1 and find1['anti_unban_warn'] is not None and find1['anti_unban'] == True:
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.unban , limit=1):
                        async for entry2 in guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                member = discord.utils.get(guild.members , id = entry.user.id)
                                if member.id == guild.me.id:
                                    pass
                                elif member.id == guild.owner_id:
                                    pass
                                elif guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:
                                    roles = find1['anti_unban_white_role']
                                    user_ids = find1['anti_unban_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True


                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['anti_unban_warn']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                            title=f"Anti Unban Log",
                                                            description= f"user Action : unbanned {entry.target.name}\nwarn limit : {find1['anti_unban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_unban_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['anti_unban_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await guild.kick(ss , reason='unban a user from server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})
                                                elif find1['anti_unban_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await guild.ban(ss, reason='unban a user from server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['anti_unban_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Unban Log",
                                                                description= f"user Action : unbanned {entry.target.name}\nwarn limit : {find1['anti_unban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_unban_punishment']}",
                                                                timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_unban_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.kick(ss, reason='unban a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})
                                                    elif find1['anti_unban_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.ban(ss, reason='unban a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"anti_unban":True, "guild":guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti Unban Log",
                                                            description= f"user Action : unbanned {entry.target.name}\nwarn limit : {find1['anti_unban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":guild.id , "anti_unban":True, "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id, "anti_unban":True, "guild":guild.id})
                                            warn=find2['warn']
                                            if warn == find1['anti_unban_warn']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                            title=f"Anti Unban Log",
                                                            description= f"user Action : unbanned {entry.target.name}\nwarn limit : {find1['anti_unban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_unban_punishment']}",
                                                            timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['anti_unban_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await guild.kick(ss, reason='unban a user from server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})
                                                elif find1['anti_unban_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await guild.ban(ss, reason='unban a user from server')
                                                    security.delete_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['anti_unban_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Unban Log",
                                                                description= f"user Action : unbanned {entry.target.name}\nwarn limit : {find1['anti_unban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_unban_punishment']}",
                                                                timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_unban_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.kick(ss, reason='unban a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})
                                                    elif find1['anti_unban_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.ban(ss, reason='unban a user from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_unban":True, "guild":guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"anti_unban":True, "guild":guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti Unban Log",
                                                            description= f"user Action : unbanned {entry.target.name}\nwarn limit : {find1['anti_unban_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

        except:
            pass

        try: #member unban log
            if (find:= collection.find_one({"user_id":guild.id , 'auto_log_creator':True})):
                async for entry in guild.audit_logs(action=discord.AuditLogAction.unban , limit=1):
                    member = discord.utils.get(guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['member_unban_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['member_unban_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Unban Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Unban')
                        embed.add_field(name=f'USER:', value=f'{user.mention}')
                        embed.add_field(name=f'UNBAN BY:', value=f'{member.mention}' , inline=False)
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(user.created_at , 'R')}",inline=False )
                        embed.add_field(name=f'ID:' , value=f"```{user.name}: {user.id}\n{member.name}: {member.id}```" ,inline=False)
                        
                        embed.set_footer(text=f'USERNAME: {user.name}',icon_url=user.display_avatar.url)
                        await webhooker.send(embed=embed)
            if (find:= collection.find_one({"user_id":guild.id , 'full_log_state':True})):
                async for entry in guild.audit_logs(action=discord.AuditLogAction.unban , limit=1):
                    member = discord.utils.get(guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Unban Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Unban')
                        embed.add_field(name=f'USER:', value=f'{user.mention}')
                        embed.add_field(name=f'UNBAN BY:', value=f'{member.mention}' , inline=False)
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(user.created_at , 'R')}",inline=False )
                        embed.add_field(name=f'ID:' , value=f"```{user.name}: {user.id}\n{member.name}: {member.id}```" ,inline=False )
                        
                        embed.set_footer(text=f'USERNAME: {user.name}',icon_url=user.display_avatar.url)
                        if channel_check is not None:
                            await webhooker.send(embed=embed)

        except:

            return
        
        return
    @commands.Cog.listener()
    async def on_guild_emojis_update(self,guild, before, after):
        
        try:
            if (find1:= security.find_one({"_id":guild.id})):
                if find1['anti_emoji_delete'] == True and find1['anti_emoji_delete_warn'] is not None:
                    if len(before) > len(after):
                        async for entry in guild.audit_logs(action=discord.AuditLogAction.emoji_delete , limit=1):
                            async for entry2 in guild.audit_logs(limit=1):
                                if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                    member = discord.utils.get(guild.members , id = entry.user.id)
                                    if member.id == guild.me.id:
                                        pass
                                    elif member.id == guild.owner_id:
                                        pass
                                    elif guild.me.top_role.position <= member.top_role.position:
                                        pass
                                    else:
                                        roles = find1['anti_emoji_white_role']
                                        user_ids = find1['anti_emoji_white_user']
                                        check_white_role=False
                                        check_white_user=False
                                        if roles is not None:
                                            for i in roles:
                                                for j in range(len(member.roles)):
                                                    if i == member.roles[j].id:
                                                        check_white_role = True
                                        if user_ids is not None:
                                            for i in user_ids:
                                                if i == member.id:
                                                    check_white_user = True

                                        all_white_roles = find1['all_white_list_role']
                                        all_white_users = find1['all_white_list_user']

                                        if all_white_roles is not None:
                                            for i in all_white_roles:
                                                for j in range(len(member.roles)):
                                                    if i == member.roles[j].id:
                                                        check_white_role = True

                                        if all_white_users is not None:
                                            for i in all_white_users:
                                                if i == member.id:
                                                    check_white_user = True


                                        if check_white_role == True or check_white_user == True:
                                            check_white_user = False
                                            check_white_role = False
                                        else:

                                            if (find2:= security.find_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})) is not None:
                                                warn=find2['warn']
                                                if warn == find1['anti_emoji_delete_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Emoji Log",
                                                                description= f"user Action : delete emoji\nwarn limit : {find1['anti_emoji_delete_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_emoji_delete_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_emoji_delete_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.kick(ss , reason='delete emoji from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                    elif find1['anti_emoji_delete_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.ban(ss, reason='delete emoji from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                else:
                                                    warn +=1
                                                    if warn == find1['anti_emoji_delete_warn']:
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                    title=f"Anti Emoji Log",
                                                                    description= f"user Action : delete emoji\nwarn limit : {find1['anti_emoji_delete_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_emoji_delete_punishment']}",
                                                                    timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                                    )
                                                                await exist_check.send(embed=embed)

                                                        if find1['anti_emoji_delete_punishment']=='Kick':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await guild.kick(ss, reason='delete emoji from server')
                                                            security.delete_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                        elif find1['anti_emoji_delete_punishment']=='Ban':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await guild.ban(ss, reason='delete emoji from server')
                                                            security.delete_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                        
                                                    else:
                                                        security.update_one({'user_id':entry.user.id, "guild":guild.id} , {'$set':{'warn':warn}})
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                title=f"Anti Emoji Log",
                                                                description= f"user Action : delete emoji\nwarn limit : {find1['anti_emoji_delete_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)

                                            else:
                                                security.insert_one({'user_id':entry.user.id , "guild":guild.id , "anti_emoji_delete":True, "warn":0})
                                                find2= security.find_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                warn=find2['warn']
                                                if warn == find1['anti_emoji_delete_warn']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                                title=f"Anti Emoji Log",
                                                                description= f"user Action : delete emoji\nwarn limit : {find1['anti_emoji_delete_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_emoji_delete_punishment']}",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                                )
                                                            await exist_check.send(embed=embed)

                                                    if find1['anti_emoji_delete_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.kick(ss, reason='delete emoji from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                    elif find1['anti_emoji_delete_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await guild.ban(ss, reason='delete emoji from server')
                                                        security.delete_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                else:
                                                    warn +=1
                                                    if warn == find1['anti_emoji_delete_warn']:
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                    title=f"Anti Emoji Log",
                                                                    description= f"user Action : delete emoji\nwarn limit : {find1['anti_emoji_delete_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['anti_emoji_delete_punishment']}",
                                                                    timestamp=datetime.now(),
                                                                    color= 0xF6F6F6
                                                                    )
                                                                await exist_check.send(embed=embed)

                                                        if find1['anti_emoji_delete_punishment']=='Kick':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await guild.kick(ss, reason='delete emoji from server')
                                                            security.delete_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                        elif find1['anti_emoji_delete_punishment']=='Ban':
                                                            ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                            await guild.ban(ss, reason='delete emoji from server')
                                                            security.delete_one({"user_id":entry.user.id,"anti_emoji_delete":True, "guild":guild.id})
                                                        
                                                    else:
                                                        security.update_one({'user_id':entry.user.id,"anti_emoji_delete":True, "guild":guild.id} , {'$set':{'warn':warn}})
                                                        if find1['security_log_channel'] is not None:
                                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                            if exist_check is not None:
                                                                embed=discord.Embed(
                                                                title=f"Anti Emoji Log",
                                                                description= f"user Action : delete emoji\nwarn limit : {find1['anti_emoji_delete_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                                timestamp=datetime.now(),
                                                                color= 0xF6F6F6
                                                                )
                                                                await exist_check.send(embed=embed)
        except:
            pass
        try:
            if (find:= collection.find_one({"user_id":guild.id , 'auto_log_creator':True})):
                if len(after)>len(before):
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.emoji_create , limit=1):
                        member = discord.utils.get(guild.members , id = entry.user.id)
                        tmp_guild = find['user_id']
                        tmp_id_channel= find['emoji_update_state']
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['emoji_update_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Emoji Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            embed.add_field(name=f'ACTION:',value=f'Create Emoji')
                            embed.add_field(name=f'CREATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'EMOJI NAME:', value=f'{entry.target.name}',inline=False)
                            embed.add_field(name=f'ANIMATED:', value=f'{entry.target.animated}',inline=False)
                            embed.add_field(name=f'MANAGED:', value=f'{entry.target.managed}',inline=False)
                            embed.add_field(name=f'ID:' , value=f"```EMOJI: {entry.target.id}\nUSER: {member.id}```" , inline=False )
                            embed.set_thumbnail(url=entry.target.url)
                            
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            await webhooker.send(embed=embed)
                elif len(before)>len(after):
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.emoji_delete , limit=1):
                        member = discord.utils.get(guild.members , id = entry.user.id)
                        tmp_guild = find['user_id']
                        tmp_id_channel= find['emoji_update_state']
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['emoji_update_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Emoji Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            namw_was =''
                            animated_log = ''
                            managed_log = ''
                            emoji_id = ''
                            emoji_url = ''
                            for i in before:
                                if i.id == entry.target.id:
                                    name_was = i.name
                                    animated_log = i.animated
                                    managed_log = i.managed
                                    emoji_id = i.id
                                    emoji_url=i.url
                            embed.add_field(name=f'ACTION:',value=f'Delete Emoji')
                            embed.add_field(name=f'DELETED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'EMOJI NAME:', value=f'{name_was}',inline=False)
                            embed.add_field(name=f'ANIMATED:', value=f'{animated_log}',inline=False)
                            embed.add_field(name=f'MANAGED:', value=f'{managed_log}',inline=False)
                            embed.add_field(name=f'ID:' , value=f"```EMOJI: {emoji_id}\nUSER: {member.id}```" , inline=False )
                            embed.set_thumbnail(url=emoji_url)
                            
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            await webhooker.send(embed=embed)
                elif len(before)==len(after):
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.emoji_update , limit=1):
                        member = discord.utils.get(guild.members , id = entry.user.id)
                        tmp_guild = find['user_id']
                        tmp_id_channel= find['emoji_update_state']
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['emoji_update_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Emoji Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            namw_was =''
                            for i in before:
                                if i.id == entry.target.id:
                                    name_was = i.name
                                
                            embed.add_field(name=f'ACTION:',value=f'Update Emoji')
                            embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'EMOJI NAME:', value=f'{entry.target.name}',inline=False)
                            embed.add_field(name=f'ANIMATED:', value=f'{entry.target.animated}',inline=False)
                            embed.add_field(name=f'MANAGED:', value=f'{entry.target.managed}',inline=False)
                            embed.add_field(name=f'NAME CHANGES LOG:', value=f'```{name_was} ---> {entry.target.name}```',inline=False)
                            embed.add_field(name=f'ID:' , value=f"```EMOJI: {entry.target.id}\nUSER: {member.id}```" , inline=False )
                            embed.set_thumbnail(url=entry.target.url)
                            
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":guild.id , 'full_log_state':True})):
                if len(after)>len(before):
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.emoji_create , limit=1):
                        member = discord.utils.get(guild.members , id = entry.user.id)
                        tmp_guild = find['user_id']
                        channel_check= find['channel']
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['full_log_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Emoji Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            embed.add_field(name=f'ACTION:',value=f'Create Emoji')
                            embed.add_field(name=f'CREATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'EMOJI NAME:', value=f'{entry.target.name}',inline=False)
                            embed.add_field(name=f'ANIMATED:', value=f'{entry.target.animated}',inline=False)
                            embed.add_field(name=f'MANAGED:', value=f'{entry.target.managed}',inline=False)
                            embed.add_field(name=f'ID:' , value=f"```EMOJI: {entry.target.id}\nUSER: {member.id}```" , inline=False )
                            embed.set_thumbnail(url=entry.target.url)
                            
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            if channel_check is not None:
                                await webhooker.send(embed=embed)
                elif len(before)>len(after):
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.emoji_delete , limit=1):
                        member = discord.utils.get(guild.members , id = entry.user.id)
                        tmp_guild = find['user_id']
                        tmp_id_channel= find['emoji_update_state']
                        channel_check= find['channel']
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['full_log_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Emoji Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            namw_was =''
                            animated_log = ''
                            managed_log = ''
                            emoji_id = ''
                            emoji_url = ''
                            for i in before:
                                if i.id == entry.target.id:
                                    name_was = i.name
                                    animated_log = i.animated
                                    managed_log = i.managed
                                    emoji_id = i.id
                                    emoji_url=i.url
                            embed.add_field(name=f'ACTION:',value=f'Delete Emoji')
                            embed.add_field(name=f'DELETED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'EMOJI NAME:', value=f'{name_was}',inline=False)
                            embed.add_field(name=f'ANIMATED:', value=f'{animated_log}',inline=False)
                            embed.add_field(name=f'MANAGED:', value=f'{managed_log}',inline=False)
                            embed.add_field(name=f'ID:' , value=f"```EMOJI: {emoji_id}\nUSER: {member.id}```" , inline=False )
                            embed.set_thumbnail(url=emoji_url)
                            
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            if channel_check is not None:
                                await webhooker.send(embed=embed)
                elif len(before)==len(after):
                    async for entry in guild.audit_logs(action=discord.AuditLogAction.emoji_update , limit=1):
                        member = discord.utils.get(guild.members , id = entry.user.id)
                        tmp_guild = find['user_id']
                        tmp_id_channel= find['emoji_update_state']
                        main_guild=self.bot.get_guild(tmp_guild)
                        channel_check= find['channel']
                        webhooker_id = find['full_log_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Emoji Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            namw_was =''
                            for i in before:
                                if i.id == entry.target.id:
                                    name_was = i.name
                                
                            embed.add_field(name=f'ACTION:',value=f'Update Emoji')
                            embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'EMOJI NAME:', value=f'{entry.target.name}',inline=False)
                            embed.add_field(name=f'ANIMATED:', value=f'{entry.target.animated}',inline=False)
                            embed.add_field(name=f'MANAGED:', value=f'{entry.target.managed}',inline=False)
                            embed.add_field(name=f'NAME CHANGES LOG:', value=f'```{name_was} ---> {entry.target.name}```',inline=False)
                            embed.add_field(name=f'ID:' , value=f"```EMOJI: {entry.target.id}\nUSER: {member.id}```" , inline=False )
                            embed.set_thumbnail(url=entry.target.url)
                            
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            if channel_check is not None:
                                await webhooker.send(embed=embed)
        except:
            pass

        return
    @commands.Cog.listener()
    async def on_message(self,message):
        try:
            bot_mentioner = discord.utils.get(message.guild.members , id = message.guild.me.id)
            if message.content == bot_mentioner.mention:
                embed,select=await help(message)
                await message.channel.send(embed=embed , view=select)
            if message.author.id == message.guild.me.id:
                pass
            elif message.author.id == message.guild.owner_id:
                pass
            elif message.guild.me.top_role.position <= message.author.top_role.position:
                pass
            else:
                if (find1:= security.find_one({"_id":message.guild.id})):
                    if find1['state']==1 and find1['server_invite_detect_security']==True:
                        member = discord.utils.get(message.guild.members , id = message.author.id)
                        roles = find1['discord_invite_white_role']
                        user_ids = find1['discord_invite_white_user']
                        check_white_role=False
                        check_white_user=False
                        if roles is not None:
                            for i in roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True
                        if user_ids is not None:
                            for i in user_ids:
                                if i == member.id:
                                    check_white_user = True
                        all_white_roles = find1['all_white_list_role']
                        all_white_users = find1['all_white_list_user']

                        if all_white_roles is not None:
                            for i in all_white_roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True

                        if all_white_users is not None:
                            for i in all_white_users:
                                if i == member.id:
                                    check_white_user = True

                        if check_white_role == True or check_white_user == True:
                            check_white_user = False
                            check_white_role = False
                        else:
                        
                            
                            check=False
                            text=message.content.split(' ')
                            for txt in text:
                                if "https://discord.gg" in txt or "https://discord.com" in txt or 'http://discord.gg' in txt or 'http://discord.com' in txt:
                                    check=True
                            
                            if check==True:
                                if find1['security_log_channel'] is not None:
                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                    if exist_check is not None:
                                        embed=discord.Embed(
                                            title=f"discord link invite delete Log",
                                            description= f"user Action : sent an invite link\nuser: <@{message.author.id}>\nbot Action: Delete message",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                            )
                                        await exist_check.send(embed=embed)

                                await message.delete()
                                check=False


            
                if (find1:= security.find_one({"_id":message.guild.id })):
                    if find1['anti_spam'] == True or find1['anti_raid']==True:
                        await self.bot.handler.propagate(message)
                        member = discord.utils.get(message.guild.members , id = message.author.id)
                        roles = find1['anti_spam_white_role']
                        user_ids = find1['anti_spam_white_user']
                        check_white_role=False
                        check_white_user=False
                        if roles is not None:
                            for i in roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True
                        if user_ids is not None:
                            for i in user_ids:
                                if i == member.id:
                                    check_white_user = True

                        all_white_roles = find1['all_white_list_role']
                        all_white_users = find1['all_white_list_user']

                        if all_white_roles is not None:
                            for i in all_white_roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True

                        if all_white_users is not None:
                            for i in all_white_users:
                                if i == member.id:
                                    check_white_user = True

                        if check_white_role == True or check_white_user == True:
                            check_white_user = False
                            check_white_role = False
                        else:
                            # await asyncio.sleep(0.21)
                            # if await anti_spam(message) == True:
                            if await self.bot.tracker.is_spamming(message):
                                if find1['security_log_channel'] is not None:
                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                    if exist_check is not None:
                                        embed=discord.Embed(
                                            title=f"Anti Spam Log",
                                            description= f"user Action : Spamming\nuser: <@{message.author.id}>\nbot Action: Timeout",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                            )
                                        await exist_check.send(embed=embed)

                                timer = find1['anti_spam_time']
                                if timer is not None:
                                    us=discord.utils.get(message.guild.members , id = message.author.id)
                                    us:discord.Member
                                    await us.timeout(Utils.utcnow()+timedelta(seconds=timer))
                                    await message.delete()
                                    await self.bot.tracker.remove_punishments(message)
                                else:
                                    us=discord.utils.get(message.guild.members , id = message.author.id)
                                    us:discord.Member
                                    await us.timeout(Utils.utcnow()+timedelta(seconds=900))
                                    await message.delete()
                                    await self.bot.tracker.remove_punishments(message)
                            #await self.bot.process_commands(message)              

                if (find1:= security.find_one({"_id":message.guild.id})):
                    if find1['state']==1 and find1['anti_bad_word']==True and find1['anti_bad_words_warn'] is not None and find1['anti_bad_words_punishment'] is not None:
                        member = discord.utils.get(message.guild.members , id = message.author.id)
                        roles = find1['anti_bad_words_white_role']
                        user_ids = find1['anti_bad_words_white_user']
                        check_white_role=False
                        check_white_user=False
                        if roles is not None:
                            for i in roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True
                        if user_ids is not None:
                            for i in user_ids:
                                if i == member.id:
                                    check_white_user = True

                        all_white_roles = find1['all_white_list_role']
                        all_white_users = find1['all_white_list_user']

                        if all_white_roles is not None:
                            for i in all_white_roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True

                        if all_white_users is not None:
                            for i in all_white_users:
                                if i == member.id:
                                    check_white_user = True

                        if check_white_role == True or check_white_user == True:
                            check_white_user = False
                            check_white_role = False
                        else:
                        
                            roles = find1['bad_words']
                            check=False
                            text=message.content.split(' ')
                            if roles is not None:
                                for i in roles:
                                    for j in text:
                                        if i.lower() ==j.lower():
                                            check=True
                            
                            if check==True:
                                if (find2:= security.find_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})) is not None:
                                    warn=find2['warn']
                                    if warn == find1['anti_bad_words_warn']:
                                        if find1['security_log_channel'] is not None:
                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                            if exist_check is not None:
                                                embed=discord.Embed(
                                                    title=f"Anti bad words Log",
                                                    description= f"user Action : used bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{message.author.id}>\nusers warn : {warn}\nbot Action: {find1['anti_bad_words_punishment']}",
                                                    timestamp=datetime.now(),
                                                    color= 0xF6F6F6
                                                    )
                                                await exist_check.send(embed=embed)

                                        if find1['anti_bad_words_punishment']=='Kick':
                                            ss=discord.Object(message.author.id , type='abc.Snowflake')
                                            # await asyncio.sleep(0.22)
                                            await message.guild.kick(ss , reason='using bad words')
                                            await message.delete()
                                            security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})

                                        elif find1['anti_bad_words_punishment']=='Ban':
                                            ss=discord.Object(message.author.id , type='abc.Snowflake')
                                            # await asyncio.sleep(0.22)
                                            await message.guild.ban(ss, reason='using bad words')
                                            await message.delete()
                                            security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})

                                        elif find1['anti_bad_words_punishment']=='Timeout':
                                            ss=discord.Object(message.author.id , type='abc.Snowflake')
                                            timer = find1['bad_word_time_timeout']
                                            # await message.guild.edit(ss,mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))
                                            us=discord.utils.get(message.guild.members , id = message.author.id)
                                            await us.timeout(Utils.utcnow()+timedelta(seconds=timer), reason='using bad words')
                                            # await us.edit(mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))
                                            # await asyncio.sleep(0.22)
                                            await message.delete()
                                            security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                    else:
                                        warn +=1
                                        if warn == find1['anti_bad_words_warn']:
                                            if find1['security_log_channel'] is not None:
                                                exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                if exist_check is not None:
                                                    embed=discord.Embed(
                                                        title=f"Anti bad words Log",
                                                        description= f"user Action : used bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{message.author.id}>\nusers warn : {warn}\nbot Action: {find1['anti_bad_words_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                    await exist_check.send(embed=embed)

                                            if find1['anti_bad_words_punishment']=='Kick':
                                                ss=discord.Object(message.author.id , type='abc.Snowflake')
                                                # await asyncio.sleep(0.5)
                                                await message.guild.kick(ss, reason='using bad words')
                                                await message.delete()

                                                security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                            elif find1['anti_bad_words_punishment']=='Ban':
                                                ss=discord.Object(message.author.id , type='abc.Snowflake')
                                                # await asyncio.sleep(0.5)
                                                await message.guild.ban(ss, reason='using bad words')
                                                await message.delete()
                                                security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})

                                            elif find1['anti_bad_words_punishment']=='Timeout':
                                                ss=discord.Object(message.author.id , type='abc.Snowflake')
                                                timer = find1['bad_word_time_timeout']
                                                us=discord.utils.get(message.guild.members , id = message.author.id)
                                                # await asyncio.sleep(0.5)
                                                await us.timeout(Utils.utcnow()+timedelta(seconds=timer), reason='using bad words')
                                                print (us)
                                                # await us.edit(mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))                                    await message.delete()
                                                security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                            
                                        else:
                                            security.update_one({'user_id':message.author.id,"anti_bad":True, "guild":message.guild.id} , {'$set':{'warn':warn}})
                                            if find1['security_log_channel'] is not None:
                                                exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                if exist_check is not None:
                                                    embed=discord.Embed(
                                                    title=f"Anti bad words Log",
                                                    description= f"user Action : used bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{message.author.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                    timestamp=datetime.now(),
                                                    color= 0xF6F6F6
                                                    )
                                                    await exist_check.send(embed=embed)


                                else:
                                    security.insert_one({'user_id':message.author.id , "guild":message.guild.id , "anti_bad":True , "warn":0})
                                    find2= security.find_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                    warn=find2['warn']
                                    if warn == find1['anti_bad_words_warn']:
                                        if find1['security_log_channel'] is not None:
                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                            if exist_check is not None:
                                                embed=discord.Embed(
                                                    title=f"Anti bad words Log",
                                                    description= f"user Action : used bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{message.author.id}>\nusers warn : {warn}\nbot Action: {find1['anti_bad_words_punishment']}",
                                                    timestamp=datetime.now(),
                                                    color= 0xF6F6F6
                                                    )
                                                # await asyncio.sleep(1)
                                                await exist_check.send(embed=embed)

                                        if find1['anti_bad_words_punishment']=='Kick':
                                            ss=discord.Object(message.author.id , type='abc.Snowflake')
                                            await message.guild.kick(ss, reason='using bad words')
                                            await message.delete()
                                            security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                        elif find1['anti_bad_words_punishment']=='Ban':
                                            ss=discord.Object(message.author.id , type='abc.Snowflake')
                                            await message.guild.ban(ss, reason='using bad words')
                                            await message.delete()
                                            security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                        elif find1['anti_bad_words_punishment']=='Timeout':
                                            ss=discord.Object(message.author.id , type='abc.Snowflake')
                                            timer = find1['bad_word_time_timeout']
                                            us=discord.utils.get(message.guild.members , id = message.author.id)
                                            await us.timeout(Utils.utcnow()+timedelta(seconds=timer), reason='using bad words')
                                            # await us.edit(mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))                                await message.delete()
                                            security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                    else:
                                        warn +=1
                                        if warn == find1['anti_bad_words_warn']:
                                            if find1['security_log_channel'] is not None:
                                                exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                if exist_check is not None:
                                                    embed=discord.Embed(
                                                        title=f"Anti bad words Log",
                                                        description= f"user Action : used bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{message.author.id}>\nusers warn : {warn}\nbot Action: {find1['anti_bad_words_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                    await exist_check.send(embed=embed)

                                            if find1['anti_bad_words_punishment']=='Kick':
                                                ss=discord.Object(message.author.id , type='abc.Snowflake')
                                                await message.guild.kick(ss, reason='using bad words')
                                                await message.delete()
                                                security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                            elif find1['anti_bad_words_punishment']=='Ban':
                                                ss=discord.Object(message.author.id , type='abc.Snowflake')
                                                await message.guild.ban(ss, reason='using bad words')
                                                await message.delete()
                                                security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                            elif find1['anti_bad_words_punishment']=='Timeout':
                                                ss=discord.Object(message.author.id , type='abc.Snowflake')
                                                timer = find1['bad_word_time_timeout']
                                                us=discord.utils.get(message.guild.members , id = message.author.id)
                                                await us.timeout(Utils.utcnow()+timedelta(seconds=timer), reason='using bad words')
                                                # await us.edit(mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))                                    await message.delete()
                                                security.delete_one({"user_id":message.author.id,"anti_bad":True, "guild":message.guild.id})
                                            
                                        else:
                                            security.update_one({'user_id':message.author.id,"anti_bad":True, "guild":message.guild.id} , {'$set':{'warn':warn}})
                                            if find1['security_log_channel'] is not None:
                                                exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                if exist_check is not None:
                                                    embed=discord.Embed(
                                                    title=f"Anti bad words Log",
                                                    description= f"user Action : used bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{message.author.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                    timestamp=datetime.now(),
                                                    color= 0xF6F6F6
                                                    )
                                                    await exist_check.send(embed=embed)

        except:
            pass

        return
    @commands.Cog.listener()
    async def on_message_edit(self,before, after):
        
        try:
            if (find1:= security.find_one({"_id":before.guild.id})):
                if find1['state']==1 and find1['server_invite_detect_security']==True:
                    member = discord.utils.get(after.guild.members , id = before.author.id)
                    if member.id == before.guild.me.id:
                        pass
                    elif member.id == before.guild.owner_id:
                        pass
                    elif before.guild.me.top_role.position <= member.top_role.position:
                        pass
                    else:
                        roles = find1['discord_invite_white_role']
                        user_ids = find1['discord_invite_white_user']
                        check_white_role=False
                        check_white_user=False
                        if roles is not None:
                            for i in roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True
                        if user_ids is not None:
                            for i in user_ids:
                                if i == member.id:
                                    check_white_user = True
                        all_white_roles = find1['all_white_list_role']
                        all_white_users = find1['all_white_list_user']

                        if all_white_roles is not None:
                            for i in all_white_roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True

                        if all_white_users is not None:
                            for i in all_white_users:
                                if i == member.id:
                                    check_white_user = True

                        if check_white_role == True or check_white_user == True:
                            check_white_user = False
                            check_white_role = False
                        else:
                        
                            roles = find1['bad_words']
                            check=False
                            text=after.content.split(' ')
                            for txt in text:
                                if "https://discord.gg" in txt:
                                    check=True
                            
                            if check==True:
                                if find1['security_log_channel'] is not None:
                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                    if exist_check is not None:
                                        embed=discord.Embed(
                                            title=f"discord link invite delete Log",
                                            description= f"user Action : sent an invite link\nuser: <@{before.author.id}>\nbot Action: Delete message",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                            )
                                        await exist_check.send(embed=embed)

                                await after.delete()
                                check=False

            if (find1:= security.find_one({"_id":before.guild.id})):
                if find1['state']==1 and find1['anti_bad_word']==True and find1['anti_bad_words_warn'] is not None and find1['anti_bad_words_punishment'] is not None:
                    member = discord.utils.get(before.guild.members , id = before.author.id)
                    if member.id == before.guild.me.id:
                        pass
                    elif member.id == before.guild.owner_id:
                        pass
                    if before.guild.me.top_role.position <= member.top_role.position:
                        pass
                    else:

                        roles = find1['anti_bad_words_white_role']
                        user_ids = find1['anti_bad_words_white_user']
                        check_white_role=False
                        check_white_user=False
                        if roles is not None:
                            for i in roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True
                        if user_ids is not None:
                            for i in user_ids:
                                if i == member.id:
                                    check_white_user = True

                        all_white_roles = find1['all_white_list_role']
                        all_white_users = find1['all_white_list_user']

                        if all_white_roles is not None:
                            for i in all_white_roles:
                                for j in range(len(member.roles)):
                                    if i == member.roles[j].id:
                                        check_white_role = True

                        if all_white_users is not None:
                            for i in all_white_users:
                                if i == member.id:
                                    check_white_user = True

                        if check_white_role == True or check_white_user == True:
                            check_white_user = False
                            check_white_role = False
                        else:
                        
                            roles = find1['bad_words']
                            check=False
                            text=after.content.split(' ')
                            for i in roles:
                                for j in text:
                                    if i.lower() ==j.lower():
                                        check=True
                            
                            if check==True:
                                if (find2:= security.find_one({"user_id":before.author.id,"anti_bad_edit":True, "guild":before.guild.id})) is not None:
                                    warn=find2['warn']
                                    if warn == find1['anti_bad_words_warn']:
                                        if find1['security_log_channel'] is not None:
                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                            if exist_check is not None:
                                                embed=discord.Embed(
                                                    title=f"Anti bad words edit message Log",
                                                    description= f"user Action : edit message and use bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{after.author.id}>\nusers warn : {warn}\nbot Action: {find1['anti_bad_words_punishment']}",
                                                    timestamp=datetime.now(),
                                                    color= 0xF6F6F6
                                                    )
                                                await exist_check.send(embed=embed)

                                        if find1['anti_bad_words_punishment']=='Kick':
                                            ss=discord.Object(after.author.id , type='abc.Snowflake')
                                            await after.guild.kick(ss, reason='using bad words')
                                            await after.delete()
                                            security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})

                                        elif find1['anti_bad_words_punishment']=='Ban':
                                            ss=discord.Object(after.author.id , type='abc.Snowflake')
                                            await after.guild.ban(ss, reason='using bad words')
                                            await after.delete()
                                            security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})

                                        elif find1['anti_bad_words_punishment']=='Timeout':
                                            ss=discord.Object(after.author.id , type='abc.Snowflake')
                                            timer = find1['bad_word_time_timeout']
                                            # await message.guild.edit(ss,mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))
                                            us=discord.utils.get(message.guild.members , id = message.author.id)
                                            await us.timeout(Utils.utcnow()+timedelta(seconds=timer), reason='using bad words')
                                            # await us.edit(mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))
                                            await after.delete()
                                            security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                    else:
                                        warn +=1
                                        if warn == find1['anti_bad_words_warn']:
                                            if find1['security_log_channel'] is not None:
                                                exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                if exist_check is not None:
                                                    embed=discord.Embed(
                                                        title=f"Anti bad words edit message Log",
                                                        description= f"user Action : edit message and use bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{after.author.id}>\nusers warn : {warn}\nbot Action: {find1['anti_bad_words_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                    await exist_check.send(embed=embed)

                                            if find1['anti_bad_words_punishment']=='Kick':
                                                ss=discord.Object(after.author.id , type='abc.Snowflake')
                                                await after.guild.kick(ss, reason='using bad words')
                                                await after.delete()

                                                security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                            elif find1['anti_bad_words_punishment']=='Ban':
                                                ss=discord.Object(after.author.id , type='abc.Snowflake')
                                                await after.guild.ban(ss, reason='using bad words')
                                                await after.delete()
                                                security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})

                                            elif find1['anti_bad_words_punishment']=='Timeout':
                                                ss=discord.Object(after.author.id , type='abc.Snowflake')
                                                timer = find1['bad_word_time_timeout']
                                                us=discord.utils.get(after.guild.members , id = after.author.id)
                                                await us.timeout(Utils.utcnow()+timedelta(seconds=timer), reason='using bad words')
                                                print (us)
                                                # await us.edit(mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))                                    await message.delete()
                                                security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                            
                                        else:
                                            security.update_one({'user_id':after.author.id, "guild":after.guild.id} , {'$set':{'warn':warn}})
                                            if find1['security_log_channel'] is not None:
                                                exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                if exist_check is not None:
                                                    embed=discord.Embed(
                                                    title=f"Anti bad words edit message Log",
                                                    description= f"user Action : edit message and use bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{after.author.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                    timestamp=datetime.now(),
                                                    color= 0xF6F6F6
                                                    )
                                                    await exist_check.send(embed=embed)


                                else:
                                    security.insert_one({'user_id':after.author.id , "guild":after.guild.id ,"anti_bad_edit":True , "warn":0})
                                    find2= security.find_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                    warn=find2['warn']
                                    if warn == find1['anti_bad_words_warn']:
                                        if find1['security_log_channel'] is not None:
                                            exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                            if exist_check is not None:
                                                embed=discord.Embed(
                                                    title=f"Anti bad words edit message Log",
                                                    description= f"user Action : edit message and use bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{after.author.id}>\nusers warn : {warn}\nbot Action: {find1['anti_bad_words_punishment']}",
                                                    timestamp=datetime.now(),
                                                    color= 0xF6F6F6
                                                    )
                                                await exist_check.send(embed=embed)

                                        if find1['anti_bad_words_punishment']=='Kick':
                                            ss=discord.Object(after.author.id , type='abc.Snowflake')
                                            await after.guild.kick(ss, reason='using bad words')
                                            await after.delete()
                                            security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                        elif find1['anti_bad_words_punishment']=='Ban':
                                            ss=discord.Object(after.author.id , type='abc.Snowflake')
                                            await after.guild.ban(ss, reason='using bad words')
                                            await after.delete()
                                            security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                        elif find1['anti_bad_words_punishment']=='Timeout':
                                            ss=discord.Object(after.author.id , type='abc.Snowflake')
                                            timer = find1['bad_word_time_timeout']
                                            us=discord.utils.get(after.guild.members , id = after.author.id)
                                            await us.timeout(Utils.utcnow()+timedelta(seconds=timer), reason='using bad words')
                                            # await us.edit(mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))                                await message.delete()
                                            security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                    else:
                                        warn +=1
                                        if warn == find1['anti_bad_words_warn']:
                                            if find1['security_log_channel'] is not None:
                                                exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                if exist_check is not None:
                                                    embed=discord.Embed(
                                                        title=f"Anti bad words edit message Log",
                                                        description= f"user Action : edit message and use bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{after.author.id}>\nusers warn : {warn}\nbot Action: {find1['anti_bad_words_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                    await exist_check.send(embed=embed)
                                            if find1['anti_bad_words_punishment']=='Kick':
                                                ss=discord.Object(after.author.id , type='abc.Snowflake')
                                                await after.guild.kick(ss, reason='using bad words')
                                                await after.delete()
                                                security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                            elif find1['anti_bad_words_punishment']=='Ban':
                                                ss=discord.Object(after.author.id , type='abc.Snowflake')
                                                await after.guild.ban(ss, reason='using bad words')
                                                await after.delete()
                                                security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                            elif find1['anti_bad_words_punishment']=='Timeout':
                                                ss=discord.Object(after.author.id , type='abc.Snowflake')
                                                timer = find1['bad_word_time_timeout']
                                                us=discord.utils.get(after.guild.members , id = after.author.id)
                                                await us.timeout(Utils.utcnow()+timedelta(seconds=timer), reason='using bad words')
                                                # await us.edit(mute=True , timed_out_until=Utils.utcnow()+timedelta(seconds=timer))                                    await message.delete()
                                                security.delete_one({"user_id":after.author.id,"anti_bad_edit":True, "guild":after.guild.id})
                                            
                                        else:
                                            security.update_one({'user_id':after.author.id,"anti_bad_edit":True, "guild":after.guild.id} , {'$set':{'warn':warn}})
                                            if find1['security_log_channel'] is not None:
                                                exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                if exist_check is not None:
                                                    embed=discord.Embed(
                                                    title=f"Anti bad words edit message Log",
                                                    description= f"user Action : edit message and use bad words\nwarn limit : {find1['anti_bad_words_warn']}\nuser: <@{after.author.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                    timestamp=datetime.now(),
                                                    color= 0xF6F6F6
                                                    )
                                                    await exist_check.send(embed=embed)
        except:
            pass
        try:
            if after.author.id != self.bot.id:
                if (find:= collection.find_one({"user_id":before.guild.id , 'auto_log_creator':True})):
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['message_edit_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['message_edit_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Message Edit Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Edit Message')
                        embed.add_field(name=f'USER:', value=f'{after.author.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(after.author.created_at , 'R')}" )
                        embed.add_field(name=f'CHANNEL:', value=f'{after.channel.mention}' , inline=False)
                        embed.add_field(name=f'ID:', value=f'```Message ID: {after.id}\nUSER: {after.author.id}```' , inline=False)                
                        embed.set_footer(text=f'USERNAME: {after.author.name}',icon_url=after.author.display_avatar.url)
                        await webhooker.send(embed=embed)

                if (find:= collection.find_one({"user_id":before.guild.id , 'full_log_state':True})):
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Message Edit Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Edit Message')
                        embed.add_field(name=f'USER:', value=f'{after.author.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(after.author.created_at , 'R')}" )
                        embed.add_field(name=f'CHANNEL:', value=f'{after.channel.mention}' , inline=False)
                        embed.add_field(name=f'ID:', value=f'```Message ID: {after.id}\nUSER: {after.author.id}```' , inline=False)                
                        embed.set_footer(text=f'USERNAME: {after.author.name}',icon_url=after.author.display_avatar.url)
                        if channel_check is not None:
                            await webhooker.send(embed=embed)
        except:
            pass
        
        return
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        try:
            if (find:= collection.find_one({"user_id":message.guild.id , 'auto_log_creator':True})):
                tmp_guild = find['user_id']
                tmp_id_channel= find['message_delete_state']
                main_guild=self.bot.get_guild(tmp_guild)
                webhooker_id = find['message_delete_webhook']
                webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                if webhooker is not None:
                    embed=discord.Embed(
                            title=f"Message Delete Log",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                    )
                    embed.add_field(name=f'ACTION:',value=f'Delete Message')
                    embed.add_field(name=f'USER:', value=f'{message.author.mention}')
                    embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(message.author.created_at , 'R')}" )
                    embed.add_field(name=f'CHANNEL:', value=f'{message.channel.mention}' , inline=False)
                    embed.add_field(name=f'Content:', value=f'{message.content}' , inline=False)
                    embed.add_field(name=f'ID:', value=f'```Message ID: {message.id}\nUSER: {message.author.id}```' , inline=False)                
                    embed.set_footer(text=f'USERNAME: {message.author.name}',icon_url=message.author.display_avatar.url)
                    await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":message.guild.id , 'full_log_state':True})):
                tmp_guild = find['user_id']
                channel_check= find['channel']
                main_guild=self.bot.get_guild(tmp_guild)
                webhooker_id = find['full_log_webhook']
                webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                if webhooker is not None:
                    embed=discord.Embed(
                            title=f"Message Delete Log",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                    )
                    embed.add_field(name=f'ACTION:',value=f'Delete Message')
                    embed.add_field(name=f'USER:', value=f'{message.author.mention}')
                    embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(message.author.created_at , 'R')}" )
                    embed.add_field(name=f'CHANNEL:', value=f'{message.channel.mention}' , inline=False)
                    embed.add_field(name=f'Content:', value=f'{message.content}' , inline=False)
                    embed.add_field(name=f'ID:', value=f'```Message ID: {message.id}\nUSER: {message.author.id}```' , inline=False)
                    embed.set_footer(text=f'USERNAME: {message.author.name}',icon_url=message.author.display_avatar.url)
                    if channel_check is not None:
                        await webhooker.send(embed=embed)

        except:
            pass
        
        return
    @commands.Cog.listener()
    async def on_guild_role_create(self,role):
        
        try:
            if (find1:= security.find_one({"_id":role.guild.id})):
                if find1['state']==1 and find1['role_create_warn_limit'] is not None and find1['role_create_enable'] == True:
                    async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_create , limit=1):
                        async for entry2 in role.guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                member = discord.utils.get(role.guild.members , id = entry.user.id)
                                if member.id == role.guild.me.id:
                                    pass
                                elif member.id == role.guild.owner_id:
                                    pass
                                elif role.guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:

                                    roles = find1['role_create_white_role']
                                    user_ids = find1['role_create_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True

                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['role_create_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti role create Log",
                                                        description= f"user Action : create role\nwarn limit : {find1['role_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_create_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)
                                                if find1['role_create_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await role.guild.kick(ss , reason='created a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                                elif find1['role_create_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await role.guild.ban(ss, reason='created a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['role_create_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role create Log",
                                                            description= f"user Action : create role\nwarn limit : {find1['role_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_create_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['role_create_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await role.guild.kick(ss, reason='created a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                                    elif find1['role_create_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await role.guild.ban(ss, reason='created a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"role_create":True, "guild":role.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role create Log",
                                                            description= f"user Action : create role\nwarn limit : {find1['role_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":role.guild.id , "role_create":True , "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                            warn=find2['warn']
                                            if warn == find1['role_create_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti role create Log",
                                                        description= f"user Action : create role\nwarn limit : {find1['role_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_create_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['role_create_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await role.guild.kick(ss, reason='created a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                                elif find1['role_create_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await role.guild.ban(ss, reason='created a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['role_create_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role create Log",
                                                            description= f"user Action : create role\nwarn limit : {find1['role_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_create_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['role_create_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await role.guild.kick(ss, reason='created a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                                    elif find1['role_create_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await role.guild.ban(ss, reason='created a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_create":True, "guild":role.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"role_create":True, "guild":role.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role create Log",
                                                            description= f"user Action : create role\nwarn limit : {find1['role_create_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
        except:
            pass
        try:
            if (find:= collection.find_one({"user_id":role.guild.id , 'auto_log_creator':True})):
                async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_create , limit=1):
                    member = discord.utils.get(role.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['role_create_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['role_create_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Role Create Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Create Role')
                        embed.add_field(name=f'CREATED BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                        embed.add_field(name=f'ROLE NAME:', value=f'{role.mention}' )
                        embed.add_field(name=f'ROLE COLOR:', value=f'{role.color}' , inline=False)
                        embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                        embed.add_field(name=f'Administrator:', value=f'{role.permissions.administrator}' )
                        embed.add_field(name=f'Manage Guild:', value=f'{role.permissions.manage_guild}' )
                        embed.add_field(name=f'Ban member:', value=f'{role.permissions.ban_members}' )
                        embed.add_field(name=f'Kick member:', value=f'{role.permissions.kick_members}' )
                        embed.add_field(name=f'Manage Channels:', value=f'{role.permissions.manage_channels}' )
                        embed.add_field(name=f'Manage Events:', value=f'{role.permissions.manage_events}' )
                        embed.add_field(name=f'Manage Roles:', value=f'{role.permissions.manage_roles}' )
                        embed.add_field(name=f'Timeout member:', value=f'{role.permissions.mute_members}' )
                        embed.add_field(name=f'View audit log:', value=f'{role.permissions.view_audit_log}' )
                        embed.add_field(name=f'Deafen member:', value=f'{role.permissions.deafen_members}' )
                        embed.add_field(name=f'ID:', value=f'```ROLE ID: {role.id}\nUSER: {member.id}```' , inline=False)                
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":role.guild.id , 'full_log_state':True})):
                async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_create , limit=1):
                    member = discord.utils.get(role.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Role Create Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Create Role')
                        embed.add_field(name=f'CREATED BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                        embed.add_field(name=f'ROLE NAME:', value=f'{role.mention}' )
                        embed.add_field(name=f'ROLE COLOR:', value=f'{role.color}' , inline=False)
                        embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                        embed.add_field(name=f'Administrator:', value=f'{role.permissions.administrator}' )
                        embed.add_field(name=f'Manage Guild:', value=f'{role.permissions.manage_guild}' )
                        embed.add_field(name=f'Ban member:', value=f'{role.permissions.ban_members}' )
                        embed.add_field(name=f'Kick member:', value=f'{role.permissions.kick_members}' )
                        embed.add_field(name=f'Manage Channels:', value=f'{role.permissions.manage_channels}' )
                        embed.add_field(name=f'Manage Events:', value=f'{role.permissions.manage_events}' )
                        embed.add_field(name=f'Manage Roles:', value=f'{role.permissions.manage_roles}' )
                        embed.add_field(name=f'Timeout member:', value=f'{role.permissions.mute_members}' )
                        embed.add_field(name=f'View audit log:', value=f'{role.permissions.view_audit_log}' )
                        embed.add_field(name=f'Deafen member:', value=f'{role.permissions.deafen_members}' )
                        embed.add_field(name=f'ID:', value=f'```ROLE ID: {role.id}\nUSER: {member.id}```' , inline=False)                
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)

                        if channel_check is not None:
                            await webhooker.send(embed=embed)

        except:
            pass
            
        return
    @commands.Cog.listener()
    async def on_guild_role_delete(self,role):
        
        try:
            if (find1:= security.find_one({"_id":role.guild.id})):
                if find1['state']==1 and find1['role_delete_warn_limit'] is not None and find1['role_delete_enable'] == True:
                    async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete , limit=1):
                        async for entry2 in role.guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                member = discord.utils.get(role.guild.members , id = entry.user.id)
                                if member.id == role.guild.me.id:
                                    pass
                                elif member.id == role.guild.owner_id:
                                    pass
                                elif role.guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:

                                    roles = find1['role_delete_white_role']
                                    user_ids = find1['role_delete_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True

                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['role_delete_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti role delete Log",
                                                        description= f"user Action : delete role\nwarn limit : {find1['role_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_delete_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)
                                                if find1['role_delete_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await role.guild.kick(ss , reason='delete a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                                elif find1['role_delete_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await role.guild.ban(ss, reason='delete a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['role_delete_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role delete Log",
                                                            description= f"user Action : delete role\nwarn limit : {find1['role_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_delete_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['role_delete_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await role.guild.kick(ss, reason='delete a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                                    elif find1['role_delete_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await role.guild.ban(ss, reason='delete a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"role_delete":True, "guild":role.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role delete Log",
                                                            description= f"user Action : delete role\nwarn limit : {find1['role_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":role.guild.id , "role_delete":True, "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                            warn=find2['warn']
                                            if warn == find1['role_delete_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti role delete Log",
                                                        description= f"user Action : delete role\nwarn limit : {find1['role_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_delete_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['role_update_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await role.guild.kick(ss, reason='delete a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                                elif find1['role_delete_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await role.guild.ban(ss, reason='delete a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['role_delete_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role delete Log",
                                                            description= f"user Action : delete role\nwarn limit : {find1['role_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_delete_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['role_delete_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await role.guild.kick(ss, reason='delete a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                                    elif find1['role_delete_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await role.guild.ban(ss, reason='delete a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_delete":True, "guild":role.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"role_delete":True, "guild":role.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role delete Log",
                                                            description= f"user Action : delete role\nwarn limit : {find1['role_delete_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

        except:
            pass
        try:  #role delete log
            if (find:= collection.find_one({"user_id":role.guild.id , 'auto_log_creator':True})):
                async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete , limit=1):
                    member = discord.utils.get(role.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['role_delete_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['role_delete_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Role Delete Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Delete Role')
                        embed.add_field(name=f'DELETED BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                        embed.add_field(name=f'ROLE NAME:', value=f'{role.name}' )
                        embed.add_field(name=f'ROLE COLOR:', value=f'{role.color}' , inline=False)
                        embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                        embed.add_field(name=f'Administrator:', value=f'{role.permissions.administrator}' )
                        embed.add_field(name=f'Manage Guild:', value=f'{role.permissions.manage_guild}' )
                        embed.add_field(name=f'Ban member:', value=f'{role.permissions.ban_members}' )
                        embed.add_field(name=f'Kick member:', value=f'{role.permissions.kick_members}' )
                        embed.add_field(name=f'Manage Channels:', value=f'{role.permissions.manage_channels}' )
                        embed.add_field(name=f'Manage Events:', value=f'{role.permissions.manage_events}' )
                        embed.add_field(name=f'Manage Roles:', value=f'{role.permissions.manage_roles}' )
                        embed.add_field(name=f'Timeout member:', value=f'{role.permissions.mute_members}' )
                        embed.add_field(name=f'View audit log:', value=f'{role.permissions.view_audit_log}' )
                        embed.add_field(name=f'Deafen member:', value=f'{role.permissions.deafen_members}' )
                        embed.add_field(name=f'ID:', value=f'```ROLE ID: {role.id}\nUSER: {member.id}```' , inline=False)                
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":role.guild.id , 'full_log_state':True})):
                async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete , limit=1):
                    member = discord.utils.get(role.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Role Delete Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Delete Role')
                        embed.add_field(name=f'DELETED BY:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                        embed.add_field(name=f'ROLE NAME:', value=f'{role.name}' )
                        embed.add_field(name=f'ROLE COLOR:', value=f'{role.color}' , inline=False)
                        embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                        embed.add_field(name=f'Administrator:', value=f'{role.permissions.administrator}' )
                        embed.add_field(name=f'Manage Guild:', value=f'{role.permissions.manage_guild}' )
                        embed.add_field(name=f'Ban member:', value=f'{role.permissions.ban_members}' )
                        embed.add_field(name=f'Kick member:', value=f'{role.permissions.kick_members}' )
                        embed.add_field(name=f'Manage Channels:', value=f'{role.permissions.manage_channels}' )
                        embed.add_field(name=f'Manage Events:', value=f'{role.permissions.manage_events}' )
                        embed.add_field(name=f'Manage Roles:', value=f'{role.permissions.manage_roles}' )
                        embed.add_field(name=f'Timeout member:', value=f'{role.permissions.mute_members}' )
                        embed.add_field(name=f'View audit log:', value=f'{role.permissions.view_audit_log}' )
                        embed.add_field(name=f'Deafen member:', value=f'{role.permissions.deafen_members}' )
                        embed.add_field(name=f'ID:', value=f'```ROLE ID: {role.id}\nUSER: {member.id}```' , inline=False)                
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        if channel_check is not None:
                            await webhooker.send(embed=embed)


        except:

            return

        return
    @commands.Cog.listener()
    async def on_scheduled_event_create(self,event): #event create
        try:
            if (find:= collection.find_one({"user_id":event.guild.id , 'auto_log_creator':True})):
                async for entry in event.guild.audit_logs(action=discord.AuditLogAction.scheduled_event_create , limit=1):
                    member = discord.utils.get(event.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['event_create_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['event_create_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Event Creation Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Event Create')
                        embed.add_field(name=f'BY WHO:',value=f'{event.creator.mention}')
                        embed.add_field(name=f'EVENT NAME:',value=f'{event.name}')
                        embed.add_field(name=f'EVENT CHANNEL:',value=f'{event.channel.mention}')
                        embed.add_field(name=f'EVENT ENTITY TYPE:',value=f'{event.entity_type}')
                        embed.add_field(name=f'EVENT PRIVACY LEVEL:',value=f'{event.privacy_level}')
                        embed.add_field(name=f'EVENT START TIME:',value=f"{discord.utils.format_dt(event.start_time , 'R')}" , inline=False)
                        embed.add_field(name=f'EVENT URL:',value=f"{event.url}" , inline=False)
                        embed.add_field(name=f'EVENT STATUS:',value=f'```{event.status}```' , inline=False)
                        embed.add_field(name=f'EVENT DESCRIPTION:',value=f'```{event.description}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {event.creator.name}',icon_url=event.creator.display_avatar.url)

                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":event.guild.id , 'full_log_state':True})):
                async for entry in event.guild.audit_logs(action=discord.AuditLogAction.scheduled_event_create , limit=1):
                    member = discord.utils.get(event.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Event Creation Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Event Create')
                        embed.add_field(name=f'BY WHO:',value=f'{event.creator.mention}')
                        embed.add_field(name=f'EVENT NAME:',value=f'{event.name}')
                        embed.add_field(name=f'EVENT CHANNEL:',value=f'{event.channel.mention}')
                        embed.add_field(name=f'EVENT ENTITY TYPE:',value=f'{event.entity_type}')
                        embed.add_field(name=f'EVENT PRIVACY LEVEL:',value=f'{event.privacy_level}')
                        embed.add_field(name=f'EVENT START TIME:',value=f"{discord.utils.format_dt(event.start_time , 'R')}" , inline=False)
                        embed.add_field(name=f'EVENT URL:',value=f"{event.url}" , inline=False)
                        embed.add_field(name=f'EVENT STATUS:',value=f'```{event.status}```' , inline=False)
                        embed.add_field(name=f'EVENT DESCRIPTION:',value=f'```{event.description}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {event.creator.name}',icon_url=event.creator.display_avatar.url)

                        if channel_check is not None:
                            await webhooker.send(embed=embed)
        except:
            pass

        return
    @commands.Cog.listener()
    async def on_scheduled_event_delete(self,event):  #event deletion
        try:
            if (find:= collection.find_one({"user_id":event.guild.id , 'auto_log_creator':True})):
                async for entry in event.guild.audit_logs(action=discord.AuditLogAction.scheduled_event_delete , limit=1):
                    member = discord.utils.get(event.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['event_delete_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['event_delete_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Event Deletion Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Event Delete')
                        embed.add_field(name=f'BY WHO:',value=f'{event.creator.mention}')
                        embed.add_field(name=f'EVENT NAME:',value=f'{event.name}')
                        embed.add_field(name=f'EVENT CHANNEL:',value=f'{event.channel.mention}')
                        embed.add_field(name=f'EVENT ENTITY TYPE:',value=f'{event.entity_type}')
                        embed.add_field(name=f'EVENT PRIVACY LEVEL:',value=f'{event.privacy_level}')
                        embed.add_field(name=f'EVENT URL:',value=f"{event.url}" , inline=False)
                        embed.add_field(name=f'EVENT STATUS:',value=f'```{event.status}```' , inline=False)
                        embed.add_field(name=f'EVENT DESCRIPTION:',value=f'```{event.description}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {event.creator.name}',icon_url=event.creator.display_avatar.url)

                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":event.guild.id , 'full_log_state':True})):
                async for entry in event.guild.audit_logs(action=discord.AuditLogAction.scheduled_event_delete , limit=1):
                    member = discord.utils.get(event.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Event Deletion Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Event Delete')
                        embed.add_field(name=f'BY WHO:',value=f'{event.creator.mention}')
                        embed.add_field(name=f'EVENT NAME:',value=f'{event.name}')
                        embed.add_field(name=f'EVENT CHANNEL:',value=f'{event.channel.mention}')
                        embed.add_field(name=f'EVENT ENTITY TYPE:',value=f'{event.entity_type}')
                        embed.add_field(name=f'EVENT PRIVACY LEVEL:',value=f'{event.privacy_level}')
                        embed.add_field(name=f'EVENT URL:',value=f"{event.url}" , inline=False)
                        embed.add_field(name=f'EVENT STATUS:',value=f'```{event.status}```' , inline=False)
                        embed.add_field(name=f'EVENT DESCRIPTION:',value=f'```{event.description}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {event.creator.name}',icon_url=event.creator.display_avatar.url)

                        if channel_check is not None:
                            await webhooker.send(embed=embed)
        except:

            return

        return

    @commands.Cog.listener()
    async def on_thread_create(self,thread):
        try:
            if (find:= collection.find_one({"user_id":thread.guild.id , 'auto_log_creator':True})):
                async for entry in thread.guild.audit_logs(action=discord.AuditLogAction.thread_create , limit=1):
                    member = discord.utils.get(thread.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['thread_create_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['thread_create_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Thread Creation Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Thread Create')
                        embed.add_field(name=f'BY WHO:',value=f'{thread.owner.mention}')
                        embed.add_field(name=f'THREAD:',value=f'{thread.mention}')
                        embed.add_field(name=f'INVITABLE:',value=f'{thread.invitable}')
                        embed.add_field(name=f'PARENT CHANNEL:',value=f'{thread.parent.mention}')
                        embed.add_field(name=f'APPLIED TAGS:',value=f'{thread.applied_tags}', inline=False)
                        embed.add_field(name=f'JUMP URL:',value=f'{thread.jump_url}' , inline=False)
                        embed.add_field(name=f'ID:',value=f'```THREAD ID: {thread.id}\nOWNER: {thread.owner_id}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {thread.owner.name}',icon_url=thread.owner.display_avatar.url)
                        
                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":thread.guild.id , 'full_log_state':True})):
                async for entry in thread.guild.audit_logs(action=discord.AuditLogAction.thread_create , limit=1):
                    member = discord.utils.get(thread.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Thread Creation Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Thread Create')
                        embed.add_field(name=f'BY WHO:',value=f'{thread.owner.mention}')
                        embed.add_field(name=f'THREAD:',value=f'{thread.mention}')
                        embed.add_field(name=f'INVITABLE:',value=f'{thread.invitable}')
                        embed.add_field(name=f'PARENT CHANNEL:',value=f'{thread.parent.mention}')
                        embed.add_field(name=f'APPLIED TAGS:',value=f'{thread.applied_tags}', inline=False)
                        embed.add_field(name=f'JUMP URL:',value=f'{thread.jump_url}' , inline=False)
                        embed.add_field(name=f'ID:',value=f'```THREAD ID: {thread.id}\nOWNER: {thread.owner_id}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {thread.owner.name}',icon_url=thread.owner.display_avatar.url)
                        
                        if channel_check is not None:
                            await webhooker.send(embed=embed)

        except:

            return

        return
    @commands.Cog.listener()
    async def on_raw_thread_delete(self,payload):
        try:
            if (find:= collection.find_one({"user_id":payload.thread.guild.id , 'auto_log_creator':True})):
                async for entry in payload.thread.guild.audit_logs(action=discord.AuditLogAction.thread_delete , limit=1):
                    member = discord.utils.get(payload.thread.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['thread_delete_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['thread_delete_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Thread Deletion Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Thread Delete')
                        embed.add_field(name=f'BY WHO:',value=f'{payload.thread.owner.mention}')
                        embed.add_field(name=f'THREAD:',value=f'{payload.thread.name}')
                        embed.add_field(name=f'INVITABLE:',value=f'{payload.thread.invitable}')
                        embed.add_field(name=f'PARENT CHANNEL:',value=f'{payload.thread.parent.mention}')
                        embed.add_field(name=f'APPLIED TAGS:',value=f'{payload.thread.applied_tags}', inline=False)
                        embed.add_field(name=f'ID:',value=f'```THREAD ID: {payload.thread.id}\nOWNER: {payload.thread.owner_id}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {payload.thread.owner.name}',icon_url=payload.thread.owner.display_avatar.url)
                        
                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":payload.thread.guild.id , 'full_log_state':True})):
                async for entry in payload.thread.guild.audit_logs(action=discord.AuditLogAction.thread_delete , limit=1):
                    member = discord.utils.get(payload.thread.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Thread Deletion Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Thread Delete')
                        embed.add_field(name=f'BY WHO:',value=f'{payload.thread.owner.mention}')
                        embed.add_field(name=f'THREAD:',value=f'{payload.thread.name}')
                        embed.add_field(name=f'INVITABLE:',value=f'{payload.thread.invitable}')
                        embed.add_field(name=f'PARENT CHANNEL:',value=f'{payload.thread.parent.mention}')
                        embed.add_field(name=f'APPLIED TAGS:',value=f'{payload.thread.applied_tags}', inline=False)
                        embed.add_field(name=f'ID:',value=f'```THREAD ID: {thread.id}\nOWNER: {payload.thread.owner_id}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {payload.thread.owner.name}',icon_url=payload.thread.owner.display_avatar.url)
                        
                        if channel_check is not None:
                            await webhooker.send(embed=embed)
        except:

            return

        return
    @commands.Cog.listener()
    async def on_raw_thread_update(self,payload):
        try:
            if (find:= collection.find_one({"user_id":payload.thread.guild.id , 'auto_log_creator':True})):
                async for entry in payload.thread.guild.audit_logs(action=discord.AuditLogAction.thread_update , limit=1):
                    member = discord.utils.get(payload.thread.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['thread_update_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['thread_update_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Thread Deletion Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Thread Update')
                        embed.add_field(name=f'BY WHO:',value=f'{payload.thread.owner.mention}')
                        embed.add_field(name=f'THREAD:',value=f'{payload.thread.name}')
                        embed.add_field(name=f'INVITABLE:',value=f'{payload.thread.invitable}')
                        embed.add_field(name=f'PARENT CHANNEL:',value=f'{payload.thread.parent.mention}')
                        embed.add_field(name=f'APPLIED TAGS:',value=f'{payload.thread.applied_tags}', inline=False)
                        embed.add_field(name=f'JUMP URL:',value=f'{payload.thread.jump_url}' , inline=False)
                        embed.add_field(name=f'ID:',value=f'```THREAD ID: {payload.thread.id}\nOWNER: {payload.thread.owner_id}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {payload.thread.owner.name}',icon_url=payload.thread.owner.display_avatar.url)
                        
                        await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":payload.thread.guild.id , 'full_log_state':True})):
                async for entry in payload.thread.guild.audit_logs(action=discord.AuditLogAction.thread_delete , limit=1):
                    member = discord.utils.get(payload.thread.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Thread Deletion Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Thread Update')
                        embed.add_field(name=f'BY WHO:',value=f'{payload.thread.owner.mention}')
                        embed.add_field(name=f'THREAD:',value=f'{payload.thread.name}')
                        embed.add_field(name=f'INVITABLE:',value=f'{payload.thread.invitable}')
                        embed.add_field(name=f'PARENT CHANNEL:',value=f'{payload.thread.parent.mention}')
                        embed.add_field(name=f'APPLIED TAGS:',value=f'{payload.thread.applied_tags}', inline=False)
                        embed.add_field(name=f'JUMP URL:',value=f'{payload.thread.jump_url}' , inline=False)
                        embed.add_field(name=f'ID:',value=f'```THREAD ID: {payload.thread.id}\nOWNER: {payload.thread.owner_id}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {payload.thread.owner.name}',icon_url=payload.thread.owner.display_avatar.url)
                        
                        if channel_check is not None:
                            await webhooker.send(embed=embed)
        except:
            pass

        return

    @commands.Cog.listener()  #join and left voice log
    async def on_voice_state_update(self,member, before, after):
        try:
            if (find:= collection.find_one({"user_id":member.guild.id , 'auto_log_creator':True})):
                if before.channel is None and after.channel is not None:
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['voice_update_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['voice_update_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Voice Join/Left Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Join Voice')
                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}')
                        embed.add_field(name=f'CHANNEL TYPE:',value=f'{after.channel.type}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" ,inline=False)
                        embed.add_field(name=f'Joined at:' , value=f"{discord.utils.format_dt(member.joined_at , 'R')}" )
                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        embed.set_thumbnail(url=member.display_avatar.url)
                        await webhooker.send(embed=embed)
            
                elif before.channel is not None and after.channel is None:
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['voice_update_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['voice_update_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Voice Join/Left Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Left Voice')
                        embed.add_field(name=f'CHANNEL:',value=f'{before.channel.mention}')
                        embed.add_field(name=f'CHANNEL TYPE:',value=f'{before.channel.type}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" ,inline=False)
                        embed.add_field(name=f'Joined at:' , value=f"{discord.utils.format_dt(member.joined_at , 'R')}" )
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {before.channel.id}\nUSER: {member.id}```' , inline=False)

                        embed.set_thumbnail(url=member.display_avatar.url)
                        await webhooker.send(embed=embed)

                async for entry in member.guild.audit_logs(action=discord.AuditLogAction.member_update , limit=1):
                    async for entry2 in member.guild.audit_logs(limit=1):
                        if entry.action == entry2.action:
                            if entry.target.id == member.id:
                                tmp_guild = find['user_id']
                                main_guild=self.bot.get_guild(tmp_guild)
                                member1 = discord.utils.get(member.guild.members , id = entry.user.id)
                                webhooker_id = find['member_update_webhook']
                                webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                                if webhooker is not None:
                                    embed=discord.Embed(
                                            title=f"Member Update Log",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                    )
                                    if before.deaf==False and after.deaf == True:
                                        embed.add_field(name=f'ACTION:',value=f'Deafen')
                                        embed.add_field(name=f'USER:',value=f'{member.mention}')
                                        embed.add_field(name=f'BY WHO:',value=f'{member1.mention}')
                                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}' , inline=False)
                                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                        await webhooker.send(embed=embed)
                                    if before.mute==False and after.mute == True:
                                        embed.add_field(name=f'ACTION:',value=f'Mute')
                                        embed.add_field(name=f'USER:',value=f'{member.mention}')
                                        embed.add_field(name=f'BY WHO:',value=f'{member1.mention}')
                                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}' , inline=False)
                                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                        await webhooker.send(embed=embed)
                                    if before.deaf==True and after.deaf == False:
                                        embed.add_field(name=f'ACTION:',value=f'Remove Deafen')
                                        embed.add_field(name=f'USER:',value=f'{member.mention}')
                                        embed.add_field(name=f'BY WHO:',value=f'{member1.mention}')
                                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}' , inline=False)
                                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                        await webhooker.send(embed=embed)
                                    if before.mute==True and after.mute == False:
                                        embed.add_field(name=f'ACTION:',value=f'Remove Mute')
                                        embed.add_field(name=f'USER:',value=f'{member.mention}')
                                        embed.add_field(name=f'BY WHO:',value=f'{member1.mention}')
                                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}' , inline=False)
                                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                        await webhooker.send(embed=embed)


            if (find:= collection.find_one({"user_id":member.guild.id , 'full_log_state':True})):
                if before.channel is None and after.channel is not None:
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Voice Join/Left Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Join Voice')
                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}')
                        embed.add_field(name=f'CHANNEL TYPE:',value=f'{after.channel.type}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" ,inline=False)
                        embed.add_field(name=f'Joined at:' , value=f"{discord.utils.format_dt(member.joined_at , 'R')}" )
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                        embed.set_thumbnail(url=member.display_avatar.url)
                        if channel_check is not None:
                            await webhooker.send(embed=embed)
            
                elif before.channel is not None and after.channel is None:
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Voice Join/Left Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        embed.add_field(name=f'ACTION:',value=f'Left Voice')
                        embed.add_field(name=f'CHANNEL:',value=f'{before.channel.mention}')
                        embed.add_field(name=f'CHANNEL TYPE:',value=f'{before.channel.type}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" ,inline=False)
                        embed.add_field(name=f'Joined at:' , value=f"{discord.utils.format_dt(member.joined_at , 'R')}" )
                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {before.channel.id}\nUSER: {member.id}```' , inline=False)
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                        embed.set_thumbnail(url=member.display_avatar.url)
                        if channel_check is not None:
                            await webhooker.send(embed=embed)

                async for entry in member.guild.audit_logs(action=discord.AuditLogAction.member_update , limit=1):
                    async for entry2 in member.guild.audit_logs(limit=1):
                        if entry.action == entry2.action:
                            if entry.target.id == member.id:
                                tmp_guild = find['user_id']
                                main_guild=self.bot.get_guild(tmp_guild)
                                channel_check= find['channel']
                                member1 = discord.utils.get(member.guild.members , id = entry.user.id)
                                webhooker_id = find['full_log_webhook']
                                webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                                if webhooker is not None:
                                    embed=discord.Embed(
                                            title=f"Member Update Log",
                                            timestamp=datetime.now(),
                                            color= 0xF6F6F6
                                    )
                                    if before.deaf==False and after.deaf == True:
                                        embed.add_field(name=f'ACTION:',value=f'Deafen')
                                        embed.add_field(name=f'USER:',value=f'{member.mention}')
                                        embed.add_field(name=f'BY WHO:',value=f'{member1.mention}')
                                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}' , inline=False)
                                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                        if channel_check is not None:
                                            await webhooker.send(embed=embed)
                                    if before.mute==False and after.mute == True:
                                        embed.add_field(name=f'ACTION:',value=f'Mute')
                                        embed.add_field(name=f'USER:',value=f'{member.mention}')
                                        embed.add_field(name=f'BY WHO:',value=f'{member1.mention}')
                                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}' , inline=False)
                                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                        if channel_check is not None:
                                            await webhooker.send(embed=embed)
                                    if before.deaf==True and after.deaf == False:
                                        embed.add_field(name=f'ACTION:',value=f'Remove Deafen')
                                        embed.add_field(name=f'USER:',value=f'{member.mention}')
                                        embed.add_field(name=f'BY WHO:',value=f'{member1.mention}')
                                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}' , inline=False)
                                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                        if channel_check is not None:
                                            await webhooker.send(embed=embed)
                                    if before.mute==True and after.mute == False:
                                        embed.add_field(name=f'ACTION:',value=f'Remove Mute')
                                        embed.add_field(name=f'USER:',value=f'{member.mention}')
                                        embed.add_field(name=f'BY WHO:',value=f'{member1.mention}')
                                        embed.add_field(name=f'CHANNEL:',value=f'{after.channel.mention}' , inline=False)
                                        embed.add_field(name=f'ID:',value=f'```CHANNEL: {after.channel.id}\nUSER: {member.id}```' , inline=False)

                                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                                        if channel_check is not None:
                                            await webhooker.send(embed=embed)

        except:

            return

        return
    @commands.Cog.listener()
    async def on_guild_role_update(self,before, after): #role update
        # await asyncio.sleep(1)
        try:
            if (find1:= security.find_one({"_id":before.guild.id})):
                if find1['state']==1 and find1['role_update_warn_limit'] is not None and find1['role_update_enable'] == True:
                    async for entry in before.guild.audit_logs(action=discord.AuditLogAction.role_update , limit=1):
                        async for entry2 in before.guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                # member = await before.guild.fetch_member(entry.user.id)
                                member = discord.utils.get(before.guild.members , id = entry.user.id)
                                if member.id == after.guild.me.id:
                                    pass
                                elif member.id == after.guild.owner_id:
                                    pass
                                if after.guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:

                                    roles = find1['role_update_white_role']
                                    user_ids = find1['role_update_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True

                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:
                                        if (find2:= security.find_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['role_update_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti role update Log",
                                                        description= f"user Action : role update\nwarn limit : {find1['role_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_update_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['role_update_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await before.guild.kick(ss , reason='update a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                                elif find1['role_update_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await before.guild.ban(ss, reason='update a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['role_update_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role update Log",
                                                            description= f"user Action : role update\nwarn limit : {find1['role_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_update_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['role_update_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await before.guild.kick(ss, reason='update a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                                    elif find1['role_update_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await before.guild.ban(ss, reason='update a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"role_update":True, "guild":before.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role update Log",
                                                            description= f"user Action : role update\nwarn limit : {find1['role_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":before.guild.id, "role_update":True , "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                            warn=find2['warn']
                                            if warn == find1['role_update_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti role update Log",
                                                        description= f"user Action : role update\nwarn limit : {find1['role_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['role_update_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['role_update_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await before.guild.kick(ss, reason='update a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                                elif find1['role_update_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await before.guild.ban(ss, reason='update a role from server')
                                                    security.delete_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['role_update_warn_limit']:
                                                    if find1['role_update_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await before.guild.kick(ss, reason='update a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                                    elif find1['role_update_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await before.guild.ban(ss, reason='update a role from server')
                                                        security.delete_one({"user_id":entry.user.id,"role_update":True, "guild":before.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"role_update":True, "guild":before.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti role update Log",
                                                            description= f"user Action : role update\nwarn limit : {find1['role_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)
        except:
            pass
       

        try:

            if (find:= collection.find_one({"user_id":before.guild.id , 'auto_log_creator':True})):
                async for entry in before.guild.audit_logs(action=discord.AuditLogAction.role_update , limit=1):
                    member = discord.utils.get(before.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['role_update_state']
                    if before.name != after.name:
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['role_update_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Role Update Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            new_li=[]
                            for i in after.permissions:
                                if i not in before.permissions:
                                    new_li.append(i)
                            embed.add_field(name=f'ACTION:',value=f'Update Role')
                            embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'ROLE NAME:', value=f'{after.mention}' )
                            embed.add_field(name=f'ROLE COLOR:', value=f'{after.color}' , inline=False)
                            embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                            embed.add_field(name=f'Administrator:', value=f'{after.permissions.administrator}' )
                            embed.add_field(name=f'Manage Guild:', value=f'{after.permissions.manage_guild}' )
                            embed.add_field(name=f'Ban member:', value=f'{after.permissions.ban_members}' )
                            embed.add_field(name=f'Kick member:', value=f'{after.permissions.kick_members}' )
                            embed.add_field(name=f'Manage Channels:', value=f'{after.permissions.manage_channels}' )
                            embed.add_field(name=f'Manage Events:', value=f'{after.permissions.manage_events}' )
                            embed.add_field(name=f'Manage Roles:', value=f'{after.permissions.manage_roles}' )
                            embed.add_field(name=f'Timeout member:', value=f'{after.permissions.mute_members}' )
                            embed.add_field(name=f'View audit log:', value=f'{after.permissions.view_audit_log}' )
                            embed.add_field(name=f'Deafen member:', value=f'{after.permissions.deafen_members}' )
                            embed.add_field(name=f'CHANGES:', value=f'```NAME: {before.name} ---> {after.name}\n{new_li}```' , inline=False)                
                            embed.add_field(name=f'ID:', value=f'```ROLE ID: {after.id}\nUSER: {member.id}```' , inline=False)                
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            await webhooker.send(embed=embed)
                    elif before.permissions != after.permissions:
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['role_update_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Role Update Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            new_li=[]
                            for i in after.permissions:
                                if i not in before.permissions:
                                    new_li.append(i)
                            embed.add_field(name=f'ACTION:',value=f'Update Role')
                            embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'ROLE NAME:', value=f'{after.mention}' )
                            embed.add_field(name=f'ROLE COLOR:', value=f'{after.color}' , inline=False)
                            embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                            embed.add_field(name=f'Administrator:', value=f'{after.permissions.administrator}' )
                            embed.add_field(name=f'Manage Guild:', value=f'{after.permissions.manage_guild}' )
                            embed.add_field(name=f'Ban member:', value=f'{after.permissions.ban_members}' )
                            embed.add_field(name=f'Kick member:', value=f'{after.permissions.kick_members}' )
                            embed.add_field(name=f'Manage Channels:', value=f'{after.permissions.manage_channels}' )
                            embed.add_field(name=f'Manage Events:', value=f'{after.permissions.manage_events}' )
                            embed.add_field(name=f'Manage Roles:', value=f'{after.permissions.manage_roles}' )
                            embed.add_field(name=f'Timeout member:', value=f'{after.permissions.mute_members}' )
                            embed.add_field(name=f'View audit log:', value=f'{after.permissions.view_audit_log}' )
                            embed.add_field(name=f'Deafen member:', value=f'{after.permissions.deafen_members}' )
                            embed.add_field(name=f'CHANGES:', value=f'```{new_li}```' , inline=False)                
                            embed.add_field(name=f'ID:', value=f'```ROLE ID: {after.id}\nUSER: {member.id}```' , inline=False)                
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            await webhooker.send(embed=embed)

                    elif before.color != after.color:
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['role_update_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Role Update Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            new_li=[]
                            for i in after.permissions:
                                if i not in before.permissions:
                                    new_li.append(i)
                            embed.add_field(name=f'ACTION:',value=f'Update Role')
                            embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'ROLE NAME:', value=f'{after.mention}' )
                            embed.add_field(name=f'ROLE COLOR:', value=f'{after.color}' , inline=False)
                            embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                            embed.add_field(name=f'Administrator:', value=f'{after.permissions.administrator}' )
                            embed.add_field(name=f'Manage Guild:', value=f'{after.permissions.manage_guild}' )
                            embed.add_field(name=f'Ban member:', value=f'{after.permissions.ban_members}' )
                            embed.add_field(name=f'Kick member:', value=f'{after.permissions.kick_members}' )
                            embed.add_field(name=f'Manage Channels:', value=f'{after.permissions.manage_channels}' )
                            embed.add_field(name=f'Manage Events:', value=f'{after.permissions.manage_events}' )
                            embed.add_field(name=f'Manage Roles:', value=f'{after.permissions.manage_roles}' )
                            embed.add_field(name=f'Timeout member:', value=f'{after.permissions.mute_members}' )
                            embed.add_field(name=f'View audit log:', value=f'{after.permissions.view_audit_log}' )
                            embed.add_field(name=f'Deafen member:', value=f'{after.permissions.deafen_members}' )
                            embed.add_field(name=f'CHANGES:', value=f'```color change: {before.color} ---> {after.color}```' , inline=False)                
                            embed.add_field(name=f'ID:', value=f'```ROLE ID: {after.id}\nUSER: {member.id}```' , inline=False)                
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":before.guild.id , 'full_log_state':True})):
                async for entry in before.guild.audit_logs(action=discord.AuditLogAction.role_update , limit=1):
                    # member = await before.guild.fetch_member(entry.user.id)
                    member = discord.utils.get(before.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    if before.name != after.name:
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['full_log_webhook']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Role Update Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            flag=False
                            if before.color != after.color:
                                flag=True
                            new_li=[]
                            for i in after.permissions:
                                if i not in before.permissions:
                                    new_li.append(i)
                            embed.add_field(name=f'ACTION:',value=f'Update Role')
                            embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'ROLE NAME:', value=f'{after.mention}' )
                            embed.add_field(name=f'ROLE COLOR:', value=f'{after.color}' , inline=False)
                            embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                            embed.add_field(name=f'Administrator:', value=f'{after.permissions.administrator}' )
                            embed.add_field(name=f'Manage Guild:', value=f'{after.permissions.manage_guild}' )
                            embed.add_field(name=f'Ban member:', value=f'{after.permissions.ban_members}' )
                            embed.add_field(name=f'Kick member:', value=f'{after.permissions.kick_members}' )
                            embed.add_field(name=f'Manage Channels:', value=f'{after.permissions.manage_channels}' )
                            embed.add_field(name=f'Manage Events:', value=f'{after.permissions.manage_events}' )
                            embed.add_field(name=f'Manage Roles:', value=f'{after.permissions.manage_roles}' )
                            embed.add_field(name=f'Timeout member:', value=f'{after.permissions.mute_members}' )
                            embed.add_field(name=f'View audit log:', value=f'{after.permissions.view_audit_log}' )
                            embed.add_field(name=f'Deafen member:', value=f'{after.permissions.deafen_members}' )
                            embed.add_field(name=f'CHANGES:', value=f'```NAME: {before.name} ---> {after.name}\nColor Change:{flag}\nPermissions Changed:\n{new_li}```' , inline=False)                
                            embed.add_field(name=f'ID:', value=f'```ROLE ID: {after.id}\nUSER: {member.id}```' , inline=False)                
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            if channel_check is not None:
                                await webhooker.send(embed=embed)
                    elif before.permissions != after.permissions:
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['full_log_webhook']
                        channel_check= find['channel']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Role Update Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            flag=False
                            if before.color != after.color:
                                flag=True
                            new_li=[]
                            for i in after.permissions:
                                if i not in before.permissions:
                                    new_li.append(i)
                            embed.add_field(name=f'ACTION:',value=f'Update Role')
                            embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'ROLE NAME:', value=f'{after.mention}' )
                            embed.add_field(name=f'ROLE COLOR:', value=f'{after.color}' , inline=False)
                            embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                            embed.add_field(name=f'Administrator:', value=f'{after.permissions.administrator}' )
                            embed.add_field(name=f'Manage Guild:', value=f'{after.permissions.manage_guild}' )
                            embed.add_field(name=f'Ban member:', value=f'{after.permissions.ban_members}' )
                            embed.add_field(name=f'Kick member:', value=f'{after.permissions.kick_members}' )
                            embed.add_field(name=f'Manage Channels:', value=f'{after.permissions.manage_channels}' )
                            embed.add_field(name=f'Manage Events:', value=f'{after.permissions.manage_events}' )
                            embed.add_field(name=f'Manage Roles:', value=f'{after.permissions.manage_roles}' )
                            embed.add_field(name=f'Timeout member:', value=f'{after.permissions.mute_members}' )
                            embed.add_field(name=f'View audit log:', value=f'{after.permissions.view_audit_log}' )
                            embed.add_field(name=f'Deafen member:', value=f'{after.permissions.deafen_members}' )
                            embed.add_field(name=f'CHANGES:', value=f'```Color Change:{flag}\nPermissions Changed:\n{new_li}```' , inline=False)                
                            embed.add_field(name=f'ID:', value=f'```ROLE ID: {after.id}\nUSER: {member.id}```' , inline=False)                
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            if channel_check is not None:
                                await webhooker.send(embed=embed)

                    elif before.color != after.color:
                        main_guild=self.bot.get_guild(tmp_guild)
                        webhooker_id = find['full_log_webhook']
                        channel_check= find['channel']
                        webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                        if webhooker is not None:
                            embed=discord.Embed(
                                    title=f"Role Update Log",
                                    timestamp=datetime.now(),
                                    color= 0xF6F6F6
                            )
                            new_li=[]
                            for i in after.permissions:
                                if i not in before.permissions:
                                    new_li.append(i)
                            embed.add_field(name=f'ACTION:',value=f'Update Role')
                            embed.add_field(name=f'UPDATED BY:', value=f'{member.mention}')
                            embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                            embed.add_field(name=f'ROLE NAME:', value=f'{after.mention}' )
                            embed.add_field(name=f'ROLE COLOR:', value=f'{after.color}' , inline=False)
                            embed.add_field(name=f'IMPORTANT PERMISSIONS LOG:', value='' , inline=False)
                            embed.add_field(name=f'Administrator:', value=f'{after.permissions.administrator}' )
                            embed.add_field(name=f'Manage Guild:', value=f'{after.permissions.manage_guild}' )
                            embed.add_field(name=f'Ban member:', value=f'{after.permissions.ban_members}' )
                            embed.add_field(name=f'Kick member:', value=f'{after.permissions.kick_members}' )
                            embed.add_field(name=f'Manage Channels:', value=f'{after.permissions.manage_channels}' )
                            embed.add_field(name=f'Manage Events:', value=f'{after.permissions.manage_events}' )
                            embed.add_field(name=f'Manage Roles:', value=f'{after.permissions.manage_roles}' )
                            embed.add_field(name=f'Timeout member:', value=f'{after.permissions.mute_members}' )
                            embed.add_field(name=f'View audit log:', value=f'{after.permissions.view_audit_log}' )
                            embed.add_field(name=f'Deafen member:', value=f'{after.permissions.deafen_members}' )
                            embed.add_field(name=f'CHANGES:', value=f'```color change: {before.color} ---> {after.color}\nPermissions Changed:\n{new_li}```' , inline=False)                
                            embed.add_field(name=f'ID:', value=f'```ROLE ID: {after.id}\nUSER: {member.id}```' , inline=False)                
                            embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)
                            if channel_check is not None:
                                await webhooker.send(embed=embed)

        except:

            return
        
        return


    @commands.Cog.listener() #log invite sakhtan
    async def on_invite_create(self,invite):
        try:
            if (find:= collection.find_one({"user_id":invite.guild.id , 'auto_log_creator':True})):
                tmp_guild = find['user_id']
                tmp_id_channel= find['invite_create_state']
                main_guild=self.bot.get_guild(tmp_guild)
                webhooker_id = find['invite_create_webhook']
                webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                if webhooker is not None:
                    embed=discord.Embed(
                            title=f"Invite Creation Log",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                    )
                    max_uses = invite.max_uses
                    if max_uses == 0:
                        max_uses ='unlimited'
                    
                    embed.add_field(name=f'ACTION:',value=f'Create Invite')
                    embed.add_field(name=f'BY WHO:', value=f'{invite.inviter.mention}')
                    embed.add_field(name=f'FROM CHANNEL:', value=f'{invite.channel.mention}')
                    embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(invite.inviter.created_at , 'R')}" )
                    embed.add_field(name=f'EXPIRES IN:', value=f'{invite.max_age}s')
                    embed.add_field(name=f'MAX USES:', value=f'{max_uses}')
                    embed.add_field(name=f'URL:', value=f'{invite.url}' , inline=False)
                    embed.add_field(name=f'ID:', value=f'```ansi\n[2;34mUSER:{invite.inviter.id}\nCHANNEL:{invite.channel.id}[0m```' , inline=False)
                    embed.set_thumbnail(url=invite.inviter.display_avatar.url)
                    embed.set_footer(text=f'USERNAME: {invite.inviter.name}',icon_url=invite.inviter.display_avatar.url)


                    await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":invite.guild.id , 'full_log_state':True})):
                tmp_guild = find['user_id']
                channel_check= find['channel']
                main_guild=self.bot.get_guild(tmp_guild)
                webhooker_id = find['full_log_webhook']
                webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                if webhooker is not None:
                    embed=discord.Embed(
                            title=f"Invite Creation Log",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                    )
                    max_uses = invite.max_uses
                    if max_uses == 0:
                        max_uses ='unlimited'
                    
                    embed.add_field(name=f'ACTION:',value=f'Create Invite')
                    embed.add_field(name=f'BY WHO:', value=f'{invite.inviter.mention}')
                    embed.add_field(name=f'FROM CHANNEL:', value=f'{invite.channel.mention}')
                    embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(invite.inviter.created_at , 'R')}" )
                    embed.add_field(name=f'EXPIRES IN:', value=f'{invite.max_age}s')
                    embed.add_field(name=f'MAX USES:', value=f'{max_uses}')
                    embed.add_field(name=f'URL:', value=f'{invite.url}' , inline=False)
                    embed.add_field(name=f'ID:', value=f'```ansi\n[2;34mUSER:{invite.inviter.id}\nCHANNEL:{invite.channel.id}[0m```' , inline=False)
                    embed.set_thumbnail(url=invite.inviter.display_avatar.url)
                    embed.set_footer(text=f'USERNAME: {invite.inviter.name}',icon_url=invite.inviter.display_avatar.url)

                    if channel_check is not None:
                        await webhooker.send(embed=embed)

        except:

            return

        return

    @commands.Cog.listener() #join to sv jadid
    async def on_guild_join(self,guild):
        try:
            flag=False
            if (find:= new_GUILD.find_one({"owner":guild.owner_id})):
                general = guild.text_channels
                if general is not None:
                    for i in general:
                        if i.permissions_for(guild.me).send_messages:
                            embed=discord.Embed(
                            title=f"APA Bot",
                            description= f"Owner i see you added me in another server before i cant be in the servers with the same owner then i guess i should say bye",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                            )
                            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
                            embed.set_image(url='https://cdn.discordapp.com/attachments/1135103098805817477/1135105421644943400/giphy.gif')
                            await i.send(embed=embed)
                            await guild.leave()
                            break
            else:
                new_GUILD.insert_one({'_id':guild.id ,'owner':guild.owner_id})
                general = guild.text_channels
                if general is not None:
                    for i in general:
                        if i.permissions_for(guild.me).send_messages:
                            embed=discord.Embed(
                            title=f"APA Bot",
                            description= f"🤖thanks for inviting me\n\n🌀 APA AIO Bot for Security , Moderation , Custom welcome and ...\n\n🌀 if you use our security feature make sure to read our help and install and config all features if you want to be safe againts any kind of attack and pls report us if you had any problem with the bot or if you have a suggestion\n\n🌀 use </help:1134780677670310004> to see our guide \n\n📌make sure to join our support server:\n\nhttps://discord.gg/te986KRP8A",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                            )
                            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
                            embed.set_image(url='https://cdn.discordapp.com/attachments/1135103098805817477/1135105421644943400/giphy.gif')
                            await i.send(embed=embed)
                            flag=True
                            break
            
            if flag==True:
                if (find1:= new_GUILD.find_one({"_id":1})):
                    counter = find1['count_guilds']
                    counter+=1
                    new_GUILD.update_one({'_id':1} ,{"$set":{'count_guilds':counter}})
                else:
                    new_GUILD.insert_one({'_id':1 ,'count_guilds':1})

        except:
            pass

      
        return

    @commands.Cog.listener() #join to sv jadid
    async def on_guild_remove(self,guild):
        try:
            if (find1:= new_GUILD.find_one({"_id":1})):
                counter = find1['count_guilds']
                counter-=1
                new_GUILD.update_one({'_id':1} ,{"$set":{'count_guilds':counter}})
                new_GUILD.delete_one({'_id':guild.id})
            if (find1:= new_GUILD.find_one({"_id":guild.id})):
                new_GUILD.delete_one({"_id":guild.id})
            if (find2:= collection.find_one({"_id":guild.id})):
                collection.delete_one({'_id':guild.id})
                collection.delete_one({'state':True , 'guild_id':guild.id})
            if (find3:= security.find_one({"_id":guild.id})):
                security.delete_one({'_id':guild.id})
                security.delete_many({'guild':guild.id})
            if (find4:= welcome.find_one({"_id":guild.id})):
                welcome.delete_one({'_id':guild.id})
            if (find4:= fun.find_one({"_id":guild.id})):
                fun.delete_one({'_id':guild.id})
        except:
            pass


            




    @commands.Cog.listener() #channel update
    async def on_guild_channel_update(self,before, after):
        try:
            if (find1:= security.find_one({"_id":before.guild.id})):
                if find1['state']==1 and find1['channel_update_warn_limit'] is not None and find1['channel_update_enable'] == True:
                    async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_update , limit=1):
                        async for entry2 in before.guild.audit_logs(limit=1):
                            if entry.action == entry2.action and entry.user.id == entry2.user.id:
                                member = discord.utils.get(before.guild.members , id = entry.user.id)
                                if member.id == after.guild.me.id:
                                    pass
                                elif member.id == after.guild.owner_id:
                                    pass
                                if after.guild.me.top_role.position <= member.top_role.position:
                                    pass
                                else:

                                    roles = find1['channel_update_white_role']
                                    user_ids = find1['channel_update_white_user']
                                    check_white_role=False
                                    check_white_user=False
                                    if roles is not None:
                                        for i in roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True
                                    if user_ids is not None:
                                        for i in user_ids:
                                            if i == member.id:
                                                check_white_user = True

                                    all_white_roles = find1['all_white_list_role']
                                    all_white_users = find1['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True


                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False
                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find1['channel_update_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti channel update Log",
                                                        description= f"user Action : update channel {after.name}\nwarn limit : {find1['channel_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_update_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['channel_update_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await before.guild.kick(ss,reason='update a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                                elif find1['channel_update_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await before.guild.ban(ss,reason='update a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['channel_update_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel update Log",
                                                            description= f"user Action : update channel {after.name}\nwarn limit : {find1['channel_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_update_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['channel_update_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await before.guild.kick(ss,reason='update a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                                    elif find1['channel_update_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await before.guild.ban(ss,reason='update a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"channel_update":True, "guild":before.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel update Log",
                                                            description= f"user Action : update channel {after.name}\nwarn limit : {find1['channel_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":before.guild.id , "channel_update":True, "warn":0})
                                            find2= security.find_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                            warn=find2['warn']
                                            if warn == find1['channel_update_warn_limit']:
                                                if find1['security_log_channel'] is not None:
                                                    exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                    if exist_check is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti channel update Log",
                                                        description= f"user Action : update channel {after.name}\nwarn limit : {find1['channel_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_update_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await exist_check.send(embed=embed)

                                                if find1['channel_update_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await before.guild.kick(ss,reason='update a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                                elif find1['channel_update_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await before.guild.ban(ss,reason='update a channel')
                                                    security.delete_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                            else:
                                                warn +=1
                                                if warn == find1['channel_update_warn_limit']:
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel update Log",
                                                            description= f"user Action : update channel {after.name}\nwarn limit : {find1['channel_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find1['channel_update_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

                                                    if find1['channel_update_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await before.guild.kick(ss,reason='update a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                                    elif find1['channel_update_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await before.guild.ban(ss,reason='update a channel')
                                                        security.delete_one({"user_id":entry.user.id,"channel_update":True, "guild":before.guild.id})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id,"channel_update":True, "guild":before.guild.id} , {'$set':{'warn':warn}})
                                                    if find1['security_log_channel'] is not None:
                                                        exist_check = discord.utils.get(await member.guild.webhooks() , id = find1['security_log_webhook'])
                                                        if exist_check is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti channel update Log",
                                                            description= f"user Action : update channel {after.name}\nwarn limit : {find1['channel_update_warn_limit']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await exist_check.send(embed=embed)

        except:
            pass
         #channel update log
        try:
            if (find:= collection.find_one({"user_id":before.guild.id, 'auto_log_creator':True})):
                async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_update , limit=1):
                    member = discord.utils.get(before.guild.members , id = entry.user.id)
                    
                    tmp_guild = find['user_id']
                    tmp_id_channel= find['channel_update_state']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['channel_update_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Channel Update Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        flag= False
                        embed.add_field(name=f'ACTION:',value=f'Channel Update')
                        embed.add_field(name=f'CHANNEL:',value=f'{after.mention}')
                        embed.add_field(name=f'CHANNEL TYPE:',value=f'{after.type}')
                        embed.add_field(name=f'BY WHO:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                        embed.add_field(name=f'CHANGES:', value='',inline=False)
                        if before.name != after.name:
                            embed.add_field(name=f'NAME:', value=f'```{before.name} --> {after.name}```', inline=False)
                            flag= True
                        if len(before.changed_roles) > len(after.changed_roles):
                            new_li = []
                            for i in before.changed_roles:
                                if i not in after.changed_roles:
                                    new_li.append(i.name)
                            embed.add_field(name=f'REMOVE ROLE', value=f'```{new_li[0]}```', inline=False)
                            flag= True
                        elif len(before.changed_roles) < len(after.changed_roles):
                            new_li = []
                            for i in after.changed_roles:
                                if i not in before.changed_roles:
                                    new_li.append(i.name)
                            embed.add_field(name=f'ADD ROLE', value=f'```{new_li[0]}```', inline=False)
                            flag= True

                        if before.overwrites != after.overwrites:
                            embed.add_field(name=f'PERMISSIONS CHANGED', value=f'```A ROLE PERMISSION IN THIS CHANNEL CHANGED```', inline=False)
                            flag= True

                        if before.position != after.position:
                            embed.add_field(name=f'POSITION CHANGED', value=f'True', inline=False)
                            flag= True

                        if before.category != after.category:
                            embed.add_field(name=f'CATEGORY CHANGE', value=f'```{before.category.name} --> {after.category.name}```', inline=False)
                            flag= True
                        if before.permissions_synced != after.permissions_synced:
                            embed.add_field(name=f'PERMISSION SYNC CHANGE', value=f'```{before.permissions_synced} --> {after.permissions_synced}```', inline=False)
                            flag= True

                        embed.add_field(name=f'ID:', value=f'```USER:{member.id}\nCHANNEL:{after.id}```' , inline=False)
                        embed.set_thumbnail(url=member.display_avatar.url)
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)

                        if flag == True:
                            await webhooker.send(embed=embed)

            if (find:= collection.find_one({"user_id":before.guild.id, 'full_log_state':True})):
                async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_update , limit=1):
                    member = discord.utils.get(before.guild.members , id = entry.user.id)
                    tmp_guild = find['user_id']
                    channel_check= find['channel']
                    main_guild=self.bot.get_guild(tmp_guild)
                    webhooker_id = find['full_log_webhook']
                    webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
                    if webhooker is not None:
                        embed=discord.Embed(
                                title=f"Channel Update Log",
                                timestamp=datetime.now(),
                                color= 0xF6F6F6
                        )
                        flag= False
                        embed.add_field(name=f'ACTION:',value=f'Channel Update')
                        embed.add_field(name=f'CHANNEL:',value=f'{after.mention}')
                        embed.add_field(name=f'CHANNEL TYPE:',value=f'{after.type}')
                        embed.add_field(name=f'BY WHO:', value=f'{member.mention}')
                        embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                        embed.add_field(name=f'CHANGES:', value='',inline=False)
                        if before.name != after.name:
                            embed.add_field(name=f'NAME:', value=f'```{before.name} --> {after.name}```', inline=False)
                            flag= True
                        if len(before.changed_roles) > len(after.changed_roles):
                            new_li = []
                            for i in before.changed_roles:
                                if i not in after.changed_roles:
                                    new_li.append(i.name)
                            embed.add_field(name=f'REMOVE ROLE', value=f'```{new_li[0]}```', inline=False)
                            flag= True
                        elif len(before.changed_roles) < len(after.changed_roles):
                            new_li = []
                            for i in after.changed_roles:
                                if i not in before.changed_roles:
                                    new_li.append(i.name)
                            embed.add_field(name=f'ADD ROLE', value=f'```{new_li[0]}```', inline=False)
                            flag= True

                        if before.overwrites != after.overwrites:
                            embed.add_field(name=f'PERMISSIONS CHANGED', value=f'```A ROLE PERMISSION IN THIS CHANNEL CHANGED```', inline=False)
                            flag= True

                        if before.position != after.position:
                            embed.add_field(name=f'POSITION CHANGED', value=f'True', inline=False)
                            flag= True

                        if before.category != after.category:
                            embed.add_field(name=f'CATEGORY CHANGE', value=f'```{before.category.name} --> {after.category.name}```', inline=False)
                            flag= True
                        if before.permissions_synced != after.permissions_synced:
                            embed.add_field(name=f'PERMISSION SYNC CHANGE', value=f'```{before.permissions_synced} --> {after.permissions_synced}```', inline=False)
                            flag= True

                        embed.add_field(name=f'ID:', value=f'```USER:{member.id}\nCHANNEL:{after.id}```' , inline=False)
                        embed.set_thumbnail(url=member.display_avatar.url)
                        embed.set_footer(text=f'USERNAME: {member.name}',icon_url=member.display_avatar.url)

                        if flag == True and channel_check is not None:
                            await webhooker.send(embed=embed)
        except:
            pass


        return




async def setup(bot : Bot):
    await bot.add_cog(log(bot))