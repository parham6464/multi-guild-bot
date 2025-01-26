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


cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["giveaway"]

class giveaway(Plugin):
    def __init__(self , bot:Bot):
        self.bot = bot

    async def cog_load(self):
        await super().cog_load()
        self.bot.add_view(GiveawayView(self.bot))
        self.giveaway_task.start()
    
    @tasks.loop(seconds=2)
    async def giveaway_task(self):
        giveaways = await Giveawaymodel.filter(is_active=True)
        if not giveaways:return
        for gw in giveaways:
            if gw.duration > time.time():
                continue
            if(
                guild:= await self.bot.get_or_fetch_guild(gw.guild_id)
            ):
                if(
                    channel:=guild.get_channel(gw.channel_id) or await guild.fetch_channel(gw.channel_id)
                ):
                    message = self.bot.get_message(gw.message_id,gw.channel_id,guild.id)
                    await gw.end_giveaway(guild , message)


    giveaway_def  =app_commands.Group(
        name = 'giveaway',
        description='giveaway moderation',
        guild_only=True,
        default_permissions=discord.Permissions(manage_guild=True)
    )
    @app_commands.describe(
        title='title of giveaway (embed)',
        description='description of Giveaway (embed) | use /n for going to new line',
        prize='prize of the giveaway',
        duration='time of giveaway with this syntanc : 1s = 1seconds , 1m=1minutes , 1h=1hour',
        channel='the channel that giveaway will be sent',
        required_role='the require role for joining the giveaway',
        winners = 'the count of winners',
        max_entries = 'join count limit'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @giveaway_def.command(name='create' , description='create giveaway')
    async def create_giveaway(
        self,
        interaction:discord.Interaction,
        title:str,
        description:str,
        prize:app_commands.Range[str,1,200],
        duration:str,
        channel: discord.TextChannel or None,
        required_role: Optional[Union[discord.Role , None]],
        winners:int =1,
        max_entries:int or None = None,
        
    
    
    
    ):
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this command' , ephemeral=True)

        try:
            ends_at = humanfriendly.parse_timespan(duration) + time.time()
        except:
            return await self.bot.error(
                f'please provide the giveaway duration in the given format: (1d) , (1m) , (10s)',interaction
            )
        else:
            assert interaction.channel is not None and isinstance(interaction.channel , discord.TextChannel)
            await interaction.response.defer(ephemeral=True)
            if max_entries is not None:
                if max_entries < winners:
                    return await self.bot.error(
                        f'you can not provide winners more than maximum entries',interaction
                    )
            messageable = channel or interaction.channel
            model = await Giveawaymodel(
                guild_id = interaction.guild_id,
                channel_id = messageable.id,
                host_id = interaction.user.id,
                required_role_id=required_role.id  if required_role else None,
                prize = prize ,
                duration = ends_at,
                winners = winners ,
                participants=[],
                max_entries=max_entries,
                is_active = True
            )
            final_text:str=''
            message_spliter = list(description.split('/n'))
            for i in range(len(message_spliter)):
                if i != len(message_spliter)-1:
                    final_text += f'{message_spliter[i]}\n'
                else:
                    final_text += f'{message_spliter[i]}'

            message = await messageable.send(
                embed = model.create_giveaway_embed(title,final_text,required_role=required_role , host = interaction.user) , view=GiveawayView(self.bot)
            )
            model.message_id = message.id
            await model.save()
            await asyncio.sleep(0.5)
            return await self.bot.success(
                f'A giveaway has been created in {messageable.mention}',interaction
            )
    @giveaway_def.command(name='reroll' , description='create giveaway' )
    @app_commands.describe(
        message_id='message id of giveaway',
        channel='the channel that giveaway sent'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def reroll_command(self , interaction:discord.Interaction, message_id:str , channel:discord.TextChannel or None):
        if interaction.guild.me.top_role.position > interaction.user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message('your role is not above me then you cant use this command' , ephemeral=True)

        assert interaction.guild and isinstance(interaction.channel , discord.TextChannel)
        messageable = channel or interaction.channel
        if not message_id.isdigit():
            return await self.bot.error(
                f'please provide a message id.',interaction
            )
        
        message = self.bot.get_message(
            int(message_id) , messageable.id , interaction.guild.id
        )
        if not message:
            return await self.bot.error(
                f'the giveaway message has been deleted' , interaction
            )
        if (model:= await Giveawaymodel.get_or_none(guild_id=interaction.guild_id , channel_id=messageable.id , message_id=int(message_id))):
            perm_checker= interaction.user.guild_permissions.administrator
            if model.host_id != interaction.user.id and model.host_id != interaction.guild.owner_id and perm_checker!=True:
                return await self.bot.error(
                    f'only host can reroll this giveaway',interaction , ephemeral=True
                )
            if model.is_active:
                return await self.bot.error(
                    f'the giveaway is still active , cannot reroll winners.' , interaction , ephemeral=True
                )
            winners = model.get_winner_mention(interaction.guild)
            embed = model.get_end_embed
            embed.clear_fields()
            if winners:
                embed.add_field(
                    name = 'Winners',
                    value = ', '.join(winners)
                )
                await message.edit(embed=embed)
                return await interaction.response.send_message(
                    f"the giveaway has been rerolled! new winners:\n{', '.join(winners)}"
                )
            else:
                return await interaction.response.send_message(
                    "No winners were selected"
                )

        else:
            return await self.bot.error(
                f'The giveaway does not exist' , interaction 
            )


            
        

async def setup(bot : Bot):
    await bot.add_cog(giveaway(bot))
