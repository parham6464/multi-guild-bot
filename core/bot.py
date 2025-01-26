from __future__ import annotations

import os
import sys
from typing import Optional
from discord.ext import commands
from logging import getLogger; log  = getLogger("Bot")
import discord
from discord import app_commands 
from embed import Embed
from tortoise import Tortoise
import config

__all__ = (

    "Bot",
)

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('a!'),
            intents=discord.Intents.all(),
            chunk_guild_at_startup=False,
            help_command=None,
        )

    async def on_tree_error(self ,interaction:discord.Interaction , error:app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            return await interaction.response.send_message(f'command cooldown try after {round(error.retry_after)}Seconds' , ephemeral=True)
        if isinstance(error,app_commands.MissingPermissions):
            return await interaction.response.send_message(f'your permission is not enough',ephemeral=True)
        if isinstance(error , app_commands.BotMissingPermissions):
            return await interaction.response.send_message(f'bot permission is not enough' , ephemeral=True)
        if isinstance(error , app_commands.MissingRole):
            return await interaction.response.send_message(f'Bot Missing Role' , ephemeral=True)
        if isinstance(error , app_commands.CheckFailure):
            return await interaction.response.send_message(f'something went wrong try again' , ephemeral=True)


    async def setup_hook(self):
        await Tortoise.init(
            db_url=f'postgres://{config.USER}:{config.PASSWORD}@{config.HOST}:{config.PORT}/{config.NAME}',
            modules={
                "models":['core.models']
            }
        )
        await Tortoise.generate_schemas(safe=True)
        for filename in os.listdir('Bot1/cogs'):
            if not filename.startswith("_") and not filename.startswith("c"):
                await self.load_extension(f'cogs.{filename}.plugin')
                
    async def on_ready(self):
        log.info(f'logged in as {self.user} , ID: {self.user.id}')
        await self.change_presence(status=discord.Status.online , activity=discord.Activity(type=discord.ActivityType.watching, name="/help | a!help"))    

    async def on_connect(self):
        log.info(f'succesfully connected')
        self.tree.on_error = self.on_tree_error
        # if '-sync' in sys.argv:
        synced_command = await self.tree.sync()
        log.info(f'synced {len(synced_command)} commands')

    async def success(self , message:str, interaction:discord.Interaction,*,ephemeral:bool=False , embed:Optional[bool] = True)->Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed = Embed(description=message , color =discord.Colour.green()),
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed = Embed(description=message , color=discord.Colour.green()),
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=message , ephemeral=ephemeral)
            return await interaction.response.send_message(content=message , ephemeral=ephemeral)

    async def error(self , message:str, interaction:discord.Interaction,*,ephemeral:bool=True , embed:Optional[bool] = True)->Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed = Embed(description=message , color =discord.Colour.red()),
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed = Embed(description=message , color=discord.Colour.red()),
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=message , ephemeral=ephemeral)
            return await interaction.response.send_message(content=message , ephemeral=ephemeral)
    


    async def get_or_fetch_guild(self,guild_id:int)-> discord.Guild | None:
        return self.get_guild(guild_id) or await self.fetch_guild(guild_id)

    
    def get_message(
        self,
        message_id:int,
        channel_id:int,
        guild_id:int,
    )->discord.PartialMessage:
        return self.get_partial_messageable(channel_id , guild_id=guild_id).get_partial_message(message_id)

