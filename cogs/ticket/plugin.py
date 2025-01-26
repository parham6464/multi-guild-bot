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
import random , string
import asyncio
from discord import ui

cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["ticket"]


class AfterClose1(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def get_admin(self,ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        admins = find['admins']
        return admins

    async def open_button_updater(self,ctx):
        collection.update_one({'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False},{"$set":{ "state":True}})

    async def delete_button_deleter(self,ctx):
        collection.delete_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False})


    @ui.button(label='OPEN TICKET' , custom_id='open_ticket' , style=discord.ButtonStyle.primary)
    async def open_ticket1(self, ctx:discord.Interaction,_):    
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check, "channel_id":ctx.channel_id , 'state':False})):
                    modal_roles=await self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        if find2['open_state'] == False:
                            collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':True , 'close_state':False}})
                            channel=find2['channel_id']
                            member = find2['user_id']
                            channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                            member_checker=discord.utils.get(ctx.guild.members, id=member)
                            permission_check = channel_temp.overwrites
                            msg = find2['msg_id']
                            for i in permission_check:
                                if i.id == member:
                                    await asyncio.sleep(0.5)
                                    await channel_temp.set_permissions(member_checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                    try:
                                        async for messager in channel_temp.history(limit=None):
                                            if messager.id == msg:
                                                await messager.delete()
                                    except:
                                        await ctx.edit_original_response(content='Ticket is open now')
                                    await self.open_button_updater(ctx)
                        else:
                            pass
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass

    @ui.button(label='DELETE TICKET' , custom_id='delete_ticket' , style=discord.ButtonStyle.red)
    async def delete_button1(self, ctx:discord.Interaction,_):    
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                    modal_roles=await self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        channel=find2['channel_id']
                        channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                        await self.delete_button_deleter(ctx)
                        await ctx.followup.send(f'ticket will be deleted in next 1 seconds')
                        await asyncio.sleep(1)
                        await channel_temp.delete()
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass
    

class CloseTicketAW1(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def get_admin(self,ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        admins = find['admins']
        return admins

    async def open_button_updater(self,ctx):
        collection.update_one({'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False},{"$set":{ "state":True}})

    async def delete_button_deleter(self,ctx):
        collection.delete_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False})

    async def close_button_updater(self,ctx):
        collection.update_one({ 'guild_id':ctx.guild.id, "channel_id":ctx.channel_id},{"$set":{ "state":False}})

    async def support_embed(self):
        embed=discord.Embed(
            title ='APA BOT',
            description=f"Support Panel:",
            color=None
        )
        return embed


    async def create_embed(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        message = var['embed_message']
        embed=discord.Embed(
            title ='APA BOT',
            description=f"{message}",
            color= 0xF6F6F6,
            timestamp=datetime.now()
        )
        return embed

    @ui.button(label='Close Ticket' , custom_id='close_ticket' , style=discord.ButtonStyle.red)
    async def open_ticket1(self, ctx:discord.Interaction,_):    
        try:
            if ctx is not None:
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                    modal_roles=await self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']==ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        if find2['close_state']==False:
                            channel=find2['channel_id']
                            member = find2['user_id']
                            channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                            member_checker=discord.utils.get(ctx.guild.members, id=member)
                            await self.close_button_updater(ctx)
                            ########## buttons section for support
                            embed = await self.support_embed()

                            collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':False , 'close_state':True}})

                            # button_view = discord.ui.View(timeout=None)
                            if member_checker is not None:
                                print('25')
                                await channel_temp.set_permissions(member_checker , read_messages=False , send_messages=False,read_message_history=False,attach_files=False , send_voice_messages=False)
                                print('26')
                                await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                print('27')
                                msg= await ctx.followup.send(embed=embed , view=AfterClose1(self.bot))
                                print('28')
                                collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                            else:
                                await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                msg= await ctx.followup.send(embed=embed , view=AfterClose1(self.bot))
                                collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                        else:
                            await ctx.response.send_message(f'you already closed ticket' , ephemeral=True)

                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass



###################update section ################
class buttons(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_count(self,ctx):
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            counter=find['count']
            return counter

    def updater(self ,ctx ,  number_of_ticket):
        number_of_ticket = int(number_of_ticket)
        number_of_ticket+=1
        number_of_ticket = str(number_of_ticket)
        collection.update_one({"_id":ctx.guild.id},{"$set":{ "count":number_of_ticket}})

    def support_embed(self ):
        embed=discord.Embed(
            title ='APA BOT',
            description=f"Support Panel:",
            color=None
        )
        return embed


    def create_embed(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        message = var['embed_message']
        embed=discord.Embed(
            title ='APA BOT',
            description=f"{message}",
            color= 0xF6F6F6,
            timestamp=datetime.now()
        )
        return embed
    
    def close_button_updater(self,ctx):
        collection.update_one({ 'guild_id':ctx.guild.id, "channel_id":ctx.channel_id},{"$set":{ "state":False}})
    
    def open_button_updater(self,ctx):
        collection.update_one({'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False},{"$set":{ "state":True}})

    def delete_button_deleter(self,ctx):
        collection.delete_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False})

    def get_category(self,ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        category_id = find['category']
        return category_id

    def get_admin(self,ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        admins = find['admins']
        return admins

    def get_title(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        title1 = var['form_title']
        # caller = ModalApplicationForm
        # caller.title = title1
        return title1

    def get_description(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        body = var['form_description']
        # caller = ModalApplicationForm
        # caller.title = title1
        return body    

    async def open_button85(self,ctx=None):
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check, "channel_id":ctx.channel_id , 'state':False})):
                    modal_roles= self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        if find2['open_state'] == False:
                            collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':True , 'close_state':False}})
                            channel=find2['channel_id']
                            member = find2['user_id']
                            channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                            member_checker=discord.utils.get(ctx.guild.members, id=member)
                            permission_check = channel_temp.overwrites
                            msg = find2['msg_id']
                            for i in permission_check:
                                if i.id == member:
                                    await asyncio.sleep(0.5)
                                    await channel_temp.set_permissions(member_checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                    try:
                                        async for messager in channel_temp.history(limit=None):
                                            if messager.id == msg:
                                                await messager.delete()
                                    except:
                                        await ctx.edit_original_response(content='Ticket is open now')
                                    self.open_button_updater(ctx)
                        else:
                            pass
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass

############################################
    async def delete_button85(self,ctx=None):
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                    modal_roles= self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        channel=find2['channel_id']
                        channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                        self.delete_button_deleter(ctx)
                        await ctx.followup.send(f'ticket will be deleted in next 1 seconds')
                        await asyncio.sleep(1)
                        await channel_temp.delete()
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass
    @ui.button(label='Close Ticket' , custom_id='close_ticket' , style=discord.ButtonStyle.red)
    async def close_ticket1(self, ctx:discord.Interaction,_):
        try:
            if ctx is not None:
                print ('1')
                guild_check = ctx.guild.id
                print ('2')
                if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                    modal_roles=self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']==ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        if find2['close_state']==False:
                            channel=find2['channel_id']
                            member = find2['user_id']
                            channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                            member_checker=discord.utils.get(ctx.guild.members, id=member)
                            self.close_button_updater(ctx)
                            ########## buttons section for support
                            embed = self.support_embed()
                            av_button = discord.ui.Button(label ='DELETE TICKET' , style=discord.ButtonStyle.red , custom_id='delete_ticket' )
                            open_button = discord.ui.Button(label ='OPEN TICKET' , style=discord.ButtonStyle.green , custom_id='open_ticket' )

                            av_button.callback = self.delete_button85
                            open_button.callback = self.open_button85
                            collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':False , 'close_state':True}})

                            button_view = discord.ui.View(timeout=None)
                            button_view.add_item(av_button)
                            button_view.add_item(open_button)

                            # button_view = discord.ui.View(timeout=None)
                            
                            if member_checker is not None:
                                await channel_temp.set_permissions(member_checker , read_messages=False , send_messages=False,read_message_history=False,attach_files=False , send_voice_messages=False)
                                await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                msg= await ctx.followup.send(embed=embed , view=button_view)
                                collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                            else:
                                await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                msg= await ctx.followup.send(embed=embed , view=button_view)
                                collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                        else:
                            await ctx.response.send_message(f'you already closed ticket' , ephemeral=True)

                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass
    @ui.button(label='DELETE TICKET' , custom_id='delete_ticket' , style=discord.ButtonStyle.red)
    async def delete_button1(self, ctx:discord.Interaction,_):    
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                    modal_roles=self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        channel=find2['channel_id']
                        channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                        self.delete_button_deleter(ctx)
                        await ctx.followup.send(f'ticket will be deleted in next 1 seconds')
                        await asyncio.sleep(1)
                        await channel_temp.delete()
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass
    @ui.button(label='OPEN TICKET' , custom_id='open_ticket' , style=discord.ButtonStyle.primary)
    async def open_ticket1(self, ctx:discord.Interaction,_):    
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check, "channel_id":ctx.channel_id , 'state':False})):
                    modal_roles=self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        if find2['open_state'] == False:
                            collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':True , 'close_state':False}})
                            channel=find2['channel_id']
                            member = find2['user_id']
                            channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                            member_checker=discord.utils.get(ctx.guild.members, id=member)
                            permission_check = channel_temp.overwrites
                            msg = find2['msg_id']
                            for i in permission_check:
                                if i.id == member:
                                    await asyncio.sleep(0.5)
                                    await channel_temp.set_permissions(member_checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                    try:
                                        async for messager in channel_temp.history(limit=None):
                                            if messager.id == msg:
                                                await messager.delete()
                                    except:
                                        await ctx.edit_original_response(content='Ticket is open now')
                                    self.open_button_updater(ctx)
                        else:
                            pass
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass

    @ui.button(label='create ticket' , custom_id='create_ticket' , style=discord.ButtonStyle.primary)
    async def create_ticket(self, ctx:discord.Interaction,_):    
        try:
            if ctx is not None:
                guild_check = ctx.guild.id
                if(find:= collection.find_one({"_id":ctx.guild.id})):
                    style_checker = find['style']
                    if(find5:= collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})):
                        for i in find5:
                            channel_checker=i['channel_id']
                            checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
                            if checker is None:
                                channel_id = i['channel_id']
                                tmp_guild = i['guild_id']
                                user_tmp = i['user_id']
                                collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})
                        
                        false_checker=collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':False})
                        for i in false_checker:
                            channel_checker=i['channel_id']
                            checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
                            if checker is None:
                                channel_id = i['channel_id']
                                tmp_guild = i['guild_id']
                                user_tmp = i['user_id']
                                collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})

                        if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                            # await ctx.response.defer()
                            guild = ctx.guild
                            member = ctx.user
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True),
                            }
                            number_of_ticket = self.get_count(ctx)
                            if number_of_ticket is None:
                                number_of_ticket = '1'
                                self.updater(ctx,number_of_ticket)
                                if len( number_of_ticket) == 1:
                                    number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                
                            elif number_of_ticket is not None:
                                self.updater(ctx,number_of_ticket)
                                if len(number_of_ticket) == 1:
                                    number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                elif len(number_of_ticket) == 2:
                                    number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                elif len(number_of_ticket) == 3:
                                    number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                else:
                                    number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                            av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red , custom_id='close_ticket' )
                            av_button.callback = self.close_ticket1
                            button_view = CloseTicketAW1(self.bot)
                            category_id = self.get_category(ctx)
                            category = discord.utils.get(ctx.guild.categories , id =category_id)
                            roles = self.get_admin(ctx)
                            embeder=self.create_embed(ctx)
                            modal_category = self.get_category(ctx)
                            modal_roles=self.get_admin(ctx)
                            print ('1')

                            async def on_sumbit(ctx):
                                if style_checker ==1:
                                    print ('5')
                                    form_title = find['form_title']
                                    form_description= find['form_description']
                                    embed = embeder
                                    category_id = modal_category
                                    category = discord.utils.get(ctx.guild.categories , id =category_id)
                                    roles = modal_roles
                                    await ctx.response.defer()
                                    if category is not None:
                                        channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                                    else:
                                        owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                                        channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                                        await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')
                                    print ('6')
                                    embed.add_field(name=form_title,value=f'{title_ticket}')
                                    embed.add_field(name=form_description , value=f'{body_ticket}')

                                    await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=CloseTicketAW1(self.bot))
                                    if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
                                        pass
                                    else:
                                        collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
                                    admins = []
                                    if roles is not None:
                                        for i in roles:
                                            checker=discord.utils.get(guild.roles, id=i)
                                            if checker is not None:
                                                await channel.set_permissions(checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                                return
                                    print ('7')
                                else:
                                    await ctx.response.send_message('the ticket style changed by admins but they didnt send new form')

                            print ('2')
                            modals = discord.ui.Modal(title='Ticket System Form')
                            title_modal = self.get_title(ctx)
                            body_modal = self.get_description(ctx)
                            title_ticket = discord.ui.TextInput(label=title_modal , style=discord.TextStyle.short , required=True)
                            body_ticket = discord.ui.TextInput(label=body_modal , style=discord.TextStyle.long, required=True)
                            modals.add_item(title_ticket)
                            modals.add_item(body_ticket)
                            modals.on_submit=on_sumbit
                            print ('3')
                            await ctx.response.send_modal(modals)
                            print ('4')
                            

                            
                        else:
                            await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)

                    else:
                        if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                            # await ctx.response.defer()
                            guild = ctx.guild
                            member = ctx.user
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True),
                            }
                            number_of_ticket = self.get_count(ctx)
                            if number_of_ticket is None:
                                number_of_ticket = '1'
                                self.updater(ctx,number_of_ticket)
                                if len( number_of_ticket) == 1:
                                    number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                
                            elif number_of_ticket is not None:
                                self.updater(ctx,number_of_ticket)
                                if len(number_of_ticket) == 1:
                                    number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                elif len(number_of_ticket) == 2:
                                    number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                elif len(number_of_ticket) == 3:
                                    number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                else:
                                    number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                            av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
                            av_button.callback = self.close_ticket1
                            button_view = CloseTicketAW1(self.bot)
                            category_id = self.get_category(ctx)
                            category = discord.utils.get(ctx.guild.categories , id =category_id)
                            roles = self.get_admin(ctx)
                            embeder=self.create_embed(ctx)
                            modal_category = self.get_category(ctx)
                            modal_roles=self.get_admin(ctx)
                            
                            async def on_sumbit1(ctx):
                                if style_checker == 1:
                                    embed = embeder
                                    category_id = modal_category
                                    category = discord.utils.get(ctx.guild.categories , id =category_id)
                                    roles = modal_roles
                                    await ctx.response.defer()
                                    if category is not None:
                                        channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                                    else:
                                        owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                                        channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                                        await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')
                                    
                                    embed.add_field(name='Ticket title:',value=f'{title_ticket1}')
                                    embed.add_field(name='Ticket Description' , value=f'{body_ticket1}')

                                    await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=CloseTicketAW1(self.bot))
                                    if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
                                        pass
                                    else:
                                        collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
                                    admins = []
                                    if roles is not None:
                                        for i in roles:
                                            checker=discord.utils.get(guild.roles, id=i)
                                            if checker is not None:
                                                await channel.set_permissions(checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                                return
                                else:
                                    await ctx.response.send_message('the ticket style changed by admins but they didnt send new form')
                            modals = discord.ui.Modal(title='Ticket System Form')
                            title_modal = self.get_title(ctx)
                            body_modal = self.get_description(ctx)
                            title_ticket1 = discord.ui.TextInput(label=title_modal , style=discord.TextStyle.short , required=True)
                            body_ticket1 = discord.ui.TextInput(label=body_modal , style=discord.TextStyle.long, required=True)
                            modals.add_item(title_ticket1)
                            modals.add_item(body_ticket1)
                            modals.on_submit=on_sumbit1
                            await ctx.response.send_modal(modals)
                        
        except:
            pass
    
    
###############################################################


##################################################
class ModalApplicationForm(discord.ui.Modal):
    
    title5 :str = None
    # title_ticket = discord.ui.TextInput(label=title5 , style=discord.TextStyle.short , required=True)
    # body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)

    def __init__(self, ctx , number_of_ticket , overwrites , close_button):
        self.ctx = ctx
        self.number_of_ticket=number_of_ticket
        self.overwrites=overwrites
        self.close_button=close_button
        self.title5 = self.get_title(ctx)
        self.body = self.get_description(ctx)
        self.styler = collection.find_one({'_id':self.ctx.guild.id})
        self.title_ticket = discord.ui.TextInput(label=self.title5 , style=discord.TextStyle.short , required=True)
        self.body_ticket = discord.ui.TextInput(label=self.body , style=discord.TextStyle.long, required=True)



        super().__init__(title='Ticket System Form' )
        ModalApplicationForm.add_item(self,item=self.title_ticket)
        ModalApplicationForm.add_item(self,item=self.body_ticket)


    def get_title(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        title1 = var['form_title']
        # caller = ModalApplicationForm
        # caller.title = title1
        return title1

    def get_description(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        body = var['form_description']
        # caller = ModalApplicationForm
        # caller.title = title1
        return body

    async def on_submit(self , interaction:discord.Interaction):
        try:
            if self.styler['style'] == 1:
                await interaction.response.defer()
                caller =TicketSystem(Bot)
                category_id = caller.get_category(self.ctx)
                category = discord.utils.get(self.ctx.guild.categories , id =category_id)
                embed = caller.create_embed(self.ctx)
                roles = caller.get_admin(self.ctx)
                
                
                if category is not None:
                    channel = await self.ctx.guild.create_text_channel(self.number_of_ticket, overwrites=self.overwrites , category=category)
                else:
                    owner = discord.utils.get(self.ctx.guild.members , id=self.ctx.guild.owner_id)
                    await asyncio.sleep(0.5)
                    channel = await self.ctx.guild.create_text_channel(self.number_of_ticket, overwrites=self.overwrites)
                    await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                embed.add_field(name=f"{self.title5}:",value=f'{self.title_ticket}')
                embed.add_field(name=f"{self.body}:" , value=f'{self.body_ticket}' , inline=False)
                
                await channel.send(f'your ticket created {self.ctx.user.mention}',embed=embed , view=self.close_button)
                if(find1:= collection.find_one({"user_id":self.ctx.user.id, "guild_id":self.ctx.guild.id, "state":True})):
                    pass
                else:
                    collection.insert_one({"user_id":self.ctx.user.id , "channel_id":channel.id , "guild_id":self.ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
                admins = []
                if roles is not None:
                    for i in roles:
                        checker=discord.utils.get(self.ctx.guild.roles, id=i)
                        if checker is not None:
                            await channel.set_permissions(checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
            else:
                try:
                    user_dm = discord.utils.get(self.ctx.guild.members , id=self.ctx.user.id)
                    await user_dm.send('the ticket style changed but the form is not updated admin should send it again')
                except:
                    pass
        except:
            try:
                user_dm = discord.utils.get(self.ctx.guild.members , id=self.ctx.user.id)
                await user_dm.send('something went wrong to create ticket for you pls try again')
            except:
                pass
        
                    
class ModalApplicationForm1(discord.ui.Modal):
    
    title5 :str = None
    # title_ticket = discord.ui.TextInput(label=title5 , style=discord.TextStyle.short , required=True)
    # body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)

    def __init__(self, ctx , number_of_ticket , overwrites , close_button , category_menu=None):
        self.ctx = ctx
        self.number_of_ticket=number_of_ticket
        self.overwrites=overwrites
        self.close_button=close_button
        self.category_menu = category_menu
        self.styler = collection.find_one({'_id':self.ctx.guild.id})
        self.title5 = self.get_title(ctx)
        self.body = self.get_description(ctx)
        self.title_ticket = discord.ui.TextInput(label=self.title5 , style=discord.TextStyle.short , required=True)
        self.body_ticket = discord.ui.TextInput(label=self.body , style=discord.TextStyle.long, required=True)



        super().__init__(title='Ticket System Form' )
        ModalApplicationForm1.add_item(self,item=self.title_ticket)
        ModalApplicationForm1.add_item(self,item=self.body_ticket)


    def get_title(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        title1 = var['form_title']
        # caller = ModalApplicationForm
        # caller.title = title1
        return title1

    def get_description(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        body = var['form_description']
        # caller = ModalApplicationForm
        # caller.title = title1
        return body
    
    def id_to_cat(self,ctx):
        var = collection.find_one({"guild_ider":ctx.guild.id , "ID":self.category_menu})
        category_id_main = var['category_id']
        return category_id_main

    def find_department(self,ctx):
        var = collection.find_one({"guild_ider":ctx.guild.id , "ID":self.category_menu})
        name_finder = var['admins_name']
        return name_finder


    async def on_submit(self , interaction:discord.Interaction):
        try:
            if self.styler['style'] == 2:
                await interaction.response.defer()
                caller =TicketSystem(Bot)
                category_getter  = self.id_to_cat(self.ctx)
                category = discord.utils.get(self.ctx.guild.categories , id =category_getter)
                embed = caller.create_embed(self.ctx)
                roles = caller.get_admin(self.ctx)
                deparment = self.find_department(self.ctx)
                
                
                if category is not None:
                    channel = await self.ctx.guild.create_text_channel(self.number_of_ticket, overwrites=self.overwrites , category=category)
                else:
                    owner = discord.utils.get(self.ctx.guild.members , id=self.ctx.guild.owner_id)
                    await asyncio.sleep(0.5)
                    channel = await self.ctx.guild.create_text_channel(self.number_of_ticket, overwrites=self.overwrites)
                    await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                embed.add_field(name=f'Department: ' , value=f'{deparment}' , inline=False)
                embed.add_field(name=f"{self.title5}:",value=f'{self.title_ticket}' , inline=False)
                embed.add_field(name=f"{self.body}:" , value=f'{self.body_ticket}' , inline=False)
                
                
                if(find1:= collection.find_one({"user_id":self.ctx.user.id, "guild_id":self.ctx.guild.id, "state":True})):
                    pass
                else:
                    collection.insert_one({"user_id":self.ctx.user.id , "channel_id":channel.id , "guild_id":self.ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
                admins = []
                text_mention=''
                menu_finder = collection.find({"ID":self.category_menu,"guild_ider":self.ctx.guild.id})
                for i in menu_finder:
                    if i['category_id'] == category_getter:
                        tmp_list = i['admins_id']
                        for j in tmp_list:
                            j=int(j)
                            roler_plus = discord.utils.get(self.ctx.guild.roles , id = j)
                            if roler_plus is not None:
                                admins.append(j)
                                text_mention+=f'<@&{j}> '
                                await channel.set_permissions(roler_plus , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                
                await channel.send(f'your ticket created {self.ctx.user.mention}\n{text_mention}',embed=embed , view=self.close_button)
            else:
                try:
                    user_dm = discord.utils.get(self.ctx.guild.members , id=self.ctx.user.id)
                    await user_dm.send('the ticket style changed but the form is not updated admin should send it again')
                except:
                    pass
        except:
            try:
                user_dm = discord.utils.get(self.ctx.guild.members , id=self.ctx.user.id)
                await user_dm.send('something went wrong to create ticket for you pls try again')
            except:
                pass


##############################updater dropw down###################
class AfterClose(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def get_admin(self,ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        admins = find['admins']
        return admins

    async def open_button_updater(self,ctx):
        collection.update_one({'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False},{"$set":{ "state":True}})

    async def delete_button_deleter(self,ctx):
        collection.delete_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False})


    @ui.button(label='OPEN TICKET' , custom_id='open_ticket' , style=discord.ButtonStyle.primary)
    async def open_ticket1(self, ctx:discord.Interaction,_):    
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check, "channel_id":ctx.channel_id , 'state':False})):
                    modal_roles=await self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        if find2['open_state'] == False:
                            collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':True , 'close_state':False}})
                            channel=find2['channel_id']
                            member = find2['user_id']
                            channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                            member_checker=discord.utils.get(ctx.guild.members, id=member)
                            permission_check = channel_temp.overwrites
                            msg = find2['msg_id']
                            for i in permission_check:
                                if i.id == member:
                                    await asyncio.sleep(0.5)
                                    await channel_temp.set_permissions(member_checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                    try:
                                        async for messager in channel_temp.history(limit=None):
                                            if messager.id == msg:
                                                await messager.delete()
                                    except:
                                        await ctx.edit_original_response(content='Ticket is open now')
                                    await self.open_button_updater(ctx)
                        else:
                            pass
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass

    @ui.button(label='DELETE TICKET' , custom_id='delete_ticket' , style=discord.ButtonStyle.red)
    async def delete_button1(self, ctx:discord.Interaction,_):    
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                    modal_roles=await self.get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        channel=find2['channel_id']
                        channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                        await self.delete_button_deleter(ctx)
                        await ctx.followup.send(f'ticket will be deleted in next 1 seconds')
                        await asyncio.sleep(1)
                        await channel_temp.delete()
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass
    

class CloseTicketAW(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def get_admin(self,ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        admins = find['admins']
        return admins

    async def open_button_updater(self,ctx):
        collection.update_one({'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False},{"$set":{ "state":True}})

    async def delete_button_deleter(self,ctx):
        collection.delete_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False})

    async def close_button_updater(self,ctx):
        collection.update_one({ 'guild_id':ctx.guild.id, "channel_id":ctx.channel_id},{"$set":{ "state":False}})

    async def support_embed(self):
        embed=discord.Embed(
            title ='APA BOT',
            description=f"Support Panel:",
            color=None
        )
        return embed


    async def create_embed(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        message = var['embed_message']
        embed=discord.Embed(
            title ='APA BOT',
            description=f"{message}",
            color= 0xF6F6F6,
            timestamp=datetime.now()
        )
        return embed

    @ui.button(label='Close Ticket' , custom_id='close_ticket' , style=discord.ButtonStyle.red)
    async def open_ticket1(self, ctx:discord.Interaction,_):    
        if ctx is not None:
            guild_check = ctx.guild.id
            if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                modal_roles=await self.get_admin(ctx)
                flager=False
                if modal_roles is not None:
                    for i in ctx.user.roles:
                        if i.id in modal_roles:
                            flager=True
                perm_checker= ctx.user.guild_permissions.administrator
                if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                    flager=True
                if find2['user_id']==ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                    if find2['close_state']==False:
                        channel=find2['channel_id']
                        member = find2['user_id']
                        channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                        member_checker=discord.utils.get(ctx.guild.members, id=member)
                        await self.close_button_updater(ctx)
                        ########## buttons section for support
                        embed = await self.support_embed()

                        collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':False , 'close_state':True}})

                        # button_view = discord.ui.View(timeout=None)
                        if member_checker is not None:
                            print('22')
                            await channel_temp.set_permissions(member_checker , read_messages=False , send_messages=False,read_message_history=False,attach_files=False , send_voice_messages=False)
                            print('23')
                            await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                            print('24')
                            msg= await ctx.followup.send(embed=embed , view=AfterClose(self.bot))
                            print ('25')
                            collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                        else:
                            await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                            msg= await ctx.followup.send(embed=embed , view=AfterClose(self.bot))
                            collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                    else:
                        await ctx.response.send_message(f'you already closed ticket' , ephemeral=True)

                else:
                    await ctx.edit_original_response(content='you are not allowed to do this')




async def updater_list(interaction=None):

    async def get_count(ctx):
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            counter=find['count']
            return counter

    async def updater(ctx ,  number_of_ticket):
        number_of_ticket = int(number_of_ticket)
        number_of_ticket+=1
        number_of_ticket = str(number_of_ticket)
        collection.update_one({"_id":ctx.guild.id},{"$set":{ "count":number_of_ticket}})

    async def support_embed():
        embed=discord.Embed(
            title ='APA BOT',
            description=f"Support Panel:",
            color=None
        )
        return embed


    async def create_embed(ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        message = var['embed_message']
        embed=discord.Embed(
            title ='APA BOT',
            description=f"{message}",
            color= 0xF6F6F6,
            timestamp=datetime.now()
        )
        return embed
    
    async def close_button_updater(ctx):
        collection.update_one({ 'guild_id':ctx.guild.id, "channel_id":ctx.channel_id},{"$set":{ "state":False}})
    
    async def open_button_updater(ctx):
        collection.update_one({'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False},{"$set":{ "state":True}})

    async def delete_button_deleter(ctx):
        collection.delete_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False})

    async def get_category(ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        category_id = find['category']
        return category_id

    async def get_admin(ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        admins = find['admins']
        return admins

    async def get_title(ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        title1 = var['form_title']
        # caller = ModalApplicationForm
        # caller.title = title1
        return title1

    async def get_description(ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        body = var['form_description']
        # caller = ModalApplicationForm
        # caller.title = title1
        return body 

###############################################open ticket        
    async def open_button22(ctx=None):
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check, "channel_id":ctx.channel_id , 'state':False})):
                    modal_roles=await get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        if find2['open_state'] == False:
                            collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':True , 'close_state':False}})
                            channel=find2['channel_id']
                            member = find2['user_id']
                            channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                            member_checker=discord.utils.get(ctx.guild.members, id=member)
                            permission_check = channel_temp.overwrites
                            msg = find2['msg_id']
                            for i in permission_check:
                                if i.id == member:
                                    await asyncio.sleep(0.5)
                                    await channel_temp.set_permissions(member_checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                    try:
                                        async for messager in channel_temp.history(limit=None):
                                            if messager.id == msg:
                                                await messager.delete()
                                    except:
                                        await ctx.edit_original_response(content='Ticket is open now')
                                    await open_button_updater(ctx)
                        else:
                            pass
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass

############################################
    async def delete_button(ctx=None):
        try:
            if ctx is not None:
                await ctx.response.defer()
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                    modal_roles=await get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        channel=find2['channel_id']
                        channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                        await delete_button_deleter(ctx)
                        await ctx.followup.send(f'ticket will be deleted in next 1 seconds')
                        await asyncio.sleep(1)
                        await channel_temp.delete()
                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass

#########################################close button

    async def close_button(ctx=None):
        try:
            if ctx is not None:
                guild_check = ctx.guild.id
                if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                    modal_roles=await get_admin(ctx)
                    flager=False
                    if modal_roles is not None:
                        for i in ctx.user.roles:
                            if i.id in modal_roles:
                                flager=True
                    perm_checker= ctx.user.guild_permissions.administrator
                    if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                        flager=True
                    if find2['user_id']==ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                        if find2['close_state']==False:
                            channel=find2['channel_id']
                            member = find2['user_id']
                            channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                            member_checker=discord.utils.get(ctx.guild.members, id=member)
                            await close_button_updater(ctx)
                            ########## buttons section for support
                            embed = await support_embed()
                            av_button33 = discord.ui.Button(label ='DELETE TICKET' , style=discord.ButtonStyle.red , custom_id='delete_ticket' )
                            open_button33 = discord.ui.Button(label ='OPEN TICKET' , style=discord.ButtonStyle.primary , custom_id='open_ticket' )

                            av_button33.callback = delete_button
                            open_button33.callback = open_button22
                            collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':False , 'close_state':True}})

                            button_view = discord.ui.View(timeout=None)
                            button_view.add_item(av_button33)
                            button_view.add_item(open_button33)

                            # button_view = discord.ui.View(timeout=None)
                            
                            if member_checker is not None:
                                await channel_temp.set_permissions(member_checker , read_messages=False , send_messages=False,read_message_history=False,attach_files=False , send_voice_messages=False)
                                await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                msg= await ctx.followup.send(embed=embed , view=AfterClose(Bot))
                                collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                            else:
                                await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                msg= await ctx.followup.send(embed=embed , view=AfterClose(Bot))
                                collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                        else:
                            await ctx.response.send_message(f'you already closed ticket' , ephemeral=True)

                    else:
                        await ctx.edit_original_response(content='you are not allowed to do this')

        except:
            pass

############################################delete ticket



    async def dropdown_callback(ctx:discord.Interaction):
        print ('1')
        if ctx is not None:
    # selector = discord.ui.Select(placeholder=self.button_name , custom_id=self.customer_id , options=self.options)
    # selector.callback = dropdown_callback
            print(selector.values)
            if selector.values[0] == '88':
                await ctx.response.defer()
            else:
                guild_check = ctx.guild.id
                flager_category=False
                if(find:= collection.find_one({"_id":ctx.guild.id})):
                    style_checker = find['style']
                    id_getter = int(selector.values[0])
                    jj_id = collection.find_one({"ID":id_getter , "guild_ider":ctx.guild.id})
                    department = jj_id['admins_name']
                    jj= discord.utils.get(ctx.guild.categories ,id=jj_id['category_id'])
                    if jj is not None:
                        flager_category=True

                    if(find5:= collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})):
                        for i in find5:
                            channel_checker=i['channel_id']
                            checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
                            if checker is None:
                                channel_id = i['channel_id']
                                tmp_guild = i['guild_id']
                                user_tmp = i['user_id']
                                collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})
                        
                        false_checker=collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':False})
                        for i in false_checker:
                            channel_checker=i['channel_id']
                            checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
                            if checker is None:
                                channel_id = i['channel_id']
                                tmp_guild = i['guild_id']
                                user_tmp = i['user_id']
                                collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})

                        if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                            # await ctx.response.defer()
                            guild = ctx.guild
                            member = ctx.user
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True, send_voice_messages=True),
                            }
                            number_of_ticket = await get_count(ctx)
                            if number_of_ticket is None:
                                number_of_ticket = '1'
                                await updater(ctx,number_of_ticket)
                                if len( number_of_ticket) == 1:
                                    number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                
                            elif number_of_ticket is not None:
                                await updater(ctx,number_of_ticket)
                                if len(number_of_ticket) == 1:
                                    number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                elif len(number_of_ticket) == 2:
                                    number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                elif len(number_of_ticket) == 3:
                                    number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                else:
                                    number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                            embeder=await create_embed(ctx)
                            av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
                            av_button.callback = close_button
                            button_view85 = discord.ui.View(timeout=None)
                            button_view85.add_item(av_button)
                            category_id = await get_category(ctx)
                            category = discord.utils.get(ctx.guild.categories , id =category_id)
                            roles = await get_admin(ctx)
                            modal_category = await get_category(ctx)
                            modal_roles=await get_admin(ctx)

                            async def on_sumbit11(ctx=None):
                                try:
                                    print ('33')
                                    if ctx is not None:
                                        print ('44')
                                        if style_checker == 2:
                                            print ('1')
                                            form_title = find['form_title']
                                            form_description= find['form_description']
                                            await ctx.response.defer()
                                            caller =TicketSystem(Bot)
                                            category = discord.utils.get(ctx.guild.categories , id =jj.id)
                                            category_menu = discord.utils.get(ctx.guild.categories , id =jj.id)
                                            embed = caller.create_embed(ctx)
                                            print ('2')
                                            
                                            if category is not None:
                                                print ('3')
                                                channel = await ctx.guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                                            else:
                                                print ('4')
                                                owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                                                await asyncio.sleep(0.5)
                                                channel = await ctx.guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                                                await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')
                                                print ('5')
                                            
                                            print ('6')
                                            embed.add_field(name=f"Department: ",value=f'{department}')
                                            embed.add_field(name=f"{form_title}:",value=f'{title_ticket}')
                                            embed.add_field(name=f"{form_description}:" , value=f'{body_ticket}' , inline=False)
                                            
                                            print ('7')
                                            if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":ctx.guild.id, "state":True})):
                                                pass
                                            else:
                                                collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
                                            
                                            print ('8')
                                            admins = []
                                            text_mention=''
                                            menu_finder = collection.find({'ID':int(selector.values[0]),"guild_ider":ctx.guild.id})
                                            for i in menu_finder:
                                                if i['category_id'] == jj.id:
                                                    tmp_list = i['admins_id']
                                                    for j in tmp_list:
                                                        j=int(j)
                                                        roler_plus = discord.utils.get(ctx.guild.roles , id = j)
                                                        if roler_plus is not None:
                                                            admins.append(j)
                                                            text_mention+=f'<@&{j}> '
                                                            await channel.set_permissions(roler_plus , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True) 
                                        print ('9')
                                        await channel.send(f'your ticket created {ctx.user.mention}\n{text_mention}',embed=embed , view=button_view85)

                                    else:
                                        await ctx.response.send_message(f'the ticket style changed by admins but they didnt send new form' , ephemeral=True)
                                except:       
                                    try:
                                        user_dm = discord.utils.get(ctx.guild.members , id=ctx.user.id)
                                        await user_dm.send('something went wrong to create ticket for you pls try again')
                                    except:
                                        pass
                            modals11 = discord.ui.Modal(title='Ticket System Form')
                            title_modal = await get_title(ctx)
                            body_modal = await get_description(ctx)
                            title_ticket = discord.ui.TextInput(label=title_modal , style=discord.TextStyle.short , required=True)
                            body_ticket = discord.ui.TextInput(label=body_modal , style=discord.TextStyle.long, required=True)
                            modals11.add_item(title_ticket)
                            modals11.add_item(body_ticket)
                            modals11.on_submit=on_sumbit11
                            caller = ModalApplicationForm1(ctx , number_of_ticket , overwrites , av_button , category_id)
                            await ctx.response.send_modal(modals11)         
                        else:
                            await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)


                    else:
                        if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                            # await ctx.response.defer()
                            guild = ctx.guild
                            member = ctx.user
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True),
                            }
                            number_of_ticket = get_count(ctx)
                            if number_of_ticket is None:
                                number_of_ticket = '1'
                                updater(ctx,number_of_ticket)
                                if len( number_of_ticket) == 1:
                                    number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                
                            elif number_of_ticket is not None:
                                updater(ctx,number_of_ticket)
                                if len(number_of_ticket) == 1:
                                    number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                elif len(number_of_ticket) == 2:
                                    number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                elif len(number_of_ticket) == 3:
                                    number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                else:
                                    number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                            av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
                            av_button.callback = close_button
                            button_view = discord.ui.View(timeout=None)
                            button_view.add_item(av_button)
                            category_id = get_category(ctx)
                            category = discord.utils.get(ctx.guild.categories , id =category_id)
                            roles = get_admin(ctx)
                            embeder=create_embed(ctx)
                            modal_category = get_category(ctx)
                            modal_roles=get_admin(ctx)
                            
                            async def on_sumbit(ctx):
                                print ('33')
                                try:
                                    print ('2')
                                    if style_checker == 2:
                                        print ('3')
                                        form_title = find['form_title']
                                        form_description= find['form_description']
                                        embed = embeder
                                        await ctx.response.defer()
                                        caller =TicketSystem(Bot)
                                        category = discord.utils.get(ctx.guild.categories , id =jj.id)
                                        category_menu = discord.utils.get(ctx.guild.categories , id =jj.id)
                                        embed = caller.create_embed(ctx)
                                        print ('4')
                                        
                                        
                                        if category is not None:
                                            print ('5')
                                            channel = await ctx.guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                                        else:
                                            print ('6')
                                            owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                                            await asyncio.sleep(0.5)
                                            channel = await ctx.guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                                            await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                                        print ('7')
                                        embed.add_field(name=f"Department: ",value=f'{department}')
                                        embed.add_field(name=f"{form_title}:",value=f'{title_ticket}')
                                        embed.add_field(name=f"{form_description}:" , value=f'{body_ticket}' , inline=False)
                                        
                                        print ('8')
                                        if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":ctx.guild.id, "state":True})):
                                            print ('9')
                                            pass
                                        else:
                                            print ('10')
                                            collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
                                        
                                        print ('11')
                                        admins = []
                                        text_mention=''
                                        menu_finder = collection.find({'ID':int(selector.values[0]),"guild_ider":ctx.guild.id})
                                        for i in menu_finder:
                                            if i['category_id'] == jj.id:
                                                tmp_list = i['admins_id']
                                                for j in tmp_list:
                                                    j=int(j)
                                                    roler_plus = discord.utils.get(ctx.guild.roles , id = j)
                                                    if roler_plus is not None:
                                                        admins.append(j)
                                                        text_mention+=f'<@&{j}> '
                                                        await channel.set_permissions(roler_plus , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)

                                        print ('12')
                                        await channel.send(f'your ticket created {ctx.user.mention}\n{text_mention}',embed=embed , view=button_view85)
                                        print ('13')
                                    else:
                                        await ctx.response.send_message(f'the ticket style changed by admins but they didnt send new form' , ephemeral=True)
                                except:    
                                    try:
                                        user_dm = discord.utils.get(ctx.guild.members , id=ctx.user.id)
                                        await user_dm.send('something went wrong to create ticket for you pls try again')
                                    except:
                                        pass                        

                            modals1 = discord.ui.Modal(title='Ticket System Form')
                            title_modal = get_title(ctx)
                            body_modal = get_description(ctx)
                            title_ticket = discord.ui.TextInput(label=title_modal , style=discord.TextStyle.short , required=True)
                            body_ticket = discord.ui.TextInput(label=body_modal , style=discord.TextStyle.long, required=True)
                            modals1.add_item(title_ticket)
                            modals1.add_item(body_ticket)
                            modals1.on_submit=on_sumbit
                            await ctx.response.send_modal(modals1)     
                                                                   
    
    ################code dropdown #######################
    find_menu = collection.find({'is_active':False})
    checker_menu1 = collection.find_one({'is_active':False})
    print(checker_menu1)
    if find_menu is not None:
        options = []           
        tmp_guild = []
        place_name = ''
        customerid_menu:str = 'apaticket_dropdown'
        for j in find_menu:
            try:
                tmp_guild.append(j['guild_ider'])
            except:
                pass
        tmp_guild = set(tmp_guild)
        tmp_guild = list(tmp_guild)
        if len(tmp_guild) !=0:
            for i in range(len(tmp_guild)):
                find_menu12 = collection.find({'guild_ider':tmp_guild[i]})
                finder_place = collection.find_one({'_id':tmp_guild[i]})
                place_name = finder_place['button_name']
                for jj in find_menu12:
                    options.append(discord.SelectOption(label=jj['admins_name'] , value=jj['ID'], emoji=f"{jj['emojies']}"))
                    # collection.update_one({'_id':jj['_id'],'ID':jj['ID'] ,'guild_ider':jj['guild_ider'] , 'emojies':jj['emojies'] , 'admins_name':jj['admins_name'] ,'is_active':False} , {'$set':{'is_active':True}})

            options.append(discord.SelectOption(label='remove selection' , value='88', emoji="⛔"))
                # if j['_id'] in self.tmp_category:
                #     self.all_ids.append(j['_id'])
                #     self.options.append(discord.SelectOption(label=j['admins_name'] , value=j['_id'], emoji=f"{j['emojies']}"))
                #     collection.update_one({'_id':j['_id'] ,'guild_ider':j['guild_ider'] , 'emojies':j['emojies'] , 'admins_name':j['admins_name'] ,'is_active':False} , {'$set':{'is_active':True}})
    global selector
    selector = discord.ui.Select(placeholder='click here' , custom_id='create_ticket' , options=options)
    selector.callback = dropdown_callback
    button_view = discord.ui.View(timeout=None)
    button_view.add_item(selector)
    return button_view


################################################################

class adminadd(discord.ui.Modal):
    
    title5 :str = None
    # title_ticket = discord.ui.TextInput(label=title5 , style=discord.TextStyle.short , required=True)
    # body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)

    def __init__(self, ctx):
        self.ctx = ctx
        self.title_ticket = discord.ui.TextInput(label='ID' , style=discord.TextStyle.short , required=True)
        self.body_ticket = discord.ui.TextInput(label='admins role id:' , style=discord.TextStyle.short, required=True)



        super().__init__(title='Ticket System Form' )
        adminadd.add_item(self,item=self.title_ticket)
        adminadd.add_item(self,item=self.body_ticket)



    def id_to_cat(self,ctx):
        var = collection.find_one({"guild_ider":ctx.guild.id , "ID":self.category_menu})
        category_id_main = var['category_id']
        return category_id_main


    async def on_submit(self , interaction:discord.Interaction):
        id_int = str(self.title_ticket)
        id_int = int(id_int)
        if(find:= collection.find_one({"_id":self.ctx.guild.id})):
            menu_finder = collection.find_one({'ID':id_int,"guild_ider":self.ctx.guild.id})
            if menu_finder is not None:
                admin_lists = menu_finder['admins_id']
                admin_int = str(self.body_ticket)
                admin_int = int(admin_int)
                role_checker = discord.utils.get(self.ctx.guild.roles , id= admin_int)
                if role_checker is not None:
                    role_Checker_str = str(role_checker.id)
                    if admin_lists is not None:
                        if role_Checker_str in admin_lists:
                            admin_lists=admin_lists.remove(role_Checker_str)
                            collection.update_one({'ID':id_int,"guild_ider":self.ctx.guild.id} , {'$set':{"admins_id":admin_lists}})
                            await interaction.response.send_message('removed successfully')
                        else:
                            await interaction.response.send_message('this role is not in your admin list of this ID')
                    else:
                        await interaction.response.send_message('you have no admin in this department')
                else:
                    await interaction.response.send_message('this role is not exist')
            else:
                await interaction.response.send_message('your id is not currect or not exist')
        else:
            await interaction.response.send_message(f'you didnt config ticket system') 
            return
class admin_remove_button(ui.View):
    def __init__(self , ctx,bot:Bot):
        super().__init__(timeout=None)
        self.ctx=ctx
        self.bot = bot

    @ui.button(label='Remove Admin' , custom_id='buttontoremoveadmin' , style=discord.ButtonStyle.primary)
    async def buttontoremoveadmin(self, interaction:discord.Interaction,_):
        caller_admin = adminadd(self.ctx)
        await interaction.response.send_modal(caller_admin)


class removeitem(discord.ui.Modal):
    
    title5 :str = None
    # title_ticket = discord.ui.TextInput(label=title5 , style=discord.TextStyle.short , required=True)
    # body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)

    def __init__(self, ctx):
        self.ctx = ctx
        self.title_ticket = discord.ui.TextInput(label='ID' , style=discord.TextStyle.short , required=True)



        super().__init__(title='Ticket System Form' )
        removeitem.add_item(self,item=self.title_ticket)



    def id_to_cat(self,ctx):
        var = collection.find_one({"guild_ider":ctx.guild.id , "ID":self.category_menu})
        category_id_main = var['category_id']
        return category_id_main


    async def on_submit(self , interaction:discord.Interaction):
        id_int = str(self.title_ticket)
        id_int = int(id_int)
        if(find:= collection.find_one({"_id":self.ctx.guild.id})):
            menu_finder = collection.find_one({'ID':id_int,"guild_ider":self.ctx.guild.id})
            if menu_finder is not None:
                collection.delete_one({'ID':id_int,"guild_ider":self.ctx.guild.id})
                id_updater=collection.find({"guild_ider":self.ctx.guild.id})
                tmp_ids = []
                for i in id_updater:
                    tmp_ids.append(i['ID'])
                for j in range(len(tmp_ids)):
                    collection.update_one({'ID':tmp_ids[j],"guild_ider":self.ctx.guild.id} ,{'$set':{'ID':j+1}})
                await interaction.response.send_message('item (department) deleted successfully')
            else:
                await interaction.response.send_message('your id is not currect or not exist')
        else:
            await interaction.response.send_message(f'you didnt config ticket system') 
            return

class item_remove_button(ui.View):
    def __init__(self , ctx,bot:Bot):
        super().__init__(timeout=None)
        self.ctx=ctx
        self.bot = bot

    @ui.button(label='Remove Item' , custom_id='buttontoremoveitem' , style=discord.ButtonStyle.primary)
    async def buttontoremoveitem(self, interaction:discord.Interaction,_):
        caller_admin = removeitem(self.ctx)
        await interaction.response.send_modal(caller_admin)



class addadminmain(discord.ui.Modal):
    
    title5 :str = None
    # title_ticket = discord.ui.TextInput(label=title5 , style=discord.TextStyle.short , required=True)
    # body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)

    def __init__(self, ctx):
        self.ctx = ctx
        self.title_ticket = discord.ui.TextInput(label='ID:' , style=discord.TextStyle.short , required=True)
        self.body_ticket = discord.ui.TextInput(label='Role ID:' , style=discord.TextStyle.short , required=True)



        super().__init__(title='Ticket System Form' )
        addadminmain.add_item(self,item=self.title_ticket)
        addadminmain.add_item(self,item=self.body_ticket)



    def id_to_cat(self,ctx):
        var = collection.find_one({"guild_ider":ctx.guild.id , "ID":self.category_menu})
        category_id_main = var['category_id']
        return category_id_main


    async def on_submit(self , interaction:discord.Interaction):
        id_int = str(self.title_ticket)
        id_int = int(id_int)
        role_int = str(self.body_ticket)
        role_int = int(role_int)
        if(find:= collection.find_one({"_id":self.ctx.guild.id})):
            menu_finder = collection.find_one({'ID':id_int,"guild_ider":self.ctx.guild.id})
            role_checker = discord.utils.get(self.ctx.guild.roles , id=role_int)
            if menu_finder is not None:
                admins_ids = menu_finder['admins_id']
                if role_checker is not None:
                    if len(admins_ids)!=0:
                        role_checker_id = str(role_checker.id)
                        if role_checker_id in admins_ids:
                            await interaction.response.send_message('this role is already exist')
                            return
                        else:
                            tmp_list=[]
                            tmp_list.extend(admins_ids)
                            tmp_list.append(role_checker_id)
                            collection.update_one({'ID':id_int,"guild_ider":self.ctx.guild.id} , {'$set':{'admins_id':tmp_list}})
                            await interaction.response.send_message('admin added successfully')
                            return
                    else:
                        role_checker_id = str(role_checker.id)
                        tmp_list=[]
                        tmp_list.append(role_checker_id)
                        collection.update_one({'ID':id_int,"guild_ider":self.ctx.guild.id} , {'$set':{'admins_id':tmp_list}})
                        await interaction.response.send_message('admin added successfully')
                        return
                else:
                    await interaction.response.send_message('this role is not exist')
                    return
            else:
                await interaction.response.send_message('your id is not currect or not exist')
                return
        else:
            await interaction.response.send_message(f'you didnt config ticket system') 
            return

class admin_add_button(ui.View):
    def __init__(self , ctx,bot:Bot):
        super().__init__(timeout=None)
        self.ctx=ctx
        self.bot = bot

    @ui.button(label='Add Admin' , custom_id='buttontaddadmin' , style=discord.ButtonStyle.primary)
    async def buttontaddadmin(self, interaction:discord.Interaction,_):
        caller_admin = addadminmain(self.ctx)
        await interaction.response.send_modal(caller_admin)



class ticketsendbutton(ui.View):
    def __init__(self , ctx,bot:Bot):
        super().__init__(timeout=None)
        self.ctx=ctx
        self.bot = bot

    @ui.button(label='Send Ticket' , custom_id='sendbutton' , style=discord.ButtonStyle.primary)
    async def sendbutton(self, ctx:discord.Interaction,_):
        guild_check = self.ctx.guild.id
        if(find5:= collection.find({"user_id":self.ctx.user.id, "guild_id":guild_check , 'state':True})):
            for i in find5:
                channel_checker=i['channel_id']
                checker = discord.utils.get(self.ctx.guild.text_channels , id=channel_checker )
                if checker is None:
                    channel_id = i['channel_id']
                    tmp_guild = i['guild_id']
                    user_tmp = i['user_id']
                    collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})
            
            false_checker=collection.find({"user_id":self.ctx.user.id, "guild_id":guild_check , 'state':False})
            for i in false_checker:
                channel_checker=i['channel_id']
                checker = discord.utils.get(self.ctx.guild.text_channels , id=channel_checker )
                if checker is None:
                    channel_id = i['channel_id']
                    tmp_guild = i['guild_id']
                    user_tmp = i['user_id']
                    collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})

            if(find2:= collection.find_one({"user_id":self.ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                # await ctx.response.defer()
                guild = self.ctx.guild
                member = self.ctx.user
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True, send_voice_messages=True),
                }
                number_of_ticket = self.get_count(self.ctx)
                if number_of_ticket is None:
                    number_of_ticket = '1'
                    self.updater(self.ctx,number_of_ticket)
                    if len( number_of_ticket) == 1:
                        number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                    
                elif number_of_ticket is not None:
                    self.updater(self.ctx,number_of_ticket)
                    if len(number_of_ticket) == 1:
                        number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                    elif len(number_of_ticket) == 2:
                        number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                    elif len(number_of_ticket) == 3:
                        number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                    else:
                        number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                
                category_id = self.get_category(self.ctx)
                category = discord.utils.get(self.ctx.guild.categories , id =category_id)
                modals = discord.ui.Modal(title='Ticket Form')
                title_ticket = discord.ui.TextInput(label='enter your title' , style=discord.TextStyle.short , required=True)
                body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)
                modals.add_item(title_ticket)
                modals.add_item(body_ticket)
                roles = self.get_admin(self.ctx)
                av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red,custom_id='close_ticket' )
                av_button.callback = close_button
                button_view = discord.ui.View(timeout=None)
                button_view.add_item(av_button)
                caller = ModalApplicationForm(self.ctx ,number_of_ticket ,overwrites , button_view)
                await self.ctx.response.send_modal(caller)
                
                # av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red )
                # av_button.callback = close_button
                # button_view = discord.ui.View(timeout=None)
                # button_view.add_item(av_button)
                
                # async def on_sumbit(self,ctx):
                #     await ctx.defer()
                #     if category is not None:
                #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                #     else:
                #         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                #         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                #     embed.add_field(name='Ticket title:',value=f'{title_ticket}')
                #     embed.add_field(name='Ticket Description' , value=f'{body_ticket}')

                #     await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=button_view)
                #     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
                #         pass
                #     else:
                #         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True})
                #     admins = []
                #     if roles is not None:
                #         for i in roles:
                #             checker=discord.utils.get(guild.roles, id=i)
                #             if checker is not None:
                #                 await channel.set_permissions(checker , read_messages=True , send_messages=True)
                #                 return

                
            else:
                await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)

        else:
            if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                # await ctx.response.defer()
                guild = ctx.guild
                member = ctx.user
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                }
                number_of_ticket = self.get_count(ctx)
                if number_of_ticket is None:
                    number_of_ticket = '1'
                    self.updater(ctx,number_of_ticket)
                    if len( number_of_ticket) == 1:
                        number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                    
                elif number_of_ticket is not None:
                    self.updater(ctx,number_of_ticket)
                    if len(number_of_ticket) == 1:
                        number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                    elif len(number_of_ticket) == 2:
                        number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                    elif len(number_of_ticket) == 3:
                        number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                    else:
                        number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                
                category_id = self.get_category(ctx)
                category = discord.utils.get(ctx.guild.categories , id =category_id)
                modals = discord.ui.Modal(title='Ticket Form')
                title_ticket = discord.ui.TextInput(label='enter your title' , style=discord.TextStyle.short , required=True)
                body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)
                modals.add_item(title_ticket)
                modals.add_item(body_ticket)
                roles = self.get_admin(ctx)
                av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
                av_button.callback = close_button
                button_view = discord.ui.View(timeout=None)
                button_view.add_item(av_button)
                caller = ModalApplicationForm(ctx ,number_of_ticket ,overwrites , button_view)
                await ctx.response.send_modal(caller)
                
                # av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red )
                # av_button.callback = close_button
                # button_view = discord.ui.View(timeout=None)
                # button_view.add_item(av_button)
                
                # async def on_sumbit(self,ctx):
                #     await ctx.defer()
                #     if category is not None:
                #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                #     else:
                #         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                #         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                #     embed.add_field(name='Ticket title:',value=f'{title_ticket}')
                #     embed.add_field(name='Ticket Description' , value=f'{body_ticket}')

                #     await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=button_view)
                #     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
                #         pass
                #     else:
                #         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True})
                #     admins = []
                #     if roles is not None:
                #         for i in roles:
                #             checker=discord.utils.get(guild.roles, id=i)
                #             if checker is not None:
                #                 await channel.set_permissions(checker , read_messages=True , send_messages=True)
                #                 return
            else:
                await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)


class TicketSystem(Plugin):
    def __init__(self , bot:Bot):
        self.bot = bot

    async def cog_load(self):
        await super().cog_load()
        self.bot.add_view(buttons(self.bot))
        sss = await updater_list()
        self.bot.add_view(sss)
        # counter1 = collection.count_documents(filter={'is_active':False})
        # for i in range(counter1+1):
        #     self.instancer = updater_new(self.bot)
        #     self.final_instancer=self.instancer.menu_view()
        #     if self.final_instancer is not None:
        #         self.bot.add_view(self.final_instancer)

        # collection.update_many({'update':True} , {'$set':{'update':False}})
        # counter = collection.count_documents(filter={'update':False})
        # for j in range(counter+1):
        #     self.instancer = updater_new(self.bot)
        #     self.final_instancer=self.instancer.view()
        #     if self.final_instancer is not None:
        #         self.bot.add_view(self.final_instancer)
        
        # collection.update_many({'is_active':True} , {'$set':{'is_active':False}})





    @commands.hybrid_command(name='ticket_config' , description='installation ticket system')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @app_commands.describe(
        title='title of the ticket embed post for people to create ticket',
        description='description of embed post for people to create ticket use /n for going to new line',
        button_name='the name of the button for click to create ticket',
        form_title = 'its will define as subject of a ticket in embed and form',
        form_description='its will define as description of a ticket in embed and form',
        embed_message='exp: wait for support to answer you',
        category='the tickets will create in this category'
    )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def ticket_config(self, ctx , title:str , description:str ,button_name:str ,form_title:str , form_description:str , embed_message:str , category:discord.CategoryChannel):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        try:
            if len(title)>100:
                await ctx.send('use maximum 100 characters for title')
                return
            if len(description) >900:
                await ctx.send('use maximum 900 characters for description')
                return
            if len(button_name)>50:
                await ctx.send('use maximum 30 characters for button name')
                return
            if len(form_title)>40:
                await ctx.send('use maximum 40 characters for form title')
                return
            if len(form_description)>40:
                await ctx.send('use maximum 40 characters for form description')
                return
            if len(embed_message)>500:
                await ctx.send('use maximum 500 characters for embed message')
                return
            final_text:str=''
            message_spliter = list(description.split('/n'))
            for i in range(len(message_spliter)):
                if i != len(message_spliter)-1:
                    final_text += f'{message_spliter[i]}\n'
                else:
                    final_text += f'{message_spliter[i]}'
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                category_check = discord.utils.get(ctx.guild.categories, id = category.id)
                if category_check is not None:            
                    collection.update_one({"_id":ctx.guild.id},{"$set":{ "title":title , "description":final_text , "category":category.id,"button_name":button_name , "count":None , "form_title":form_title , "form_description":form_description , "embed_message":embed_message }})
                    await ctx.send('settings saved')
                else:
                    await ctx.send('the category channel is not exist try again!')
                    return
            else:
                category_check = discord.utils.get(ctx.guild.categories, id = category.id)
                if category_check is not None:
                    collection.insert_one({"_id":ctx.guild.id , "title":title , "description":final_text , "category":category.id , "admins":None , "button_name":button_name , "count":None , "form_title":form_title , "form_description":form_description , "embed_message":embed_message , 'style':None})
                    await ctx.send('settings saved')
                else:
                    await ctx.send('the category channel is not exist try again!')
                    return
        except:
            await ctx.send('something went wrong pls try again')


    @commands.hybrid_command(name='ticket_show_admins' , description='show all ticket system admins')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @app_commands.choices(style=[
        app_commands.Choice(name='button' , value=1),
        app_commands.Choice(name='menu' , value=2),
    ])
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def Ticket_showw_admins(self, ctx , style:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            if style.value == 1:
                admins = find['admins']
                new_admins = []
                if admins is not None:
                    for i in admins:
                        checker = discord.utils.get(ctx.guild.roles , id = i)
                        if checker is not None:
                            user = '<@&' + str(i) + '>'
                            new_admins.append(user)
                    embed = discord.Embed(
                        title='APA BOT',
                        description=f'Ticket System Admins:\n{new_admins}',
                        timestamp=datetime.now()
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    await ctx.send(f'there is no admin in your admin section to show !')
                    return
            elif style.value == 2:
                if(find1:= collection.find({"guild_ider":ctx.guild.id})):
                    final_text = ''
                    for i in find1:
                        admins = i['admins_id']
                        department_name = i['admins_name']
                        category = i['category_id']
                        new_admins = []
                        category_checker = discord.utils.get(ctx.guild.categories , id=category )
                        if category_checker is not None:
                            final_text += f'> department name: {department_name}\n admins: '
                        else:
                            pass
                        if admins is not None:
                            for j in admins:
                                j=int(j)
                                checker = discord.utils.get(ctx.guild.roles , id = j)
                                if checker is not None:
                                    final_text+= '<@&' + str(j) + '>' + ' '
                            final_text+='\n'
                        else:
                            final_text+='\n'

                                


                    embed = discord.Embed(
                        title='APA BOT',
                        description=f'Ticket Menu System Admins:\n{final_text}',
                        timestamp=datetime.now()
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    await ctx.send(f'there is no admin in your admin section to show !')
                    return

        else:
            await ctx.send(f'you didnt config ticket system') 
            return

    @commands.hybrid_command(name='ticket_remove_all' , description='removing all of your admins')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def Ticket_remove_all(self, ctx):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                admins = find['admins']
                if admins is not None:
                    if len(admins)>0:
                        collection.update_one({"_id":ctx.guild.id},{"$set":{"admins":None}})
                        await ctx.send(f'all of your admins in button section removed successfully')
                    else:
                        await ctx.send('there is no admin to delete in button section')
                        
                else:
                    await ctx.send('there is nothing in your admin button section !')
                    
                if(find1:= collection.find({"guild_ider":ctx.guild.id})):

                    collection.update_many({"guild_ider":ctx.guild.id},{"$set":{"admins_id":None}})
                    await ctx.send(f'all of your admins in dropdown section removed successfully')
                else:
                    await ctx.send('there is no dropdown section config to check their admins and deleting them')


            else:
                await ctx.send(f'you didnt config ticket system') 
                return
        except:
            await ctx.send('something went wrong pls try again')


    @commands.hybrid_command(name='ticket_remove_admin_menu' , description='remove specific admin from menu style')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def Ticket_remove_menu_admin(self, ctx):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            if(find1:= collection.find({"guild_ider":ctx.guild.id})):
                final_text = ''
                for i in find1:
                    admins = i['admins_id']
                    department_name = i['admins_name']
                    category = i['category_id']
                    new_admins = []
                    category_checker = discord.utils.get(ctx.guild.categories , id=category )
                    if category_checker is not None:
                        final_text += f'> department name: {department_name}\n ID:{i["ID"]} \nadmins: '
                    else:
                        pass
                    if admins is not None:
                        for j in admins:
                            j=int(j)
                            checker = discord.utils.get(ctx.guild.roles , id = j)
                            if checker is not None:
                                final_text+= '<@&' + str(j) + '>' + ' '
                        final_text+='\n'

                            


                embed = discord.Embed(
                    title='APA BOT',
                    description=f'Ticket Menu System Admins:\n{final_text}',
                    timestamp=datetime.now()
                )
                embed.add_field(name='Help' , value="you must remove admin by the ID of your department ID so remember it and click the below button and enter the exact ID and role ID to remove otherwise it won't work")
                await ctx.send(embed=embed , view=admin_remove_button(ctx,self.bot))
                return
            else:
                await ctx.send('there is no item(department) in your ticket menu system')
        else:
            await ctx.send('you didn`t config ticket system')
        



    @commands.hybrid_command(name='ticket_remove_menu_item' , description='remove specific item from dropdown menu of ticket')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def Ticket_remove_menu(self, ctx , remove_all:Optional[bool]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        if remove_all == True:
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if(find1:= collection.find({"guild_ider":ctx.guild.id})):

                    collection.delete_many({"guild_ider":ctx.guild.id})
                    await ctx.send('all items deleted successfully')
                    return
                else:
                    await ctx.send('there is no item(department) in your ticket menu system')
                    return
            else:
                await ctx.send('you didn`t config ticket system')
                return
        else:
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                if(find1:= collection.find({"guild_ider":ctx.guild.id})):
                    final_text = ''
                    for i in find1:
                        admins = i['admins_id']
                        department_name = i['admins_name']
                        category = i['category_id']
                        new_admins = []
                        category_checker = discord.utils.get(ctx.guild.categories , id=category )
                        if category_checker is not None:
                            final_text += f'> department name: {department_name}\n ID:{i["ID"]} \nadmins: '
                        else:
                            pass
                        if admins is not None:
                            for j in admins:
                                j=int(j)
                                checker = discord.utils.get(ctx.guild.roles , id = j)
                                if checker is not None:
                                    final_text+= '<@&' + str(j) + '>' + ' '
                            final_text+='\n'

                                


                    embed = discord.Embed(
                        title='APA BOT',
                        description=f'Ticket Menu System Admins:\n{final_text}',
                        timestamp=datetime.now()
                    )
                    embed.add_field(name='Help' , value="you must remove item by the ID of your department ID so remember it and click the below button and enter the exact ID to remove otherwise it won't work")
                    await ctx.send(embed=embed , view=item_remove_button(ctx,self.bot))
                    return
                else:
                    await ctx.send('there is no item(department) in your ticket menu system')
                    return
            else:
                await ctx.send('you didn`t config ticket system')
                return


    @commands.hybrid_command(name='ticket_remove_admin_button' , description='remove specific admin')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def Ticket_remove_admin(self, ctx ,admin_choose:discord.Role):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        try:
            flag= False
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                admins = find['admins']
                if admins is not None:
                    if len(admins)>0:
                        for i in admins:
                            if i == admin_choose.id:
                                admins.remove(i)
                                collection.update_one({"_id":ctx.guild.id} , {"$set":{"admins":admins}})
                                flag =True
                                break

                        if flag == True:
                            await ctx.send(f'admin removed successfully')
                        else:
                            await ctx.send(f'i cant find this role in your ticket admin section')
                    else:
                        await ctx.send('there is nothing in your admin section !')
                        return
                else:
                    await ctx.send('there is nothing in your admin section !')
                    return
            else:
                await ctx.send(f'you didnt config ticket system') 
                return
        except:
            await ctx.send('something went wrong pls try again')


    @commands.hybrid_command(name='ticket_add_admin_button' , description='add admin to ticket system')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def Ticket_add_admin(self, ctx , role:discord.Role):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        try:
            role_check = discord.utils.get(ctx.guild.roles, id = role.id)
            if role_check is not None:
                if(find:= collection.find_one({"_id":ctx.guild.id})):
                    admins = find['admins']
                    if admins is not None:
                        roles = []
                        roles.append(role.id)
                        roles.extend(admins)
                        collection.update_one({"_id":ctx.guild.id} , {"$set":{"admins":roles}})
                        await ctx.send('settings saved')
                        return
                    else:
                        roles = []
                        roles.append(role.id)
                        collection.update_one({"_id":ctx.guild.id} , {"$set":{"admins":roles}})
                        await ctx.send('setting saved')
                        return
                else:
                    await ctx.send('use ticket config first then use this')
                    return
            
            else:
                await ctx.send("the role is not exist")
                return
        except:
            await ctx.send('something went wrong pls try again')

    @commands.hybrid_command(name='ticket_add_admin_menu' , description='add admin to ticket system')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def Ticket_add_admin(self, ctx):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            if(find1:= collection.find({"guild_ider":ctx.guild.id})):
                final_text = ''
                for i in find1:
                    admins = i['admins_id']
                    department_name = i['admins_name']
                    category = i['category_id']
                    new_admins = []
                    category_checker = discord.utils.get(ctx.guild.categories , id=category )
                    if category_checker is not None:
                        final_text += f'> department name: {department_name}\n ID:{i["ID"]} \nadmins: '
                    else:
                        pass
                    if admins is not None:
                        for j in admins:
                            j=int(j)
                            checker = discord.utils.get(ctx.guild.roles , id = j)
                            if checker is not None:
                                final_text+= '<@&' + str(j) + '>' + ' '
                        final_text+='\n'

                            


                embed = discord.Embed(
                    title='APA BOT',
                    description=f'Ticket Menu System Admins:\n{final_text}',
                    timestamp=datetime.now()
                )
                embed.add_field(name='Help' , value="you must add admin by the ID of your department ID so remember it and click the below button and enter the exact ID and role ID to add admin otherwise it won't work")
                await ctx.send(embed=embed , view=admin_add_button(ctx,self.bot))
                return
            else:
                await ctx.send('there is no item(department) in your ticket menu system')
                return
        else:
            await ctx.send('you didn`t config ticket system')
            return


    def get_count(self,ctx):
        if(find:= collection.find_one({"_id":ctx.guild.id})):
            counter=find['count']
            return counter

    def updater(self ,ctx ,  number_of_ticket):
        number_of_ticket = int(number_of_ticket)
        number_of_ticket+=1
        number_of_ticket = str(number_of_ticket)
        collection.update_one({"_id":ctx.guild.id},{"$set":{ "count":number_of_ticket}})

    def support_embed(self ):
        embed=discord.Embed(
            title ='APA BOT',
            description=f"Support Panel:",
            color=None
        )
        return embed


    def create_embed(self,ctx):
        var = collection.find_one({"_id":ctx.guild.id})
        message = var['embed_message']
        embed=discord.Embed(
            title ='APA BOT',
            description=f"{message}",
            color= 0xF6F6F6,
            timestamp=datetime.now()
        )
        return embed
    
    def close_button_updater(self,ctx):
        collection.update_one({ 'guild_id':ctx.guild.id, "channel_id":ctx.channel_id},{"$set":{ "state":False}})
    
    def open_button_updater(self,ctx):
        collection.update_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False},{"$set":{ "state":True}})

    def delete_button_deleter(self,ctx):
        collection.delete_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False})

    def get_category(self,ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        category_id = find['category']
        return category_id

    def get_admin(self,ctx):
        find=collection.find_one({"_id":ctx.guild.id})
        admins = find['admins']
        return admins
    
    # def updater_modal(self,ctx,item1,item2):
    #     find=collection.find_one({"_id":ctx.guild.id})
    #     collection.update_one({"guild_id":ctx.guild.id} , {'$set':{'admins_id':item1 , 'admins_category':item2}})
        
    def model_creator(self):
        form_new = discord.ui.Modal(title='CATEGORY SETTINGS' , timeout=None )
        name_section = discord.ui.TextInput(label='name to show in menu' , style=discord.TextStyle.short , required=True)
        emoji_section = discord.ui.TextInput(label='emoji of name' , style=discord.TextStyle.short , required=True)
        category_section = discord.ui.TextInput(label='category id' , style=discord.TextStyle.short , required=True)
        role_id_section = discord.ui.TextInput(label='admin role id' , style=discord.TextStyle.short , required=True)
        form_new.add_item(name_section)
        form_new.add_item(emoji_section)
        form_new.add_item(category_section)
        form_new.add_item(role_id_section)
        return emoji_section,name_section,category_section,role_id_section,form_new


    @commands.hybrid_command(name='ticket_style' , description='choose ticket option')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @app_commands.choices(style=[
        app_commands.Choice(name='button' , value=1),
        app_commands.Choice(name='menu' , value=2),
    ])

    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def Ticket_style(self, ctx , style:app_commands.Choice[int]):
        guild_check = ctx.guild.id
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)

        if(find:= collection.find_one({"_id":ctx.guild.id})):
            collection.update_one({"_id":ctx.guild.id} , {'$set':{'style':style.value}})
            if style.value ==1:
                await ctx.send('style change done')
                if (find5:=collection.find_one({'guild_checker':ctx.guild.id})):
                    checker_channel_last = find5['channel']
                    checker_msg_id = find5['msg']
                    if style.value != find['style']:
                        checker_channel_last = discord.utils.get(ctx.guild.text_channels , id=checker_channel_last) 
                        if checker_channel_last is not None and checker_msg_id is not None:
                            async for messager in checker_channel_last.history(limit=None):
                                if messager.id == checker_msg_id:
                                    await messager.delete()
                                    await ctx.send('your past ticket embed deleted send it again')

            else:
                if (find5:=collection.find_one({'guild_checker':ctx.guild.id})):
                    checker_channel_last = find5['channel']
                    checker_msg_id = find5['msg']
                    if style.value != find['style']:
                        checker_channel_last = discord.utils.get(ctx.guild.text_channels , id=checker_channel_last) 
                        if checker_channel_last is not None and checker_msg_id is not None:
                            async for messager in checker_channel_last.history(limit=None):
                                if messager.id == checker_msg_id:
                                    await messager.delete()
                                    await ctx.send('your past ticket embed deleted send it again')

                async def modal_callback(ctx):
                    await ctx.response.defer()
                    try:
                        if category_second is not None:
                            category_int = str(category_second)
                            role_int = str(role_id_second)
                            role_int = role_int.split(',')
                            name_checker  = str(name_second)
                            emoji_checker = str(emoji_second)
                    except:
                        category_int = str(category_section)
                        role_int = str(role_id_section)
                        role_int = role_int.split(',')
                        name_checker  = str(name_section)
                        emoji_checker = str(emoji_section)
                    
                    emoji_list = list(emoji_checker.split(','))
                    tmp_emoji=[]
                    for i in emoji_list:
                        i = i.replace("'" , "")
                        i = i.replace(' ','')
                        tmp_emoji.append(i)

                    if len(name_checker) > 60:
                        return
                    flag=False
                    category_int=int(category_int)
                    for i in role_int:
                        i=int(i)
                        role_checker = discord.utils.get(ctx.guild.roles , id=i)
                        if role_checker is None:
                            flag=True
                                            
                    category_checker = discord.utils.get(ctx.guild.categories , id=category_int)
                    role_checker = discord.utils.get(ctx.guild.roles , id=role_int)
                    if category_checker is None or flag==True:
                        await ctx.followup.send('check category id or role id again something is wrong')
                    else:
                        counter = collection.count_documents(filter={'category_id':category_int, 'guild_ider':ctx.guild.id})
                        if counter is not None:
                            if counter == 24:
                                await ctx.edit_original_response(content='you cant add more than 25 items goodbye',embed=None , view=None)
                                return
                            else:
                                counter+=1
                                collection.insert_one({'category_id':category_int , 'guild_ider':ctx.guild.id, 'emojies':tmp_emoji[0],'admins_id':role_int , 'admins_name':name_checker , 'is_active':False , 'ID':counter})
                        else:
                            collection.insert_one({'category_id':category_int , 'guild_ider':ctx.guild.id, 'emojies':tmp_emoji[0],'admins_id':role_int , 'admins_name':name_checker , 'is_active':False , 'ID':1})

                        embed_question=discord.Embed(
                            title='Notice',
                            description='do you wanna add more?'
                        )
                        embed_yes = discord.Embed(
                            title = 'Add category and admin',
                            description = 'in inputs enter category id and role ids and click the button to open the form'
                        )
                        embed_no = discord.Embed(
                            title='goodbye',
                            description='you can close this tab now'
                        )
                        
                        async def yes_button(ctx):
                            await ctx.response.defer()
                            buttone_new5 = discord.ui.Button(label='Form' , style=discord.ButtonStyle.green)
                            global category_second
                            global role_id_second     
                            global name_second
                            global emoji_second                       
                            emoji_second,name_second,category_second , role_id_second , form_new6 = self.model_creator()
                            form_new6.on_submit = modal_callback
                            async def callback5(ctx):
                                await ctx.response.send_modal(form_new6)

                            buttone_new5.callback=callback5
                            viewer5 = discord.ui.View(timeout=None)
                            viewer5.add_item(buttone_new5)

                            await ctx.edit_original_response(embed=embed_yes , view=viewer5)
                            return

                        async def no_button(ctx):
                            await ctx.response.defer()
                            await ctx.edit_original_response(embed=embed_no , view=None)



                        buttone_new2 = discord.ui.Button(label='yes' , custom_id='yes' , style=discord.ButtonStyle.green)
                        buttone_new3 = discord.ui.Button(label='no' , custom_id='no' , style=discord.ButtonStyle.red)
                        buttone_new2.callback=yes_button
                        buttone_new3.callback=no_button
                        viewer1 = discord.ui.View(timeout=None)
                        viewer1.add_item(buttone_new2)
                        viewer1.add_item(buttone_new3)
                        await ctx.edit_original_response(embed=embed_question , view=viewer1)
                        return
                        # await ctx.followup.send('done')

                # form_new = discord.ui.Modal(title='CATEGORY SETTINGS' , timeout=None )
                # category_section = discord.ui.TextInput(label='category id' , style=discord.TextStyle.short , required=True)
                # role_id_section = discord.ui.TextInput(label='admin role id' , style=discord.TextStyle.short , required=True)
                # form_new.add_item(category_section)
                # form_new.add_item(role_id_section)
                emoji_section,name_section,category_section , role_id_section , form_new = self.model_creator()
                form_new.on_submit = modal_callback


                embed = discord.Embed(
                    title = 'Add category and admin',
                    description = 'in inputs enter category id and role ids and click the button to open the form'
                )
                async def callback(ctx):
                    await ctx.response.send_modal(form_new)

                buttone_new = discord.ui.Button(label='Form' , style=discord.ButtonStyle.green)
                buttone_new.callback=callback
                viewer = discord.ui.View(timeout=None)
                viewer.add_item(buttone_new)
                msg=await ctx.send(embed=embed , view=viewer , ephemeral=True)


            
        else:
            await ctx.send('Please setup ticket config first')


    @commands.hybrid_command(name='ticket_send' , description='send ticket creation form')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(use_application_commands=True)
    @commands.has_permissions(use_application_commands=True)
    @app_commands.choices(embed_color=[
        app_commands.Choice(name='white' , value=1),
        app_commands.Choice(name='black' , value=2),
        app_commands.Choice(name='purple' , value=3),
        app_commands.Choice(name='blue' , value=4),
        app_commands.Choice(name='red' , value=5),
        app_commands.Choice(name='pink' , value=6),
        app_commands.Choice(name='yellow' , value=7),
        app_commands.Choice(name='green' , value=8)

    ])

    @commands.cooldown(1, 10, commands.BucketType.guild)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    async def Ticket_send(self, ctx , channel:discord.TextChannel , embed_color:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('your role is not above me then you cant use this command' , ephemeral=True)
        try:
            await ctx.defer()
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                style_checker = find['style']
                if style_checker == 1:
                    guild_check = ctx.guild.id
                    async def open_button_callback(ctx):
                        await ctx.response.defer()
                        if(find2:= collection.find_one({'guild_id':guild_check, "channel_id":ctx.channel_id , 'state':False})):
                            modal_roles=self.get_admin(ctx)
                            flager=False
                            if modal_roles is not None:
                                for i in ctx.user.roles:
                                    if i.id in modal_roles:
                                        flager=True
                            perm_checker= ctx.user.guild_permissions.administrator
                            if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                                flager=True
                            if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                                if find2['open_state'] == False:
                                    collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':True , 'close_state':False}})
                                    channel=find2['channel_id']
                                    member = find2['user_id']
                                    channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                                    member_checker=discord.utils.get(ctx.guild.members, id=member)
                                    permission_check = channel_temp.overwrites
                                    msg = find2['msg_id']
                                    for i in permission_check:
                                        if i.id == member:
                                            await asyncio.sleep(0.5)
                                            await channel_temp.set_permissions(member_checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                            async for messager in ctx.channel.history(limit=None):
                                                if messager.id == msg:
                                                    await messager.delete()
                                            self.open_button_updater(ctx)
                                else:
                                    pass
                            else:
                                await ctx.edit_original_response(content='you are not allowed to do this')

                        else:
                            await ctx.edit_original_response(content='you are not allowed to do this')

                    async def delete_button(ctx):
                        if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                            await ctx.response.defer()
                            modal_roles=self.get_admin(ctx)
                            flager=False
                            if modal_roles is not None:
                                for i in ctx.user.roles:
                                    if i.id in modal_roles:
                                        flager=True
                            perm_checker= ctx.user.guild_permissions.administrator
                            if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                                flager=True
                            if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                                channel=find2['channel_id']
                                channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                                self.delete_button_deleter(ctx)
                                await ctx.followup.send(f'ticket will be deleted in next 1 seconds')
                                await asyncio.sleep(1)
                                await channel_temp.delete()
                            else:
                                await ctx.edit_original_response(content='you are not allowed to do this')
                    async def close_button(ctx):
                        if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                            modal_roles=self.get_admin(ctx)
                            flager=False
                            if modal_roles is not None:
                                for i in ctx.user.roles:
                                    if i.id in modal_roles:
                                        flager=True
                            perm_checker= ctx.user.guild_permissions.administrator
                            if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                                flager=True
                            if find2['user_id']==ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                                if find2['close_state'] == False:
                                    channel=find2['channel_id']
                                    member = find2['user_id']
                                    channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                                    member_checker=discord.utils.get(ctx.guild.members, id=member)
                                    self.close_button_updater(ctx)
                                    ########## buttons section for support
                                    embed = self.support_embed()
                                    av_button = discord.ui.Button(label ='DELETE TICKET' , style=discord.ButtonStyle.red , custom_id='delete_ticket' )
                                    open_button = discord.ui.Button(label ='OPEN TICKET' , style=discord.ButtonStyle.green , custom_id='open_ticket' )

                                    av_button.callback = delete_button
                                    open_button.callback = open_button_callback

                                    button_view = discord.ui.View(timeout=None)
                                    button_view.add_item(av_button)
                                    button_view.add_item(open_button)

                                    collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':False , 'close_state':True}})
                                    if member_checker is not None:
                                        await channel_temp.set_permissions(member_checker , read_messages=False, attach_files=False , send_messages=False,read_message_history=False, send_voice_messages=False)
                                        await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                        msg= await ctx.followup.send(embed=embed , view=button_view)
                                        collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                                    else:
                                        await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                        msg= await ctx.followup.send(embed=embed , view=button_view)  
                                        collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                                else:
                                    await ctx.response.send_message(f'you already closed ticket' , ephemeral=True)
                            else:
                                pass

                            
                    ########################button ticket create######################################
                    async def button_callback(ctx):
                        
                        if(find5:= collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})):
                            for i in find5:
                                channel_checker=i['channel_id']
                                checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
                                if checker is None:
                                    channel_id = i['channel_id']
                                    tmp_guild = i['guild_id']
                                    user_tmp = i['user_id']
                                    collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})
                            
                            false_checker=collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':False})
                            for i in false_checker:
                                channel_checker=i['channel_id']
                                checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
                                if checker is None:
                                    channel_id = i['channel_id']
                                    tmp_guild = i['guild_id']
                                    user_tmp = i['user_id']
                                    collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})

                            if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                                # await ctx.response.defer()
                                guild = ctx.guild
                                member = ctx.user
                                overwrites = {
                                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                    member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True, send_voice_messages=True),
                                }
                                number_of_ticket = self.get_count(ctx)
                                if number_of_ticket is None:
                                    number_of_ticket = '1'
                                    self.updater(ctx,number_of_ticket)
                                    if len( number_of_ticket) == 1:
                                        number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                    
                                elif number_of_ticket is not None:
                                    self.updater(ctx,number_of_ticket)
                                    if len(number_of_ticket) == 1:
                                        number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                    elif len(number_of_ticket) == 2:
                                        number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                    elif len(number_of_ticket) == 3:
                                        number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                    else:
                                        number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                                
                                category_id = self.get_category(ctx)
                                category = discord.utils.get(ctx.guild.categories , id =category_id)
                                modals = discord.ui.Modal(title='Ticket Form')
                                title_ticket = discord.ui.TextInput(label='enter your title' , style=discord.TextStyle.short , required=True)
                                body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)
                                modals.add_item(title_ticket)
                                modals.add_item(body_ticket)
                                roles = self.get_admin(ctx)
                                av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red,custom_id='close_ticket' )
                                av_button.callback = close_button
                                button_view = CloseTicketAW(self.bot)
                                caller = ModalApplicationForm(ctx ,number_of_ticket ,overwrites , button_view)
                                await ctx.response.send_modal(caller)
                                
                                # av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red )
                                # av_button.callback = close_button
                                # button_view = discord.ui.View(timeout=None)
                                # button_view.add_item(av_button)
                                
                                # async def on_sumbit(self,ctx):
                                #     await ctx.defer()
                                #     if category is not None:
                                #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                                #     else:
                                #         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                                #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                                #         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                                #     embed.add_field(name='Ticket title:',value=f'{title_ticket}')
                                #     embed.add_field(name='Ticket Description' , value=f'{body_ticket}')

                                #     await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=button_view)
                                #     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
                                #         pass
                                #     else:
                                #         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True})
                                #     admins = []
                                #     if roles is not None:
                                #         for i in roles:
                                #             checker=discord.utils.get(guild.roles, id=i)
                                #             if checker is not None:
                                #                 await channel.set_permissions(checker , read_messages=True , send_messages=True)
                                #                 return

                                
                            else:
                                await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)

                        else:
                            if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                                # await ctx.response.defer()
                                guild = ctx.guild
                                member = ctx.user
                                overwrites = {
                                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                    member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                }
                                number_of_ticket = self.get_count(ctx)
                                if number_of_ticket is None:
                                    number_of_ticket = '1'
                                    self.updater(ctx,number_of_ticket)
                                    if len( number_of_ticket) == 1:
                                        number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                    
                                elif number_of_ticket is not None:
                                    self.updater(ctx,number_of_ticket)
                                    if len(number_of_ticket) == 1:
                                        number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                    elif len(number_of_ticket) == 2:
                                        number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                    elif len(number_of_ticket) == 3:
                                        number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                    else:
                                        number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                                
                                category_id = self.get_category(ctx)
                                category = discord.utils.get(ctx.guild.categories , id =category_id)
                                modals = discord.ui.Modal(title='Ticket Form')
                                title_ticket = discord.ui.TextInput(label='enter your title' , style=discord.TextStyle.short , required=True)
                                body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)
                                modals.add_item(title_ticket)
                                modals.add_item(body_ticket)
                                roles = self.get_admin(ctx)
                                av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
                                av_button.callback = close_button
                                button_view = CloseTicketAW(self.bot)
                                caller = ModalApplicationForm(ctx ,number_of_ticket ,overwrites , button_view)
                                await ctx.response.send_modal(caller)
                                
                                # av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red )
                                # av_button.callback = close_button
                                # button_view = discord.ui.View(timeout=None)
                                # button_view.add_item(av_button)
                                
                                # async def on_sumbit(self,ctx):
                                #     await ctx.defer()
                                #     if category is not None:
                                #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                                #     else:
                                #         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                                #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                                #         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                                #     embed.add_field(name='Ticket title:',value=f'{title_ticket}')
                                #     embed.add_field(name='Ticket Description' , value=f'{body_ticket}')

                                #     await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=button_view)
                                #     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
                                #         pass
                                #     else:
                                #         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True})
                                #     admins = []
                                #     if roles is not None:
                                #         for i in roles:
                                #             checker=discord.utils.get(guild.roles, id=i)
                                #             if checker is not None:
                                #                 await channel.set_permissions(checker , read_messages=True , send_messages=True)
                                #                 return
                            else:
                                await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)

                    ############################################################################################################
                    tmp_color = 0xFFFFFF
                    if embed_color.name =='white':
                        tmp_color = 0xFFFFFF
                    elif embed_color.name =='black':
                        tmp_color = 0x000000
                    elif embed_color.name =='purple':
                        tmp_color = 0x9C05FE
                    elif embed_color.name =='blue':
                        tmp_color = 0x0554FE
                    elif embed_color.name =='red':
                        tmp_color = 0xFE0505
                    elif embed_color.name =='pink':
                        tmp_color = 0xF568E8
                    elif embed_color.name=='yellow':
                        tmp_color = 0xE9F61A
                    elif embed_color.name=='green':
                        tmp_color = 0x26F915
                    checker = discord.utils.get(ctx.guild.text_channels , id=channel.id )
                    if checker is not None:
                        embed = discord.Embed(
                            title=f"{find['title']}",
                            description=f"{find['description']}",
                            timestamp=datetime.now(),
                            color=tmp_color
                        )
                        embed.set_footer(text='APA BOT Ticket System',icon_url='https://cdn.discordapp.com/attachments/1135103098805817477/1135105421644943400/giphy.gif')
                        button_name= find['button_name']
                        letters = string.ascii_lowercase
                        customer_id=''.join(random.choice(letters) for i in range(10))
                        av_button = discord.ui.Button(label =button_name , style=discord.ButtonStyle.green , custom_id='create_ticket' )
                        collection.update_one({"_id":ctx.guild.id},{"$set":{ "custom_id":customer_id , 'update':False}})
                        av_button.callback = button_callback
                        button_view111 = discord.ui.View(timeout=None)
                        button_view111.add_item(av_button)

                        msg=await checker.send(embed=embed , view= button_view111)
                        if (find5:=collection.find_one({'guild_checker':ctx.guild.id})):
                            collection.update_one({"guild_checker":ctx.guild.id} , {'$set':{'msg':msg.id,'channel':checker.id}})
                        else:
                            collection.insert_one({"guild_checker":ctx.guild.id , 'msg':msg.id , 'channel':checker.id})
                        await ctx.send(f"ticket form sent in {channel.mention}")
                        
                    else:
                        await ctx.followup.send('channel is not exist')
                        return
                elif style_checker == 2:
                    guild_check = ctx.guild.id
                    async def open_button_callback(ctx):
                        await ctx.response.defer()
                        if(find2:= collection.find_one({'guild_id':guild_check, "channel_id":ctx.channel_id , 'state':False})):
                            modal_roles=self.get_admin(ctx)
                            flager=False
                            if modal_roles is not None:
                                for i in ctx.user.roles:
                                    if i.id in modal_roles:
                                        flager=True
                            perm_checker= ctx.user.guild_permissions.administrator
                            if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                                flager=True
                            if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                                if find2['open_state'] == False:
                                    collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':True , 'close_state':False}})
                                    channel=find2['channel_id']
                                    member = find2['user_id']
                                    channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                                    member_checker=discord.utils.get(ctx.guild.members, id=member)
                                    permission_check = channel_temp.overwrites
                                    msg = find2['msg_id']
                                    for i in permission_check:
                                        if i.id == member:
                                            await asyncio.sleep(0.5)
                                            await channel_temp.set_permissions(member_checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                            async for messager in ctx.channel.history(limit=None):
                                                if messager.id == msg:
                                                    await messager.delete()
                                            self.open_button_updater(ctx)
                                else:
                                    pass
                            else:
                                await ctx.edit_original_response(content='you are not allowed to do this')

                        else:
                            await ctx.edit_original_response(content='you are not allowed to do this')

                    async def delete_button(ctx):
                        if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                            await ctx.response.defer()
                            modal_roles=self.get_admin(ctx)
                            flager=False
                            if modal_roles is not None:
                                for i in ctx.user.roles:
                                    if i.id in modal_roles:
                                        flager=True
                            perm_checker= ctx.user.guild_permissions.administrator
                            if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                                flager=True
                            if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                                channel=find2['channel_id']
                                channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                                self.delete_button_deleter(ctx)
                                await ctx.followup.send(f'ticket will be deleted in next 1 seconds')
                                await asyncio.sleep(1)
                                await channel_temp.delete()
                            else:
                                await ctx.edit_original_response(content='you are not allowed to do this')
                    async def close_button(ctx):
                        if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
                            modal_roles=self.get_admin(ctx)
                            flager=False
                            if modal_roles is not None:
                                for i in ctx.user.roles:
                                    if i.id in modal_roles:
                                        flager=True
                            perm_checker= ctx.user.guild_permissions.administrator
                            if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
                                flager=True
                            if find2['user_id']==ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
                                if find2['close_state'] == False:
                                    channel=find2['channel_id']
                                    member = find2['user_id']
                                    channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
                                    member_checker=discord.utils.get(ctx.guild.members, id=member)
                                    self.close_button_updater(ctx)
                                    ########## buttons section for support
                                    embed = self.support_embed()
                                    av_button = discord.ui.Button(label ='DELETE TICKET' , style=discord.ButtonStyle.red , custom_id='delete_ticket' )
                                    open_button = discord.ui.Button(label ='OPEN TICKET' , style=discord.ButtonStyle.green , custom_id='open_ticket' )

                                    av_button.callback = delete_button
                                    open_button.callback = open_button_callback

                                    button_view = discord.ui.View(timeout=None)
                                    button_view.add_item(av_button)
                                    button_view.add_item(open_button)

                                    collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':False , 'close_state':True}})
                                    if member_checker is not None:
                                        await channel_temp.set_permissions(member_checker , read_messages=False, attach_files=False , send_messages=False,read_message_history=False, send_voice_messages=False)
                                        await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                        msg= await ctx.followup.send(embed=embed , view=button_view)
                                        collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                                    else:
                                        await ctx.response.send_message(f'ticket closed' , ephemeral=True)
                                        msg= await ctx.followup.send(embed=embed , view=button_view)  
                                        collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
                                else:
                                    await ctx.response.send_message(f'you already closed ticket' , ephemeral=True)
                            else:
                                pass

                            
                    ########################button ticket create######################################
                    async def dropdown_callback(ctx):
                        if selector.values[0] == '88':
                            await ctx.response.defer()
                        else:
                            flager_category=False
                            id_getter = int(selector.values[0])
                            jj_id = collection.find_one({"ID":id_getter , "guild_ider":ctx.guild.id})
                            jj= discord.utils.get(ctx.guild.categories ,id=jj_id['category_id'])
                            if jj is not None:
                                flager_category=True

                            if(find5:= collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})):
                                for i in find5:
                                    channel_checker=i['channel_id']
                                    checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
                                    if checker is None:
                                        channel_id = i['channel_id']
                                        tmp_guild = i['guild_id']
                                        user_tmp = i['user_id']
                                        collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})
                                
                                false_checker=collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':False})
                                for i in false_checker:
                                    channel_checker=i['channel_id']
                                    checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
                                    if checker is None:
                                        channel_id = i['channel_id']
                                        tmp_guild = i['guild_id']
                                        user_tmp = i['user_id']
                                        collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})

                                if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                                    # await ctx.response.defer()
                                    guild = ctx.guild
                                    member = ctx.user
                                    overwrites = {
                                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                        member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True, send_voice_messages=True),
                                    }
                                    number_of_ticket = self.get_count(ctx)
                                    if number_of_ticket is None:
                                        number_of_ticket = '1'
                                        self.updater(ctx,number_of_ticket)
                                        if len( number_of_ticket) == 1:
                                            number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                        
                                    elif number_of_ticket is not None:
                                        self.updater(ctx,number_of_ticket)
                                        if len(number_of_ticket) == 1:
                                            number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                        elif len(number_of_ticket) == 2:
                                            number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                        elif len(number_of_ticket) == 3:
                                            number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                        else:
                                            number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                                    category_id = self.get_category(ctx)
                                    category = discord.utils.get(ctx.guild.categories , id =category_id)
                                    modals = discord.ui.Modal(title='Ticket Form')
                                    title_ticket = discord.ui.TextInput(label='enter your title' , style=discord.TextStyle.short , required=True)
                                    body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)
                                    modals.add_item(title_ticket)
                                    modals.add_item(body_ticket)
                                    roles = self.get_admin(ctx)
                                    av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
                                    av_button.callback = close_button
                                    button_view = CloseTicketAW(self.bot)
                                    caller = ModalApplicationForm1(ctx ,number_of_ticket ,overwrites , button_view , int(selector.values[0]))
                                    try:
                                        await ctx.response.send_modal(caller)
                                    except:
                                        pass
                                    

                                    
                                    # roles = self.get_admin(ctx)
                                    # av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red,custom_id='close_ticket' )
                                    # av_button.callback = close_button
                                    # button_view = discord.ui.View(timeout=None)
                                    # button_view.add_item(av_button)
                                    # embeder = self.create_embed(ctx)
                                    # if jj is not None:
                                    #     channel_sender=await ctx.guild.create_text_channel(number_of_ticket , overwrites=overwrites , category=jj)
                                    # else:
                                    #     channel_sender=await ctx.guild.create_text_channel(number_of_ticket , overwrites=overwrites )

                                    
                                    # admins = []
                                    # text_mention=''
                                    # menu_finder = collection.find({"guild_id":ctx.guild.id})
                                    # for i in menu_finder:
                                    #     if i['_id'] == jj:
                                    #         for j in i['admins_id']:
                                    #             j=int(j)
                                    #             roler_plus = discord.utils.get(ctx.guild.role , id = j)
                                    #             if roler_plus is not None:
                                    #                 admins.append(j)
                                    #                 text_mention+=f'<@{j}> '

                                    # await channel_sender.send(f'your ticket created {ctx.user.mention}\n{text_mention}' ,embed=embeder , view=button_view)

                                    # if len(admins)!=0 :
                                    #     for i in roles:
                                    #         checker=discord.utils.get(guild.roles, id=i)
                                    #         if checker is not None:
                                    #             await channel_sender.set_permissions(checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)

                                    
                                    # av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red )
                                    # av_button.callback = close_button
                                    # button_view = discord.ui.View(timeout=None)
                                    # button_view.add_item(av_button)
                                    
                                    # async def on_sumbit(self,ctx):
                                    #     await ctx.defer()
                                    #     if category is not None:
                                    #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                                    #     else:
                                    #         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                                    #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                                    #         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                                    #     embed.add_field(name='Ticket title:',value=f'{title_ticket}')
                                    #     embed.add_field(name='Ticket Description' , value=f'{body_ticket}')

                                    #     await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=button_view)
                                    #     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
                                    #         pass
                                    #     else:
                                    #         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True})
                                    #     admins = []
                                    #     if roles is not None:
                                    #         for i in roles:
                                    #             checker=discord.utils.get(guild.roles, id=i)
                                    #             if checker is not None:
                                    #                 await channel.set_permissions(checker , read_messages=True , send_messages=True)
                                    #                 return

                                    
                                else:
                                    await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)

                            else:
                                if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
                                    # await ctx.response.defer()
                                    guild = ctx.guild
                                    member = ctx.user
                                    overwrites = {
                                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                        member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                    }
                                    number_of_ticket = self.get_count(ctx)
                                    if number_of_ticket is None:
                                        number_of_ticket = '1'
                                        self.updater(ctx,number_of_ticket)
                                        if len( number_of_ticket) == 1:
                                            number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                        
                                    elif number_of_ticket is not None:
                                        self.updater(ctx,number_of_ticket)
                                        if len(number_of_ticket) == 1:
                                            number_of_ticket= '000'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                        elif len(number_of_ticket) == 2:
                                            number_of_ticket = '00'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                        elif len(number_of_ticket) == 3:
                                            number_of_ticket='0'+number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'
                                        else:
                                            number_of_ticket=number_of_ticket+'-ᴛɪᴄᴋᴇᴛ'

                                    
                                    category_id = self.get_category(ctx)
                                    category = discord.utils.get(ctx.guild.categories , id =category_id)
                                    modals = discord.ui.Modal(title='Ticket Form')
                                    title_ticket = discord.ui.TextInput(label='enter your title' , style=discord.TextStyle.short , required=True)
                                    body_ticket = discord.ui.TextInput(label='description' , style=discord.TextStyle.long, required=True)
                                    modals.add_item(title_ticket)
                                    modals.add_item(body_ticket)
                                    roles = self.get_admin(ctx)
                                    av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
                                    av_button.callback = close_button
                                    button_view = CloseTicketAW(self.bot)
                                    caller = ModalApplicationForm1(ctx ,number_of_ticket ,overwrites , button_view , int(selector.values[0]))
                                    try:
                                        await ctx.response.send_modal(caller)
                                    except:
                                        pass
                                    
                                    # av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red )
                                    # av_button.callback = close_button
                                    # button_view = discord.ui.View(timeout=None)
                                    # button_view.add_item(av_button)
                                    
                                    # async def on_sumbit(self,ctx):
                                    #     await ctx.defer()
                                    #     if category is not None:
                                    #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
                                    #     else:
                                    #         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
                                    #         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
                                    #         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

                                    #     embed.add_field(name='Ticket title:',value=f'{title_ticket}')
                                    #     embed.add_field(name='Ticket Description' , value=f'{body_ticket}')

                                    #     await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=button_view)
                                    #     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
                                    #         pass
                                    #     else:
                                    #         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True})
                                    #     admins = []
                                    #     if roles is not None:
                                    #         for i in roles:
                                    #             checker=discord.utils.get(guild.roles, id=i)
                                    #             if checker is not None:
                                    #                 await channel.set_permissions(checker , read_messages=True , send_messages=True)
                                    #                 return
                                else:
                                    await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)

                    ############################################################################################################
                    tmp_color = 0xFFFFFF
                    if embed_color.name =='white':
                        tmp_color = 0xFFFFFF
                    elif embed_color.name =='black':
                        tmp_color = 0x000000
                    elif embed_color.name =='purple':
                        tmp_color = 0x9C05FE
                    elif embed_color.name =='blue':
                        tmp_color = 0x0554FE
                    elif embed_color.name =='red':
                        tmp_color = 0xFE0505
                    elif embed_color.name =='pink':
                        tmp_color = 0xF568E8
                    elif embed_color.name=='yellow':
                        tmp_color = 0xE9F61A
                    elif embed_color.name=='green':
                        tmp_color = 0x26F915
                    checker = discord.utils.get(ctx.guild.text_channels , id=channel.id )
                    if checker is not None:
                        embed = discord.Embed(
                            title=f"{find['title']}",
                            description=f"{find['description']}",
                            timestamp=datetime.now(),
                            color=tmp_color
                        )
                        embed.set_footer(text='APA BOT Ticket System',icon_url='https://cdn.discordapp.com/attachments/1135103098805817477/1135105421644943400/giphy.gif')
                        button_name= find['button_name']
                        letters = string.ascii_lowercase
                        customer_id=''.join(random.choice(letters) for i in range(10))
                        options =[]
                        gathering_menu = collection.find({"guild_ider":ctx.guild.id})
                        for i in gathering_menu:
                            checker_plus = discord.utils.get(ctx.guild.categories , id = i['category_id'])
                            if checker_plus is not None:
                                options.append(discord.SelectOption(label=i['admins_name'] , value=i['ID'], emoji=f"{i['emojies']}"))
                        # options.append(discord.SelectOption(label=self.names_list[i] , value=self.last_ids_list[i], emoji=f'{self.new_emoji_list[i]}'))
                        if len(options) == 0:
                            return await ctx.send(f'none of your categories find try to add new and valid categories then send ticket form')

                        options.append(discord.SelectOption(label='remove selection' , value='88', emoji="⛔"))
                        selector = discord.ui.Select(placeholder=button_name , custom_id='create_ticket' , options=options)
                        if style_checker ==1:
                            collection.update_one({"_id":ctx.guild.id},{"$set":{ "custom_id":customer_id , 'update':False}})
                        elif style_checker ==2:
                            collection.update_one({"_id":ctx.guild.id},{"$set":{ "custom_id_menu":customer_id , 'update':False}})
                        selector.callback = dropdown_callback
                        button_view111 = discord.ui.View(timeout=None)
                        button_view111.add_item(selector)

                        msg=await checker.send(embed=embed , view= button_view111)
                        if (find5:=collection.find_one({'guild_checker':ctx.guild.id})):
                            collection.update_one({"guild_checker":ctx.guild.id} , {'$set':{'msg':msg.id,'channel':checker.id}})
                        else:
                            collection.insert_one({"guild_checker":ctx.guild.id , 'msg':msg.id , 'channel':checker.id})
                        await ctx.send(f"ticket form sent in {channel.mention}")
                        
                    else:
                        await ctx.followup.send('channel is not exist')
                        return
                else:
                    return await ctx.send('set ticket style first')                        

            else:
                await ctx.send('set ticket config first then set admins and in the end use this to send the ticket form')
        except Exception as e:
            await ctx.send('something went wrong pls try again')
#################################################################################################################################    
######################################################### updater class
# class updater_new():

#     def __init__(self , bot:Bot):
#         self.bot = bot
#         self.find = collection.find_one({'update':False})
#         if self.find is not None:
#             self.guild_id = self.find['_id']
#             self.button_name=self.find['button_name']
#             self.customer_id = self.find['custom_id']
#             # self.modal_custom_id = self.find['modal_id']
#             collection.update_one({"_id":self.guild_id},{"$set":{ "update":True}})
        
        
#         if self.find is None:
#             self.find1 = collection.find({'update':True})
#             if self.find1 is not None:
#                 for j in self.find1:
#                     self.guild_id = j['_id']
#                     collection.update_one({"_id":self.guild_id},{"$set":{ "update":False}})
#                     self.finder = collection.find_one({'update':False})
#                     if self.finder is None:
#                         pass

#         self.find_menu = collection.find({'is_active':False})
#         self.checker_menu1 = collection.find_one({'is_active':False})
#         print(self.checker_menu1)
#         if self.find_menu is not None:
#             self.options = []           
#             self.tmp_guild = []
#             self.place_name = ''
#             self.customerid_menu:str=None
#             for j in self.find_menu:
#                 try:
#                     self.tmp_guild.append(j['guild_ider'])
#                 except:
#                     pass
#             self.tmp_guild = set(self.tmp_guild)
#             self.tmp_guild = list(self.tmp_guild)
#             if len(self.tmp_guild) !=0:
#                 for i in range(1):
#                     self.find_menu12 = collection.find({'guild_ider':self.tmp_guild[i]})
#                     self.finder_place = collection.find_one({'_id':self.tmp_guild[i]})
#                     self.place_name = self.finder_place['button_name']
#                     self.customerid_menu = self.finder_place['custom_id_menu']
#                     print(self.customerid_menu)
#                     for jj in self.find_menu12:
#                         self.options.append(discord.SelectOption(label=jj['admins_name'] , value=jj['ID'], emoji=f"{jj['emojies']}"))
#                         collection.update_one({'_id':jj['_id'],'ID':jj['ID'] ,'guild_ider':jj['guild_ider'] , 'emojies':jj['emojies'] , 'admins_name':jj['admins_name'] ,'is_active':False} , {'$set':{'is_active':True}})

#                 self.options.append(discord.SelectOption(label='remove selection' , value='88', emoji="⛔"))
#                     # if j['_id'] in self.tmp_category:
#                     #     self.all_ids.append(j['_id'])
#                     #     self.options.append(discord.SelectOption(label=j['admins_name'] , value=j['_id'], emoji=f"{j['emojies']}"))
#                     #     collection.update_one({'_id':j['_id'] ,'guild_ider':j['guild_ider'] , 'emojies':j['emojies'] , 'admins_name':j['admins_name'] ,'is_active':False} , {'$set':{'is_active':True}})

#         self.find_menu1 = collection.find_one({'is_active':False})
#         if self.find_menu1 is None:
#             self.find_menu1 = collection.find({'is_active':True})
#             if self.find_menu1 is not None:
#                 for j in self.find_menu1:
#                     collection.update_one({'_id':j['_id'] ,'ID':j['ID'],'guild_ider':j['guild_ider'] , 'emojies':j['emojies'] , 'admins_name':j['admins_name'] ,'is_active':True} , {'$set':{'is_active':False}})


#     def get_count(self,ctx):
#         if(find:= collection.find_one({"_id":ctx.guild.id})):
#             counter=find['count']
#             return counter

#     def updater(self ,ctx ,  number_of_ticket):
#         number_of_ticket = int(number_of_ticket)
#         number_of_ticket+=1
#         number_of_ticket = str(number_of_ticket)
#         collection.update_one({"_id":ctx.guild.id},{"$set":{ "count":number_of_ticket}})

#     def support_embed(self ):
#         embed=discord.Embed(
#             title ='APA BOT',
#             description=f"Support Panel:",
#             color=None
#         )
#         return embed


#     def create_embed(self,ctx):
#         var = collection.find_one({"_id":ctx.guild.id})
#         message = var['embed_message']
#         embed=discord.Embed(
#             title ='APA BOT',
#             description=f"{message}",
#             color= 0xF6F6F6,
#             timestamp=datetime.now()
#         )
#         return embed
    
#     def close_button_updater(self,ctx):
#         collection.update_one({ 'guild_id':ctx.guild.id, "channel_id":ctx.channel_id},{"$set":{ "state":False}})
    
#     def open_button_updater(self,ctx):
#         collection.update_one({'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False},{"$set":{ "state":True}})

#     def delete_button_deleter(self,ctx):
#         collection.delete_one({ 'guild_id':ctx.guild.id , "channel_id":ctx.channel_id , 'state':False})

#     def get_category(self,ctx):
#         find=collection.find_one({"_id":ctx.guild.id})
#         category_id = find['category']
#         return category_id

#     def get_admin(self,ctx):
#         find=collection.find_one({"_id":ctx.guild.id})
#         admins = find['admins']
#         return admins

#     def get_title(self,ctx):
#         var = collection.find_one({"_id":ctx.guild.id})
#         title1 = var['form_title']
#         # caller = ModalApplicationForm
#         # caller.title = title1
#         return title1

#     def get_description(self,ctx):
#         var = collection.find_one({"_id":ctx.guild.id})
#         body = var['form_description']
#         # caller = ModalApplicationForm
#         # caller.title = title1
#         return body

# ###############################################open ticket        
#     async def open_button(self,ctx=None):
#         try:
#             if ctx is not None:
#                 await ctx.response.defer()
#                 guild_check = ctx.guild.id
#                 if(find2:= collection.find_one({'guild_id':guild_check, "channel_id":ctx.channel_id , 'state':False})):
#                     modal_roles=self.get_admin(ctx)
#                     flager=False
#                     if modal_roles is not None:
#                         for i in ctx.user.roles:
#                             if i.id in modal_roles:
#                                 flager=True
#                     perm_checker= ctx.user.guild_permissions.administrator
#                     if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
#                         flager=True
#                     if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
#                         if find2['open_state'] == False:
#                             collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':True , 'close_state':False}})
#                             channel=find2['channel_id']
#                             member = find2['user_id']
#                             channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
#                             member_checker=discord.utils.get(ctx.guild.members, id=member)
#                             permission_check = channel_temp.overwrites
#                             msg = find2['msg_id']
#                             for i in permission_check:
#                                 if i.id == member:
#                                     await asyncio.sleep(0.5)
#                                     await channel_temp.set_permissions(member_checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
#                                     try:
#                                         async for messager in channel_temp.history(limit=None):
#                                             if messager.id == msg:
#                                                 await messager.delete()
#                                     except:
#                                         await ctx.edit_original_response(content='Ticket is open now')
#                                     self.open_button_updater(ctx)
#                         else:
#                             pass
#                     else:
#                         await ctx.edit_original_response(content='you are not allowed to do this')

#         except:
#             pass



# #################################################create ticket
#     async def create_ticket(self,ctx=None):
#         try:
#             if ctx is not None:
#                 guild_check = ctx.guild.id
#                 if(find:= collection.find_one({"_id":ctx.guild.id})):
#                     style_checker = find['style']
#                     if(find5:= collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})):
#                         for i in find5:
#                             channel_checker=i['channel_id']
#                             checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
#                             if checker is None:
#                                 channel_id = i['channel_id']
#                                 tmp_guild = i['guild_id']
#                                 user_tmp = i['user_id']
#                                 collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})
                        
#                         false_checker=collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':False})
#                         for i in false_checker:
#                             channel_checker=i['channel_id']
#                             checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
#                             if checker is None:
#                                 channel_id = i['channel_id']
#                                 tmp_guild = i['guild_id']
#                                 user_tmp = i['user_id']
#                                 collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})

#                         if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
#                             # await ctx.response.defer()
#                             guild = ctx.guild
#                             member = ctx.user
#                             overwrites = {
#                                 guild.default_role: discord.PermissionOverwrite(read_messages=False),
#                                 member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True),
#                             }
#                             number_of_ticket = self.get_count(ctx)
#                             if number_of_ticket is None:
#                                 number_of_ticket = '1'
#                                 self.updater(ctx,number_of_ticket)
#                                 if len( number_of_ticket) == 1:
#                                     number_of_ticket= '000'+number_of_ticket+'-Ticket'
                                
#                             elif number_of_ticket is not None:
#                                 self.updater(ctx,number_of_ticket)
#                                 if len(number_of_ticket) == 1:
#                                     number_of_ticket= '000'+number_of_ticket+'-Ticket'
#                                 elif len(number_of_ticket) == 2:
#                                     number_of_ticket = '00'+number_of_ticket+'-Ticket'
#                                 elif len(number_of_ticket) == 3:
#                                     number_of_ticket='0'+number_of_ticket+'-Ticket'
#                                 else:
#                                     number_of_ticket=number_of_ticket+'-Ticket'

#                             av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red , custom_id='close_ticket' )
#                             av_button.callback = self.close_button
#                             button_view = discord.ui.View(timeout=None)
#                             button_view.add_item(av_button)
#                             category_id = self.get_category(ctx)
#                             category = discord.utils.get(ctx.guild.categories , id =category_id)
#                             roles = self.get_admin(ctx)
#                             embeder=self.create_embed(ctx)
#                             modal_category = self.get_category(ctx)
#                             modal_roles=self.get_admin(ctx)

#                             async def on_sumbit(ctx):
#                                 if style_checker ==1:
#                                     form_title = find['form_title']
#                                     form_description= find['form_description']
#                                     embed = embeder
#                                     category_id = modal_category
#                                     category = discord.utils.get(ctx.guild.categories , id =category_id)
#                                     roles = modal_roles
#                                     await ctx.response.defer()
#                                     if category is not None:
#                                         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
#                                     else:
#                                         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
#                                         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
#                                         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')
                                    
#                                     embed.add_field(name=form_title,value=f'{title_ticket}')
#                                     embed.add_field(name=form_description , value=f'{body_ticket}')

#                                     await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=button_view)
#                                     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
#                                         pass
#                                     else:
#                                         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
#                                     admins = []
#                                     if roles is not None:
#                                         for i in roles:
#                                             checker=discord.utils.get(guild.roles, id=i)
#                                             if checker is not None:
#                                                 await channel.set_permissions(checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
#                                                 return
#                                 else:
#                                     await ctx.response.send_message('the ticket style changed by admins but they didnt send new form')
                        
#                             modals = discord.ui.Modal(title='Ticket System Form')
#                             title_modal = self.get_title(ctx)
#                             body_modal = self.get_description(ctx)
#                             title_ticket = discord.ui.TextInput(label=title_modal , style=discord.TextStyle.short , required=True)
#                             body_ticket = discord.ui.TextInput(label=body_modal , style=discord.TextStyle.long, required=True)
#                             modals.add_item(title_ticket)
#                             modals.add_item(body_ticket)
#                             modals.on_submit=on_sumbit
#                             await ctx.response.send_modal(modals)
                            
                            

                            
#                         else:
#                             await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)

#                     else:
#                         if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
#                             # await ctx.response.defer()
#                             guild = ctx.guild
#                             member = ctx.user
#                             overwrites = {
#                                 guild.default_role: discord.PermissionOverwrite(read_messages=False),
#                                 member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True),
#                             }
#                             number_of_ticket = self.get_count(ctx)
#                             if number_of_ticket is None:
#                                 number_of_ticket = '1'
#                                 self.updater(ctx,number_of_ticket)
#                                 if len( number_of_ticket) == 1:
#                                     number_of_ticket= '000'+number_of_ticket+'-Ticket'
                                
#                             elif number_of_ticket is not None:
#                                 self.updater(ctx,number_of_ticket)
#                                 if len(number_of_ticket) == 1:
#                                     number_of_ticket= '000'+number_of_ticket+'-Ticket'
#                                 elif len(number_of_ticket) == 2:
#                                     number_of_ticket = '00'+number_of_ticket+'-Ticket'
#                                 elif len(number_of_ticket) == 3:
#                                     number_of_ticket='0'+number_of_ticket+'-Ticket'
#                                 else:
#                                     number_of_ticket=number_of_ticket+'-Ticket'

#                             av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
#                             av_button.callback = self.close_button
#                             button_view = discord.ui.View(timeout=None)
#                             button_view.add_item(av_button)
#                             category_id = self.get_category(ctx)
#                             category = discord.utils.get(ctx.guild.categories , id =category_id)
#                             roles = self.get_admin(ctx)
#                             embeder=self.create_embed(ctx)
#                             modal_category = self.get_category(ctx)
#                             modal_roles=self.get_admin(ctx)
                            
#                             async def on_sumbit(ctx):
#                                 if style_checker == 1:
#                                     embed = embeder
#                                     category_id = modal_category
#                                     category = discord.utils.get(ctx.guild.categories , id =category_id)
#                                     roles = modal_roles
#                                     await ctx.response.defer()
#                                     if category is not None:
#                                         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
#                                     else:
#                                         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
#                                         channel = await guild.create_text_channel(number_of_ticket, overwrites=overwrites)
#                                         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')
                                    
#                                     embed.add_field(name='Ticket title:',value=f'{title_ticket}')
#                                     embed.add_field(name='Ticket Description' , value=f'{body_ticket}')

#                                     await channel.send(f'your ticket created {ctx.user.mention}',embed=embed , view=button_view)
#                                     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check, "state":True})):
#                                         pass
#                                     else:
#                                         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
#                                     admins = []
#                                     if roles is not None:
#                                         for i in roles:
#                                             checker=discord.utils.get(guild.roles, id=i)
#                                             if checker is not None:
#                                                 await channel.set_permissions(checker , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
#                                                 return
#                                 else:
#                                     await ctx.response.send_message('the ticket style changed by admins but they didnt send new form')
#                                 modals = discord.ui.Modal(title='Ticket System Form')
#                                 title_modal = self.get_title(ctx)
#                                 body_modal = self.get_description(ctx)
#                                 title_ticket = discord.ui.TextInput(label=title_modal , style=discord.TextStyle.short , required=True)
#                                 body_ticket = discord.ui.TextInput(label=body_modal , style=discord.TextStyle.long, required=True)
#                                 modals.add_item(title_ticket)
#                                 modals.add_item(body_ticket)
#                                 modals.on_submit=on_sumbit
#                                 await ctx.response.send_modal(modals)
                        
#         except:
#             pass
#                     ########################button ticket create######################################
#     async def dropdown_callback(self,ctx=None):
#         print ('1')
#         if ctx is not None:
#     # selector = discord.ui.Select(placeholder=self.button_name , custom_id=self.customer_id , options=self.options)
#     # selector.callback = dropdown_callback
#             print(selector.values)
#             if selector.values[0] == '88':
#                 await ctx.response.defer()
#             else:
#                 guild_check = ctx.guild.id
#                 flager_category=False
#                 if(find:= collection.find_one({"_id":ctx.guild.id})):
#                     style_checker = find['style']
#                     id_getter = int(selector.values[0])
#                     jj_id = collection.find_one({"ID":id_getter , "guild_ider":ctx.guild.id})
#                     department = jj_id['admins_name']
#                     jj= discord.utils.get(ctx.guild.categories ,id=jj_id['category_id'])
#                     if jj is not None:
#                         flager_category=True

#                     if(find5:= collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})):
#                         for i in find5:
#                             channel_checker=i['channel_id']
#                             checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
#                             if checker is None:
#                                 channel_id = i['channel_id']
#                                 tmp_guild = i['guild_id']
#                                 user_tmp = i['user_id']
#                                 collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})
                        
#                         false_checker=collection.find({"user_id":ctx.user.id, "guild_id":guild_check , 'state':False})
#                         for i in false_checker:
#                             channel_checker=i['channel_id']
#                             checker = discord.utils.get(ctx.guild.text_channels , id=channel_checker )
#                             if checker is None:
#                                 channel_id = i['channel_id']
#                                 tmp_guild = i['guild_id']
#                                 user_tmp = i['user_id']
#                                 collection.delete_one({"user_id":user_tmp , "guild_id":tmp_guild , "channel_id":channel_id})

#                         if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
#                             # await ctx.response.defer()
#                             guild = ctx.guild
#                             member = ctx.user
#                             overwrites = {
#                                 guild.default_role: discord.PermissionOverwrite(read_messages=False),
#                                 member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True, send_voice_messages=True),
#                             }
#                             number_of_ticket = self.get_count(ctx)
#                             if number_of_ticket is None:
#                                 number_of_ticket = '1'
#                                 self.updater(ctx,number_of_ticket)
#                                 if len( number_of_ticket) == 1:
#                                     number_of_ticket= '000'+number_of_ticket+'-Ticket'
                                
#                             elif number_of_ticket is not None:
#                                 self.updater(ctx,number_of_ticket)
#                                 if len(number_of_ticket) == 1:
#                                     number_of_ticket= '000'+number_of_ticket+'-Ticket'
#                                 elif len(number_of_ticket) == 2:
#                                     number_of_ticket = '00'+number_of_ticket+'-Ticket'
#                                 elif len(number_of_ticket) == 3:
#                                     number_of_ticket='0'+number_of_ticket+'-Ticket'
#                                 else:
#                                     number_of_ticket=number_of_ticket+'-Ticket'
#                             embeder=self.create_embed(ctx)
#                             av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
#                             av_button.callback = self.close_button
#                             button_view85 = discord.ui.View(timeout=None)
#                             button_view85.add_item(av_button)
#                             category_id = self.get_category(ctx)
#                             category = discord.utils.get(ctx.guild.categories , id =category_id)
#                             roles = self.get_admin(ctx)
#                             modal_category = self.get_category(ctx)
#                             modal_roles=self.get_admin(ctx)

#                             async def on_sumbit11(ctx=None):
#                                 if ctx is not None:
#                                     if style_checker == 2:
#                                         form_title = find['form_title']
#                                         form_description= find['form_description']
#                                         await ctx.response.defer()
#                                         caller =TicketSystem(Bot)
#                                         category = discord.utils.get(ctx.guild.categories , id =jj.id)
#                                         category_menu = discord.utils.get(ctx.guild.categories , id =jj.id)
#                                         embed = caller.create_embed(ctx)
                                        
                                        
#                                         if category is not None:
#                                             channel = await ctx.guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
#                                         else:
#                                             owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
#                                             await asyncio.sleep(0.5)
#                                             channel = await ctx.guild.create_text_channel(number_of_ticket, overwrites=overwrites)
#                                             await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

#                                         embed.add_field(name=f"Department: ",value=f'{department}')
#                                         embed.add_field(name=f"{form_title}:",value=f'{title_ticket}')
#                                         embed.add_field(name=f"{form_description}:" , value=f'{body_ticket}' , inline=False)
                                        
                                        
#                                         if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":ctx.guild.id, "state":True})):
#                                             pass
#                                         else:
#                                             collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
#                                         admins = []
#                                         text_mention=''
#                                         menu_finder = collection.find({'ID':int(selector.values[0]),"guild_ider":ctx.guild.id})
#                                         for i in menu_finder:
#                                             if i['category_id'] == jj.id:
#                                                 tmp_list = i['admins_id']
#                                                 for j in tmp_list:
#                                                     j=int(j)
#                                                     roler_plus = discord.utils.get(ctx.guild.roles , id = j)
#                                                     if roler_plus is not None:
#                                                         admins.append(j)
#                                                         text_mention+=f'<@&{j}> '
#                                                         await channel.set_permissions(roler_plus , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)
                                    
#                                         await channel.send(f'your ticket created {ctx.user.mention}\n{text_mention}',embed=embed , view=button_view85)
#                                         try:
#                                             user_dm = discord.utils.get(ctx.guild.members , id=ctx.user.id)
#                                             await user_dm.send('something went wrong to create ticket for you pls try again')
#                                         except:
#                                             pass
#                                     else:
#                                         await ctx.response.send_message(f'the ticket style changed by admins but they didnt send new form' , ephemeral=True)

#                             modals11 = discord.ui.Modal(title='Ticket System Form')
#                             title_modal = self.get_title(ctx)
#                             body_modal = self.get_description(ctx)
#                             title_ticket = discord.ui.TextInput(label=title_modal , style=discord.TextStyle.short , required=True)
#                             body_ticket = discord.ui.TextInput(label=body_modal , style=discord.TextStyle.long, required=True)
#                             modals11.add_item(title_ticket)
#                             modals11.add_item(body_ticket)
#                             modals11.on_submit=on_sumbit11
#                             await ctx.response.send_modal(modals11)                                                                        
#                         else:
#                             await ctx.response.send_message(f'you already have a ticket' , ephemeral=True)


#                     else:
#                         if(find2:= collection.find_one({"user_id":ctx.user.id, "guild_id":guild_check , 'state':True})) is None:
#                             # await ctx.response.defer()
#                             guild = ctx.guild
#                             member = ctx.user
#                             overwrites = {
#                                 guild.default_role: discord.PermissionOverwrite(read_messages=False),
#                                 member: discord.PermissionOverwrite(read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True),
#                             }
#                             number_of_ticket = self.get_count(ctx)
#                             if number_of_ticket is None:
#                                 number_of_ticket = '1'
#                                 self.updater(ctx,number_of_ticket)
#                                 if len( number_of_ticket) == 1:
#                                     number_of_ticket= '000'+number_of_ticket+'-Ticket'
                                
#                             elif number_of_ticket is not None:
#                                 self.updater(ctx,number_of_ticket)
#                                 if len(number_of_ticket) == 1:
#                                     number_of_ticket= '000'+number_of_ticket+'-Ticket'
#                                 elif len(number_of_ticket) == 2:
#                                     number_of_ticket = '00'+number_of_ticket+'-Ticket'
#                                 elif len(number_of_ticket) == 3:
#                                     number_of_ticket='0'+number_of_ticket+'-Ticket'
#                                 else:
#                                     number_of_ticket=number_of_ticket+'-Ticket'

#                             av_button = discord.ui.Button(label ='Close Ticket' , style=discord.ButtonStyle.red ,custom_id='close_ticket')
#                             av_button.callback = self.close_button
#                             button_view = discord.ui.View(timeout=None)
#                             button_view.add_item(av_button)
#                             category_id = self.get_category(ctx)
#                             category = discord.utils.get(ctx.guild.categories , id =category_id)
#                             roles = self.get_admin(ctx)
#                             embeder=self.create_embed(ctx)
#                             modal_category = self.get_category(ctx)
#                             modal_roles=self.get_admin(ctx)
                            
#                             async def on_sumbit(ctx):
#                                 if style_checker == 2:
#                                     form_title = find['form_title']
#                                     form_description= find['form_description']
#                                     embed = embeder
#                                     await ctx.response.defer()
#                                     caller =TicketSystem(Bot)
#                                     category = discord.utils.get(ctx.guild.categories , id =jj.id)
#                                     category_menu = discord.utils.get(ctx.guild.categories , id =jj.id)
#                                     embed = caller.create_embed(ctx)
                                    
                                    
#                                     if category is not None:
#                                         channel = await ctx.guild.create_text_channel(number_of_ticket, overwrites=overwrites , category=category)
#                                     else:
#                                         owner = discord.utils.get(ctx.guild.members , id=ctx.guild.owner_id)
#                                         await asyncio.sleep(0.5)
#                                         channel = await ctx.guild.create_text_channel(number_of_ticket, overwrites=overwrites)
#                                         await owner.send(f'Hello\nTicket Alert:\nYour ticket category is not exist anymore try to config it again\ni will create new tickets without category untill you fix the config')

#                                     embed.add_field(name=f"Department: ",value=f'{department}')
#                                     embed.add_field(name=f"{form_title}:",value=f'{title_ticket}')
#                                     embed.add_field(name=f"{form_description}:" , value=f'{body_ticket}' , inline=False)
                                    
                                    
#                                     if(find1:= collection.find_one({"user_id":ctx.user.id, "guild_id":ctx.guild.id, "state":True})):
#                                         pass
#                                     else:
#                                         collection.insert_one({"user_id":ctx.user.id , "channel_id":channel.id , "guild_id":ctx.guild_id , "state":True , 'open_state':False , 'close_state':False})
#                                     admins = []
#                                     text_mention=''
#                                     menu_finder = collection.find({'ID':int(selector.values[0]),"guild_ider":ctx.guild.id})
#                                     for i in menu_finder:
#                                         if i['category_id'] == jj.id:
#                                             tmp_list = i['admins_id']
#                                             for j in tmp_list:
#                                                 j=int(j)
#                                                 roler_plus = discord.utils.get(ctx.guild.roles , id = j)
#                                                 if roler_plus is not None:
#                                                     admins.append(j)
#                                                     text_mention+=f'<@&{j}> '
#                                                     await channel.set_permissions(roler_plus , read_messages=True , send_messages=True,read_message_history=True,attach_files=True , send_voice_messages=True)

#                                     await channel.send(f'your ticket created {ctx.user.mention}\n{text_mention}',embed=embed , view=button_view85)
#                                     try:
                                        # user_dm = discord.utils.get(ctx.guild.members , id=ctx.user.id)
                                        # await user_dm.send('something went wrong to create ticket for you pls try again')
#                                     except:
#                                         pass
#                                 else:
#                                     await ctx.response.send_message(f'the ticket style changed by admins but they didnt send new form' , ephemeral=True)
                        
#                             modals1 = discord.ui.Modal(title='Ticket System Form')
#                             title_modal = self.get_title(ctx)
#                             body_modal = self.get_description(ctx)
#                             title_ticket = discord.ui.TextInput(label=title_modal , style=discord.TextStyle.short , required=True)
#                             body_ticket = discord.ui.TextInput(label=body_modal , style=discord.TextStyle.long, required=True)
#                             modals1.add_item(title_ticket)
#                             modals1.add_item(body_ticket)
#                             modals1.on_submit=on_sumbit
#                             await ctx.response.send_modal(modals1)                                                                        


# #########################################close button

#     async def close_button(self,ctx=None):
#         try:
#             if ctx is not None:
#                 guild_check = ctx.guild.id
#                 if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
#                     modal_roles=self.get_admin(ctx)
#                     flager=False
#                     if modal_roles is not None:
#                         for i in ctx.user.roles:
#                             if i.id in modal_roles:
#                                 flager=True
#                     perm_checker= ctx.user.guild_permissions.administrator
#                     if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
#                         flager=True
#                     if find2['user_id']==ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
#                         if find2['close_state']==False:
#                             channel=find2['channel_id']
#                             member = find2['user_id']
#                             channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
#                             member_checker=discord.utils.get(ctx.guild.members, id=member)
#                             self.close_button_updater(ctx)
#                             ########## buttons section for support
#                             embed = self.support_embed()
#                             av_button = discord.ui.Button(label ='DELETE TICKET' , style=discord.ButtonStyle.red , custom_id='delete_ticket' )
#                             open_button = discord.ui.Button(label ='OPEN TICKET' , style=discord.ButtonStyle.green , custom_id='open_ticket' )

#                             av_button.callback = self.delete_button
#                             open_button.callback = self.open_button
#                             collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'open_state':False , 'close_state':True}})

#                             button_view = discord.ui.View(timeout=None)
#                             button_view.add_item(av_button)
#                             button_view.add_item(open_button)

#                             # button_view = discord.ui.View(timeout=None)
                            
#                             if member_checker is not None:
#                                 await channel_temp.set_permissions(member_checker , read_messages=False , send_messages=False,read_message_history=False,attach_files=False , send_voice_messages=False)
#                                 await ctx.response.send_message(f'ticket closed' , ephemeral=True)
#                                 msg= await ctx.followup.send(embed=embed , view=button_view)
#                                 collection.update_one({ "guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
#                             else:
#                                 await ctx.response.send_message(f'ticket closed' , ephemeral=True)
#                                 msg= await ctx.followup.send(embed=embed , view=button_view)
#                                 collection.update_one({"guild_id":guild_check, "channel_id":ctx.channel_id} , {'$set':{'msg_id':msg.id}})
#                         else:
#                             await ctx.response.send_message(f'you already closed ticket' , ephemeral=True)

#                     else:
#                         await ctx.edit_original_response(content='you are not allowed to do this')

#         except:
#             pass

# ############################################delete ticket

#     async def delete_button(self,ctx=None):
#         try:
#             if ctx is not None:
#                 await ctx.response.defer()
#                 guild_check = ctx.guild.id
#                 if(find2:= collection.find_one({'guild_id':guild_check , "channel_id":ctx.channel_id})):
#                     modal_roles=self.get_admin(ctx)
#                     flager=False
#                     if modal_roles is not None:
#                         for i in ctx.user.roles:
#                             if i.id in modal_roles:
#                                 flager=True
#                     perm_checker= ctx.user.guild_permissions.administrator
#                     if ctx.guild.me.top_role.position < ctx.user.top_role.position and perm_checker == True:
#                         flager=True
#                     if find2['user_id']!=ctx.user.id or flager==True or ctx.user.id==ctx.user.guild.owner_id:
#                         channel=find2['channel_id']
#                         channel_temp = discord.utils.get(ctx.guild.text_channels , id=channel)
#                         self.delete_button_deleter(ctx)
#                         await ctx.followup.send(f'ticket will be deleted in next 1 seconds')
#                         await asyncio.sleep(1)
#                         await channel_temp.delete()
#                     else:
#                         await ctx.edit_original_response(content='you are not allowed to do this')

#         except:
#             pass





#     def view(self):
#         try:
#             if self.find is not None:
#                 button_create = discord.ui.Button(label=self.button_name, emoji='🔽' , style=discord.ButtonStyle.green , custom_id=self.customer_id)
#                 button_create.callback=self.create_ticket
#                 button_close = discord.ui.Button(label='Close Ticket' , style=discord.ButtonStyle.red , custom_id='close_ticket')
#                 button_close.callback=self.close_button
#                 button_delete = discord.ui.Button(label='DELETE TICKET' , style=discord.ButtonStyle.red , custom_id='delete_ticket')
#                 button_delete.callback=self.delete_button
#                 button_open = discord.ui.Button(label='OPEN TICKET', style=discord.ButtonStyle.green , custom_id='open_ticket')
#                 button_open.callback=self.open_button
#                 viewer = discord.ui.View(timeout=None)
#                 viewer.add_item(button_create)
#                 viewer.add_item(button_close)
#                 viewer.add_item(button_delete)
#                 viewer.add_item(button_open)
#                 return viewer
#             else:
#                 return None
#         except:
#             pass

    
#     def menu_view(self):
#         if self.customerid_menu is not None:
#             print('2')
#             global selector
#             print (self.options)
#             selector = discord.ui.Select(placeholder=self.place_name , custom_id=self.customerid_menu , options=self.options)
#             selector.callback = self.dropdown_callback
#             button_view = discord.ui.View(timeout=None)
#             button_view.add_item(selector)
#             return button_view
            









############################################################################################

async def setup(bot : Bot):
    await bot.add_cog(TicketSystem(bot))
