from __future__ import annotations
from gc import collect

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
import demoji
import json
import asyncio
import random
import string


cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["selectrole"]

class selectmenu(discord.ui.Select):
    def __init__(self , inter):
        self.interaction = inter
        if inter is not None:
            self.find = collection.find({'guild_id':self.interaction.guild_id , 'user_id':self.interaction.user.id , 'is_active':False})
        else:
            self.find = collection.find({})
        self.last_ids_list =None
        self.new_emoji_list = None
        self.names_list = None
        self.placeholder1 = None
        if self.find is not None:
            for j in self.find:
                self.last_ids_list = j['role_ids']
                self.new_emoji_list = j['emoji_list']
                self.names_list = j['name_list']
                self.placeholder1 = j['placeholder']
                self.customer_id = j['custom_id']        
                if len(self.last_ids_list)== len(self.names_list) and len(self.last_ids_list) == len(self.new_emoji_list):
                    options = []
                    for i in range(len(self.last_ids_list)):
                        options.append(discord.SelectOption(label=self.names_list[i] , value=self.last_ids_list[i], emoji=f'{self.new_emoji_list[i]}'))
                
                max_counter = len(options)
                super().__init__(placeholder=self.placeholder1 , options=options , custom_id=self.customer_id , min_values=1 , max_values=max_counter )

                if inter is not None:
                    collection.update_one({'guild_id':self.interaction.guild_id , 'user_id':self.interaction.user.id , 'is_active':False} , {'$set':{'is_active':True , 'min_value':1 ,'max_value':max_counter }})

    async def callback(self , interact:discord.Interaction):
        await interact.response.defer(thinking=True , ephemeral=True)
        add_names= ''
        counter_add = 0
        counter_remove=0
        remove_names=''
        counter_not_found:int=0
        for i in range(len(self.values)):
            jj= discord.utils.get(interact.guild.roles ,id=int(self.values[i]))

            if jj is not None:
                if jj not in interact.user.roles:
                    await interact.user.add_roles(jj)
                    counter_add +=1
                    if counter_add > 1:
                        add_names += f',{jj.name}'
                    else:
                        add_names += f'{jj.name}'
                else:
                    await interact.user.remove_roles(jj) 
                    counter_remove +=1
                    if counter_remove > 1:
                        remove_names += f',{jj.name}'
                    else:
                        remove_names += f'{jj.name}'
            else:
                counter_not_found +=1
        
        await interact.edit_original_response(content=f'added roles: {add_names}\nremoved roles: {remove_names} \nnot found roles: {counter_not_found}' )

def update_false():
    ...

async def updater(interaction=None):
    
    async def callback(interact:discord.Interaction):
        await interact.response.defer(thinking=True , ephemeral=True)
        add_names= ''
        counter_add = 0
        counter_remove=0
        remove_names=''
        counter_not_found:int=0
        for i in range(len(generate.values)):
            jj= discord.utils.get(interact.guild.roles ,id=int(generate.values[i]))

            if jj is not None:
                if jj not in interact.user.roles:
                    await interact.user.add_roles(jj)
                    counter_add +=1
                    if counter_add > 1:
                        add_names += f',{jj.name}'
                    else:
                        add_names += f'{jj.name}'
                else:
                    await interact.user.remove_roles(jj) 
                    counter_remove +=1
                    if counter_remove > 1:
                        remove_names += f',{jj.name}'
                    else:
                        remove_names += f'{jj.name}'
            else:
                counter_not_found +=1
        
        await interact.edit_original_response(content=f'added roles: {add_names}\nremoved roles: {remove_names} \nnot found roles: {counter_not_found}' )
    

    find = collection.find_one({'update':False})
    if find is not None:
        last_ids_list =None
        new_emoji_list = None
        names_list = None
        placeholder1 = None
        last_ids_list = find['role_ids']
        new_emoji_list = find['emoji_list']
        names_list = find['name_list']
        placeholder1 = find['placeholder']
        customer_id = find['custom_id']  
        miner_value = find['min_value']
        maxer_value = find['max_value']      
        if len(last_ids_list)== len(names_list) and len(last_ids_list) == len(new_emoji_list):
            options = []
            for i in range(len(last_ids_list)):
                options.append(discord.SelectOption(label=names_list[i] , value=last_ids_list[i], emoji=f'{new_emoji_list[i]}'))
        
        if miner_value is not None and maxer_value is not None:
            generate = discord.ui.Select(options=options , custom_id=customer_id , placeholder=placeholder1 , min_values=miner_value , max_values=maxer_value)
        else:
            generate = discord.ui.Select(options=options , custom_id=customer_id , placeholder=placeholder1)
        generate.callback=callback
        select_view = discord.ui.View(timeout=None )
        select_view.add_item(generate)
        collection.update_one({'role_ids':last_ids_list ,'emoji_list':new_emoji_list , 'name_list':names_list , 'placeholder':placeholder1 , 'custom_id':customer_id} , {"$set":{"update":True}})        
        return select_view
    else:
        find = collection.find({})
        for j in find:
            last_ids_list = j['role_ids']
            new_emoji_list = j['emoji_list']
            names_list = j['name_list']
            placeholder1 = j['placeholder']
            customer_id = j['custom_id']
            collection.update_one({'role_ids':last_ids_list ,'emoji_list':new_emoji_list , 'name_list':names_list , 'placeholder':placeholder1 , 'custom_id':customer_id} , {"$set":{"update":False}})
        return None        




class DropDownView(discord.ui.View ):
    def __init__(self , interaction=None ):
        self.interaction = interaction
        self.selectmenu1 = selectmenu(self.interaction)
        super().__init__(timeout=None)
        self.add_item(self.selectmenu1)           
        # self.add_item(self.selectmenu1)

     


class SelectRoles(Plugin):
    def __init__(self , bot:Bot):
        self.bot = bot

    async def cog_load(self):
        await super().cog_load()
        counter = collection.count_documents(filter={'is_active':True})
        for i in range(counter+1):
            instancer =await updater()
            if instancer is not None:
                self.bot.add_view(instancer)
            else:
                return

        
    @app_commands.command(
        name='selectrole',
        description='generate select role menus'
    )
    @app_commands.choices(color=[
        app_commands.Choice(name='white' , value=1),
        app_commands.Choice(name='black' , value=2),
        app_commands.Choice(name='purple' , value=3),
        app_commands.Choice(name='blue' , value=4),
        app_commands.Choice(name='red' , value=5),
        app_commands.Choice(name='pink' , value=6),
        app_commands.Choice(name='yellow' , value=7),
        app_commands.Choice(name='green' , value=8)

    ])
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.describe(
        title='title of embed',
        description='description of embed , use /n for going to new line exp: hello/nare you good?',
        names='seprate names with , exp: item1,item2,item3',
        role_ids = 'use role ids without space and seprate with , exp : 1119555882953620190,1119755849921249390',
        emoji1='use emojies without space and seprate with , exp: 👶,👼'
    )
    async def selectrole(self,interaction:discord.Interaction,*,title:str,description:str ,placeholder:str ,names:str , role_ids:str , emoji1:str , channel_send:discord.TextChannel,color:app_commands.Choice[int]):
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this command' , ephemeral=True)
        try:
            checker_channel = discord.utils.get(interaction.guild.channels , id = channel_send.id)
            if checker_channel is None:
                await interaction.response.send_message('the channel is not exist')
                return
            tmp_color = 0xFFFFFF
            if color.value ==1:
                tmp_color = 0xFFFFFF
            elif color.value ==2:
                tmp_color = 0x000000
            elif color.value ==3:
                tmp_color = 0x9C05FE
            elif color.value ==4:
                tmp_color = 0x0554FE
            elif color.value ==5:
                tmp_color = 0xFE0505
            elif color.value ==6:
                tmp_color = 0xF568E8
            elif color.value ==7:
                tmp_color = 0xE9F61A
            elif color.value ==8:
                tmp_color = 0x26F915
            
            count=len(emoji1)-1
            emoji_list = list(emoji1.split(','))
            new_emoji_list = []
            for i in emoji_list:
                i = i.replace("'" , "")
                i = i.replace(' ','')
                new_emoji_list.append(i)
            # emoji1 = emoji1.replace("'" , "")
            if len(title)>60:
                await interaction.response.send_message('use maximum 60 characters for title' ,ephemeral=True)
                return
            
            if len(description)>900:
                await interaction.response.send_message('use maximum 900 characters for description' ,ephemeral=True)
                return
            if len(placeholder) > 30:
                await interaction.response.send_message('use maximum 30 chracters for placeholder' ,ephemeral=True)
                return
            final_text:str=''
            message_spliter = list(description.split('/n'))
            for i in range(len(message_spliter)):
                if i != len(message_spliter)-1:
                    final_text += f'{message_spliter[i]}\n'
                else:
                    final_text += f'{message_spliter[i]}'
            names_list  = list(names.split(','))
            ids_list = list(role_ids.split(','))
            if len(ids_list) >30 or len(names_list)>30:
                await interaction.response.send_message('use maximum 30 names or roles try again' ,ephemeral=True)
                return
            last_ids_list = []
            if len(names_list) != len(ids_list):
                await interaction.response.send_message('the count of names and ids must be equal try again' ,ephemeral=True)
                return
            flag = False
            for i in ids_list:
                i = int(i)
                for j in interaction.guild.roles:
                    if i == j.id:
                        if interaction.guild.me.top_role.position < j.position:
                            await interaction.response.send_message('one of the roles that you choosed is above me !' ,ephemeral=True)
                            return
                        last_ids_list.append(i)
                        flag=True
            if flag ==True:
                if len(last_ids_list)== len(names_list) and len(last_ids_list) == len(new_emoji_list):
                    letters = string.ascii_lowercase
                    customer_id=''.join(random.choice(letters) for i in range(10))

                    collection.insert_one({'guild_id':interaction.guild_id , 'user_id':interaction.user.id,"role_ids":last_ids_list , 'name_list':names_list , 'emoji_list':new_emoji_list , 'placeholder':placeholder , 'is_active':False , 'custom_id':customer_id , 'update':False, 'min_value':None ,'max_value':None })
                    embed = discord.Embed(title=f'{title}' ,description=f'{final_text}' , timestamp=datetime.now() , color=tmp_color )
                    embed.set_image(url='https://cdn.discordapp.com/attachments/1135103098805817477/1135105421644943400/giphy.gif')
                    await interaction.response.defer()
                    await interaction.followup.send('done')
                    viewsender=DropDownView(interaction)
                    await checker_channel.send(embed=embed , view=viewsender)
                else:
                    await interaction.response.send_message('i couldnt find all roles in the server copy roles id correctly or roles and names and emojies are not equal!\nor maybe you entered equal but one of the roles are not exist !' ,ephemeral=True)
                    return
            else:
                await interaction.response.send_message('i couldnt find even one of these roles' ,ephemeral=True)
        except:
            await interaction.followup.send(f'{interaction.user.mention} something went wrong maybe you didnt use this command with correct options or its just server issue then pls try again and make sure you enter everything correctly')





async def setup(bot : Bot):
    await bot.add_cog(SelectRoles(bot))
