import discord
from discord.ext import commands
import json

# command prefix
bot = commands.Bot(command_prefix=',')
bot.remove_command('help')

# check for a specific channel
def check_channel(ctx, channel):
    if str(ctx.message.channel) == channel:
        return True
    else:
        return False

# check author role
def check_role(ctx, roles):
    for role in roles:
        if str(discord.utils.get(ctx.author.roles, name=role)) == role:
            return True
    return False

# check user role
def check_role_user(user, roles):
    for role in roles:
        if str(discord.utils.get(user.roles, name=role)) == role:
            return True
    return Flase

# when bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=",help"))
    print('Bot Ready!!')

# error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        emb = discord.Embed(
            title='Command Not Found',
            description='404, Not Found\nRun `,help` to list all commands.',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Error',
            description='An unknown error occured\nPlease refer to `,help`\nor cantact admins',
            color=1040190
        )
        await ctx.send(embed=emb)

# check the latency of the bot
@bot.command()
async def ping(ctx):
    emb = discord.Embed(
        title='Ping',
        description=f'{round(bot.latency*1000)} ms',
        color=1040190
    )
    await ctx.send(embed=emb)

# to clear some ammount of messages
@bot.command()
async def clear(ctx,amount=1):
    allowed_roles = ['admins', 'heads', 'sensei']
    if check_role(ctx, allowed_roles):
        await ctx.channel.purge(limit=amount)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='Inappropriate Role !! :(',
            color=1040190
        )
        await ctx.send(embed=emb)

# generate an invite
@bot.command()
async def invite(ctx, age, uses):
    allowed_roles = ['sensei', 'heads', 'admins']
    if check_role(ctx, allowed_roles):
        link = await ctx.channel.create_invite(max_age=int(age), max_uses=int(uses), reason='')
        emb = discord.Embed(
            title='Link Created',
            description=f'Max Age: {age}\nMax Uses: {uses}\nLink: {link}',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='Inappropriate Channel !! :(',
            color=1040190
        )
        await ctx.send(embed=emb)

# kick a member
@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, user: discord.Member, reason='No reason specified !!!'):
    allowed_roles = ['sensei', 'heads', 'admins']
    if check_role(ctx, allowed_roles):
        await user.kick(reason=reason)
        emb = discord.Embed(
            title='User Kicked',
            description=f'{user.mention} kicked\nBy: {ctx.message.author.mention}\nReason: {reason}',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='You are not allowed to use this command.',
            color=1040190
        )
        await ctx.send(embed=emb)

# to report a member
@bot.command()
async def report(ctx, user: discord.Member, reason):
    channel_id = discord.utils.get(ctx.guild.channels, name='reports').id
    channel = bot.get_channel(channel_id)
    emb = discord.Embed(
        title='Report',
        color=1040190
    )
    emb.add_field(name='By', value=ctx.message.author.mention, inline=False)
    emb.add_field(name='To', value=user.mention, inline=False)
    emb.add_field(name='Reason', value=reason, inline=False)
    await channel.send(embed=emb)
    emb = discord.Embed(
        title='Successful',
        description='The user was reported successfully.',
        color=1040190
    )
    await ctx.send(embed=emb)

# to give roles to members
@bot.command()
async def grole(ctx, user: discord.Member, role: discord.Role):
    allowed_roles = ['admins', 'heads', 'sensei']
    if check_role(ctx, allowed_roles):
        await user.add_roles(role)
        emb = discord.Embed(
            title='Role Given',
            description=f'User {user.mention} is added to the role {role.mention}',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='You are not allowed to use this command.',
            color=1040190
        )
        await ctx.send(embed=emb)

# to remove roles from members
@bot.command()
async def rrole(ctx, user: discord.Member, role: discord.Role):
    allowed_roles = ['admins', 'heads', 'sensei']
    if check_role(ctx, allowed_roles):
        await user.remove_roles(role)
        emb = discord.Embed(
            title='Role Removed',
            description=f'Role {role.mention} removed from user {user.mention}',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='You are not allowed to use this command.',
            color=1040190
        )
        await ctx.send(embed=emb)

# to kick all members of a role
@commands.has_permissions(kick_members=True)
@bot.command()
async def kick_all(ctx, role: discord.Role):
    allowed_roles = ['admins', 'heads', 'sensei']
    if check_role(ctx, allowed_roles):
        for member in ctx.guild.members:
            if role in member.roles:
                await ctx.guild.kick(member, reason='')
        emb = discord.Embed(
            title='All members kicked',
            description=f'All members of role {role.mention} kicked.',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='You are not allowed to use this command.',
            color=1040190
        )
        await ctx.send(embed=emb)

# add an event
@bot.command()
async def add_event(ctx, name):
    allowed_roles = ['admins', 'heads', 'sensei']
    if check_role(ctx, allowed_roles):
        f = open('events.json', 'r')
        events = json.load(f)
        f.close()
        event = {events.keys()[-1]+1:name}
        events.update(event)
        f = open('events.json', 'w')
        events = json.dumps(events)
        f.write(events)
        f.close()
        emb = discord.Embed(
            title='Event Added',
            description=f'Event added successfully.\n`id = {events.keys()[-1]}`',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='You are not allowed to use this command.',
            color=1040190
        )
        await ctx.send(embed=emb)

# remove an event
@bot.command()
async def rem_event(ctx, id):
    allowed_roles = ['admins', 'heads', 'sensei']
    if check_role(ctx, allowed_roles):
        id = int(id)
        f = open('events.json', 'r')
        events = json.load(f)
        f.close()
        for event in events:
            if events[event] == id:
                del events[event]
        events = json.dumps(events)
        f = open('events.json', 'w')
        f.write(events)
        f.close()
        emb = discord.Embed(
            title='Event Removed',
            description=f'Event removed successfully.\n`id = {events.keys()[-1]}`',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='You are not allowed to use this command.',
            color=1040190
        )
        await ctx.send(embed=emb)

# show all active events
@bot.command()
async def show_events(ctx):
    allowed_roles = ['admins', 'heads', 'sensei', 'core-team']
    if check_role(ctx, allowed_roles):
        emb = discord.Embed(
            title='List of all events',
            color=1040190
        )
        f = open('events.json', 'r')
        events = json.load(f)
        f.close()
        for event in events:
            emb.add_field(name=f'{event}', value=f'{events[event]}')
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='You are not allowed to use this command.',
            color=1040190
        )
        await ctx.send(embed=emb)

# help command 
@bot.command(name='help')
async def _help(ctx):
    emb = discord.Embed(
        title='List Of Commands',
        color=1040190
    )
    channel = discord.ChannelType
    emb.add_field(name='1. `,help`', value='Display this help message.', inline=False)
    emb.add_field(name='2. `,ping`', value='A command that shows the latency of the bot.', inline=False)
    emb.add_field(name='3. `,clear`', value='A command to clear messages.\nUsage: `,clear <amount>(including this line)`', inline=False)
    emb.add_field(name='4. `,invite`', value='A command to create an invite.\nUsage: `,invite <AGE>(In seconds) <USES>(In integer)`', inline=False)
    emb.add_field(name='5. `,kick`', value='A command to kick a member.\nUsage: `,kick <mention member>`', inline=False)
    emb.add_field(name='6. `,report`', value='A command to report a member.\nUsage: `,report <mention member> <reason>`', inline=False)
    emb.add_field(name='7. `,grole`', value='Give a role to a member.\nUsage: `,grole <mention member> <mention role>`', inline=False)
    emb.add_field(name='8. `,rrole`', value='Remove a role from a member.\nUsage: `,rrole <mention member> <mention role>`', inline=False)
    emb.add_field(name='9. `,kick_all`', value='Kick all members of a role\nUsage: `,kick_all <mention role>`', inline=False)
    await ctx.send(embed=emb)

# test command
@bot.command()
async def test(ctx, user: discord.Member):
    await ctx.send(f'{str(discord.utils.get(user.roles, name="admins"))}')

if __name__ == '__main__':
    f = open('token', 'r')
    token = f.read()
    f.close()
    bot.run(token)
