import asyncio
import json
import os
import random as r
from datetime import datetime, timezone

import colored as c
import discord
from pathlib import Path
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, check
from discord.ext.commands import CheckFailure, check
from discord.ext.commands import MissingPermissions

#define needed variables
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=False)
client = commands.Bot(command_prefix='&', case_insensitive=True, intents=intents)
client.remove_command('help') #Removes the hideous default help command
color = 0x729C69
token = 'Put your bot token here as a string'
administrators = [] #add administrators by their numerical ID as a list of integers
moderators = [] #moderators will be implemented soon
watchlist = [] #add suspiscious users you want to keep an eye on to the watchlist
kick_images = ['https://media2.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif?cid=ecf05e47f9x6cgqirlenqtijv34964komuulz6yq25rxoft4&rid=giphy.gif',
'https://media3.giphy.com/media/eH3OSi9ffKx1wHkkOU/giphy.gif',
'https://media1.giphy.com/media/3o7TKwVQMoQh2At9qU/giphy.gif?cid=ecf05e47b8a8e3d15339319e800d5266201aaedcf84346a3&rid=giphy.gif']

@client.event
async def on_ready():
    print("LAZARUS has successfully risen.")
    print('There are currently {} administrators'.format(len(administrators)))
    print('There are currently {} moderators.'.format(len(moderators)))
    print('There are currently {} users on the watchlist.'.format(len(watchlist)))

#the help command needs to be finished, just a matter of add_field statements
@client.command(aliases=['?', 'helpmenu'])
async def help(ctx, *args):
    embed = discord.Embed(title="LAZARUS HELP MENU", color=color)
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/778843477428535317/1a0575788bcc43fc7e03025d74483e06.png?size=512')
    if len(args) == 0:
        embed.add_field(name="av", value='Usage: `&av [user]`\nDisplays avatar of desired user or yourself.', inline=False)
        embed.add_field(name="av", value='Usage: `&av [user]`\nDisplays avatar of desired user or yourself.', inline=False)

    await ctx.send(embed=embed)

@client.command(aliases=['avatar', 'pfp'])
async def av(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    embed = discord.Embed(title="Avatar", color=color)
    embed.set_author(name=f"{member}", icon_url=f'{member.avatar_url}')
    embed.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embed)

@client.command(name='inv', aliases=['invite', 'invitation'])
async def inv(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(color=color)
    embed.add_field(name="BOT INVITE", value='Click this to invite our bot to your server:\n [***__Click Here__***](https://discord.com/api/oauth2/authorize?client_id=778843477428535317&permissions=470809847&scope=bot)', inline=False)
    await ctx.message.channel.send(embed=embed)

@client.command(aliases=['user'])
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    date_format = "%a , %d %b %Y %I:%M %p"
    join_pos = sorted(ctx.guild.members, key=lambda member: member.joined_at).index(member) + 1
    roles = [role for role in member.roles]
    embed = discord.Embed(timestamp=ctx.message.created_at, color=color)
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)

    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(name="Display Name:", value=member.display_name, inline=False)

    embed.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                    inline=False)

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Highest Role:", value=member.top_role.mention, inline=False)
    embed.set_footer(text=f"Command executed by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

#channel specific lockdown command, only allows elevated permission users talk
@client.command()
@has_permissions(administrator=True)
async def lockdown(ctx, *args):
    if len(args) == 0:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(color=color)
        embed.add_field(name="LOCKDOWN STARTED", value="This channel has been locked down.", inline=False)
        await ctx.send(embed=embed)
@client.command()
@has_permissions(administrator=True)
async def unlock(ctx, *args):
    if len(args) == 0:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(color=color)
        embed.add_field(name="LOCKDOWN ENDED", value="This channel's lockdown has ended.", inline=False)
        await ctx.send(embed=embed)

#gathers basic piblic information about the server the bot is in
@client.command()
async def serverinfo(ctx):
    name = ctx.guild.name
    create_server = ctx.guild.created_at
    owner_server = ctx.guild.owner
    server = ctx.message.guild
    role_count = len(server.roles)
    emoji_count = len(server.emojis)
    channel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

    embed = discord.Embed(timestamp=ctx.message.created_at, color=color)
    embed.set_author(name=str(name), icon_url=ctx.guild.icon_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)

    embed.add_field(name="Owner", value=owner_server, inline=False)
    embed.add_field(name='Region', value=server.region, inline=False)
    embed.add_field(name='Members', value=server.member_count, inline=False)
    embed.add_field(name="Created On", value=create_server.strftime("%a, %#d %B %Y"), inline=False)
    embed.add_field(name='Text Channels', value=str(channel_count), inline=False)
    embed.add_field(name='Number of Roles', value=str(role_count))
    embed.add_field(name='Number of Emotes', value=str(emoji_count))
    embed.set_footer(text=f"Command executed by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#kick commands that attaches 1 of 3 funny gifs when used
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await ctx.guild.kick(member)
    embed = discord.Embed(timestamp=ctx.message.created_at, color=color)
    embed.add_field(name='KICKED!', value=f'User {member} has been kicked.')
    embed.set_image(url=kick_images[r.randint(0,len(kick_images)-1)])
    await ctx.channel.send(embed=embed)

#simple yet effective ban
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.ban(reason=reason)
    ban = discord.Embed(title=f"Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}",
                        color=color)
    await ctx.message.delete()
    await ctx.channel.send(embed=ban)

#users must be unbanned by their numerical ID, since they are no longer in the server
@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, id, reason="No reason provided"):
    try:
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        unban = discord.Embed(title=f"Unbanned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}",color=color)
        await ctx.channel.send(embed=unban)
    except:
        embed = discord.Embed(color=color)
        embed.add_field(name='LAZARUS ERROR', value='User not found, make sure to use their numerical ID.')
        await ctx.channel.send(embed=embed)

#very weak nuke command, can be improved
@client.command()
@has_permissions(ban_members=True)
async def nuke(ctx, total=3):
    await ctx.channel.purge(limit=total)

#this gives all the missing permission errors for elevated permission commands
@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(color=color)
        embed.add_field(name='LAZARUS ERROR', value='You do not have permission to do that.')
        await ctx.send(embed=embed)
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(color=color)
        embed.add_field(name='LAZARUS ERROR', value='You do not have permission to do that.')
        await ctx.send(embed=embed)
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(color=color)
        embed.add_field(name='LAZARUS ERROR', value='You do not have permission to do that.')
        await ctx.send(embed=embed)
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(color=color)
        embed.add_field(name='LAZARUS ERROR', value='You do not have permission to do that.')
        await ctx.send(embed=embed)
@lockdown.error
async def lockdown_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(color=color)
        embed.add_field(name='LAZARUS ERROR', value='You do not have permission to do that.')
        await ctx.send(embed=embed)

#this is the secret administrator command, it can only be used through DMs with your bot
#this command is basically a prefix for important global commands
@client.command()
async def superuser(ctx, *args):
    if not args and administrators.count(ctx.author.id) > 0:
        channel = await ctx.author.create_dm()
        await channel.send("An argument must be provided")
    elif administrators.count(ctx.author.id) > 0:
        if not str(ctx.message.channel) == 'Direct Message with ' + str(ctx.author):
            channel = await ctx.author.create_dm()
            await channel.send("Superuser can only be used via DMs")
        else:
            if args[0] == 'help':
                channel = await ctx.author.create_dm()
                embed = discord.Embed(color=color)
                embed.set_author(name='Lazarus Superuser Help Menu', icon_url=ctx.author.avatar_url)
                embed.add_field(name="status", value=
                ' Usage: `&superuser status [status/list] [text] [url]`\nChanges Lazarus\' current status\nonly use url if status is being set to streaming\nUse _ to represent a space', inline=False)
                embed.add_field(name='watchlist', value='Usage" `&superuser watchlist [add/remove/list] [userID]`\nAdds or removes users from watchlist\nlists them as well', inline=False)
                embed.add_field(name='lookup', value='Usage" `&superuser lookup [userID]`\nRetrieves information about users via ID\nShows username, avatar, badges and creation time', inline=False)
                await channel.send(embed=embed)
            elif args[0] == 'status': #directly change the status of the bot to whatever you please
                channel = await ctx.author.create_dm()
                if len(args) > 1: #this isnt really necessary, but it prevents errors in console
                    if args[1] == 'playing':
                        try:
                            await client.change_presence(activity=discord.Game(name=args[2].replace('_',' ')))
                            await channel.send("Success!")
                            now = datetime.now()
                            ct = now.strftime("%H:%M:%S")
                            print('[SUPERUSER]'+' ['+ct+'] ['+str(ctx.author)+'] '+'Status changed to Playing ' + args[2].replace('_',' '))
                        except:
                            await channel.send("Invalid arguments")
                    elif args[1] == 'streaming':
                        try:
                            await client.change_presence(activity=discord.Streaming(name=args[2].replace('_',' '), url=args[3]))
                            await channel.send("Success!")
                            now = datetime.now()
                            ct = now.strftime("%H:%M:%S")
                            print('[SUPERUSER]'+' ['+ct+'] ['+str(ctx.author)+'] '+'Status changed to Streaming ' + args[2].replace('_',' '))
                        except:
                            await channel.send("Invalid arguments")
                    elif args[1] == 'listening':
                        try:
                            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=args[2].replace('_',' ')))
                            await channel.send("Success!")
                            now = datetime.now()
                            ct = now.strftime("%H:%M:%S")
                            print('[SUPERUSER]'+' ['+ct+'] ['+str(ctx.author)+'] '+'Status changed to Listening to ' + args[2].replace('_',' '))
                        except:
                            await channel.send("Invalid arguments")
                    elif args[1] == 'watching':
                        try:
                            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=args[2].replace('_',' ')))
                            await channel.send("Success!")
                            now = datetime.now()
                            ct = now.strftime("%H:%M:%S")
                            print('[SUPERUSER]'+' ['+ct+'] ['+str(ctx.author)+'] '+'Status changed to Watching ' + args[2].replace('_',' '))
                        except:
                            await channel.send("Invalid arguments")
                    elif args[1] == 'list':
                        await channel.send("`playing`\n`listening`\n`watching`\n`streaming`")
            elif args[0] == 'watchlist': #temporarily adds a user ot removes a user from the watchlist
                channel = await ctx.author.create_dm()
                if len(args) > 1:
                    now = datetime.now()
                    ct = now.strftime("%H:%M:%S")
                    if args[1] == 'add':
                        watchlist.append(int(args[2]))
                        await channel.send("User ID " + str(args[2]) + ' added.')
                        print('[SUPERUSER]'+' ['+ct+'] ['+str(ctx.author)+'] '+'Added user ID ' +str(args[2])+' to Watchlist.')
                    elif args[1] == 'remove':
                        t = watchlist.index(str(args[2]))
                        watchlist.pop(t)
                        await channel.send("User ID " + str(args[2]) + ' removed.')
                        print('[SUPERUSER]'+' ['+ct+'] ['+str(ctx.author)+'] '+'Removed user ID ' +str(args[2])+' from Watchlist.')
                    elif args[1] == 'list':
                        t = ''
                        for i in range(0, len(watchlist)):
                            t += '`'+str(watchlist[i])
                            t += '` '
                        await channel.send('Watchlist: ' + t)
            elif args[0] == 'lookup': #performs a discord api request that can only be made by bots to find info through an ID
                channel = await ctx.author.create_dm()
                user = await client.fetch_user(args[1])
                embed = discord.Embed(timestamp=ctx.message.created_at, color=color)
                embed.set_author(name=user.name, icon_url=user.avatar_url)
                embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name="Username", value=user.name+'#'+user.discriminator, inline=False)
                embed.add_field(name="Badges", value=user.public_flags.all(), inline=False)
                embed.add_field(name="Joined", value=user.created_at, inline=False)
                await ctx.channel.send(embed=embed)
                now = datetime.now()
                ct = now.strftime("%H:%M:%S")
                print('[SUPERUSER]'+' ['+ct+'] ['+str(ctx.author)+'] '+'Performed an API Lookup.')

#log the messages of a watchlisted user
@client.event
async def on_message(message):
    if watchlist.count(message.author.id) > 0:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('[WATCHLIST] ['+current_time+'] ['+str(message.author)+'] ['+str(message.guild)+'] '+str(message.content))
    await client.process_commands(message)

client.run(token, bot=True)
