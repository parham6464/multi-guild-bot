from __future__ import annotations
from unicodedata import name



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

cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["security"]


def cand_moderate():
    async def predicate(interaction:discord.Interaction):
        target: discord.Member = interaction.namespace.member or interaction.namespace.target
        if not target:
            return True
        assert interaction.guild is not None and isinstance(interaction.user , discord.Member)
        if(target.top_role.position > interaction.user.top_role.position
            or target.guild_permissions.kick_members
            or target.guild_permissions.ban_members
            or target.guild_permissions.administrator
            or target.guild_permissions.manage_guild
            ):
            if interaction.user.id == interaction.guild.owner_id:
                return True
            else:
                return await interaction.response.send_message(f'you dont have permission' , ephemeral=True)
        else:
            return True
    return app_commands.check(predicate) 


def moderete_ban_kick():
    async def predicate(interaction:discord.Interaction):
        target: discord.Member = interaction.namespace.member or interaction.namespace.target
        if not target:
            return True
        assert interaction.guild is not None and isinstance(interaction.user , discord.Member)
        if(target.top_role.position > interaction.user.top_role.position):
            if interaction.user.id == interaction.guild.owner_id:
                return True
            else:
                return await interaction.response.send_message(f'you dont have permission' , ephemeral=True)
        else:
            return True
    return app_commands.check(predicate) 


class Mod(Plugin):
    def __init__(self , bot:Bot):
        self.bot = bot

    async def clean_message(
        self,
        interaction:discord.Interaction,
        amount : int ,
        check : Callable
    ) :
        if isinstance((channel := interaction.channel),(CategoryChannel , ForumChannel , PartialMessageable)): 
            return 
        assert channel is not None
        try:
            msgs =[
                    m async for m in channel.history(
                    limit=300,
                    before=Object(id=interaction.id),
                    after=None
                ) if check(m) == True and UTC.localize(datetime.now() - timedelta(days=14)) <= m.created_at
            ][:amount]
            await channel.delete_messages(msgs)
            
        except:
                msg = await self.bot.error(
                    f'i cant purge messages',
                    interaction
                )
                if msg:
                    await msg.delete(delay=5)
        else:
            if len(msgs)<1:
                msg=await self.bot.error(
                    f'no message found',
                    interaction
                )
                if msg:
                    await msg.delete(delay=5)
            else:
                msg = await self.bot.success(
                    f'successfully purged',
                    interaction
                )
                if msg:
                    await msg.delete(delay=5)
        
    @app_commands.command(
        name='kick',
        description='kick member from server'
        
    )
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.describe(
        member ="select a member to kick",
        reason = "write your reason"
    )
    @app_commands.guild_only()
    @moderete_ban_kick() 
    async def kick_command(self,interaction:discord.Interaction, member:discord.Member , reason:Optional[str]):
        try:
            flag= False
            flag_member = False
            if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'anti_kick':True})):
                if find['anti_kick_white_role'] is not None:
                    for i in interaction.user.roles:
                        if i.id in find['anti_kick_white_role']:
                            flag=True
                            break
                if find['anti_kick_white_user'] is not None:  
                    if interaction.user.id in find['anti_kick_white_user']:
                        flag_member= True 

                if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                    if not reason: reason = "No reason"
                    try:
                        await member.kick(reason=reason)
                        await interaction.response.send_message(f'successfully kicked from the server' , ephemeral= True)
                    except:
                        await interaction.response.send_message(f'couldnt kick member' , ephemeral= True)
                else:
                    await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)
            else:
                if not reason: reason = "No reason"
                try:
                    await member.kick(reason=reason)
                    await interaction.response.send_message(f'successfully kicked from the server' , ephemeral= True)
                except:
                    await interaction.response.send_message(f'couldnt kick member' , ephemeral= True)

        except:
            await interaction.response.send_message(f'something went wrong pls try again' , ephemeral= True)

        return

    @app_commands.command(
        name='ban',
        description='Ban member from Server'
    )
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.describe(
        member ="select a member to Ban",
        reason = "write your reason"
    )
    @moderete_ban_kick()
    async def ban_command(self,interaction:discord.Interaction, member:discord.Member , reason:Optional[str]):
        try:
            flag= False
            flag_member = False
            if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'anti_ban':True})):
                if find['anti_ban_white_role'] is not None:
                    for i in interaction.user.roles:
                        if i.id in find['anti_ban_white_role']:
                            flag=True
                            break
                if find['anti_ban_white_user'] is not None:  
                    if interaction.user.id in find['anti_ban_white_user']:
                        flag_member= True 

                if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                    if not reason: reason = "No reason"
                    try:
                        await member.ban(reason=reason)
                        await interaction.response.send_message(f'successfully banned from the server' , ephemeral= True)
                    except:
                        await interaction.response.send_message(f'couldnt ban member' , ephemeral= True)
                else:
                    await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)

            else:
                if not reason: reason = "No reason"
                try:
                    await member.ban(reason=reason)
                    await interaction.response.send_message(f'successfully banned from the server' , ephemeral= True)
                except:
                    await interaction.response.send_message(f'couldnt ban member' , ephemeral= True)

        except:
            await interaction.response.send_message(f'something went wrong pls try again' , ephemeral= True)

        return
    @app_commands.command(
        name='unban',
        description='Unban member from Server'
    )
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.describe(
        user ="ENTER USER ID FOR UNBAN",
        reason = "write your reason"
    )
    @app_commands.guild_only()
    async def unban_command(self,interaction:discord.Interaction, user:User , reason:Optional[str]):
        flag= False
        flag_member = False
        if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'anti_unban':True})):
            if find['anti_unban_white_role'] is not None:
                for i in interaction.user.roles:
                    if i.id in find['anti_unban_white_role']:
                        flag=True
                        break
            if find['anti_unban_white_user'] is not None:  
                if interaction.user.id in find['anti_unban_white_user']:
                    flag_member= True 

            if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                if not reason: reason = "No reason"
                assert interaction.guild is not None
                try:
                    await interaction.guild.unban(user)
                    await interaction.response.send_message(f'successfully unbanned from the server' , ephemeral= True)
                except:
                    await interaction.response.send_message(f'member is not banned' , ephemeral= True)
                else:
                    try:
                        await interaction.guild.unban(user , reason=reason)
                    except:
                        await interaction.response.send_message(f'i cant unban the user' , ephemeral= True)
            else:
                await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)

        else:
            if not reason: reason = "No reason"
            assert interaction.guild is not None
            try:
                await interaction.guild.unban(user)
                await interaction.response.send_message(f'successfully unbanned from the server' , ephemeral= True)
            except:
                await interaction.response.send_message(f'member is not banned' , ephemeral= True)
            else:
                try:
                    await interaction.guild.unban(user , reason=reason)
                except:
                    await interaction.response.send_message(f'i cant unban the user' , ephemeral= True)

        return
    @app_commands.command(
        name='mute',
        description='timeout member'
    )
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @cand_moderate()
    @app_commands.describe(

        target = 'choose the member that you want timeout',
        duration = 'choose the time of timeout ex: 1d , 1m , 1s' ,
        reason = 'write your reason'
    )
    async def mute_comamnd(
        self,
        interaction:discord.Interaction,
        target:discord.Member,
        duration:str,
        reason: Optional[str]
    ):
        try:
            flag= False
            flag_member = False
            if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'anti_timeout':True})):
                if find['anti_timeout_white_role'] is not None:
                    for i in interaction.user.roles:
                        if i.id in find['anti_timeout_white_role']:
                            flag=True
                            break
                if find['anti_timeout_white_user'] is not None:  
                    if interaction.user.id in find['anti_timeout_white_user']:
                        flag_member= True 

                if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                    if not duration: duration = 'id'
                    try:
                        real_duration = parse_timespan(duration)
                    except InvalidTimespan:
                        await interaction.response.send_message('you didnt enter a valid time')

                    else:
                        try:
                            await target.timeout(Utils.utcnow()+timedelta(seconds=real_duration) , reason=reason)
                            await interaction.response.send_message(f'member is timeout successfully' , ephemeral= True)
                        except:
                            await interaction.response.send_message(f'i cant timeout the user' , ephemeral= True)

                else:
                    await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)

            else:
                if not duration: duration = 'id'
                try:
                    real_duration = parse_timespan(duration)
                except InvalidTimespan:
                    await interaction.response.send_message('you didnt enter a valid time')

                else:
                    try:
                        await target.timeout(Utils.utcnow()+timedelta(seconds=real_duration) , reason=reason)
                        await interaction.response.send_message(f'member is timeout successfully' , ephemeral= True)
                    except:
                        await interaction.response.send_message(f'i cant timeout the user' , ephemeral= True)

        except:
            await interaction.response.send_message(f'something went wrong pls try again' , ephemeral= True)
        
        return
    @app_commands.command(
        name='unmute',
        description='remove member timeout'
    )
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @cand_moderate()
    @app_commands.describe(

        target = 'member that you want remove timeout',
        reason = 'write your reason'
    )
    async def unmute_comamnd(
        self,
        interaction:discord.Interaction,
        target:discord.Member,
        reason: Optional[str]
    ):
        try:
            if not target.is_timed_out():
                return await interaction.response.send_message(f'the user is not timeout write your member carefully')
            try:
                await target.timeout(None,reason=reason)
                await interaction.response.send_message(f'timeout removed' , ephemeral=True)
            except:
                await interaction.response.send_message(f'something went wrong' , ephemeral=True)
        except:
            await interaction.response.send_message(f'something went wrong pls try again' , ephemeral= True)

        return


    @commands.hybrid_command(name='purge' , description='clear optional amount of messages')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx,amount:int):
        try:
            amount = abs(amount)
            if amount == 0:
                return await ctx.send('your number is 0 enter again')
            elif amount >100:
                return await ctx.send('max number is 100 enter e number less than 100')
            await ctx.defer()
            try:
                await ctx.channel.purge(limit=(int(amount)+ 1))   
            except:
                pass
            await ctx.send('purge done')     
        except:
            await ctx.send(f'something went wrong pls try again')
        
        return

    # @app_commands.command(
    #     name='purge',
    #     description='Purges messages in the channel'
    # )
    # @app_commands.default_permissions(manage_messages=True)
    # @app_commands.describe(
    #     amount='the amount of the messages to delete (default:10)',
    #     user='only checks the messages by this user',
    #     content='only checks the messages by thin content'

    # )
    # async def purge_command(self , interaction:discord.Interaction , amount : Optional[int] , user: Optional[User] , content:Optional[str]):
    #     if not amount and amount !=0:
    #         amount = 10
    #     if amount < 1: return await interaction.response.send_message(f'the amount is too small' , ephemeral=True)

    #     if amount > 100: return await interaction.response.send_message(f'the amount is too big' , ephemeral=True)
        
    #     if user == None and content == None:
    #         check = lambda x:x.pinned==False
    #     else:
    #         if user != None and content != None:
    #             check = lambda x:x.author.id == user.id and x.content.lower() == content.lower() and x.pinned == False
    #         elif user != None and content == None:
    #             check = lambda x:x.author.id == user.id and x.pinned== False
    #         else:
    #             assert content is not None
    #             check = lambda x:x.content.lower() == content.lower() and x.pinned == False
            
        
    #     await interaction.response.defer()
    #     await self.clean_message(
    #             interaction=interaction, 
    #             amount = amount,
    #             check=check
    #         )
    
    @app_commands.command(
        name = 'lock',
        description='lock a text channel for sending messages'
    )
    @app_commands.describe(channel='Select a channel to lock sending messages permission')
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    async def lock_command(self , interaction:discord.Interaction , channel:Optional[TextChannel]):
        target = channel or interaction.channel
        assert interaction.guild is not None and isinstance(target , TextChannel)
        flag= False
        flag_member = False
        if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'channel_update_enable':True})):
            if find['channel_update_white_role'] is not None:
                for i in interaction.user.roles:
                    if i.id in find['channel_update_white_role']:
                        flag=True
                        break
            if find['channel_update_white_user'] is not None:  
                if interaction.user.id in find['channel_update_white_user']:
                    flag_member= True 

            if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                try:
                    await target.set_permissions(interaction.guild.default_role , send_messages=False)
                except:
                    await self.bot.error(
                        f'i cant lock the text channel',
                        interaction
                    )
                else:
                    await self.bot.success(
                        f'successfully locked' ,
                        interaction
                    )
            else:
                await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)
        else:
            try:
                await target.set_permissions(interaction.guild.default_role , send_messages=False)
            except:
                await self.bot.error(
                    f'i cant lock the text channel',
                    interaction
                )
            else:
                await self.bot.success(
                    f'successfully locked' ,
                    interaction
                )

        return

    @app_commands.command(
        name = 'unlock',
        description='unlock the locked text channel for sending messages'
    )
    @app_commands.describe(channel='Select a channel to unlock sending messages' , reset = 'if this is true then it will only reset the permissions')
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.default_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def unlock_command(self , interaction:discord.Interaction , channel:Optional[TextChannel] , reset:Optional[bool]):
        target = channel or interaction.channel
        assert interaction.guild is not None and isinstance(target , TextChannel)
        flag= False
        flag_member = False
        if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'channel_update_enable':True})):
            if find['channel_update_white_role'] is not None:
                for i in interaction.user.roles:
                    if i.id in find['channel_update_white_role']:
                        flag=True
                        break
            if find['channel_update_white_user'] is not None:  
                if interaction.user.id in find['channel_update_white_user']:
                    flag_member= True 

            if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                try:
                    await target.set_permissions(interaction.guild.default_role , send_messages=None if reset else True)
                except:
                    await self.bot.error(
                        f'i cant unlock the text channel',
                        interaction
                    )
                else:
                    await self.bot.success(
                        f'successfully unlocked',
                        interaction
                    )
            else:
                await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)
        else:
            try:
                await target.set_permissions(interaction.guild.default_role , send_messages=None if reset else True)
            except:
                await self.bot.error(
                    f'i cant unlock the text channel',
                    interaction
                )
            else:
                await self.bot.success(
                    f'successfully unlocked',
                    interaction
                )

        return
    channel=app_commands.Group(
        name = 'channel',
        description='manage server channels',
        default_permissions=Permissions(manage_channels=True),
        guild_only=True
    )
    @channel.command(
        name='create',
        description='Create a new channel'
    )
    @app_commands.describe(
        name='the name of the channel',
        type='the type of the channel',
        category='the category that channel will be created at',
        nsfw='if you set to True channel will have nsfw allowed'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def channel_create(
        self,
        interaction:discord.Interaction,
        name:str,
        type:Literal['Text Channel' , 'Voice Channel' , "Stage Channel" , "Forum Channel" , "Annoucement Channel"],
        category: Optional[CategoryChannel],
        nsfw:Optional[bool],
        reason: Optional[str],
    ):
        assert interaction.guild is not None
        category,nsfw,reason = category or None,nsfw or False , reason or "No reason"
        flag= False
        flag_member = False
        if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'channel_create_enable':True})):
            if find['channel_create_white_role'] is not None:
                for i in interaction.user.roles:
                    if i.id in find['channel_create_white_role']:
                        flag=True
                        break
            if find['channel_create_white_user'] is not None:  
                if interaction.user.id in find['channel_create_white_user']:
                    flag_member= True 

            if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                try:
                    if type == 'Text Channel':
                        await interaction.guild.create_text_channel(
                            name=name,
                            reason=reason,
                            category=category,
                            nsfw=nsfw
                        )
                    elif type == 'Annoucement Channel':
                        await interaction.guild.create_text_channel(
                            name=name,
                            reason=reason,
                            category=category,
                            nsfw=nsfw,
                            news = True
                        )

                    elif type == 'Voice Channel':
                        await interaction.guild.create_voice_channels(
                            name=name,
                            reason=reason,
                            category=category
                        )
                    elif type == 'Forum Channel':
                        await interaction.guild.create_forum(
                            name=name,
                            category=category,
                            nsfw=nsfw,
                            reason=reason

                        )
                    elif type == 'Stage Channel':
                        await interaction.guild.create_stage_channel(
                            name=name,
                            reason=reason,
                            category=category
                        )
                except:
                    await self.bot.error(
                        f'i could`nt create channel',
                        interaction
                    )
                else:
                    await self.bot.success(
                        f'channel created successfully',
                        interaction
                    )
            else:
                await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)
        else:
            try:
                if type == 'Text Channel':
                    await interaction.guild.create_text_channel(
                        name=name,
                        reason=reason,
                        category=category,
                        nsfw=nsfw
                    )
                elif type == 'Annoucement Channel':
                    await interaction.guild.create_text_channel(
                        name=name,
                        reason=reason,
                        category=category,
                        nsfw=nsfw,
                        news = True
                    )

                elif type == 'Voice Channel':
                    await interaction.guild.create_voice_channels(
                        name=name,
                        reason=reason,
                        category=category
                    )
                elif type == 'Forum Channel':
                    await interaction.guild.create_forum(
                        name=name,
                        category=category,
                        nsfw=nsfw,
                        reason=reason

                    )
                elif type == 'Stage Channel':
                    await interaction.guild.create_stage_channel(
                        name=name,
                        reason=reason,
                        category=category
                    )
            except:
                await self.bot.error(
                    f'i could`nt create channel',
                    interaction
                )
            else:
                await self.bot.success(
                    f'channel created successfully',
                    interaction
                )

        return    
    @channel.command(
        name='delete',
        description='delete a channel'
    )
    @app_commands.describe(
        channel='Select the channel that you wants to delete',
        reason = 'write your reason'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def channel_delete(self , interaction:discord.Interaction , channel: Union[TextChannel, VoiceChannel , ForumChannel , StageChannel ] , reason : Optional[str]='no reason'):
        flag= False
        flag_member = False
        if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'channel_delete_enable':True})):
            if find['channel_delete_white_role'] is not None:
                for i in interaction.user.roles:
                    if i.id in find['channel_delete_white_role']:
                        flag=True
                        break
            if find['channel_delete_white_user'] is not None:  
                if interaction.user.id in find['channel_delete_white_user']:
                    flag_member= True 

            if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                try:
                    await channel.delete(reason=reason)
                except:
                    await self.bot.error(
                        f'something went wrong',
                        interaction
                    )
                else:
                    await self.bot.success(
                        f'successfully deleted' , 
                        interaction
                    )

            else:
                await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)
        else:
            try:
                await channel.delete(reason=reason)
            except:
                await self.bot.error(
                    f'something went wrong',
                    interaction
                )
            else:
                await self.bot.success(
                    f'successfully deleted' , 
                    interaction
                )
        return
    _role = app_commands.Group(
        name = 'role' ,
        description='Moderate Server Roles',
        default_permissions=Permissions(manage_roles=True),
        guild_only=True
    )
    @_role.command(
        name='rolecreate',
        description='create a new role'
    )
    @app_commands.describe(
        color='enter hex code colors (use html color generators)'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def role_Create(
        self,
        interaction : discord.Interaction,
        name: str,
        hoist: Optional[bool],
        mentionable:Optional[bool],
        color: Optional[str],
        display_icon : Optional[Attachment]
    ):
        assert interaction.guild is not None
        flag= False
        flag_member = False
        if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'role_create_enable':True})):
            if find['role_create_white_role'] is not None:
                for i in interaction.user.roles:
                    if i.id in find['role_create_white_role']:
                        flag=True
                        break
            if find['role_create_white_user'] is not None:  
                if interaction.user.id in find['role_create_white_user']:
                    flag_member= True 

            if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                try:
                    hoist , mentionable , color_obj ,display_icon_bytes = (
                        hoist or Utils.MISSING,
                        mentionable or Utils.MISSING,
                        Color.from_str(color) if color else Utils.MISSING,
                        await display_icon.read() if display_icon else Utils.MISSING
                    )

                    role = await interaction.guild.create_role(
                        name=name,
                        hoist=hoist,
                        mentionable=mentionable,
                        color=color_obj,
                        display_icon=display_icon_bytes
                    )
                except Forbidden as e:
                    await self.bot.error(
                        e.text,
                        interaction
                    )
                except:
                    await self.bot.error(
                        f'i cant create the role', 
                        interaction
                    )
                else:
                    await self.bot.success(
                        f'role created successfully',
                        interaction
                    )
            else:
                await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)
        else:
            try:
                hoist , mentionable , color_obj ,display_icon_bytes = (
                    hoist or Utils.MISSING,
                    mentionable or Utils.MISSING,
                    Color.from_str(color) if color else Utils.MISSING,
                    await display_icon.read() if display_icon else Utils.MISSING
                )

                role = await interaction.guild.create_role(
                    name=name,
                    hoist=hoist,
                    mentionable=mentionable,
                    color=color_obj,
                    display_icon=display_icon_bytes
                )
            except Forbidden as e:
                await self.bot.error(
                    e.text,
                    interaction
                )
            except:
                await self.bot.error(
                    f'i cant create the role', 
                    interaction
                )
            else:
                await self.bot.success(
                    f'role created successfully',
                    interaction
                )
        return

    @_role.command(
        name='deleterole',
        description='Delete the role'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def role_delete(self , interaction:discord.Interaction , role:Role , reason:Optional[str]):
        flag= False
        flag_member = False
        if(find:= collection.find_one({"_id":interaction.guild_id , 'state':1 , 'role_delete_enable':True})):
            if find['role_delete_white_role'] is not None:
                for i in interaction.user.roles:
                    if i.id in find['role_delete_white_role']:
                        flag=True
                        break
            if find['role_delete_white_user'] is not None:  
                if interaction.user.id in find['role_delete_white_user']:
                    flag_member= True 

            if flag_member == True or flag==True or interaction.user.id == interaction.guild.owner_id:
                try:
                    await role.delete(reason=reason)
                except:
                    await self.bot.error(
                        f'i cant delete the role',
                        interaction
                    )
                else:
                    await self.bot.success(
                        f'the role deleted successfully',
                        interaction
                    )

            else:
                await interaction.response.send_message(f'You are not in whitelist to use this command' , ephemeral= True)
        else:            
            try:
                await role.delete(reason=reason)
            except:
                await self.bot.error(
                    f'i cant delete the role',
                    interaction
                )
            else:
                await self.bot.success(
                    f'the role deleted successfully',
                    interaction
                )
        return

    @_role.command(
        name='add',
        description='add a role to user'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @cand_moderate()
    async def role_add(
        self,
        interaction:discord.Interaction,
        member:discord.Member,
        role:Role
    ):
        assert interaction.guild is not None
        try:
            await member.add_roles(role)

        except:
            await self.bot.error(
                f'i cant add the role',
                interaction
            )
        else:
            await self.bot.success(
                f'the role added successfully',
                interaction
            )

        return
    @_role.command(
        name='remove',
        description='remove a role from user'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @cand_moderate()
    async def role_remove(
        self,
        interaction:discord.Interaction,
        member:discord.Member,
        role:Role
    ):
        assert interaction.guild is not None
        try:
            await member.remove_roles(role)

        except:
            await self.bot.error(
                f'i cant remove the role',
                interaction
            )
        else:
            await self.bot.success(
                f'the role removed successfully',
                interaction
            )
        return

    @app_commands.command(
        name='avatar',
        description='find a user or your avatar'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.default_permissions(use_application_commands=True)
    async def avatar(self,interaction:discord.Interaction , user:Optional[Union[discord.Member , User]]):
        try:
            await interaction.response.defer()
            if not user:user=interaction.user
            embed = discord.Embed(colour=0x047EF8)
            embed.set_image(url=user.display_avatar.url)
            av_button = discord.ui.Button(label ='Download' , url =user.display_avatar.url , emoji='🔽')
            view= discord.ui.View()
            view.add_item(av_button)
            await interaction.followup.send(embed=embed , view=view)
        except:
            await interaction.followup.send('something went wrong pls try again')
        
        return

    async def getanime(self):
        try:
            async with ClientSession() as resp:
                async with resp.get(f'https://api.waifu.pics/sfw/waifu') as response:
                    data = await response.json()
            return data['url']
        except:
            pass

    @app_commands.command(
        name='anime',
        description='generate random anime picture'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.default_permissions(use_application_commands=True)
    async def waifu(self,interaction:discord.Interaction):
        try:
            await interaction.response.defer()
            url1= await self.getanime()
            av_button = discord.ui.Button(label ='Download' , url =url1 , emoji='🔽')
            view= discord.ui.View()
            view.add_item(av_button)        
            await interaction.followup.send(
                embed=discord.Embed(color=0x047EF8).set_image(url=url1),
                view=view
            )
        except:
            await interaction.followup.send('server is busy or you dont have permission')

        return


async def setup(bot : Bot):
    await bot.add_cog(Mod(bot))
