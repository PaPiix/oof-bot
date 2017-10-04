#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import asyncio
import sys
import os
from discord.ext import commands
from datetime import datetime
import discord.ext.commands.errors as err

bot = commands.Bot(command_prefix='oof ')
bot.remove_command('help')
token = 'MzYyMzUwMzMzNjQyNTM5MDE4.DKxYjw.1QzpVclbRUvvIEshYXVVjXoCGlg'
token = sys.argv[1] if len(sys.argv) > 1 else token


def log(content, timestamp=True):
    if timestamp is True:
        time = datetime.now()
        time = time.strftime('[%H:%M]: ')
    elif timestamp is False:
        time = '\t '
    elif timestamp is None:
        time = ''

    log = '%s%s' % (time, content)
    print(log)


def is_owner():
    return commands.check(lambda ctx: ctx.message.author == owner)

# message utilities


async def try_del(message: discord.Message):
    try:
        await bot.delete_message(message)
    except:
        pass


async def slp_del(message: discord.Message, slp: int = 2):
    slp = await asyncio.sleep(slp) if slp else slp
    await try_del(message)

# on_event()


@bot.event
async def on_ready():
    global login_time, owner
    await bot.change_presence(game=discord.Game(name='Roblox'))
    owner = await bot.get_user_info('197904839253032961')
    login_time = datetime.now()

    log('Logged in as %s' % bot.user)


@bot.event
async def on_message(message):
    if message.author.id in bot.user.id:
        return

    await bot.process_commands(message)

    if message.channel.is_private:
        return
    if message.server.id == '258233037723140096':
        if message.author.id != '148194601793093632':
            return
    if message.server.id == '264445053596991498':
        return

    for role in message.server.roles:
        if 'unoofable' in role.name:
            if role in message.author.roles:
                return

    await bot.send_message(message.channel, 'oof')
    log('oofed at {0.author} in #{0.channel} ({0.server})'.format(message))


@bot.event
async def on_command_error(exception, ctx):
    if isinstance(exception, err.CommandNotFound):
        return
    raise exception

# owner commands


@is_owner()
@bot.command(pass_context=True)
async def shutdown(ctx, slp: int = 2):
    msg = slp if slp > 1 else 'now'
    msg = 'in %ss' % msg if isinstance(msg, int) else msg

    await try_del(ctx.message)
    sent = await bot.say('logging off %s' % msg)
    await slp_del(sent, 2)
    slp = await asyncio.sleep(slp) if slp > 1 else None

    await bot.logout()
    log('Logged out at %s' % datetime.now().strftime('%H:%M (%B %d)'))

    def etime(t):
        time = (t.seconds//3600) % 60
        mess = '%sh ' % time if time else ''
        time = (t.seconds//60) % 60
        mess += '%smin ' % time
        time = t.seconds % 60
        mess += '%ss' % time if time else ''
        return mess
    log('Been running for %s\n' % etime(datetime.now() - login_time))


@is_owner()
@bot.command(pass_context=True)
async def restart(ctx, slp: int = 1):
    msg = slp if slp > 1 else 'now'
    msg = 'in %ss' % msg if isinstance(msg, int) else msg

    await try_del(ctx.message)
    sent = await bot.say('restarting bot %s' % msg)
    await slp_del(sent, 2)
    slp = await asyncio.sleep(slp) if slp > 1 else None

    log('Restarted bot at %s' % datetime.now().strftime('%H:%M (%B %d)'))

    def etime(t):
        time = (t.seconds//3600) % 60
        mess = '%sh ' % time if time else ''
        time = (t.seconds//60) % 60
        mess += '%smin ' % time
        time = t.seconds % 60
        mess += '%ss' % time if time else ''
        return mess
    log('Been running for %s\n' % etime(datetime.now() - login_time))
    python = sys.executable
    os.execl(python, python, * sys.argv)


@is_owner()
@bot.command(pass_context=True)
async def source(ctx):
    await try_del(ctx.message)
    sent = await bot.send_file(ctx.message.channel, __file__)
    log('Sent source code to {0.author} at {0.channel} ({0.server})'.format(
        ctx.message))
    await slp_del(sent, 10)


# anyone else's commands
@bot.command(pass_context=True)
async def feedback(ctx, *, message: str = None):
    await try_del(ctx.message)
    if not message:
        await try_del(ctx.message)
        sent = await bot.say('no feedback message was passed')
        return await slp_del(sent, 2)
    auth = ctx.message.author
    mess = ctx.message
    message = 'Feedback from %s (%s) at (%s): \n%s' % (
        auth, auth.id, mess.server, message)
    await bot.send_message(owner, message)


@bot.command(pass_context=True)
async def invite(ctx):
    await try_del(ctx.message)
    await bot.say(discord.utils.oauth_url(bot.user.id))


@bot.command(pass_context=True)
async def help(ctx):
    await try_del(ctx.message)

    then = login_time.strftime('%H:%M, %B %d')
    commands = ('feedback', 'help', 'invite')

    def etime(t):
        time = (t.seconds//3600) % 60
        mess = '%sh ' % time if time else ''
        time = (t.seconds//60) % 60
        mess += '%smin ' % time
        time = t.seconds % 60
        mess += '%ss' % time if time else ''
        return mess
    now = etime(datetime.now() - login_time)

    em_1 = discord.Embed(title='')
    em_1.set_author(name='Running bot with %s' % bot.user)
    em_1.set_thumbnail(url=bot.user.avatar_url)
    em_1.set_footer(text='Bot developed by %s.\n' % owner,
                    icon_url=owner.avatar_url)
    em_1.add_field(name='Commands', value=', '.join(commands))
    em_1.add_field(name='Online since', value='%s (%s)' % (then, now))
    em_1.add_field(name='Present in', value='%s servers' % len(bot.servers))

    try:
        em_1.color = ctx.message.server.me.color or discord.Embed.Empty
    except:
        em_1.color = discord.Embed.Empty

    em_2 = discord.Embed(title='')
    em_2.set_author(name='Running bot with %s' % bot.user)
    em_2.set_thumbnail(url=bot.user.avatar_url)
    em_2.set_footer(text='Bot developed by %s.\n' % owner,
                    icon_url=owner.avatar_url)
    em_2.add_field(name='The way oofs work:', value=(
        'The bot will oof anyone who speaks under a channel it ' +
        'can see and speak on, but users with a role by the name' +
        ' of "unfoofable" will be ignored. That\'s basically all ' +
        'there is to this bot, really.'))
    em_2.add_field(name='Have some feedback?', value=(
        'Use the feedback command to tell me things that ' +
        'would make the bot better in any way. But keep ' +
        'any feedback and suggestions being sent only ' +
        'through this command and not my personal discord PMs.'))

    try:
        em_2.color = ctx.message.server.me.color or discord.Embed.Empty
    except:
        em_2.color = discord.Embed.Empty

    sent = await bot.say(embed=em_1)
    used_embed = em_1

    while True:
        ne = '▶' if used_embed is em_1 else '◀'
        await bot.edit_message(sent, embed=used_embed)
        await bot.add_reaction(sent, ne)
        await bot.add_reaction(sent, '↩')

        react = (await bot.wait_for_reaction([ne, '↩'],
                 user=ctx.message.author, timeout=15.0, message=sent))
        if not react:
            return await try_del(sent)
        await bot.clear_reactions(sent)

        react = react[0].emoji
        if used_embed is em_1:
            used_embed = None if react == '↩' else em_2
        elif used_embed is em_2:
            used_embed = None if react == '↩' else em_1

        if not used_embed:
            return await try_del(sent)
        await bot.edit_message(sent, embed=used_embed)

try:
    bot.run(token)
except:
    log('Could not run the bot')
