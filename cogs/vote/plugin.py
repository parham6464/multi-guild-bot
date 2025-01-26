from __future__ import annotations

from core.bot import Bot
from typing import Any, Optional , Callable , Literal , Union
from datetime import timedelta , datetime
from cogs.cog_config import Plugin
from discord.ext import commands , tasks 
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
from core.embed import Embed
from core.models import Giveawaymodel
from views.giveaway import GiveawayView
import time
import humanfriendly
import asyncio
from discord import ui
from discord import Colour


cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["vote"]

class yesno(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':True,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':True,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':True,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']

    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':True,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']


    @ui.button(label='Yes' , custom_id='yesss' , style=discord.ButtonStyle.primary)
    async def yesss(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':True,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed another option remove that option and choose this' , ephemeral=True)
            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':True, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers , 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':True, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':True, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                
    
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)
    @ui.button(label='No' , custom_id='noooo' , style=discord.ButtonStyle.primary)
    async def nooo(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':True,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed another option remove that option and choose this' , ephemeral=True)
            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':True, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':True, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)

            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':True, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                


            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='total votes: 0' , custom_id='vt_count' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...

    @ui.button(label='Finish Vote' , custom_id='finish_yesno', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':True,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_yesno', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':True,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )



class optione2(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']
    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']


    @ui.button(label='1' , custom_id='option1_2' , style=discord.ButtonStyle.primary)
    async def option1_2(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed another option remove that option and choose this' , ephemeral=True)
            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)
    

    @ui.button(label='2' , custom_id='option2_2' , style=discord.ButtonStyle.primary)
    async def option2_2(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed another option remove that option and choose this' , ephemeral=True)
            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='total votes: 0' , custom_id='vt_2' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...
    @ui.button(label='Finish Vote' , custom_id='finish_2', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_2', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )


class optione3(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2'] , find['option3']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']
    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']


    @ui.button(label='1' , custom_id='option1_3' , style=discord.ButtonStyle.primary)
    async def option1_3(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)
    

    @ui.button(label='2' , custom_id='option2_3' , style=discord.ButtonStyle.primary)
    async def option2_3(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2, list3 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)


            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='3' , custom_id='option3_3' , style=discord.ButtonStyle.primary)
    async def option3_3(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione3_count']
            users = []
            users.append(interaction.user.id)
            if list3 is not None:
                if interaction.user.id not in list3:
                    list3.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list3.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list3 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='total votes: 0' , custom_id='vt_3' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...

    @ui.button(label='Finish Vote' , custom_id='finish_3', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_3', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )


class optione4(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2'] , find['option3'] , find['option4']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']
    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']


    @ui.button(label='1' , custom_id='option1_4' , style=discord.ButtonStyle.primary)
    async def option1_4(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)
    

    @ui.button(label='2' , custom_id='option2_4' , style=discord.ButtonStyle.primary)
    async def option2_4(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2, list3 , list4 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='3' , custom_id='option3_4' , style=discord.ButtonStyle.primary)
    async def option3_4(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione3_count']
            users = []
            users.append(interaction.user.id)
            if list3 is not None:
                if interaction.user.id not in list3:
                    list3.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list3.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list3 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)



    @ui.button(label='4' , custom_id='option4_4' , style=discord.ButtonStyle.primary)
    async def option4_4(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione4_count']
            users = []
            users.append(interaction.user.id)
            if list4 is not None:
                if interaction.user.id not in list4:
                    list4.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list4.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list4 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='total votes: 0' , custom_id='vt_4' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...
    @ui.button(label='Finish Vote' , custom_id='finish_4', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_4', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )


class optione5(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2'] , find['option3'] , find['option4'] , find['option5']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']
    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']


    @ui.button(label='1' , custom_id='option1_5' , style=discord.ButtonStyle.primary)
    async def option1_5(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)
    

    @ui.button(label='2' , custom_id='option2_5' , style=discord.ButtonStyle.primary)
    async def option2_5(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2, list3 , list4 , list5 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)


            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='3' , custom_id='option3_5' , style=discord.ButtonStyle.primary)
    async def option3_5(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)


            numbers  =find['optione3_count']
            users = []
            users.append(interaction.user.id)
            if list3 is not None:
                if interaction.user.id not in list3:
                    list3.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list3.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list3 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='4' , custom_id='option4_5' , style=discord.ButtonStyle.primary)
    async def option4_5(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione4_count']
            users = []
            users.append(interaction.user.id)
            if list4 is not None:
                if interaction.user.id not in list4:
                    list4.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list4.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list4 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='5' , custom_id='option5_5' , style=discord.ButtonStyle.primary)
    async def option5_5(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione5_count']
            users = []
            users.append(interaction.user.id)
            if list5 is not None:
                if interaction.user.id not in list5:
                    list5.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list5.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list5 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)

            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='total votes: 0' , custom_id='vt_5' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...
    @ui.button(label='Finish Vote' , custom_id='finish_5', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_5', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )


class optione6(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2'] , find['option3'] , find['option4'] , find['option5'] , find['option6']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']

    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']

    @ui.button(label='1' , custom_id='option1_6' , style=discord.ButtonStyle.primary)
    async def option1_6(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    return

                else:
                    numbers-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    return
            else:
                numbers+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                return
    
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='2' , custom_id='option2_6' , style=discord.ButtonStyle.primary)
    async def option2_6(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2, list3 , list4 , list5 , list6 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)


            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='3' , custom_id='option3_6' , style=discord.ButtonStyle.primary)
    async def option3_6(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)


            numbers  =find['optione3_count']
            users = []
            users.append(interaction.user.id)
            if list3 is not None:
                if interaction.user.id not in list3:
                    list3.extend(users)
                    numbers+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    list3.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                list3 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='4' , custom_id='option4_6' , style=discord.ButtonStyle.primary)
    async def option4_6(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione4_count']
            users = []
            users.append(interaction.user.id)
            if list4 is not None:
                if interaction.user.id not in list4:
                    list4.extend(users)
                    numbers+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    list4.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                list4 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='5' , custom_id='option5_6' , style=discord.ButtonStyle.primary)
    async def option5_6(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione5_count']
            users = []
            users.append(interaction.user.id)
            if list5 is not None:
                if interaction.user.id not in list5:
                    list5.extend(users)
                    numbers+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    list5.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                list5 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='6' , custom_id='option6_6' , style=discord.ButtonStyle.primary)
    async def option6_6(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione6_count']
            users = []
            users.append(interaction.user.id)
            if list6 is not None:
                if interaction.user.id not in list6:
                    list6.extend(users)
                    numbers+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    list6.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                list6 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='total votes: 0' , custom_id='vt_6' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...
    @ui.button(label='Finish Vote' , custom_id='finish_6', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_6', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )


class optione7(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2'] , find['option3'] , find['option4'] , find['option5'] , find['option6'] , find['option7']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']
    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']


    @ui.button(label='1' , custom_id='option1_7' , style=discord.ButtonStyle.primary)
    async def option1_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)
    

    @ui.button(label='2' , custom_id='option2_7' , style=discord.ButtonStyle.primary)
    async def option2_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2, list3 , list4 , list5 , list6 , list7 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)


            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='3' , custom_id='option3_7' , style=discord.ButtonStyle.primary)
    async def option3_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)


            numbers  =find['optione3_count']
            users = []
            users.append(interaction.user.id)
            if list3 is not None:
                if interaction.user.id not in list3:
                    list3.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list3.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list3 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='4' , custom_id='option4_7' , style=discord.ButtonStyle.primary)
    async def option4_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione4_count']
            users = []
            users.append(interaction.user.id)
            if list4 is not None:
                if interaction.user.id not in list4:
                    list4.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list4.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list4 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='5' , custom_id='option5_7' , style=discord.ButtonStyle.primary)
    async def option5_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione5_count']
            users = []
            users.append(interaction.user.id)
            if list5 is not None:
                if interaction.user.id not in list5:
                    list5.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list5.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list5 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='6' , custom_id='option6_7' , style=discord.ButtonStyle.primary)
    async def option6_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione6_count']
            users = []
            users.append(interaction.user.id)
            if list6 is not None:
                if interaction.user.id not in list6:
                    list6.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list6.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list6 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='7' , custom_id='option7_7' , style=discord.ButtonStyle.primary)
    async def option7_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione7_count']
            users = []
            users.append(interaction.user.id)
            if list7 is not None:
                if interaction.user.id not in list7:
                    list7.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list7.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list7 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='total votes: 0' , custom_id='vt_7' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...

    @ui.button(label='Finish Vote' , custom_id='finish_7', style=discord.ButtonStyle.danger )
    async def finish_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_7', style=discord.ButtonStyle.danger )
    async def cancel_7(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )


class optione8(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2'] , find['option3'] , find['option4'] , find['option5'] , find['option6'] , find['option7'] , find['option8']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']

    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']

    @ui.button(label='1' , custom_id='option1_8' , style=discord.ButtonStyle.primary)
    async def option1_8(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                
    
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='2' , custom_id='option2_8' , style=discord.ButtonStyle.primary)
    async def option2_8(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2, list3 , list4 , list5 , list6 , list7 , list8 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)


            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='3' , custom_id='option3_8' , style=discord.ButtonStyle.primary)
    async def option3_8(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)


            numbers  =find['optione3_count']
            users = []
            users.append(interaction.user.id)
            if list3 is not None:
                if interaction.user.id not in list3:
                    list3.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list3.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list3 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='4' , custom_id='option4_8' , style=discord.ButtonStyle.primary)
    async def option4_8(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione4_count']
            users = []
            users.append(interaction.user.id)
            if list4 is not None:
                if interaction.user.id not in list4:
                    list4.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list4.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list4 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='5' , custom_id='option5_8' , style=discord.ButtonStyle.primary)
    async def option5_8(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione5_count']
            users = []
            users.append(interaction.user.id)
            if list5 is not None:
                if interaction.user.id not in list5:
                    list5.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list5.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list5 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='6' , custom_id='option6_8' , style=discord.ButtonStyle.primary)
    async def option6_8(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione6_count']
            users = []
            users.append(interaction.user.id)
            if list6 is not None:
                if interaction.user.id not in list6:
                    list6.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list6.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list6 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='7' , custom_id='option7_8' , style=discord.ButtonStyle.primary)
    async def option7_8(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione7_count']
            users = []
            users.append(interaction.user.id)
            if list7 is not None:
                if interaction.user.id not in list7:
                    list7.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list7.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list7 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='8' , custom_id='option8_8' , style=discord.ButtonStyle.primary)
    async def option8_8(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione8_count']
            users = []
            users.append(interaction.user.id)
            if list8 is not None:
                if interaction.user.id not in list8:
                    list8.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list8.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list8 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='total votes: 0' , custom_id='vt_8' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...
    @ui.button(label='Finish Vote' , custom_id='finish_8', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_8', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )


class optione9(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2'] , find['option3'] , find['option4'] , find['option5'] , find['option6'] , find['option7'] , find['option8'] , find['option9']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']
    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']


    @ui.button(label='1' , custom_id='option1_9' , style=discord.ButtonStyle.primary)
    async def option1_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 , list9 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)
    

    @ui.button(label='2' , custom_id='option2_9' , style=discord.ButtonStyle.primary)
    async def option2_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2, list3 , list4 , list5 , list6 , list7 , list8 , list9 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)


            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='3' , custom_id='option3_9' , style=discord.ButtonStyle.primary)
    async def option3_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)
 
            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 , list9 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)


            numbers  =find['optione3_count']
            users = []
            users.append(interaction.user.id)
            if list3 is not None:
                if interaction.user.id not in list3:
                    list3.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list3.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list3 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='4' , custom_id='option4_9' , style=discord.ButtonStyle.primary)
    async def option4_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 ,list9 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione4_count']
            users = []
            users.append(interaction.user.id)
            if list4 is not None:
                if interaction.user.id not in list4:
                    list4.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list4.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list4 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='5' , custom_id='option5_9' , style=discord.ButtonStyle.primary)
    async def option5_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 , list9 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione5_count']
            users = []
            users.append(interaction.user.id)
            if list5 is not None:
                if interaction.user.id not in list5:
                    list5.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list5.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list5 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='6' , custom_id='option6_9' , style=discord.ButtonStyle.primary)
    async def option6_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 , list9 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione6_count']
            users = []
            users.append(interaction.user.id)
            if list6 is not None:
                if interaction.user.id not in list6:
                    list6.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list6.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list6 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='7' , custom_id='option7_9' , style=discord.ButtonStyle.primary)
    async def option7_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 , list9 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione7_count']
            users = []
            users.append(interaction.user.id)
            if list7 is not None:
                if interaction.user.id not in list7:
                    list7.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list7.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list7 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='8' , custom_id='option8_9' , style=discord.ButtonStyle.primary)
    async def option8_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 , list9 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione8_count']
            users = []
            users.append(interaction.user.id)
            if list8 is not None:
                if interaction.user.id not in list8:
                    list8.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list8.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list8 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='9' , custom_id='option9_9' , style=discord.ButtonStyle.primary)
    async def option9_9(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 , list9 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione9_count']
            users = []
            users.append(interaction.user.id)
            if list9 is not None:
                if interaction.user.id not in list9:
                    list9.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option9':list9 , 'optione9_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list9.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option9':list9 , 'optione9_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list9 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option9':list9 , 'optione9_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='total votes: 0' , custom_id='vt_9' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...
    @ui.button(label='Finish Vote' , custom_id='finish_9', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_9', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )

class optione10(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    def get_lister(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['option1'] , find['option2'] , find['option3'] , find['option4'] , find['option5'] , find['option6'] , find['option7'] , find['option8'] , find['option9'] , find['option10']
    def get_number_yes(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione1_count']
    def get_number_no(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['optione2_count']
    def get_total(self,interaction):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):        
            return find['total_options']


    @ui.button(label='1' , custom_id='option1_10' , style=discord.ButtonStyle.primary)
    async def option1_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 , list9 , list10 = self.get_lister(interaction)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)

            numbers  =self.get_number_yes(interaction)
            users = []
            users.append(interaction.user.id)
            if lists is not None:
                if interaction.user.id not in lists:
                    lists.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':list2 , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)
                    

                else:
                    numbers-=1
                    total_votes-=1
                    lists.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
                    
            else:
                numbers+=1
                total_votes+=1
                lists = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option1':lists , 'optione1_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
                
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)
    

    @ui.button(label='2' , custom_id='option2_10' , style=discord.ButtonStyle.primary)
    async def option2_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2, list3 , list4 , list5 , list6 , list7 , list8 , list9 , list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)


            numbers  =self.get_number_no(interaction)
            users = []
            users.append(interaction.user.id)
            if list2 is not None:
                if interaction.user.id not in list2:
                    list2.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list2.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list2 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option2':list2 , 'optione2_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='3' , custom_id='option3_10' , style=discord.ButtonStyle.primary)
    async def option3_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 , list9 , list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)


            numbers  =find['optione3_count']
            users = []
            users.append(interaction.user.id)
            if list3 is not None:
                if interaction.user.id not in list3:
                    list3.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list3.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list3 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option3':list3 , 'optione3_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='4' , custom_id='option4_10' , style=discord.ButtonStyle.primary)
    async def option4_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 ,list9 , list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione4_count']
            users = []
            users.append(interaction.user.id)
            if list4 is not None:
                if interaction.user.id not in list4:
                    list4.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list4.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list4 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option4':list4 , 'optione4_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='5' , custom_id='option5_10' , style=discord.ButtonStyle.primary)
    async def option5_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 , list9 , list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione5_count']
            users = []
            users.append(interaction.user.id)
            if list5 is not None:
                if interaction.user.id not in list5:
                    list5.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list5.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list5 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option5':list5 , 'optione5_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='6' , custom_id='option6_10' , style=discord.ButtonStyle.primary)
    async def option6_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6 , list7 , list8 , list9 , list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione6_count']
            users = []
            users.append(interaction.user.id)
            if list6 is not None:
                if interaction.user.id not in list6:
                    list6.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list6.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list6 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option6':list6 , 'optione6_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='7' , custom_id='option7_10' , style=discord.ButtonStyle.primary)
    async def option7_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 , list9 , list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione7_count']
            users = []
            users.append(interaction.user.id)
            if list7 is not None:
                if interaction.user.id not in list7:
                    list7.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list7.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list7 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option7':list7 , 'optione7_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='8' , custom_id='option8_10' , style=discord.ButtonStyle.primary)
    async def option8_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 , list9 , list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione8_count']
            users = []
            users.append(interaction.user.id)
            if list8 is not None:
                if interaction.user.id not in list8:
                    list8.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list8.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list8 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option8':list8 , 'optione8_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='9' , custom_id='option9_10' , style=discord.ButtonStyle.primary)
    async def option9_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 , list9 ,list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list10 is not None:
                if interaction.user.id in list10:
                    return await interaction.response.send_message('you already choosed option 10 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione9_count']
            users = []
            users.append(interaction.user.id)
            if list9 is not None:
                if interaction.user.id not in list9:
                    list9.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option9':list9 , 'optione9_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list9.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option9':list9 , 'optione9_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list9 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option9':list9 , 'optione9_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)

    @ui.button(label='10' , custom_id='option10_10' , style=discord.ButtonStyle.primary)
    async def option10_10(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            required_role = find['required_role']
            total_votes = self.get_total(interaction)
            role_checker = discord.utils.get(interaction.guild.roles , id = required_role)
            flag=False
            if required_role is not None:
                if role_checker is not None:
                    for j in interaction.user.roles:
                        if j.id == role_checker.id:
                            flag=True
                else:
                    flag=True
            else:
                flag=True
            
            if flag==False:
                return await interaction.response.send_message(f'you dont have required role' , ephemeral=True)

            lists , list2 , list3 , list4 , list5 , list6  ,list7 , list8 , list9 , list10 = self.get_lister(interaction)
            if lists is not None:
                if interaction.user.id in lists:
                    return await interaction.response.send_message('you already choosed option 1 remove that option and choose this' , ephemeral=True)
            if list2 is not None:
                if interaction.user.id in list2:
                    return await interaction.response.send_message('you already choosed option 2 remove that option and choose this' , ephemeral=True)
            if list3 is not None:
                if interaction.user.id in list3:
                    return await interaction.response.send_message('you already choosed option 3 remove that option and choose this' , ephemeral=True)
            if list4 is not None:
                if interaction.user.id in list4:
                    return await interaction.response.send_message('you already choosed option 4 remove that option and choose this' , ephemeral=True)
            if list5 is not None:
                if interaction.user.id in list5:
                    return await interaction.response.send_message('you already choosed option 5 remove that option and choose this' , ephemeral=True)
            if list6 is not None:
                if interaction.user.id in list6:
                    return await interaction.response.send_message('you already choosed option 6 remove that option and choose this' , ephemeral=True)
            if list7 is not None:
                if interaction.user.id in list7:
                    return await interaction.response.send_message('you already choosed option 7 remove that option and choose this' , ephemeral=True)
            if list8 is not None:
                if interaction.user.id in list8:
                    return await interaction.response.send_message('you already choosed option 8 remove that option and choose this' , ephemeral=True)
            if list9 is not None:
                if interaction.user.id in list9:
                    return await interaction.response.send_message('you already choosed option 9 remove that option and choose this' , ephemeral=True)

            numbers  =find['optione10_count']
            users = []
            users.append(interaction.user.id)
            if list10 is not None:
                if interaction.user.id not in list10:
                    list10.extend(users)
                    numbers+=1
                    total_votes+=1
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option10':list10 , 'optione10_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you voted successfully' , ephemeral=True)

                else:
                    numbers-=1
                    total_votes-=1
                    list10.remove(interaction.user.id)
                    collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option10':list10 , 'optione10_count':numbers, 'total_options':total_votes}})
                    await interaction.response.send_message('you removed from vote' , ephemeral=True)
            else:
                numbers+=1
                total_votes+=1
                list10 = users
                collection.update_one({"guild_id":interaction.guild_id ,'end_vote':False, 'yesmode':False, "msg_id":interaction.message.id , 'channel_id':interaction.channel.id} , {'$set':{'option10':list10 , 'optione10_count':numbers, 'total_options':total_votes}})
                await interaction.response.send_message('you voted successfully' , ephemeral=True)
            self.vt_count.label = "total votes: "+str(total_votes) 
            await interaction.message.edit(view=self)


    @ui.button(label='total votes: 0' , custom_id='vt_10' , disabled=True)
    async def vt_count(self, interaction:discord.Interaction,_):
        ...

    @ui.button(label='Finish Vote' , custom_id='finish_10', style=discord.ButtonStyle.danger )
    async def finish_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                collection.update_one({"msg_id":interaction.message.id} , {'$set':{'duration':time.time()}})
                await self.bot.success(
                    f'vote finished successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can finish the vote',
                    interaction,
                    ephemeral=True
                )
    @ui.button(label='Cancel Vote' , custom_id='cancel_10', style=discord.ButtonStyle.danger )
    async def cancel_yesno(self, interaction:discord.Interaction,_):
        if (find:=collection.find_one({"guild_id":interaction.guild_id , 'yesmode':False,"msg_id":interaction.message.id , 'channel_id':interaction.channel.id,'end_vote':False})):
            userid = find['user_id']
            if interaction.user.id == userid or interaction.user.id == interaction.guild.owner_id:
                await interaction.message.delete()
                collection.delete_one({'msg_id':interaction.message.id})
                await self.bot.success(
                    f'vote canceled successfully',
                    interaction,
                    ephemeral=True
                )
            else:
                await self.bot.error(
                    f'only host or owner can cancel the vote',
                    interaction,
                    ephemeral=True
                )

class Embednew(discord.Embed):
    def __init__(self , color:Optional[Union[int , Colour]]=Colour.blurple(),**kwargs):
        super().__init__(color=color , **kwargs)

class vote(Plugin):
    def __init__(self , bot:Bot):
        self.bot = bot

    async def cog_load(self):
        await super().cog_load()
        self.bot.add_view(yesno(self.bot))
        self.bot.add_view(optione2(self.bot))
        self.bot.add_view(optione3(self.bot))
        self.bot.add_view(optione4(self.bot))
        self.bot.add_view(optione5(self.bot))
        self.bot.add_view(optione6(self.bot))
        self.bot.add_view(optione7(self.bot))
        self.bot.add_view(optione8(self.bot))
        self.bot.add_view(optione9(self.bot))
        self.bot.add_view(optione10(self.bot))
        self.vote_task.start()
    
    @tasks.loop(seconds=2)
    async def vote_task(self):
        try:
            votes = collection.find({"end_vote":False})
            if not votes:return
            for vw in votes:
                guilder = vw['guild_id']
                msg_id = vw['msg_id']
                channelid = vw['channel_id']
                timer = vw['duration']

                if timer < time.time():
                    if(
                        guild:= await self.bot.get_or_fetch_guild(guilder)
                    ):
                        if(
                            channel:=guild.get_channel(channelid) or await guild.fetch_channel(channelid)
                        ):
                            message = self.bot.get_message(msg_id,channelid,guild.id)
                            await self.end_votee(guild , message , channel)
        except:
            return



    def end_vote_updater(self,guild,message):
        collection.delete_one({'guild_id':guild.id , 'msg_id':message.id})

    async def end_votee(self,guild:discord.Guild , message:discord.PartialMessage ,channel:discord.TextChannel):
        checker_channel = discord.utils.get(guild.channels , id = channel.id)
        flager_mesesage =False
        async for messager in checker_channel.history(limit=None):
            if messager.id == message.id:
                flager_mesesage=True
        
        if flager_mesesage == False:
            self.end_vote_updater(guild,message)

        if (find:=collection.find_one({'guild_id':guild.id , 'msg_id':message.id})):
            subject = find['subject']
            names_value  = find['names']
            embed_title = find['title']
            embed_description = find['description']
            embed_color = find['color']
            embed_pic = find['img']
            final_texter1:str=''
            total_count_vt = find['total_options']
            user_host  = find['user_id']
            message_spliter = list(embed_description.split('/n'))
            for i in range(len(message_spliter)):
                if i != len(message_spliter)-1:
                    final_texter1 += f'{message_spliter[i]}\n'
                else:
                    final_texter1 += f'{message_spliter[i]}'
            num1=find['optione1_count']
            num2=find['optione2_count']
            num3=find['optione3_count']
            num4=find['optione4_count']
            num5=find['optione5_count']
            num6=find['optione6_count']
            num7=find['optione7_count']
            num8=find['optione8_count']
            num9=find['optione9_count']
            num10=find['optione10_count']
            yesmode_checker = find['yesmode']
            if num1 ==0 and num2 ==0 and num3 ==0 and num4 ==0 and num5 ==0 and num6 ==0 and num7 ==0 and num8 ==0 and num9 ==0 and num10 ==0:
                embed_result=Embednew(description='no one joined to vote' , color=embed_color)
                await message.reply(embed=embed_result)
                embed = discord.Embed(
                    title = embed_title,
                    description=final_texter1,
                    color=embed_color,
                    timestamp=datetime.now()
                )
                if embed_pic is not None:
                    embed.set_image(url=embed_pic)
                embed.add_field(name='Subject' , value=subject , inline=False)
                if len(names_value) !=0:
                    for i in range(len(names_value)):
                        tmp_txt= "> "+str(i)+":"
                        embed.add_field(name=tmp_txt , value=names_value[i] , inline=False)

                host_checker = discord.utils.get(guild.members , id=user_host)
                if host_checker is not None:
                    embed.add_field(name='> Host:' , value=host_checker.mention , inline=False)


                embed.add_field(name='> Vote Result:' , value='no one joined to vote' , inline=False)
                embed.add_field(name='> Vote ended:' , value='vote ended successfully' , inline=False)
                embed.add_field(name=f'> Total Votes: {total_count_vt}' , value='' , inline=False)
                await message.edit(embed=embed , view=None)
                self.end_vote_updater(guild,message)
            else:
                my_li  =[]
                my_li.append(num1)
                my_li.append(num2)
                my_li.append(num3)
                my_li.append(num4)
                my_li.append(num5)
                my_li.append(num6)
                my_li.append(num7)
                my_li.append(num8)
                my_li.append(num9)
                my_li.append(num10)

                max_number = max(my_li)
                index_finder = my_li.index(max_number)
                final_text:str
                final_list=[]
                embed = discord.Embed(
                    title = embed_title,
                    description=final_texter1,
                    color=embed_color,
                    timestamp=datetime.now()
                )
                if embed_pic is not None:
                    embed.set_image(url=embed_pic)
                embed.add_field(name='Subject' , value=subject , inline=False)
                if len(names_value) !=0:
                    for i in range(len(names_value)):
                        tmp_txt= "> "+str(i)+":"
                        embed.add_field(name=tmp_txt , value=names_value[i], inline=False)
                        
                host_checker = discord.utils.get(guild.members , id=user_host)
                if host_checker is not None:
                    embed.add_field(name='> Host:' , value=host_checker.mention , inline=False)
 
                
                for i in range(len(my_li)):
                    if max_number == my_li[i]:
                        final_list.append(str(i+1))
                if len(final_list) >1:
                    final_text = ','.join(final_list)
                    if yesmode_checker == False:
                        embed_result=Embednew(description=f'options {final_text} were tied by majority vote' , color=embed_color)
                        await message.reply(embed=embed_result)
                        embed.add_field(name='> Vote Result:' , value=f'options {final_text} were tied by majority vote', inline=False)
                    else:
                        embed_result=Embednew(description=f'The voting result is equal' , color=embed_color)
                        await message.reply(embed=embed_result)
                        embed.add_field(name='> Vote Result:' , value=f'The vote was only contain yes and no options and The voting result is equal', inline=False)
                else:
                    if yesmode_checker == False:
                        embed_result=Embednew(description=f'option {index_finder+1} was chosen by majority vote' , color=embed_color)
                        await message.reply(embed=embed_result)
                        embed.add_field(name='> Vote Result:' , value=f'option {index_finder+1} was chosen by majority vote', inline=False)
                    else:
                        if index_finder == 0:
                            embed_result=Embednew(description=f'the majority of people voted for yes', color=embed_color)
                            await message.reply(embed=embed_result)
                            embed.add_field(name='> Vote Result:' , value='the majority of people voted for yes', inline=False)
                        elif index_finder ==1:
                            embed_result=Embednew(description=f'the majority of people voted for no', color=embed_color)
                            await message.reply(embed=embed_result)
                            embed.add_field(name='> Vote Result:' , value='the majority of people voted for no', inline=False)

                embed.add_field(name='> Vote Ended:' , value='the vote ended successfully' , inline=False)
                embed.add_field(name=f'> Total Votes: {total_count_vt}' , value='' , inline=False)
                await message.edit(embed=embed , view=None)
                self.end_vote_updater(guild,message)
        # await message.reply('yes')
    @app_commands.command(name='vote' , description='create vote' )
    @app_commands.describe(
        channel='the channel that vote will send',
        description='you can go to new line with /n',
        duration = 'exp : 1d, 1s , 1h',
        img = 'can be only picture',
        question = 'you can go to new line with /n'
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

    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def votenew(self , interaction:discord.Interaction,question:str ,title:str,description:str, color:app_commands.Choice[int] ,duration:str , channel:discord.TextChannel ,required_role:Optional[discord.Role],img:Optional[discord.Attachment], option1:Optional[Union[str,str]], option2:Optional[Union[str,str]] ,option3:Optional[Union[str,str]], option4:Optional[Union[str,str]], option5:Optional[Union[str,str]], option6:Optional[Union[str,str]] ,option7:Optional[Union[str,str]], option8:Optional[Union[str,str]] ,option9:Optional[Union[str,str]] ,option10:Optional[Union[str,str]]):
        ends_at = humanfriendly.parse_timespan(duration) + time.time()
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
        
        final_texter_question:str=''
        message_spliter1 = list(question.split('/n'))
        for i in range(len(message_spliter1)):
            if i != len(message_spliter1)-1:
                final_texter_question += f'{message_spliter1[i]}\n'
            else:
                final_texter_question += f'{message_spliter1[i]}'


        final_texter:str=''
        message_spliter = list(description.split('/n'))
        for i in range(len(message_spliter)):
            if i != len(message_spliter)-1:
                final_texter += f'{message_spliter[i]}\n'
            else:
                final_texter += f'{message_spliter[i]}'
        totla_count = 0
        names_value = []
        if option1 is not None:
            totla_count+=1
            names_value.append(option1)
        if option2 is not None:
            totla_count+=1
            names_value.append(option2)
        if option3 is not None:
            totla_count+=1
            names_value.append(option3)
        if option4 is not None:
            totla_count+=1
            names_value.append(option4)
        if option5 is not None:
            totla_count+=1
            names_value.append(option5)
        if option6 is not None:
            totla_count+=1
            names_value.append(option6)
        if option7 is not None:
            totla_count+=1
            names_value.append(option7)
        if option8 is not None:
            totla_count+=1
            names_value.append(option8)
        if option9 is not None:
            totla_count+=1
            names_value.append(option9)
        if option10 is not None:
            totla_count+=1
            names_value.append(option10)
        global msg
        if totla_count == 1:
            return await interaction.response.send_message('one option for question?! what kind of vote is this try again' , ephemeral=True)
        if totla_count !=0:
            img_contain =''
            embed = discord.Embed(
                title = title,
                description=final_texter,
                color = tmp_color,
                timestamp=datetime.now()
            )
            embed.add_field(name='Subject: ' , value=final_texter_question , inline=False)
            for i in range(len(names_value)):
                j=str(i +1)
                name_option = "> "+j+':'
                embed.add_field(name=name_option , value = names_value[i] , inline=False)
            
            if required_role is not None:
                embed.add_field (name='required role:' , value = required_role.mention , inline=False)

            if img is not None:
                typer = img.content_type
                if typer.startswith('image'):
                    embed.set_image(url=f'{img.url}')
                    img_contain = str(img.url)
                else:
                    img_contain = None
            else:
                img_contain = None
            embed.add_field (name='> Host:' , value = interaction.user.mention , inline=False)     
            embed.add_field(name='end at' , value = discord.utils.format_dt(datetime.fromtimestamp(ends_at),'R'))
            if totla_count == 2:
                msg=await channel.send(embed=embed , view=optione2(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )
            elif totla_count ==3:
                msg=await channel.send(embed=embed , view=optione3(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )
            elif totla_count ==4:
                msg=await channel.send(embed=embed , view=optione4(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )
            elif totla_count ==5:
                msg=await channel.send(embed=embed , view=optione5(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )
            elif totla_count ==6:
                msg=await channel.send(embed=embed , view=optione6(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )
            elif totla_count ==7:
                msg=await channel.send(embed=embed , view=optione7(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )
            elif totla_count ==8:
                msg=await channel.send(embed=embed , view=optione8(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )
            elif totla_count ==9:
                msg=await channel.send(embed=embed , view=optione9(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )
            elif totla_count ==10:
                msg=await channel.send(embed=embed , view=optione10(self.bot))
                await self.bot.success(
                    f'vote sent in {channel.mention}',
                    interaction,
                    ephemeral=True
                )

            if required_role is not None:
                collection.insert_one({'guild_id':interaction.guild_id ,'user_id':interaction.user.id,'duration':ends_at,'title':title,'color':tmp_color,'img':img_contain,'description':description,'names':names_value,'subject':final_texter_question ,'yesmode':False,'required_role':required_role.id,'total_options':0,'channel_id':channel.id , 'msg_id':msg.id,'end_vote':False ,'option1':None,'optione1_count':0,'option2':None,'optione2_count':0,'option3':None,'optione3_count':0,'option4':None,'optione4_count':0,'option5':None,'optione5_count':0,'option6':None,'optione6_count':0,'option7':None,'optione7_count':0,'option8':None,'optione8_count':0,'option9':None,'optione9_count':0,'optione10_count':0,'option10':None}) 
            else:
                collection.insert_one({'guild_id':interaction.guild_id ,'user_id':interaction.user.id,'duration':ends_at,'title':title,'color':tmp_color,'img':img_contain,'description':description,'names':names_value,'subject':final_texter_question ,'yesmode':False,'required_role':None,'total_options':0,'channel_id':channel.id , 'msg_id':msg.id,'end_vote':False ,'option1':None,'optione1_count':0,'option2':None,'optione2_count':0,'option3':None,'optione3_count':0,'option4':None,'optione4_count':0,'option5':None,'optione5_count':0,'option6':None,'optione6_count':0,'option7':None,'optione7_count':0,'option8':None,'optione8_count':0,'option9':None,'optione9_count':0,'optione10_count':0,'option10':None}) 

        else:
            embed = discord.Embed(
                title = title,
                description=final_texter,
                color = tmp_color,
                timestamp=datetime.now()
            )
            img_contain=''
            if img is not None:
                typer = img.content_type
                if typer.startswith('image'):
                    embed.set_image(url=f'{img.url}')
                    img_contain = str(img.url)
                else:
                    img_contain = None
            else:
                img_contain = None

            embed.add_field(name='> Subject: ' , value=final_texter_question , inline=False)  
            embed.add_field (name='> Host:' , value = interaction.user.mention , inline=False)         
            if required_role is not None:
                embed.add_field (name='> required role:' , value = required_role.mention , inline=False)   
            embed.add_field(name='> end at' , value = discord.utils.format_dt(datetime.fromtimestamp(ends_at),'R'))
            # viwer = discord.ui.View(timeout=None)
            # viwer.add_item(yesno())
            msg=await channel.send(embed=embed , view=yesno(self.bot))
            await self.bot.success(
                f'vote sent in {channel.mention}',
                interaction,
                ephemeral=True
            )
            
            
            if required_role is not None:
                collection.insert_one({'guild_id':interaction.guild_id ,'user_id':interaction.user.id,'duration':ends_at,'title':title,'color':tmp_color,'img':img_contain,'description':description,'names':names_value,'subject':final_texter_question,'yesmode':True,'required_role':required_role.id,'total_options':0,'channel_id':channel.id , 'msg_id':msg.id,'end_vote':False ,'option1':None,'optione1_count':0,'option2':None,'optione2_count':0,'option3':None,'optione3_count':0,'option4':None,'optione4_count':0,'option5':None,'optione5_count':0,'option6':None,'optione6_count':0,'option7':None,'optione7_count':0,'option8':None,'optione8_count':0,'option9':None,'optione9_count':0,'optione10_count':0,'option10':None}) 
            else:
                collection.insert_one({'guild_id':interaction.guild_id ,'user_id':interaction.user.id,'duration':ends_at,'title':title,'color':tmp_color,'img':img_contain,'description':description,'names':names_value,'subject':final_texter_question,'yesmode':True,'required_role':None,'total_options':0,'channel_id':channel.id , 'msg_id':msg.id,'end_vote':False ,'option1':None,'optione1_count':0,'option2':None,'optione2_count':0,'option3':None,'optione3_count':0,'option4':None,'optione4_count':0,'option5':None,'optione5_count':0,'option6':None,'optione6_count':0,'option7':None,'optione7_count':0,'option8':None,'optione8_count':0,'option9':None,'optione9_count':0,'optione10_count':0,'option10':None}) 

        # for i in range(totla_count):
                


        

async def setup(bot : Bot):
    await bot.add_cog(vote(bot))
