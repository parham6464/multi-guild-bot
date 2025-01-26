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
import os
from typing import Union 
import asyncio



cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["discord"]
collection = db["welcome"]
security = db['security']
autorole = db['autorole']
logerr = db['log']


class welcome(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_member_join(self,member):
        
        # if(find:= security.find_one({"_id":member.guild.id})):
        #     if find['anti_prune_role_id'] is not None and find['anti_prune'] == True:
        #         for role in member.guild.roles:
        #             if role.id == find['anti_prune_role_id']:
        #                 await member.add_roles(role)
        try:
            if(find:= autorole.find_one({"_id":member.guild.id})):
                roles = find['role']
                if roles is not None:
                    for role in member.guild.roles:
                        for i in roles:
                            check_member = discord.utils.get(member.guild.roles , id=i)
                            if member.guild.me.top_role.position < role.position:
                                pass
                            elif role.id == i:
                                await member.add_roles(role)
        except:
            pass

        try:
            if(find:= security.find_one({"_id":member.guild.id , 'bot_invite_ban_security':True})):             #anti prune
                if find['bot_invite_warn'] is not None:
                    async for entry in member.guild.audit_logs(action=discord.AuditLogAction.bot_add , limit=1):
                            if entry.target.id == member.id:
                                member = discord.utils.get(member.guild.members , id = entry.user.id)
                                if member.id == member.guild.me.id:
                                    pass
                                elif member.id == member.guild.owner_id:
                                    pass
                                if member.guild.me.top_role <= member.top_role:
                                    pass
                                else:
                                    bot_id = discord.utils.get(member.guild.members , id = entry.target.id)
                                    roles = find['bot_invite_white_role']
                                    user_ids = find['bot_invite_white_user']
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
                                    if check_white_role == True or check_white_user == True:
                                        check_white_user = False
                                        check_white_role = False

                                    all_white_roles = find['all_white_list_role']
                                    all_white_users = find['all_white_list_user']

                                    if all_white_roles is not None:
                                        for i in all_white_roles:
                                            for j in range(len(member.roles)):
                                                if i == member.roles[j].id:
                                                    check_white_role = True

                                    if all_white_users is not None:
                                        for i in all_white_users:
                                            if i == member.id:
                                                check_white_user = True

                                    else:

                                        if (find2:= security.find_one({"user_id":entry.user.id,"bot_add":True, "guild":member.guild.id})) is not None:
                                            warn=find2['warn']
                                            if warn == find['bot_invite_warn']:
                                                if find['security_log_channel'] is not None:
                                                    channel_sender = discord.utils.get(member.guild.text_channels , id =find['security_log_channel'])
                                                    if channel_sender is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti bot invite Log",
                                                        description= f"user Action : invite a bot\nwarn limit : {find['bot_invite_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find['bot_invite_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await channel_sender.send(embed=embed)
                                                if find['bot_invite_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await member.guild.kick(ss , reason='add a bot')
                                                    bot_added_id=discord.Object(entry.target.id , type='abc.Snowflake')
                                                    await member.guild.kick(bot_added_id , reason='none whitelist user added bot')
                                                    security.delete_one({"user_id":entry.user.id, "guild":member.guild.id,"bot_add":True})
                                                elif find['bot_invite_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await member.guild.ban(ss, reason='add a bot')
                                                    security.delete_one({"user_id":entry.user.id, "guild":member.guild.id,"bot_add":True})
                                                    bot_added_id=discord.Object(entry.target.id , type='abc.Snowflake')
                                                    await member.guild.ban(bot_added_id, reason='none whitelist user added bot')

                                            else:
                                                warn +=1
                                                if warn == find['bot_invite_warn']:
                                                    if find['security_log_channel'] is not None:
                                                        channel_sender = discord.utils.get(member.guild.text_channels , id =find['security_log_channel'])
                                                        if channel_sender is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti bot invite Log",
                                                            description= f"user Action : invite a bot\nwarn limit : {find['bot_invite_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find['bot_invite_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await channel_sender.send(embed=embed)
                                                    if find['bot_invite_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await member.guild.kick(ss, reason='add a bot')
                                                        bot_added_id=discord.Object(entry.target.id , type='abc.Snowflake')
                                                        await member.guild.kick(bot_added_id, reason='none whitelist user added bot')
                                                        security.delete_one({"user_id":entry.user.id, "guild":member.guild.id,"bot_add":True})
                                                    elif find['bot_invite_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await member.guild.ban(ss, reason='add a bot')
                                                        bot_added_id=discord.Object(entry.target.id , type='abc.Snowflake')
                                                        await member.guild.ban(bot_added_id, reason='none whitelist user added bot')
                                                        security.delete_one({"user_id":entry.user.id, "guild":member.guild.id,"bot_add":True})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id, "guild":member.guild.id,"bot_add":True} , {'$set':{'warn':warn}})
                                                    if find['security_log_channel'] is not None:
                                                        channel_sender = discord.utils.get(member.guild.text_channels , id =find['security_log_channel'])
                                                        if channel_sender is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti bot invite Log",
                                                            description= f"user Action : invite a bot\nwarn limit : {find['bot_invite_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await channel_sender.send(embed=embed)
                                        else:
                                            security.insert_one({'user_id':entry.user.id , "guild":member.guild.id , "bot_add":True, "warn":1})
                                            find2= security.find_one({"user_id":entry.user.id, "guild":member.guild.id,"bot_add":True})
                                            warn=find2['warn']
                                            if warn == find['bot_invite_warn']:
                                                if find['security_log_channel'] is not None:
                                                    channel_sender = discord.utils.get(member.guild.text_channels , id =find['security_log_channel'])
                                                    if channel_sender is not None:
                                                        embed=discord.Embed(
                                                        title=f"Anti bot invite Log",
                                                        description= f"user Action : invite a bot\nwarn limit : {find['bot_invite_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find['bot_invite_punishment']}",
                                                        timestamp=datetime.now(),
                                                        color= 0xF6F6F6
                                                        )
                                                        await channel_sender.send(embed=embed)
                                                if find['bot_invite_punishment']=='Kick':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await member.guild.kick(ss, reason='add a bot')
                                                    bot_added_id=discord.Object(entry.target.id , type='abc.Snowflake')
                                                    await member.guild.kick(bot_added_id, reason='none whitelist user added bot')
                                                    security.delete_one({"_id":entry.user.id})
                                                elif find['bot_invite_punishment']=='Ban':
                                                    ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                    await member.guild.ban(ss, reason='add a bot')
                                                    bot_added_id=discord.Object(entry.target.id , type='abc.Snowflake')
                                                    await member.guild.ban(bot_added_id, reason='none whitelist user added bot')
                                                    security.delete_one({"_id":entry.user.id})
                                            else:
                                                warn +=1
                                                if warn == find['bot_invite_warn']:
                                                    if find['security_log_channel'] is not None:
                                                        channel_sender = discord.utils.get(member.guild.text_channels , id =find['security_log_channel'])
                                                        if channel_sender is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti bot invite Log",
                                                            description= f"user Action : invite a bot\nwarn limit : {find['bot_invite_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: {find['bot_invite_punishment']}",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await channel_sender.send(embed=embed)
                                                    if find['bot_invite_punishment']=='Kick':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await member.guild.kick(ss, reason='add a bot')
                                                        bot_added_id=discord.Object(entry.target.id , type='abc.Snowflake')
                                                        await member.guild.kick(bot_added_id, reason='none whitelist user added bot')
                                                        security.delete_one({"user_id":entry.user.id, "guild":member.guild.id,"bot_add":True})
                                                    elif find['bot_invite_punishment']=='Ban':
                                                        ss=discord.Object(entry.user.id , type='abc.Snowflake')
                                                        await member.guild.ban(ss, reason='add a bot')
                                                        bot_added_id=discord.Object(entry.target.id , type='abc.Snowflake')
                                                        await member.guild.ban(bot_added_id, reason='none whitelist user added bot')
                                                        security.delete_one({"user_id":entry.user.id, "guild":member.guild.id,"bot_add":True})
                                                    
                                                else:
                                                    security.update_one({'user_id':entry.user.id, "guild":member.guild.id,"bot_add":True} , {'$set':{'warn':warn}})
                                                    if find['security_log_channel'] is not None:
                                                        channel_sender = discord.utils.get(member.guild.text_channels , id =find['security_log_channel'])
                                                        if channel_sender is not None:
                                                            embed=discord.Embed(
                                                            title=f"Anti bot invite Log",
                                                            description= f"user Action : invite a bot\nwarn limit : {find['bot_invite_warn']}\nuser: <@{entry.user.id}>\nusers warn : {warn}\nbot Action: increasing warn",
                                                            timestamp=datetime.now(),
                                                            color= 0xF6F6F6
                                                            )
                                                            await channel_sender.send(embed=embed)
        except:
            pass

        
        try:
            if(find:= collection.find_one({"_id":member.guild.id})):
                if find['style']==1:
                    tmp_guild = find['_id']
                    tmp_id_channel= find['channel']
                    webhooker_id = find['webhook']
                    if tmp_id_channel is not None:
                        main_guild=self.bot.get_guild(tmp_guild)
                        channel_send = discord.utils.get(main_guild.text_channels , id = tmp_id_channel)
                        exist_check = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
        

                        user = member.mention
                        user = user.replace("<","")
                        user = user.replace(">","")
                        user = user.replace("@","")
                        headers = {"Authorization": f"Bot {TOKEN}"}
                        userid = user
                        # req = requests.get(f"https://discord.com/api/v10/users/{userid}", headers=headers)
                        # ss=req.json()
                        
                        image_loader = await load_image_async(member.display_avatar.url)
                        bg = Editor(image_loader).resize((600,600)).blur("gaussian" , amount=9)
                        profile = Editor(image_loader).resize((350,350)).circle_image()
                        bg.paste(profile.image , (124,140))
                        # if ss['banner_color']==None:
                        bg.ellipse((122,138),width=352 , height=352 , stroke_width=15 , outline='white')
                        # else:
                        #     bg.ellipse((122,138),width=352 , height=352 , stroke_width=15 , outline=ss['banner_color'])
                            
                
                        #fonter=Font('OMEGLE.ttf' , size=30)
                        #########################
                        mc = main_guild.member_count
                        #######################
                        fonter_2=Font.poppins(size=20 ,variant='regular')
                        fonter=Font.poppins(size=30,variant='bold')
                        text=str(member)
                        if len(text)>30:
                            text = text[:30]
                        else:
                            text = str(member)
                        text2='members: '+str(mc) +' '
                        font_size2=fonter_2.getsize(text=text2)
                        font_size=fonter.getsize(text=text)
                        pluster3 = 300-(font_size2[0] / 2) 
                        pluser =  300-(font_size[0] / 2) 
                        pluser2= 300-(font_size[0] / 2) 
                        # if ss['banner_color']==None:

                        bg.rectangle((pluser-17,68),width=font_size[0]+20 , height=font_size[1]+20 , stroke_width=3 , outline='white'   , radius=30)
                        bg.text((pluser2-5,80),text=text , font=fonter  , color='white' )
                        bg.rectangle((46,503),width=511.5 , height=font_size2[1]+20 , stroke_width=3 , outline='white'  , radius=30)
                        bg.text((pluster3,515),text=text2 , font=fonter_2 , stroke_fill='#373c57' , color='white' )

                        # else:
                        #     bg.rectangle((pluser-17,68),width=font_size[0]+20 , height=font_size[1]+20 , stroke_width=3 , outline=ss['banner_color'] , fill=ss['banner_color']  , radius=30)
                        #     bg.text((pluser2-5,80),text=text , font=fonter , stroke_fill='#373c57' , color='white' )
                        #     bg.text((10,5),text='being a NITRO USER:ON' , font=fonter_2 , stroke_fill='#373c57' , color='white' )
                        #     bg.rectangle((46,503),width=511.5 , height=font_size2[1]+20 , stroke_width=3 , outline=ss['banner_color'] , fill=ss['banner_color']  , radius=30)
                        #     bg.text((pluster3,515),text=text2 , font=fonter_2 , stroke_fill='#373c57' , color='white' )

                        ##########################################################
                        ###################################################################
                        

                        # bg.text((250,90),text='👥' , font=fonter_2 , stroke_fill='#373c57' , color='white' )
                        file = discord.File(fp=bg.image_bytes, filename='circle.png')
                        user_title = find['title']
                        user_message = find['embed_text']
                        text_title=''
                        text_body=''
                        if user_title is not None:
                            text_title = str(user_title)
                        else:
                            text_title = member.guild.name+" server"
                        
                        if user_message is not None:
                            text_body = str(user_message)
                        else:
                            text_body = "welcome to the "+member.guild.name

                        if '@user_mention' in text_body:
                            text_body = text_body.replace("@user_mention" , member.mention)
                        color_choosen = find['color']
                        embed = discord.Embed(
                        title=f"{text_title}",
                        description= f"{text_body}",
                        timestamp=datetime.now(),
                        color= color_choosen
                        )
                        embed.set_image(url="attachment://circle.png")
                        embed.set_footer(text=f'Welcome To {member.guild.name}' , icon_url=member.display_avatar.url)
                        if channel_send is not None and exist_check is not None:
                            
                            await exist_check.send(embed=embed,file=file)
                elif find['style']==2:

                    tmp_guild = find['_id']
                    tmp_id_channel= find['channel']
                    user_message = find["message"]
                    user_title = find['title']
                    webhooker_id = find['webhook']
                    if tmp_id_channel is not None:
                        main_guild=self.bot.get_guild(tmp_guild)
                        channel_send = discord.utils.get(main_guild.text_channels , id = tmp_id_channel)
                        exist_check = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)

                        user = member.mention
                        user = user.replace("<","")
                        user = user.replace(">","")
                        user = user.replace("@","")
                
                        
                        image_loader = await load_image_async(member.display_avatar.url)
                        # image_loader1 = await load_image_async('welcome/back.jpg')
                        last_path = "\\welcome"
                        # finaler=os.path.join(last_path,"D:\\nabeghe_project\\New folder\\public bot\\cogs\\welcome","back.jpg")
                        finaler = os.path.abspath(os.getcwd())
                        background = Editor('./Bot1/cogs/welcome/back.jpg').resize((800,450)).blur("gaussian" , amount=9)
                        profile = Editor(image_loader).resize((150, 150)).circle_image()
                        text=str(member)
                        if len(text)>30:
                            text = text[:30]
                        else:
                            text = str(member)
                        # For profile to use users profile picture load it from url using the load_image/load_image_async function
                        # profile_image = load_image(str(ctx.author.avatar_url))
                        # profile = Editor(profile_image).resize((150, 150)).circle_image()

                        mc = main_guild.member_count
                        # Fonts
                        poppins = Font.poppins(size=50, variant="bold")
                        poppins_small = Font.poppins(size=25, variant="regular")
                        poppins_light = Font.poppins(size=20, variant="light")
                        if user_title is not None:
                            text2= find['title']
                            text2 = str(text2)
                        else:
                            text2 = member.guild.name
                            text2 = str(text2)
                        
                        if user_message is not None:
                            text3 = str(user_message)
                        else:
                            text3 = 'You are the ' + str(mc) + ' Member'
                        font_size2=poppins.getsize(text=text2)
                        font_size1=poppins_small.getsize(text=text)
                        font_size0=poppins_small.getsize(text=text3)

                        pluster3 = 400-(font_size2[0] / 2)
                        pluster2 = 400-(font_size1[0] / 2)
                        pluster1 = 400-(font_size0[0] / 2)

                        background.paste(profile, (325, 90))
                        background.ellipse((325, 90), 150, 150, outline="gold", stroke_width=4)
                        background.text((pluster3, 260), text=text2, color="white", font=poppins)
                        background.text(
                            (pluster2, 325), text=text, color="white", font=poppins_small
                        )
                        background.text(
                            (pluster1, 360),
                            text=text3,
                            color="#0BE7F5",
                            font=poppins_small)
                            
                        file = discord.File(fp=background.image_bytes, filename='circle.png')
                        if channel_send is not None and exist_check is not None:
                            await exist_check.send(file=file)
        except:
            pass

        if (find:= logerr.find_one({"user_id":member.guild.id , 'auto_log_creator':True})):
            tmp_guild = find['user_id']
            tmp_id_channel= find['member_join_state']
            main_guild=self.bot.get_guild(tmp_guild)
            webhooker_id = find['member_join_webhook']
            webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
            if webhooker is not None:
                embed=discord.Embed(
                        title=f"Join Log",
                        timestamp=datetime.now(),
                        color= 0xF6F6F6
                )
                embed.add_field(name=f'ACTION:',value=f'Join Server')
                embed.add_field(name=f'USER:', value=f'{member.mention}')
                embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f'USER ID: {member.id}',icon_url=member.display_avatar.url)
                await webhooker.send(embed=embed)

        if (find:= logerr.find_one({"user_id":member.guild.id , 'full_log_state':True})):
            tmp_guild = find['user_id']
            tmp_id_channel= find['channel']
            main_guild=self.bot.get_guild(tmp_guild)
            webhooker_id = find['full_log_webhook']
            webhooker = discord.utils.get(await main_guild.webhooks() , id = webhooker_id)
            if webhooker is not None:
                embed=discord.Embed(
                        title=f"Join Log",
                        timestamp=datetime.now(),
                        color= 0xF6F6F6
                )
                embed.add_field(name=f'ACTION:',value=f'Join Server')
                embed.add_field(name=f'USER:', value=f'{member.mention}')
                embed.add_field(name=f'ACCOUNT AGE:' , value=f"{discord.utils.format_dt(member.created_at , 'R')}" )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f'USER ID: {member.id}',icon_url=member.display_avatar.url)
                await webhooker.send(embed=embed)

        return 

    @commands.hybrid_command(name='welcome_enable' , description='Enable welcome Feature')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def welcome_enable(self,ctx):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            welcome_text = f'# welcome to the ' + ctx.guild.name
            if(find:= collection.find_one({"_id":ctx.guild.id})):
                return await ctx.send('# welcome already enabled')

            collection.insert_one({'_id':ctx.guild.id , "channel":None , 'webhook':None , "message" : welcome_text , "title":ctx.guild.name , "style":None , 'color':None , 'embed_text':None})
            await ctx.send("# Welcome Feature Enabled successfully ")
        except:
            await ctx.send('# something went wrong pls try again')
        
        return

    @commands.hybrid_command(name='welcome_disable' , description='disable welcome Feature and delete all of your config')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def welcome_disable(self,ctx):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            if not (find:= collection.find_one({"_id":ctx.guild.id})):
                return await ctx.send('# Welcome Feature its already disable')


            collection.delete_one({'_id':ctx.guild.id})
            await ctx.send("# welcome Feature disabled successfully if you enable this feature you must config it again")
        
        except:
            await ctx.send('# something went wrong pls try agian')
        
        return
    
    @commands.hybrid_command(name='welcome_channel_set' , description='set a text channel for welcome')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 3600.0, key=lambda i: (i.guild.id))
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def welcome_channel_set(self,ctx , channel:discord.TextChannel):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        await ctx.defer()
        try:
            if not(find:= collection.find_one({"_id":ctx.guild.id})):
                return await ctx.send('# Welcome Feature is disable')

            member1 = discord.utils.get(ctx.guild.members , id = ctx.guild.me.id)
            webhook_avatar =member1.display_avatar
            profile_webhook= await webhook_avatar.read()

            find= collection.find_one({"_id":ctx.guild.id})
            webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
            webhook_check = find['webhook']
            if webhook_check is not None:
                exist_check = discord.utils.get(await ctx.guild.webhooks() , id = webhook_check)
                if exist_check is not None:
                    await exist_check.edit(channel=webhook_channel_set)
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel':channel.id}} )
                    await ctx.send('# welcome channel set successfully')
                else:
                    webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                    await webhooker.edit(channel=webhook_channel_set)
                    collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel':channel.id , 'webhook':webhooker.id}} )
                    await ctx.send('# welcome channel set successfully')
            else:
                webhooker=await channel.create_webhook(name='APA BOT' , avatar=profile_webhook)
                await webhooker.edit(channel=webhook_channel_set)
                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel':channel.id , 'webhook':webhooker.id}} )
                await ctx.send('# welcome channel set successfully')


            

        # webhook_channel_set=discord.Object(channel.id , type='abc.Snowflake')
        # #################webhook setting##########################

        except:
            await ctx.send('# something went wrong pls try again')

        return
    @commands.hybrid_command(name='welcome_channel_remove' , description='remove welcome channel')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def welcome_channel_remove(self,ctx ):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            if not(find:= collection.find_one({"_id":ctx.guild.id})):
                return await ctx.send('# Welcome Feature is disable')

            collection.update_one({'_id':ctx.guild.id} ,{'$set':{'channel':None}} )
            await ctx.send('# welcome channel removed successfully\nthe webhook wont delete and its do nothing so dont worry its not a bug')   
        except:
            await ctx.send('# something went wrong pls try again')       

        return      

    @commands.hybrid_command(name='reset_welcome_config' , description='its will reset titile and message to default one')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def reset_welcome_config(self,ctx):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            if (find:= collection.find_one({"_id":ctx.guild.id})):
                collection.update_one({'_id':ctx.guild.id} ,{'$set':{'message':None , 'title':None}} )
                await ctx.send('# message and title reset to default one successfully')
               
        except:
            return await ctx.send('# something went wrong')

        return

    @commands.hybrid_command(name='welcome_config' , description='set message and title and style of welcome message')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @app_commands.describe(
        message='welcome message | /n = newline(only for embed) | @user_mention = mention user',
        color='its will only affect on embed style',
    )
    @app_commands.choices(style=[
        app_commands.Choice(name='Embed Style' , value=1),
        app_commands.Choice(name='Card Style' , value=2)
    ])
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild.id))
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
    async def welcome_message_set(self,ctx , *,message:Optional[Union[str , str]],title:Optional[Union[str,str]],style:app_commands.Choice[int] , color:app_commands.Choice[int]):
        if ctx.guild.me.top_role.position > ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send('# your role is not above me then you cant use this command' , ephemeral=True)
        try:
            if not(find:= collection.find_one({"_id":ctx.guild.id})):
                return await ctx.send('# Welcome Feature is disable')
        except:
            return await ctx.send('# something went wrong')
        try:
            tmp_color = 0xFFFFFF
            if style.value ==2:
                if message is not None:
                    if len(message)>50: 
                        return await ctx.send('# use maximum 50 characters for message in card style | you must do the config again')
                if title is not None:
                    if len(title)>25:
                        return await ctx.send('# use maximum 25 characters for title in card style | you must do the config again')

            elif style.value ==1:
                if title is not None:
                    if len(title) > 200:
                        await ctx.send('# use maximum 200 chracters for embed style')
                        return
                if message is not None:
                    if len(message) >950:
                        await ctx.send('# use maximum 950 chracters for embed style')
                        return


            final_text:str= ''
            if message is not None:
                final_text:str= ''
                message_spliter = list(message.split('/n'))
                for i in range(len(message_spliter)):
                    if i != len(message_spliter)-1:
                        final_text += f'{message_spliter[i]}\n'
                    else:
                        final_text += f'{message_spliter[i]}'
            else:
                final_text=message
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

            collection.update_one({'_id':ctx.guild.id} ,{'$set':{'message':message}} )
            collection.update_one({'_id':ctx.guild.id} ,{'$set':{'title':title}} )
            collection.update_one({'_id':ctx.guild.id} ,{'$set':{'style':style.value}} )
            collection.update_one({'_id':ctx.guild.id} ,{'$set':{'color':tmp_color}} )
            collection.update_one({'_id':ctx.guild.id} ,{'$set':{'embed_text':final_text}} )


            await ctx.send('# welcome settings set successfully')                
        except:
            await ctx.send('# something went wrong pls try again')
        

        return



async def setup(bot : Bot):
    await bot.add_cog(welcome(bot))